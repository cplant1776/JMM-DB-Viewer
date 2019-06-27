# Convert main_window.ui to main_window.py
$screens = Get-ChildItem -Name -Filter *.ui

try {
    foreach ($screen in $screens)
    {
        Write-Output $screen
        # Get file name
        $screen -match "(?<filename>.*)\."
        $out_file = "..\" + $matches['filename'] + ".py"
        # Convert .ui -> .py
        ..\..\..\venv\Scripts\python.exe ..\..\..\venv\Scripts\pyuic5.exe -o $out_file $screen
    }

    Write-Host "Finished with no errors!"
    # Read-Host -Prompt "Finished with no errors! Press Enter to exit."
}

catch {

    Write-Error $_.Exception.ToString()
    Write-Host "The above error occurred."
    # Read-Host -Prompt "The above error occurred. Press Enter to exit."

}