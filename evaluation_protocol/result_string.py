from tabulate import tabulate
import pandas as pd

def eval_string():
    # headers = ["Model", "Time Elapsed (sec)", "Memory usage (MB)", "MAPE", "sMAPE", "Grubbs", "Shape similarity"]

    df = pd.read_csv("session_file.csv")
    df['model'] = df['model'].replace("predict_","", regex=True)
    # Create a list of lists for each row in the table
    string_to_return = tabulate(df, headers='keys', tablefmt="grid")

    # Print the table using tabulate
    # string_to_return = tabulate(table_data, headers=headers, tablefmt="grid")

    return string_to_return