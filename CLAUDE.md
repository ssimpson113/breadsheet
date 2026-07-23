# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Breadsheet is a baking calculator built with Streamlit that provides baker's percentages, recipe scaling, unit conversions, and recipe analysis. The application serves both professional bakers (using percentages) and home bakers (using volume measurements).

## Architecture

### Three-Layer Design

1. **Data Models** (`breadsheet/models.py`)
   - `Ingredient`: Represents a single ingredient with name, amount, unit, and optional baker's percentage
   - `Recipe`: Container for ingredients with flour_weight tracking (basis for percentages)

2. **Business Logic** (`breadsheet/`)
   - `BakersCalculator` (`calculator.py`): All baker's percentage calculations and scaling operations
   - `ConversionManager` (`conversions.py`): King Arthur Flour conversion data + custom conversions with JSON persistence

3. **GUI** (`app.py`)
   - Single-file Streamlit application with 7 tabs
   - Uses Streamlit session state for calculator, current_recipe, and conversion_manager
   - Each tab is a separate function (`recipe_builder_tab()`, `bakers_percentage_tab()`, etc.)

### Key Design Decisions

**Baker's Percentages Auto-Detection**:
- `calculate_percentages()` automatically detects flour by searching for "flour" in ingredient names
- Sums all flour types (all-purpose, whole wheat, rye, etc.) to get the 100% basis
- Updates `recipe.flour_weight` automatically - no manual tracking needed

**Unit Conversion Flow**:
- All internal calculations use grams
- `ConversionManager.convert_to_grams()` → calculations → `ConversionManager.convert_from_grams()`
- King Arthur Flour data is hardcoded in `DEFAULT_CONVERSIONS`
- Custom conversions stored in `custom_conversions.json` (auto-saved)

**Streamlit Session State**:
- `st.session_state.current_recipe`: The working recipe across all tabs
- `st.session_state.calculator`: BakersCalculator instance (shared)
- `st.session_state.conversion_manager`: ConversionManager instance (persists custom conversions)
- Recipe modifications in one tab are immediately visible in other tabs via session state

## Running the Application

### Development
```bash
# Quick start (Linux/macOS)
./run.sh

# Manual start
streamlit run app.py

# With specific port
streamlit run app.py --server.port 8080
```

### Testing
```bash
# Run all tests
pytest test_breadsheet.py

# Run specific test
pytest test_breadsheet.py::TestBakersCalculator::test_calculate_percentages

# Verbose output
pytest test_breadsheet.py -v
```

### Building Executables
```bash
# Automated build (detects platform)
python build_executable.py

# Manual PyInstaller
# Linux/macOS:
pyinstaller --onefile --windowed --add-data "breadsheet:breadsheet" --name Breadsheet app.py

# Windows:
pyinstaller --onefile --windowed --add-data "breadsheet;breadsheet" --name Breadsheet app.py
```

## Critical Implementation Details

### Baker's Percentage Calculation

The key insight: flour weight is auto-detected, not manually tracked.

```python
# In BakersCalculator.calculate_percentages():
total_flour = sum(
    ingredient.amount 
    for ingredient in recipe.ingredients.values() 
    if "flour" in ingredient.name.lower()
)
recipe.flour_weight = total_flour  # Auto-update

for ingredient in recipe.ingredients.values():
    ingredient.percentage = (ingredient.amount / flour_basis) * 100
```

**Why this matters**: If you're debugging percentage issues, check that:
1. At least one ingredient has "flour" in its name (case-insensitive)
2. The flour amount > 0
3. No accidental double-counting of flour

### Recipe Analysis Logic

The analysis tab (`recipe_analysis_tab()`) categorizes ingredients by detecting keywords:

- **Salt**: `'salt' in name_lower`
- **Yeast**: `'yeast' in name_lower`
- **Liquids**: `'water', 'milk', 'cream', 'buttermilk', 'yogurt'` in name
- **Eggs**: 75% liquid, 11% fat (by percentage)
- **Whole grain flour**: `'whole wheat', 'whole grain', 'rye', 'spelt'` in name

Hydration = sum of all liquid percentages (relative to flour weight)

### Conversion Data Structure

```python
DEFAULT_CONVERSIONS = {
    "all-purpose flour": {
        "cup": 120,        # grams per cup
        "tablespoon": 7.5,
        "teaspoon": 2.5
    },
    "yeast (instant)": {
        "packet": 7,       # Standard US packet
        "envelope": 7,
        "tablespoon": 8.5,
        "teaspoon": 2.8
    }
    # ... 30+ ingredients
}
```

**Adding new ingredients**: Use the Custom Conversions tab or directly edit `DEFAULT_CONVERSIONS` in `conversions.py`

### Scaling Operations

All scaling methods in `BakersCalculator`:

1. **By Flour Weight**: `scale_recipe_by_flour(recipe, new_flour_weight)`
2. **By Factor**: `scale_recipe_by_factor(recipe, 2.0)` for double
3. **By Total Weight**: `scale_recipe_to_total_weight(recipe, target_grams)`
4. **By Ingredient**: `scale_by_ingredient(recipe, "water", 400, "g")`

All return a **new Recipe object** - original is never modified.

## Deployment

### Streamlit Cloud
- Push to GitHub
- Connect at share.streamlit.io
- Select `app.py` as main file
- Auto-deploys on every push to main branch

### Local Network Access
```bash
streamlit run app.py --server.address 0.0.0.0
# Others access at http://YOUR_IP:8501
```

## Common Modification Patterns

### Adding a New Ingredient to Defaults
Edit `breadsheet/conversions.py`:
```python
DEFAULT_CONVERSIONS = {
    # ... existing ingredients
    "sourdough starter": {
        "cup": 240,
        "tablespoon": 15
    }
}
```

### Adding a New Tab
1. Add tab name in `main()`: `tab8 = st.tabs([...new tab...])`
2. Create function: `def new_tab_function(): ...`
3. Call in main: `with tab8: new_tab_function()`

### Adding Analysis Rules
Edit `recipe_analysis_tab()` in `app.py`:
```python
# Add to ingredients_by_type classification
if 'new_ingredient_type' in name_lower:
    ingredients_by_type['new_type'] += ingredient.percentage

# Add analysis section
st.subheader("🆕 New Analysis")
if ingredients_by_type['new_type'] > threshold:
    warnings.append("⚠️ Warning message")
```

## Files Not to Edit Directly

- `custom_conversions.json`: Auto-generated by ConversionManager, managed via GUI
- `dist/` and `build/`: PyInstaller output directories
- `.streamlit/`: Streamlit config (auto-generated)

## Version Management

Current version: **1.0.0** (defined in `breadsheet/__init__.py` and `setup.py`)

To release a new version:
1. Update version in both files
2. Create git tag: `git tag -a v1.x.x -m "Description"`
3. Update README.md "What's New" section
