import json


def get_classes():
    with open("defect.json") as jsonfile:
        defect_dict = json.load(jsonfile)
        return defect_dict['defects']
