@echo off
setlocal

rem Set the URL from which to download the file
set "download_url=https://bluehousemall.azurewebsites.net/serve/db"

rem Set the local file name to replace
set "local_file=test.db"

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
