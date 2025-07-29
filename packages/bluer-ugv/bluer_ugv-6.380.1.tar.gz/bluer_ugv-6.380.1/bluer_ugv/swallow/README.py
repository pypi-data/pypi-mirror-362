assets2 = "https://github.com/kamangir/assets2/blob/main/bluer-swallow"
assets = "https://github.com/kamangir/assets/raw/main"

dict_of_images = {
    f"{assets}/bluer-ugv/bluer-light.png?raw=true": "",
    "../../../diagrams/bluer_swallow/3d-design.png": "../../../diagrams/bluer_swallow/3d-design.stl",
    f"{assets2}/20250605_180136.jpg?raw=true": "",
    "../../../diagrams/bluer_swallow/analog.png": "../../../diagrams/bluer_swallow/analog.svg",
    f"{assets2}/20250608_144453.jpg?raw=true": "",
    "../../../diagrams/bluer_swallow/digital.png": "../../../diagrams/bluer_swallow/digital.svg",
    f"{assets2}/20250609_164433.jpg?raw=true": "",
    f"{assets2}/20250611_100917.jpg?raw=true": "",
    f"{assets2}/20250614_102301.jpg?raw=true": "",
    f"{assets2}/20250614_114954.jpg?raw=true": "",
    f"{assets2}/20250615_192339.jpg?raw=true": "",
    f"{assets2}/20250616_134654.jpg?raw=true": "",
    f"{assets2}/20250616_145049.jpg?raw=true": "",
    f"{assets2}/20250618_102816~2_1.gif?raw=true": "",
    f"{assets2}/20250618_122604.jpg?raw=true": "",
    "../../../diagrams/bluer_swallow/cover.png": "../../../diagrams/bluer_swallow/cover.stl",
    f"{assets2}/20250629_123616.jpg?raw=true": "",
    f"{assets2}/20250630_214923.jpg?raw=true": "",
    f"{assets2}/20250701_2206342_1.gif?raw=true": "",
    f"{assets2}/20250703_153834.jpg?raw=true": "",
    "../../../diagrams/bluer_swallow/steering-over-current.png": "../../../diagrams/bluer_swallow/steering-over-current.svg",
    f"{assets2}/20250707_122000.jpg?raw=true": "",
    f"{assets2}/20250707_182818.jpg?raw=true": "",
    f"{assets2}/2025-07-08-13-09-38-so54ao.png?raw=true": "",
    f"{assets}/2025-07-09-10-26-30-itpbmu/grid.png?raw=true": "./digital/dataset/collection/validation.md",
    f"{assets}/2025-07-09-10-26-30-itpbmu/grid-timeline.png?raw=true": "./digital/dataset/review.md",
    f"{assets2}/lab.png?raw=true": "",
    f"{assets2}/20250709_111955.jpg?raw=true": "",
    f"{assets2}/2025-07-09-11-20-27-4qf255-000-2.png?raw=true": "",
    f"{assets}/swallow-dataset-2025-07-11-10-53-04-n3oybs/grid.png?raw=true": "./digital/dataset/combination/validation.md",
    f"{assets}/swallow-model-2025-07-11-15-04-03-2glcch/loss.png?raw=true": "./digital/model/validation.md",
    f"{assets}/swallow-model-2025-07-11-15-04-03-2glcch/evaluation.png?raw=true": "./digital/model/validation.md",
    f"{assets}/swallow-model-2025-07-11-15-04-03-2glcch/confusion_matrix.png?raw=true": "./digital/model/validation.md",
    f"{assets2}/2025-07-09-11-18-07-azy27w.png?raw=true": "https://github.com/kamangir/bluer-algo/blob/main/bluer_algo/docs/image_classifier/dataset/sequence.md",
    f"{assets}/sequence-2025-07-12-21-58-04-0wmt6d/grid.png?raw=true": "https://github.com/kamangir/bluer-algo/blob/main/bluer_algo/docs/image_classifier/dataset/sequence.md",
}

items = [
    "[![image]({})]({})".format(image, url if url else image)
    for image, url in dict_of_images.items()
]
