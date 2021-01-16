import sys
class Item:
    weights = {
        "Hitroll": 0,
        "Damroll": 0,

        "Mana": .1,
        "Hit Points": 0,

        "Mage Spells": 200,
        "Cleric Spells": 0,

        "Dexterity": 0,
        "Constitution":0,
        "Intelligence": 0,
        "Strength": 0,
        "Wisdom": 0,

        "Moves": 0,

        "Save vs Spell": 0,
        "Armor Class": 0,
        "Save vs Breath": 0,
        "Save vs Affect": 0,
        "Damage": 0,

    }

    name = None

    classRestriction = None
    antiClassRestriction = None
    levelres = None
    align = None  # THIS IS YOU CAN WEAR IT GOOD ITEMS WITH GOOD PEOPLE

    damage = None
    score = None
    slot = None
    affects = None
    grants = None

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def generate_score(self):
        self.score = 0
        for k, v in self.affects.items():
            if v != 0:
                # print(v,self.weights[k.strip()])
                try:
                    self.score += int(v) * self.weights[k.strip()]
                except ValueError:
                    print(self.name)
                    print(f"v {v}")
                    print(f"k strip {k.strip()}")
                    print(f"weight self.weights[k.strip()]")
                    sys.exit()
        if self.damage is not None:

            self.score += self.damage * self.weights['Damage']


    def __key(self):
        to_hash = [
                   self.classRestriction,
                   self.levelres,
                   self.align,
                   self.damage,
                   self.slot]
        for k, v in self.affects.items():
            to_hash.append((k.strip(), v))
        for k, v in self.grants.items():
            to_hash.append((k.strip(), v))

        return tuple(to_hash)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__key() == other.__key()
        return NotImplemented

    def __init__(self):
        self.affects = {
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
            "Constitution": 0

        }
        self.classRestriction = []
        self.antiClassRestriction = []
        self.grants = []
        self.align = ["Good", "Neutral", "Evil"]

    def __str__(self):
        ret = f"{self.score} -- {self.name}\n"
        for k, v in self.affects.items():
            if v != 0:
                ret += f"\t{k}: {v}"
        ret += f"\n\tREQ {self.levelres} {self.align} {self.classRestriction}"
        return ret

    def __repr__(self):
        return str(self)

    def build_item(self, ilines):

        # print("YES THIS IS BEING CALLED")
        for iline in ilines:
            if "Affects" in iline:
                # EXTRACT AFFECTS AND AMOUNTS
                # print(iline)
                iline = iline[9:]
                parts = iline.split("by")
                affect, amount = parts
                if "(" in amount and ")" in amount:
                    startp = amount.find("(")
                    endp = amount.find(")")
                    add = amount[startp + 1:endp]
                    amounts = amount.strip().split(" ")
                    amount = int(amounts[0].strip()) + int(add.strip())
                self.affects[affect.strip()] = amount
                continue
            elif "Object" in iline:  # We are also going to get worn here, and item type
                # EXTRACT NAME
                parts = iline.split("  ")
                sub_part = parts[0].split(":")
                self.name = sub_part[1].strip()

                if "Item type" in iline and "Worn" not in iline:
                    parts = iline.split("type: ")
                    if parts[1] == "Other":  # THIS ISNT USEFUL TO ME
                        return None
                    if parts[1] == "Light":
                        self.slot = 0  # SLOT 0
                if "Worn" in iline:
                    if "Item type" in iline:
                        parts = iline.split("  ")
                        # print(parts)
                        sub_part = parts[1].split("Worn: ")
                        slot = sub_part[1]
                        # print(slot)
                    else:
                        parts = iline.split("Worn: ")
                        # print(parts)
                        slot = parts[1]
                        """
                        <used as light>           0---
                        <worn on finger>          1--- x2
                        <worn around neck>        2--- x2
                        <worn on body>            3---
                        <worn on head>            4---
                        <worn on legs>            5---
                        <worn on feet>            6---
                        <worn on hands>           7---
                        <worn on arms>            8---
                        <worn as shield>          9---
                        <worn about body>         10---
                        <worn about waist>        11--- x2
                        <worn around wrist>       12---
                        <primary weapon>          13---
                        <held>                    14--- 
    
                        """
                    if slot == "Finger":
                        self.slot = 1  # SLOT 1
                        continue
                    if slot == "Neck":
                        self.slot = 2
                        continue
                    if slot == "Body":
                        self.slot = 3
                        continue
                    if slot == "Head":
                        self.slot = 4
                        continue
                    if slot == "Legs":
                        self.slot = 5
                        continue
                    if slot == "Feet":
                        self.slot = 6
                        continue
                    if slot == "Hands":
                        self.slot = 7
                        continue
                    if slot == "Arms":
                        self.slot = 8
                        continue
                    if slot == "Shield":
                        self.slot = 9
                        continue
                    if slot == "About":
                        self.slot = 10
                        continue
                    if slot == "Waist":
                        self.slot = 11
                        continue
                    if slot == "Wrist":
                        self.slot = 12
                        continue
                    if slot == "Wield":
                        self.slot = 13
                        continue
                    if slot == "Hold":
                        self.slot = 14
                        continue
                    print(iline)
                    print("WE GOT HERE AND SHOULDNT HAVE -- SLOT")
                    continue
            elif "Class Restrictions:" in iline:
                parts = iline[20:].split(",")
                if "Only" in iline:
                    for part in parts:
                        part = part.replace("Only", "")
                        self.classRestriction.append(part.strip())
                if "Anti" in iline:
                    for part in parts:
                        part = part.replace("Anti-", "")
                        self.antiClassRestriction.append(part.strip())
                # print(self.classRestriction)
            elif "Grants:" in iline:
                part = iline[11:].strip()
                # print(part)
                self.grants.append(part)
            elif "Item is:" in iline:
                if "Anti" in iline:
                    iline = iline.replace("Item is: ", "")
                    parts = iline.split(", ")
                    # print(parts)
                    for part in parts:
                        if "Anti" in part:
                            if "Good" in part:
                                self.align.remove("Good")
                                # print("no good")
                            elif "Evil" in part:
                                self.align.remove("Evil")
                                # print("no evil")

                            elif "Neutral" in part:
                                self.align.remove("Neutral")
                                # print("no neut")

                            else:
                                print("HOW DID I GET HERE?")
            elif "Level" in iline:
                # print(iline)
                parts = iline.split("Level: ")
                level = parts[1].replace(" Stat ", "")
                # print(level)
                self.levelres = level
            elif "average damage" in iline:
                # print(iline)
                parts = iline.split()
                self.damage = float(parts[len(parts) - 1])
                # print(float(parts[len(parts)-1]))
            else:
                # print(iline)
                if "Durability" in iline:
                    pass
                elif "Can affect you as" in iline:
                    pass
                elif "      None" == iline or "None" == iline:
                    pass
                elif "Weapon enchant" in iline:
                    pass
                elif "Maximum weight" in iline:
                    pass
                elif "Hours of light:" in iline:
                    pass
                elif "You feel informed" in iline:
                    pass
                elif "This Scroll casts:" in iline:
                    pass
                elif iline.encode('ascii') == b'' or iline == b'':
                    pass
                else:
                    print("*" * 100)
                    print(iline.encode('ascii'))
                    print(iline)

                    print("WE HAVENT ACCOUNTED FOR THIS LINE")
