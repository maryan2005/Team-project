$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Invoke-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE : $Executable $Arguments"
    }
}

function Find-Python3 {
    $Launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($Launcher) {
        & $Launcher.Source -3.12 -c "import sys; raise SystemExit(sys.version_info[:2] != (3, 12))" *> $null
        if ($LASTEXITCODE -eq 0) {
            return [pscustomobject]@{ Executable = $Launcher.Source; Prefix = @("-3.12") }
        }
    }

    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($PythonCommand) {
        & $PythonCommand.Source -c "import sys; raise SystemExit(sys.version_info[:2] != (3, 12))" *> $null
        if ($LASTEXITCODE -eq 0) {
            return [pscustomobject]@{ Executable = $PythonCommand.Source; Prefix = @() }
        }
    }

    return $null
}

$PythonInfo = Find-Python3
if (-not $PythonInfo) {
    $Winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $Winget) {
        throw "Python 3 was not found and winget is unavailable. Install Python 3.12 and rerun this script."
    }

    Invoke-Checked $Winget.Source @("install", "--id", "Python.Python.3.12", "--exact", "--scope", "user", "--silent", "--accept-package-agreements", "--accept-source-agreements")
    $MachinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$MachinePath;$UserPath"
    $PythonInfo = Find-Python3
    if (-not $PythonInfo) {
        throw "Python installed, but this session could not find it. Restart PowerShell and rerun this script."
    }
}

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    & $VenvPython -c "import sys; raise SystemExit(sys.version_info[:2] != (3, 12))" *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "The existing .venv is not Python 3.12. Rename or remove .venv, then rerun this script."
    }
} else {
    Invoke-Checked $PythonInfo.Executable ($PythonInfo.Prefix + @("-m", "venv", ".venv"))
}

Invoke-Checked $VenvPython @("-m", "pip", "install", "--upgrade", "pip")
Invoke-Checked $VenvPython @("-m", "pip", "install", "-r", "Code/requirements.txt", "pytest")

$CodePath = Join-Path $Root "Code"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$CodePath$([IO.Path]::PathSeparator)$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $CodePath
}
$env:SDL_VIDEODRIVER = "dummy"
$env:SDL_AUDIODRIVER = "dummy"

Invoke-Checked $VenvPython @("-m", "pytest", (Join-Path $Root "Tests"))
Write-Host "Setup and tests completed. Start the game with: .venv\Scripts\python.exe Code\main.py"