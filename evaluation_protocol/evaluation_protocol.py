import importlib
# from performance_metrics import rmse, nme, mae, mse, mape, smape
# from shape_similarity import dtw
# from grubbs import grubbs_score
from result_string import eval_string

# Take real and predicted as input 
def run_performance_metrics(real, predicted, method_type, method):
    performance_results = []
    module = importlib.import_module("performance_metrics")
    for name, function in module.__dict__.items():
        if callable(function):
            performance_results.append(function(real, predicted))

    module = importlib.import_module("grubbs")
    if method_type == 'Naive Methods' and method != 'random_walk':
            performance_results.append(0)
    else:
        for name, function in module.__dict__.items():
            if callable(function) and name.endswith("scores"):
                performance_results.append(function(real, predicted))

    module = importlib.import_module("shape_similarity")
    for name, function in module.__dict__.items():
        if callable(function):
            performance_results.append(function(real, predicted))

    return performance_results


# Return performance dictionary 
def eval_protocol(predicted_dictionary, real, method_type, scores_dict):
    for key in predicted_dictionary:
        perf_metrics = run_performance_metrics(real,
                                predicted_dictionary[key],
                                method_type,
                                key)
        for metric in perf_metrics:
            scores_dict[key].append(metric)

    # string_to_return = f"{method_type}\n"
    # string_to_return += "- " * len(method_type) + "\n"
    # string_to_return += eval_string(scores_dict)

    return scores_dict