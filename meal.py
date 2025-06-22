"""Run Meal Filter and Meal Selection."""
import tkinter as tk


class MealFunc:
    """Filter selection of meals."""

    def __init__(self, main_frame, meal_name, menu_values, meat_types):
        """Initialise (self initialise) attributes given."""
        self.meal_frame = tk.Frame(main_frame)
        self.meal_frame.pack(fill='x', pady=4)

        self.label = tk.Label(self.meal_frame, text=meal_name)  # Meal titles
        self.label.pack(anchor='w')

        self.meat = tk.StringVar(value='None')  # None is the first option
        # dropdown box for filters
        self.filter_dropdown = tk.OptionMenu(self.meal_frame,
                                             self.meat, *meat_types)
        self.filter_dropdown.pack(side='left', padx=(0, 10))

        self.meal = tk.StringVar()  # meal dropdown boxes
        self.meal_selection = tk.OptionMenu(self.meal_frame,
                                            self.meal, *menu_values.keys())
        self.meal_selection.pack(side='left', padx=(0, 10))

        def filter(*args):
            preferred_meat = self.meat.get()
            filtered = []  # list of meals based on filter
            for selected_meal, meal_details in menu_values.items():
                # if the meal's meat matches the user's preferred meat
                if (
                    preferred_meat == 'None'
                    or preferred_meat == meal_details['meat']
                    or selected_meal == 'NO SELECTION/SKIP'
                ):
                    filtered.append(selected_meal)  # add meal to filtered list
            self.meal_selection['menu'].delete(0, 'end')  # reset dropdown box
            for options in filtered:  # for each item in the filtered meals
                # add filtered meal to dropdown
                self.meal_selection['menu'].add_command(
                    label=options, command=lambda
                    opt=options: self.meal.set(opt))
            if filtered:  # if list is not empty
                self.meal.set(filtered[0])  # show first item in list

        self.meat.trace_add('write', filter)  # listens for user to use filter
        filter()  # runs filter func if user uses filter

    def selections(self):
        """Return values."""
        return self.meat, self.meal
