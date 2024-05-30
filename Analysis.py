import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# Load CSV files into pandas DataFrames and using dictionary data structure
data_files = {
    2021: '/Users/zaid/Desktop/Daily_Rainfall_2021.csv',
    2022: '/Users/zaid/Desktop/Daily_Rainfall_2022.csv',
    2023: '/Users/zaid/Desktop/Daily_Rainfall_2023.csv'
}
dataframes = {year: pd.read_csv(path) for year, path in data_files.items()}

def plot_rainfall_analysis(df, year):
    """ Function to plot monthly total and average rainfall data. """
    # Creating visualizations

    # Create a figure with three subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))


    """using dictionaries makes the code more manageable and the overall structure cleaner and more scalable"""
    
    monthly_data = {'Total': df.groupby('Month')['Rainfall amount (millimetres)'].sum(),
                    'Average': df.groupby('Month')['Rainfall amount (millimetres)'].mean()}
    
    # Total Rainfall Plot
    axes[0].bar(monthly_data['Total'].index, monthly_data['Total'].values, color='b')
    axes[0].set_title(f'Monthly Total Rainfall in {year}')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Total Rainfall (mm)')

    # Average Rainfall Plot
    axes[1].plot(monthly_data['Average'].index, monthly_data['Average'].values, marker='o', linestyle='-', color='r')
    axes[1].set_title(f'Monthly Average Rainfall in {year}')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Average Rainfall (mm)')

    # Histogram of Daily Rainfall Amounts
    axes[2].hist(df['Rainfall amount (millimetres)'].dropna(), bins=20, color='g', alpha=0.7)
    axes[2].set_title('Distribution of Daily Rainfall Amounts')
    axes[2].set_xlabel('Rainfall (mm)')
    axes[2].set_ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def display_statistics(df, year):
    """ Function to display basic statistics for rainfall data. """
    # Calculating and displaying statistics
    stats = {
        'Total Rainfall': df['Rainfall amount (millimetres)'].sum(),
        'Mean Rainfall': df['Rainfall amount (millimetres)'].mean(),
        'Median Rainfall': df['Rainfall amount (millimetres)'].median(),
        'Mode Rainfall': df['Rainfall amount (millimetres)'].mode().iloc[0],
        'Standard Deviation': df['Rainfall amount (millimetres)'].std(),
        'Variance': df['Rainfall amount (millimetres)'].var(),
        'Max Rainfall Day': df[df['Rainfall amount (millimetres)'] == df['Rainfall amount (millimetres)'].max()]
    }

    print(f"Statistics for {year}:")
    for key, value in stats.items():
        if key != 'Max Rainfall Day':
            print(f"{key}: {value:.2f}")
        else:
            print("Day with Maximum Rainfall:")
            display(value[['Year', 'Month', 'Day', 'Rainfall amount (millimetres)']])
    print("\n")

def display_high_rainfall_days(df, year):
    """ Displays days with rainfall above 20mm for a given year. """
    high_rainfall_days = df[df['Rainfall amount (millimetres)'] > 20]
    
    print(f"Days with rainfall above 20mm in {year}:")
    if high_rainfall_days.empty:
        print("No days with rainfall above 20mm.")
    else:
        display(high_rainfall_days[['Year', 'Month', 'Day', 'Rainfall amount (millimetres)']])
    print("\n")

# Output widget and function handling with dictionary mapping
output = widgets.Output()
functions_map = {
    'Visualize Rainfall Data': plot_rainfall_analysis,
    'Show Basic Statistics': display_statistics,
    'Show Days with Rainfall > 20mm': display_high_rainfall_days
}

# Function to handle user selection
def handle_selection(change):
    with output:
        clear_output(wait=True)
        if change['new'] in functions_map:
            for year, df in dataframes.items():
                functions_map[change['new']](df, year)
        elif change['new'] == 'Exit':
            print("Exiting the program.")

# # Making basic UI 
menu = widgets.Dropdown(
    options=['Select Option'] + list(functions_map.keys()) + ['Exit'],
    value='Select Option',
    description='Menu:',
    disabled=False,
)

# To display the menu
display(menu, output)

# Connecting menu to the handle section function
menu.observe(handle_selection, names='value')
