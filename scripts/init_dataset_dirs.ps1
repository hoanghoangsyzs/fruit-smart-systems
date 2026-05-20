$root = Join-Path $PSScriptRoot "..\dataset"
$tasks = @("disease", "ripeness")
$splits = @("train", "val", "test")
$diseaseClasses = @("healthy", "leaf_spot", "anthracnose")
$ripenessClasses = @("unripe", "half_ripe", "ripe")

foreach ($task in $tasks) {
    $classes = if ($task -eq "disease") { $diseaseClasses } else { $ripenessClasses }
    foreach ($split in $splits) {
        foreach ($cls in $classes) {
            $path = Join-Path $root "$task\$split\$cls"
            New-Item -ItemType Directory -Force -Path $path | Out-Null
        }
    }
}
Write-Host "Dataset folders created under $root"
