# AgentOps: AI-Powered Requirements-Driven Test Automation

[![PyPI version](https://badge.fury.io/py/agentops-ai.svg)](https://pypi.org/project/agentops-ai/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AgentOps is a next-generation, AI-powered development platform that automatically generates requirements and tests from your codebase. Using advanced multi-agent AI systems, AgentOps bridges the gap between technical implementation and business requirements through bidirectional analysis.

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install agentops-ai

# Or install from source
git clone https://github.com/knaig/agentops_ai.git
cd agentops_ai
pip install -e .
```

### Basic Usage

```bash
# 1. Initialize your project
agentops init

# 2. Run complete analysis on your code
agentops runner myfile.py

# 3. Check results and status
agentops status

# 4. View traceability matrix
agentops traceability
```

That's it! AgentOps will automatically:
- ✅ Analyze your code structure
- ✅ Generate business-focused requirements
- ✅ Create comprehensive test cases
- ✅ Execute tests and provide results
- ✅ Generate traceability matrices

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `agentops init` | Initialize project structure | `agentops init` |
| `agentops runner <file>` | Complete workflow execution | `agentops runner src/main.py` |
| `agentops tests <file>` | Generate test suites | `agentops tests src/main.py` |
| `agentops analyze <file>` | Deep requirements analysis | `agentops analyze src/main.py` |
| `agentops status` | Check project status | `agentops status` |
| `agentops traceability` | Generate traceability matrix | `agentops traceability` |
| `agentops onboarding` | Interactive setup guide | `agentops onboarding` |
| `agentops version` | Show version information | `agentops version` |
| `agentops help` | Show detailed help | `agentops help` |

### 🚀 Power User Options

| Option | Description | Example |
|--------|-------------|---------|
| `--all` | Process all Python files | `agentops runner --all` |
| `--auto-approve` | Skip manual review | `agentops runner myfile.py --auto-approve` |
| `-v, --verbose` | Detailed output | `agentops runner myfile.py -v` |

**Combined Usage:**
```bash
# Batch process entire project with automation
agentops runner --all --auto-approve -v

# Generate tests for all files
agentops tests --all --auto-approve

# Detailed analysis with verbose output
agentops analyze myfile.py -v
```

## 🎯 Enhanced CLI Experience

### Interactive Onboarding
New users can get started quickly with the interactive onboarding:

```bash
agentops onboarding
```

This will:
- ✅ Check your installation and API key setup
- ✅ Create sample files for demonstration
- ✅ Run a complete demo workflow
- ✅ Show you all available commands and options
- ✅ Guide you through next steps

### Batch Processing
Process your entire project with a single command:

```bash
# Analyze all Python files in your project
agentops runner --all

# Generate tests for all files
agentops tests --all

# With automation and verbose output
agentops runner --all --auto-approve -v
```

### CI/CD Integration
Perfect for automated workflows:

```bash
# Fully automated analysis
agentops runner --all --auto-approve

# Check project status
agentops status -v
```

## 🔧 Configuration

### Environment Setup

Create a `.env` file in your project root:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom settings
AGENTOPS_OUTPUT_DIR=.agentops
AGENTOPS_LOG_LEVEL=INFO
```

### API Key Validation

Validate your API keys before running:

```bash
# Run the validation script
./scripts/validate_api_keys.sh
```

## 📁 Generated Artifacts

After running AgentOps, you'll find these artifacts in your project:

```
.agentops/
├── requirements/
│   ├── requirements.gherkin    # Requirements in Gherkin format
│   └── requirements.md         # Requirements in Markdown format
├── tests/
│   ├── test_main.py           # Generated test files
│   └── test_coverage.xml      # Test coverage reports
├── traceability/
│   └── traceability_matrix.md # Requirements-to-tests mapping
└── reports/
    └── analysis_report.json   # Detailed analysis results
```

## 🎯 Key Features

### 🤖 Multi-Agent AI System
- **Code Analyzer**: Deep code structure and dependency analysis
- **Requirements Engineer**: Business-focused requirement extraction
- **Test Architect**: Comprehensive test strategy design
- **Test Generator**: High-quality, maintainable test code
- **Quality Assurance**: Automated test validation and scoring

### 📊 Requirements-Driven Testing
- **Bidirectional Analysis**: Code → Requirements → Tests
- **Business Context**: Requirements focus on real-world value
- **Traceability**: Complete mapping from requirements to tests
- **Multiple Formats**: Gherkin (BDD) and Markdown outputs

### 🔄 Streamlined Workflow
- **Single Command**: `agentops runner` does everything
- **Automatic Export**: Requirements and traceability always up-to-date
- **Error Recovery**: Robust handling of common issues
- **Progress Tracking**: Real-time status updates

## 📖 Examples

### Basic Python File Analysis

```python
# myfile.py
def calculate_total(items, tax_rate=0.1):
    """Calculate total with tax for a list of items."""
    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax

def apply_discount(total, discount_percent):
    """Apply percentage discount to total."""
    discount = total * (discount_percent / 100)
    return total - discount
```

```bash
# Run analysis
agentops runner myfile.py
```

**Generated Requirements (Gherkin):**
```gherkin
Feature: Shopping Cart Calculations

Scenario: Calculate total with tax
  Given a list of items with prices [10, 20, 30]
  And a tax rate of 10%
  When I calculate the total
  Then the result should be 66.0

Scenario: Apply discount to total
  Given a total amount of 100
  And a discount of 15%
  When I apply the discount
  Then the final amount should be 85.0
```

**Generated Tests:**
```python
def test_calculate_total_with_tax():
    items = [10, 20, 30]
    result = calculate_total(items, tax_rate=0.1)
    assert result == 66.0

def test_apply_discount():
    result = apply_discount(100, 15)
    assert result == 85.0
```

## 🛠️ Advanced Usage

### Custom Configuration

```python
# agentops_ai/agentops_core/config.py
LLM_MODEL = "gpt-4"
LLM_TEMPERATURE = 0.1
OUTPUT_DIR = ".agentops"
LOG_LEVEL = "INFO"
```

### Python API

```python
from agentops_ai.agentops_core.orchestrator import AgentOrchestrator

# Create orchestrator
orchestrator = AgentOrchestrator()

# Run analysis
result = orchestrator.run_workflow("myfile.py")

# Access results
print(f"Requirements: {len(result.requirements)}")
print(f"Tests generated: {len(result.test_code)} lines")
print(f"Quality score: {result.quality_score}")
```

## 🔍 Troubleshooting

### Common Issues

**API Key Errors:**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

**Permission Errors:**
```bash
# Ensure write permissions
chmod 755 .agentops/
```

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Getting Help

```bash
# Show detailed help
agentops help

# Check version
agentops version

# Validate setup
agentops status
```

## 📚 Documentation

- [Quick Start Guide](docs/02_testing/01_quick_start.md)
- [Architecture Overview](docs/02_testing/02_architecture_overview.md)
- [API Reference](docs/02_testing/03_api_reference.md)
- [Integration Guide](docs/02_testing/03_integration_guide.md)
- [Changelog](docs/01_project_management/03_changelog.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/05_development/01_contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/knaig/agentops_ai/issues)
- **Documentation**: [Project Docs](docs/)
- **Email**: agentops_info@protonmail.com

---

**AgentOps**: Bridging technical implementation and business requirements through AI-powered analysis. 🚀 