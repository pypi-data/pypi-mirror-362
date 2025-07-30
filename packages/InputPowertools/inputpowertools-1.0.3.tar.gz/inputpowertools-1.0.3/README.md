# InputPowertools
> Eliminate the annoyances of getting input or building a cli in python!
## Prolog
I love using **c**ommand **l**ine **i**nterfaces and I think most people like building these small tools as well, but its really annoying to have to build the interface between the user and your program, hence I build this python package to take care of this part for you.
## Installation
```shell
$ pip install InputPowertools
```
## Examples
### input()
#### Alpha
```
>>> print(f"Result: {input('Type your name:', Mode.ALPHA)}")

Type your name:  >? 123
🛑 Please enter a value that is completely alphabetic (no punctuation, numbers, emojis or nothing)...
Type your name:  >? Malte
Result: Malte
```
#### Numeric
```
>>> print(f"Result: {input('How old are you:', Mode.NUMERIC, domain=lambda x: x % 1 == 0)}")

How old are you:  >? 😀
🛑 Please enter a number...
How old are you:  >? 13.5
🛑 Please enter a value that fits the answers domain...
How old are you:  >? 16
Result: 16
```
#### Options
```
>>> print(f"Result: {input('Are you a what kind of person are you?', Mode.OPTIONS, options=['Cat person', 'Dog person', 'Bird person'])}")

Are you a what kind of person are you? 
1 -> Cat person
2 -> Dog person
3 -> Bird person
Select option [1-3]:  >? Though question
🛑 Please enter a number...
Select option [1-3]:  >? 0
🛑 Please enter a value that fits the answers domain...
Select option [1-3]:  >? 4
🛑 Please enter a value that fits the answers domain...
Select option [1-3]:  >? 2
Result: (1, 'Dog person')
```
### Regex
```
>>> print(f"Result: {input('What is your favorite hex color?', Mode.REGEX, regex=r'(#([a-fA-F0-9]{6}|[a-fA-F0-9]{3}))', regex_description='Hexadecimal Color. Something like #123 or #FF32CD')}")

What is your favorite hex color?  >? red
🛑 Please enter a value that fits this description: Hexadecimal Color. Something like #123 or #FF32CD
What is your favorite hex color?  >? #F00
Result: #F00
```
### Defaults
#### Just pressing enter
```
>>> print(f"Result: {input('Type your name:', Mode.ALPHA, default='Hannes')}")

Type your name: (Hannes) >? 
Result: Hannes
```
#### Typing something else
```
>>> print(f"Result: {input('Type your name:', Mode.ALPHA, default='Hannes')}")

Type your name: (Hannes) >? Malte
Result: Malte
```
### Confirm
```
>>> print(f"Result: {input('Type your name:', Mode.ALPHA, confrim=True)}")

Type your name:  >? Malte
Do you want to select "Malte"? 
1 -> yes
2 -> no
Select option [1-2]: (2) >? 1
Result: Malte
```
## CLI
### Guide
```
$  python examples/example\ 1.py

For more information: examples/example 1.py --help
```
### Analysing the docstring and type hints to generate --help
```
$  python examples/example\ 1.py --help

Some function
  A function that is truly amazing... wow!
Return: Some fascinating thing
        Options:
                --help
                        Prints out information about the program.
                         Type:    bool
                         Default: False
                --a
                        Is a variable called a
                --b
                        Is a variable called b
                         Type:    str
                --c
                        Is a variable called c
                         Type:    list
                --d
                        Is a variable called d
                         Type:    bool
                         Default: False
```
### Analysing the function parameters to generate cli
```
$ python examples/example\ 1.py  --a lol --b "this is a value with spaces" --c 4 2 "test123" --d

a='lol' b='this is a value with spaces' c=[4, 2, 'test123'] d=True
```
