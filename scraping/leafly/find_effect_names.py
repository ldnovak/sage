import json
import numpy as np

effects = {}
negatives = {}
medicals = {}


def find_names(file_name, dic_put_names):
    with open(file_name, 'r') as json_strains:
        effects = json.load(json_strains)
        for strain in effects:
            for feeling in effects[strain]:
                name_of_feeling, value_of_feeling = feeling
                if name_of_feeling not in dic_put_names:
                    dic_put_names[name_of_feeling] = [value_of_feeling]
                else:
                    dic_put_names[name_of_feeling].append(value_of_feeling)

    for name in dic_put_names:
        dic_put_names[name] = np.array(dic_put_names[name])


def make_name_file(name_of_file, effect_dict, neg_dict, medical_dict):
    f = open(name_of_file, 'w')
    f.write('effect names: ' + str(list(effect_dict.keys())) + '\n')
    f.write('negative names: ' + str(list(neg_dict.keys())) + '\n')
    f.write('medical names: ' + str(list(medical_dict.keys())) + '\n')
    f.close()


def make_simple_info_file(name_of_file, dict):
    f = open(name_of_file, 'w')
    f.write('number, total, ave, median, min, max\n')
    for feeling in dict:
        feeling_array = dict[feeling]
        number_strains_with_feeling = len(feeling_array)
        total_feeling_count = np.sum(feeling_array)
        ave_feeling_count = np.mean(feeling_array)
        median_feeling_count = np.median(feeling_array)
        min_feeling = np.min(feeling_array)
        max_feeling = np.max(feeling_array)
        f.write("{} : [{}, {}, {}, {}, {}, {}]\n".format(feeling, number_strains_with_feeling, total_feeling_count
                                                         , ave_feeling_count, median_feeling_count
                                                         , min_feeling, max_feeling))
    f.close()

find_names('effects.json', effects)
find_names('negatives.json', negatives)
find_names('medical.json', medicals)
make_name_file('names.txt', effects, negatives, medicals)
make_simple_info_file('effect simple info.txt', effects)
make_simple_info_file('negative simple info.txt', negatives)
make_simple_info_file('medical simple info.txt', medicals)


