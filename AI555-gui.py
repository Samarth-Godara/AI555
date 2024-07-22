import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
import pandas as pd
import numpy as np
from scipy.optimize import minimize

t1_d=0.0
t2_d=0.0
approx_decimal_r = 1000
approx_decimal_c = 7
n_sols = 10
disp_sols = 3

def calculate_t1_t2(r1, r2, c1):
  t1 = 0.693 * (r1 + r2) * c1
  t2 = 0.693 * r2 * c1
  return t1, t2

def calc_err(params):
  r1, r2, c1 = params
  t1_a, t2_a = calculate_t1_t2(r1, r2, c1)
  error = abs(t1_d - t1_a) + abs(t2_d - t2_a)
  return error

def calc_error(comb):
    t1_a, t2_a = calculate_t1_t2(comb[0], comb[1], comb[2])
    error = abs(t1_d - t1_a) + abs(t2_d - t2_a)
    return error, t1_a, t2_a

def ai_555_calc(t1_d, t2_d, n_sols):

    df_r1 = []
    df_r2 = []
    df_c1 = []
    df_t1 = []
    df_t2 = []
    df_error = []
    df_phase = []
    df_sol = []

    #t1_d = 5 #seconds
    #t2_d = 1 #seconds
    #n_sols = 5

    output_list=[]

    r1_coeff_list = [i for i in range(1,11)]
    r2_coeff_list = [i for i in range(1,11)]
    c1_coeff_list = [i for i in range(1,11)]
    r1_power_list = [1,10,100,1000,10000,100000,1000000]
    r2_power_list = [1,10,100,1000,10000,100000,1000000]
    c1_power_list = [1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9]

    combinations_list = []
    for r1_coeff in r1_coeff_list:
        for r2_coeff in r2_coeff_list:
            for c1_coeff in c1_coeff_list:
                for r1_power in r1_power_list:
                    for r2_power in r2_power_list:
                        for c1_power in c1_power_list:
                            combinations_list.append([r1_coeff * r1_power, r2_coeff * r2_power, c1_coeff * c1_power])

    #print("Total combinations to be checked = ",len(combinations_list))

    r1_res_list=[]
    r2_res_list=[]
    c1_res_list=[]
    err_res_list=[]
    t1_res_list=[]
    t2_res_list=[]

    for combination in combinations_list:
        err, t1_a, t2_a = calc_error(combination)
        r1_res_list.append(combination[0])
        r2_res_list.append(combination[1])
        c1_res_list.append(combination[2])
        err_res_list.append(err)
        t1_res_list.append(t1_a)
        t2_res_list.append(t2_a)

    res_df = pd.DataFrame()
    res_df['r1'] = r1_res_list
    res_df['r2'] = r2_res_list
    res_df['c1'] = c1_res_list
    res_df['error'] = err_res_list
    res_df['t1'] = t1_res_list
    res_df['t2'] = t2_res_list

    #res_df.sort_values(by=['error'], ascending=True)
    best_sols = res_df.sort_values(by=['error'], ascending=True).values[0:n_sols]
    #print(best_sols)

    sol_count=0

    for params in best_sols:

        first_output=[]

        first_sol=[]

        # Initial guess for parameters
        params0 = np.array([params[0], params[1], params[2]])

        sol_count+=1
        #print("\n\n\nSolution #"+str(sol_count)+", Initial Parameters, r1, r2, c2 : ", params0)

        # Print optimal values
        #print("\nPhase I Optimal values (Grid-search):")
        #print("r1:", params[0], "Ohm")
        #print("r2:", params[1], "Ohm")
        #print("c1:", params[2], "Farad")
        t1,t2 = calculate_t1_t2(params[0], params[1], params[2])
        #print("t1:", t1, "Seconds")
        #print("t2:", t2, "Seconds")
        #print("error:", calc_err(params0), "Seconds")

        first_sol.append(params[0])
        first_sol.append(params[1])
        first_sol.append(params[2])
        first_sol.append(t1)
        first_sol.append(t2)
        first_sol.append(calc_err(params0))

        second_sol=[]

        # Bounds for parameters
        bounds = ((0.0, None), (0.0, None), (0.0, None))

        # Perform gradient descent
        result = minimize(calc_err, params0, method='Nelder-Mead', bounds=bounds)

        # Extract optimal values
        r1_opt, r2_opt, c1_opt = result.x

        # Print optimal values
        #print("\nPhase II Optimal values (Gradient-based search):")
        #print("r1:", r1_opt, "Ohm")
        #print("r2:", r2_opt, "Ohm")
        #print("c1:", c1_opt, "Farad")
        t1,t2 = calculate_t1_t2(r1_opt, r2_opt, c1_opt)
        #print("t1:", t1, "Seconds")
        #print("t2:", t2, "Seconds")
        #print("error:", calc_err(result.x), "Seconds")

        second_sol.append(r1_opt)
        second_sol.append(r2_opt)
        second_sol.append(c1_opt)
        second_sol.append(t1)
        second_sol.append(t2)
        second_sol.append(calc_err(result.x))

        third_sol=[]

        # Print optimal values
        #print("\nPhase III Optimal values (rounded-off values):")
        #print("r1:", (int(r1_opt/100))*100, "Ohm")
        #print("r2:", (int(r2_opt/100))*100, "Ohm")
        #print("c1:", round(c1_opt,7), "Farad")
        
        r1_aprx = (int(r1_opt/approx_decimal_r))*approx_decimal_r
        r2_aprx = (int(r2_opt/approx_decimal_r))*approx_decimal_r
        c1_aprx = round(c1_opt,approx_decimal_c)
        t1,t2 = calculate_t1_t2(r1_aprx, r2_aprx, c1_aprx)
        #print("t1:", t1, "Seconds")
        #print("t2:", t2, "Seconds")
        #print("error:", calc_err(np.array([ (int(r1_opt/100))*100, (int(r2_opt/100))*100, round(c1_opt,7)])), "Seconds")

        third_sol.append(r1_aprx)
        third_sol.append(r2_aprx)
        third_sol.append(c1_aprx)
        third_sol.append(t1)
        third_sol.append(t2)
        third_sol.append(calc_err(np.array([ r1_aprx, r2_aprx, c1_aprx])))

        first_output.append(first_sol)
        first_output.append(second_sol)
        first_output.append(third_sol)

        output_list.append(first_output)

        df_r1.append(first_sol[0])
        df_r2.append(first_sol[1])
        df_c1.append(first_sol[2])
        df_t1.append(first_sol[3])
        df_t2.append(first_sol[4])
        df_error.append(first_sol[5])
        df_phase.append(1)
        df_sol.append(sol_count)

        df_r1.append(second_sol[0])
        df_r2.append(second_sol[1])
        df_c1.append(second_sol[2])
        df_t1.append(second_sol[3])
        df_t2.append(second_sol[4])
        df_error.append(second_sol[5])
        df_phase.append(2)
        df_sol.append(sol_count)

        df_r1.append(third_sol[0])
        df_r2.append(third_sol[1])
        df_c1.append(third_sol[2])
        df_t1.append(third_sol[3])
        df_t2.append(third_sol[4])
        df_error.append(third_sol[5])
        df_phase.append(3)
        df_sol.append(sol_count)


    result_df = pd.DataFrame()
    result_df['R1'] = df_r1
    result_df['R2'] = df_r2
    result_df['C'] = df_c1
    result_df['T1'] = df_t1
    result_df['T2'] = df_t2
    result_df['error'] = df_error
    result_df['phase'] = df_phase
    result_df['sol'] = df_sol

    #return output_list
    return result_df

