import tkinter as tk
import json
import os
from calculator import CalcFunc
from meal import MealFunc

with open('menus.json', 'r') as f:
    menus = json.load(f)

max_calories = 2300
charts = None
custom_meals = []
menu_dict = {"Breakfast": "breakfast_menu", 
            "Morning Tea": "morning_tea_menu", "Lunch": "lunch_menu",
            "Dessert": "dessert_menu", "Dinner": "dinner_menu"}
menu_names = ["Breakfast", "Morning Tea", "Lunch",
            "Dessert","Dinner"]

def save_selections():
    selections = [var.get() for var in selected_meals]
    with open('last_selections.json', 'w') as f:
        json.dump(selections, f)
        

def on_closing():  # When user closes window (X)
    save_selections()  # Run function to save selec
    root.destroy()  # destroy frame


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

# Frames
root = tk.Tk()
root.minsize(350, 300)

main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side='left', fill='y', expand=False)

right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.pack(side='left', fill='both', expand=True)

breakfast = MealFunc(left_frame, "Preference     -------     Breakfast:",
                     menus["breakfast_menu"], meat_types[0])
morning_tea = MealFunc(left_frame, "Preference     -------     Morning Tea:",
                       menus["morning_tea_menu"], meat_types[1])
lunch = MealFunc(left_frame, "Preference     -------     Lunch:",
                 menus["lunch_menu"], meat_types[2])
dessert = MealFunc(left_frame, "Preference     -------     Dessert:",
                   menus["dessert_menu"], meat_types[3])
dinner = MealFunc(left_frame, "Preference     -------     Dinner:",
                  menus["dinner_menu"], meat_types[4])

breakfast_preference, selected_breakfast = breakfast.selections()
morning_tea_preference, selected_morning_tea = morning_tea.selections()
lunch_preference, selected_lunch = lunch.selections()
dessert_preference, selected_dessert = dessert.selections()
dinner_preference, selected_dinner = dinner.selections()

selected_prefs = [breakfast_preference, morning_tea_preference, lunch_preference,
                  dessert_preference, dinner_preference]

selected_meals = [selected_breakfast, selected_morning_tea, selected_lunch,
                  selected_dessert, selected_dinner,]

menu_map = {
    "breakfast_menu": breakfast,
    "morning_tea_menu": morning_tea,
    "lunch_menu": lunch,
    "dessert_menu": dessert,
    "dinner_menu": dinner
}


# DATA PERSISTENCE
def on_selection_change(*args):
    """Save selections for data persist."""
    save_selections()


for var in selected_meals:
    var.trace_add('write', on_selection_change)
load_selections()

results = tk.Label(left_frame, text="")  # empty to edit later
results.pack()


def calculation_and_graph():
    """Run calculations for nutrients."""
    for widget in right_frame.winfo_children():
        widget.destroy()
    global charts
    calculator = CalcFunc(charts, ALL_MENUS, selected_meals,
                          results, right_frame, root, max_calories)
    charts = calculator.calculation_and_graph()
    save_selections()


def hide_charts():
    """Hide graphs when other sections are opened."""
    global charts
    if charts is not None:
        try:
            charts.get_tk_widget().destroy()
        except Exception:
            pass
        charts = None


def meal_create():
    """Make the frame for custom meal section."""
    hide_charts()
    meal_create.inputs_frame = tk.Frame(right_frame, bg='#e0e0e0')
    meal_create.inputs_frame.pack(fill='x', pady=20, padx=20)

    # Input boxes
    labels = ["Name", "Calories", "Protein", "Fats", "Carbs"]
    global custom_meals
    for i, macro_name in enumerate(labels):  # print key and value
        label = tk.Label(meal_create.inputs_frame, text=f"{macro_name}:", bg='#e0e0e0')
        label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(meal_create.inputs_frame)  # Input box
        entry.grid(row=i, column=1, padx=5, pady=2)
        custom_meals.append(entry)  # Add to list of custom meals

    global menu_names
    global menu_choice_var
    menu_choice_var = tk.StringVar()
    menu_choice_var.set(menu_names[0])  # dfault is bfast

    # Dropdown boxes and labels
    menu_label = tk.Label(meal_create.inputs_frame, text="Add to menu:", bg='#e0e0e0')
    menu_label.grid(row=len(labels), column=0, sticky='e', padx=5, pady=2)
    menu_dropdown = tk.OptionMenu(meal_create.inputs_frame, menu_choice_var, *menu_names)
    menu_dropdown.grid(row=len(labels), column=1, padx=5, pady=2)

    # Submit button
    submit = tk.Button(meal_create.inputs_frame,
                       text="Submit",command=process_inputs)
    submit.grid(row=len(labels) + 1, column=0,
                columnspan=2, pady=(10, 2))

    def close_inputs():
        toggle_meal_create(shown=True)

    # Close inputs button
    close = tk.Button(meal_create.inputs_frame,
                      text="Close Inputs", command=close_inputs)
    close.grid(row=len(labels) + 2, 
               column=0, columnspan=2, pady=(2, 10))


