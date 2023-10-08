def eval_string(score_dict, method):
    if method == 'Naive Methods':
        string_to_return = "Model\t\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"
    else:    
        string_to_return = "Model\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"

    line_string = "-" * len(string_to_return.expandtabs()) + '\n'
    string_to_return += line_string

    index = 0

    for key in score_dict:
        model = key
        string_to_return += f"{model}\t|\t{score_dict[key][0]}\t|\t{score_dict[key][1]}\t|\t{score_dict[key][2]}\t|\t{score_dict[key][3]}\t\t\t|\n"
        string_to_return += line_string
        index += 1

    return string_to_return