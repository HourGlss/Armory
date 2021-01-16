import time
import pickle
from utils.Item import Item


class Player:
    tn = None
    possibleGear = {

    }

    affects = {
        "Moves": 0,
        "Intelligence": 0,
        "Hitroll": 0,
        "Mana": 0,
        "Save vs Breath": 0,
        "Save vs Affect": 0,
        "Strength": 0,
        "Save vs Spell": 0,
        "Armor Class": 0,
        "Wisdom": 0,
        "Mage Spells": 0,
        "Cleric Spells": 0,
        "Damroll": 0,
        "Hit Points": 0,
        "Dexterity": 0,
    }
    details = {
        "username": "Radicaledward",
        "password": "password",
        "level": 41,
        "align": "Good",  # Use a capital at start
        "class": ["Mage", "Cleric", "Thief", "Illusionist"]  # use a properly spelled class name with capital
        # "class": ["Cleric","Mage","Warrior","Ranger"]
        # "class": ["Cleric"]
    }

    totals = {
        "Moves": 0,
        "Intelligence": 0,
        "Hitroll": 0,
        "Mana": 0,
        "Save vs Breath": 0,
        "Save vs Affect": 0,
        "Strength": 0,
        "Save vs Spell": 0,
        "Armor Class": 0,
        "Wisdom": 0,
        "Mage Spells": 0,
        "Cleric Spells": 0,
        "Damroll": 0,
        "Hit Points": 0,
        "Dexterity": 0,
        "Constitution": 0,
    }

    logged_in = False

    gear = None

    slot_meaning = {
        0: "Light",
        1: "Finger",
        2: "Neck",
        3: "Body",
        4: "Head",
        5: "Legs",
        6: "Feet",
        7: "hands",
        8: "Arms",
        9: "Shield",
        10: "About",
        11: "Waist",
        12: "Wrist",
        13: "Weapon",
        14: "Held"
    }

    def __print_response(self):
        response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        print("---")
        for i, line in enumerate(response.decode('ascii').split("\n")):
            print(i, line)

    def get_detail(self, detail):
        return f"{self.details[detail]}\n".encode('ascii')

    def login(self):
        line = self.tn.read_very_eager()
        if line == b'':
            return

        try:

            line = line.decode('ascii')
            print(line)
        except:
            self.tn.write("\n".encode('ascii'))

            return
        # if line != "":
        #     print(line.strip())
        if "what name do you wish to be known?" in line:
            self.tn.write(self.get_detail("username"))
            print("username")
        if "Password:" in line:
            print("pass")

            self.tn.write(self.get_detail("password"))
            resp = self.tn.read_very_eager()
            # print(resp)
            # print("stop pass")
        if "PRESS RETURN" in line:
            self.tn.write("\n".encode('ascii'))
            resp = self.tn.read_very_eager()
            print("rett")
        if "Do you have an ANSI" in line:
            self.tn.write("y\n".encode("ascii"))
            resp = self.tn.read_very_eager()
            print("ascii check")
        if "Make your choice:" in line:
            self.tn.write("1\n".encode('ascii'))
            resp = self.tn.read_very_eager()
            print("enter world")
            self.logged_in = True
        if "over your own body" in line:
            print("take over")
            self.logged_in = True
        if "Reconnecting" in line:
            print("recon")
            self.logged_in = True

    def logout(self):
        print("logout start")
        self.tn.write("goho\n".encode('ascii'))
        # response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        self.tn.read_very_eager()
        self.tn.write("quit\n".encode('ascii'))
        # response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        self.tn.read_very_eager()
        time.sleep(1)
        self.tn.write("0\n".encode('ascii'))
        time.sleep(1)
        print("Logout complete")

    def get_inv(self):
        print("get inv")
        # self.tn.write(f"c det inv \n".encode('ascii'))
        # response = self.tn.read_until(b"123", timeout=1)
        time.sleep(1)
        response = self.tn.read_until(b"123", timeout=1)
        self.tn.write("inv\n".encode('ascii'))
        response = self.tn.read_until(b"123", timeout=1)
        # print("------" * 20)
        # print(response.decode('ascii'))
        # print("------" * 20)
        lines = response.decode('ascii').split("\n")
        # print(lines)
        items_to_id = []
        itemnames = {}
        for line in lines:
            line = line.strip()
            if "examine" in line:
                start = line.find("examine") + len("examine ")

                end = line.find("|")
                part = line[start:end].strip()
                part.replace(".", "")
                new = ""
                for c in part:
                    if c.isalpha():
                        new += c
                count = 1
                if line.startswith("("):
                    startp = line.find("(")
                    endp = line.find(")")
                    count = int(line[startp + 1:endp])
                if new not in itemnames.keys():
                    itemnames[new] = count
                else:
                    itemnames[new] += count
        for k, v in itemnames.items():
            if v == 1:
                items_to_id.append(k)
            else:
                for i in range(1, v + 1):
                    if i != 1:
                        items_to_id.append(f"{i}.{k}")
                    else:

                        items_to_id.append(k)
        return items_to_id

    def __clean(self, s):
        normal = ""
        cap = True
        for c in s:
            if c == '\x1b':
                cap = False
                continue
            if not cap and c == "m":
                cap = True
                continue
            if cap:
                normal += c
        return normal

    def __extract_id_only(self, k):
        start = False
        good_part = []
        for c in k:
            # print(c)
            if "You feel informed" in c:
                # print("start")
                start = True
                continue
            if start:
                # print("in start")
                if "xp]" in c:
                    # print("END")
                    return good_part
                if c != "":
                    good_part.append(c.strip())

    def id_all(self, itemnames):
        print("start ID")
        # self.tn.write(f"c det inv \n".encode('ascii'))
        # response = self.tn.read_until(b"123", timeout=1)
        items = []
        for k, name in enumerate(itemnames):
            print(f"id item {k} {name}")
            done = False
            while not done:

                # print(f"c id {name}")
                self.tn.write(f"c id {name}\n".encode('ascii'))
                response = self.tn.read_until(b"123", timeout=1)
                clean = self.__clean(response.decode('ascii'))
                # print(clean)
                # print("\t\t\t\t\t\tLENGTH",len(response.decode('ascii')))
                if "You haven't the energy to cast that spell!" in clean:
                    print(response.decode('ascii'))
                    print("RAN OUT OF MANA")
                    time.sleep(20)
                    # print("dont sleeping")
                    continue
                if "You lost your conc" not in clean:
                    done = True
                    i = Item()

                    # print(clean)
                    id_only = self.__extract_id_only(clean.split("\n"))
                    if id_only is not None:
                        i.build_item(id_only)
                        i.generate_score()
                        print(k, i)
                        items.append(i)
                        self.tn.write(f"sayid\n".encode('ascii'))
                        response = self.tn.read_until(b"123", timeout=1)
                    else:
                        print("ITEM WAS NONE", name)
                        print("======================")
                        print(response)
                        print("======================")

                if "Cannot find the target of your spell" in clean:
                    print("CANNOT FIND ITEM", name)
        print("SAVING ITEMS")
        print(f"ITEMS LENGTH {len(items)}")
        pickle.dump(items, open(f"./data/{self.details['username']}.p", "wb"))

    def sort_items(self, item):
        if item.slot not in self.possibleGear.keys():
            self.possibleGear[item.slot] = []
        self.possibleGear[item.slot].append(item)
        # print(f"adding {item} to {item.slot}")

    def can_wear(self, item):
        if int(item.levelres) > int(self.details['level']):
            return False
        if len(item.classRestriction) != 0:
            # print("MUST")
            # print(item.classRestriction)
            # print(self.details['class'])
            union = set.intersection(set(self.details["class"]), set(item.classRestriction))
            if len(union) == 0:
                # print("---FALSE")
                return False
        if len(item.antiClassRestriction) != 0:
            # print("ANTI")
            # print(item.antiClassRestriction)
            # print(self.details['class'])
            for cla in self.details["class"]:
                if cla in item.antiClassRestriction:
                    # print("---FALSE")

                    return False
        if self.details['align'] not in item.align:
            return False
        return True

    def find_gear(self):
        # 2 - 1
        # 2 - 2
        # 2 - 12
        self.gear = {
            12: [],
            0: None,
            1: [],
            4: None,
            11: None,
            13: None,
            6: None,
            14: None,
            2: [],
            8: None,
            10: None,
            7: None,
            3: None,
            9: None,
            5: None,
        }
        if "Ranger" in self.details['class']:
            self.gear[13] = []
        possibleGear = self.possibleGear.copy()
        # FIND A SORT GEAR
        # k = SLOT
        # v = list of items
        for k, v in possibleGear.items():
            if k is not None:
                # for p in v:
                # print(p)
                # time.sleep(5)
                # print("-----------   S O R T   -------------")

                v.sort()
                # temp = v.pop()
                # print(temp)
                # print("-----------   E N D   -------------")
                # print(self.slot_meaning[k])
                # for p in v:
                #     print(p)
                # break
                if k == 1 or k == 2 or k == 12:
                    for i in range(2):
                        # print(item)
                        # print(k)
                        # print(self.gear[k])
                        done = False
                        while not done:
                            possible = v.pop()
                            if self.can_wear(possible):
                                done = True
                                self.gear[k].append(possible)
                elif "Ranger" in self.details['class'] and k ==13:
                    for i in range(2):
                        # print(item)
                        # print(k)
                        # print(self.gear[k])
                        done = False
                        while not done:
                            possible = v.pop()
                            if self.can_wear(possible):
                                done = True
                                self.gear[k].append(possible)
                else:

                    done = False

                    while not done:

                        possible = v.pop()

                        if self.can_wear(possible):
                            done = True
                            self.gear[k] = possible

        # GET TOTALS FOR STATS
        for k, v in self.gear.items():
            # print(self.slot_meaning[k])
            if k is None:
                print("k was NONE")
                continue
            if v is None:
                print("v was none")
                continue

            if k == 1 or k == 2 or k == 12 or ("Ranger" in self.details['class'] and k ==13):
                for e in v:
                    # print(e)
                    for affect, value in e.affects.items():
                        self.totals[affect.strip()] += int(value)

            else:
                # print(v)
                for affect, value in v.affects.items():
                    self.totals[affect.strip()] += int(value)

        # PRINT THE GEAR TO WEAR
        for k, v in self.totals.items():
            print(k, v)

    def show_all_possibles(self):
        for k, v in self.possibleGear.items():
            print(self.slot_meaning[k])
            if k == 1 or k == 2 or k == 12:
                for u in v:
                    print(u)
            else:
                print(v)

    def print_gear(self):
        for k, v in self.gear.items():
            print(self.slot_meaning[k])
            if k == 1 or k == 2 or k == 12:
                for u in v:
                    print(u)
            else:
                print(v)
