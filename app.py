"""
Breadsheet - Baking Calculator with Baker's Percentages
Streamlit GUI Application
"""

import streamlit as st
from breadsheet import BakersCalculator, ConversionManager, Ingredient, Recipe

# Page configuration
st.set_page_config(
    page_title="Breadsheet - Baking Calculator",
    page_icon="🍞",
    layout="wide",
)

# Initialize session state
if "calculator" not in st.session_state:
    st.session_state.calculator = BakersCalculator()

if "current_recipe" not in st.session_state:
    st.session_state.current_recipe = Recipe(name="My Recipe")

if "conversion_manager" not in st.session_state:
    st.session_state.conversion_manager = ConversionManager()


def main():
    st.title("🍞 Breadsheet - Baking Calculator")
    st.markdown("*Baker's percentages, scaling, and unit conversions made easy*")

    # Create tabs for different functions
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Recipe Builder",
        "📊 Baker's Percentages",
        "⚖️ Scale Recipe",
        "📋 Recipe Converter",
        "🔄 Unit Converter",
        "➕ Custom Conversions"
    ])

    with tab1:
        recipe_builder_tab()

    with tab2:
        bakers_percentage_tab()

    with tab3:
        scale_recipe_tab()

    with tab4:
        recipe_converter_tab()

    with tab5:
        unit_converter_tab()

    with tab6:
        custom_conversions_tab()


def recipe_builder_tab():
    """Tab for building and editing recipes."""
    st.header("Recipe Builder")

    col1, col2 = st.columns([2, 1])

    with col1:
        recipe_name = st.text_input(
            "Recipe Name",
            value=st.session_state.current_recipe.name,
            key="recipe_name"
        )
        st.session_state.current_recipe.name = recipe_name

        st.subheader("Add Ingredient")

        add_col1, add_col2, add_col3, add_col4 = st.columns([2, 1, 1, 1])

        with add_col1:
            # Ingredient selector with autocomplete
            all_ingredients = st.session_state.conversion_manager.get_all_ingredients()
            ingredient_name = st.selectbox(
                "Ingredient",
                options=[""] + all_ingredients + ["-- Custom --"],
                key="add_ingredient_name"
            )

            if ingredient_name == "-- Custom --":
                ingredient_name = st.text_input("Custom ingredient name", key="custom_ingredient_name")

        with add_col2:
            amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0, key="add_amount")

        with add_col3:
            # Get available units for selected ingredient
            if ingredient_name and ingredient_name != "-- Custom --":
                available_units = st.session_state.conversion_manager.get_available_units(ingredient_name)
                available_units = available_units + ["g", "oz", "lb"]
                default_units = list(set(available_units))  # Remove duplicates
            else:
                default_units = ["g", "cup", "tablespoon", "teaspoon", "oz", "lb"]

            unit = st.selectbox("Unit", options=default_units, key="add_unit")

        with add_col4:
            is_flour = st.checkbox("Is Flour?", key="is_flour")

        if st.button("➕ Add Ingredient", type="primary"):
            if ingredient_name and ingredient_name not in ["", "-- Custom --"]:
                try:
                    st.session_state.calculator.add_ingredient_to_recipe(
                        st.session_state.current_recipe,
                        ingredient_name,
                        amount,
                        unit,
                        is_flour=is_flour
                    )
                    st.success(f"Added {ingredient_name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding ingredient: {e}")
            else:
                st.warning("Please enter an ingredient name")

    with col2:
        st.subheader("Current Recipe")

        if st.session_state.current_recipe.ingredients:
            st.markdown(f"**{st.session_state.current_recipe.name}**")
            st.markdown(f"*Flour weight: {st.session_state.current_recipe.flour_weight:.1f}g*")

            for name, ingredient in st.session_state.current_recipe.ingredients.items():
                cols = st.columns([3, 1])
                with cols[0]:
                    st.text(f"{ingredient.name}: {ingredient.amount:.1f}{ingredient.unit}")
                with cols[1]:
                    if st.button("🗑️", key=f"remove_{name}"):
                        st.session_state.current_recipe.remove_ingredient(name)
                        st.rerun()

            st.markdown("---")
            st.markdown(f"**Total: {st.session_state.current_recipe.get_total_weight():.1f}g**")

            if st.button("🗑️ Clear Recipe", type="secondary"):
                st.session_state.current_recipe = Recipe(name="My Recipe")
                st.rerun()
        else:
            st.info("No ingredients added yet")


