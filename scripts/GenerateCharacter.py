from importlib.metadata import metadata
import os, json
from random import randint, random
from PIL import Image, ImageShow

ASSETS_FOLDER = 'assets\\'
NFT_FOLDER = "NFT_Collection"

metadata = {
    "name": "You NFT token name",
    "description": "Something Cool here",
    "image": "",
    "attributes": []
}

def generate_meta_data(token_id):
    metadata["name"] = str(token_id)
    metadata["description"] = 'An Eternal Ethereum Digital Homie!'
    metadata["image"] = ''
    # Will add image and attributes after creation of image/meta
    metadata["attributes"] = []
    return metadata

takenSeeds = []

def generateSeed(layers):
    seed =[]
    for layer in layers:
        lenght = len(os.listdir(ASSETS_FOLDER + layer))
        randomNumber = randint(0, lenght - 1)
        seed.append(randomNumber)

    if (seed in takenSeeds):
        print('seed ' + seed + 'was already taken #########################')
        generateSeed()
    else:
        takenSeeds.append(seed)
        return seed

def generateCharacter():
    layers = os.listdir(ASSETS_FOLDER)
    seed = generateSeed(layers)

    new_im = Image.new('RGB', (250, 250), (255,255,255))

    for layer in layers:
        randomNumber = seed[layers.index(layer)]
        img = Image.open(ASSETS_FOLDER + layer + "\\" + layer + str(randomNumber) + '.png')
        new_im.paste(img, (0,0), img.convert('RGBA'))

    print('final seed', seed)
    return new_im

for x in range(42):
    pic = generateCharacter()

    meta = json.dumps(generate_meta_data(x))
    print(meta)
    
    pic.save(NFT_FOLDER + "\\" + str(x) + '.png')