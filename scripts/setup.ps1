# DraftVision - Setup script (Windows PowerShell)
# Executa setup inicial do projeto

Write-Host "DraftVision - Setup" -ForegroundColor Cyan

# Backend
Write-Host "`n[1/3] Backend (Python)" -ForegroundColor Yellow
Set-Location app/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host "  .env criado - edite com suas chaves" }
Set-Location ..\..

# Frontend
Write-Host "`n[2/3] Frontend (Next.js)" -ForegroundColor Yellow
Set-Location app/web
pnpm install
if (-not (Test-Path .env.local)) { Copy-Item .env.example .env.local }
Set-Location ..\..

Write-Host "`n[3/3] Concluido" -ForegroundColor Green
Write-Host "Proximos passos:"
Write-Host "  1. Edite app/api/.env com RIOT_API_KEY e DATABASE_URL"
Write-Host "  2. Inicie Redis: redis-server"
Write-Host "  3. Backend: cd app/api && uvicorn main:app --reload"
Write-Host "  4. Frontend: cd app/web && pnpm dev"
