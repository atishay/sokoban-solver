from Level import Level
import cPickle as pickle
from supervised import getAction

data = {}

def load(file):
    with open(file, "rb") as input_file:
        d = pickle.load(input_file)
        global data
        data = dict(data.items() + d.items())


load("test-0-8-weight.pkl")
load("test-1-37476-weight.pkl")
load("test-2-41617-weight.pkl")
load("test-3-43652-weight.pkl")
load("test-4-43837-weight.pkl")
load("test-5-44118-weight.pkl")
load("test-6-44193-weight.pkl")
load("test-7-44414-weight.pkl")
load("test-8-45029-weight.pkl")
load("test-9-48413-weight.pkl")
load("test-10-56545-weight.pkl")
load("test-11-1060338-weight.pkl")
load("test-12-1085133-weight.pkl")
load("test-13-1134657-weight.pkl")
load("test-14-1144167-weight.pkl")
load("magic_sokoban6-1-2340-weight.pkl")
load("magic_sokoban6-2-1267-weight.pkl")
load("magic_sokoban6-3-52620-weight.pkl")
load("magic_sokoban6-4-9330-weight.pkl")
load("magic_sokoban6-5-29500-weight.pkl")
load("magic_sokoban6-6-22410-weight.pkl")
load("magic_sokoban6-7-23044-weight.pkl")
load("magic_sokoban6-8-193683-weight.pkl")
load("magic_sokoban6-9-313548-weight.pkl")

cnt = {'test': [0, 15], 'magic_sokoban6': [1, 10]}
for level_set in ['test', 'magic_sokoban6']:
    for level_number in range(cnt[level_set][0], cnt[level_set][1]):
        level = Level(level_set, level_number).matrix
        if level.toString(True) not in data:
            continue
        oracle = data[level.toString(True)]
        actual = oracle
        learned = ""
        match = 0
        while len(actual) > 0:
            action = getAction(level)[0]
            learned += action
            level = level.successor(actual[0])
            if action is actual[0]:
                match = match + 1
            actual = actual[1:]
        print "Set: %s, Level: %d, Oracle: %s, Learned: %s, Match: %d/%d"%(level_set, level_number, oracle, learned, match, len(oracle))