def bakers_percentage_tab():
    """Tab for calculating and displaying baker's percentages."""
    st.header("Baker's Percentages")

    if not st.session_state.current_recipe.ingredients:
        st.warning("Please add ingredients to your recipe first (Recipe Builder tab)")
        return

    if st.session_state.current_recipe.flour_weight <= 0:
        st.warning("Please add flour to your recipe and mark it as 'Is Flour?' when adding")
        return

    # Calculate percentages
    try:
        recipe_with_percentages = st.session_state.calculator.calculate_percentages(
            st.session_state.current_recipe
        )

        st.subheader(f"📊 {recipe_with_percentages.name}")
        st.markdown(f"*Flour basis: {recipe_with_percentages.flour_weight:.1f}g (100%)*")

        # Display as table
        data = []
        for ingredient in recipe_with_percentages.ingredients.values():
            data.append({
                "Ingredient": ingredient.name,
                "Amount": f"{ingredient.amount:.1f}g",
                "Percentage": f"{ingredient.percentage:.1f}%"
            })

        st.table(data)

        # Calculate hydration (liquids as % of flour)
        liquid_ingredients = ["water", "milk", "cream", "buttermilk", "oil", "yogurt",
                             "honey", "maple syrup", "molasses", "eggs"]
        total_liquid = 0.0
        for ingredient in recipe_with_percentages.ingredients.values():
            # Check if ingredient name contains any liquid keywords
            if any(liquid in ingredient.name.lower() for liquid in liquid_ingredients):
                total_liquid += ingredient.amount

        hydration = (total_liquid / recipe_with_percentages.flour_weight) * 100 if recipe_with_percentages.flour_weight > 0 else 0

        st.markdown("---")
        st.markdown(f"**Total Weight:** {recipe_with_percentages.get_total_weight():.1f}g")
        st.markdown(f"**Total Percentage:** {sum(i.percentage for i in recipe_with_percentages.ingredients.values()):.1f}%")
        st.markdown(f"**Hydration:** {hydration:.1f}% ({total_liquid:.1f}g liquid)")

    except Exception as e:
        st.error(f"Error calculating percentages: {e}")


