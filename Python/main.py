import bs4 as bs
import urllib
from urllib import request
import os.path
import ast


class RecipeParse(object):
    def __init__(self, url):
        """
        Generates generic RecipeParse object
        :param url: Input url
        :return: None
        """
        self.url = url
        self.soup = self.lets_get_soup()
        self.title = ''
        self.img_url = ''
        self.recipe_yield = ''
        self.ingredients = {}
        self.instructions = []

    def __str__(self):
        """
        Generates markup styled string
        :return: None
        """

    def lets_get_soup(self):
        """
        Gets BeautifulSoup object from url
        :return: False or BeautifulSoup object
        """
        try:
            # pretend to be Firefox
            req = urllib.request.Request(self.url,
                                         headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as url_file:
                url_byte = url_file.read()
        except urllib.request.HTTPError as e:  # HTTP status code
            print(e.__str__())
            return False
        except urllib.request.URLError as e:  # General Error
            print(e.__str__())
            return False
        except OSError as e:  # Vague Error
            print(e.__str__())
            return False
        except Exception as e:  # Anything
            print(e.__str__())
            return False

        try:
            url_string = url_byte.decode(encoding='latin1').encode(
                encoding='utf-8')
        except UnicodeDecodeError as e:
            print(e.__str__())
            return False
        except Exception as e:
            print(e.__str__())
            return False
        return bs.BeautifulSoup(url_string, "html.parser")

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from Food52 recipe
        :return: None
        """

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """

    def set_recipe_contents(self):
        """
        Sets all recipe elements
        :return:
        """

    def make_markup(self):
        """
        Creates and writes markup styled recipe to a file
        :return: True or IOError is raised
        """
        file = ''
        directory = os.path.dirname(os.path.dirname(__file__)) + "/Recipes/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            self.title = ''.join(c for c in self.title if 0 < ord(c) < 127)
            x = str(directory + self.title + ".md")
            file = open(x, "w")
            file.write(self.__str__())
        except IOError:
            raise IOError
        except:
            raise Exception
        finally:
            if file:
                try:
                    file.close()
                except IOError:
                    raise IOError
                except Exception:
                    raise Exception
        return True


class Food52Parse(RecipeParse):
    def __init__(self, url):
        """
        Generates Food52Parse object
        :param url: Input String of form 52food.com/recipes/xxx
        :return: None
        """
        super(Food52Parse, self).__init__(url)

    def __str__(self):
        """
        Generates markup styled string
        :return: None
        """
        ingredients_table = ''
        instruction_list = ''

        for ingredient, amount in self.ingredients.items():
            ingredients_table += "|" + ''.join(amount) + "|" + \
                                 ingredient + "|\n"

        for step in self.instructions:
            instruction_list += "\n\n* " + step

        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Quantity|" \
               "Ingredient|\n----------:|:-------\n{}\n###Instructions{}" \
               "".format(self.title, self.url, self.img_url, ingredients_table,
                         instruction_list)

    def set_recipe_title(self):
        """
        Gets recipe title from Food52.com recipe
        :return: None
        """
        self.title = self.soup.find(
            "h1", {"class": "article-header-title"}
        ).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = "https:" + self.soup.find(
            "figure", {"class": "photo-frame first"}).find("img")['src']

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from Food52 recipe
        :return: None
        """
        self.recipe_yield = self.soup.find("p", itemprop="recipeYield")

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """
        # find all for multi-part recipes
        for div in self.soup.findAll("ul", {"class": "recipe-list"}):
            # find all ingredient <li> elements
            for element in div.findAll("li", itemprop="ingredients"):
                # find all ingredient names
                for ingredient in element.findAll(
                        "span", {"class": "recipe-list-item-name"}):
                    # if ingredient is already present in dict
                    if ingredient.text.strip() in self.ingredients.keys():
                        self.ingredients[
                            ingredient.text.strip()
                        ].append(
                            element.find(
                                "span", {"class": "recipe-list-quantity"}
                            ).text.strip()
                        )
                    # if ingredient is not present in dict or None
                    if ingredient.text is not None and ingredient.text.strip()\
                            not in self.ingredients.keys():
                        self.ingredients[ingredient.text.strip()] = []
                        self.ingredients[
                            ingredient.text.strip()
                        ].append(
                            element.find(
                                "span", {"class": "recipe-list-quantity"}
                            ).text.strip()
                        )

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """
        self.instructions = [
            step.text.strip() for step in self.soup.findAll(
                "li", itemprop="recipeInstructions")
            ]

    def set_recipe_contents(self):
        """
        Sets all class variables in prep for make_markup()
        :return: None
        """
        if self.soup:
            self.set_recipe_title()
            self.set_recipe_img()
            self.set_recipe_yield()
            self.set_ingredients()
            self.set_instructions()
        else:
            raise Exception("Unset class variables")


class AllRecipesParse(RecipeParse):
    def __init__(self, url):
        """
        Generates AllRecipesParse object
        :param url: Input String of form allrecipes.com/recipe/xxx
        :return: None
        """
        super(AllRecipesParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
        """
        Generates markup styled string
        :return: None
        """
        ingredients_table = ''
        instruction_list = ''

        for ingredient in self.ingredients:
            ingredients_table += "|" + ''.join(ingredient) + "|\n"

        for step in self.instructions:
            instruction_list += "\n\n* " + step

        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Ingredient|" \
               "\n|:-------|\n{}\n###Instructions{}".format(
                self.title, self.url, self.img_url, ingredients_table,
                instruction_list)

    def set_recipe_title(self):
        """
        Gets recipe title from Food52.com recipe
        :return: None
        """
        self.title = self.soup.find(
            "h1", {"class": "recipe-summary__h1"}).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find(
            "img", {"class": "rec-photo"})['src']

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """
        # find all for multi-part recipes
        self.ingredients = [
            ingredient.text.strip() for ingredient in self.soup.findAll(
                "span", {"class": "recipe-ingred_txt added"})
                ]

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return: None
        """
        self.instructions = [
            step.text for step in self.soup.findAll(
                "span", {"class": "recipe-directions__list--item"}
            ) if step.text
            ]

    def set_recipe_contents(self):
        """
        Sets all class variables in prep for make_markup()
        :return: None
        """
        if self.soup:
            self.set_recipe_title()
            self.set_recipe_img()
            self.set_ingredients()
            self.set_instructions()
        else:
            raise Exception("Unset class variables")


class FoodDotComParse(RecipeParse):
    def __init__(self, url):
        super(FoodDotComParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
        """
        Generates markup styled string
        :return: None
        """

        ingredients_table = ''
        instruction_list = ''

        for ingredient in self.ingredients:
            ingredients_table += "|" + ''.join(ingredient) + "|\n"

        for step in self.instructions:
            instruction_list += "\n\n* " + step

        return "#[{}]({})\n![alt text]\n({})\n###Ingredients\n" \
               "|Ingredient|\n|:-------|\n{}\n###Instructions{}".format(
                self.title, self.url, self.img_url,
                ingredients_table, instruction_list
        )

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """
        self.title = self.soup.find(
            "h1", {"class": "fd-recipe-title"}).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find(
            "img", {"class": "slide-photo"})['data-src']

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """
        self.ingredients = ast.literal_eval(self.soup.find("input", {
            "name": "ingredient"})['value'])

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """
        self.instructions = [
            str(step.string) for step in self.soup.find("ol")
            if str(step.string.replace('\n', ''))
            ]

    def set_recipe_contents(self):
        """
        Sets all recipe elements
        :return:
        """
        if self.soup:
            self.set_recipe_title()
            self.set_recipe_img()
            self.set_recipe_yield()
            self.set_ingredients()
            self.set_instructions()

    def make_markup(self):
        """
        Creates and writes markup styled recipe to a file
        :return: True or IOError is raised
        """
        file = ''
        directory = os.path.dirname(os.path.dirname(__file__)) + "/Recipes/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            self.title = ''.join(c for c in self.title if 0 < ord(c) < 127)
            x = str(directory + self.title + ".md")
            file = open(x, "w")
            file.write(self.__str__())
        except IOError:
            raise IOError
        except:
            raise Exception
        finally:
            if file:
                try:
                    file.close()
                except IOError:
                    raise IOError
                except Exception:
                    raise Exception
        return True


def read_input_file(file):
    content = []
    try:
        with open(file, 'r') as f:
            content = f.read().splitlines()
    except IOError:
        raise IOError
    return content


def main(file):
    try:
        content = read_input_file(file=file)
    except IOError as e:
        print("UNABLE TO OPEN FILE: ", e)

    count = 0

    for url in content:
        if "food52" in url:
            thisrecipe = Food52Parse(url)
            thisrecipe.set_recipe_contents()

        if "allrecipes" in url:
            thisrecipe = AllRecipesParse(url)
            thisrecipe.set_recipe_contents()

        if "food.com" in url:
            thisrecipe = FoodDotComParse(url)
            thisrecipe.set_recipe_contents()
        try:
            thisrecipe.make_markup()
            count += 1
        except IOError as e:
            print(thisrecipe.title, "\tFILE NOT CREATED:\t", e.__str__())
        except Exception as e:
            print(thisrecipe.title, "\tFILE NOT CREATED:\t", e.__str__())

    if count == len(content):
        return True
    else:
        return False

file = "/Users/brooke/Desktop/recipes.txt"

if main(file):
    print("Success")
else:
    print("Not all markup files were generated")
