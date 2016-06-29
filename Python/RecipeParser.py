# coding: utf-8
import bs4 as bs
import urllib
from urllib import request
import os.path
import ast
from Python.help_me import *


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
        Generates markdown styled string
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

    def make_markdown(self):
        """
        Creates and writes markdown styled recipe to a file
        :return: True or IOError is raised
        """
        new_file = ''
        directory = os.path.dirname(os.path.dirname(__file__)) + "/Recipes/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            self.title = ''.join(c for c in self.title if 0 < ord(c) < 127)
            if os.path.isfile(directory + self.title + ".md"):
                raise FileExistsError
            x = str(directory + self.title + ".md")
            new_file = open(x, "w")
            new_file.write(self.__str__())
        except FileExistsError:
            raise FileExistsError(directory + self.title + ".md")
        except IOError:
            raise IOError
        except:
            raise Exception
        finally:
            if new_file:
                try:
                    new_file.close()
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
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Quantity|" \
               "Ingredient|\n----------:|:-------\n{}\n###Instructions{}" \
               "".format(self.title, self.url, self.img_url,
                         get_ingredient_table(self.ingredients),
                         get_instruction_list(self.instructions))

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
        Sets all class variables in prep for make_markdown()
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
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Ingredient|" \
               "\n|:-------|\n{}\n###Instructions{}".format(
                self.title, self.url, self.img_url,
                get_ingredient_table_simple(self.ingredients),
                get_instruction_list(self.instructions))

    def set_recipe_title(self):
        """
        Gets recipe title from AllRecipes.com recipe
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
        Sets ingredient dict from AllRecipes.com {"ingredient": "quantity"}
        :return: None
        """
        # find all for multi-part recipes
        self.ingredients = [
            ingredient.text.strip() for ingredient in self.soup.findAll(
                "span", {"class": "recipe-ingred_txt added"})
                ]

    def set_instructions(self):
        """
        Sets instructions for AllRecipes.com recipe
        :return: None
        """
        self.instructions = [
            step.text for step in self.soup.findAll(
                "span", {"class": "recipe-directions__list--item"}
            ) if step.text
            ]

    def set_recipe_contents(self):
        """
        Sets all class variables in prep for make_markdown()
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
        """
        Generates FoodDotComParse object
        :param url: Input String of form Food.com/recipe/xxx
        :return: None
        """
        super(FoodDotComParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]\n({})\n###Ingredients\n" \
               "|Ingredient|\n|:-------|\n{}\n###Instructions{}".format(
                self.title, self.url, self.img_url,
                get_ingredient_table_simple(self.ingredients),
                get_instruction_list(self.instructions))

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
        Sets ingredient list from Food.com
        :return: None
        """
        self.ingredients = ast.literal_eval(self.soup.find("input", {
            "name": "ingredient"})['value'])

    def set_instructions(self):
        """
        Sets instructions for Food.com recipe
        :return:
        """
        self.instructions = [
            step.string for step in self.soup.find("ol")
            if step.string.replace('\n', '')
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
        else:
            raise Exception("Unset class variables")


class CookingNYTimesParse(RecipeParse):
    def __init__(self, url):
        """
        Generates CookingNYTimesParse object
        :param url: Input String of form cooking.nytimes.com/recipes/xxx
        :return: None
        """
        super(CookingNYTimesParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Ingredient|\n" \
               "|:-------\n{}\n###Instructions{}" \
               "".format(self.title, self.url, self.img_url,
                         get_ingredient_table_simple(self.ingredients),
                         get_instruction_list(self.instructions))

    def set_recipe_title(self):
        """
        Gets recipe title from cooking.nytimes.com recipe
        :return: None
        """
        self.title = self.soup.find(
            "h1", {"class": "recipe-title title name"}
        ).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find(
            "meta", itemprop="thumbnailUrl")['content']

    def set_ingredients(self):
        """
        Sets ingredient dict from cooking.nytimes.com
        {"ingredient": "quantity"}
        :return: None
        """
        self.ingredients = [
            x.text.replace("\n", ' ') for x in self.soup.findAll(
                "li", itemprop="recipeIngredient")
            ]

    def set_instructions(self):
        """
        Sets instructions for cooking.nytimes.com recipe
        :return:
        """
        self.instructions = [
            x.string.replace("\n", '') for x in self.soup.find(
                "ol", itemprop="recipeInstructions")
            if x.string.replace("\n", '')
            ]

    def set_recipe_contents(self):
        """
        Sets all class variables in prep for make_markdown()
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


class SweetAndSavoryParse(RecipeParse):
    def __init__(self, url):
        """
        Generates SweetAndSavoryParse object
        :param url: Input String of form sweetandsavorybyshinee.com/xxxx
        :return: None
        """
        super(SweetAndSavoryParse, self).__init__(url)

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n###Ingredients\n{}" \
               "\n###Instructions{}".format(self.title, self.url, self.img_url,
                                            get_ingredient_list_with_subtitles(
                                                self.ingredients),
                                            get_instruction_list(
                                                self.instructions))

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """
        self.title = self.soup.find("h2", itemprop="name").text

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = "http://" + self.soup.find("div", id="content").find(
            "img")['src'][2:]

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from SweetAndSavory recipe
        :return: None
        """
        self.recipe_yield = self.soup.find("span", itemprop="recipeYield").text

    def set_ingredients(self):
        """
        Sets ingredient dict from SweetAndSavory.com
        {"sub-recipe": "ingredient"}
        if no sub-recipe field is set to ' '
        :return: None
        """
        sub_title = ' '
        is_set = False

        for sub in self.soup.find("div", {"class": "ingredients"}):
            if sub.find("div") and not is_set:  # sub-title in div
                sub_title = sub.text.split(':')[0]
                self.ingredients[sub_title] = []
                is_set = True
            if sub.find("li") is None and not is_set:  # sub-title in list
                sub_title = sub.text
                self.ingredients[sub_title] = []
                is_set = True
                continue
            if not sub.find('p') and not is_set:  # no sub-title
                is_set = True
            if not is_set:  # sub title within inner div as p, along with li
                for count, y in enumerate(sub.findAll('p')):
                    self.ingredients[y.string] = [
                        strip_bad_ascii(li.text) for li in
                        sub.findAll("ul")[count]]
                    count += 1
                return
            if sub.find("li"):
                self.ingredients[sub_title] = [
                    strip_bad_ascii(x.text) for x in sub.findAll("li")]
            is_set = False

    def set_instructions(self):
        """
        Sets instructions for SweetAndSavory.com recipe
        :return: None
        """
        for directions in self.soup.findAll("div", {"class": "instructions"}):
            if directions.find("ol"):
                for step in directions.find("ol"):
                    self.instructions.append(strip_bad_ascii(step.text))
            else:
                for step in directions:
                    self.instructions.append(strip_bad_ascii(step.text))

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
        else:
            raise Exception("Unset class variables")


class FoodNetworkParse(RecipeParse):
    def __init__(self, url):
        """
        Generates FoodNetworkParse object
        :param url: Input String of form foodnetwork.com/recipes/xxxx
        :return: None
        """
        super(FoodNetworkParse, self).__init__(url)
        self.instructions = {}

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n###Ingredients\n{}" \
               "\n###Instructions{}".format(self.title, self.url, self.img_url,
                                            get_ingredient_list_with_subtitles(
                                                self.ingredients),
                                            get_ingredient_list_with_subtitles(
                                                self.instructions))

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """
        self.title = self.soup.find("h1", itemprop="name").text

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        # recipe video image within a href class="#lightbox-recipe-video"
        for element in self.soup.find("div", {"class": "col12 pic collapsed"}):
            if element.find("img") != -1:
                self.img_url = element.find("img")['src']

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from FoodNetwork recipe
        :return: None
        """
        self.recipe_yield = self.soup.find("div", {"class": "difficulty"}
                                           ).find("dd").text

    def set_ingredients(self):
        """
        Sets ingredient dict from FoodNetwork.com
        {"sub-recipe": "ingredient"}
        if no sub-recipe field is set to ' '
        :return: None
        """
        self.ingredients[''] = []
        temp = ''

        for instruction in self.soup.find("section", {
            "class": "ingredients-instructions recipe-instructions section"}
                                ).find("div", {"class", "bd"}
                                       ).find("div").findAll("li"):
            if "class" in instruction.attrs:
                temp = instruction.string
                self.ingredients[temp] = []
            else:
                self.ingredients[temp].append(instruction.string)

    def set_instructions(self):
        """
        Sets instructions dict for FoodNetwork.com recipe, form of:
         {'sub-title': ['step1'....'stepx'], '':['step1'....'stepx']
         where a key with the value '' has no subtitle, or is a single section
         recipe
        :return: None
        """
        self.instructions[''] = []
        temp = ''

        for element in self.soup.find("div", {"class": "col10 directions"}):
            if isinstance(element, bs.element.Tag) and \
                    element.attrs.get('class'):
                cur_class = ''.join(element.attrs.get('class'))
                # recipe directions stored in <ul> with below class
                if 'recipe-directions-list' == cur_class:
                    for step in element:
                        self.instructions[temp].append(step.text)
                # recipes divided by <span> with below class
                if 'subtitle' == cur_class:
                    temp = element.text
                    self.instructions[temp] = []

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
        else:
            raise Exception("Unset class variables")


class MarthaStewartParse(RecipeParse):
    def __init__(self, url):
        """
        Generates MarthaStewartParse object
        :param url: Input String of form marthastewart.com/xxxx/recipe-title
        :return: None
        """
        super(MarthaStewartParse, self).__init__(url)

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        if self.recipe_yield:
            return "#[{}]({})\n![alt text]({})\n######{}\n###Ingredients\n{}" \
                   "\n###Instructions{}".format(
                    self.title, self.url, self.img_url, self.recipe_yield,
                    get_ingredient_list_with_subtitles(self.ingredients),
                    get_instruction_list(self.instructions)
                    )
        else:
            return "#[{}]({})\n![alt text]({})\n###Ingredients\n{}" \
                   "\n###Instructions{}".format(
                    self.title, self.url, self.img_url,
                    get_ingredient_list_with_subtitles(self.ingredients),
                    get_instruction_list(self.instructions)
                    )

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """
        self.title = self.soup.find("h1", itemprop="name").text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find(
            "img", {"class": "feat-primary-img"})['data-original']

    def set_recipe_yield(self):
            """
            Gets recipe yield (serving size) from MarthaStewart recipe
            :return: None
            """
            # if yield is specified, set it, otherwise set to None
            self.recipe_yield = self.soup.find(
                "span", itemprop="recipeYield").text \
                if self.soup.find("span", itemprop="recipeYield") else None

    def set_ingredients(self):
        """
        Sets ingredient dict from MarthaStewart.com
        {"sub-recipe": "ingredient"}
        if no sub-recipe field is set to ''
        :return: None
        """
        for element in self.soup.find_all("section",
                                          {"class": "components-group"}):
            # assign section title iff exists, else assign to None
            title = element.find(
                "h3", {"class": "components-group-header"}).text.strip() \
                if element.find("h3", {"class": "components-group-header"}) \
                else ''
            ingredients = [
                y.text.strip() for y in element.find_all(
                    "li", itemprop="ingredients")
                ]
            self.ingredients[title] = ingredients

    def set_instructions(self):
        """
        Sets instruction list for MarthaStewart.com recipe, form of:
        ['step1'....'stepx']
        :return: None
        """
        self.instructions = [
            step.text.strip() for step in self.soup.find_all(
                "p", {"class": "directions-item-text"})
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
        else:
            raise Exception("Unset class variables")


class LiveEatLearnParse(RecipeParse):
    def __init__(self, url):
        """
        Generates LivEatLearnParse object
        :param url: Input String of form liveEatlearn.com/xxxx
        :return: None
        """
        super(LiveEatLearnParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
        """
        Generates markdown styled string
        :return: None
        """
        return "#[{}]({})\n![alt text]({})\n\n|Ingredients|\n" \
               "| ------------- |\n{}\n###Instructions{}".format(
                    self.title, self.url, self.img_url,
                    get_ingredient_table_simple(self.ingredients),
                    get_instruction_list(self.instructions)
                    )

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """
        self.title = self.soup.find("h1", itemprop="headline").text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find("img", {"class": "aligncenter"})['src']

    def set_recipe_yield(self):
            """
            Gets recipe yield (serving size) from LiveEatLearn recipe
            :return: None
            """
            self.recipe_yield = self.soup.find(
                "div", {"class": "ERSServes"}).text

    def set_ingredients(self):
        """
        Sets ingredient list from LiveEatLearn.com
        :return: None
        """
        self.ingredients = [
            strip_bad_ascii(element.text.strip()) for element in
            self.soup.find_all("li", {"class": "ingredient"})
            ]

    def set_instructions(self):
        """
        Sets instruction list for LiveEatLearn.com recipe, form of:
        ['step1'....'stepx']
        :return: None
        """
        self.instructions = [
            strip_bad_ascii(element.text.strip()) for element in
            self.soup.find_all("li", {"class": "instruction"})
            ]

    def set_recipe_contents(self):
        if self.soup:
            self.set_recipe_title()
            self.set_recipe_img()
            self.set_recipe_yield()
            self.set_ingredients()
            self.set_instructions()
        else:
            raise Exception("Unset class variables")
