import os
import sys
# import argparse # for better cmd line args
# import glob # for arbitrary file finding w/ any extension
import bpy

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
    
if input_path[-1] == "/":
    input_path = input_path[:-1]

if output_path[-1] == "/":
    output_path = output_path[:-1]

input_obj = input_path + "/texturedMesh.obj"
input_mtl = input_path + "/texturedMesh.mtl"
input_exr = input_path + "/texture_1001.exr"
output_glb = output_path + "/texturedMesh.glb"


#bpy.ops.wm.obj_import(filepath="C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs/texturedMesh.obj", directory="C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs")
bpy.ops.wm.obj_import(filepath=input_obj, directory=input_path)
bpy.ops.paint.texture_paint_toggle()
bpy.ops.export_scene.gltf(filepath=output_glb)

# blender -b -P blender_glb_output.py -- C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs