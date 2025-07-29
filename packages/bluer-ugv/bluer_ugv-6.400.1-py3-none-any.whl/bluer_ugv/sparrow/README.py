assets2 = "https://github.com/kamangir/assets2/blob/main/bluer-sparrow"

dict_of_images = {
    f"{assets2}/20250712_114819.jpg?raw=true": "",
    f"{assets2}/20250713_172325.jpg?raw=true": "",
    f"{assets2}/20250713_172413.jpg?raw=true": "",
    f"{assets2}/20250713_172442_1.gif?raw=true": "",
}

items = [
    "[![image]({})]({})".format(image, url if url else image)
    for image, url in dict_of_images.items()
]
