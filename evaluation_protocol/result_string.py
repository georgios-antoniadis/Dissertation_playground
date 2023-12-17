from tabulate import tabulate
import pandas as pd

def eval_string():

    df = pd.read_csv("session_file.csv")
    df['model'] = df['model'].replace("predict_","", regex=True)
    string_to_return = tabulate(df, headers='keys', tablefmt="grid")

    return string_to_return