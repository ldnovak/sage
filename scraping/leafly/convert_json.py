import pandas as pd
import json

effect_names = ['Relaxed', 'Hungry', 'Sleepy', 'Creative', 'Energetic', 'Aroused', 'Uplifted', 'Happy', 'Tingly', 'Euphoric', 'Giggly', 'Talkative', 'Focused']
negative_names = ['Relaxed', 'Hungry', 'Sleepy', 'Creative', 'Energetic', 'Aroused', 'Uplifted', 'Happy', 'Tingly', 'Euphoric', 'Giggly', 'Talkative', 'Focused']
medical_names = ['Relaxed', 'Hungry', 'Sleepy', 'Creative', 'Energetic', 'Aroused', 'Uplifted', 'Happy', 'Tingly', 'Euphoric', 'Giggly', 'Talkative', 'Focused']
def json_to_pd(json_path, type=None):
    if type == 'effects':
        names = effect_names
    elif type == 'negatives':
        names = negative_names
    elif type == 'medical':
        names = medical_names
    else:
        names = get_json_names(json_path)
    df = pd.DataFrame(columns=names)
    with open(json_path, 'r') as json_obj:
        strain_dict = json.load(json_obj)
        for strain in strain_dict:
            effect_dict = {}
            for effect, value in strain_dict[strain]:
                effect_dict[effect] = value
            row = []
            for effect in names:
                if effect in effect_dict:
                    row.append(effect_dict[effect])
                else:
                    row.append(0)
            df.loc[strain] = row
    return df

def get_json_names(json_path):
    names = set()
    with open(json_path, 'r') as json_obj:
        strain_dict = json.load(json_obj)
        for strain in strain_dict:
            for name, value in strain_dict[strain]:
                names.add(name)
    return list(names)



