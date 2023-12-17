import pandas as pd

# df = pd.read_csv("session_file.csv")
# df['model'] = df['model'].replace("predict_","", regex=True)

w1 = 0.0025
w2 = 0.0025
w3 = 0.0025
w4 = 0.0025
w5 = 0.99

# Accuracy metrics 
acc_metrics = 0.6

# Outliers 
outliers = 0.5

# Shape similarity 
shape_similarity = 0.2

# Time 
time_elapsed = 0.05

# Naive 
compared_to_naive_methods = 0.1

final_score = (w1*acc_metrics) + (w2*outliers) + (w3*shape_similarity) + (w4*time_elapsed) + (1-(w5*compared_to_naive_methods))

print(final_score)