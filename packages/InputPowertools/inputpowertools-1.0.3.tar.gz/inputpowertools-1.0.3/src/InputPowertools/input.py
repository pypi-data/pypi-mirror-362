import re
from enum import Enum
from typing import Union, Callable

from colorama import Style, Fore

# this is just the default configuration for the InputPowertools.input function
default_config = {
    'add space after question': True,
    'number of allowed errors': 10,
    'use emojis': True,
    'color schema': {
        'error': Fore.RED,
        'default': Fore.LIGHTCYAN_EX,
        'question': {
            'normal': Fore.GREEN,
            'option': Fore.YELLOW
        },
        'options': {
            'index': Fore.CYAN,
            'answer': Fore.BLUE
        }
    }
}


class Mode(Enum):
    """Input modes for InputPowertools.input


    > NORMAL is just like the normal input() gets a question in form of a str, returns the answer as a str.

    > ALPHA is similar to NORMAL, but it only accepts answers that return true on answer.isalpha().

    > NUMERIC is similar to NORMAL, but it only accepts answers that are full matches for re'[+|-]?\d+(.\d+)?' this regular expression, than the answer will be returned as a float, but if the answer does all so not contain a . than the answer will be returned as a int.

    > REGEX only accepts answers that fit the entered regex

    > OPTIONS this will prompt the user with a selection (it is best just to test it or to look at the docs to understand what I mean), when the user chooses one of these it will return the answer in this form (index, options[index]).
    """
    NORMAL = 0
    ALPHA = 1
    NUMERIC = 2
    REGEX = 3
    OPTIONS = 4


