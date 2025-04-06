from PIL import Image
import sys
import os
import imagehash
import cv2
import shutil


min_args = 2
max_args = 3 # program, input, hash type

hash_options = ["phash", "crh"]
hash_opt = "phash"
phash_size = 10

hash_list = list()
hashes_idx = dict()
hashes_to_imgs = dict()

def laplace_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def check_and_copy(filepath, output_path):
    if os.path.isfile(filepath):
        return shutil.copy2(filepath, output_path)
    else:
        return False


def get_hash(path, hash_opt):
    if hash_opt == "phash":
        file_hash = imagehash.phash(Image.open(path), hash_size=phash_size)
    elif hash_opt == "crh":
        file_hash = imagehash.crop_resistant_hash(Image.open(path), hash_func=imagehash.phash)

    return file_hash

def check_hash(hash, hash_dict, hash_list, hash_opt):
    if hash_opt == "phash":
        if str(hash) in hash_dict:
            return True, None
        else:
            return False, None
    elif hash_opt == "crh":
        for hash_preexist in hash_list:
            if hash.hash_diff(hash_preexist, None, .2)[0] >= (.8 * len(hash.segment_hashes)):
                return True, hash_preexist
        return False, None
    
    return False, None

def rename_inorder(index, filename):
    extension = os.path.splitext(filename)[1]
    os.rename(os.path.join(output_dir, filename), os.path.join(output_dir, "image_" + f"{index:04d}" + f"{extension}"))


n = len(sys.argv)
print(n)

if n < min_args:
    print("Too few arguments")
    exit()
elif n > max_args:
    print("Too many arguments")
    exit()

input_path = sys.argv[1]
hash_opt = sys.argv[2]

input_path = input_path.replace("\\", "/")
    
if input_path[-1] == "/":
    input_path = input_path[:-1]

output_dir = input_path + f"/{hash_opt}_output_imgs"

skip_copy = False

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
elif len(os.listdir(output_dir)) > 2:
    skip_copy = True


if not skip_copy:
    input_path_initial = os.listdir(input_path)
    input_path_len_initial = len(input_path_initial)
    in_dir_iter = list(map(os.path.join, [input_path]*len(input_path_initial), input_path_initial))
    out_dir_iter = [output_dir]*len(os.listdir(input_path))
    success = list(map(check_and_copy, in_dir_iter, out_dir_iter))

# Rename all files to be normally indexed
files_in_dir = os.listdir(output_dir)
nums = range(len(files_in_dir))
files_in_dir = list(map(os.path.join, [output_dir]*len(files_in_dir), files_in_dir))
success = list(map(rename_inorder, nums, files_in_dir))

uniq_hash_idx = 0

files = os.listdir(output_dir)
files = sorted(files)

for index, filename in enumerate(files):
    extension = os.path.splitext(filename)[1]
    path = os.path.join(output_dir, filename)
    file_hash = get_hash(path, hash_opt)
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
    else:
        boolVal, cropMatch = check_hash(file_hash, hashes_idx, hash_list, hash_opt)
        if not boolVal:
            new_name_uniq = f"{path[:-len(extension)]}_bin_{str(uniq_hash_idx)}_{blurmetric}{extension}"
            os.rename(path, new_name_uniq)
            hashes_to_imgs[str(file_hash)] = [(new_name_uniq,blurmetric)]
            hashes_idx[str(file_hash)] = uniq_hash_idx
            hash_list.append(file_hash)
            uniq_hash_idx += 1

        else:
            if cropMatch is not None:
                new_name_dupe = f"{path[:-len(extension)]}_bin_{str(hashes_idx[str(cropMatch)])}_dupe_{str(len(list(hashes_to_imgs[str(cropMatch)]))-1)}_{blurmetric}{extension}"
                os.rename(path, new_name_dupe)
                list_imgs = list(hashes_to_imgs[str(cropMatch)])
                list_imgs.append((new_name_dupe,blurmetric))
                hashes_to_imgs[str(cropMatch)] = list_imgs
            else:
                new_name_dupe = f"{path[:-len(extension)]}_bin_{str(hashes_idx[str(file_hash)])}_dupe_{str(len(list(hashes_to_imgs[str(file_hash)]))-1)}_{blurmetric}{extension}"
                os.rename(path, new_name_dupe)
                list_imgs = list(hashes_to_imgs[str(file_hash)])
                list_imgs.append((new_name_dupe,blurmetric))
                hashes_to_imgs[str(file_hash)] = list_imgs
            

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


    