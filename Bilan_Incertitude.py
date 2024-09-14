#!/usr/bin/python3
# author: Tristan Gayrard

"""
Métrologie - Bilan d'Incertitudes
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

# Create the root Tkinter window
root = tk.Tk()
root.title("Application de Budget d'Incertitude")

# Define columns for the DataFrame
colonnes = ["Type d'incertitude", "Loi", "Borne", 'Incertitude type', 'Coefficient de sensibilité', "(cu)²", "%"]

# Create the DataFrame and populate it with empty rows
df = pd.DataFrame(columns=colonnes)
for i in range(1):  # Adds 1 empty row initially
    df.loc[i] = ["", "", "", "", "", "", ""]

# Create a frame to hold the table-like structure
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

# Add column headers
for col_idx, col in enumerate(colonnes):
    header = ttk.Label(frame, text=col, width=15, anchor='center', font=('Arial', 10, 'bold'))
    header.grid(row=0, column=col_idx, padx=5, pady=5)

# Dropdown options for 'Type d'incertitude'
options = ['répétabilité', 'reproductibilité', 'constructeur', 'température thermostaté']
loi = ["Uniforme", "Uniforme", "Uniforme", "Triangle"]
valeur_loi = [np.sqrt(3), np.sqrt(3), np.sqrt(3), np.sqrt(2)]

# Variables to store the option menu variables
option_vars = []
borne_vars = []  # To store Borne entry variables
loi_entries = []  # To store "Loi" entry widgets

# Function to update the "Loi" and calculate "Incertitude type"
def update(var, row_idx):
    selected_option = var.get()
    if selected_option in options:
        loi_index = options.index(selected_option)
        loi_value = loi[loi_index]
        valeur_loi_value = valeur_loi[loi_index]
        
        # Update the "Loi" cell in the corresponding row
        loi_entry = loi_entries[row_idx]  # Access the stored "Loi" entry widget
        loi_entry.delete(0, tk.END)
        loi_entry.insert(0, loi_value)
        
        # Get the value of "Borne"
        borne_value = borne_vars[row_idx].get()
        try:
            borne_value = float(borne_value)  # Convert to float
            incertitude_type = borne_value / valeur_loi_value
        except ValueError:
            incertitude_type = ""  # If Borne is not a number, leave it blank
        
        # Update the "Incertitude type" cell
        incertitude_entry = frame.grid_slaves(row=row_idx + 1, column=3)[0]  # Get the 'Incertitude type' entry widget
        incertitude_entry.delete(0, tk.END)
        incertitude_entry.insert(0, str(incertitude_type))

# Function to add a new row
def add_row():
    row_idx = len(option_vars)  # Index for the new row
    
    # Create OptionMenu for 'Type d'incertitude'
    var = tk.StringVar(root)
    var.set("Sélectionner l'incertitude")
    
    # Set the callback to update the "Loi" column when the option is selected
    var.trace_add("write", lambda *args, var=var, row_idx=row_idx: update(var, row_idx))
    
    option_menu = ttk.OptionMenu(frame, var, "Sélectionner l'incertitude", *options)
    option_menu.grid(row=row_idx + 1, column=0, padx=5, pady=5)
    
    option_vars.append(var)  # Store the variable

    # Add entry for "Loi"
    loi_entry = ttk.Entry(frame, width=15)
    loi_entry.grid(row=row_idx + 1, column=1, padx=5, pady=5)
    loi_entries.append(loi_entry)  # Store the Loi entry widget

    # Add entry for "Borne" with a StringVar to keep track of the value
    borne_var = tk.StringVar()
    borne_var.trace_add("write", lambda *args, row_idx=row_idx: update(option_vars[row_idx], row_idx))  # Update "Incertitude type" when Borne changes
    borne_entry = ttk.Entry(frame, textvariable=borne_var, width=15)
    borne_entry.grid(row=row_idx + 1, column=2, padx=5, pady=5)
    
    borne_vars.append(borne_var)  # Store the Borne variable

    # Add empty cells for the other columns (except "Loi" and "Borne", which are handled above)
    for col_idx in range(3, len(colonnes)):  # Start from column 3 ("Incertitude type")
        entry = ttk.Entry(frame, width=15)
        entry.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

# Add the initial row
add_row()

# Create a "+" button to add a new row
add_button = ttk.Button(root, text="+", command=add_row)
add_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Run the Tkinter main loop
root.mainloop()
