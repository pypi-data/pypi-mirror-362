import re
import sys
import inspect

import typic
from colorama import Fore, Style
from docstring_parser import parse

default_config = {
    'color schema': {
        'short docstring': Fore.LIGHTGREEN_EX,
        'long docstring': Fore.GREEN,
        'return': Fore.LIGHTRED_EX,
        'command': Fore.BLUE,
        'description': Fore.MAGENTA,
        'key': Fore.CYAN,
        'type': Fore.RED,
        'default': Fore.YELLOW,
        'error': Fore.RED
    },
    'prefix': {
        'short description': '',
        'long description': ' ',
        'return': 'Return: ',
        'options': '\t',
        'option': '\t\t',
        'option description': '\t\t\t',
        'flags': '\t\t\t '
    },
    'use emojis': True
}


def run(function: callable, config=None):
    if config is None:
        config = default_config

    # parsing the function_parameters
    function_parameters = inspect.signature(function).parameters

    # parsing the docstring
    if function.__doc__:
        docstring = parse(function.__doc__)
    parameter_descriptions = dict([
        (meta.args[1], meta.description)
        for meta in docstring.meta if meta.args[0] != 'return' and meta.description != ''
    ]) if docstring is not None else {}

    # parsing the sys.argv
    args = sys.argv[1:]
    parameters_list = []
    for arg in args:
        if len(arg) >= 3 and arg[:2] == '--':
            parameters_list.append([arg[2:], []])
        else:
            value = arg
            if isinstance(value, str):
                if value == 'True' or value == 'False':
                    parameters_list[-1][1].append(value == 'True')
                    continue
                if re.fullmatch(r'[+|-]?\d+(.\d+)?', value):
                    float_val = float(value)
                    if float_val % 1 == 0:
                        parameters_list[-1][1].append(int(float_val))
                        continue
                    parameters_list[-1][1].append(float_val)
                    continue
            parameters_list[-1][1].append(arg)
    for parameter_list in parameters_list:
        if len(parameter_list[1]) == 1:
            parameter_list[1] = parameter_list[1][0]
        elif len(parameter_list[1]) == 0:
            parameter_list[1] = True
    parameters = dict(parameters_list)

    if len(function_parameters) == 0:
        # function doesn't take any parameters, so I just run the function
        function()
    else:
        if len(sys.argv) == 1:
            print(f"For more information: {config['color schema']['command']}{sys.argv[0]} --help{Style.RESET_ALL}")
        elif sys.argv[1] == '--help':
            docstring = None
            if docstring:
                print(config['prefix']['short description'] + config['color schema']['short docstring'] + docstring.short_description + Style.RESET_ALL)
                if docstring.long_description:
                    print(f"{config['prefix']['long description']}{config['color schema']['long docstring']} {docstring.long_description + Style.RESET_ALL}")
                if docstring.meta[-1].args[0] == 'return':
                    print(f"{config['prefix']['return']}{config['color schema']['return']}{docstring.meta[-1].description}{Style.RESET_ALL}")

            print(f"{config['prefix']['options']}Options:")
            print(f"{config['prefix']['option']}{config['color schema']['command']}--help{Style.RESET_ALL}")
            print(f"{config['prefix']['option description']}{config['color schema']['description']}Prints out information about the program.{Style.RESET_ALL}")
            print(f"{config['prefix']['flags']}{config['color schema']['key']}Type:    {config['color schema']['type']}bool{Style.RESET_ALL}")
            print(f"{config['prefix']['flags']}{config['color schema']['key']}Default: {config['color schema']['default']}False{Style.RESET_ALL}")

            for key in function_parameters.keys():
                parameter = function_parameters[key]
                print(f"{config['prefix']['option']}{config['color schema']['command']}--{parameter.name}{Style.RESET_ALL}")

                if parameter.name in parameter_descriptions:
                    print(f"{config['prefix']['option description']}{config['color schema']['description']}{parameter_descriptions[parameter.name]}{Style.RESET_ALL}")

                if parameter.annotation.__name__ != '_empty':
                    print(f"{config['prefix']['flags']}{config['color schema']['key']}Type:    {config['color schema']['type'] + parameter.annotation.__name__}{Style.RESET_ALL}")

                if parameter.default != parameter.empty:
                    print(f"{config['prefix']['flags']}{config['color schema']['key']}Default: {config['color schema']['default']}{parameter.default}{Style.RESET_ALL}")
        else:
            try:
                typic.al(function, strict=True)(**parameters)
            except typic.constraints.error.ConstraintValueError as e:
                print(f"{config['color schema']['error']}{'🛑 ' if config['use emojis'] else ''}Type Error: {e}{Style.RESET_ALL}")
