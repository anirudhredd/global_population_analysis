import pandas as pd
from ydata_profiling import ProfileReport #comment this out if you can't get the data profiling package installed
import os
import shutil
from tkinter import Tk, filedialog
import numpy as np

# Create a GUI window to select the .csv file
root = Tk()
root.withdraw()  # Hide the root window

# Ask the user to select the .csv file
csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

df = pd.read_csv(csv_file_path)

for column in df: #grouped columns by existing data type (object vs float64 and presence of 0s or negative values)
    if column in ('Total Population','Urban Population','Rural Population', 'Infant Mortality Rate'):
        df[column].replace('-', pd.NA, inplace=True)  # Replace '-' with NA to exclude these from summary statistics
        df[column] = df[column].str.replace(',', '')  # Remove commas
        df[column] = df[column].astype('Float64')  # Convert to float64 which can handle nulls
        print(df[column].describe())
    if column in ('Population Density', 'Life Expectancy', 'Fertility Rate'): #handle these separately since we need to remove 0 values
        df.loc[df[column] == '0', column] = pd.NA # Replace 0 with NA to exclude these from summary statistics
        df[column].replace('-', pd.NA, inplace=True)  # Replace '-' with NA to exclude these from summary statistics
        df[column] = df[column].str.replace(',', '') # Remove commas
        df[column] = df[column].astype('Float64') # Convert to float64 which can handle nulls
    if column in ('Birth Rate','Death Rate'):
        df.loc[df[column] == '0', column] = pd.NA # Replace 0 with NA to exclude these from summary statistics
        df[column].replace('-', pd.NA, inplace=True)  # Replace '-' with NA to exclude these from summary statistics
    if column in ('Growth Rate'):
        df.loc[df[column] == '-', column] = pd.NA # Replace - with NA to exclude these from summary statistics. Keeps negatives
        df[column] = df[column].astype('Float64')

#comment out lines below if you can't get the data profiler to work. and want to proceed with the cleaned data frame generated above
profile = ProfileReport(df)

output_file_name = os.path.splitext(os.path.basename(csv_file_path))[0] + "_profile.html" # Save the HTML report to same location as csv
profile.to_file(output_file_name)

download_folder = os.path.dirname(csv_file_path) # Define the destination folder for downloaded reports

source_file_path = output_file_name  # Define the source file path

download_file_path = os.path.join(download_folder, output_file_name) # Define the destination file path

shutil.copy(source_file_path, download_file_path) # Copy the file to the download folder
