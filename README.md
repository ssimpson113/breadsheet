# 🍞 Breadsheet - Baking Calculator

A comprehensive baking calculator that helps you work with baker's percentages, scale recipes, and convert between different units of measurement. Built with Python and Streamlit.

Perfect for bakers of all skill levels - from professionals using baker's percentages to home bakers who prefer measuring cups!

## Features

### 📝 Recipe Builder
- Create and manage baking recipes with automatic unit conversion
- Add ingredients in any unit (grams, cups, tablespoons, ounces, etc.)
- Automatic flour detection for baker's percentages
- Easy ingredient management (add/remove)

### 📊 Baker's Percentages
- Calculate baker's percentages where flour = 100%
- **Automatic hydration calculation** - see liquid percentage
- View total recipe weight and percentages
- Industry-standard format for professional baking

### 🔬 Recipe Analysis (NEW!)
- **Expert insights** on your recipe formulation
- **Smart warnings** for common issues (too much salt, extreme hydration, etc.)
- **Professional tips** based on ingredient ratios
- Analysis of:
  - Salt levels (1.8-2.2% is typical)
  - Hydration (categorized as low/medium/high/very high)
  - Yeast amounts (with fermentation time estimates)
  - Sugar content (lean vs enriched dough)
  - Fat content (lean vs enriched)
  - Whole grain vs white flour ratios
- Automatic bread type identification (artisan, enriched, whole grain, etc.)

### ⚖️ Recipe Scaling
Scale recipes by:
- **Flour weight** - Enter desired flour weight
- **Scale factor** - Double (2x), half (0.5x), or any multiplier
- **Total weight** - Target final dough weight
- **Specific ingredient** - Scale based on one ingredient

### 📋 Recipe Converter (NEW!)
**Perfect for people who don't use scales!**
- Convert entire recipes to:
  - **Cups & Spoons** - Uses common fractions (¼, ⅓, ½, ¾)
  - **Ounces** - Imperial weight (shows pounds when appropriate)
  - **Grams** - Metric (original measurements)
- Smart unit selection (cups for large amounts, tsp for small)

### 🔄 Unit Converter
- Convert between any units for individual ingredients
- Supports: cups, grams, ounces, pounds, tablespoons, teaspoons
- **Yeast packets** - 7g standard US packet size

### ➕ Custom Conversions
- Add your own ingredient conversions
- Based on King Arthur Flour data (30+ ingredients included)
- Persistent storage (saved automatically)
- View and manage all conversions

## Installation

### Option 1: Run Locally

#### Linux / macOS (Quick Start)
```bash
git clone https://github.com/yourusername/breadsheet.git
cd breadsheet
./run.sh
```

The launcher script will automatically install dependencies and start the app!

#### Manual Installation (All Platforms)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/breadsheet.git
cd breadsheet
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install streamlit
```

4. Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your forked repository, branch (main), and main file (app.py)
6. Click "Deploy"

Your app will be live at `your-app-name.streamlit.app`

### Option 3: Create Executable

For non-technical users who want a click-to-run application:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
# Windows
pyinstaller --onefile --windowed --add-data "breadsheet;breadsheet" --name Breadsheet app.py

# macOS/Linux
pyinstaller --onefile --windowed --add-data "breadsheet:breadsheet" --name Breadsheet app.py
```

3. Find the executable in the `dist/` folder

**Note**: Executables are platform-specific. Build on Windows for Windows users, macOS for Mac users, etc.

## Usage Guide

### 📝 Recipe Builder Tab

