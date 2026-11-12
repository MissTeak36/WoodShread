# Scan result format

`POST /scan` (multipart form, field `file`: PNG, JPEG or PDF) returns:

```json
{
  "title": "Medium fast swing chart",
  "clef": "bass",
  "key": "F",
  "time": "cut",
  "flag_threshold": 0.8,
  "flagged_count": 2,
  "bars": [
    {
      "number": 27,
      "confidence": 0.71,
      "flagged": true,
      "marks": [{ "type": "dynamic", "value": "mf", "confidence": 0.95, "flagged": false }],
      "items": [
        { "type": "note", "pitch": "F3", "duration": "quarter", "articulation": "staccato", "confidence": 0.93, "flagged": false },
        { "type": "rest", "duration": "eighth", "confidence": 0.98, "flagged": false },
        { "type": "note", "pitch": null, "duration": "eighth", "confidence": 0.55, "flagged": true }
      ]
    }
  ]
}
```

## Fields

- **confidence**: 0 to 1, from the recognition engine. Bar confidence is the lowest of its items and marks.
- **flagged**: `true` when confidence is below `flag_threshold`. The player shows these in red.
- **pitch**: scientific pitch (`F3`), written pitch for the part. `null` when the reader found a rhythm but not a pitch.
- **type**: `note`, `rest`, `slash` (chord slash), `rhythm` (rhythm slash), `chord` (chord symbol, with `value` such as `Dmi7`).
- **marks**: dynamics, hairpins, rehearsal marks, repeats, attached to the bar.

Corrections made by the player are kept in the browser and override the scanner's result for that item.
