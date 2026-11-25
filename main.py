# One-Line Office Joke Laugh-Off — make.fun bounty
# u-suzy-one-line-office-joke-laugh-off-f574ac73
#
# The program writes one funny one-line office joke to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. is a one-line office joke about work life
#   2. lands a real laugh, sharp and surprising punchline
#   3. clear on one read, no setup that needs explaining
#   4. fresh, avoiding office cliches everyone has heard before
#   5. tight wording, every word earning its place
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # REVISED (second pass, 2026-11-25): the first draft ended "and they
    # sent me a follow-up survey about it" — "about it" was vague and
    # "follow-up survey" wordy, so the recursion never quite landed.
    # Tightened to "a survey asking about my answer": the loop is now
    # explicit and the punch sits on the last two words. Tight 8 -> 9.
    # score: office 10, punch 9, clarity 10, fresh 9, tight 9 = 47.
    ("HR's wellness survey asked what would improve my mental health; "
     "I wrote 'fewer wellness surveys,' so they sent me a survey "
     "asking about my answer.",
     47),
    # score: office 10, punch 8, clarity 10, fresh 9, tight 8 = 45.
    # A charming label gag, but the punch ("nobody has touched it")
    # is a beat more predictable than the winner's recursion.
    ("The office fridge has a sign saying 'label your food,' so I "
     "labelled mine 'emotional support lasagne' and nobody has "
     "touched it since.",
     45),
    # score: office 10, punch 7, clarity 10, fresh 8, tight 10 = 45.
    # Very tight and short, but the punch is a mild wordplay turn
    # rather than a real laugh.
    ("I asked for a standing desk and got promoted to standing in "
     "meetings instead.",
     45),
    # score: office 9, punch 8, clarity 10, fresh 8, tight 9 = 44.
    # "Closest thing to a hug" is a sweet turn, but IT-ticket jokes
    # are a familiar shape and the office frame is thinner.
    ("I asked IT to fix my computer and they sent me a ticket number, "
     "which is the closest thing to a hug this company offers.",
     44),
    # score: office 9, punch 8, clarity 10, fresh 8, tight 9 = 44.
    # The swimming-course reply is a good literal-minded turn, but
    # "drowning in work" is a well-worn setup phrase.
    ("I told my manager I was drowning in work and he sent me a link "
     "to a swimming course — professional development, apparently.",
     44),
    # score: office 10, punch 8, clarity 9, fresh 8, tight 8 = 43.
    # Dave "circling back since March" is specific and relatable, but
    # the line needs a beat to land and the punch is gentle.
    ("I put 'team player' on my CV, which in this office means I carry "
     "the team, the project, and Dave, who has been 'circling back' "
     "since March.",
     43),
    # score: office 10, punch 8, clarity 10, fresh 7, tight 8 = 43.
    # "The deadline is sacred" is a solid kicker, but fire-drill
    # jokes are a familiar office gag.
    ("The fire alarm went off and everyone calmly finished their "
     "emails first — the building could burn, but the deadline is "
     "sacred.",
     43),
    # score: office 9, punch 7, clarity 10, fresh 8, tight 8 = 42.
    # Cute ("even my autoresponder has imposter syndrome") but the
    # punch explains itself and the laugh is mild.
    ("My out-of-office reply says I'm away, yet my inbox still expects "
     "me to reply — even my autoresponder has imposter syndrome.",
     42),
    # score: office 10, punch 7, clarity 9, fresh 6, tight 7 = 39.
    # "Quick sync" and "will to live" are both tired office-joke
    # ingredients; the line is also the longest of the set.
    ("Our 'quick sync' has a recurring invite, an agenda, and a "
     "pre-read; the only thing quick about it is how fast my will "
     "to live leaves.",
     39),
    # score: office 9, punch 7, clarity 10, fresh 5, tight 8 = 39.
    # The open-door gag is one of the oldest office jokes; the
    # budget twist does not rescue it.
    ("My boss said his door is always open, so I walked in and asked "
     "for a raise — turns out the door was open, the budget was not.",
     39),
    # score: office 10, punch 6, clarity 10, fresh 4, tight 8 = 38.
    # A meeting about a meeting is the single most-told office joke;
    # nothing here is fresh.
    ("We had a meeting to plan the meeting about the meeting, and the "
     "only action item was scheduling another meeting.",
     38),
    # score: office 9, punch 7, clarity 10, fresh 4, tight 8 = 38.
    # Printer jokes are office-cliche central; "sold their soul"
    # is a decent turn but cannot carry the staleness.
    ("The printer finally works, which is how I know someone in this "
     "office sold their soul — and honestly, it was worth it.",
     38),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    joke = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(joke)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-200 characters, single line, non-blank) and print a
    # SHA-256 digest so any truncation or alteration is visible. A
    # file that does not match the selected joke must fail loudly
    # instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != joke:
        print("error: /output/entry.txt does not match selected joke",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(joke)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
