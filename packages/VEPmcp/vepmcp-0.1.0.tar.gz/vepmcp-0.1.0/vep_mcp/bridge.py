"""
Bridge module for VEPmcp - VEP API client implementation.
"""

import asyncio
import logging
import re
import time
from typing import Any, Dict, List, Optional, cast
from urllib.parse import urlencode
from dataclasses import dataclass
import aiohttp

# Configure logging
logger = logging.getLogger("vep-mcp")

# Ensembl REST API base URLs
VEP_BASE_URL = "https://rest.ensembl.org/vep"
ENSEMBL_BASE_URL = "https://rest.ensembl.org"

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 15  # requests per second
RATE_LIMIT_WINDOW = 1.0  # time window in seconds


@dataclass
class Config:
    """Configuration for VEPmcp."""

    vep_base_url: str = VEP_BASE_URL
    ensembl_base_url: str = ENSEMBL_BASE_URL
    timeout: float = 30.0
    rate_limit_requests: int = RATE_LIMIT_REQUESTS
    rate_limit_window: float = RATE_LIMIT_WINDOW


class RateLimiter:
    """Rate limiter for Ensembl API requests (15 requests/second)"""

    def __init__(
        self,
        max_requests: int = RATE_LIMIT_REQUESTS,
        window: float = RATE_LIMIT_WINDOW,
    ):
        self.max_requests = max_requests
        self.window = window
        self.requests: List[float] = []

    async def acquire(self) -> None:
        """Acquire a rate limit slot, waiting if necessary"""
        now = time.time()

        # Remove requests outside the current window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.window]

        # If we're at the limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            if sleep_time > 0:
                logger.debug(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
                await asyncio.sleep(sleep_time)
                await self.acquire()  # Recursive call after sleeping
                return

        # Add this request to the list
        self.requests.append(now)


class VEPValidator:
    """Validator for VEP input parameters"""

    @staticmethod
    def validate_species(species: str) -> str:
        """Validate and normalize species name"""
        if not species:
            raise ValueError("Species cannot be empty")

        # Convert to lowercase and replace spaces with underscores
        normalized = species.lower().replace(" ", "_")

        # Basic validation - should contain only letters, numbers, and underscores
        if not re.match(r"^[a-z0-9_]+$", normalized):
            raise ValueError(f"Invalid species format: {species}")

        return normalized

    @staticmethod
    def validate_hgvs_notation(hgvs: str) -> str:
        """Validate HGVS notation format including SPDI"""
        if not hgvs:
            raise ValueError("HGVS notation cannot be empty")

        # HGVS patterns: coding/genomic/protein substitutions, indels, duplications, rs IDs, and SPDI
        patterns = [
            # Traditional HGVS patterns
            r"^[A-Za-z0-9_.]+:[cgmnpr]\.\d+[ACGT]>[ACGT]$",  # Substitution, e.g., ENST..:c.803C>T
            r"^[A-Za-z0-9_.]+:[cgmnpr]\.\d+_\d+del(?:[ACGT]+)?$",  # Deletion, e.g., c.1431_1433del or delTTC
            r"^[A-Za-z0-9_.]+:[cgmnpr]\.\d+_\d+ins[ACGT]+$",  # Insertion, e.g., insATG
            r"^[A-Za-z0-9_.]+:[cgmnpr]\.\d+_\d+dup(?:[ACGT]+)?$",  # Duplication, e.g., dup or dupTTC
            r"^[A-Za-z0-9_.]+:p\.[A-Z][a-z]{2}\d+[A-Z][a-z]{2}$",  # Protein, e.g., p.Tyr124Cys
            r"^[A-Za-z0-9_.]+:p\.[A-Z][a-z]{2}\d+\*$",  # Stop codon, e.g., p.Gln137Ter or p.Gln137*
            # Genomic coordinate patterns (simplified HGVS)
            r"^(?:\d+|X|Y|MT):g\.\d+[ACGT]>[ACGT]$",  # Genomic substitution, e.g., 17:g.41276107A>C
            r"^(?:\d+|X|Y|MT):g\.\d+_\d+del(?:[ACGT]+)?$",  # Genomic deletion
            r"^(?:\d+|X|Y|MT):g\.\d+_\d+ins[ACGT]+$",  # Genomic insertion
            # SPDI notation (Sequence:Position:Deletion:Insertion)
            r"^[A-Za-z0-9_.]+:\d+:[ACGT]*:[ACGT]*$",  # SPDI format, e.g., NC_000016.10:68684738:G:A
            r"^(?:\d+|X|Y|MT):\d+:\d*:[ACGT]*$",  # Simplified SPDI with chromosome, e.g., 16:68684738:2:AC
            # Variant IDs
            r"^rs\d+$",  # dbSNP ID
        ]

        if not any(re.match(pattern, hgvs, re.IGNORECASE) for pattern in patterns):
            raise ValueError(f"Invalid HGVS notation: {hgvs}")

        return hgvs

    @staticmethod
    def validate_variant_id(variant_id: str) -> str:
        """Validate variant identifier (e.g., rs number)"""
        if not variant_id:
            raise ValueError("Variant ID cannot be empty")

        # Common variant ID patterns
        patterns = [
            r"^rs\d+$",  # dbSNP rs number
            r"^COSM\d+$",  # COSMIC ID
            r"^COSV\d+$",  # COSMIC structural variant
            r"^CM\d+$",  # ClinVar
        ]

        if not any(re.match(pattern, variant_id, re.IGNORECASE) for pattern in patterns):
            logger.warning(f"Variant ID format may be unusual: {variant_id}")

        return variant_id

    @staticmethod
    def validate_genomic_region(region: str) -> str:
        """
        Validate genomic region format for VEP API.

        Supported formats for single region queries:
        - chr:pos (e.g., "17:41276107")
        - chr:start-end (e.g., "17:41276106-41276107")
        - chr:pos:ref/alt (e.g., "17:41276107:A/C")

        Supported formats for BATCH processing:
        - VCF format: "CHR POS ID REF ALT" (e.g., "1 230710048 . A G")
          This is the REQUIRED format for vep_region_batch!
        - SPDI format: "CHR:POS:DEL:INS" (e.g., "17:41276106::T")

        IMPORTANT: The colon-separated format (chr:pos:ref/alt) does NOT work for batch
        processing. You MUST use space-separated VCF format for batch operations.
        """
        if not region:
            raise ValueError("Genomic region cannot be empty")

        # Patterns for region formats that work with VEP API
        patterns = [
            # Single position formats (for GET requests)
            r"^(?:\d+|X|Y|MT):\d+$",  # chr:pos, e.g., 1:230710048
            r"^(?:\d+|X|Y|MT):\d+-\d+$",  # chr:start-end, e.g., 1:1000-2000
            r"^(?:\d+|X|Y|MT):\d+:[ACGT]/[ACGT]$",  # chr:pos:ref/alt, e.g., 1:230710048:A/G
            r"^(?:\d+|X|Y|MT):\d+-\d+:[ACGT]/[ACGT]$",  # chr:start-end:ref/alt
            r"^(?:\d+|X|Y|MT):\d+:[ACGT-]+/[ACGT-]+$",  # chr:pos:ref/alt with indels
            # VCF format for POST batch requests - REQUIRED FORMAT FOR BATCH
            r"^(?:\d+|X|Y|MT)\s+\d+\s+[.\w-]+\s+[ACGT-]+\s+[ACGT-]+(?:\s+.*)?$",  # VCF: CHR POS ID REF ALT
            # SPDI notation formats
            r"^[A-Za-z0-9_.]+:\d+:[ACGT]*:[ACGT]*$",  # Full SPDI format, e.g., NC_000016.10:68684738:G:A
            r"^(?:\d+|X|Y|MT):\d+:[ACGT]*:[ACGT]+$",  # SPDI with chromosome, e.g., 17:41276106::T
            r"^(?:\d+|X|Y|MT):\d+:\d+:[ACGT]+$",  # SPDI with numeric deletion length
        ]

        if not any(re.match(pattern, region, re.IGNORECASE) for pattern in patterns):
            raise ValueError(
                f"Invalid genomic region format: {region}. "
                f"For batch operations, use VCF format: 'CHR POS ID REF ALT' (e.g., '1 230710048 . A G')"
            )

        return region

    @staticmethod
    def validate_batch_size(items: List[str], max_size: int = 1000) -> List[str]:
        """Validate batch size doesn't exceed limits"""
        if len(items) > max_size:
            raise ValueError(f"Batch size {len(items)} exceeds maximum of {max_size}")

        if not items:
            raise ValueError("Batch cannot be empty")

        return items


class Bridge:
    """
    Main bridge class for VEPmcp - Client for interacting with Ensembl VEP REST API.

    This class provides the main interface for interacting with the VEP API.
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """
        Initialize the bridge.

        Args:
            config: Configuration object. If None, uses default configuration.
        """
        self.config = config or Config()
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = RateLimiter(
            self.config.rate_limit_requests, self.config.rate_limit_window
        )
        self.validator = VEPValidator()

    async def __aenter__(self) -> "Bridge":
        self.session = aiohttp.ClientSession(
            headers={"Content-Type": "application/json"},
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session:
            await self.session.close()

    async def _make_request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting"""
        if not self.session:
            raise RuntimeError("Bridge session not initialized")

        # Apply rate limiting
        await self.rate_limiter.acquire()

        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 429:
                    # Rate limit exceeded - back off more aggressively
                    backoff_time = 2.0
                    logger.warning(f"Rate limit exceeded, backing off for {backoff_time}s")
                    await asyncio.sleep(backoff_time)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=429,
                        message="Rate limit exceeded",
                    )
                elif response.status >= 400:
                    error_text = await response.text()
                    logger.error(f"HTTP {response.status} error: {error_text}")
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP {response.status}: {error_text}",
                    )

                return cast(Dict[str, Any], await response.json())
        except Exception as e:
            logger.error(f"Request failed: {method} {url} - {str(e)}")
            raise

    def _build_query_params(self, **options: Any) -> str:
        """Build query parameter string for VEP requests with comprehensive parameter support"""
        params: Dict[str, str] = {}

        # Core VEP boolean parameters
        boolean_params = [
            "canonical",  # Only canonical transcripts
            "hgvs",  # HGVS nomenclature
            "domains",  # Protein domains
            "ccds",  # CCDS transcripts
            "protein",  # Protein sequences
            "numbers",  # Include sequence numbers
            "minimal",  # Minimal output
            "variant_class",  # Variant class
            "tsl",  # Transcript support level
            "appris",  # APPRIS annotations
            "mane",  # MANE transcripts
            "uniprot",  # UniProt IDs
        ]

        # Pathogenicity prediction tools
        pathogenicity_params = [
            "AlphaMissense",  # AlphaMissense pathogenicity
            "CADD",  # CADD deleteriousness scores
            "REVEL",  # REVEL pathogenicity scores
            "ClinPred",  # ClinPred pathogenicity
        ]

        # Conservation and functional scores
        conservation_params = [
            "Conservation",  # Conservation scores
            "Blosum62",  # BLOSUM62 substitution scores
        ]

        # Functional annotation parameters
        functional_params = [
            "GO",  # Gene Ontology terms
            "Phenotypes",  # Phenotype data
            "LoF",  # Loss of function predictions
        ]

        # Process all boolean parameters
        all_boolean_params = (
            boolean_params + pathogenicity_params + conservation_params + functional_params
        )
        for param in all_boolean_params:
            if options.get(param):
                params[param] = "1"

        # Integer parameters with validation
        integer_params = {
            "distance": (0, 5000000),  # Distance for regulatory features (0-5MB)
            "SpliceAI": (0, 1),  # SpliceAI score threshold (0-1)
        }

        for param, (min_val, max_val) in integer_params.items():
            if param in options:
                value = int(options[param])
                if not (min_val <= value <= max_val):
                    raise ValueError(f"{param} must be between {min_val} and {max_val}")
                params[param] = str(value)

        # String parameters with validation
        string_params = {
            "pick_order": [
                "mane",
                "canonical",
                "appris",
                "tsl",
                "biotype",
                "ccds",
                "rank",
                "length",
            ],
            "transcript_id": None,  # No specific validation
            "dbNSFP": None,  # No specific validation
        }

        for param, valid_values in string_params.items():
            if param in options:
                value = options[param]
                if valid_values and value not in valid_values:
                    raise ValueError(f"{param} must be one of: {', '.join(valid_values)}")
                params[param] = value

        return urlencode(params) if params else ""

    # VEP HGVS Endpoints
    async def vep_hgvs_single(
        self,
        species: str,
        hgvs_notation: str,
        **options: Any,
    ) -> Dict[str, Any]:
        """GET vep/{species}/hgvs/{hgvs_notation} - Single HGVS annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        hgvs_notation = self.validator.validate_hgvs_notation(hgvs_notation)

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/hgvs/{hgvs_notation}"
        if query_params:
            url += f"?{query_params}"

        return await self._make_request("GET", url)

    async def vep_hgvs_batch(
        self, species: str, hgvs_notations: List[str], **options: Any
    ) -> Dict[str, Any]:
        """POST vep/{species}/hgvs - Batch HGVS annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        hgvs_notations = self.validator.validate_batch_size(hgvs_notations)

        # Validate each HGVS notation
        validated_hgvs = [self.validator.validate_hgvs_notation(hgvs) for hgvs in hgvs_notations]

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/hgvs"
        if query_params:
            url += f"?{query_params}"

        payload = {"hgvs_notations": validated_hgvs}
        return await self._make_request("POST", url, json=payload)

    # VEP ID Endpoints
    async def vep_id_single(
        self,
        species: str,
        variant_id: str,
        **options: Any,
    ) -> Dict[str, Any]:
        """GET vep/{species}/id/{id} - Single variant ID annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        variant_id = self.validator.validate_variant_id(variant_id)

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/id/{variant_id}"
        if query_params:
            url += f"?{query_params}"

        return await self._make_request("GET", url)

    async def vep_id_batch(
        self,
        species: str,
        variant_ids: List[str],
        **options: Any,
    ) -> Dict[str, Any]:
        """POST vep/{species}/id - Batch variant ID annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        variant_ids = self.validator.validate_batch_size(variant_ids)

        # Validate each variant ID
        validated_ids = [self.validator.validate_variant_id(vid) for vid in variant_ids]

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/id"
        if query_params:
            url += f"?{query_params}"

        payload = {"ids": validated_ids}
        return await self._make_request("POST", url, json=payload)

    # VEP Region Endpoints
    async def vep_region_single(
        self, species: str, region: str, allele: str, **options: Any
    ) -> Dict[str, Any]:
        """GET vep/{species}/region/{region}/{allele}/ - Single region annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        region = self.validator.validate_genomic_region(region)

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/region/{region}/{allele}/"
        if query_params:
            url += f"?{query_params}"

        return await self._make_request("GET", url)

    async def vep_region_batch(
        self, species: str, regions: List[str], **options: Any
    ) -> Dict[str, Any]:
        """POST vep/{species}/region - Batch region annotation"""
        # Validate inputs
        species = self.validator.validate_species(species)
        regions = self.validator.validate_batch_size(regions)

        # Validate each region
        validated_regions = [self.validator.validate_genomic_region(region) for region in regions]

        query_params = self._build_query_params(**options)
        url = f"{self.config.vep_base_url}/{species}/region"
        if query_params:
            url += f"?{query_params}"

        payload = {"variants": validated_regions}
        return await self._make_request("POST", url, json=payload)

    # Other Endpoints
    async def get_vep_species(self) -> Dict[str, Any]:
        """GET /info/species - Get available VEP species"""
        url = f"{self.config.ensembl_base_url}/info/species"
        return await self._make_request("GET", url)

    async def get_consequence_types(self) -> Dict[str, Any]:
        """GET /info/variation/consequence_types - Get available consequence types"""
        url = f"{self.config.ensembl_base_url}/info/variation/consequence_types"
        return await self._make_request("GET", url)

    async def get_assembly_info(self, species: str) -> Dict[str, Any]:
        """GET /info/assembly/{species} - Get genome assembly information for a species"""
        species = self.validator.validate_species(species)
        url = f"{self.config.ensembl_base_url}/info/assembly/{species}"
        return await self._make_request("GET", url)
