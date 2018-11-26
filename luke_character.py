import diceroll
import mentionrouter
import json
import os

skill_ability = {"str": "str", "dex": "dex", "con": "con", "int": "int", "wis": "wis", "cha": "cha", "proflist": "",
                 "athletics": "str", "acrobatics": "dex", "sleight_of_hand": "dex", "stealth": "dex",
                 "arcana": "int", "history": "int", "investigation": "int", "nature": "int", "religion": "int",
                 "animal_handling": "wis", "insight": "wis", "medicine": "wis", "perception": "wis",
                 "survival": "wis", "deception": "cha", "intimidation": "cha", "performance": "cha",
                 "persuasion": "cha"}


class NoCharacterException(Exception):
    """Thrown when the asked Character doesn't exist"""
    def __init__(self, asked_character):
        self.asked_character = asked_character
        print("sorry, I don't know who that is!")


class NotaTaskException(Exception):
    """Thrown when the number of dice is too big"""
    def __init__(self, asked_task):
        self.asked_task = asked_task


class NotaAbilityException(Exception):
    """Thrown when the number of dice is too big"""
    def __init__(self, asked_ability):
        self.asked_ability = asked_ability


class Character:

    def __init__(self, name):
        self.__Character__ = True
        self.CharName = str(name)
        self.level = 1
        self.proflist = {"str": 0
                         }
        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0

        self.athletics = 0

        self.acrobatics = 0
        self.sleight_of_hand = 0
        self.stealth = 0

        self.arcana = 0
        self.history = 0
        self.investigation = 0
        self.nature = 0
        self.religion = 0

        self.animal_handling = 0
        self.insight = 0
        self.medicine = 0
        self.perception = 0
        self.survival = 0

        self.deception = 0
        self.intimidation = 0
        self.performance = 0
        self.persuasion = 0

    def stat_mod(self, ability):
        mod = (getattr(self, skill_ability[ability])-10)//2
        dct = self.proflist
        print(dct)
        prof = int(dct[ability]) * self.cur_prof_bonus()
        return mod + prof

    def roll_stat(self, stat, adv, bonus):
        statmod = self.stat_mod(stat)
        if adv == "+":
            result = max(diceroll.DiceRoll().roll(20, 2))
            msg = "With Advantage, you "
        elif adv == "-":
            result = min(diceroll.DiceRoll().roll(20, 2))
            msg = "With Disadvantage, you "
        else:
            result = max(diceroll.DiceRoll().roll(20, 1))
            msg = "You flatly "
        total = int(result) + int(statmod) + int(bonus)
        msg = msg + "rolled a " + str(result) + " plus mod of " + str(statmod) + " plus a arbitrary bonus of " + str(bonus)
        msg = msg + " Totalling " + str(total)
        return msg

    def cur_prof_bonus(self):
        return 2 + int(self.level/4)

    def update_stat(self, stat, mod):
        """6 primary attributes should be set, along with level and proficiency list
           Then by defualt proficiencies, half-prof, and expertise will not need handling
           rolling will need to lookup proficiencies then.
           if arbitrary mods are needed due to other bonuses, those should be added directly to the ability."""
        try:
            mod = int(mod)
            ability = getattr(self, stat)
            setattr(self, stat, ability + mod)

        except TypeError:
            msg= "this is an error I suppose"

        msg = ""
        return msg

    def write_char(self):
        char_file = open(self.CharName + ".json", "w")
        # json.dump(self,char_file)
        json.dump(self, char_file, default=encode_char)
        char_file.close()


