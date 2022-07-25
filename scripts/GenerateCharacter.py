from distutils.log import debug
from email.mime import image
from hashlib import new
import os
from random import randint, random
from PIL import Image, ImageShow

ASSETS_FOLDER = 'assets\\'
NFT_FOLDER = "NFT_Collection"

def generateCharacter():

    layers = os.listdir(ASSETS_FOLDER)
    seed = []

    new_im = Image.new('RGB', (250, 250), (255,255,255))

    for layer in layers:
        lenght = len(os.listdir(ASSETS_FOLDER + layer))
        randomNumber = randint(0, lenght - 1)
        seed.append(randomNumber)

    for layer in layers:
        randomNumber = seed[layers.index(layer)]
        img = Image.open(ASSETS_FOLDER + layer + "\\" + layer + str(randomNumber) + '.png')
        new_im.paste(img, (0,0), img.convert('RGBA'))

    print('final seed', seed)
    return new_im


generateCharacter()

for x in range(42):
    pic = generateCharacter()
    pic.save(NFT_FOLDER + "\\" + str(x) + '.png')