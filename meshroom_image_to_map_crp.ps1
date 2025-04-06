param (
    [Parameter(Mandatory=$true)][string]$inputDir
)

Write-Host $inputDir
$outputDir = "$inputDir/crh_output_imgs"

.\.venv\Scripts\Activate.ps1
python .\remove_dupes.py $inputDir crh
meshroom_batch -i $inputDir -p photogrammetry -o "$outputDir/maps" --cache "$outputDir/cache"
blender -b -P blender_glb_output.py -- "$outputDir/maps" "$outputDir/maps"
deactivate
