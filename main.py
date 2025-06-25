import tkinter as tk
import json
import os
from calculator import CalcFunc
from meal import MealFunc

with open('menus.json', 'r') as f:
    menus = json.load(f)

def save_selections():
    selections = [var.get() for var in selected_meals]
    with open('last_selections.json', 'w') as f:
        json.dump(selections, f)

def load_selections():
    if os.path.exists('last_selections.json'):
        with open('last_selections.json', 'r') as f:
            try:
                selections = json.load(f)
                for var, value in zip(selected_meals, selections):
                    var.set(value)
            except Exception:
                pass

ALL_MENUS = [
    menus["breakfast_menu"],
    menus["morning_tea_menu"],
    menus["lunch_menu"],
    menus["dessert_menu"],
    menus["dinner_menu"],
]

def meat_type_func(menu):
    """Extract unique meat types from provided menu."""
    try:
        meat_type = set()
        for meal in menu.values():
            meat_type.add(meal['meat'])
        return ['None'] + sorted(meat_type - {'None'})
    except Exception as e:
        print("meat_type_func error:", e)
        return ['None']

meat_types = [meat_type_func(each_menu) for each_menu in ALL_MENUS]

charts = None

root = tk.Tk()
root.minsize(350, 300)

main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side='left', fill='y', expand=False)

right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.pack(side='left', fill='both', expand=True)

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

breakfast_meat, selected_breakfast = breakfast.selections()
morning_tea_meat, selected_morning_tea = morning_tea.selections()
lunch_meat, selected_lunch = lunch.selections()
dessert_meat, selected_dessert = dessert.selections()
dinner_meat, selected_dinner = dinner.selections()

selected_meats = [breakfast_meat, morning_tea_meat, lunch_meat,
                  dessert_meat, dinner_meat,]

selected_meals = [selected_breakfast, selected_morning_tea, selected_lunch,
                  selected_dessert, selected_dinner,]


def on_selection_change(*args):
    """Save selections for data persist"""
    save_selections()

for var in selected_meals:
    var.trace_add('write', on_selection_change)

load_selections()

results = tk.Label(left_frame, text="")
results.pack()

bottom_left_frame = tk.Frame(left_frame)
bottom_left_frame.pack(fill='x')

extra_entries = []


def calculation_and_graph():
    """Run calculations for nutrients"""
    global charts
    calculator = CalcFunc(charts, ALL_MENUS, selected_meals,
                          results, right_frame, root)
    charts = calculator.calculation_and_graph()
    save_selections()


def hide_charts():
    global charts
    if charts is not None:
        try:
            charts.get_tk_widget().destroy()
        except Exception:
            pass
        charts = None


def custom_meal():
    """Make the frame for custom meal section."""
    hide_charts()
    custom_meal.inputs_frame = tk.Frame(right_frame, bg='#e0e0e0')
    custom_meal.inputs_frame.pack(fill='x', pady=20, padx=20)

    # Input boxes
    labels = ["Name", "Calories", "Protein", "Fats", "Carbs"]
    global extra_entries
    extra_entries = []
    for i, macro_name in enumerate(labels):  # print key and value
        label = tk.Label(custom_meal.inputs_frame, text=f"{macro_name}:", bg='#e0e0e0')
        label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(custom_meal.inputs_frame)  # Input box
        entry.grid(row=i, column=1, padx=5, pady=2)
        extra_entries.append(entry)  # Add to list of custom meals

    menu_names = ["Breakfast", "Morning Tea", "Lunch",
                  "Dessert","Dinner"]

    global menu_choice_var
    menu_choice_var = tk.StringVar()
    menu_choice_var.set(menu_names[0])  # defolt choice is bfast

    # Dropdown boxes and labels
    menu_label = tk.Label(custom_meal.inputs_frame, text="Add to menu:", bg='#e0e0e0')
    menu_label.grid(row=len(labels), column=0, sticky='e', padx=5, pady=2)
    menu_dropdown = tk.OptionMenu(custom_meal.inputs_frame, menu_choice_var, *menu_names)
    menu_dropdown.grid(row=len(labels), column=1, padx=5, pady=2)

    # Submit button
    submit = tk.Button(custom_meal.inputs_frame,
                       text="Submit",command=process_inputs)
    submit.grid(row=len(labels) + 1, 
                column=0, columnspan=2, pady=(10, 2))

    def close_inputs():
        toggle_extra_inputs(shown=True)

    # Close inputs button
    close = tk.Button(custom_meal.inputs_frame,
                      text="Close Inputs", command=close_inputs)
    close.grid(row=len(labels) + 2, 
               column=0, columnspan=2, pady=(2, 10))


