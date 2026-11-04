"""Place voice-over phrases on the film timeline and emit the ffmpeg filter + film-time word cues."""
import json, sys
plan = json.load(open(sys.argv[1]))
words = json.load(open(sys.argv[2]))
words = words.get("words") or [x for s in words.get("segments", []) for x in s.get("words", [])]
FADE = 0.02
parts, labels, cues = [], [], []
for i, p in enumerate(plan):
    dur = p["to"] - p["from"]
    ms = int(round(p["at"] * 1000))
    parts.append(f"[0:a]atrim={p['from']}:{p['to']},asetpts=PTS-STARTPTS,afade=t=in:d={FADE},afade=t=out:st={dur-FADE:.3f}:d={FADE},adelay={ms}|{ms}[p{i}]")
    labels.append(f"[p{i}]")
    for w in words:
        if w["start"] >= p["from"] and w["end"] <= p["to"] + 0.05:
            off = p["at"] - p["from"]
            cues.append({"text": w["word"].strip(), "start": round(w["start"] + off, 3), "end": round(w["end"] + off, 3)})
mix = "".join(labels) + f"amix=inputs={len(plan)}:normalize=0:dropout_transition=0"
chain = "highpass=f=90,afftdn=nr=10:nf=-45,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-2:LRA=7"
print(json.dumps({"filter": ";".join(parts) + ";" + mix + "," + chain + "[vo]", "cues": cues}))
