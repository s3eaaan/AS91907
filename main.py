import tkinter as tk
import json
from calculator import CalcFunc
from meal import MealFunc
with open('menus.json', 'r') as f:
    menus = json.load(f)

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

results = tk.Label(left_frame, text="")
results.pack()

bottom_left_frame = tk.Frame(left_frame)
bottom_left_frame.pack(side='bottom', fill='x')

extra_entries = []

def show_extra_inputs():
    # Create new input frame
    show_extra_inputs.inputs_frame = tk.Frame(right_frame, bg='#e0e0e0')
    show_extra_inputs.inputs_frame.pack(fill='x', pady=20, padx=20)

    # Input fields and labels
    labels = ["Name", "Calories", "Protein", "Fats", "Carbs"]
    global extra_entries
    extra_entries = []
    for i, label_text in enumerate(labels):
        label = tk.Label(show_extra_inputs.inputs_frame, text=f"{label_text}:", bg='#e0e0e0')
        label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(show_extra_inputs.inputs_frame)
        entry.grid(row=i, column=1, padx=5, pady=2)
        extra_entries.append(entry)

    menu_names = ["Breakfast", "Morning Tea", "Lunch",
                  "Dessert","Dinner"]

    global menu_choice_var
    menu_choice_var = tk.StringVar()
    menu_choice_var.set(menu_names[0])  # defolt choice is bfast

    menu_label = tk.Label(show_extra_inputs.inputs_frame, text="Add to menu:", bg='#e0e0e0')
    menu_label.grid(row=len(labels), column=0, sticky='e', padx=5, pady=2)
    menu_dropdown = tk.OptionMenu(show_extra_inputs.inputs_frame, menu_choice_var, *menu_names)
    menu_dropdown.grid(row=len(labels), column=1, padx=5, pady=2)

    # Submit button to process inputs
    submit = tk.Button(show_extra_inputs.inputs_frame,
                       text="Submit",command=process_inputs)

    submit.grid(row=len(labels) + 1, 
                column=0, columnspan=2, pady=(10, 2))

    def close_inputs():
        toggle_extra_inputs(shown=True)

    close = tk.Button(show_extra_inputs.inputs_frame,
        text="Close Inputs", command=close_inputs)

    close.grid(row=len(labels) + 2, 
                   column=0, columnspan=2, pady=(2, 10))

def process_inputs():
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
    menu_key = menu_key_lookup[selected_menu_display]
    with open('menus.json', 'w') as f: #SAVE NEW SELECTIONS
        json.dump(menus, f, indent=4)
    display_string = f"{name.upper()} (CUSTOM)\n\n Calories: {meal_info['calories']} | Protein: {meal_info['protein']}g | Fats: {meal_info['fats']}g"
    menus[menu_key][display_string] = meal_info
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
    if hasattr(show_extra_inputs, "inputs_frame"):
    # if show_extra_inputs has an open frame
        try:
            show_extra_inputs.inputs_frame.destroy()
        except Exception:
            pass
        del show_extra_inputs.inputs_frame

def toggle_extra_inputs(shown=False):
    if hasattr(show_extra_inputs, "inputs_frame"):
        if show_extra_inputs.inputs_frame.winfo_exists():
            hide_extra_inputs()
            return
    if not shown:
        show_extra_inputs()

tk.Button(bottom_left_frame, text="Show Extra Inputs", command=toggle_extra_inputs).pack(fill='x', pady=5)

def calculation_and_graph():
    global charts
    calculator = CalcFunc(charts, ALL_MENUS, selected_meals, 
                          results, right_frame, root)
    charts = calculator.calculation_and_graph()

tk.Button(left_frame, text="Calculate Nutrition", command=calculation_and_graph).pack()

root.mainloop()
