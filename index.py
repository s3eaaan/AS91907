"""Present meals and calculate calories."""

import tkinter as tk

from calculator import CalcFunc
from meal import MealFunc
from menus import menus

# Constants and Globals
ALL_MENUS = [
    menus["breakfast_menu"],
    menus["morning_tea_menu"],
    menus["lunch_menu"],
    menus["dessert_menu"],
    menus["dinner_menu"],
]
charts = None

# Initialize root window
root = tk.Tk()
root.minsize(350, 300)

# Frames
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side='left', fill='y', expand=False)

right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.pack(side='left', fill='both', expand=True)

# Filter dropdown box function


def meat_type_func(*menus):
    """Extract unique meat types from provided menus."""
    try:
        meat_type = set()
        for each_menu in menus:
            for meal in each_menu.values():
                meat_type.add(meal['meat'])
        # "None" is always the starting option
        return ['None'] + sorted(meat_type - {'None'})
    except Exception:
        results.config(
            text='An error occurred during the filtering. \nPlease try again.'
        )
        return None


meat_types = [meat_type_func(each_menu)  # Get meat types for each menu
              for each_menu in ALL_MENUS]

# Runs MealFunc class on every meal
breakfast = MealFunc(
    left_frame, "Preference     -------     Breakfast:",
    menus["breakfast_menu"], meat_types[0])
morning_tea = MealFunc(
    left_frame, "Preference     -------     Morning Tea:",
    menus["morning_tea_menu"], meat_types[1])
lunch = MealFunc(
    left_frame, "Preference     -------     Lunch:",
    menus["lunch_menu"], meat_types[2])
dessert = MealFunc(
    left_frame, "Preference     -------     Dessert:",
    menus["dessert_menu"], meat_types[3])
dinner = MealFunc(
    left_frame, "Preference     -------     Dinner:",
    menus["dinner_menu"], meat_types[4])

# Get meat and meal selections
breakfast_meat, selected_breakfast = breakfast.selections()
morning_tea_meat, selected_morning_tea = morning_tea.selections()
lunch_meat, selected_lunch = lunch.selections()
dessert_meat, selected_dessert = dessert.selections()
dinner_meat, selected_dinner = dinner.selections()

# Lists for selected meats and meals
selected_meats = [
    breakfast_meat,
    morning_tea_meat,
    lunch_meat,
    dessert_meat,
    dinner_meat,
]
selected_meals = [
    selected_breakfast,
    selected_morning_tea,
    selected_lunch,
    selected_dessert,
    selected_dinner,
]

# Result label
results = tk.Label(left_frame, text="")
results.pack()


def calculation_and_graph():
    """Run the calculation section."""
    global charts
    calculator = CalcFunc(
        charts, ALL_MENUS, selected_meals, results, right_frame, root
    )
    charts = calculator.calculation_and_graph()


# Calculate button
tk.Button(left_frame, text="Calculate Nutrition",
          command=calculation_and_graph).pack()

# Mainloop
root.mainloop()
