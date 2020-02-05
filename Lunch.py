from yaml import load
from random import choice

def lunch():
    restos = load(open('restos.yml'))
    cat = choice(list(restos.keys()))
    resto = choice(restos[cat])
    return resto