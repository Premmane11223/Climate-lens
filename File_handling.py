
import pandas as pd

def load_cleaned_data(file_name):
    return pd.read_csv(file_name)

def save_cleaned_data(file_name, df):
    df.to_csv(file_name, index=False)  #our data is already cleaned dso we dont need this part


    