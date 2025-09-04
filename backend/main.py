import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import TransmissionRequest, TransmissionAnalysisOutput
from calculations import calculate_wkg_for_all_gears


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API Transmission Vélo 🚴"}

@app.post("/calculate-transmission", response_model=TransmissionAnalysisOutput)
def calculate_transmission(data: TransmissionRequest):
    return calculate_wkg_for_all_gears(data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 