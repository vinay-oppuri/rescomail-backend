from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the backend"}


@app.get("/dashboard")
def dashboard():
    return {"message": "Welcome to the dashboard"}


@app.get("/upload-resume")
def upload_resume():
    return {"message": "Upload resume"}


@app.get("/enhance-resume")
def enhance_resume():
    return {"message": "Enhance resume"}


@app.get("/generate-cover-letter")
def generate_cover_letter():
    return {"message": "Generate cover letter"}