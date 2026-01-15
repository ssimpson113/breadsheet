"""
Basic tests for Breadsheet functionality
Run with: pytest test_breadsheet.py
"""

import pytest
from breadsheet import BakersCalculator, ConversionManager, Ingredient, Recipe


class TestConversionManager:
    """Tests for unit conversion system."""

    def test_convert_to_grams_flour(self):
        """Test converting flour from cups to grams."""
        cm = ConversionManager()
        result = cm.convert_to_grams("all-purpose flour", 1, "cup")
        assert result == 120

    def test_convert_from_grams_sugar(self):
        """Test converting sugar from grams to cups."""
        cm = ConversionManager()
        result = cm.convert_from_grams("granulated sugar", 200, "cup")
        assert result == 1.0

    def test_add_custom_conversion(self):
        """Test adding a custom conversion."""
        cm = ConversionManager()
        cm.add_custom_conversion("custom ingredient", "cup", 150)
        result = cm.convert_to_grams("custom ingredient", 1, "cup")
        assert result == 150

    def test_get_available_units(self):
        """Test getting available units for an ingredient."""
        cm = ConversionManager()
        units = cm.get_available_units("all-purpose flour")
        assert "cup" in units
        assert "tablespoon" in units


class TestRecipe:
    """Tests for Recipe model."""

    def test_add_ingredient(self):
        """Test adding an ingredient to a recipe."""
        recipe = Recipe(name="Test Recipe")
        ingredient = Ingredient(name="flour", amount=500, unit="g")
        recipe.add_ingredient(ingredient)

        assert "flour" in recipe.ingredients
        assert recipe.ingredients["flour"].amount == 500

    def test_get_total_weight(self):
        """Test calculating total recipe weight."""
        recipe = Recipe(name="Test Recipe")
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g"))
        recipe.add_ingredient(Ingredient(name="water", amount=350, unit="g"))
        recipe.add_ingredient(Ingredient(name="salt", amount=10, unit="g"))

        assert recipe.get_total_weight() == 860

    def test_remove_ingredient(self):
        """Test removing an ingredient from a recipe."""
        recipe = Recipe(name="Test Recipe")
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g"))
        recipe.remove_ingredient("flour")

        assert "flour" not in recipe.ingredients


class TestBakersCalculator:
    """Tests for baker's percentage calculations."""

    def test_calculate_percentages(self):
        """Test calculating baker's percentages."""
        calc = BakersCalculator()
        recipe = Recipe(name="Test Bread", flour_weight=500)
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g"))
        recipe.add_ingredient(Ingredient(name="water", amount=350, unit="g"))
        recipe.add_ingredient(Ingredient(name="salt", amount=10, unit="g"))

        result = calc.calculate_percentages(recipe)

        assert result.ingredients["flour"].percentage == 100
        assert result.ingredients["water"].percentage == 70
        assert result.ingredients["salt"].percentage == 2

    def test_scale_recipe_by_flour(self):
        """Test scaling a recipe by flour weight."""
        calc = BakersCalculator()
        recipe = Recipe(name="Test Bread", flour_weight=500)
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g", percentage=100))
        recipe.add_ingredient(Ingredient(name="water", amount=350, unit="g", percentage=70))

        scaled = calc.scale_recipe_by_flour(recipe, 1000)

        assert scaled.flour_weight == 1000
        assert scaled.ingredients["flour"].amount == 1000
        assert scaled.ingredients["water"].amount == 700

    def test_scale_recipe_by_factor(self):
        """Test scaling a recipe by a multiplier."""
        calc = BakersCalculator()
        recipe = Recipe(name="Test Bread", flour_weight=500)
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g"))
        recipe.add_ingredient(Ingredient(name="water", amount=350, unit="g"))

        scaled = calc.scale_recipe_by_factor(recipe, 2.0)

        assert scaled.flour_weight == 1000
        assert scaled.ingredients["flour"].amount == 1000
        assert scaled.ingredients["water"].amount == 700

    def test_scale_recipe_to_total_weight(self):
        """Test scaling a recipe to a target total weight."""
        calc = BakersCalculator()
        recipe = Recipe(name="Test Bread", flour_weight=500)
        recipe.add_ingredient(Ingredient(name="flour", amount=500, unit="g"))
        recipe.add_ingredient(Ingredient(name="water", amount=350, unit="g"))
        recipe.add_ingredient(Ingredient(name="salt", amount=10, unit="g"))
        # Total: 860g

        scaled = calc.scale_recipe_to_total_weight(recipe, 1720)

        assert scaled.get_total_weight() == pytest.approx(1720, rel=0.01)

    def test_create_recipe_from_percentages(self):
        """Test creating a recipe from baker's percentages."""
        calc = BakersCalculator()
        percentages = {
            "water": 70,
            "salt": 2,
            "yeast": 1
        }

        recipe = calc.create_recipe_from_percentages("Test Bread", 500, percentages)

        assert recipe.flour_weight == 500
        assert recipe.ingredients["flour"].amount == 500
        assert recipe.ingredients["water"].amount == 350
        assert recipe.ingredients["salt"].amount == 10
        assert recipe.ingredients["yeast"].amount == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