def scale_recipe_tab():
    """Tab for scaling recipes."""
    st.header("Scale Recipe")

    if not st.session_state.current_recipe.ingredients:
        st.warning("Please add ingredients to your recipe first (Recipe Builder tab)")
        return

    # Calculate percentages first
    try:
        recipe = st.session_state.calculator.calculate_percentages(
            st.session_state.current_recipe
        )
    except Exception as e:
        st.error(f"Error: {e}")
        return

    scaling_method = st.radio(
        "Scaling Method",
        ["By Flour Weight", "By Scale Factor", "By Total Weight", "By Specific Ingredient"],
        horizontal=True
    )

    scaled_recipe = None

    if scaling_method == "By Flour Weight":
        new_flour_weight = st.number_input(
            "New Flour Weight (g)",
            min_value=1.0,
            value=recipe.flour_weight * 2,
            step=50.0
        )

        if st.button("Scale Recipe"):
            try:
                scaled_recipe = st.session_state.calculator.scale_recipe_by_flour(
                    recipe, new_flour_weight
                )
            except Exception as e:
                st.error(f"Error: {e}")

    elif scaling_method == "By Scale Factor":
        scale_factor = st.number_input(
            "Scale Factor (e.g., 2 for double, 0.5 for half)",
            min_value=0.1,
            value=2.0,
            step=0.1
        )

        if st.button("Scale Recipe"):
            try:
                scaled_recipe = st.session_state.calculator.scale_recipe_by_factor(
                    recipe, scale_factor
                )
            except Exception as e:
                st.error(f"Error: {e}")

    elif scaling_method == "By Total Weight":
        target_weight = st.number_input(
            "Target Total Weight (g)",
            min_value=1.0,
            value=recipe.get_total_weight() * 2,
            step=100.0
        )

        if st.button("Scale Recipe"):
            try:
                scaled_recipe = st.session_state.calculator.scale_recipe_to_total_weight(
                    recipe, target_weight
                )
            except Exception as e:
                st.error(f"Error: {e}")

    elif scaling_method == "By Specific Ingredient":
        ingredient_names = list(recipe.ingredients.keys())
        selected_ingredient = st.selectbox("Select Ingredient", ingredient_names)

        col1, col2 = st.columns(2)
        with col1:
            new_amount = st.number_input("New Amount", min_value=0.1, value=200.0, step=10.0)
        with col2:
            available_units = st.session_state.conversion_manager.get_available_units(selected_ingredient)
            available_units = list(set(available_units + ["g", "oz", "lb"]))
            new_unit = st.selectbox("Unit", available_units)

        if st.button("Scale Recipe"):
            try:
                scaled_recipe = st.session_state.calculator.scale_by_ingredient(
                    recipe, selected_ingredient, new_amount, new_unit
                )
            except Exception as e:
                st.error(f"Error: {e}")

    # Display scaled recipe
    if scaled_recipe:
        st.success("Recipe scaled successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Recipe")
            display_recipe(recipe)

        with col2:
            st.subheader("Scaled Recipe")
            display_recipe(scaled_recipe)

            if st.button("Use Scaled Recipe"):
                st.session_state.current_recipe = scaled_recipe
                st.success("Scaled recipe is now your current recipe!")
                st.rerun()


