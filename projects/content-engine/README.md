# Content engine (Nov 2026)

Stage 1 storytelling practice, automated with local AI: **Ollama** writes, **Harper** proofreads, and
**Open WebUI** is the chat front end. Nothing leaves the machine.

From one campaign objective it:

1. **Generates 20 content ideas** (title, hook, format, one-line story), asking again until it has 20 distinct ones.
2. **Scores each idea** 1–10 for originality, relatability and emotional potential, then ranks them.
3. **Finds storytelling angles** for the top 5 (confession, transformation, contrarian, POV…).
4. **Writes a creative brief** for each of the top 5 using its strongest angle: hook, audience, core message,
   beginning/middle/end, emotional beat, phone-filmable shot list, a ≤ 60-word voice-over, caption and call to action.
5. **Builds a content calendar** around recurring themes: the model groups all 20 ideas into themes, each posting
   day keeps the same theme every week, and each theme's best-scoring ideas go first.

Then **Harper** checks every hook, voice-over, caption and call to action and lists anything to fix.

The prompts follow the Stage 1 skills: three-act structure, curiosity hooks, relatability and vulnerability,
why people watch and share, and natural conversational voice-over. Who the content is for lives in
`creator.md`; edit it to change the voice.

## Run it

Needs Ollama running with a model pulled, Python 3.10+ (standard library only), and optionally `harper-cli`.

```sh
python3 -m content_engine.engine "Your campaign objective in a sentence or two"
```

The plan is written to `runs/<date>-<objective>/plan.md` (readable report) and `plan.json` (all the data).
Example output: `runs/example-everyday-adventures/plan.md`.

| Option | Default | |
|---|---|---|
| `--model` | `llama3.2:3b` | Any Ollama model. Bigger (e.g. `qwen3:8b`) writes better but is slower on CPU. |
| `--count` / `--top` | 20 / 5 | Ideas generated / ideas that get angles and briefs |
| `--themes` | 3 | Recurring themes |
| `--weeks` / `--days` / `--start` | 4 / `mon,wed,fri` / next Monday | Calendar shape |
| `--creator-file` | `creator.md` | Who the content is for and about |
| `--no-harper` | | Skip the grammar check |

**Scores are a starting point, not a verdict.** A small model scoring its own ideas is generous and
inconsistent; use the ranking to shortlist, then trust your own judgement.

## Harper

[Harper](https://github.com/Automattic/harper) is an offline grammar checker. Its CLI isn't on crates.io, so build it
from GitHub (needs Rust; about 3 minutes):

```sh
cargo install --git https://github.com/Automattic/harper harper-cli --locked
```

Harper has no New Zealand English, so the checks use **Australian** (colour, favourite, organise). Words it
shouldn't flag (te reo Māori and place names) go in `dictionary.txt`, one per line.

### In Open WebUI

`openwebui/harper_tool.py` makes Harper available inside Open WebUI chats. In Open WebUI: **Workspace → Tools → +**,
paste the file and save, then enable it for a chat (the **+** menu in the message box) or for a model
(**Workspace → Models → edit → Tools**). Ask "check the grammar of this caption: …" and the model calls Harper.
Add words it shouldn't flag in the tool's settings (the cog next to the tool → *Known words*).

## Setup in a fresh machine

```sh
curl -fsSL https://ollama.com/install.sh | sh     # needs zstd
ollama serve &                                    # if systemd isn't running it
ollama pull llama3.2:3b
uv venv --python 3.11 ~/open-webui-venv && VIRTUAL_ENV=~/open-webui-venv uv pip install open-webui
OLLAMA_BASE_URL=http://127.0.0.1:11434 ~/open-webui-venv/bin/open-webui serve --port 8080
```

## Tests

```sh
pip install pytest pytest-cov
python3 -m pytest --cov=content_engine     # Ollama isn't needed; a fake model stands in
```
