import sys
import os
import random
import json
from datetime import datetime
from PIL import Image 
from itertools import combinations, product

# Config
resourcesFolder = "resources"
projectName = "project_name"
baseURL = "https://www.google.com"
finalImageExtension = ".png"

# Start layers combination
layers = []

for dirName, dirNames, fileNames in os.walk(resourcesFolder):
    files = [os.path.join(dirName, fileName) for fileName in fileNames if not fileName.startswith(".")]
    if files:
     layers.append(files)

layers.sort()
combinations = list(product(*layers))
random.shuffle(combinations)

if not combinations:
    print("It seems that you don't have enough layer combinations")
    sys.exit(1)

# Start the layer mix
for combination in combinations:
    print(combination)

    # First layers composition
    firstLayer = Image.open(f'{combination[0]}').convert('RGBA')
    secondLayer = Image.open(f'{combination[1]}').convert('RGBA')
    composition = Image.alpha_composite(firstLayer, secondLayer)

    # Do more layer compositions
    for layer in combination[2:]:
        nLayer = Image.open(f'{layer}').convert('RGBA')
        composition = Image.alpha_composite(composition, nLayer)

    # Save image
    finalImage = composition.convert('RGB')
    fileName = f"{combinations.index(combination)}_{projectName}"
    finalImage.save(f"generated/{fileName}{finalImageExtension}")

    # Save metadata for this new NFT
    nftMetadata = {}
    nftMetadata['image'] = f"{baseURL}/{fileName}{finalImageExtension}"
    nftMetadata['tokenId'] = f"{combinations.index(combination)}"
    nftMetadata['name'] = f"{projectName} #{combinations.index(combination)}"
    nftMetadata['attributes'] = []

    with open(f"./generated/{fileName}.json", "w") as outfile:
        json.dump(nftMetadata, outfile, indent=4)