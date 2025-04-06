import sys
import shutil
import os


def check_and_copy(filepath, output_path):
    if os.path.isfile(filepath):
        return shutil.copy2(filepath, output_path)
    else:
        return False

min_args = 2
max_args = 2 # program, input, hash type

n = len(sys.argv)
print(n)

if n < min_args:
    print("Too few arguments")
    exit()
elif n > max_args:
    print("Too many arguments")
    exit()

input_path = sys.argv[1]

input_path = input_path.replace("\\", "/")
    
if input_path[-1] == "/":
    input_path = input_path[:-1]

output_dir = input_path + "/raw_output_imgs"

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