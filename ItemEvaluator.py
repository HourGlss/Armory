import pickle
from utils.Player import Player
from utils.Item import Item
raditems = pickle.load(open('data/Radicaledward.p', 'rb'))
horoitems = pickle.load(open('data/horologe_longer.p', 'rb'))
items = raditems + horoitems
print(len(items))
p = Player()
for item in items:
    item.generate_score()
    p.sort_items(item)
p.find_gear()
p.print_gear()