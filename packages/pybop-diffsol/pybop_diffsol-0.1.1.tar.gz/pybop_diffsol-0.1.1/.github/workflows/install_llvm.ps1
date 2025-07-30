param (
    [string]$DestinationFolder = "$PSScriptRoot\llvm"
)

# Define the URL and archive path
$url = "https://github.com/vovkos/llvm-package-windows/releases/download/llvm-17.0.6/llvm-17.0.6-windows-x86-msvc17-libcmt.7z"
$archivePath = Join-Path $DestinationFolder "llvm.7z"

# Create destination folder if it doesn't exist
if (-not (Test-Path $DestinationFolder)) {
    New-Item -ItemType Directory -Path $DestinationFolder | Out-Null
}

# Download the file
Write-Host "Downloading LLVM package..."
Invoke-WebRequest -Uri $url -OutFile $archivePath

# Check if 7z.exe is available
if (-not (Get-Command "7z" -ErrorAction SilentlyContinue)) {
    Write-Error "7z.exe not found in PATH. Please install 7-Zip."
    exit 1
}

# Extract the archive in-place
Write-Host "Extracting archive..."
Push-Location -Path $DestinationFolder
& 7z x "llvm.7z" -y
Pop-Location

# Print contents of the destination directory (now should work!)
Write-Host "`nTop-level contents of: $DestinationFolder"
Get-ChildItem -Path $DestinationFolder