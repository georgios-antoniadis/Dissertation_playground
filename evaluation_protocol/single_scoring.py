import pandas as pd
# Config files
from configparser import ConfigParser
from tabulate import tabulate

# Normalization is based on the scores of the rest of the models 
def normalize(value, min_value, max_value):
    if value == 0:
        normalized_value = 0
    else:
        normalized_value = (value-min_value) / (max_value-min_value)
    return normalized_value

# Calculating accuracy 
def acc(row, df):
    min_rmse = df['rmse'].min()
    max_rmse = df['rmse'].max()

    min_mae = df['mae'].min()
    max_mae = df['mae'].max()

    min_mse = df['mse'].min()
    max_mse = df['mse'].max()
    
    accuracy_score = (normalize(row['rmse'], min_rmse, max_rmse) 
                    + row['nme'] 
                    + normalize(row['mae'], min_mae, max_mae) 
                    + normalize(row['mse'], min_mse, max_mse) 
                    + row['mape'] 
                    + row['smape']
                    ) / 6

    # Debugging
    print(f"""
{row['model']}
RMSE: {normalize(row['rmse'], min_rmse, max_rmse)} 
NME: {row['nme']}
MAE: {normalize(row['mae'], min_mae, max_mae)}
MSE: {normalize(row['mse'], min_mse, max_mse)} 
MAPE: {row['mape']} 
SMAPE: {row['smape']}
""")

    return accuracy_score


def single_score(row, df, w_accuracy, w_outliers, w_shape, w_time, w_complexity):
    accuracy_score = acc(row, df)
    min_grubbs = df['grubbs'].min()
    max_grubbs = df['grubbs'].max()

    min_shape_similarity = df['shape_similarity'].min()
    max_shape_similarity = df['shape_similarity'].max()
    
    min_time = df['time_elapsed_sec'].min()
    max_time = df['time_elapsed_sec'].max()

    outliers = normalize(row['grubbs'], min_grubbs, max_grubbs)
    time = normalize(row['time_elapsed_sec'], min_time, max_time)
    shape_similarity = normalize(row['shape_similarity'], min_shape_similarity, max_shape_similarity)
    complexity = row['complexity']

    # Debugging 
    print(f"""
model: {row['model']}
accuracy: {accuracy_score}
outliers: {outliers}
shape: {shape_similarity}
time: {time}
complexity: {complexity}
          """)


    total_single_score = round((w_accuracy*accuracy_score),2) \
    + round((w_outliers*outliers),2) \
    - round((w_shape*shape_similarity),2) \
    - round((w_time*time),2) \
    + round((w_complexity+complexity),2)

    return total_single_score


def find_best_naive_method(df, save_file, w_accuracy, w_outliers, w_shape, w_time, w_complexity):
    best_naive_method = ''
    # Assigning a random very large number
    best_score = 10e10

    for index, row in df.iterrows():
        if row['method_type'] == 'Naive Methods':
            
            single_scoring = single_score(row, df, w_accuracy, w_outliers, w_shape, w_time, w_complexity)

            print(f"Single score of {row['model']} is {single_scoring}")

            if single_scoring < best_score:
                best_score = single_scoring
                best_naive_method = row['model']
    
    return best_naive_method, best_score

def score():
    df = pd.read_csv("session_file.csv")
    # csv columns 
    # model,method_type,time_elapsed_sec,memory_usage_mb,rmse,nme,mae,mse,mape,smape,grubbs,shape_similarity
    df['model'] = df['model'].replace("predict_","", regex=True)
    
    save_file = open("Exports/single_scores.csv", "w")
    save_file.write("method,score\n")

    # Weights 
    #Read config file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Get the SINGLESCOREINFO section
    scoring_config = config_object["SINGLESCOREINFO"]
    
    w_accuracy = int(scoring_config['accuracy'])
    w_outliers = int(scoring_config['outliers']) 
    w_shape = int(scoring_config['shape'])  
    w_time = int(scoring_config['time'])
    w_complexity = int(scoring_config['complexity'])
    w_naive = int(scoring_config['naive']) 

    # Debugging
    # print(w_accuracy, w_outliers, w_shape, w_time, w_complexity)

    # Naive methods
    best_naive_method, best_naive_score = find_best_naive_method(df, save_file, w_accuracy, w_outliers, w_shape, w_time, w_complexity)
    # print(best_naive_score)

    print(f"Best naive method: {best_naive_method} with a score: {best_naive_score}")

    for index, row in df.iterrows():
        single_scoring = single_score(row, df, w_accuracy, w_outliers, w_shape, w_time, w_complexity)
        
        # Debugging
        print(f"Single score of {row['model']}: {single_scoring}")
        single_scoring += w_naive * (single_scoring/best_naive_score)
        print(f"Score {row['model']} after naive is accounted for: {single_scoring}")
        print("======================================")
        print("")

        save_file.write(f"{row['model']},{round(single_scoring,2)}\n")


    save_file.close()

    try:
        single_scores_df = pd.read_csv("Exports/single_scores.csv") 
        single_scores_df = single_scores_df.sort_values(by='score')
        single_scores_df.to_csv("Exports/single_scores.csv", index=False)

        df = pd.read_csv("Exports/single_scores.csv")
        string_to_return = tabulate(df, headers='keys', tablefmt="grid")
        single_scores_txt = open("Exports/single_scores.txt","w")
        single_scores_txt.write(string_to_return)
        single_scores_txt.close()

        return f"Message: File saved successfully"
    except: 
        return f"Error: File not saved successfully"