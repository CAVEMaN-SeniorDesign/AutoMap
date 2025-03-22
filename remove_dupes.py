from PIL import Image
import os
import imagehash
import cv2
import numpy as np


hashes_idx = dict()
hashes_to_imgs = dict()

def laplace_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

directory = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test1"

# Rename all files to be normally indexed
for index, filename in enumerate(os.listdir(directory)):
    os.rename(os.path.join(directory, filename), os.path.join(directory, "image_" + f"{index:04d}" + ".png"))


uniq_hash_idx = 0

files = os.listdir(directory)
files = sorted(files)

for index, filename in enumerate(files):
    path = os.path.join(directory, filename)
    file_hash = imagehash.phash(Image.open(path), hash_size=8)
    file_multi_hash = imagehash.crop_resistant_hash(Image.open(path), hash_func=imagehash.phash)
    # print(file_multi_hash)
    img = cv2.imread(path)
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        isRGB = True
    except:
        gray = img

    blurmetric = int(laplace_variance(gray))

    # Remove fundamentally blurry images
    if(blurmetric < 150):
        os.remove(path)
        1 == 1
    else:
        if str(file_multi_hash) not in hashes_idx.keys():
            # new_name_uniq = path[:-4] + "_bin_" + str(uniq_hash_idx) + path[-4:]
            new_name_uniq = f"{path[:-4]}_bin_{str(uniq_hash_idx)}_{blurmetric}{path[-4:]}"
            os.rename(path, new_name_uniq)
            hashes_to_imgs[str(file_multi_hash)] = [(new_name_uniq,blurmetric)]
            hashes_idx[str(file_multi_hash)] = uniq_hash_idx
            uniq_hash_idx += 1

        else:
            # new_name_dupe = path[:-4] + "_bin_" + str(hashes_idx[str(file_hash)]) + "_dupe_" + str(len(list(hashes_to_imgs[str(file_hash)]))-1) + path[-4:]
            new_name_dupe = f"{path[:-4]}_bin_{str(hashes_idx[str(file_multi_hash)])}_dupe_{str(len(list(hashes_to_imgs[str(file_multi_hash)]))-1)}_{blurmetric}{path[-4:]}"
            os.rename(path, new_name_dupe)
            list_imgs = list(hashes_to_imgs[str(file_multi_hash)])
            list_imgs.append((new_name_dupe,blurmetric))
            hashes_to_imgs[str(file_multi_hash)] = list_imgs

# Remove all but the best image from all dupes
for bin in hashes_to_imgs.values():
    binList = list(bin)
    maxVal = 0
    maxValImg = ""
    for img in binList:
        if img[1] > maxVal:
            maxVal = img[1]
            maxValImg = img[0]
        else:
            os.remove(img[0])
            binList.remove(img)
    for img in binList:
        if img != (maxValImg, maxVal):
            os.remove(img[0])
            binList.remove(img)


    