def process_inputs():
    """Process custom information."""
    name = custom_meals[0].get().strip()  # remove whitespace
    calories = custom_meals[1].get().strip()
    protein = custom_meals[2].get().strip()
    fats = custom_meals[3].get().strip()
    carbs = custom_meals[4].get().strip()
    if not name:  # if name is left blank
        results.config(text="Please enter a name for the meal.")
        return
    try:  #if values meet good data type
        meal_info = { "calories": int(calories), "fats": int(fats),
            "carbs": int(carbs), "protein": int(protein),
            "meat": "None"}
    except ValueError:  # if incorect data type
        results.config(text="ONLY NUMBERS for nutritional values.")
        return
    
    global menu_dict
    selected_menu_display = menu_choice_var.get()
    chosen_menu = menu_dict[selected_menu_display]  # dropdown box for meal type
    new_meal = f"{name.upper()} (CUSTOM)\n\n Calories: {meal_info['calories']} | Protein: {meal_info['protein']}g | Fats: {meal_info['fats']}g"
    menus[chosen_menu][new_meal] = meal_info
    with open('menus.json', 'w') as f:  # save new selections
        json.dump(menus, f, indent=4)
    results.config(text=f"Customised meal '{name}' added to {selected_menu_display} menu.")

    # Update the chosen menu
    global menu_map
    if chosen_menu in menu_map:
        menu_map[chosen_menu].update_menu_options(menus[chosen_menu])

    for entry in custom_meals:
        entry.delete(0, tk.END)  # clear everyhting
        

def toggle_meal_create(shown=False):
    if hasattr(meal_create, "inputs_frame") and meal_create.inputs_frame.winfo_exists():
        meal_create.inputs_frame.destroy()
        del meal_create.inputs_frame
        return
    if not shown:
        meal_create()


# Detect if user close window, if yes, run onclosing func
root.protocol("WM_DELETE_WINDOW", on_closing) 

bottom_left_frame = tk.Frame(left_frame)
bottom_left_frame.pack(fill='x')


def show_delete_meal():
    """Delete custom meals."""
    hide_charts()
    show_delete_meal.frame = tk.Frame(right_frame, bg='#ffe0e0')
    show_delete_meal.frame.pack(fill='x', pady=20, padx=20)

    global menu_names
    global menu_dict

    # Asks which menu custom meal is in
    delete_menu_var = tk.StringVar()
    delete_menu_var.set(menu_names[0])  # default is breakffast
    tk.Label(show_delete_meal.frame, text="Select Menu:", 
             bg="#ffe0e0").grid(row=0, column=0, padx=5, pady=2, sticky='e')
    menu_dropdown = tk.OptionMenu(show_delete_meal.frame, delete_menu_var, *menu_names)
    menu_dropdown.grid(row=0, column=1, padx=5, pady=2)

    # Asks which meal should be deleted
    delete_meal_var = tk.StringVar()


    def update_dropdown(*args):
        """Update selected dropdown box."""
        chosen_menu = menu_dict[delete_menu_var.get()]
        custom_meals = [key for key in menus[chosen_menu] if "(CUSTOM)" in key]
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

    all_meal_creations = [key for key in menus[menu_dict[menu_names[0]]] if "(CUSTOM)" in key]
    meal_dropdown = tk.OptionMenu(show_delete_meal.frame, delete_meal_var, *(all_meal_creations or [""]))
    meal_dropdown.grid(row=1, column=1, padx=5, pady=2)

    # When menu changes, update meal dropdown
    delete_menu_var.trace_add("write", lambda *args: update_dropdown())

    def delete():
        """Delete custom meal."""
        chosen_menu = menu_dict[delete_menu_var.get()]
        meal_key = delete_meal_var.get()
        if not meal_key or meal_key not in menus[chosen_menu]:
            results.config(text="No custom meal selected to delete.")
            return
        # Remove from menu dict and save
        del menus[chosen_menu][meal_key]
        with open('menus.json', 'w') as f:
            json.dump(menus, f, indent=4)
        results.config(text=f"Deleted custom meal '{meal_key}' from {delete_menu_var.get()}.")
        # Update GUI options
        global menu_map
        if chosen_menu in menu_map:
            menu_map[chosen_menu].update_menu_options(menus[chosen_menu])
        update_dropdown()  # refresh dropdown

    delete_btn = tk.Button(show_delete_meal.frame, text="Delete Selected Meal", command=delete)
    delete_btn.grid(row=2, column=0, columnspan=2, pady=10)

