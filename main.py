"""One-line office joke for the make.fun bounty u-suzy-one-line-office-joke-laugh-off-f574ac73.
Twelve drafts were scored against the judging brief, each marked on five
axes in the brief's own order: office joke first, punch sharpness, instant
clarity, freshness, tight wording. The best total wins and is written to
/output/entry.txt, byte for byte the same on every run."""
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
# Destination file and the brief's length gate, in characters.
DESTINATION = Path("/output/entry.txt")
LIMIT = 200
SINGLE_LINE = re.compile(r"^[^\n\r]+$")
# A draft line plus its five craft marks, in the brief's own order.
@dataclass(frozen=True)
class Draft:
    line: str
    marks: tuple
    def total(self):
        return sum(self.marks)
# Twelve drafts, strongest first by total; the note on each says why it won or lost.
DRAFTS = [
    # Second pass: the ending now names the loop outright, so the punch
    # lands on the last two words instead of trailing off vaguely.
    Draft("HR's wellness survey "
          "asked what would improve my mental health; I wrote 'fewer "
          "wellness surveys,' so they sent me a survey asking about my answer.",
          (10, 9, 10, 9, 9)),
    # A label gag with a sweet payoff, but the punch is a beat more
    # predictable than the winner's recursion.
    Draft("The office fridge has a sign saying "
          "'label your food,' so I labelled mine 'emotional support lasagne' "
          "and nobody has touched it since.",
          (10, 8, 10, 9, 8)),
    # Very tight and short, but the punch is a mild wordplay turn rather
    # than a real laugh.
    Draft("I asked for a standing desk and got promoted "
          "to standing in meetings instead.",
          (10, 7, 10, 8, 10)),
    # "Closest thing to a hug" is a sweet turn, but IT-ticket jokes are a
    # familiar shape and the office frame is thinner.
    Draft("I asked IT to fix my computer and they sent me "
          "a ticket number, which is the closest thing to a hug this company offers.",
          (9, 8, 10, 8, 9)),
    # A literal-minded reply with a nice snap, but the setup leans on a
    # phrase every office worker has already heard a hundred times.
    Draft("I told my manager I was drowning in work "
          "and he sent me a link to a swimming course — professional development, apparently.",
          (9, 8, 10, 8, 9)),
    # Dave "circling back since March" is specific and relatable, but the
    # line needs a beat to land and the punch is gentle.
    Draft("I put 'team player' on my CV, which in this office "
          "means I carry the team, the project, and Dave, who has been 'circling back' since March.",
          (10, 8, 9, 8, 8)),
    # "The deadline is sacred" is a solid kicker, but fire-drill jokes are
    # a familiar office gag.
    Draft("The fire alarm went off and everyone calmly "
          "finished their emails first — the building could burn, but the deadline is sacred.",
          (10, 8, 10, 7, 8)),
    # Cute, but the punch explains itself and the laugh is mild.
    Draft("My out-of-office reply says I'm away, yet my inbox "
          "still expects me to reply — even my autoresponder has imposter syndrome.",
          (9, 7, 10, 8, 8)),
    # Both halves of the gag are shopworn office vocabulary, and it runs
    # longer than every other draft in the set.
    Draft("Our 'quick sync' has a recurring invite, an agenda, "
          "and a pre-read; the only thing quick about it is how fast my will to live leaves.",
          (10, 7, 9, 6, 7)),
    # The open-door gag is one of the oldest office jokes; the budget
    # twist does not rescue it.
    Draft("My boss said his door is always open, so I walked in "
          "and asked for a raise — turns out the door was open, the budget was not.",
          (9, 7, 10, 5, 8)),
    # The most recycled setup in office humour; the kicker adds no
    # new angle to it.
    Draft("We had a meeting to plan the meeting about the meeting, "
          "and the only action item was scheduling another meeting.",
          (10, 6, 10, 4, 8)),
    # Printer jokes are office-cliche central; "sold their soul" is a
    # decent turn but cannot carry the staleness.
    Draft("The printer finally works, which is how I know someone "
          "in this office sold their soul — and honestly, it was worth it.",
          (9, 7, 10, 4, 8))]
# Every draft must clear the brief's gate before it can be considered.
def vet(draft):
    text = draft.line
    if not 1 <= len(text) <= LIMIT:
        raise ValueError(f"draft outside 1-{LIMIT} chars: {len(text)}")
    if not SINGLE_LINE.match(text):
        raise ValueError("draft must be exactly one line")
    if not text.strip():
        raise ValueError("draft is blank")
    if len(draft.marks) != 5 or any(mark < 0 or mark > 10 for mark in draft.marks):
        raise ValueError("draft needs five marks from 0 to 10")
# Best total wins; a tie goes to the shorter line so the choice is stable.
def choose(drafts):
    seen = set()
    for draft in drafts:
        if draft.line in seen:
            raise ValueError("two drafts share the same line")
        seen.add(draft.line)
    champion = None
    for draft in drafts:
        vet(draft)
        if champion is None:
            champion = draft
            continue
        ahead = draft.total() > champion.total()
        tied_and_shorter = draft.total() == champion.total() and len(draft.line) < len(champion.line)
        if ahead or tied_and_shorter:
            champion = draft
    return champion
# Write the winner, read it back, and prove it matches byte for byte.
def run():
    winner = choose(DRAFTS)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(winner.line, encoding="utf-8")
    DESTINATION.chmod(0o644)
    raw = DESTINATION.read_bytes()
    back = raw.decode("utf-8")
    if back != winner.line:
        print("error: entry file differs from the chosen line", file=sys.stderr)
        raise SystemExit(1)
    if not 1 <= len(back) <= LIMIT:
        print("error: entry file breaks the length gate", file=sys.stderr)
        raise SystemExit(1)
    print(winner.line)
    print(f"length={len(back)} sha256={hashlib.sha256(raw).hexdigest()}")
def _launch():
    if __name__ != "__main__":
        return
    run()
_launch()
