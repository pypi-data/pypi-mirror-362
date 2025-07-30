"""
MCP Server implementation for VEPmcp.
"""

import json
import sys
import logging
from typing import Any, Dict, Optional

from .bridge import Bridge

# Configure logging
logger = logging.getLogger("vep-mcp")


class MCPServer:
    """MCP Server for VEPmcp."""

    def __init__(self) -> None:
        """Initialize the MCP server."""
        self.bridge = Bridge()
        self.request_id = 0

    def send_response(self, result: Any, error: Optional[str] = None) -> None:
        """Send a JSON-RPC response."""
        response = {
            "jsonrpc": "2.0",
            "id": self.request_id,
        }

        if error:
            response["error"] = {"code": -1, "message": error}
        else:
            response["result"] = result

        print(json.dumps(response))
        sys.stdout.flush()

    async def handle_request(self, request: Dict[str, Any]) -> None:
        """Handle a JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        self.request_id = request.get("id", 0)

        try:
            if method == "initialize":
                self.handle_initialize(params)
            elif method == "tools/list":
                self.handle_list_tools()
            elif method == "tools/call":
                await self.handle_call_tool(params)
            else:
                self.send_response(None, f"Unknown method: {method}")
        except Exception as e:
            logger.error(f"Error handling request {method}: {str(e)}")
            self.send_response(None, str(e))

    def handle_list_tools(self) -> None:
        """Handle tools/list request."""
        # Common VEP parameter schema for reuse
        common_vep_params = {
            # Core annotation options
            "canonical": {
                "type": "boolean",
                "description": "Include only canonical transcripts per gene",
                "default": False,
            },
            "hgvs": {
                "type": "boolean",
                "description": "Include HGVS nomenclature",
                "default": False,
            },
            "domains": {
                "type": "boolean",
                "description": "Include protein domain information",
                "default": False,
            },
            "ccds": {
                "type": "boolean",
                "description": "Include CCDS transcript identifiers",
                "default": False,
            },
            "protein": {
                "type": "boolean",
                "description": "Include protein sequence identifiers",
                "default": False,
            },
            # Pathogenicity predictors
            "AlphaMissense": {
                "type": "boolean",
                "description": "Include AlphaMissense pathogenicity scores",
                "default": False,
            },
            "CADD": {
                "type": "boolean",
                "description": "Include CADD deleteriousness scores",
                "default": False,
            },
            "REVEL": {
                "type": "boolean",
                "description": "Include REVEL pathogenicity scores",
                "default": False,
            },
            "ClinPred": {
                "type": "boolean",
                "description": "Include ClinPred pathogenicity predictions",
                "default": False,
            },
            # Conservation scores
            "Conservation": {
                "type": "boolean",
                "description": "Include conservation scores",
                "default": False,
            },
            "Blosum62": {
                "type": "boolean",
                "description": "Include BLOSUM62 substitution scores",
                "default": False,
            },
            # Functional annotations
            "GO": {
                "type": "boolean",
                "description": "Include Gene Ontology annotations",
                "default": False,
            },
            "Phenotypes": {
                "type": "boolean",
                "description": "Include phenotype data",
                "default": False,
            },
            # Advanced options
            "tsl": {
                "type": "boolean",
                "description": "Include transcript support level",
                "default": False,
            },
            "appris": {
                "type": "boolean",
                "description": "Include APPRIS annotations",
                "default": False,
            },
            "mane": {
                "type": "boolean",
                "description": "Include MANE transcript annotations",
                "default": False,
            },
            "distance": {
                "type": "integer",
                "description": "Distance for regulatory features (bp, 0-5000000)",
                "minimum": 0,
                "maximum": 5000000,
            },
            "SpliceAI": {
                "type": "number",
                "description": "SpliceAI score threshold (0-1)",
                "minimum": 0,
                "maximum": 1,
            },
        }

        tools = [
            # HGVS Tools
            {
                "name": "vep_hgvs_single",
                "description": "Annotate a single variant using HGVS notation (genomic g., coding c., protein p.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "hgvs_notation": {
                            "type": "string",
                            "description": "HGVS notation (e.g., 'ENST00000366667:c.803C>T', '17:g.41276107A>C', 'ENSP00000401091.1:p.Tyr124Cys')",
                            "pattern": "^([A-Za-z0-9_.]+:[cgmnpr]\\.\\d+[ACGT]>[ACGT]|rs\\d+|[A-Za-z0-9_.]+:p\\.[A-Z][a-z]{2}\\d+[A-Z][a-z]{2})$",
                        },
                        **common_vep_params,
                    },
                    "required": ["species", "hgvs_notation"],
                },
            },
            {
                "name": "vep_hgvs_batch",
                "description": "Annotate multiple variants using HGVS notation in batch",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "hgvs_notations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of HGVS notations (e.g., ['ENST00000366667:c.803C>T', '9:g.22125504G>C'])",
                        },
                        **{
                            k: v
                            for k, v in common_vep_params.items()
                            if k
                            in [
                                "canonical",
                                "hgvs",
                                "domains",
                                "ccds",
                                "protein",
                                "AlphaMissense",
                                "CADD",
                                "REVEL",
                                "Conservation",
                            ]
                        },
                    },
                    "required": ["species", "hgvs_notations"],
                },
            },
            # ID Tools
            {
                "name": "vep_id_single",
                "description": "Annotate a single variant using an identifier (e.g., rs1234567, COSM476)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "variant_id": {
                            "type": "string",
                            "description": "Variant identifier (rs or COSM/COSV/CM IDs)",
                            "pattern": "^(rs\\d+|COSM\\d+|COSV\\d+|CM\\d+)$",
                        },
                        **common_vep_params,
                    },
                    "required": ["species", "variant_id"],
                },
            },
            {
                "name": "vep_id_batch",
                "description": "Annotate multiple variants using identifiers in batch",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "variant_ids": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "pattern": "^(rs\\d+|COSM\\d+|COSV\\d+|CM\\d+)$",
                            },
                            "description": "List of variant identifiers (e.g., ['rs56116432', 'COSM476'])",
                        },
                        **{
                            k: v
                            for k, v in common_vep_params.items()
                            if k
                            in [
                                "canonical",
                                "hgvs",
                                "domains",
                                "ccds",
                                "protein",
                                "AlphaMissense",
                                "CADD",
                                "REVEL",
                                "Conservation",
                            ]
                        },
                    },
                    "required": ["species", "variant_ids"],
                },
            },
            # Region Tools
            {
                "name": "vep_region_single",
                "description": "Annotate a variant using genomic region and allele",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "region": {
                            "type": "string",
                            "description": "Genomic region (pos or range, optionally with allele)",
                            "pattern": "^(?:\\d+|X|Y|MT):\\d+(?:-\\d+)?(?:\\:[ACGT]\\/[ACGT])?$",
                        },
                        "allele": {
                            "type": "string",
                            "description": "Allele base (A,C,G,T)",
                            "pattern": "^[ACGT]$",
                        },
                        **common_vep_params,
                    },
                    "required": ["species", "region", "allele"],
                },
            },
            {
                "name": "vep_region_batch",
                "description": "Annotate multiple variants using genomic coordinates in batch",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (e.g., 'homo_sapiens', 'mus_musculus')",
                            "default": "homo_sapiens",
                        },
                        "regions": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "pattern": "^(?:\\d+|X|Y|MT)\\s+\\d+\\s+[.\\w-]+\\s+[ACGT-]+\\s+[ACGT-]+(?:\\s+.*)?$",
                            },
                            "description": "List of variants in VCF format (e.g., ['1 230710048 . A G', '9 22125504 . G C']). Format: 'CHR POS ID REF ALT' where CHR=chromosome, POS=position, ID=identifier (use '.' if unknown), REF=reference allele, ALT=alternate allele.",
                        },
                        **{
                            k: v
                            for k, v in common_vep_params.items()
                            if k
                            in [
                                "canonical",
                                "hgvs",
                                "domains",
                                "ccds",
                                "protein",
                                "AlphaMissense",
                                "CADD",
                                "REVEL",
                                "Conservation",
                            ]
                        },
                    },
                    "required": ["species", "regions"],
                },
            },
            # Utility Tools
            {
                "name": "get_vep_species",
                "description": "Get list of available species for VEP annotation",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
            {
                "name": "get_consequence_types",
                "description": "Get available VEP consequence types and descriptions",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
            {
                "name": "get_assembly_info",
                "description": "Get genome assembly information for a species",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "species": {
                            "type": "string",
                            "description": "Species name (lowercase, alphanumeric or underscores)",
                            "default": "homo_sapiens",
                            "pattern": "^[a-z0-9_]+$",
                        },
                    },
                    "required": ["species"],
                },
            },
        ]

        self.send_response({"tools": tools})

    def handle_initialize(self, params: Dict[str, Any]) -> None:
        """Handle initialize request."""
        response = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "VEPmcp-mcp", "version": "0.1.0"},
        }
        self.send_response(response)

    async def handle_call_tool(self, params: Dict[str, Any]) -> None:
        """Handle tools/call request."""
        name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            async with self.bridge as bridge:
                # HGVS Tools
                if name == "vep_hgvs_single":
                    result = await bridge.vep_hgvs_single(
                        arguments["species"],
                        arguments["hgvs_notation"],
                        **{
                            k: v
                            for k, v in arguments.items()
                            if k not in ["species", "hgvs_notation"]
                        },
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                elif name == "vep_hgvs_batch":
                    result = await bridge.vep_hgvs_batch(
                        arguments["species"],
                        arguments["hgvs_notations"],
                        **{
                            k: v
                            for k, v in arguments.items()
                            if k not in ["species", "hgvs_notations"]
                        },
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                # ID Tools
                elif name == "vep_id_single":
                    result = await bridge.vep_id_single(
                        arguments["species"],
                        arguments["variant_id"],
                        **{
                            k: v for k, v in arguments.items() if k not in ["species", "variant_id"]
                        },
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                elif name == "vep_id_batch":
                    result = await bridge.vep_id_batch(
                        arguments["species"],
                        arguments["variant_ids"],
                        **{
                            k: v
                            for k, v in arguments.items()
                            if k not in ["species", "variant_ids"]
                        },
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                # Region Tools
                elif name == "vep_region_single":
                    result = await bridge.vep_region_single(
                        arguments["species"],
                        arguments["region"],
                        arguments["allele"],
                        **{
                            k: v
                            for k, v in arguments.items()
                            if k not in ["species", "region", "allele"]
                        },
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                elif name == "vep_region_batch":
                    result = await bridge.vep_region_batch(
                        arguments["species"],
                        arguments["regions"],
                        **{k: v for k, v in arguments.items() if k not in ["species", "regions"]},
                    )
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                # Utility Tools
                elif name == "get_vep_species":
                    result = await bridge.get_vep_species()
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                elif name == "get_consequence_types":
                    result = await bridge.get_consequence_types()
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                elif name == "get_assembly_info":
                    result = await bridge.get_assembly_info(arguments["species"])
                    self.send_response(
                        {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    )

                else:
                    raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}")
            self.send_response(None, str(e))

    async def run(self) -> None:
        """Main event loop for the MCP server."""
        print("VEPmcp MCP server ready...", file=sys.stderr)
        import platform

        try:
            if platform.system() == "Windows":
                # Windows-specific implementation to handle pipe issues
                await self._run_windows()
            else:
                # Unix-like systems
                await self._run_unix()
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise

    async def _run_windows(self) -> None:
        """Windows-specific implementation for reading stdin."""
        import asyncio
        import sys

        # Check if stdin is actually connected to a pipe
        if sys.stdin.isatty():
            logger.warning("No MCP client connected. Server is running but waiting for input.")
            print(
                "Warning: No MCP client detected. Server is waiting for JSON-RPC messages on stdin.",
                file=sys.stderr,
            )

        # Use a simpler approach for Windows
        loop = asyncio.get_event_loop()

        def read_line() -> Optional[str]:
            try:
                line = sys.stdin.readline()
                return line.strip() if line else None
            except (EOFError, OSError):
                return None

        while True:
            try:
                # Use run_in_executor to avoid blocking the event loop
                line = await loop.run_in_executor(None, read_line)

                if line is None:
                    # EOF or error occurred
                    break

                if not line:
                    continue

                try:
                    request = json.loads(line)
                    await self.handle_request(request)
                except json.JSONDecodeError as e:
                    print(f"Bad JSON from host: {e}", file=sys.stderr)
                    continue

            except KeyboardInterrupt:
                logger.info("Server stopped by user")
                break
            except Exception as e:
                logger.error(f"Error reading input: {str(e)}")
                break

    async def _run_unix(self) -> None:
        """Unix-like systems implementation for reading stdin."""
        import asyncio

        async def read_stdin() -> asyncio.StreamReader:
            loop = asyncio.get_event_loop()
            reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(reader)
            await loop.connect_read_pipe(lambda: protocol, sys.stdin)
            return reader

        try:
            reader = await read_stdin()

            async for line in reader:
                line_str = line.decode().strip()
                if not line_str:
                    continue

                try:
                    request = json.loads(line_str)
                    await self.handle_request(request)
                except json.JSONDecodeError as e:
                    print(f"Bad JSON from host: {e}", file=sys.stderr)
                    continue

        except Exception as e:
            logger.error(f"Error in Unix stdin reader: {str(e)}")
            raise