def toggle_delete_meal(shown=False):
    """Toggle ability to open and close delete meal section."""
    if hasattr(show_delete_meal, "frame") and show_delete_meal.frame.winfo_exists():
        show_delete_meal.frame.destroy()
        del show_delete_meal.frame
        return
    if not shown:
        show_delete_meal()

def show_calorie_input():
    show_calorie_input.frame = tk.Frame(right_frame, bg='#e0f7fa')
    show_calorie_input.frame.pack(fill='x', pady=20, padx=20)

    # Sex dropdown
    tk.Label(show_calorie_input.frame, text="Sex:", bg='#e0f7fa').grid(row=0, column=0, padx=5, pady=2, sticky='e')
    sex_var = tk.StringVar(value="Male")
    tk.OptionMenu(show_calorie_input.frame, sex_var, "Male", "Female").grid(row=0, column=1, padx=5, pady=2)

    # Height
    tk.Label(show_calorie_input.frame, text="Height (CENTIMETRES):", bg='#e0f7fa').grid(row=1, column=0, padx=5, pady=2, sticky='e')
    height_entry = tk.Entry(show_calorie_input.frame)
    height_entry.grid(row=1, column=1, padx=5, pady=2)

    # Weight
    tk.Label(show_calorie_input.frame, text="Weight (KILOGRAMS):", bg='#e0f7fa').grid(row=2, column=0, padx=5, pady=2, sticky='e')
    weight_entry = tk.Entry(show_calorie_input.frame)
    weight_entry.grid(row=2, column=1, padx=5, pady=2)

    hide_charts()

    # Calculate Button
    def set_max_calories():
        """Calculate max calories."""
        try:
            sex = sex_var.get()
            height = int(height_entry.get())
            weight = int(weight_entry.get())
            if sex == "Male":
                bmr = 10*weight + 6.25*height + 5  # traditionally/common calculation
            else:
                bmr = 10*weight + 6.25*height - 161
            new_max_calories = int(bmr * 1.2)
            global max_calories  # Change the constant to a variable
            max_calories = new_max_calories
            results.config(text=f"Max Calories set to {max_calories} kcal.")
            show_calorie_input.frame.destroy()
        except Exception as e:
            results.config(text="Please enter whole numbers.")

    tk.Button(show_calorie_input.frame, text="Set Max Calories", command=set_max_calories).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(show_calorie_input.frame, text="Cancel", command=show_calorie_input.frame.destroy).grid(row=5, column=0, columnspan=2, pady=2)


def toggle_max_cal(shown=False):
    """Toggle ability to open and close max calorie section."""
    if hasattr(show_calorie_input, "frame") and show_calorie_input.frame.winfo_exists():
        show_calorie_input.frame.destroy()
        del show_calorie_input.frame
        return
    if not shown:
        show_calorie_input()

tk.Button(bottom_left_frame, text="Create Custom Meal", command=toggle_meal_create).pack(fill='x')
tk.Button(bottom_left_frame, text="Delete Custom Meal", command=toggle_delete_meal).pack(fill='x')
tk.Button(bottom_left_frame, text="Set Max Calories", command=toggle_max_cal).pack(fill='x')
tk.Button(left_frame, text="Calculate Nutrition", command=calculation_and_graph).pack()


root.mainloop()