def recipe_converter_tab():
    """Tab for converting entire recipe to volume or imperial measurements."""
    st.header("Recipe Converter")
    st.markdown("*Convert your entire recipe to cups, tablespoons, or ounces for people who don't use a scale*")

    if not st.session_state.current_recipe.ingredients:
        st.warning("Please add ingredients to your recipe first (Recipe Builder tab)")
        return

    st.subheader(f"📋 {st.session_state.current_recipe.name}")

    # Choose conversion system
    conversion_system = st.radio(
        "Convert to:",
        ["Volume (Cups & Spoons)", "Imperial Weight (Ounces)", "Metric (Grams - Original)"],
        horizontal=True
    )

    st.markdown("---")

    # Create converted recipe display
    converted_data = []
    cannot_convert = []

    for ingredient in st.session_state.current_recipe.ingredients.values():
        ingredient_name = ingredient.name
        amount_grams = ingredient.amount

        if conversion_system == "Metric (Grams - Original)":
            # Just show original
            converted_data.append({
                "Ingredient": ingredient_name,
                "Amount": f"{amount_grams:.1f}g"
            })

        elif conversion_system == "Imperial Weight (Ounces)":
            # Convert to ounces
            ounces = st.session_state.conversion_manager.convert_from_grams(
                ingredient_name, amount_grams, "oz"
            )
            if ounces is not None:
                # Also show pounds if >= 16 oz
                if ounces >= 16:
                    pounds = ounces / 16
                    remaining_oz = ounces % 16
                    if remaining_oz > 0.1:
                        converted_data.append({
                            "Ingredient": ingredient_name,
                            "Amount": f"{pounds:.0f} lb {remaining_oz:.1f} oz ({ounces:.1f} oz)"
                        })
                    else:
                        converted_data.append({
                            "Ingredient": ingredient_name,
                            "Amount": f"{pounds:.1f} lb ({ounces:.1f} oz)"
                        })
                else:
                    converted_data.append({
                        "Ingredient": ingredient_name,
                        "Amount": f"{ounces:.1f} oz"
                    })
            else:
                converted_data.append({
                    "Ingredient": ingredient_name,
                    "Amount": f"{amount_grams:.1f}g (no conversion)"
                })
                cannot_convert.append(ingredient_name)

        elif conversion_system == "Volume (Cups & Spoons)":
            # Try to convert to the best volume unit
            cups = st.session_state.conversion_manager.convert_from_grams(
                ingredient_name, amount_grams, "cup"
            )

            if cups is not None:
                # Determine best display format
                if cups >= 1:
                    # Show cups
                    whole_cups = int(cups)
                    remaining = cups - whole_cups

                    if remaining >= 0.75:
                        result = f"{whole_cups + 1} cups"
                    elif remaining >= 0.66:
                        result = f"{whole_cups} ¾ cups" if whole_cups > 0 else "¾ cup"
                    elif remaining >= 0.5:
                        result = f"{whole_cups} ½ cups" if whole_cups > 0 else "½ cup"
                    elif remaining >= 0.33:
                        result = f"{whole_cups} ⅓ cups" if whole_cups > 0 else "⅓ cup"
                    elif remaining >= 0.25:
                        result = f"{whole_cups} ¼ cups" if whole_cups > 0 else "¼ cup"
                    elif whole_cups > 0:
                        result = f"{whole_cups} cup{'s' if whole_cups > 1 else ''}"
                    else:
                        # Less than 1/4 cup, show in tablespoons
                        tbsp = st.session_state.conversion_manager.convert_from_grams(
                            ingredient_name, amount_grams, "tablespoon"
                        )
                        if tbsp:
                            result = f"{tbsp:.1f} tbsp"
                        else:
                            result = f"{cups:.2f} cups"

                    converted_data.append({
                        "Ingredient": ingredient_name,
                        "Amount": result
                    })
                elif cups >= 0.25:
                    # Between 1/4 and 1 cup
                    if cups >= 0.75:
                        result = "¾ cup"
                    elif cups >= 0.66:
                        result = "⅔ cup"
                    elif cups >= 0.5:
                        result = "½ cup"
                    elif cups >= 0.33:
                        result = "⅓ cup"
                    else:
                        result = "¼ cup"

                    converted_data.append({
                        "Ingredient": ingredient_name,
                        "Amount": result
                    })
                else:
                    # Less than 1/4 cup, try tablespoons
                    tbsp = st.session_state.conversion_manager.convert_from_grams(
                        ingredient_name, amount_grams, "tablespoon"
                    )

                    if tbsp is not None:
                        if tbsp >= 1:
                            converted_data.append({
                                "Ingredient": ingredient_name,
                                "Amount": f"{tbsp:.1f} tbsp"
                            })
                        else:
                            # Try teaspoons
                            tsp = st.session_state.conversion_manager.convert_from_grams(
                                ingredient_name, amount_grams, "teaspoon"
                            )
                            if tsp:
                                converted_data.append({
                                    "Ingredient": ingredient_name,
                                    "Amount": f"{tsp:.1f} tsp"
                                })
                            else:
                                converted_data.append({
                                    "Ingredient": ingredient_name,
                                    "Amount": f"{tbsp:.2f} tbsp"
                                })
                    else:
                        converted_data.append({
                            "Ingredient": ingredient_name,
                            "Amount": f"{amount_grams:.1f}g (no conversion)"
                        })
                        cannot_convert.append(ingredient_name)
            else:
                # No cup conversion available, show in grams
                converted_data.append({
                    "Ingredient": ingredient_name,
                    "Amount": f"{amount_grams:.1f}g (no conversion)"
                })
                cannot_convert.append(ingredient_name)

    # Display the converted recipe
    st.table(converted_data)

    # Show warnings for items that couldn't be converted
    if cannot_convert:
        st.warning(f"⚠️ Could not convert: {', '.join(cannot_convert)}. Add custom conversions in the Custom Conversions tab.")

    # Add helpful notes
    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("- Volume measurements are less accurate than weight - results may vary")
    st.markdown("- For best results, use a kitchen scale and measure in grams")
    st.markdown("- Common fractions are shown for easier measuring (¼, ⅓, ½, ¾)")


