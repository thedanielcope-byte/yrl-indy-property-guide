#!/usr/bin/env python3
"""generalize_agent_copy.py — take the agent's personal name OUT of the general
marketing/CTA prose across the site, so everything reads as the brokerage/team.

KEEPS (never touched):
  • the compact agent tile (lines with daniel-cope.jpg or /agents/daniel-cope/)
  • blog posts + resource guides (bylines/author boxes) — excluded dirs
  • the agent profile pages — excluded dir
Scope: every other *.html (cities, counties, services, neighborhoods, hubs, home).

HTML-only, no whitespace reflow. Idempotent. Run, then re-grep for any remaining
prose "Daniel" and add rules until only the tile lines remain.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
EXCLUDE_DIRS = ("/blog/", "/resources/", "/agents/", "/node_modules/")
KEEP_LINE = ("daniel-cope.jpg", "/agents/daniel-cope/")

# Ordered, specific → general. Each is (regex, replacement). Applied per line.
RULES = [
    # ── "Daniel Cope and <group>" compound subjects ─────────────────────────
    (r"Daniel Cope and the Your Realty Link team", "The Your Realty Link team"),
    (r"Daniel Cope and the team at Your Realty Link", "The team at Your Realty Link"),
    (r"Daniel Cope and our our agents", "Our agents"),
    (r"Daniel Cope and our experienced agents", "Our experienced agents"),
    (r"Daniel Cope and our agents", "Our agents"),
    (r"Daniel Cope and our ((?:[A-Z][A-Za-z]+ )?(?:County|side|[A-Za-z-]+) )?team", r"Our \1team"),
    (r"Daniel Cope and our team", "Our team"),
    (r"Daniel Cope and the YRL team", "The YRL team"),
    (r"Daniel Cope and the team", "The team"),
    (r"Daniel Cope and a team invested", "a team invested"),
    (r"Daniel Cope and Your Realty Link", "Your Realty Link"),
    (r"Your Realty Link and Daniel Cope have", "Your Realty Link has"),
    # ── "Led by … Daniel Cope …" positioning ────────────────────────────────
    (r"Led by <strong>Daniel Cope</strong>, Real Estate Broker and longtime agent, our team serves", "Our team serves"),
    (r"(MIBOR[- ]?(?:member )?brokerage) led by <strong>Daniel Cope</strong>", r"\1"),
    (r"MIBOR brokerage led by Daniel Cope[,—-]+ ?helps", "MIBOR brokerage helps"),
    (r"(brokerage) led by Daniel Cope\. Our agents", r"\1. Our agents"),
    (r"(brokerage) led by Daniel Cope —", r"\1 —"),
    (r"[Aa] brokerage led by Daniel Cope\.", "a full-service brokerage."),
    (r"led by Real Estate Broker <strong>Daniel Cope</strong>", "led by an experienced team of brokers"),
    (r"and Real Estate Broker <strong>Daniel Cope</strong>", "and an experienced team of brokers"),
    (r"directly with Real Estate Broker <strong>Daniel Cope</strong>", "directly with an experienced team of brokers"),
    (r"led by Real Estate Broker Daniel Cope", "led by an experienced team of brokers"),
    (r"and Broker Daniel Cope (brings|helps|guides|works)", r"and our brokers \1"),
    (r"Broker Daniel Cope (brings|helps|guides|works)", r"Our brokers \1"),
    (r"experienced agents and broker Daniel Cope\.", "experienced agents and brokers."),
    (r"direct access to broker Daniel Cope for", "direct access to our brokers for"),
    # ── CTA verbs with the name as object ───────────────────────────────────
    (r"Call Daniel today", "Call us today"),
    (r"Call Daniel Now", "Call Us Now"),
    (r"Call Daniel:", "Call Us:"),
    (r"Call Daniel at ", "Call us at "),
    (r"Call Daniel Today", "Call Us Today"),
    (r"Call Daniel Cope today\.", "Call us today."),
    (r"Call Daniel Cope today", "Call us today"),
    (r"Call Daniel Cope at 317-997-7404", "Call us at 317-997-7404"),
    (r"call Daniel Cope at 317-997-7404", "call us at 317-997-7404"),
    (r"Call Daniel Cope for", "Call us for"),
    (r"Call Daniel Cope to", "Call us to"),
    (r"Call Daniel Cope directly\.", "Call us directly."),
    (r"Call Daniel Cope directly", "Call us directly"),
    (r"Call Daniel Cope first", "Call us first"),
    (r"Call Daniel Cope before", "Call us before"),
    (r"Call Daniel Cope or", "Call us or"),
    (r"Call Daniel Cope\.", "Call us."),
    (r"Call Daniel Cope", "Call us"),
    (r"call Daniel Cope directly", "call us directly"),
    (r"call Daniel Cope for", "call us for"),
    (r"call Daniel Cope at", "call us at"),
    (r"call Daniel Cope", "call us"),
    (r"call Daniel or start", "call us or start"),
    (r"call Daniel at ", "call us at "),
    (r"Contact Daniel Cope at 317-997-7404", "Contact Your Realty Link at 317-997-7404"),
    (r"contact Daniel Cope directly at", "contact us directly at"),
    (r"Or contact Daniel Cope directly at", "Or contact us directly at"),
    (r"or contact Daniel Cope at", "or contact us at"),
    (r"Contact Daniel Cope at ", "Contact Your Realty Link at "),
    (r"Contact Daniel(?![ ]Cope)", "Contact Us"),
    (r"Meet Daniel Cope today", "Meet the Your Realty Link team today"),
    (r"Meet Daniel Cope", "Meet Our Team"),
    (r"Email Daniel Confidentially", "Email Us Confidentially"),
    (r"Email Daniel(?![ ]Cope)", "Email Us"),
    (r"Talk to Daniel Today", "Talk to Our Team Today"),
    (r"Talk to Daniel(?![ ]Today)", "Talk to Our Team"),
    (r"Talk with Daniel Cope about", "Talk with our team about"),
    (r"Let Daniel show you", "Let us show you"),
    (r"Reach out to Daniel Cope and the team", "Reach out to the Your Realty Link team"),
    (r"connect with Daniel Cope for", "connect with our team for"),
    (r"connect with Daniel Cope and a trusted", "connect with the Your Realty Link team and a trusted"),
    (r"Connect with Daniel Cope and the Your Realty Link team", "Connect with the Your Realty Link team"),
    (r"Connect with Daniel Cope and a trusted", "Connect with the Your Realty Link team and a trusted"),
    (r"Call or message Daniel Cope", "Call or message us"),
    (r"work directly with Daniel Cope and a team", "work directly with a team"),
    (r"work directly with Daniel Cope", "work directly with our team"),
    (r"access to Daniel Cope for questions", "access to our brokers for questions"),
    (r"access to Daniel Cope,", "access to our brokers,"),
    (r"with Daniel Cope, hands-on mentorship", "with our brokers, hands-on mentorship"),
    (r"a personalized CMA from Daniel Cope\.", "a personalized CMA from Your Realty Link."),
    (r"valuation from Daniel Cope and the YRL team\.", "valuation from the YRL team."),
    (r"valuation from Daniel Cope and our south-side team\.", "valuation from our south-side team."),
    (r"valuation from Daniel Cope —", "valuation from Your Realty Link —"),
    (r"valuation from Daniel Cope\.", "valuation from Your Realty Link."),
    (r"CMA from Daniel for", "CMA from Your Realty Link for"),
    (r"offer from Daniel Cope\.", "offer from Your Realty Link."),
    (r"prepared by Daniel Cope using", "prepared by our team using"),
    (r"conversation with Daniel Cope about", "conversation with our team about"),
    (r"consultation with Daniel Cope is the best", "consultation with our team is the best"),
    (r"consultation with Daniel Cope\.", "consultation with our team."),
    (r"Free consultation with Daniel Cope\.", "Free consultation with Your Realty Link."),
    (r"no-pressure consultation with Daniel Cope\.", "no-pressure consultation with Your Realty Link."),
]

# "Daniel Cope <verb>" and "Daniel <verb>" bare subjects -> "Our team <verb>"
# (kept as a general fallback AFTER the specific rules above).
SUBJECT = [
    (r"\bDaniel Cope and our team\b", "Our team"),
    (r"\bDaniel Cope and the team\b", "The team"),
    (r"\bDaniel Cope\b", "Our team"),
    (r"\bDaniel\b", "our team"),
]

# team singular-verb agreement after collapsing "Daniel Cope and the team"
TEAM_VERB = {"know": "knows", "help": "helps", "have": "has", "move": "moves",
             "provide": "provides", "approach": "approaches", "treat": "treats",
             "start": "starts", "understand": "understands", "walk": "walks",
             "represent": "represents", "work": "works", "take": "takes",
             "bring": "brings", "believe": "believes", "coordinate": "coordinates",
             "manage": "manages", "lead": "leads", "review": "reviews",
             "want": "wants", "answer": "answers", "tour": "tours",
             "negotiate": "negotiates", "do": "does", "don't": "doesn't"}


def fix_team_verbs(s):
    def rep(m):
        pre, verb = m.group(1), m.group(2)
        return pre + TEAM_VERB.get(verb, verb)
    # "(The|Our) ... team <verb>" and "(The|Our) ... team are"
    s = re.sub(r"((?:The|Our)(?: [A-Za-z-]+){0,3} team )(know|help|have|move|provide|approach|treat|start|understand|walk|represent|work|take|bring|believe|coordinate|manage|lead|review|want|answer|tour|negotiate|do|don't)\b", rep, s)
    s = re.sub(r"((?:The|Our)(?: [A-Za-z-]+){0,3} team )are\b", r"\1is", s)
    return s


def process(html):
    out = []
    for line in html.split("\n"):
        if any(k in line for k in KEEP_LINE):
            out.append(line); continue
        if "Daniel" not in line:
            out.append(line); continue
        for pat, rep in RULES:
            line = re.sub(pat, rep, line)
        for pat, rep in SUBJECT:
            line = re.sub(pat, rep, line)
        line = fix_team_verbs(line)
        out.append(line)
    return "\n".join(out)


def main():
    pages = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if not any(d in p.replace(ROOT, "") for d in EXCLUDE_DIRS)]
    changed = 0
    for p in pages:
        src = open(p, encoding="utf-8").read()
        new = process(src)
        if new != src:
            open(p, "w", encoding="utf-8").write(new); changed += 1
    print("rewrote %d of %d general pages" % (changed, len(pages)))


if __name__ == "__main__":
    main()
