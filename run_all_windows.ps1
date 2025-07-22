# run_all_windows.ps1
# IMPORTANT: Run this script in PowerShell with execution policy set appropriately

# Setup: Stop on errors
$ErrorActionPreference = "Stop"

# Vars
$remote_host = "158.160.135.246"
$private_key = "portforward_key"  # Adjust path if needed
$port_file   = Join-Path $env:TEMP "random_port.txt"

# 1. Generate or load random port
if (Test-Path $port_file) {
    $random_port = (Get-Content $port_file -Raw).Trim()
} else {
    $random_port = Get-Random -Minimum 1024 -Maximum 65536
    Set-Content -Path $port_file -Value $random_port
}
Write-Host "Random port generated: $random_port"

# 2. Install Poetry
Write-Host "Trying to install Poetry..."
(Invoke-WebRequest -Uri "https://install.python-poetry.org" -UseBasicParsing).Content | python -
Write-Host "Poetry installed successfully."

# 3. Add Poetry bin directory to PATH
$poetryBin = Join-Path $env:APPDATA "Python\Scripts"
if ($env:PATH -notmatch [regex]::Escape($poetryBin)) {
    $env:PATH += ";$poetryBin"
    Write-Host "Added Poetry bin directory to PATH: $poetryBin"
} else {
    Write-Host "Poetry bin directory already in PATH: $poetryBin"
}

# 4. Install project dependencies
Write-Host "Installing Project's dependencies..."
poetry install
Write-Host "Dependencies installed successfully."

# 5. Fix access rules on the SSH key
$icaclsOutput = icacls $private_key /inheritance:r /grant:r "$($env:USERNAME):F"
Write-Host "icacls output:" $icaclsOutput

# 6. Start SSH tunnel (reverse port forwarding)
$sshArgs = "-i `"$private_key`" -N -R 0.0.0.0:${random_port}:localhost:6872 forwarduser@${remote_host} -o StrictHostKeyChecking=no"
Write-Host "Starting SSH tunnel with: ssh $sshArgs"
Start-Process ssh -ArgumentList $sshArgs -NoNewWindow

# Time for Tunnel to start
Start-Sleep -Seconds 2

# 7. Launch FastAPI uvicorn
Write-Host "Launching the FastAPI app on port 6872..."
Start-Process -FilePath "poetry" -ArgumentList "run", "fastapi", "dev", "app/api/main.py", "--host", "::", "--port", "6872"

# Time for FastAPI to start
Start-Sleep -Seconds 5

# 8. Check local port 6872
Write-Host "Checking local port 6872..."
$tcLocal = Test-NetConnection -ComputerName localhost -Port 6872
if ($tcLocal.TcpTestSucceeded) {
    Write-Host "Local port 6872 is UP (FastAPI should be running)."
} else {
    Write-Host "Local port 6872 is DOWN."
}

# Time for checking
Start-Sleep -Seconds 1

# 9. Launch Streamlit on local port 8502
Write-Host "Launching the Streamlit app on port 8502..."
$env:PYTHONPATH = (Get-Location).Path
Start-Process -FilePath "poetry" -ArgumentList "run", "streamlit", "run", "app/web/streamlit_app.py", "--server.port=8502", "--server.address=127.0.0.1"

# 10. Log address for registration
Write-Host "Your address for registration is:"
Write-Host "http://${remote_host}:${random_port}"