def process_inputs():
    """Process custom information"""
    name = extra_entries[0].get().strip()  # remove whitespace
    calories = extra_entries[1].get().strip()
    protein = extra_entries[2].get().strip()
    fats = extra_entries[3].get().strip()
    carbs = extra_entries[4].get().strip()
    if not name:  # if name is left blank
        results.config(text="Please enter a name for the meal.")
        return
    try:  #if values meet corresponding data typ
        meal_info = {
            "calories": int(calories),
            "fats": int(fats),
            "carbs": int(carbs),
            "protein": int(protein),
            "meat": "None"
        }
    except ValueError:  # if incorect data type
        results.config(text="ONLY NUMBERS for nutritional values.")
        return

    selected_menu_display = menu_choice_var.get()
    menu_key_lookup = {
        "Breakfast": "breakfast_menu",
        "Morning Tea": "morning_tea_menu",
        "Lunch": "lunch_menu",
        "Dessert": "dessert_menu",
        "Dinner": "dinner_menu"
    }
    menu_key = menu_key_lookup[selected_menu_display]  # dropdown box for meal type
    display_string = f"{name.upper()} (CUSTOM)\n\n Calories: {meal_info['calories']} | Protein: {meal_info['protein']}g | Fats: {meal_info['fats']}g"
    menus[menu_key][display_string] = meal_info
    with open('menus.json', 'w') as f:  # save new selections
        json.dump(menus, f, indent=4)
    results.config(text=f"Customised meal '{name}' added to {selected_menu_display} menu.")

    # Update the chosen menu
    if menu_key == "breakfast_menu":
        breakfast.update_menu_options(menus["breakfast_menu"])
    elif menu_key == "morning_tea_menu":
        morning_tea.update_menu_options(menus["morning_tea_menu"])
    elif menu_key == "lunch_menu":
        lunch.update_menu_options(menus["lunch_menu"])
    elif menu_key == "dessert_menu":
        dessert.update_menu_options(menus["dessert_menu"])
    elif menu_key == "dinner_menu":
        dinner.update_menu_options(menus["dinner_menu"])

    for entry in extra_entries:
        entry.delete(0, tk.END)  # clear everyhting in widget
        

def hide_extra_inputs():
    """Hide custom meal section"""
    hide_charts()
    if hasattr(custom_meal, "inputs_frame"):
    # if custom_meal has an open frame
        try:
            custom_meal.inputs_frame.destroy()
        except Exception:
            pass
        del custom_meal.inputs_frame

def toggle_extra_inputs(shown=False):
    """Toggle ability to open and close section"""
    if hasattr(custom_meal, "inputs_frame"):
        if custom_meal.inputs_frame.winfo_exists():
            hide_extra_inputs()
            return
    if not shown:
        custom_meal()


def on_closing():  # When user closes window (X)
    save_selections()  # Run function to save selec
    root.destroy()  # destroy frame

# Detect if user close wind, if yes, run onclosing func
root.protocol("WM_DELETE_WINDOW", on_closing) 


