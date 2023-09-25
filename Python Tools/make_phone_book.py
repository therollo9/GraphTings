import os
import json
from bs4 import BeautifulSoup
import requests
# import re


def main():
    path = "data/"
    phone_book_location = "phone_book.json"
    # print(phone_book.read())

    brand_string_list = []
    model_list = []

    # Finding the brand names and putting them to a list
    URL = "https://www.rtings.com/headphones/index"
    page = requests.get(URL)
    # print(page.status_code) # making sure that it's working. If it's code 200, we good

    soup = BeautifulSoup(page.content, "html.parser")
    brand_list = soup.find_all("div", "silo_reviews_page-brand")

    # these renamings are because RTings has different names from other stuff.
    for brand in brand_list:
        if brand.string == "1More":
            brand_string_list.append("1MORE")
        elif brand.string == "7HZ":
            brand_string_list.append("7Hz")
        elif brand.string == "Astro":
            brand_string_list.append("ASTRO")
        elif brand.string == "BRAINWAVZ":
            brand_string_list.append("Brainwavz")
        elif brand.string == "COUGAR":
            brand_string_list.append("Cougar")
        elif brand.string == "HiFiMan":
            brand_string_list.append("HIFIMAN")
        elif brand.string == "MEE audio":
            brand_string_list.append("MEE Audio")
        elif brand.string == "MOONDROP":
            brand_string_list.append("Moondrop")
        elif brand.string == "Harman/Kardon":
            brand_string_list.append("Harman Kardon")
        elif brand.string == "TIN Audio":
            brand_string_list.append("Tin HiFi")
        else:
            brand_string_list.append(brand.string)

    print(f"Number of brands: {len(brand_string_list)}")

    brand_string_list.sort()

    # Output list of brands
    # for brand in brand_string_list:
    #     print(brand)

    # Getting all measurements and making a model list.
    file_list = os.listdir(path)
    file_list.sort()
    for file in file_list:
        file_name, file_extension = os.path.splitext(file)
        if file_extension == "":
            continue
        model_list.append(file[:-6])
    print(f"Number of models: {len(model_list)}")

    # Then for the brand dictionaries, the phones parameter is an array of model dictionaries
    # Lastly, the phone book is an array of brand dictionaries.

    brand_dictionary = {
        "name": brand,
        "phones": []  # an array of dictionaries
    }

    model_dictionary = {
        "index": 0,
        "name": "",
        "file": ""
    }

    phone_book_list = []
    model_dictionary_list = []

    # Brands are placed in a list, so their indexes will be used as reference to the models.
    for brand in brand_string_list:
        temp_brand_dictionary = {
            "name": brand,
            "phones": []  # an array of dictionaries
        }
        phone_book_list.append(temp_brand_dictionary)

    # I will make a list of model dictionaries, with using the file parameter to modify the index parameter
    for model in model_list:
        brand_index = 0
        model_name = ""
        for index, brand in enumerate(brand_string_list):
            if brand in model:
                brand_index = index
                model_name = model.replace(brand, "")
                break

        temp_model_dictionary = {
            "index": brand_index,
            "name": model_name.strip(" "),
            "file": model.strip(" ")
        }

        model_dictionary_list.append(temp_model_dictionary)

    # prints the whole dictionary list of models
    # for model in model_dictionary_list:
    #     print(model)

    # Checks if the model name is the same as the file name
    # for model in model_dictionary_list:
    #     if model.get("name") == model.get("file"):
    #         print(f"{model}")
    # for model in model_dictionary_list:
    #     if model.get("index") == 0:
    #         print(f"{model}")

    for index, brand in enumerate(phone_book_list):
        is_adding = False
        temp_phones_list = []
        for model in model_dictionary_list:
            if index == model.get("index"):
                is_adding = True
                temp_phones_list.append(model)
            else:
                if is_adding:
                    break

        # print(brand.get("name") + f": {len(temp_phones_list)}")
        temp_phones = {"phones": temp_phones_list}
        brand.update(temp_phones)

    # Printing the whole Phone Book
    # for brand in phone_book_list:
    #     print(brand)

    # # Writing the JSON File
    trim_phone_book = []
    for brand in phone_book_list:
        if len(brand.get("phones")) == 0:
            continue
        trim_phone_book.append(brand)

    phone_book = open(phone_book_location, "w")
    json.dump(trim_phone_book, phone_book)


if __name__ == '__main__':
    main()
