# Porneste backend si frontend in paralel
Write-Host "Pornesc backend FastAPI pe http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Pornesc frontend React pe http://localhost:5173 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "App disponibila la: http://localhost:5173" -ForegroundColor Green
Write-Host "API docs la:        http://localhost:8000/docs" -ForegroundColor Green
