"""
Integration tests for VEPmcp - these tests require internet connection.
"""

import pytest
import asyncio
from typing import Any, Dict, List, Union
from vep_mcp.bridge import Bridge, Config


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_vep_species_integration():
    """Test actual API call to get VEP species."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        result = await bridge.get_vep_species()

        # Basic validation
        assert isinstance(result, dict)
        assert "species" in result
        assert len(result["species"]) > 0

        # Check for common species
        species_names = [s["name"] for s in result["species"]]
        assert "homo_sapiens" in species_names


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_consequence_types_integration():
    """Test actual API call to get VEP consequence types."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        result = await bridge.get_consequence_types()

        # Basic validation
        assert isinstance(result, (dict, list))
        if isinstance(result, list):
            assert len(result) > 0
        else:
            # Handle different response formats
            assert len(result.keys()) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_assembly_info_integration():
    """Test actual API call to get assembly info."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        result = await bridge.get_assembly_info("homo_sapiens")

        # Basic validation
        assert isinstance(result, dict)
        # Common assembly fields
        expected_fields = ["assembly_name", "assembly_accession", "chromosomes"]
        # At least one of these should be present
        assert any(field in result for field in expected_fields)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vep_hgvs_single_integration():
    """Test actual VEP HGVS annotation - basic case."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        # Test with proper HGVS notation
        hgvs_notation = "ENST00000366667:c.803C>T"
        result: Union[List[Dict[str, Any]], Dict[str, Any]] = await bridge.vep_hgvs_single(
            species="homo_sapiens", hgvs_notation=hgvs_notation, canonical=True
        )

        # Basic validation
        assert isinstance(result, list)
        assert len(result) > 0

        # Check first result structure
        if result and isinstance(result, list):
            first_result = result[0]  # type: ignore
            assert isinstance(first_result, dict)
            assert "input" in first_result
            assert first_result["input"] == hgvs_notation


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vep_id_single_integration():
    """Test actual VEP ID annotation."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        result: Union[List[Dict[str, Any]], Dict[str, Any]] = await bridge.vep_id_single(
            species="homo_sapiens", variant_id="rs699", canonical=True
        )

        # Basic validation
        assert isinstance(result, list)
        assert len(result) > 0

        # Check first result
        if result and isinstance(result, list):
            first_result = result[0]  # type: ignore
            assert isinstance(first_result, dict)
            assert "input" in first_result
            assert first_result["input"] == "rs699"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_limiting():
    """Test that rate limiting works properly."""
    config = Config()
    bridge = Bridge(config)

    async with bridge:
        # Make several quick requests to test rate limiting
        tasks = []
        for i in range(5):
            task = bridge.get_vep_species()
            tasks.append(task)

        # All should complete without errors
        results = await asyncio.gather(*tasks)

        # All results should be valid
        for result in results:
            assert isinstance(result, dict)
            assert "species" in result
