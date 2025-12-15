# Creates Windows Desktop shortcuts for KCK Swap Shop
# - Backend+Frontend launcher: start.bat
# - Sets a custom icon if available

param(
    [string]$WorkspacePath = "$PSScriptRoot\.."
)

$ErrorActionPreference = 'Stop'

function New-DesktopShortcut {
    param(
        [string]$Name,
        [string]$TargetPath,
        [string]$IconLocation
    )

    $shell = New-Object -ComObject WScript.Shell
    $desktop = [Environment]::GetFolderPath('Desktop')
    $shortcutPath = Join-Path $desktop ("$Name.lnk")

    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $TargetPath
    $shortcut.WorkingDirectory = Split-Path $TargetPath
    $shortcut.IconLocation = $IconLocation
    $shortcut.Description = 'Launch KCK Swap Shop (Backend + Frontend)'
    $shortcut.Save()

    Write-Host "Created shortcut: $shortcutPath" -ForegroundColor Green
}

# Resolve paths
$startBat = Join-Path $WorkspacePath 'start.bat'
if (!(Test-Path $startBat)) {
    throw "start.bat not found at $startBat"
}

# Prefer a custom icon from the workspace if available
$customIconBase = Join-Path $WorkspacePath 'images\shortcut_logo'
$icon = "$env:SystemRoot\System32\SHELL32.dll,85"

# Try common icon file variants
$possibleIcons = @(
    "$customIconBase.ico",
    "$customIconBase.icns",
    "$customIconBase.exe",
    "$customIconBase.dll"
)

foreach ($p in $possibleIcons) {
    if (Test-Path $p) {
        # For .ico files, use full path without index
        if ($p -like "*.ico") {
            $icon = "$p,0"
        } else {
            $icon = $p
        }
        Write-Host "Using custom icon: $icon" -ForegroundColor Cyan
        break
    }
}

if ($icon -like "*SHELL32.dll*") {
    Write-Host "Using default Windows icon (no custom icon found at $customIconBase.*)" -ForegroundColor Yellow
}

New-DesktopShortcut -Name 'KCK Swap Shop' -TargetPath $startBat -IconLocation $icon

Write-Host "`nDone! Double-click the desktop shortcut to launch." -ForegroundColor Green
