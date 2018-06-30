import json

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
                    dic_put_names[name_of_feeling] = [1, value_of_feeling, value_of_feeling, value_of_feeling]
                else:
                    dic_put_names[name_of_feeling][0] += 1
                    dic_put_names[name_of_feeling][1] += value_of_feeling
                    dic_put_names[name_of_feeling][2] = min(value_of_feeling, dic_put_names[name_of_feeling][2])
                    dic_put_names[name_of_feeling][3] = max(value_of_feeling, dic_put_names[name_of_feeling][3])

    for name in dic_put_names:
        dic_put_names[name].append(dic_put_names[name][1] / dic_put_names[name][0])


def make_name_file(name_of_file, effect_dict, neg_dict, medical_dict):
    f = open(name_of_file, 'w')
    f.write('effect names: ' + str(list(effect_dict.keys())) + '\n')
    f.write('negative names: ' + str(list(neg_dict.keys())) + '\n')
    f.write('medical names: ' + str(list(medical_dict.keys())) + '\n')
    f.close()


def make_simple_info_file(name_of_file, dict):
    f = open(name_of_file, 'w')
    f.write('form of name: number of strains with feeling, total count of feeling, min value, max value, ave count of feeling\n')
    for feeling in dict:
        f.write("{} : {}\n".format(feeling, dict[feeling]))
    f.close()

find_names('effects.json', effects)
find_names('negatives.json', negatives)
find_names('medical.json', medicals)
make_name_file('names.txt', effects, negatives, medicals)
make_simple_info_file('effect simple info.txt', effects)
make_simple_info_file('negative simple info.txt', negatives)
make_simple_info_file('medical simple info.txt', medicals)