class CharacterHandler(mentionrouter.Handler):
    def __init__(self, slack_client):
        self.slack_client = slack_client

    def handle_mention(self, from_user, to_user, cmd, remaining_msg, channel):

        remaining_msg = (remaining_msg.lower()).replace(" ", "_")
        match = remaining_msg.split(",")
        print(match)

        return_msg = ""
        if match is not None:
            # discern what tasks to do, then do a task
            """
            asked_character = match[0]
            asked_task = match[1]
            asked_ability = match[2]
            asked_value_1 = match[3]
            asked_value_2 = match[4]
            return_msg = ""
            """
            try:
                asked_character = match[0]
                asked_task = match[1]
                asked_ability = 0
                asked_value_1 = 0
                asked_value_2 = 0
            except IndexError:
                print("you didn't input the right number of details!")
            if len(match) >= 3:
                asked_ability = match[2]
            if len(match) >= 4:
                asked_value_1 = match[3]
            if len(match) >= 5:
                asked_value_2 = match[4]

            try:
                if asked_task == "create":
                    return_msg = check_exists(asked_character)
                    if return_msg:
                        return_msg = "This character already exists"
                    else:
                        mychar = Character(asked_character)
                        mychar.write_char()
                        return_msg = roll_scores()

                elif asked_task == "delete":
                    return_msg = del_character(asked_character)

                elif asked_task == "roll":
                    mychar = load_char(asked_character)
                    if isinstance(mychar, Character):
                        return_msg = mychar.roll_stat(asked_ability, asked_value_1, asked_value_2)

                    else:
                        return_msg = mychar

                elif asked_task == "update":
                    mychar = load_char(asked_character)
                    if isinstance(mychar, Character):
                        return_msg = mychar.update_stat(asked_ability, asked_value_1)
                        return_msg = return_msg + str(mychar.__getattribute__(asked_ability))
                        return_msg = return_msg + str(mychar.write_char())

                    else:
                        return_msg = mychar
                else:
                    return_msg = "I don't know how to do that yet, why don't you practice some python and teach me how!"

            except NoCharacterException:
                return_msg = "Sorry, I can't find that character.  Check your spelling? "
                return_msg = return_msg + "I'm not case-sensitive."

            except NotaAbilityException:
                return_msg = "Sorry, that ability hasn't been defined. Check your spelling? "
                return_msg = return_msg + "I'm not case-sensitive."


        else:
            return_msg = "Sorry, I don't know how to roll that. Try something like "
            return_msg = return_msg + "'character,bagadesh,roll,perception'"

        print(return_msg)
        # self.slack_client.api_call("chat.postMessage", channel=channel, text=return_msg, )


def new_ability_score():
    rolls = diceroll.DiceRoll().roll(6, 4)
    # print(rolls)
    rolls.remove(min(rolls))
    # print(rolls)
    return sum(rolls)


def check_exists(name):
    fname = name + ".json"
    try:
        char_file = open(fname, "r")
        char_file.close()
        return True
    except IOError:
        #raise NoCharacterException
        return False


def roll_scores():
    statlist = ""
    for i in range(6):
        statlist = statlist + str(new_ability_score()) + ", "
    msg = "your rolled stats to distribute are: " + statlist
    return msg


def create_char_file(name):
    char_file = check_exists(name)
    fname = name + ".json"
    if isinstance(char_file, str):
        return False
    else:
        char_file = open(fname, "w")
        char_file.close()
        return True


def del_character(char_name):
    fname = char_name + ".json"
    try:
        os.remove(fname)
        return "*Thanos Snap*  What did it cost?"
    except IOError:
        # raise NoCharacterException(fname)
        return "target not found."


def load_char(char_name):
    exists = check_exists(char_name)
    if exists:
        file_obj = open(char_name + ".json", "r")
        data = file_obj.read()
        print(data)
        # msg = json.load(file_obj)
        msg = json.loads(data, object_hook=decode_char)
    else:
        msg = "Character doesn't exist"
    return msg


def encode_char(char):
    if isinstance(char, Character):
        return (char.__dict__)
    else:
        return "That's not a Character, fugehdaboudit!"


def decode_char(jchar):
    if "__Character__" in jchar:
        """because my character class isn't initialized with a value for every attribute
        I will need to create the object, and then update all of the attributes one by one.
        """
        dummy_char = Character(jchar["CharName"])
        for at in skill_ability:
            # print(type(at))
            setattr(dummy_char, at, jchar[at])
            # print(getattr(dummy_char, at))
        return dummy_char
    else:
        return "What is this file you had me read? Tastes like sand!"
