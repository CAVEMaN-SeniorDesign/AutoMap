param (
    [Parameter(Mandatory=$true)][string]$inputDir
)

Start-Process powershell -ArgumentList "-NoExit -Command .\meshroom_image_to_map.ps1 -inputDir ${inputDir}"
Start-Process powershell -ArgumentList "-NoExit -Command .\meshroom_image_to_map_phash.ps1 -inputDir ${inputDir}"
Start-Process powershell -ArgumentList "-NoExit -Command .\meshroom_image_to_map_crp.ps1 -inputDir ${inputDir}"