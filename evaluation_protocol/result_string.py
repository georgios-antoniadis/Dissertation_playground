from tabulate import tabulate

def eval_string(scores_dict):
    headers = ["Model", "Time Elapsed (sec)", "Memory usage (MB)", "MAPE", "sMAPE", "Grubbs", "Shape similarity"]

    # Create a list of lists for each row in the table
    table_data = [[key.replace("predict_","")] + value for key, value in scores_dict.items()]

    # Print the table using tabulate
    string_to_return = tabulate(table_data, headers=headers, tablefmt="grid")

    return string_to_return