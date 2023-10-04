def eval_string(score_dict):
    
    string_to_return = "Model\t\t|\tMAPE\t|\tsMAPE\t|\tGrubbs\t|\tShape similarity\t|\n"
    string_to_return += "--------------------------------------------------------------------------------------------------\n"
    
    index = 0

    for key in score_dict:
        model = key
        string_to_return += f"{model}\t\t|\t{score_dict[key][0]}\t|\t{score_dict[key][1]}\t|\t{score_dict[key][2]}\t|\t{score_dict[key][3]}\t\t\t|\n"
        string_to_return += "--------------------------------------------------------------------------------------------------\n"
        index += 1

    return string_to_return