def unit_converter_tab():
    """Tab for converting between units."""
    st.header("Unit Converter")

    st.markdown("Convert between different units for baking ingredients")

    col1, col2, col3 = st.columns(3)

    with col1:
        all_ingredients = st.session_state.conversion_manager.get_all_ingredients()
        ingredient = st.selectbox("Ingredient", all_ingredients)

    with col2:
        from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)
        from_unit = st.selectbox(
            "From Unit",
            st.session_state.conversion_manager.get_available_units(ingredient) + ["g", "oz", "lb"]
        )

    with col3:
        to_unit = st.selectbox(
            "To Unit",
            st.session_state.conversion_manager.get_available_units(ingredient) + ["g", "oz", "lb"],
            key="to_unit_select"
        )

    if st.button("Convert"):
        try:
            # First convert to grams
            grams = st.session_state.conversion_manager.convert_to_grams(
                ingredient, from_amount, from_unit
            )

            if grams is None:
                st.error("Conversion not available")
            else:
                # Then convert from grams to target unit
                result = st.session_state.conversion_manager.convert_from_grams(
                    ingredient, grams, to_unit
                )

                if result is None:
                    st.error("Conversion not available")
                else:
                    st.success(f"**{from_amount} {from_unit}** of {ingredient} = **{result:.2f} {to_unit}**")
                    st.info(f"(= {grams:.2f}g)")

        except Exception as e:
            st.error(f"Error: {e}")


def custom_conversions_tab():
    """Tab for managing custom conversions."""
    st.header("Custom Conversions")

    st.markdown("Add your own ingredient conversions or modify existing ones")

    # Add new conversion
    st.subheader("Add Custom Conversion")

    col1, col2, col3 = st.columns(3)

    with col1:
        custom_ingredient = st.text_input("Ingredient Name")

    with col2:
        custom_unit = st.text_input("Unit (e.g., 'cup', 'tablespoon')")

    with col3:
        grams_per_unit = st.number_input("Grams per Unit", min_value=0.1, value=100.0, step=1.0)

    if st.button("Add Conversion"):
        if custom_ingredient and custom_unit:
            try:
                st.session_state.conversion_manager.add_custom_conversion(
                    custom_ingredient, custom_unit, grams_per_unit
                )
                st.success(f"Added: 1 {custom_unit} of {custom_ingredient} = {grams_per_unit}g")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill in all fields")

    # Display existing conversions
    st.subheader("All Available Conversions")

    all_ingredients = st.session_state.conversion_manager.get_all_ingredients()

    # Filter
    filter_text = st.text_input("Filter ingredients", "")

    filtered_ingredients = [
        ing for ing in all_ingredients
        if filter_text.lower() in ing.lower()
    ]

    for ingredient in filtered_ingredients:
        with st.expander(f"📦 {ingredient}"):
            units = st.session_state.conversion_manager.get_available_units(ingredient)

            for unit in units:
                conversions = st.session_state.conversion_manager.conversions[ingredient]
                grams = conversions[unit]

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"1 {unit} = {grams}g")
                with col2:
                    # Only allow deletion of custom conversions
                    is_default = (ingredient in ConversionManager.DEFAULT_CONVERSIONS and
                                unit in ConversionManager.DEFAULT_CONVERSIONS.get(ingredient, {}))

                    if not is_default:
                        if st.button("🗑️", key=f"del_{ingredient}_{unit}"):
                            st.session_state.conversion_manager.remove_custom_conversion(
                                ingredient, unit
                            )
                            st.rerun()


def display_recipe(recipe: Recipe):
    """Helper function to display a recipe."""
    st.markdown(f"**{recipe.name}**")

    if recipe.flour_weight > 0:
        st.markdown(f"*Flour: {recipe.flour_weight:.1f}g*")

    data = []
    for ingredient in recipe.ingredients.values():
        row = {
            "Ingredient": ingredient.name,
            "Amount": f"{ingredient.amount:.1f}g"
        }
        if ingredient.percentage:
            row["Percentage"] = f"{ingredient.percentage:.1f}%"
        data.append(row)

    st.table(data)

    st.markdown(f"**Total:** {recipe.get_total_weight():.1f}g")


if __name__ == "__main__":
    main()
