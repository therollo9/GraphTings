# What are these Python Tools?
These 2 Python files made my life easier considering the fact that RTings has measured over 400 models from over 100 brands.
# Explanation Time
## The Renamer (renamer.py)
Like what the name suggests, it renames the CSVs into TXT files, with appropriate suffixes depending on whether or not it's an IEM database or a headphone database. IEMs end with L, while headphones end with L1.
## Phone Book Generator (make_phone_book.py)
This Python file, while not perfect, is a lifesaver, and it took me 2 days of learning Python (because it's not my main language) and figure out the flow. Before I explain how the generator works, I will lay out some questions I asked myself throughout the weekend:
- How to generate a JSON file using Python?
- What is the structure of the Phone Book JSON file?
- Knowing the above, how to represent datatypes in Python?
- How to figure out the brand names from the model names?
- Is this perfect? (No, lmao. But I'll explain.)

These questions are what I wondered when creating this database because if I have to make the Phone Book JSON manually, that means I will copy and paste at least 100 times and modify each pasted model and object. It can already be tedious if you are just starting out and you measured 30 IEMs or headphones. Imagine doing that for at least 300 models.

The first question can be answered easily. We already have a module for that. 
For the second question, let's analyze one of the brands inside the Phone Book:
```json
{
        "name": "Moondrop",
        "phones": [
            {
                "index": 66,
                "name": "Aria 2021",
                "file": "Moondrop Aria 2021"
            },
            {
                "index": 66,
                "name": "Blessing 3",
                "file": "Moondrop Blessing 3"
            },
            {
                "index": 66,
                "name": "KATO",
                "file": "Moondrop KATO"
            }
        ]
    }
```
The index parameter will be explained later

In this example, each brand has a name and a list of phones (models); each model has its name and the file that represents it. It can be a singular file or a list of files. Knowing this, we can dissect the format to have this pattern:
```py
brand_dictionary = {
        "name": brand,
        "phones": []  # a list of models
    }

    model_dictionary = {
        "index": 0,
        "name": "",
        "file": ""
    }
```
And this is how it's represented in Python as a dictionary. So technically speaking, the Phone Book is a list of brand dictionaries, and in each brand dictionary, it contains a list of model dictionaries.

Now that we have the appropriate representation of the phone book, let's start taking note of the brands
.
.
.
but how?
### How to figure out the brand names from the model names?
My initial plan is to take the first word of the file names as brands, but as I quickly realized, it's more complicated. It makes sense for JBL, AKG, and Samsung. And then there's Altec Lansing, Turtle Beach, and Bang & Olufsen, which is more than one word. So, I need to take another approach. After having empty thoughts and a cup of coffee, I realized that RTings did the work for me via the [Review Index](https://www.rtings.com/headphones/index). There are brand names labeled, so what I did is scrape the labels and place them in a list. Easy. We have a list of brands, but I have to make some slight modifications:
```py
for brand in brand_list:
        if brand.string == "1More":
            brand_string_list.append("1MORE")
        elif brand.string == "7HZ":
            brand_string_list.append("7Hz")
        elif brand.string == "Astro":
            brand_string_list.append("ASTRO")
        ...
```
For specific brands, I have to manually rename them because it's different compared to the AutoEQ CSV files. It's a bit inconvenient but it helps me in the long term.

Now, we already have the brand names, and we have the file names. Now, we can separate the brand names from the file names; this will leave us with the model names. The only problem is for model names that also have their brand names (Nura Nuraphones). I've yet to find a solution for this, but after the process, the model name becomes "phones" instead of "Nuraphones". Not to mention that some file names differ entirely from those in RTings, so this is not a perfect solution. But with this, it gets into the ballpark compared to the alternative of pain and suffering. Now, we talk about the last step.
### How to put the models to their respective brands?
It sounds pretty inefficient to always get the contents of the "phones" parameter, then add/append a model, then update the phones parameter, so I created the list of model dictionaries first, then update the phones parameter. Then, I take advantage of representing the brands in numbers. This is where the index parameter comes into play. Instead of finding the brand in the file (again), I compare the order number of the brand to the index inside the model dictionary. 
If the model has an index of 66, it has to be part of the 66th brand. All models with an index of 66 will be placed on the same list. The process of getting the index is already done when making the model dictionaries.

The last step is to write the JSON file after removing brands that don't have any models inside the list. Fortunately, it directly converts the directories to JSON. It's literally one function. 
