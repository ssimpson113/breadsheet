"""
Data models for ingredients and recipes.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Ingredient:
    """Represents a single ingredient in a recipe."""

    name: str
    amount: float
    unit: str
    percentage: Optional[float] = None  # Baker's percentage

    def __str__(self) -> str:
        if self.percentage is not None:
            return f"{self.name}: {self.amount:.2f} {self.unit} ({self.percentage:.1f}%)"
        return f"{self.name}: {self.amount:.2f} {self.unit}"


@dataclass
class Recipe:
    """Represents a complete recipe with multiple ingredients."""

    name: str
    ingredients: Dict[str, Ingredient] = field(default_factory=dict)
    flour_weight: float = 0.0  # Total flour weight (basis for percentages)

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """Add an ingredient to the recipe."""
        self.ingredients[ingredient.name] = ingredient

    def remove_ingredient(self, name: str) -> None:
        """Remove an ingredient from the recipe."""
        if name in self.ingredients:
            del self.ingredients[name]

    def get_ingredient(self, name: str) -> Optional[Ingredient]:
        """Get an ingredient by name."""
        return self.ingredients.get(name)

    def get_total_weight(self) -> float:
        """Calculate total recipe weight in grams."""
        total = 0.0
        for ingredient in self.ingredients.values():
            # All calculations should be in grams
            total += ingredient.amount
        return total

    def __str__(self) -> str:
        lines = [f"Recipe: {self.name}"]
        lines.append(f"Flour weight: {self.flour_weight:.2f}g")
        lines.append("Ingredients:")
        for ingredient in self.ingredients.values():
            lines.append(f"  {ingredient}")
        lines.append(f"Total weight: {self.get_total_weight():.2f}g")
        return "\n".join(lines)
