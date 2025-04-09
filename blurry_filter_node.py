import sys
import shutil
import os
import cv2


def check_and_copy(filepath, output_path):
    if os.path.isfile(filepath):
        return shutil.copy2(filepath, output_path)
    else:
        return False

def laplace_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def thresh_and_remove(path, output_path, threshold):
    if not os.path.isfile(path):
        return

    img = cv2.imread(path)
    
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        gray = img

    blurmetric = laplace_variance(gray)

    if(blurmetric >= threshold):
        shutil.copy2(path, output_path)


min_args = 2
max_args = 3 # program, input, threshold

n = len(sys.argv)
print(n)

if n < min_args:
    print("Too few arguments")
    exit()
elif n > max_args:
    print("Too many arguments")
    exit()

input_path = sys.argv[1]

if n == 3:
    try:
        threshold = int(sys.argv[2])
    except:
        print("threshold must be an integer")
        exit()
else:
    threshold = 150

input_path = input_path.replace("\\", "/")
    
if input_path[-1] == "/":
    input_path = input_path[:-1]

output_dir = input_path + f"/blur_thresh_{threshold}_output_imgs"

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


input_path_initial = os.listdir(input_path)
input_path_len_initial = len(input_path_initial)
in_dir_iter = list(map(os.path.join, [input_path]*input_path_len_initial, input_path_initial))


list(map(thresh_and_remove, in_dir_iter, [output_dir]*input_path_len_initial, [threshold]*input_path_len_initial))