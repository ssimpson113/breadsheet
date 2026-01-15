"""
Unit conversions for baking ingredients based on King Arthur Flour conversion table.
Supports adding custom conversions.
"""

import json
import os
from typing import Dict, Optional


class ConversionManager:
    """Manages unit conversions for baking ingredients."""

    # King Arthur Flour conversion data (grams per cup)
    # Source: https://www.kingarthurbaking.com/learn/ingredient-weight-chart
    DEFAULT_CONVERSIONS = {
        # Flours
        "all-purpose flour": {"cup": 120, "tablespoon": 7.5, "teaspoon": 2.5},
        "bread flour": {"cup": 120, "tablespoon": 7.5, "teaspoon": 2.5},
        "whole wheat flour": {"cup": 113, "tablespoon": 7, "teaspoon": 2.3},
        "cake flour": {"cup": 114, "tablespoon": 7, "teaspoon": 2.3},
        "pastry flour": {"cup": 106, "tablespoon": 6.6, "teaspoon": 2.2},
        "rye flour": {"cup": 102, "tablespoon": 6.4, "teaspoon": 2.1},

        # Sugars
        "granulated sugar": {"cup": 200, "tablespoon": 12.5, "teaspoon": 4.2},
        "brown sugar": {"cup": 213, "tablespoon": 13.3, "teaspoon": 4.4},
        "powdered sugar": {"cup": 113, "tablespoon": 7, "teaspoon": 2.3},
        "honey": {"cup": 340, "tablespoon": 21, "teaspoon": 7},
        "maple syrup": {"cup": 312, "tablespoon": 19.5, "teaspoon": 6.5},
        "molasses": {"cup": 336, "tablespoon": 21, "teaspoon": 7},

        # Fats
        "butter": {"cup": 227, "tablespoon": 14, "teaspoon": 4.7, "stick": 113},
        "oil": {"cup": 218, "tablespoon": 13.6, "teaspoon": 4.5},
        "shortening": {"cup": 191, "tablespoon": 12, "teaspoon": 4},

        # Liquids
        "water": {"cup": 227, "tablespoon": 14.2, "teaspoon": 4.7},
        "milk": {"cup": 227, "tablespoon": 14.2, "teaspoon": 4.7},

        # Other common ingredients
        "salt": {"cup": 292, "tablespoon": 18, "teaspoon": 6},
        "baking powder": {"tablespoon": 13.8, "teaspoon": 4.6},
        "baking soda": {"tablespoon": 13.8, "teaspoon": 4.6},
        "yeast (active dry)": {"tablespoon": 8.5, "teaspoon": 2.8},
        "yeast (instant)": {"tablespoon": 8.5, "teaspoon": 2.8},
        "cocoa powder": {"cup": 85, "tablespoon": 5.3, "teaspoon": 1.8},
        "vanilla extract": {"tablespoon": 13, "teaspoon": 4.3},
        "eggs (whole)": {"large": 50, "medium": 44, "extra-large": 56},
    }

    def __init__(self, custom_conversions_file: Optional[str] = None):
        """
        Initialize the conversion manager.

        Args:
            custom_conversions_file: Path to JSON file with custom conversions
        """
        self.conversions = self.DEFAULT_CONVERSIONS.copy()
        self.custom_conversions_file = custom_conversions_file or "custom_conversions.json"
        self.load_custom_conversions()

    def convert_to_grams(self, ingredient: str, amount: float, unit: str) -> Optional[float]:
        """
        Convert an ingredient amount to grams.

        Args:
            ingredient: Name of the ingredient (case-insensitive)
            amount: Amount in the given unit
            unit: Unit of measurement (cup, tablespoon, teaspoon, etc.)

        Returns:
            Amount in grams, or None if conversion not found
        """
        ingredient_lower = ingredient.lower()
        unit_lower = unit.lower()

        # Handle grams directly
        if unit_lower in ["g", "gram", "grams"]:
            return amount

        # Handle ounces
        if unit_lower in ["oz", "ounce", "ounces"]:
            return amount * 28.35

        # Handle pounds
        if unit_lower in ["lb", "lbs", "pound", "pounds"]:
            return amount * 453.592

        # Look up conversion
        if ingredient_lower in self.conversions:
            conversions = self.conversions[ingredient_lower]
            if unit_lower in conversions:
                return amount * conversions[unit_lower]

        return None

    def convert_from_grams(self, ingredient: str, grams: float, unit: str) -> Optional[float]:
        """
        Convert grams to another unit.

        Args:
            ingredient: Name of the ingredient (case-insensitive)
            grams: Amount in grams
            unit: Target unit of measurement

        Returns:
            Amount in target unit, or None if conversion not found
        """
        ingredient_lower = ingredient.lower()
        unit_lower = unit.lower()

        # Handle grams directly
        if unit_lower in ["g", "gram", "grams"]:
            return grams

        # Handle ounces
        if unit_lower in ["oz", "ounce", "ounces"]:
            return grams / 28.35

        # Handle pounds
        if unit_lower in ["lb", "lbs", "pound", "pounds"]:
            return grams / 453.592

        # Look up conversion
        if ingredient_lower in self.conversions:
            conversions = self.conversions[ingredient_lower]
            if unit_lower in conversions:
                return grams / conversions[unit_lower]

        return None

    def add_custom_conversion(self, ingredient: str, unit: str, grams_per_unit: float) -> None:
        """
        Add a custom conversion for an ingredient.

        Args:
            ingredient: Name of the ingredient
            unit: Unit of measurement
            grams_per_unit: How many grams per unit
        """
        ingredient_lower = ingredient.lower()
        unit_lower = unit.lower()

        if ingredient_lower not in self.conversions:
            self.conversions[ingredient_lower] = {}

        self.conversions[ingredient_lower][unit_lower] = grams_per_unit
        self.save_custom_conversions()

    def remove_custom_conversion(self, ingredient: str, unit: Optional[str] = None) -> None:
        """
        Remove a custom conversion.

        Args:
            ingredient: Name of the ingredient
            unit: Specific unit to remove, or None to remove entire ingredient
        """
        ingredient_lower = ingredient.lower()

        if ingredient_lower in self.conversions:
            if unit is None:
                # Remove entire ingredient if it's not in defaults
                if ingredient_lower not in self.DEFAULT_CONVERSIONS:
                    del self.conversions[ingredient_lower]
            else:
                unit_lower = unit.lower()
                if unit_lower in self.conversions[ingredient_lower]:
                    # Only remove if not in defaults
                    if (ingredient_lower not in self.DEFAULT_CONVERSIONS or
                        unit_lower not in self.DEFAULT_CONVERSIONS[ingredient_lower]):
                        del self.conversions[ingredient_lower][unit_lower]

        self.save_custom_conversions()

    def get_available_units(self, ingredient: str) -> list:
        """Get list of available units for an ingredient."""
        ingredient_lower = ingredient.lower()
        if ingredient_lower in self.conversions:
            return list(self.conversions[ingredient_lower].keys())
        return []

    def get_all_ingredients(self) -> list:
        """Get list of all ingredients with conversions."""
        return sorted(self.conversions.keys())

    def save_custom_conversions(self) -> None:
        """Save custom conversions to file."""
        # Only save conversions that aren't in defaults
        custom_only = {}
        for ingredient, units in self.conversions.items():
            if ingredient not in self.DEFAULT_CONVERSIONS:
                custom_only[ingredient] = units
            else:
                # Check for custom units
                for unit, value in units.items():
                    if unit not in self.DEFAULT_CONVERSIONS[ingredient]:
                        if ingredient not in custom_only:
                            custom_only[ingredient] = {}
                        custom_only[ingredient][unit] = value

        try:
            with open(self.custom_conversions_file, 'w') as f:
                json.dump(custom_only, f, indent=2)
        except Exception as e:
            print(f"Error saving custom conversions: {e}")

    def load_custom_conversions(self) -> None:
        """Load custom conversions from file."""
        if os.path.exists(self.custom_conversions_file):
            try:
                with open(self.custom_conversions_file, 'r') as f:
                    custom = json.load(f)
                    for ingredient, units in custom.items():
                        if ingredient not in self.conversions:
                            self.conversions[ingredient] = {}
                        self.conversions[ingredient].update(units)
            except Exception as e:
                print(f"Error loading custom conversions: {e}")
