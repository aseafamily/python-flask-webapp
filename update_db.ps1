# Define the file name constant
$file_name = "test"
$local_file = "$file_name.db"
$backup_folder = ".\backup_db"

# Set the URL from which to download the file
$download_url = "https://bluehousemall.azurewebsites.net/serve/db"
$downloaded_file = "$local_file.tmp"

# Check if the backup folder exists, if not, create it
if (-not (Test-Path -Path $backup_folder)) {
    New-Item -ItemType Directory -Path $backup_folder | Out-Null
}

# Download the file from the URL
Invoke-WebRequest -Uri $download_url -OutFile $downloaded_file

# Check if the download was successful
if (-not (Test-Path -Path $downloaded_file)) {
    Write-Host "Failed to download the file."
    exit 1
}

# Find the latest backup in backup_folder by file timestamp
$latest_backup = Get-ChildItem -Path $backup_folder -Filter "$file_name*.db" | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1

# If a latest backup is found, compare it with the downloaded file
if ($latest_backup) {
    Write-Host "Comparing current file $downloaded_file with latest backup $($latest_backup.FullName)"
    $comparison = Compare-Object -ReferenceObject (Get-Content $downloaded_file) -DifferenceObject (Get-Content $latest_backup.FullName)
    if (-not $comparison) {
        Write-Host "No changes detected. No backup created."
    }
    else {
        Write-Host "Changes detected. Creating a new backup."
        # Create a new backup file in backup_folder with timestamp
        $timestamp = Get-Date -Format "yyyyMMddHHmmss"
        Move-Item -Path $local_file -Destination "$backup_folder\$file_name.$timestamp.db" -Force
    }
}
else {
    Write-Host "No existing backup found. Creating a new backup."
    # If there's no existing backup, create a backup with timestamp
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    Move-Item -Path $local_file -Destination "$backup_folder\$file_name.$timestamp.db" -Force
}

# Replace the local file with the downloaded file
Move-Item -Path $downloaded_file -Destination $local_file -Force

Write-Host "File replaced successfully."
