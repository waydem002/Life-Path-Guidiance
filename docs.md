# 1. Navigate to your project root

cd "C:\Users\user\Desktop\project folder\life_path_guidiance"

# 2. Navigate into your frontend folder (where package.json lives)

cd frontend

# 3. Start Vite / React

npm run dev

# Backend

cd backend

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
