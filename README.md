#Clone the repo -

git clone https://github.com/janmesh1814/Loop-AI.git
cd Loop-AI

#Backend setup

cd backend
python -m venv venv
venv\Scripts\activate (for windows) OR source venv/bin/activate (macOS/Linux)

pip install fastapi uvicorn httpx

uvicorn main:app --reload


#Frontend setup
cd frontend
npm install

npm start

 
