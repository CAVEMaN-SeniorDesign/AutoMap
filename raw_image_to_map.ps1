param (
    [Parameter(Mandatory=$true)][string]$inputDir,
    [Parameter(Mandatory=$true)][string]$outputDir,
    [string]$inputSrc = "all_images",
    [string]$outputSrc = "map_glb"
)

Write-Host $inputDir
Write-Host $outputDir
Write-Host $inputSrc
Write-Host $outputSrc

$images_all = "all_images"
$images_filtered = "images_filtered"
$maps_obj = "maps_obj"
$maps_glb = "maps_glb"
$maps_view_blender = "maps_view_blender"
$maps_view_customapp = "maps_view_customapp"

