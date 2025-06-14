import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalcFunc:
    def __init__(self, charts, all_menus, selected_meals, results, frame, root):
        self.charts = charts
        self.all_menus = all_menus
        self.selected_meals = selected_meals
        self.results = results
        self.frame = frame
        self.root = root

    def calculation_and_graph(self):

        #ERROR PREVENTION
        if all(meal_selected.get() == "NO SELECTION/SKIP" for meal_selected in self.selected_meals):
            self.results.config(text="No meals selected. \nPlease select at least one meal to calculate nutrition.")
            if self.charts is not None: #if there's an open chart window
                self.charts.get_tk_widget().destroy() #destroy said window
                self.charts = None #set to None so that IF doesnt run again
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.pack_forget() #close chart frame
            self.root.update_idletasks() #stop all ongoing tasks
            self.root.geometry("")  #Resize to previous window size
            return self.charts
        
        #---CALCULATIONS START HERE---
        try: #safety net for ANY unexpected errors during calculation
            nutrients = ['calories', 'protein', 'fats', 'carbs']
            nutrient_totals = {}
            for nutrient in nutrients: #for each nutrient in the list
                nutrient_value = 0 #for each nutrient, reset value to zero
                for menu, selection_var in zip(self.all_menus, self.selected_meals): #for each selection
                    nutrient_value += menu[selection_var.get()][nutrient] #get selected meals nutrient info
                nutrient_totals[nutrient] = nutrient_value #updates value for each nutrient
            total_calories, total_protein, total_fats, total_carbs = (nutrient_totals[n] for n in nutrients)
            MAX_CALORIES = 2300 #constant variable
            calories_remaining = MAX_CALORIES - total_calories
            total_macros = total_fats + total_protein + total_carbs
            RDI_PERCENTS = {'carbs': 0.4, 'fats': 0.3, 'protein': 0.3} #constant variable
            rdi = {nutrient_type: total_macros * value for nutrient_type, value in RDI_PERCENTS.items()}

            #RESULTS
            self.results.config(text=(f"Total Nutritional Information:\n"
                                    f"Calories: {total_calories} kcal\n"
                                    f"Protein: {total_protein} g\n"
                                    f"Fats: {total_fats} g"))
            with open("nutrition_report.txt", "w") as f:
                f.write(f"MEALS SELECTED:\n\n"
                        f"\nBreakfast: {self.selected_meals[0].get()}\n\n"
                        f"\nMorning Tea: {self.selected_meals[1].get()}\n\n"
                        f"\nLunch: {self.selected_meals[2].get()}\n\n"
                        f"\nDinner: {self.selected_meals[3].get()}\n\n"
                        f"\nDessert: {self.selected_meals[4].get()}\n\n"
                        f"Total Nutritional Information:\n"
                        f" Calories: {total_calories} kcal\n"
                        f" Protein: {total_protein} g\n"
                        f" Fats: {total_fats} g\n"
                        f" Carbs: {total_carbs} g\n")
                os.startfile("nutrition_report.txt")

        except: #if an unexpected/unknown error occurs
            self.results.config(text="An error occurred during calculation.\nPlease try again.")
            return None #stops the function

        
        #---CHARTS AND GRAPHS START HERE---
        try: #safety net for graphing erorrs
            fig, axs = plt.subplots(1, 3, figsize=(10, 5), facecolor="#f0f0f0")
            fig.canvas.manager.set_window_title('Macronutrients Charts and Graphs')

            #FIRST CHART (CALORIES CONSUMED/REMAINING)
            if total_calories <= MAX_CALORIES: #if user doesnt exceed recomended calories
                pie_one_labels = [f'Consumed: {total_calories} kcal', f'Left: {calories_remaining} kcal']
                pie_one_sizes = [total_calories, calories_remaining]
                pie_one_colours = ['#ff9999', '#8fd9b6']
            else: #if user exceeds recomended calories
                exceeded = total_calories - MAX_CALORIES
                pie_one_labels = [f'Allowed: {MAX_CALORIES} kcal',f'Exceeded: {exceeded} kcal']
                pie_one_sizes = [MAX_CALORIES, exceeded]
                pie_one_colours = ['#ff9999', '#ff6666']
            explode = (0.1, 0) #aesthetics
            axs[0].pie(pie_one_sizes, labels=pie_one_labels, colors=pie_one_colours, explode=explode,
                        startangle=90, wedgeprops={'edgecolor': '#4b4b4b', 'linewidth': 1})
            axs[0].set_title("Calories Consumed vs Calories Left")
            axs[0].axis('equal') #makes pie chart a circle

            #SECOND CHART (TOTAL MACROS)
            pie_two_labels = [f'Protein: {total_protein}g ({total_protein/total_macros:.0%})',
                            f'Fats: {total_fats}g ({total_fats/total_macros:.0%})',
                            f'Carbs: {total_carbs}g ({total_carbs/total_macros:.0%})']
            pie_two_sizes = [total_protein, total_fats, total_carbs]
            explode = (0.05, 0.05, 0.05)
            pie_two_colours = ['#66b3ff', '#ffcc99', '#99ff99']
            axs[1].pie(pie_two_sizes, labels=pie_two_labels, colors=pie_two_colours, startangle=90, explode=explode, wedgeprops={'edgecolor':'#4b4b4b', 'linewidth': 1})
            axs[1].set_title("Total Macros")
            axs[1].axis('equal') #makes the whole thing a circle

            #THIRD CHART (CONSUMED/RDI COMPARIOSN)
            width = 0.1  # the width of the bars
            labels = ['Carbs', 'Fats', 'Protein']
            macronutrients = [total_carbs, total_fats, total_protein]
            rdiMacros = [rdi["carbs"], rdi["fats"], rdi["protein"]]
            x = np.arange(len(labels))  # the label locations
            axs[2].bar(x - width/2, macronutrients, width, label='Total Consumed')
            axs[2].bar(x + width/2, rdiMacros, width, label='Recommended Daily Intake')
            axs[2].set_ylabel('Macros')
            axs[2].set_title('Macro Comparison')
            axs[2].set_xticks(x)
            axs[2].set_xticklabels(labels)
            axs[2].legend(['Total Consumed', 'Recommended Daily Intake'])

            plt.tight_layout()
            if self.charts is not None: #If theres an chart thats running
                self.charts.get_tk_widget().destroy() #destroy that chart
                self.charts = None #once chart is destroyed, set value to None
            self.charts = fig
            self.frame.pack(side='left', fill='both', expand=True)
            self.charts = FigureCanvasTkAgg(fig, master=self.frame)
            self.charts.draw()

            #Resize and configure window
            canvas_widget = self.charts.get_tk_widget()
            canvas_widget.config(bg='#f0f0f0', highlightthickness=0)
            canvas_widget.pack(fill='both', expand=True)
            return self.charts
        
        except: #if an unknown error occurs during graphing
            self.results.config(text="An error has occurred during graphing.\nPlease try again.")
            return None #exit function