# VEPmcp

VEPmcp is a Model Context Protocol (MCP) server for the [Ensembl Variant Effect Predictor (VEP) API](https://rest.ensembl.org/). It enables annotation and effect prediction of genetic variants, with full support for batch and single queries, and is designed for seamless integration with MCP-compatible clients (e.g., Claude Desktop, VS Code MCP extension).

---

## Features

- Annotate variants using Ensembl VEP (HGVS, variant ID, or genomic region)
- Batch and single variant support
- Retrieve available species, consequence types, and assembly info
- Fast, robust, and rate-limited HTTP client
- JSON-RPC 2.0 over stdio for easy integration with AI tools and editors

---

## Installation

```bash
pip install -e .
# or, when available (soon):
pip install VEPmcp
```

---

## Usage

### Command Line

```bash
VEPmcp --help
VEPmcp --test-connection      # Test Ensembl API connectivity
VEPmcp --test-mode            # Run server in test mode with sample requests
```

### As an MCP Server

Run the server (for use with MCP clients):

```bash
VEPmcp
```

The server communicates via stdio using JSON-RPC 2.0.

---

## Supported Tools

- `vep_hgvs_single` / `vep_hgvs_batch`: Annotate by HGVS notation
- `vep_id_single` / `vep_id_batch`: Annotate by variant ID (e.g., rsID)
- `vep_region_single` / `vep_region_batch`: Annotate by genomic region
- `get_vep_species`: List available species
- `get_consequence_types`: List consequence types
- `get_assembly_info`: Get assembly info for a species

---

## Example MCP Client Configurations

### Claude Desktop

```json
{
  "mcp_servers": {
    "vepmcp": {
      "command": "VEPmcp",
      "args": [],
      "env": {}
    }
  }
}
```

### VS Code MCP Extension

```json
{
  "mcp.servers": {
    "vepmcp": {
      "command": "VEPmcp",
      "args": [],
      "env": {},
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

## Example Usage

Prompt your MCP client with:

```
"Annotate the variant rs56116432 in humans using VEP"
```

---

## Testing

- `VEPmcp --test-connection` — check API connectivity
- `VEPmcp --test-mode` — run server in test mode
- `python run_tests.py --mode all --verbose` — run all unit/integration tests
- `python run_tests.py --mode ci` — run CI pipeline (linting + type checking + unit tests)

### Continuous Integration

This project uses GitHub Actions for automated testing on every pull request. The CI pipeline includes:
- Linting with Ruff
- Type checking with MyPy  
- Unit and integration tests across Python 3.9-3.13
- Security scanning
- Code coverage reporting

---

## Troubleshooting

- Ensure VEPmcp is installed and in your PATH
- Check internet connectivity for Ensembl API access
- Use `--verbose` for detailed logs

---

## Development

```bash
pip install -e .[dev]
python run_tests.py --mode ci  # Run linting, type checking, and unit tests
python run_tests.py --mode all --verbose  # Run all tests including integration
```

### Local Testing Commands

```bash
# Linting and formatting
python run_tests.py --mode lint

# Type checking  
python run_tests.py --mode type

# Unit tests only
python run_tests.py --mode unit --verbose

# Integration tests (requires internet)
python run_tests.py --mode integration --verbose
```

---

## License

MIT License — see LICENSE

---

## Contributing

1. Fork and branch
2. Make changes and add tests
3. Run the test suite
4. Submit a pull request

---

## Support

For issues and questions, use the GitHub issue tracker.

---