1. Enter a recipe name
2. Select an ingredient from the dropdown (or enter a custom one)
3. Enter the amount and unit
4. Check "Is Flour?" for any flour ingredients (needed for baker's percentages)
5. Click "Add Ingredient"
6. Repeat for all ingredients

**Note**: Flour is auto-detected, so you don't always need to check "Is Flour?"

### 📊 Baker's Percentages Tab

After building a recipe with flour:
- View all ingredients as percentages of flour weight
- Flour is always 100%
- See **hydration percentage** (liquids as % of flour)
- View total weight and total percentage

**Example:**
- All-purpose flour: 500g (100%)
- Water: 350g (70%)
- Salt: 10g (2%)
- Yeast: 7g (1.4%)
- **Hydration: 70%** (350g liquid)

### 🔬 Recipe Analysis Tab

Get expert feedback on your recipe:
- **Salt Analysis**: Warns if too high/low (typical: 1.8-2.2%)
- **Hydration Analysis**: Categorizes as low/medium/high with specific bread types
- **Yeast Analysis**: Estimates fermentation time based on percentage
- **Sugar & Fat Analysis**: Identifies lean vs enriched doughs
- **Flour Composition**: Analyzes whole grain ratios
- **Overall Assessment**: Identifies recipe type and provides tips

**Example Warnings:**
- 🔴 "Salt is too high! (15%) - Will make bread very salty"
- ⚠️ "Very high hydration (85%) - Challenging to handle"

**Example Tips:**
- 💡 "Whole grain absorbs more water - consider increasing hydration by 5-10%"
- 💡 "Use stretch-and-fold technique instead of kneading"

### ⚖️ Scale Recipe Tab

Choose your scaling method:

**By Flour Weight**: Enter desired flour weight, all ingredients scale proportionally

**By Scale Factor**: Enter multiplier (2 = double, 0.5 = half)

**By Total Weight**: Enter desired total dough weight

**By Specific Ingredient**: Select an ingredient and enter its new amount

### 📋 Recipe Converter Tab

Perfect for sharing recipes with people who don't use scales!

**Volume (Cups & Spoons)**:
- 500g flour → 4 ¼ cups
- 350g water → 1 ½ cups
- 10g salt → 1.7 tsp
- Shows common fractions for easy measuring

**Imperial Weight (Ounces)**:
- 500g flour → 17.6 oz (1.1 lb)
- Automatically converts to pounds when appropriate

**Metric (Grams)**:
- Shows original measurements

### 🔄 Unit Converter Tab

Convert between units for individual ingredients:
1. Select an ingredient
2. Enter amount and "from" unit
3. Select "to" unit
4. Click "Convert"

**Supports**: cups, grams, ounces, pounds, tablespoons, teaspoons, packets (for yeast)

### ➕ Custom Conversions Tab

Add your own ingredient conversions:
1. Enter ingredient name
2. Enter unit (e.g., "cup", "tablespoon")
3. Enter grams per unit
4. Click "Add Conversion"

View and manage all conversions (default + custom)

## Included Ingredients

The app comes pre-loaded with King Arthur Flour conversion data for **30+ common baking ingredients**:

- **Flours**: All-purpose, bread, whole wheat, cake, pastry, rye
- **Sugars**: Granulated, brown, powdered, honey, maple syrup, molasses
- **Fats**: Butter, oil, shortening
- **Liquids**: Water, milk
- **Leavening**: Yeast (active dry & instant, including **7g packets**), baking powder, baking soda
- **Other**: Salt, cocoa powder, vanilla, eggs (large, medium, extra-large)

## Project Structure

```
breadsheet/
├── breadsheet/              # Main package
│   ├── __init__.py         # Package initialization
│   ├── models.py           # Data models (Ingredient, Recipe)
│   ├── conversions.py      # King Arthur Flour conversion data
│   └── calculator.py       # Baker's percentage calculations
├── app.py                  # Streamlit GUI (7 tabs)
├── run.sh                  # Linux/macOS launcher script
├── build_executable.py     # PyInstaller build script
├── test_breadsheet.py      # Test suite
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── README.md              # Documentation
├── DEPLOYMENT.md          # Deployment guide
└── LICENSE                # GPL-3.0 license
```

## What's New in v1.0.0

✨ **New Features:**
- 🔬 **Recipe Analysis Tab** - Get expert insights and warnings about your recipe
- 📋 **Recipe Converter Tab** - Convert entire recipes to cups/spoons/ounces
- 💧 **Hydration Calculation** - Automatic liquid percentage in Baker's Percentages tab
- 📦 **Yeast Packet Measurements** - Support for standard 7g packets
- 🐧 **Linux Launcher** - Easy `./run.sh` script for quick startup

🐛 **Bug Fixes:**
- Fixed baker's percentage calculation to correctly use flour as 100% basis
- Auto-detects all flour types (all-purpose, whole wheat, rye, etc.)

## Development

### Running Tests

```bash
pytest test_breadsheet.py
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Technical Details

- **Python Version**: 3.8+
- **GUI Framework**: Streamlit
- **Packaging**: PyInstaller for executables
- **License**: GPL-3.0

## Tips for Bakers

### Understanding Baker's Percentages

Baker's percentages express each ingredient as a percentage of the total flour weight:
- Makes recipes easy to scale
- Allows easy comparison between recipes
- Industry standard for professional baking

### Common Baker's Percentages

**Basic Bread**:
- Flour: 100%
- Water: 60-70%
- Salt: 2%
- Yeast: 1-2%

**Pizza Dough**:
- Flour: 100%
- Water: 65%
- Salt: 2-3%
- Yeast: 0.5-1%
- Oil: 2-3%

## Troubleshooting

**App won't start**:
- Make sure you have Python 3.8+ installed (`python --version`)
- Install Streamlit: `pip install streamlit`
- On Linux: Try `./run.sh` which handles everything automatically

**Baker's percentages showing wrong values**:
- Make sure you've marked flour ingredients (they'll auto-detect if "flour" is in the name)
- Check that flour weight is greater than 0

**Conversion not found**:
- Add a custom conversion in the Custom Conversions tab
- Check spelling of ingredient name
- Use the "Custom Conversions" tab to view all available ingredients

**Recipe Analysis not showing**:
- Make sure you have flour in your recipe
- Add more ingredients for comprehensive analysis

**Executable too large**:
- This is normal - executables bundle Python and all dependencies (50-150 MB)
- No way to reduce size significantly

**Linux: Permission denied when running ./run.sh**:
```bash
chmod +x run.sh
./run.sh
```

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Acknowledgments

- Conversion data based on [King Arthur Baking's Ingredient Weight Chart](https://www.kingarthurbaking.com/learn/ingredient-weight-chart)
- Built with [Streamlit](https://streamlit.io)

## Author

Your Name - [Your GitHub](https://github.com/yourusername)

---

Happy Baking! 🍞
