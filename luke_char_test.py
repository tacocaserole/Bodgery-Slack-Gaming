import luke_character
import diceroll
import json


def test_char():
    print("This will allow you to enter a body of text as if it were passed to the handler.")
    cont = "1"
    """
    izzy = luke_character.Character("izzy")
    obj = {'a': 2}
    output=json.dumps(obj)
    print(type(output))
    input = json.loads(output)
    print(type(input))
    """

    while cont == "1":
        print("What is your input message?")
        command = input()
        cmd = '1'
        luke_character.CharacterHandler("abc").handle_mention("abc", "DEF", cmd, command, "channel")
        print("Do you want to continue? 1/0")
        cont = input()


test_char()