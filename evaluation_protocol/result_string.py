def eval_string(score_dict, method):
    # if method == 'Naive Methods':
    #     string_to_return = "Model\t\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"
    # else:    
    #     string_to_return = "Model\t\t|\tTime Elapsed (sec)\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"

    string_to_return = "Model\t\t|\tTime Elapsed (sec)\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"
    line_string = "-" * len(string_to_return.expandtabs()) + '\n'
    string_to_return += line_string

    index = 0

    # Debugging 
    print(score_dict)

    for key in score_dict:
        model = key
        string_to_return += f"{model.replace('predict_','')}\t|\t{score_dict[key][0]}\t|\t{score_dict[key][1]}\t|\t{score_dict[key][2]}\t|\t{score_dict[key][3]}\t|\t{score_dict[key][4]}\t|\n"
        string_to_return += line_string
        index += 1

    return string_to_return