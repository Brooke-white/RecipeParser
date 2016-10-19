# coding: utf-8
from Python.help_me import *
from Python.RecipeParser import *


def main(cur_file):
    count = -1
    try:
        content = read_input_file(my_file=cur_file)
    except IOError as e:
        print("UNABLE TO OPEN FILE: ", e)
        return False

    content[:] = ["http://" + content if "http" not in content else content
                  for content in content]

    for count, url in enumerate(content):

        if "food52" in url:
            thisrecipe = Food52Parse(url)

        if "allrecipes" in url:
            thisrecipe = AllRecipesParse(url)

        if "food.com" in url:
            thisrecipe = FoodDotComParse(url)

        if "nytimes" in url:
            thisrecipe = CookingNYTimesParse(url)

        if "sweetandsavory" in url:
            thisrecipe = SweetAndSavoryParse(url)

        if "foodnetwork" in url:
            thisrecipe = FoodNetworkParse(url)

        if "marthastewart" in url:
            thisrecipe = MarthaStewartParse(url)

        if "liveeatlearn" in url:
            thisrecipe = LiveEatLearnParse(url)

        if thisrecipe:
            thisrecipe.set_recipe_contents()
            try:
                thisrecipe.make_markdown()
                count += 1
            except FileExistsError as e:
                print(thisrecipe.title, "\t FILE EXISTS:\t", e.__str__())
            except IOError as e:
                print(thisrecipe.title, "\tFILE NOT CREATED:\t", e.__str__())
            except Exception as e:
                pass
                print(thisrecipe.title, "\tFILE NOT CREATED:\t", e.__str__())
        else:
            print("UNSUPPORTED URL:\t", url)

    if count == len(content):
        return True
    else:
        return False

if __name__ == "__main__":
    file = "/Users/brooke/Desktop/recipes.txt"

    if main(file):
        print("Success")
    else:
        print("Not all markdown files were generated")
