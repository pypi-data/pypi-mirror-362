"""
Tests for VEPmcp main functionality.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from vep_mcp.bridge import Bridge


@pytest.mark.asyncio
async def test_vep_hgvs_single(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result({"input": "test"})
        result = await bridge.vep_hgvs_single("homo_sapiens", "ENST00000366667:c.803C>T")
        assert result == {"input": "test"}
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_vep_hgvs_batch(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result([{"input": "test1"}, {"input": "test2"}])
        result = await bridge.vep_hgvs_batch("homo_sapiens", ["ENST00000366667:c.803C>T"])
        assert result == [{"input": "test1"}, {"input": "test2"}]
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_vep_id_single(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result({"input": "rs123"})
        result = await bridge.vep_id_single("homo_sapiens", "rs123")
        assert result == {"input": "rs123"}
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_vep_id_batch(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result([{"input": "rs123"}, {"input": "rs456"}])
        result = await bridge.vep_id_batch("homo_sapiens", ["rs123", "rs456"])
        assert result == [{"input": "rs123"}, {"input": "rs456"}]
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_vep_region_single(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result({"input": "1:230710048:A/G"})
        result = await bridge.vep_region_single("homo_sapiens", "1:230710048", "G")
        assert result == {"input": "1:230710048:A/G"}
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_vep_region_batch(bridge: Bridge):
    with patch("vep_mcp.bridge.Bridge._make_request", new_callable=MagicMock) as mock_request:
        mock_request.return_value = asyncio.Future()
        mock_request.return_value.set_result([{"input": "region1"}, {"input": "region2"}])
        result = await bridge.vep_region_batch(
            "homo_sapiens", ["1:230710048:A/G", "2:158267250:T/C"]
        )
        assert result == [{"input": "region1"}, {"input": "region2"}]
        mock_request.assert_called_once()


def test_species_validation(bridge: Bridge):
    """Test species name validation."""
    from vep_mcp.bridge import VEPValidator

    # Valid species
    assert VEPValidator.validate_species("homo_sapiens") == "homo_sapiens"
    assert VEPValidator.validate_species("Homo sapiens") == "homo_sapiens"

    # Invalid species
    with pytest.raises(ValueError):
        VEPValidator.validate_species("")

    with pytest.raises(ValueError):
        VEPValidator.validate_species("invalid-species!")


def test_hgvs_validation(bridge: Bridge):
    """Test HGVS notation validation."""
    from vep_mcp.bridge import VEPValidator

    # Valid HGVS (basic patterns)
    valid_hgvs = [
        "ENST00000366667:c.803C>T",
        "rs12345",
    ]

    for hgvs in valid_hgvs:
        assert VEPValidator.validate_hgvs_notation(hgvs) == hgvs

    # Invalid HGVS
    with pytest.raises(ValueError):
        VEPValidator.validate_hgvs_notation("")


def test_batch_size_validation(bridge: Bridge):
    """Test batch size validation."""
    from vep_mcp.bridge import VEPValidator

    # Valid batch
    items = ["item1", "item2", "item3"]
    assert VEPValidator.validate_batch_size(items) == items

    # Empty batch
    with pytest.raises(ValueError):
        VEPValidator.validate_batch_size([])

    # Too large batch
    large_batch = ["item"] * 1001
    with pytest.raises(ValueError):
        VEPValidator.validate_batch_size(large_batch)