def _numeric_input_handler(question: str, confirm: bool, domain: callable, default: int or float, config):
    if default:
        assert domain(default)
    for _ in range(config['number of allowed errors']):
        str_value = std_input(f"{config['color schema']['question']['normal']}{question} {config['color schema']['default'] + f'({default})' if default else ''}{Style.RESET_ALL}{(' ' if config['add space after question'] else '')}")
        if default and str_value == '':
            if confirm and input(f'Do you want to select \"{default}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                return default
            elif confirm:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                continue
            else:
                return default
        if re.fullmatch(r'[+|-]?\d+(.\d+)?', str_value):
            value = int(str_value) if not '.' in str_value else float(str_value)
            if domain(value):
                if confirm and input(f'Do you want to select \"{value}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                    return value
                elif confirm:
                    print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                    continue
                else:
                    return value
            else:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Please enter a value that fits the answers domain...{Style.RESET_ALL}")
        else:
            print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Please enter a number...{Style.RESET_ALL}")
    print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Terminated after {config['number f allowed errors']} errors! {Style.RESET_ALL}")
    return False


def _options_input_handler(question: str, confirm: bool, options, default: int, config):
    if default:
        assert default in range(len(options))

    print(config['color schema']['question']['normal'] + question + Style.RESET_ALL + (' ' if config['add space after question'] else ''))

    for i, option in enumerate(options):
        print(f"{config['color schema']['options']['index']}{i + 1}{Style.RESET_ALL} {'-' * int(len(str(len(options))) - len(str(i + 1)))}-> {config['color schema']['options']['answer']}{option}{Style.RESET_ALL}")

    temp = config['color schema']['question']['normal']
    config['color schema']['question']['normal'] = config['color schema']['question']['option']
    index = input(f"Select option {config['color schema']['options']['index']}[1-{len(options)}]{Style.RESET_ALL}:", Mode.NUMERIC, confirm, default=(default + 1) if default else None, domain=lambda x: x in range(1, 1 + len(options)), config=config) - 1
    config['color schema']['question']['normal'] = temp

    return index, options[index]


def _alpha_input_handler(question: str, confirm: bool, default: str, config):
    for _ in range(config['number of allowed errors']):
        value = std_input(f"{config['color schema']['question']['normal']}{question} {config['color schema']['default'] + f'({default})' if default else ''}{Style.RESET_ALL}{(' ' if config['add space after question'] else '')}")
        if default and value == '':
            if confirm and input(f'Do you want to select \"{default}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                return default
            elif confirm:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                continue
            else:
                return default
        if value.isalpha():
            if confirm and input(f'Do you want to select \"{value}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                return value
            elif confirm:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                continue
            else:
                return value
        else:
            print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Please enter a value that is completely alphabetic (no punctuation, numbers, emojis or nothing)...{Style.RESET_ALL}")
    print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Terminated after {config['number f allowed errors']} errors! {Style.RESET_ALL}")
    return False


def _regex_input_handler(question: str, confirm: bool, regex: Union[re.Pattern, str], regex_description: str, default: str, config):
    if default:
        assert regex.fullmatch(default)
    for _ in range(config['number of allowed errors']):
        value = std_input(f"{config['color schema']['question']['normal']}{question} {config['color schema']['default'] + f'({default})' if default else ''}{Style.RESET_ALL}{(' ' if config['add space after question'] else '')}")
        if default and value == '':
            if confirm and input(f'Do you want to select \"{default}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                return default
            elif confirm:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                continue
            else:
                return default
        if re.fullmatch(regex, value):
            if confirm and input(f'Do you want to select \"{value}\"?', Mode.OPTIONS, default=1, options=['yes', 'no'])[1] == 'yes':
                return value
            elif confirm:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}You rejected the value. {Style.RESET_ALL}")
                continue
            else:
                return value
        else:
            if regex_description:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Please enter a value that fits this description: {regex_description}{Style.RESET_ALL}")
            else:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Please enter a value that fits the regex pattern {regex.pattern.title() if isinstance(regex, re.Pattern) else regex}...{Style.RESET_ALL}")
    print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Terminated after {config['number f allowed errors']} errors! {Style.RESET_ALL}")
    return False
    pass


std_input = input


def input(question: str, mode: Mode = Mode.NORMAL, confirm: bool = False, default: Union[str, int, float] = None, options: list[str] = None, domain: Callable[[Union[int, float]], bool] = lambda x: True, regex: Union[re.Pattern, str] = None, regex_description: str = None, config: dict = None) -> Union[str, int, float, tuple[int, str]]:
    """
    Kind of like an addon on to the normal input function.

    :param question: What question do you want to prompt the user with?
    :param mode: What mode do you want? (Look at the docs for InputPowertools.Mode for more information)
    :param confirm: Do you want the user to confirm their answer?
    :param default: What should be the default answer? (This will be returned if the user just hits and enter but if confirm is True it still has to be confirmed!)
    :param options: If you use Mode.OPTIONS, what options do you want?
    :param domain: If you use Mode.NUMERIC, what kind of number do you want? (A x is considered to be in the domain if domain(x) == True
    :param regex: If you use Mode.REGEX, what is the pattern that you are asking for?
    :param regex_description: If you use Mode.REGEX, what does this regex check for?
    :param config: What kind of styling do you want and some other slight things? (You usually will not need to touch this thing)
    :return: The value that the user entered/selected. This will not always be a string: Return types for Mode.NORMAL, Mode.ALPHA and Mode.REGEX: str; Mode.NUMERIC: int or float; Mode.OPTIONS: tuple(int, str).
    """
    # initialize config
    if config is None:
        config = default_config.copy()

    # for numeric
    if mode == Mode.NUMERIC:
        return _numeric_input_handler(question, confirm, domain, (int(default) if float(default) % 1 == 0 else float(default)) if default else None, config)

    # for regex
    if mode == Mode.REGEX:
        return _regex_input_handler(question, confirm, regex, regex_description, default, config)

    # for options
    if mode == Mode.OPTIONS:
        return _options_input_handler(question, confirm, options, int(default) if default else None, config)

    # for alpha
    if mode == Mode.ALPHA:
        return _alpha_input_handler(question, confirm, default, config)

    return std_input(config['color schema']['question']['normal'] + question + Style.RESET_ALL + (
        ' ' if config['add space after question'] else ''))
