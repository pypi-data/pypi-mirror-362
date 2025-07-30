from InputPowertools import input, Mode


def test_input():
    print(f"Result: {input('Type your name:', Mode.ALPHA, default='Hannes')}")
    print(f"Result: {input('How old are you:', Mode.NUMERIC, confirm=True, domain=lambda x: x % 1 == 0)}")
    print(f"Result: {input('Are you a what kind of person are you?', Mode.OPTIONS, options=['Cat person', 'Dog person', 'Bird person'])}")
    print(f"Result: {input('What is your favorite hex color?', Mode.REGEX, regex=r'(#([a-fA-F0-9]{6}|[a-fA-F0-9]{3}))', regex_description='Hexadecimal Color. Something like #123 or #FF32CD')}")


if __name__ == '__main__':
    test_input()
