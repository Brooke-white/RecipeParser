# coding: utf-8

# Helper functions for RecipeParser and sub classes...


def read_input_file(my_file):
    """
    Reads txt file in, line by line
    :param my_file: path to txt file
    :return: List containing urls
    """
    try:
        with open(my_file, 'r') as f:
            content = f.read().splitlines()
    except IOError:
        raise IOError
    return content


def strip_bad_ascii(string):
    """
    Removes ascii chars excluding those for 1/4, 1/2, and 3/4
    :param string: input string containing ascii to be stripped
    :return: string containing above specified ascii chars
    """
    return "".join(filter(
        lambda x: ord(x) < 128 or 187 < ord(x) < 191, string))


def get_ingredient_table(ingredient_dict):
    """
    Creates a markdown table
    :param ingredient_dict: Dictionary of form {'ingredient' : 'quantity'}
    :return: String containing markdown 2 column table (Quantity|Ingredient)
    """
    ingredient_table = ''

    for ingredient, amount in ingredient_dict.items():
            ingredient_table += "|" + ''.join(amount) + "|" + \
                                 ingredient + "|\n"
    return ingredient_table


def get_ingredient_table_simple(ingredient_list):
    """
    Creates a markdown table
    :param ingredient_list: List of form ['x ingredient a', 'y ingredient b']
    :return: String containing markdown 1 column table (Ingredient)
    """
    ingredient_table = ''
    for ingredient in ingredient_list:
            ingredient_table += "|" + ''.join(ingredient) + "|\n"
    return ingredient_table


def get_ingredient_list_with_subtitles(ingredient_dict):
    """
    Creates a markdown list from a dict containing recipe instructions
    :param ingredient_dict: Dictionary of form
    {'title', ['step0', ... , 'stepX'}}
    :return: String containing markdown list with sub-title
    """
    ingredient_list = ''

    for title, ingredients in ingredient_dict.items():
            ingredient_list += "\n###### " + title + "\n" if title else ''
            for ingredient in ingredients:
                ingredient_list += "* " + ingredient + "\n"
    return ingredient_list


def get_instruction_list(instruction_list):
    """
    Creates a markdown list from a list containing recipe instructions
    :param instruction_list: List of form ['step0', ... , 'stepX']
    :return: String containing markdown list
    """
    instruction_list_string = ''
    for step in instruction_list:
            instruction_list_string += "\n\n* " + step
    return instruction_list_string


def get_instruction_dict_with_subtitles(instruction_dict):
    """
    Creates a markdown list from a dict containing instructions
    :param instruction_dict: Dictionary of form
    {'title' : ['step0', ... , 'stepX']}
    :return: String containing markdown list with sub-titles
    """
    instruction_list = ''
    for title, steps in instruction_dict.items():
            if title:
                instruction_list += "\n#### " + title + "\n"
            else:
                instruction_list += "\n"
            for step in steps:
                instruction_list += "* " + step + "\n"
            instruction_list += "\n"
