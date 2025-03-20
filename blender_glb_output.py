import os
import sys
# import argparse # for better cmd line args
# import glob # for arbitrary file finding w/ any extension
import bpy


list_of_usable_textures = [".exr", ".jpg", ".jpeg", ".tga", ".dds", ".psd"]
texture_found = False

n = len(sys.argv)
print(n)

if n < 2:
    print("Too few arguments")
    exit()
elif n > 10:
    print("Too many arguments")
    exit()


input_path = sys.argv[5]
output_path = sys.argv[6]

print(input_path)
print(output_path)

if(not os.path.isdir(input_path) or not os.path.isdir(output_path)):
    exit()

input_path = input_path.replace("\\", "/")
output_path = output_path.replace("\\", "/")
    
if input_path[-1] == "/":
    input_path = input_path[:-1]

if output_path[-1] == "/":
    output_path = output_path[:-1]

for filename in os.listdir(input_path):
    name, ext = os.path.splitext(filename)
    if ext:
        if ext.lower() in list_of_usable_textures:
            print("Texture file found")
            texture_found = True
            texture = filename

if not texture_found:
    print("Texture file not found")
    exit()

input_obj = input_path + "/texturedMesh.obj"
input_mtl = input_path + "/texturedMesh.mtl"
input_texture_file = input_path + "/" + texture
output_glb = output_path + "/texturedMesh.glb"


print(input_texture_file)

#bpy.ops.wm.obj_import(filepath="C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs/texturedMesh.obj", directory="C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False, confirm=True)
bpy.ops.wm.obj_import(filepath=input_obj, directory=input_path)
bpy.ops.paint.texture_paint_toggle()
bpy.ops.export_scene.gltf(filepath=output_glb)

# blender -b -P blender_glb_output.py -- C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs