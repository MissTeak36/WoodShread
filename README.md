# WoodShread

A practice tool for reading musicians. Upload a scan of your part, check anything the reader wasn't sure of, then practise it: loop sections, step the tempo up, choose the feel, and play along with a guide, drums and click.

## How it fits together

| Folder | What it is | Where it runs |
| --- | --- | --- |
| `web/` | The player: upload, score view, corrections, practice tools | GitHub Pages |
| `scanner/` | The scan reader: turns an image or PDF into notes, with a confidence score for each symbol | Railway |

The web page sends the scan to the scanner and gets back the music as JSON. Anything the scanner isn't confident about is marked `flagged` and shown in red for the player to confirm or correct.

## Instruments

The player chooses their instrument. That sets the clef, written vs concert pitch, the guide's sound and octave, and what the guide plays over chord slashes.

## Status

- [x] Repository structure
- [x] Scan result format (`scanner/schema.md`)
- [ ] Recognition engine wired into the scanner (currently returns a sample result)
- [ ] Score rendering in the player
- [ ] Practice player (transport, sections, tempo, mix)

## Running locally

Scanner:

```
cd scanner
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Player: open `web/index.html` in a browser. It talks to `http://localhost:8000` by default.
