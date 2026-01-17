"""
Baker's percentage calculator and recipe scaler.
"""

from typing import Dict, Optional
from .models import Ingredient, Recipe
from .conversions import ConversionManager


class BakersCalculator:
    """Calculator for baker's percentages and recipe scaling."""

    def __init__(self, conversion_manager: Optional[ConversionManager] = None):
        """
        Initialize the calculator.

        Args:
            conversion_manager: ConversionManager instance for unit conversions
        """
        self.conversion_manager = conversion_manager or ConversionManager()

    def calculate_percentages(self, recipe: Recipe) -> Recipe:
        """
        Calculate baker's percentages for all ingredients in a recipe.
        Flour is the basis (100%), all other ingredients are percentages of flour.

        Args:
            recipe: Recipe with ingredients in grams

        Returns:
            Recipe with percentages calculated
        """
        # Auto-detect flour weight by summing all ingredients with "flour" in the name
        total_flour = 0.0
        for ingredient in recipe.ingredients.values():
            if "flour" in ingredient.name.lower():
                total_flour += ingredient.amount

        # Use detected flour weight, or fall back to recipe.flour_weight
        flour_basis = total_flour if total_flour > 0 else recipe.flour_weight

        if flour_basis <= 0:
            raise ValueError("Flour weight must be greater than 0 for baker's percentages")

        # Update the recipe's flour weight with the detected value
        recipe.flour_weight = flour_basis

        for ingredient in recipe.ingredients.values():
            ingredient.percentage = (ingredient.amount / flour_basis) * 100

        return recipe

    def scale_recipe_by_flour(self, recipe: Recipe, new_flour_weight: float) -> Recipe:
        """
        Scale a recipe based on a new flour weight.

        Args:
            recipe: Original recipe with baker's percentages
            new_flour_weight: Desired flour weight in grams

        Returns:
            New recipe scaled to the desired flour weight
        """
        if recipe.flour_weight <= 0:
            raise ValueError("Original recipe must have a flour weight")

        scale_factor = new_flour_weight / recipe.flour_weight

        scaled_recipe = Recipe(name=f"{recipe.name} (scaled)", flour_weight=new_flour_weight)

        for name, ingredient in recipe.ingredients.items():
            scaled_amount = ingredient.amount * scale_factor
            scaled_ingredient = Ingredient(
                name=ingredient.name,
                amount=scaled_amount,
                unit="g",
                percentage=ingredient.percentage
            )
            scaled_recipe.add_ingredient(scaled_ingredient)

        return scaled_recipe

    def scale_recipe_by_factor(self, recipe: Recipe, scale_factor: float) -> Recipe:
        """
        Scale a recipe by a multiplier.

        Args:
            recipe: Original recipe
            scale_factor: Multiplier (e.g., 2.0 for double, 0.5 for half)

        Returns:
            New recipe scaled by the factor
        """
        if scale_factor <= 0:
            raise ValueError("Scale factor must be greater than 0")

        scaled_recipe = Recipe(
            name=f"{recipe.name} (×{scale_factor})",
            flour_weight=recipe.flour_weight * scale_factor
        )

        for name, ingredient in recipe.ingredients.items():
            scaled_amount = ingredient.amount * scale_factor
            scaled_ingredient = Ingredient(
                name=ingredient.name,
                amount=scaled_amount,
                unit=ingredient.unit,
                percentage=ingredient.percentage
            )
            scaled_recipe.add_ingredient(scaled_ingredient)

        return scaled_recipe

    def scale_recipe_to_total_weight(self, recipe: Recipe, target_weight: float) -> Recipe:
        """
        Scale a recipe to achieve a specific total weight.

        Args:
            recipe: Original recipe
            target_weight: Desired total weight in grams

        Returns:
            New recipe scaled to target weight
        """
        if target_weight <= 0:
            raise ValueError("Target weight must be greater than 0")

        current_weight = recipe.get_total_weight()
        if current_weight <= 0:
            raise ValueError("Current recipe weight must be greater than 0")

        scale_factor = target_weight / current_weight
        return self.scale_recipe_by_factor(recipe, scale_factor)

    def scale_by_ingredient(self, recipe: Recipe, ingredient_name: str,
                           new_amount: float, new_unit: str = "g") -> Recipe:
        """
        Scale a recipe based on a specific ingredient amount.

        Args:
            recipe: Original recipe
            ingredient_name: Name of ingredient to base scaling on
            new_amount: Desired amount of that ingredient
            new_unit: Unit for the new amount

        Returns:
            New recipe scaled accordingly
        """
        ingredient = recipe.get_ingredient(ingredient_name)
        if not ingredient:
            raise ValueError(f"Ingredient '{ingredient_name}' not found in recipe")

        # Convert new amount to grams if needed
        new_grams = self.conversion_manager.convert_to_grams(
            ingredient_name, new_amount, new_unit
        )

        if new_grams is None:
            # If conversion fails, assume it's already in grams
            if new_unit.lower() in ["g", "gram", "grams"]:
                new_grams = new_amount
            else:
                raise ValueError(f"Cannot convert {new_unit} to grams for {ingredient_name}")

        # Calculate scale factor
        scale_factor = new_grams / ingredient.amount

        return self.scale_recipe_by_factor(recipe, scale_factor)

    def convert_recipe_units(self, recipe: Recipe, target_units: Dict[str, str]) -> Recipe:
        """
        Convert recipe ingredients to different units.

        Args:
            recipe: Recipe to convert
            target_units: Dict mapping ingredient names to desired units

        Returns:
            New recipe with converted units
        """
        converted_recipe = Recipe(
            name=recipe.name,
            flour_weight=recipe.flour_weight
        )

        for name, ingredient in recipe.ingredients.items():
            if name in target_units:
                target_unit = target_units[name]
                # Convert from grams to target unit
                converted_amount = self.conversion_manager.convert_from_grams(
                    name, ingredient.amount, target_unit
                )

                if converted_amount is not None:
                    converted_ingredient = Ingredient(
                        name=ingredient.name,
                        amount=converted_amount,
                        unit=target_unit,
                        percentage=ingredient.percentage
                    )
                else:
                    # If conversion fails, keep original
                    converted_ingredient = Ingredient(
                        name=ingredient.name,
                        amount=ingredient.amount,
                        unit=ingredient.unit,
                        percentage=ingredient.percentage
                    )
            else:
                # Keep original if no target unit specified
                converted_ingredient = Ingredient(
                    name=ingredient.name,
                    amount=ingredient.amount,
                    unit=ingredient.unit,
                    percentage=ingredient.percentage
                )

            converted_recipe.add_ingredient(converted_ingredient)

        return converted_recipe

    def add_ingredient_to_recipe(self, recipe: Recipe, name: str, amount: float,
                                unit: str, is_flour: bool = False) -> Recipe:
        """
        Add an ingredient to a recipe with automatic unit conversion to grams.

        Args:
            recipe: Recipe to add ingredient to
            name: Ingredient name
            amount: Amount in the given unit
            unit: Unit of measurement
            is_flour: Whether this is flour (affects baker's percentages)

        Returns:
            Updated recipe
        """
        # Convert to grams
        grams = self.conversion_manager.convert_to_grams(name, amount, unit)

        if grams is None:
            # If conversion fails, assume it's already in grams
            if unit.lower() in ["g", "gram", "grams"]:
                grams = amount
            else:
                raise ValueError(f"Cannot convert {unit} to grams for {name}")

        ingredient = Ingredient(name=name, amount=grams, unit="g")
        recipe.add_ingredient(ingredient)

        # Update flour weight if this is flour
        if is_flour:
            recipe.flour_weight += grams

        return recipe

    def create_recipe_from_percentages(self, name: str, flour_weight: float,
                                      percentages: Dict[str, float]) -> Recipe:
        """
        Create a recipe from baker's percentages.

        Args:
            name: Recipe name
            flour_weight: Weight of flour in grams (100% basis)
            percentages: Dict of ingredient names to percentages

        Returns:
            Complete recipe with amounts calculated
        """
        recipe = Recipe(name=name, flour_weight=flour_weight)

        # Add flour first
        flour_ingredient = Ingredient(
            name="flour",
            amount=flour_weight,
            unit="g",
            percentage=100.0
        )
        recipe.add_ingredient(flour_ingredient)

        # Add other ingredients based on percentages
        for ingredient_name, percentage in percentages.items():
            if ingredient_name.lower() != "flour":
                amount = (percentage / 100.0) * flour_weight
                ingredient = Ingredient(
                    name=ingredient_name,
                    amount=amount,
                    unit="g",
                    percentage=percentage
                )
                recipe.add_ingredient(ingredient)

        return recipe
