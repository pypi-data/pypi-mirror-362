# emtest - Python Testing Utilities

A Python package providing testing utilities.

## Features

### 🎨 Clean Test Output for Pytest
- **MinimalReporter**: Custom pytest reporter with clean, colored output using simple symbols (✓/✗/-)
- **Configurable Output**: Toggle between minimal and standard pytest output modes

### 🔧 Development Utilities  
- **Source Path Management**: Dynamically add directories to Python path for testing source code
- **Module Source Validation**: Ensure modules are loaded from source directories (not installed packages)
- **Thread Cleanup Monitoring**: Wait for and verify proper thread cleanup in tests

### ⚡ Enhanced Test Execution
- **Dual Execution Pattern**: Run tests both as pytest tests and standalone Python scripts
- **Breakpoint Integration**: Easy debugging with pytest's `--pdb` integration
- **Progress Indicators**: Visual progress bars for waiting operations

## Installation

```sh
pip install emtest
```

## Usage

See the `examples/` directory for complete working examples showing:
- Basic test setup with `conftest.py`
- Dual execution pattern implementation
- Source loading validation
- Thread cleanup testing


