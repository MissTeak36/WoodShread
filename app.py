"""WoodShread scanner: receives a scan and returns the music as JSON.

The recognition engine is not wired in yet. For now /scan returns a sample
result so the player can be built against the real format (see schema.md).
"""
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

FLAG_THRESHOLD = float(os.environ.get("FLAG_THRESHOLD", "0.8"))
ALLOWED_TYPES = {"image/png", "image/jpeg", "application/pdf"}
MAX_BYTES = 20 * 1024 * 1024

app = FastAPI(title="WoodShread scanner")

origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def flag(item: dict) -> dict:
    item["flagged"] = item["confidence"] < FLAG_THRESHOLD
    return item


def finish(result: dict) -> dict:
    """Mark flagged items and work out bar confidence and the flagged count."""
    count = 0
    for bar in result["bars"]:
        parts = [flag(i) for i in bar["items"]] + [flag(m) for m in bar.get("marks", [])]
        bar["confidence"] = min((p["confidence"] for p in parts), default=1.0)
        bar["flagged"] = bar["confidence"] < FLAG_THRESHOLD
        count += sum(p["flagged"] for p in parts)
    result["flag_threshold"] = FLAG_THRESHOLD
    result["flagged_count"] = count
    return result


def note(pitch, duration, conf, articulation=None):
    n = {"type": "note", "pitch": pitch, "duration": duration, "confidence": conf}
    if articulation:
        n["articulation"] = articulation
    return n


def rest(duration, conf=0.98):
    return {"type": "rest", "duration": duration, "confidence": conf}


def slashes(conf=0.96):
    return [{"type": "slash", "duration": "quarter", "confidence": conf} for _ in range(4)]


def sample_result() -> dict:
    """Bars 25 to 35 of a medium fast swing chart, with two deliberately weak reads."""
    return finish({
        "title": "Medium fast swing chart",
        "clef": "bass",
        "key": "F",
        "time": "cut",
        "bars": [
            {"number": 25, "items": [rest("whole")]},
            {"number": 26, "items": [rest("whole")]},
            {"number": 27,
             "marks": [{"type": "dynamic", "value": "mf", "confidence": 0.95}],
             "items": [note("F3", "quarter", 0.93, "staccato"), rest("eighth"),
                       note(None, "eighth", 0.55, "staccato"), rest("quarter"),
                       note("F3", "quarter", 0.9, "staccato")]},
            {"number": 28,
             "items": [rest("eighth"), note("C3", "eighth", 0.91, "staccato"), rest("quarter"),
                       note("D3", "eighth", 0.88), note("E3", "eighth", 0.87),
                       note("F3", "quarter", 0.9, "staccato")]},
            {"number": 29,
             "items": [note("F3", "quarter", 0.92, "staccato"), rest("eighth"),
                       note("A2", "eighth", 0.9, "staccato"), rest("quarter"),
                       note("Bb2", "quarter", 0.86, "staccato")]},
            {"number": 30,
             "items": [rest("eighth"), note("B2", "eighth", 0.62, "staccato"), rest("quarter"),
                       note("C3", "eighth", 0.9), note("D3", "eighth", 0.9),
                       note("E3", "eighth", 0.89), note("F3", "eighth", 0.9)]},
            {"number": 31,
             "items": [note("G3", "quarter", 0.92), rest("eighth"),
                       note("D3", "eighth", 0.9), rest("quarter"), note("G2", "quarter", 0.91)]},
            {"number": 32,
             "items": [rest("eighth"), note("C3", "eighth", 0.92), rest("quarter"),
                       note("D3", "eighth", 0.9), note("E3", "eighth", 0.9),
                       note("F3", "quarter", 0.92)]},
            {"number": 33,
             "marks": [{"type": "hairpin", "value": "crescendo", "confidence": 0.84}],
             "items": [note("F3", "quarter", 0.93), rest("eighth"),
                       note("C3", "eighth", 0.9), rest("quarter"), note("A2", "quarter", 0.9)]},
            {"number": 34,
             "items": [note("Bb2", "quarter", 0.9), note("B2", "quarter", 0.89),
                       note("C3", "quarter", 0.9), note("C#3", "quarter", 0.88)]},
            {"number": 35,
             "items": [{"type": "chord", "value": "Dmi7", "confidence": 0.94}] + slashes()},
        ],
    })


@app.get("/")
def health():
    return {"service": "woodshread-scanner", "status": "ok"}


@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, "Upload a PNG, JPEG or PDF.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "That file is over 20 MB.")
    # TODO: run the recognition engine on `data` and build the result from it.
    return sample_result()
