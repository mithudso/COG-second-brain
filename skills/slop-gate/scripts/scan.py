#!/usr/bin/env python3
"""slop-gate: deterministic scan for AI-slop tells in anything about to be published.

Usage
-----
    python3 scan.py FILE [FILE...]      # scan files
    cat draft.md | python3 scan.py -    # scan stdin
    python3 scan.py --hook              # Claude Code PreToolUse/Stop hook mode (JSON on stdin)

Exit codes: 0 clean, 1 tells found, 2 unreadable input (batch checks continue).

Two tiers
---------
HARD tells fail on a single hit. They have no legitimate use in finished prose.
FILLER words fail at SOFT_LIMIT or more, because one is a word choice and five is
decoration.

Text inside backticks or quotation marks is stripped before scanning, so a piece
that quotes a tell as an exhibit does not fail on its own examples.
"""
import json
import os
import re
import sys
from pathlib import Path

SOFT_LIMIT = 3

HARD = [
    ("em dash", r"—", 0),
    ("honesty framing",
     r"\b(honestly|to be honest|if I'm being honest|the honest (part|truth|answer|reason)|I'll be honest)\b", re.I),
    ("not-X-it's-Y contrast",
     r"\b(it'?s|this is|that'?s|the (question|point|problem|issue)) (is )?not (just |only |about )?[^.\n]{2,60}[.,;] ?(it'?s|but|it is) ", re.I),
    ("not-X-it's-Y contrast", r"\bnot just [^.\n]{2,40}, (it'?s|but) ", re.I),
    ("not-X-it's-Y contrast",
     r"\b(it|this|that) (is|was) not (about |just |only )?[^.,;\n]{2,50}, (it|this|that) (is|was) ", re.I),
    ("X-not-Y contrast", r"\b[a-z][a-z-]+, not (a |an |the |just |only )?[a-z][a-z -]{1,30}[.;:]", 0),
    ("X-not-Y contrast", r"\b(rather than|instead of) [a-z][a-z -]{1,30}[.;]", re.I),
    ("rhetorical heading",
     r"^[ \t]*(#{1,6}|<h[1-6][^\r\n>]*>)[ \t]*(why (this|it) matters|the (key|real) (insight|point|opportunity|truth)|what this is not|the bottom line|the deeper point|the uncomfortable truth|here'?s the thing|the takeaway|so what|what comes next|what'?s next|where (it|this|we) go(es)? (from here|next))\b", re.I | re.M),
    ("The <Noun> heading", r"^[ \t]*(#{1,6}|<h[1-6][^\r\n>]*>)[ \t]*The [A-Z][a-z]+(?:[ \t]*</h[1-6]>)?[ \t]*$", re.M),
    ("verdict kicker",
     r"\bThat(?: is| was|['’]s) (the (point|lie|whole (point|thing)|part [a-z ]{3,30})|all [a-z ]{2,30} is for)\.", re.I),
    ("fake-profound closer",
     r"\b(let that sink in|this changes everything|what nobody (tells|talks about)|the part (everyone|most people) miss(es)?|and that'?s not nothing)\b", re.I),
    ("throat-clearing",
     r"\b(here'?s the thing|let me be clear|it'?s worth noting|it is worth noting|it'?s important to note|at the end of the day|in today'?s (fast-paced|ever-evolving|digital))\b", re.I),
    ("sycophancy",
     r"\b(great question|you'?re (absolutely )?right to push back|that'?s on me|you were right to)\b", re.I),
    ("summary-recap ending", r"^[ \t]*(in conclusion|ultimately|overall|to sum up|in summary)\b", re.I | re.M),
    ("emoji heading", r"^[ \t]*#{1,6}[ \t]*[\U0001F300-\U0001FAFF☀-➿]", re.M),
]

FILLER = re.compile(
    r"\b(delve|delves|delving|leverag(e|es|ing)|utiliz(e|es|ing)|seamless(ly)?|robust(ly)?"
    r"|tapestry|game[- ]changer|paradigm shift|cutting-edge|empower(s|ing)?|streamlin(e|es|ing)"
    r"|load-bearing|unlock the (potential|power)|genuinely|quietly|deep dive|dive in(to)?"
    r"|clean|plain|simple|elegant|powerful|lightweight)\b", re.I)

QUOTED = re.compile(r"`[^`\n]*`|\"[^\"\n]{0,160}\"|“[^”\n]{0,160}”", re.M | re.S)

TEXT_EXT = {".md", ".mdx", ".html", ".htm", ".txt", ".svg", ".rst", ""}
SKIP_COMPONENTS = {"no-ai-slop", "slop-gate", "voice-baseline", "memory", "hooks", "logs",
                   "node_modules", "site", "build", "dist"}


def strip_fences(text):
    """Ignore CommonMark-style backtick/tilde exhibits, preserving line boundaries."""
    output, fence_char, fence_size = [], '', 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip('\r\n')
        stripped = content.lstrip(' ')
        indentation = len(content) - len(stripped)
        if fence_char:
            closing = stripped.rstrip(' \t')
            if indentation <= 3 and len(closing) >= fence_size and set(closing) == {fence_char}:
                fence_char = ''
            output.append('\n' if line.endswith(('\n', '\r')) else '')
            continue
        opening = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', content)
        if opening and not (opening[1][0] == '`' and '`' in opening[2]):
            fence_char, fence_size = opening[1][0], len(opening[1])
            output.append('\n' if line.endswith(('\n', '\r')) else '')
        else:
            output.append(line)
    return ''.join(output)