def get_results_string(t1_d, t2_d, res):
    #import pandas as pd  # Make sure pandas is imported for DataFrame operations

    # Initialize the string
    results_string = ""

    # Add required time durations
    results_string += f"Required time durations: T1 = {t1_d} sec, T2 = {t2_d} sec\n\n"

    # Add solutions with least error
    results_string += "A. Solutions with least error:\n"
    p_res = res[(res.C > 0.0) & (res.R1 > 0.0)  & (res.R2 > 0.0)]
    sorted_res = p_res.sort_values(by=['error'], ascending=True)
    least_error_solutions = sorted_res.head(disp_sols)[res.columns[:-3]].set_axis(range(1, disp_sols+1)).to_string(index=True)
    results_string += least_error_solutions + "\n\n"

    # Add approximated solutions with least error
    results_string += "B. Approximated Solutions with least error:\n"
    p_res = res[((res.phase == 3) | (res.phase == 1))  & (res.C > 0.0) & (res.R1 > 0.0)  & (res.R2 > 0.0)]
    least_error_approx_solutions = p_res.sort_values(by=['error'], ascending=True).head(disp_sols)[res.columns[:-3]].set_axis(range(1, disp_sols+1)).to_string(index=True)
    results_string += least_error_approx_solutions + "\n\n"

    # Add approximated solutions with least capacitance
    results_string += "C. Approximated Solutions with least capacitance:\n"
    p_res_cap = res[((res.phase == 3) | (res.phase == 1)) & (res.C > 0.0) & (res.R1 > 0.0)  & (res.R2 > 0.0)]
    least_capacitance_solutions = p_res_cap.sort_values(by=['C'], ascending=True).head(disp_sols)[res.columns[:-3]].set_axis(range(1, disp_sols+1)).to_string(index=True)
    results_string += least_capacitance_solutions + "\n\n"

    # Add units
    results_string += "Units: Resistance = Ohm, Capacitance = Farad, Time = Second"

    return results_string


