import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from menus import breakfast_menu, morning_tea_menu, lunch_menu, dessert_menu, dinner_menu
from calculator import CalcFunc
from meal import MealFunc

all_menus = [breakfast_menu, morning_tea_menu, lunch_menu, dessert_menu, dinner_menu]
charts = None

root = tk.Tk()

#Frames
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)
left_frame = tk.Frame(main_frame)
left_frame.pack(side='left', fill='y', expand=False)
right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.pack(side='left', fill='both', expand=True)

#Filter dropdown box
def meat_type_func(*menus):
    try: #safety net for errors
        meat_type = set() #empty set to append meat types later
        for each_menu in menus: #for each menu in all the menus
            for meal in each_menu.values(): #for each meal in the current menu
                meat_type.add(meal['meat']) #append meat type to meat set/list
        return ['None'] + sorted(meat_type - {'None'}) #"None" is always the starting option
    except: #if unexpected error occurs
        results.config(text='An error has occured during the meat filtering. \nPlease try again.')
        return None #exit func
        
#lists for menus and meat types
all_menus = [breakfast_menu, morning_tea_menu, lunch_menu, dessert_menu, dinner_menu] #meal menus
meat_types = [meat_type_func(each_menu) for each_menu in all_menus] #get all meat types from each menu

#call MealFunc class from external meal.py file 
breakfast = MealFunc(left_frame, "Preference     -------     Breakfast:", breakfast_menu, meat_types[0])
morningTea = MealFunc(left_frame, "Preference     -------     Morning Tea:", morning_tea_menu, meat_types[1])
lunch = MealFunc(left_frame, "Preference     -------     Lunch:", lunch_menu, meat_types[2])
dessert = MealFunc(left_frame, "Preference     -------     Dessert:", dessert_menu, meat_types[3])
dinner = MealFunc(left_frame, "Preference     -------     Dinner:", dinner_menu, meat_types[4])

#get the meat and meal selections by accessing MealFunc class and selections function
breakfast_meat, selected_breakfast = breakfast.selections() #Get meat and meat selection
morning_tea_meat, selected_morning_tea = morningTea.selections()
lunch_meat, selected_lunch = lunch.selections()
dessert_meat, selected_dessert = dessert.selections()
dinner_meat, selected_dinner = dinner.selections()

#lists for selected meats for coresponding selected meals
selected_meats = [breakfast_meat, morning_tea_meat, lunch_meat, dessert_meat, dinner_meat]
selected_meals = [selected_breakfast, selected_morning_tea, selected_lunch, selected_dessert, selected_dinner]

results = tk.Label(left_frame, text="") #Result text output
results.pack()

#function
def calculation_and_graph():
    global charts #access global charts variable
    calculator = CalcFunc(charts, all_menus, selected_meals, results, right_frame, root)
    charts = calculator.calculation_and_graph()

tk.Button(left_frame, text="Calculate Nutrition", command=calculation_and_graph).pack() #Calculate button

root.mainloop()