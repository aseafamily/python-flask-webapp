@echo off
setlocal enabledelayedexpansion

rem Set the URL from which to download the file
set "download_url=https://bluehousemall.azurewebsites.net/serve/db"

rem Set the local file name to replace
set "local_file=test.db"
set "backup_folder=.\backup_db"

rem Check if the backup folder exists, if not, create it
if not exist "%backup_folder%" (
    mkdir "%backup_folder%"
)

rem Get the current date in yyyyMMdd format using PowerShell
for /f %%a in ('powershell -Command "Get-Date -Format 'yyyyMMdd'"') do set "current_date=%%a"

rem Set backup file with yyyyMMdd format
set "backup_file=%backup_folder%\%local_file%.!current_date!"

rem Check if there are more than five backup copies, delete the oldest one
powershell -Command "Get-ChildItem '%backup_folder%\%local_file%.*' | Sort-Object CreationTime -Descending | Select-Object -Skip 5 | Remove-Item -Force"

rem Backup the existing file
if exist "%local_file%" (
    move /Y "%local_file%" "%backup_file%" >nul
)

rem Download the file from the URL
echo Downloading file from %download_url%
powershell -Command "(New-Object Net.WebClient).DownloadFile('%download_url%', '%local_file%.tmp')"

rem Check if the download was successful
if %ERRORLEVEL% neq 0 (
    echo Failed to download the file.
    goto :EOF
)

rem Replace the local file with the downloaded file
echo Moving downloaded file to replace %local_file%
move /Y "%local_file%.tmp" "%local_file%"

rem Check if the move was successful
if %ERRORLEVEL% neq 0 (
    echo Failed to replace %local_file%.
    goto :EOF
)

echo File replaced successfully.

:end
