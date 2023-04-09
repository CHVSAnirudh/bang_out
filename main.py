import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi import Query,Body
import logging
from body_detect import tracking
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pipeline").setLevel("INFO")

app = FastAPI(title="FaceSig Recon", version="1.0")    

@app.get("/start")
def start():
    logging.info("starting the game")
    track = tracking()
    track.detect()

@app.get("/get_body")
def get_body():
    track = tracking()
    res = track.get_body()
    return {res}

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=5000,
    )