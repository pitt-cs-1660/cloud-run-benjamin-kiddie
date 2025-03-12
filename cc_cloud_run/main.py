from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")

@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    votes = votes_collection.stream()
    vote_data = []
    for v in votes:
        vote_data.append(v.to_dict())

    tabs_count = len(list(filter(lambda v: v["team"] == "TABS", vote_data)))
    spaces_count = len(vote_data) - tabs_count
    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": spaces_count,
        "recent_votes": vote_data[-5:]
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    votes_collection.add({
        "team": team,
        "time_cast": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

    return {
        "detail": "Vote successfully cast.",
    }
    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
