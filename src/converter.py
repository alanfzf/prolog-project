from typing import List
from models.parameter import Parameter, ParamType
from data.values import SYNONYMS, VARIABLES, OBJECTS


def find_relation(word):
    if word in SYNONYMS:
        return word
    # word is not in the dictionary search inside the synonyms list
    for key, value in SYNONYMS.items():
        find = next((syn for syn in value if syn == word), None)
        if find is not None:
            return key
    return None 

def find_vars(variable):
    val = next((var for var in VARIABLES if var == variable), None)
    return val

def find_object(obj):
    val = next((ob for ob in OBJECTS if ob == obj), None)
    return val

def check_sentence(params: List[Parameter]):
    """
    Rules for a good sentence:
    - 3 parameters
    - relation must be in the middle
    - (1 object and 1 variable) or (1 variable and 1 object )
    - (2 variables) or (2 objects)
    """
    if len(params) != 3:
        return False

    patterns = [
        [ParamType.OBJECT, ParamType.RELATION, ParamType.OBJECT],
        [ParamType.VARIABLE, ParamType.RELATION, ParamType.VARIABLE],
        [ParamType.OBJECT, ParamType.RELATION, ParamType.VARIABLE],
        [ParamType.VARIABLE, ParamType.RELATION, ParamType.OBJECT]
    ]
    # extract all paramter types
    ptypes = [param.param_type for param in params]
    # check if all paramters match a defined pattern
    return ptypes in patterns


def search_parameters(sentence):
    words = sentence.split()
    params = []

    for word in words:
        # find relations
        rel = find_relation(word)
        if rel is not None:
            params.append(Parameter(rel, ParamType.RELATION))
            continue
        # find objects
        obj = find_object(word)
        if obj is not None:
            params.append(Parameter(obj, ParamType.OBJECT))
            continue
        # find vars
        var = find_vars(word)
        if var is not None:
            params.append(Parameter(var, ParamType.VARIABLE))
            continue
    return params

def construct_query(params: List[Parameter]):
    rel = params[1]
    val1 = params[0]
    val2 = params[2]

    obj1 = val1.value if val1.param_type == ParamType.OBJECT else 'X' 
    obj2 = val2.value if val2.param_type == ParamType.OBJECT else 'Y'

    return f'{rel.value}({obj1}, {obj2})'
