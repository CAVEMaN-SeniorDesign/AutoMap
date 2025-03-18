from simlabpy import *

filepath_backslash = "C:\\Users\\parek\\Desktop\\SeniorDesign\\RTABMAP\\437desksetupdata\\imageOuts\\rgb\\outputs"
filepath_fwdslash = "C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/outputs"


input_glb_b = filepath_backslash + "\\texturedMesh.glb"
output_vrpackage_b = filepath_backslash + "\\test.vrpackage"
output_sim_file_b = filepath_backslash + "\\test.zim"

input_glb_f = filepath_fwdslash + "/texturedMesh.glb"
output_vrpackage_f = filepath_fwdslash + "/test.vrpackage"
output_sim_file_f = filepath_fwdslash + "/test.zim"

title = "Filler"

scene = Scene()
node = scene.importFile(filepath_fwdslash)
exportSuccess = scene.exportVrPackage(output_vrpackage, title, title, title, "3d", "", True)
scene.saveFile(output_sim_file)

print(exportSuccess)