def show_delete_meal():
    """Delete custom meals"""
    if hasattr(show_delete_meal, "frame") and show_delete_meal.frame.winfo_exists():
        show_delete_meal.frame.destroy()    # Remove old delete frame
    show_delete_meal.frame = tk.Frame(right_frame, bg='#ffe0e0')
    if charts and hasattr(charts, 'get_tk_widget'):
        show_delete_meal.frame.pack(fill='x', pady=20, padx=20, before=charts.get_tk_widget())
    else:
        show_delete_meal.frame.pack(fill='x', pady=20, padx=20)

    menu_names = ["Breakfast", "Morning Tea", "Lunch", "Dessert", "Dinner"]
    menu_key_lookup = {
        "Breakfast": "breakfast_menu",
        "Morning Tea": "morning_tea_menu",
        "Lunch": "lunch_menu",
        "Dessert": "dessert_menu",
        "Dinner": "dinner_menu"
    }

    # Asks which menu custom meal is in
    delete_menu_var = tk.StringVar()
    delete_menu_var.set(menu_names[0])
    tk.Label(show_delete_meal.frame, text="Select Menu:", 
             bg="#ffe0e0").grid(row=0, column=0, padx=5, pady=2, sticky='e')
    menu_dropdown = tk.OptionMenu(show_delete_meal.frame, delete_menu_var, *menu_names)
    menu_dropdown.grid(row=0, column=1, padx=5, pady=2)

    # Asks which meal should be deleted
    delete_meal_var = tk.StringVar()
    # Only show custom meals in the dropdown
    def update_meal_options(*args):
        menu_key = menu_key_lookup[delete_menu_var.get()]
        custom_meals = [key for key in menus[menu_key] if "(CUSTOM)" in key]
        if custom_meals:
            delete_meal_var.set(custom_meals[0])
        else:
            delete_meal_var.set("")
        menu = menu_dropdown.nametowidget(menu_dropdown.menuname)
        menu.delete(0, "end")  # clear old options
        for name in menu_names:
            menu.add_command(label=name, command=lambda value=name: delete_menu_var.set(value))

        meal_menu = meal_dropdown.nametowidget(meal_dropdown.menuname)
        meal_menu.delete(0, "end")
        for meal in custom_meals:
            meal_menu.add_command(label=meal, command=lambda value=meal: delete_meal_var.set(value))

    tk.Label(show_delete_meal.frame, text="Select Custom Meal:", bg="#ffe0e0").grid(row=1, column=0, padx=5, pady=2, sticky='e')
    # Create initial list of custom meals for the default menu
    initial_custom_meals = [key for key in menus[menu_key_lookup[menu_names[0]]] if "(CUSTOM)" in key]
    meal_dropdown = tk.OptionMenu(show_delete_meal.frame, delete_meal_var, *(initial_custom_meals or [""]))
    meal_dropdown.grid(row=1, column=1, padx=5, pady=2)

    # When menu changes, update meal dropdown
    delete_menu_var.trace_add("write", lambda *args: update_meal_options())

    def perform_delete():
        """Delete custom meal"""
        menu_key = menu_key_lookup[delete_menu_var.get()]
        meal_key = delete_meal_var.get()
        if not meal_key or meal_key not in menus[menu_key]:
            results.config(text="No custom meal selected to delete.")
            return
        # Remove from menu dict and save
        del menus[menu_key][meal_key]
        with open('menus.json', 'w') as f:
            json.dump(menus, f, indent=4)
        results.config(text=f"Deleted custom meal '{meal_key}' from {delete_menu_var.get()}.")
        # Update GUI options
        if menu_key == "breakfast_menu":
            breakfast.update_menu_options(menus["breakfast_menu"])
        elif menu_key == "morning_tea_menu":
            morning_tea.update_menu_options(menus["morning_tea_menu"])
        elif menu_key == "lunch_menu":
            lunch.update_menu_options(menus["lunch_menu"])
        elif menu_key == "dessert_menu":
            dessert.update_menu_options(menus["dessert_menu"])
        elif menu_key == "dinner_menu":
            dinner.update_menu_options(menus["dinner_menu"])
        update_meal_options()  # refresh dropdown

    delete_btn = tk.Button(show_delete_meal.frame, text="Delete Selected Meal", command=perform_delete)
    delete_btn.grid(row=2, column=0, columnspan=2, pady=10)

def toggle_delete_meal(shown=False):
    """Toggle ability to open and close delete meal section."""
    if hasattr(show_delete_meal, "frame") and show_delete_meal.frame.winfo_exists():
        show_delete_meal.frame.destroy()
        del show_delete_meal.frame
        return
    if not shown:
        show_delete_meal()

tk.Button(bottom_left_frame, text="Create Custom Meal", command=toggle_extra_inputs).pack(fill='x')
tk.Button(bottom_left_frame, text="Delete Custom Meal", command=toggle_delete_meal).pack(fill='x')
tk.Button(left_frame, text="Calculate Nutrition", command=calculation_and_graph).pack()

root.mainloop()
