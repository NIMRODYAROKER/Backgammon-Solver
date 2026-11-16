# GNU BG check for the exercise bank

Every exercise in `index.html` must agree with GNU Backgammon before it goes live.

Run from an empty work folder:

    bash tools/gnubg/setup.sh                 # once: builds the engine into /tmp/gbuild
    node tools/gnubg/extract.js index.html    # writes bank.js + ex.json
    node tools/gnubg/dump.js                  # writes dump.json (all legal plays per exercise)
    python3 tools/gnubg/analyze.py            # GNU BG 2-ply equity for every play -> res.json (~5 min)
    node tools/gnubg/verify.js                # lists checker exercises that disagree
    python3 tools/gnubg/cube.py               # lists cube questions that disagree

Rules used:
- Checker play: GNU BG neural net, 2-ply, cubeless money equity of the position after the move.
  best = within 0.01 of the top move; near ("כמעט") = within 0.04; worse = wrong.
- Pure bear-off with no contact (`flag:'bear'`): fewest expected rolls, from GNU BG's one-sided bear-off database.
- Cube: GNU BG cube decision at 2-ply in a 25-point match (close to money play).
- When GNU BG's answer differs from a rule of thumb (8-9-12 etc.), the explanation says why in plain words.
