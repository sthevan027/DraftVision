#!/bin/bash
# DraftVision - Setup script (Linux/macOS)
set -e

echo -e "\033[36mDraftVision - Setup\033[0m"

# Backend
echo -e "\n\033[33m[1/3] Backend (Python)\033[0m"
cd app/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || { cp .env.example .env; echo "  .env criado - edite com suas chaves"; }
cd ../..

# Frontend
echo -e "\n\033[33m[2/3] Frontend (Next.js)\033[0m"
cd app/web
pnpm install
[ -f .env.local ] || cp .env.example .env.local
cd ../..

echo -e "\n\033[32m[3/3] Concluído\033[0m"
echo "Próximos passos:"
echo "  1. Edite app/api/.env com RIOT_API_KEY e DATABASE_URL"
echo "  2. Inicie Redis: redis-server"
echo "  3. Backend: cd app/api && uvicorn main:app --reload"
echo "  4. Frontend: cd app/web && pnpm dev"