def strip_quoted(text):
    """Quoted, fenced and code-formatted spans are exhibits, not the author's voice."""
    return QUOTED.sub(" ", strip_fences(text))


def scan(text, soft_limit=SOFT_LIMIT):
    body = strip_quoted(text)
    hits = []
    for label, rx, flags in HARD:
        for m in re.finditer(rx, body, flags):
            frag = body[max(0, m.start() - 28):m.end() + 28].replace("\n", " ").strip()
            hits.append("[%s] ...%s..." % (label, frag))
            if len(hits) >= 12:
                return hits
    soft = []
    for m in re.finditer(FILLER, body):
        frag = body[max(0, m.start() - 28):m.end() + 28].replace("\n", " ").strip()
        soft.append("[filler word, %d of %d allowed] ...%s..." % (len(soft) + 1, soft_limit, frag))
    if len(soft) >= soft_limit:
        hits.extend(soft[:6])
    return hits


def exempt(path, text):
    if "slop-ok:" in text:
        return True
    if not path:
        return False
    if set(Path(os.path.normpath(path)).parts) & SKIP_COMPONENTS:
        return True
    ext = os.path.splitext(path)[1].lower()
    return bool(ext) and ext not in TEXT_EXT


# --------------------------------------------------------------------------- hook mode
def hook():
    """Claude Code hook mode. Reads the hook payload on stdin, writes a decision on stdout."""
    try:
        d = json.loads(sys.stdin.read())
    except Exception:
        print("{}")
        return 0

    if not isinstance(d, dict):
        print("{}")
        return 0

    if d.get("hook_event_name") == "Stop":
        if d.get("stop_hook_active"):
            print("{}")
            return 0
        text, last = "", None
        try:
            with open(d.get("transcript_path", ""), encoding="utf-8") as f:
                for line in f:
                    try:
                        o = json.loads(line)
                    except Exception:
                        continue
                    if o.get("type") == "assistant":
                        last = o
            for c in (last or {}).get("message", {}).get("content", []):
                if c.get("type") == "text":
                    text += c.get("text", "") + "\n"
        except Exception:
            pass
        hits = scan(text)
        if hits:
            print(json.dumps({"decision": "block",
                              "reason": "slop-gate (reply): rewrite without these tells, then stop.\n"
                                        + "\n".join(hits)}))
        else:
            print("{}")
        return 0

    tool = d.get("tool_name", "")
    ti = d.get("tool_input") or {}
    if not isinstance(ti, dict):
        print("{}")
        return 0
    path = ti.get("file_path") or ti.get("path") or ""
    if not isinstance(path, str):
        print("{}")
        return 0
    text = ""
    if tool == "Write":
        text = ti.get("content", "") or ""
    elif tool == "Edit":
        text = ti.get("new_string", "") or ""
        if not isinstance(text, str):
            print("{}")
            return 0
        if path and os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as source:
                    existing = source.read()
                old = ti.get("old_string")
                replace_all = ti.get("replace_all") is True
                if isinstance(old, str) and old and old in existing and (replace_all or existing.count(old) == 1):
                    text = existing.replace(old, text, -1 if replace_all else 1)
            except (OSError, UnicodeError):
                pass

    else:
        # Any message-sending tool: Slack, Confluence, Jira, Linear, email.
        for key in ("message", "text", "body", "content"):
            if ti.get(key):
                text = ti[key] if isinstance(ti[key], str) else json.dumps(ti[key])
                break
        path = ""
        if not text:
            print("{}")
            return 0

    if not isinstance(text, str) or exempt(path, text) or not text:
        print("{}")
        return 0

    hits = scan(text)
    if hits:
        reason = ("slop-gate: %s blocked. Rewrite without these tells. "
                  "For a deliberate exhibit add `slop-ok: <reason>` to the file.\n" % tool) + "\n".join(hits)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                 "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))
    else:
        print("{}")
    return 0


def main():
    args = [a for a in sys.argv[1:] if a != "--"]
    if "--hook" in args:
        return hook()
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return 0
    failed = 0
    for path in args:
        label = "stdin" if path == "-" else path
        if path != "-" and exempt(path, ""):
            print("%s: exempt" % label)
            continue
        try:
            if path == "-":
                text = sys.stdin.read()
            else:
                with open(path, encoding="utf-8") as source:
                    text = source.read()
        except (OSError, UnicodeError) as error:
            print("%s: cannot read: %s" % (label, error), file=sys.stderr)
            failed = 2
            continue
        if exempt(path if path != "-" else "", text):
            print("%s: exempt" % label)
            continue
        hits = scan(text)
        if hits:
            failed = max(failed, 1)
            print("%s: %d tell(s)" % (label, len(hits)))
            for h in hits:
                print("  " + h)
        else:
            print("%s: clear" % label)
    return failed


if __name__ == "__main__":
    sys.exit(main())
