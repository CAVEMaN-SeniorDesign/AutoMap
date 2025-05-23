echo $#

if [[ $# < 2 ]]; then
    echo "Not enough command line args: Should have 2"
elif [[ $# > 2 ]]; then
    echo "Too many command line args: Should have 2"
fi

# echo $0
echo $1
echo $2
# echo $3

if [[ -f "$1" ]]; then
    echo "input needs to be a file directory"
elif [[ -d "$1" ]]; then
    echo ""
else
    echo "invalid input file path"
fi

if [[ -f "$2" ]]; then
    echo "output needs to be a file directory"
elif [[ -d "$2" ]]; then
    echo ""
else
    echo "invalid output file path"
fi

# TODO: Create and Source the Python 3.11 Venv

# python remove_dupes.py $1 $2
# ./meshroom_image_to_map.sh "$2/img_mod" "$2/maps"
# blender -b -P blender_glb_output.py -- "$2/maps" "$2/maps"

# ./meshroom_image_to_map "$1" "$2/maps"
# blender -b -P blender_glb_output.py -- "$2/maps" "$2/maps"
