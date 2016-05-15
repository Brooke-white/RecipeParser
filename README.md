# RecipeParser


# [My Recipes](https://github.com/Brooke-white/RecipeParser/tree/master/Recipes)


## About
A python script that parses recipe websites to create markup files with essential recipe information, like ingredients, instructions, and a photo of course! I made this so I can keep all of my favorite recipes organized in a psuedo recipe book. 


## Dependencies
BeautifulSoup4 (pip install bs4)


## Supported Recipe Websites
+ [Food52](https://www.Food52.com/)

+ [AllRecipes](https://www.allrecipes.com/)

+ [Food.com](http://www.food.com/)


## Usage
file: A text file containing recipe urls from the supported websites

    file = "/Users/you/anywhere/recipes.txt"
    main(file)


If generating the markup files is a success you will see a success message, otherwise you'll see which markup files weren't generated and the corresponding error messages.


#### recipes.txt
    http://food52.com/recipes/31276-oatmeal-cream-pies#comments
    http://www.food.com/recipe/tsr-version-of-benihana-japanese-onion-soup-by-todd-wilbur-391952
    http://allrecipes.com/recipe/41460/sweet-corn-tomalito/


