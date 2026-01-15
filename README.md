# 🍞 Breadsheet - Baking Calculator

A comprehensive baking calculator that helps you work with baker's percentages, scale recipes, and convert between different units of measurement. Built with Python and Streamlit.

## Features

- **📝 Recipe Builder**: Create and manage your baking recipes with automatic unit conversion
- **📊 Baker's Percentages**: Calculate baker's percentages where flour = 100%
- **⚖️ Recipe Scaling**: Scale recipes by:
  - Flour weight
  - Scale factor (double, half, etc.)
  - Total weight
  - Specific ingredient amount
- **🔄 Unit Converter**: Convert between cups, grams, ounces, tablespoons, and more
- **➕ Custom Conversions**: Add your own ingredient conversions based on King Arthur Flour conversion table
- **💾 Persistent Storage**: Custom conversions are saved automatically

## Installation

### Option 1: Run Locally

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
pip install -r requirements.txt
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

### Recipe Builder Tab

1. Enter a recipe name
2. Select an ingredient from the dropdown (or enter a custom one)
3. Enter the amount and unit
4. Check "Is Flour?" for any flour ingredients (needed for baker's percentages)
5. Click "Add Ingredient"
6. Repeat for all ingredients

### Baker's Percentages Tab

After building a recipe with flour:
- View all ingredients as percentages of flour weight
- Flour is always 100%
- Other ingredients show their percentage relative to flour

Example:
- Flour: 500g (100%)
- Water: 350g (70%)
- Salt: 10g (2%)

### Scale Recipe Tab

Choose your scaling method:

**By Flour Weight**: Enter desired flour weight, all ingredients scale proportionally

**By Scale Factor**: Enter multiplier (2 = double, 0.5 = half)

**By Total Weight**: Enter desired total dough weight

**By Specific Ingredient**: Select an ingredient and enter its new amount

### Unit Converter Tab

Convert between different units for any ingredient:
1. Select an ingredient
2. Enter amount and "from" unit
3. Select "to" unit
4. Click "Convert"

### Custom Conversions Tab

Add your own ingredient conversions:
1. Enter ingredient name
2. Enter unit (e.g., "cup", "tablespoon")
3. Enter grams per unit
4. Click "Add Conversion"

## Included Ingredients

The app comes pre-loaded with King Arthur Flour conversion data for:

- **Flours**: All-purpose, bread, whole wheat, cake, pastry, rye
- **Sugars**: Granulated, brown, powdered, honey, maple syrup, molasses
- **Fats**: Butter, oil, shortening
- **Liquids**: Water, milk
- **Other**: Salt, baking powder, baking soda, yeast, cocoa powder, vanilla, eggs

## Project Structure

```
breadsheet/
├── breadsheet/           # Main package
│   ├── __init__.py
│   ├── models.py        # Data models (Ingredient, Recipe)
│   ├── conversions.py   # Unit conversion system
│   └── calculator.py    # Baker's percentage calculations
├── app.py               # Streamlit GUI application
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── README.md           # This file
└── LICENSE             # GPL-3.0 license
```

## Development

### Running Tests

```bash
pytest
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

**App won't start**: Make sure you have Python 3.8+ and all dependencies installed

**Conversion not found**: Add a custom conversion in the Custom Conversions tab

**Executable too large**: This is normal - executables bundle Python and all dependencies

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Acknowledgments

- Conversion data based on [King Arthur Baking's Ingredient Weight Chart](https://www.kingarthurbaking.com/learn/ingredient-weight-chart)
- Built with [Streamlit](https://streamlit.io)

## Author

Your Name - [Your GitHub](https://github.com/yourusername)

---

Happy Baking! 🍞
