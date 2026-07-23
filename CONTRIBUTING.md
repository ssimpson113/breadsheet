# Contributing to Breadsheet

Welcome! This guide helps developers and AI coding assistants understand the codebase and contribute effectively.

## Quick Start

```bash
# Clone and run
git clone https://github.com/ssimpson113/breadsheet.git
cd breadsheet
./run.sh  # Linux/macOS quick start

# Or manually
pip install streamlit
streamlit run app.py
```

## Project Architecture

### Overview
Breadsheet is a baking calculator with a clean 3-layer architecture:

```
┌─────────────────────────┐
│   Streamlit GUI (app.py)│  ← 7 interactive tabs
├─────────────────────────┤
│   Business Logic        │  ← BakersCalculator, ConversionManager
├─────────────────────────┤
│   Data Models           │  ← Ingredient, Recipe
└─────────────────────────┘
```

### Key Components

**Data Layer** (`breadsheet/models.py`)
- `Ingredient`: Represents a single ingredient (name, amount, unit, percentage)
- `Recipe`: Container for ingredients with flour_weight tracking

**Business Logic** (`breadsheet/`)
- `BakersCalculator` (`calculator.py`): All percentage calculations and scaling operations
- `ConversionManager` (`conversions.py`): Unit conversions with King Arthur Flour data

**Presentation** (`app.py`)
- Single Streamlit application with 7 tabs
- Session state manages: calculator, current_recipe, conversion_manager
- Each tab is a separate function

## Development Workflow

### Running Tests
```bash
# All tests
pytest test_breadsheet.py

# Specific test
pytest test_breadsheet.py::TestBakersCalculator::test_calculate_percentages

# With coverage
pytest test_breadsheet.py --cov=breadsheet
```

### Running the Application
```bash
# Development mode
streamlit run app.py

# With auto-reload
streamlit run app.py --server.runOnSave=true

# Custom port
streamlit run app.py --server.port 8080

# Network access
streamlit run app.py --server.address 0.0.0.0
```

### Building Executables
```bash
# Automated (detects platform)
python build_executable.py

# Manual
pyinstaller Breadsheet.spec
```

## Important Implementation Details

### Baker's Percentage Auto-Detection

The system automatically detects flour ingredients by name:

```python
# Searches for "flour" in ingredient names (case-insensitive)
total_flour = sum(
    ingredient.amount 
    for ingredient in recipe.ingredients.values() 
    if "flour" in ingredient.name.lower()
)
```

**This means:**
- Any ingredient with "flour" in the name counts toward the 100% basis
- Multiple flour types are automatically summed (e.g., "all-purpose flour" + "whole wheat flour")
- No manual tracking required - `recipe.flour_weight` is auto-calculated

### Unit Conversion Flow

All calculations use grams internally:

```
Input (any unit) → convert_to_grams() → calculations → convert_from_grams() → Output (any unit)
```

**Conversion data:**
- King Arthur Flour data hardcoded in `DEFAULT_CONVERSIONS`
- Custom conversions saved to `custom_conversions.json`
- Auto-saved when users add custom ingredients via GUI

### Streamlit Session State

Three critical session state objects:
```python
st.session_state.calculator          # BakersCalculator instance
st.session_state.current_recipe      # Working recipe (shared across tabs)
st.session_state.conversion_manager  # ConversionManager with custom data
```

Changes in one tab are immediately visible in others via shared session state.

## Common Tasks

### Adding a New Ingredient to Defaults

Edit `breadsheet/conversions.py`:
```python
DEFAULT_CONVERSIONS = {
    "ingredient name": {
        "cup": 120,        # grams per cup
        "tablespoon": 7.5,
        "teaspoon": 2.5
    }
}
```

### Adding a New Tab

1. Update tab list in `app.py` `main()`:
```python
tab1, tab2, ..., tab8 = st.tabs([
    "📝 Recipe Builder",
    # ... existing tabs ...
    "🆕 New Tab Name"
])
```

2. Create tab function:
```python
def new_tab_function():
    st.header("New Feature")
    # Your implementation
```

3. Wire it up:
```python
with tab8:
    new_tab_function()
```

### Adding Recipe Analysis Rules

Edit `recipe_analysis_tab()` in `app.py`:

```python
# 1. Add to ingredient classification
if 'keyword' in name_lower:
    ingredients_by_type['new_category'] += ingredient.percentage

# 2. Add analysis logic
if ingredients_by_type['new_category'] > threshold:
    warnings.append("⚠️ Your warning message")
    tips.append("💡 Your tip")
```

## Code Style

- **Functions**: Use descriptive names (`calculate_percentages` not `calc_pct`)
- **Comments**: Explain WHY, not WHAT (code should be self-documenting)
- **Type hints**: Use for public APIs (`def convert_to_grams(self, ingredient: str, amount: float, unit: str) -> Optional[float]`)
- **Docstrings**: Include for all public functions

## Testing Guidelines

Write tests for:
- All calculation functions (baker's percentages, scaling)
- Unit conversions (both directions)
- Edge cases (zero flour, negative values, missing ingredients)

Don't test:
- Streamlit UI components (integration tests are expensive)
- King Arthur conversion data (trusted source)

## File Structure

```
breadsheet/
├── breadsheet/              # Core package
│   ├── __init__.py         # Package exports
│   ├── models.py           # Data classes
│   ├── calculator.py       # Business logic
│   └── conversions.py      # Conversion data
├── app.py                  # Streamlit GUI
├── test_breadsheet.py      # Test suite
├── run.sh                  # Quick launcher
├── build_executable.py     # PyInstaller builder
├── requirements.txt        # Dependencies
├── setup.py               # Package config
├── README.md              # User documentation
├── CONTRIBUTING.md        # This file
├── DEPLOYMENT.md          # Deployment guide
└── CLAUDE.md              # Claude Code specific docs
```

## Dependencies

**Core:**
- Python 3.8+
- Streamlit 1.28.0+ (GUI framework)

**Optional:**
- PyInstaller 6.0.0+ (for building executables)
- pytest 7.4.0+ (for testing)

## Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect repository at [share.streamlit.io](https://share.streamlit.io)
3. Select `app.py` as main file
4. Deploy (auto-updates on every push)

### GitHub Releases
1. Build executables for each platform
2. Create release with tag (e.g., `v1.0.0`)
3. Upload platform-specific binaries

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Versioning

Current version: **1.0.0**

Version is defined in:
- `breadsheet/__init__.py` (`__version__`)
- `setup.py` (`version=`)

To release a new version:
1. Update version in both files
2. Update README.md "What's New" section
3. Create git tag: `git tag -a v1.x.x -m "Description"`
4. Push tag: `git push origin v1.x.x`

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/ssimpson113/breadsheet/issues)
- **Documentation**: See README.md, DEPLOYMENT.md, CLAUDE.md
- **Code Questions**: Check inline comments and docstrings

## License

GPL-3.0 - See [LICENSE](LICENSE) file for details.

All contributions must be compatible with GPL-3.0.
