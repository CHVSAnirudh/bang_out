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


@app.get("/punch")
def play_punch_sound(sevearity: str = Query(..., max_length=50, min_length=3)):
    try:
        logging.info("recieved a task for converting recon result to excel")
        
        logging.info("recon to excel successfully completed")
        return JSONResponse(status_code=200)
    except Exception as e:
        logging.error("error occured in converting result to excel.",exc_info=True)
        return JSONResponse(status_code=500, content={"content":{"result":"failed to convert result to excel."}})
    

@app.get("/start")
def start():
    logging.info("starting the game")
    track = tracking()
    track.detect()

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=5000,
    )