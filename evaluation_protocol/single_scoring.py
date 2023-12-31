import pandas as pd
# Config files
from configparser import ConfigParser


def normalize(value, min_value, max_value):
    if value == 0:
        normalized_value = 0
    else:
        normalized_value = (value-min_value) / (max_value-min_value)
    return normalized_value

def acc(row, df):
    min_rmse = df['rmse'].max()
    max_rmse = df['rmse'].min()

    min_mae = df['mae'].max()
    max_mae = df['mae'].min()

    min_mse = df['mse'].max()
    max_mse = df['mse'].min()
    
    accuracy_score = (normalize(row['rmse'], min_rmse, max_rmse) 
                    + row['nme'] 
                    + normalize(row['mae'], min_mae, max_mae) 
                    + normalize(row['mse'], min_mse, max_mse) 
                    + row['mape'] 
                    + row['smape']
                    ) / 6

    return accuracy_score


def single_score(row, df, w_accuracy, w_outliers, w_shape, w_time):
    accuracy_score = acc(row, df)
    min_grubbs = df['grubbs'].max()
    max_grubbs = df['grubbs'].min()

    min_shape_similarity = df['shape_similarity'].max()
    max_shape_similarity = df['shape_similarity'].min()

    min_time = df['time_elapsed_sec'].max()
    max_time = df['time_elapsed_sec'].min()
    
    outliers = normalize(row['grubbs'], min_grubbs, max_grubbs)
    time = normalize(row['time_elapsed_sec'], min_time, max_time)
    shape_similarity = normalize(row['shape_similarity'], min_shape_similarity, max_shape_similarity)

    score = (w_accuracy*accuracy_score) + (w_outliers*outliers) + (w_shape*shape_similarity) + (w_time*time)

    return score


def find_best_naive_method(df, save_file, w_accuracy, w_outliers, w_shape, w_time):
    best_naive_method = ''
    best_score = 1000

    for index, row in df.iterrows():
        if row['method_type'] == 'Naive Methods':
            
            score = single_score(row, df, w_accuracy, w_outliers, w_shape, w_time)
            save_file.write(f"{row['model']},{score}\n")
            
            if score < best_score:
                best_score = score
                best_naive_method = row['model']
    
    return best_naive_method, best_score

def score():
    df = pd.read_csv("../session_file.csv")
    # csv columns 
    # model,method_type,time_elapsed_sec,memory_usage_mb,rmse,nme,mae,mse,mape,smape,grubbs,shape_similarity
    df['model'] = df['model'].replace("predict_","", regex=True)
    
    save_file = open("single_scores.csv", "w")
    save_file.write("method,score\n")

    # Weights 
    #Read config file
    config_object = ConfigParser()
    config_object.read("../evaluation_protocol/config.ini")

    #Get the SINGLESCOREINFO section
    scoring_config = config_object["SINGLESCOREINFO"]
    
    w_accuracy = int(scoring_config['accuracy'])
    w_outliers = int(scoring_config['outliers']) 
    w_shape = int(scoring_config['shape'])  
    w_time = int(scoring_config['time'])
    w_naive = int(scoring_config['naive']) 

    # Accuracy metrics 
    acc_metrics = 0.6
    # Naive methods
    best_naive_method, best_naive_score = find_best_naive_method(df, save_file, w_accuracy, w_outliers, w_shape, w_time)
    # print(best_naive_score)

    for index, row in df.iterrows():
        if row['method_type'] not in ['Naive Methods']:
            score = single_score(row, df, w_accuracy, w_outliers, w_shape, w_time)
            print(f"{row['model']}:{score}")
            score += w_naive * (score - best_naive_score)
            print(f"{row['model']}:{score}")
            save_file.write(f"{row['model']},{score*10}\n")


    save_file.close()
    try:
        single_scores_df = pd.read_csv("single_scores.csv") 
        single_scores_df = single_scores_df.sort_values(by='score')
        single_scores_df.to_csv("single_scores.csv", index=False)
        return f"Message: File saved successfully"
    except: 
        return f"Error: File not saved successfully"