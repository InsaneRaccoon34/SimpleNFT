from email import header
from email.mime import image
from importlib.metadata import metadata
import os, json, io
from random import randint, random
from PIL import Image, ImageShow
import requests

PINATA_BASE_URL = 'https://api.pinata.cloud/'
PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJiM2JkY2FiNS0yZWI0LTQ2NWEtYjRiMy1jNWQ4ZmZkMGQyNmYiLCJlbWFpbCI6Im1vcm96dWs0NEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX0seyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiYzc2Njg4ZmVhZDM3YzAyYjgzNmQiLCJzY29wZWRLZXlTZWNyZXQiOiIzNzI0YzZkM2EyNDQ3ZjYyZDgxNTcxZTNkNmExYWVlY2ZjODIyNWNkMzFjNTc5ZWQ4MzgzZmQ5MDU0YjBhYjMxIiwiaWF0IjoxNjU5MDg0MDM1fQ.pNwj2vBxYoGTjbxsDuF134090PNWjSb-xaxyAQIcNkI"
HEADERS = { 'Authorization': 'Bearer ' + PINATA_JWT}
GATEWAY_URL = 'https://gateway.pinata.cloud/ipfs/'

ASSETS_FOLDER = 'assets\\'
NFT_FOLDER = "NFT_Collection"


def testPinataConnection():
    url = "https://api.pinata.cloud/data/testAuthentication"
    payload={} 
    response = requests.request("GET", url, headers=HEADERS, data=payload)
    print(response.text)

metadata = {
    "name": "You NFT token name",
    "description": "Something Cool here",
    "image": "",
    "attributes": []
}

def generate_meta_data(tokenId, responseText):
    metadata["name"] = str(tokenId)
    metadata["description"] = 'An Eternal Ethereum Digital Homie!'
    metadata["image"] = GATEWAY_URL + responseText['IpfsHash']
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
        print('seed ' + seed + ' was already taken')
        generateSeed()
    else:
        takenSeeds.append(seed)
        return seed

def generatePicture():
    layers = os.listdir(ASSETS_FOLDER)
    seed = generateSeed(layers)

    new_im = Image.new('RGB', (250, 250), (255,255,255))

    for layer in layers:
        randomNumber = seed[layers.index(layer)]
        img = Image.open(ASSETS_FOLDER + layer + "\\" + layer + str(randomNumber) + '.png')
        new_im.paste(img, (0,0), img.convert('RGBA'))

    print('final seed', seed)
    return new_im

def generateCharacter():
    for imageIteration in range(42):
        pic = generatePicture()
        picturePath = NFT_FOLDER + "\\" + str(imageIteration) + '.png'
        pic.save(picturePath)

        with open(picturePath, "rb") as image:
            f = image.read()
            byteImage = bytearray(f)

        endpoint = 'pinning/pinFileToIPFS'
        payload={
            'pinataOptions': '{"cidVersion": 1}',
            'pinataMetadata': ''
            }
        payload['pinataMetadata'] = json.dumps({
            'name': str(imageIteration) + '.png',
            "keyvalues": {"company": "Pinata"}
        })

        response = requests.request(
            "POST",
            url = PINATA_BASE_URL + endpoint,
            data = payload,
            files = { "file": byteImage },
            headers = HEADERS
        )

        meta = json.dumps(generate_meta_data(imageIteration, json.loads(response.text)))
        print(meta)
    


generateCharacter()