class AI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-based 555 IC Components' Values Calculator - Astable Mode")
        
        #self.root.geometry("400x400")
        
        label_font = font.Font(size=15, weight='bold')
        label_font2 = font.Font(size=10, weight='bold')
        button_font = font.Font(size=10, weight='bold')
        
        self.label1 = tk.Label(root, text="AI-based 555 timer IC's\n components-value calculator" , font=label_font)
        self.label1.grid(column=0, row=0, columnspan=4, ipady = 10)

        self.label1 = tk.Label(root, text="Calculate multiple solution for IC's R1, R2 and C for astable mode.")
        self.label1.grid(column=0, row=1, columnspan=4, ipady = 10)
        
        # Label and entry for T1
        self.label1 = tk.Label(root, text="Input ON Time \n(T1) in seconds :", font=label_font2)
        self.label1.grid(column=0, row=2, ipady = 10, sticky='e')
        self.entry1 = tk.Entry(root, width=10)
        self.entry1.grid(column=1, row=2, sticky='w')
        #self.label12 = tk.Label(root, text="in seconds")
        #self.label12.grid(column=2, row=1)
        
        # Label and entry for T2
        self.label2 = tk.Label(root, text="Input OFF Time \n(T2) in seconds :", font=label_font2)
        self.label2.grid(column=2, row=2, ipady = 10, sticky='e')
        self.entry2 = tk.Entry(root, width=10)
        self.entry2.grid(column=3, row=2, sticky='w')
        #self.label22 = tk.Label(root, text="in seconds")
        #self.label22.grid(column=2, row=2)`

        # Label and entry for T1
        self.label1 = tk.Label(root, text="Rounding-off factor \nfor Ressistance (in Ohm) : ")
        self.label1.grid(column=0, row=3, ipady = 10, sticky='e')
        self.entry3 = tk.Entry(root, width=10)
        self.entry3.grid(column=1, row=3, sticky='w')
        self.entry3.insert(0,'1000')
        
        # Label and entry for T2
        self.label2 = tk.Label(root, text="Rounding-off factor \nfor Capacitance (1e-? F) : ")
        self.label2.grid(column=2, row=3, ipady = 10, sticky='e')
        self.entry4 = tk.Entry(root, width=10)
        self.entry4.grid(column=3, row=3, sticky='w')
        self.entry4.insert(0,'7')


        # Label and entry for T1
        self.label1 = tk.Label(root, text="Total solutions \nto be generated : ")
        self.label1.grid(column=0, row=4, ipady = 10, sticky='e')
        self.entry5 = tk.Entry(root, width=10)
        self.entry5.grid(column=1, row=4, sticky='w')
        self.entry5.insert(0,'10')
        
        # Label and entry for T2
        self.label2 = tk.Label(root, text="Total Options\nto be displayed : ")
        self.label2.grid(column=2, row=4, ipady = 10, sticky='e')
        self.entry6 = tk.Entry(root, width=10)
        self.entry6.grid(column=3, row=4, sticky='w')
        self.entry6.insert(0,'3')
        
        # Calculate button
        self.calculate_button = tk.Button(root, text="Calculate multiple solutions for R1, R2 and C", command=self.calculate, font=button_font, borderwidth=5)
        self.calculate_button.grid(column=0, row=5, columnspan=4, pady = 10)

        # Result panel
        self.result_panel = scrolledtext.ScrolledText(root, width=65, height=22)
        self.result_panel.insert(tk.END, "Steps for calculating the R1, R2 and C values:\n\n1. Input the On and OFF time (T1 and T2) in seconds\n\n2. Click on 'Calculate' button.")
        self.result_panel.config(state='disabled')
        self.result_panel.grid(column=0, row=6, columnspan=4,pady=10,padx=10)

        self.label2 = tk.Label(root, text="Developement Team:\n1. Dr. Samarth Godara, ICAR-IASRI, New Delhi, India (Email : samarth.godara@gmail.com)\n2. Er. Madhur Behl, I.I.T. Kharagpur, West Bengal, India (Email : madhurbehl22@gmail.com)", justify='left')
        self.label2.grid(column=0, row=7, ipady = 10, sticky='w', columnspan=4,padx=10)
        
        
    def enable_and_print(self, text):
        self.result_panel.config(state='normal')
        self.result_panel.delete('1.0', tk.END)
        self.result_panel.insert(tk.END, text)
        self.result_panel.config(state='disabled')
        
    def calculate(self):
        try:
            T1 = float(self.entry1.get())
            T2 = float(self.entry2.get())
            
            global t1_d #seconds
            global t2_d #seconds
            global approx_decimal_r
            global approx_decimal_c
            global n_sols
            global disp_sols
            
            t1_d = T1 
            t2_d = T2 

            approx_decimal_r = int(self.entry3.get())
            approx_decimal_c = int(self.entry4.get())

            n_sols = int(self.entry5.get())
            disp_sols = int(self.entry6.get())

            res = ai_555_calc(t1_d, t2_d, n_sols)

            txt = get_results_string(t1_d, t2_d, res)

            self.enable_and_print(txt)

            #print(res)

            #self.result_panel.insert(tk.END, f"T1: {T1}, T2: {T2}, Result: {result}\n")
        except ValueError:
            self.result_panel.insert(tk.END, "Invalid input! Please enter valid numbers.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AI_Calculator(root)
    root.mainloop()
