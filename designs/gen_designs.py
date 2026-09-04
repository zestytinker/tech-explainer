import os, textwrap

OUT = "/mnt/user-data/outputs/designs"

# ---------- low-fidelity kit ----------
CSS = """
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,sans-serif;color:#222;background:#fff;max-width:960px;padding:24px;margin:0 auto}
h1{font-size:28px;margin:0 0 8px}h2{font-size:20px;margin:24px 0 8px}
p{max-width:64ch}
.wire{border:1px dashed #999;padding:12px;margin:12px 0;color:#666}
.note{font-size:13px;color:#888;border-left:3px solid #ddd;padding-left:8px;margin:8px 0}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
button,.btn{font:inherit;padding:6px 12px;border:2px solid #222;background:#fff;border-radius:6px;cursor:pointer}
.btn.secondary{border-color:#aaa;color:#666}.btn.disabled{border-color:#ddd;color:#bbb}
input{font:inherit;padding:6px 8px;border:1px solid #888;border-radius:4px}
.strip{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}
.bulb{width:22px;height:22px;border-radius:50%;border:2px solid #444;background:#fff}
.bulb.on{border-color:transparent}
.bulb.ring{outline:3px solid #222;outline-offset:2px}
.words{display:flex;gap:8px;flex-wrap:wrap}
.word{padding:2px 8px;border-radius:12px;color:#fff;font-size:14px}
.verdict{font-weight:600;padding:8px 12px;border:1px solid #222;display:inline-block}
.sources{font-size:14px;color:#555;margin-top:32px;border-top:1px solid #ddd;padding-top:12px}
.sources li{margin:4px 0}
nav.site{font-size:14px;color:#666;margin-bottom:16px}
nav.site a{color:#222}
.card{border:1px solid #999;border-radius:8px;padding:16px;width:280px}
.card.ghost{border-style:dashed;color:#aaa}
.grid{display:flex;gap:16px;flex-wrap:wrap}
.steps{display:flex;gap:4px;margin:16px 0}
.step{padding:6px 10px;border:1px solid #999;font-size:14px}.step.cur{background:#222;color:#fff}
.side{display:flex;gap:24px}.side>aside{width:200px;flex:none;font-size:14px}
.side>aside a{display:block;color:#222;padding:3px 0}
.coach{border:2px solid #222;border-radius:8px;padding:12px;width:300px;flex:none}
.coach li{margin:6px 0}.coach li.done{color:#999;text-decoration:line-through}
.mascot{width:120px;height:120px;border:2px dashed #999;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#888;font-size:12px;text-align:center}
.full{min-height:70vh;display:flex;flex-direction:column;justify-content:center}
details summary{cursor:pointer;color:#555}
.search{font-size:22px;padding:14px;width:100%;max-width:640px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.chip{border:1px solid #999;border-radius:16px;padding:4px 12px;font-size:14px}.chip.off{color:#bbb;border-color:#ddd}
@media(max-width:480px){.side{flex-wrap:wrap}.side>aside,.coach{width:100%}.bulb{width:20px;height:20px}.strip{max-width:312px}}
.tag{font-size:12px;color:#666;border:1px solid #ccc;border-radius:4px;padding:0 6px;margin-right:4px}
"""

COLORS = ["#c0392b","#2980b9","#27ae60","#8e44ad","#d35400","#16a085","#7f8c8d","#2c3e50"]
SEED = ["cat","dog","fig","sun","map","jar","owl","ink"]
# fake but fixed bulb indices per seed word (3 each), chosen so a few bulbs are shared
SEED_BITS = {"cat":[4,11,19],"dog":[2,11,22],"fig":[7,15,19],"sun":[0,9,14],
             "map":[3,11,20],"jar":[5,13,23],"owl":[1,9,18],"ink":[8,15,21]}

def strip(lit=None, ring=None, hollow=False, n=24):
    lit = lit or {}
    ring = ring or []
    out = []
    for i in range(n):
        cls = "bulb"
        style = ""
        if i in lit:
            cls += " on"; style = f' style="background:{lit[i]}"'
        if i in ring: cls += " ring"
        out.append(f'<span class="{cls}"{style} title="bulb {i}"></span>')
    return f'<div class="strip">{"".join(out)}</div>'

def seeded_strip(ring=None):
    lit = {}
    for w, bits in SEED_BITS.items():
        c = COLORS[SEED.index(w)]
        for b in bits:
            lit.setdefault(b, c)      # first word wins (D16)
    return strip(lit, ring)

def words(ws=SEED):
    return '<div class="words">' + "".join(
        f'<span class="word" style="background:{COLORS[SEED.index(w)]}">{w}</span>' for w in ws) + "</div>"

def playground(state="seeded", verdict=None, ring=None, compact=False, copy=("Definitely not in the set","Might be in the set")):
    if state == "empty":
        s = strip(); wl = '<div class="wire">word list (empty)</div>'
        seedbtn = '<button>Seed 8 words</button>'
        suggest = '<span class="btn secondary disabled">Suggest a word</span>'
    else:
        s = seeded_strip(ring); wl = words()
        seedbtn = '<span class="btn disabled">Seed 8 words</span>'
        suggest = '<span class="btn secondary">Suggest a word</span>'
    v = f'<p><span class="verdict">{verdict}</span></p>' if verdict else ""
    return f"""
<div class="row"><input placeholder="add a word"><button>Add</button>{seedbtn}<span class="btn secondary">Reset</span></div>
{s}
{wl}
<div class="row" style="margin-top:12px"><input placeholder="is this word in the set?"><button>Check</button>{suggest}</div>
{v}
{'' if compact else '<p class="note">Hover a word to light its three bulbs. After a check, the three bulbs it looked at keep a ring.</p>'}
"""

def sources(n=2):
    items = ['Bloom, B. H. (1970). Space/time trade-offs in hash coding with allowable errors. CACM 13(7). <a href="https://doi.org/10.1145/362686.362692">doi</a>',
             'Broder &amp; Mitzenmacher (2004). Network applications of Bloom filters: a survey. Internet Mathematics 1(4).']
    extra = ['<span class="wire" style="display:inline">[source needed: system X docs]</span>'] * max(0, n-2)
    return '<div class="sources"><b>Sources</b><ol>' + "".join(f"<li>{x}</li>" for x in (items+extra)[:n]) + "</ol></div>"

def sitenav(current="bloom-filter", extra=""):
    return f'<nav class="site"><a href="landing.html">All explainers</a> &nbsp;/&nbsp; {current} {extra}</nav>'

def page(title, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"

ORIGIN = ('<p>In 1970 Burton Bloom was looking at a problem where checking a big list was expensive and '
          'being occasionally wrong in one direction was survivable. He showed you could shrink the list '
          'to a strip of bits if you accepted a small rate of false "yes" answers, and never a false "no".<sup>[1]</sup></p>')

# ---------- designs ----------
D = {}

def add(slug, title, files, rationale, tradeoff, bends, checks, meta):
    D[slug] = dict(title=title, files=files, rationale=rationale, tradeoff=tradeoff, bends=bends, checks=checks, meta=meta)

# 1 single scroll, playground first
landing_cards = f"""
<h1>Explainers</h1><p>Build a tiny version of a hard idea, then break it.</p>
<div class="grid">
 <div class="card"><b>Bloom filter</b><p>A list that says "definitely not" or "might be", and nothing else.</p>{strip({4:COLORS[0],11:COLORS[0],19:COLORS[0],2:COLORS[1],22:COLORS[1]}, n=12)}<a class="btn" href="explainer.html">Open</a></div>
 <div class="card ghost"><b>Next concept</b><p>Same skeleton: title, playground, one paragraph, sources.</p><div class="wire">playground thumbnail</div><span class="btn disabled">Soon</span></div>
</div>"""
add("01-single-scroll-playground-first", "Single scroll, playground first",
 {"landing.html": page("Explainers", landing_cards),
  "explainer.html": page("Bloom filter", sitenav() + "<h1>Bloom filter</h1><p>A list that can say \"definitely not\" or \"might be\", and nothing else. Add words, then ask about one you never added.</p>"
     + playground("seeded", "Might be in the set", ring=[4,11,22]) + "<h2>Why this exists</h2>" + ORIGIN + sources(2))},
 "The spec's baseline. Everything above the fold is the playground; the only prose is one sentence on top and one origin paragraph below. The landing is a card list with one real card and one ghost card that shows the skeleton the second concept will fill.",
 "Reader who does not spontaneously connect the lit bulbs to the false positive gets no help. Hit rate on goal 1 rides entirely on D7 and D8.",
 "None.",
 ["Reviewer path (seed, check, suggest, check, hover, reset) completes without scrolling at 1280 and with one scroll at 375.",
  "Landing to explainer is one click; explainer back to landing is one click.",
  "Count factual sentences: exactly the origin paragraph, 1 to 2 numbered claims, both resolving to sources 1 and 2.",
  "Ghost card dry run: copy the card, point it at an empty /second/ folder, nothing in /bloom-filter/ changes."],
 dict(prose="1 para", facts=2, verify="Low", sixty="Yes", scale="Good", cost="Fits", hit="Medium"))

# 2 stepped six-part
def steps(cur):
    names = ["Why","How","Break it","Origin","Real world","Read further"]
    return '<div class="steps">' + "".join(f'<span class="step{" cur" if i==cur else ""}">{i+1}. {n}</span>' for i,n in enumerate(names)) + "</div>"
add("02-stepped-six-part", "Stepped six-part page",
 {"landing.html": page("Explainers", landing_cards.replace("explainer.html","explainer-1-why.html")),
  "explainer-1-why.html": page("Why", sitenav() + "<h1>Bloom filter</h1>" + steps(0) + "<h2>Why would anyone want a list that lies?</h2><p>Imagine checking every new username against a hundred million taken ones. The real list lives on a slow disk. What if you had a cheap thing in memory that could say \"definitely free\" most of the time, and only sent the hard cases to the disk?<sup>[1]</sup></p><div class='wire'>illustration: fast small box in front of slow big box</div><p><a class='btn' href='explainer-3-break.html'>Next: How</a></p>" + sources(2)),
  "explainer-3-break.html": page("Break it", sitenav() + "<h1>Bloom filter</h1>" + steps(2) + "<h2>Break it</h2><p>Seed the list, then ask about a word you never added. Keep going until it says \"might be\".</p>" + playground("seeded","Might be in the set",ring=[4,11,22]) + "<p><a class='btn' href='explainer-5-real.html'>Next: Origin</a></p>" + sources(2)),
  "explainer-5-real.html": page("Real world", sitenav() + "<h1>Bloom filter</h1>" + steps(4) + "<h2>Where this runs today</h2><p>Databases use one in front of every file on disk so a lookup for a missing key never touches the disk.<sup>[3]</sup></p><p>Browsers have used one to check URLs against a blocklist without shipping the whole list.<sup>[4]</sup></p><p>CDNs use one to avoid caching things that will only ever be asked for once.<sup>[5]</sup></p><div class='wire'>each claim above needs current official docs before it ships</div><p><a class='btn' href='#'>Next: Read further</a></p>" + sources(5))},
 "A course, not a page. Six steps in a fixed order carry the reader from motivation to playground to history to applications. The stepped nav is honest here because the content really is a sequence.",
 "Reviewer must click through five steps to see everything, which kills the 60 second path. The Real world step alone adds three claims that each need current documentation; this is the design where the facts rule costs the most.",
 "D21 (one paragraph of prose) is broken outright. Goal 2 is at risk. The playground is on step 3, so a reviewer landing cold sees prose first.",
 ["Time a cold reviewer clicking through all six steps. Must be under 60 s or the design fails goal 2.",
  "Count factual claims across all six steps. Each needs a resolving source before deploy; expect 8 to 12.",
  "Step 5 claims about named systems: open each system's current docs on deploy day and confirm the claim is still true.",
  "Second concept dry run: the six step names must fit the new concept without renaming. If they don't, the skeleton is not shared."],
 dict(prose="6 sections", facts=10, verify="High", sixty="No", scale="Medium", cost="Over", hit="High"))

# 3 search first landing (revised per review: fixed local list, no input can fail)
BUILT=[("bloom filter","explainer.html")]
KNOWN=["hash table","merkle tree","consistent hashing","hyperloglog","cuckoo filter","lru cache"]   # sample of the ~200 allowlist entries (content/allowlist.py)
def search_landing(state="focus", typed=""):
    box=f'<input class="search" placeholder="try: bloom filter" value="{typed}">'
    offer="".join(f'<a class="chip" href="{h}">{n}</a>' for n,h in BUILT)
    if state=="focus":
        dd=('<div class="wire" style="max-width:640px;margin-top:0"><b>Built</b><br>'+"".join(f'<a href="{h}">{n}</a><br>' for n,h in BUILT)
            +'<span style="color:#888">Or type to search about 200 concepts: '+", ".join(KNOWN[:4])+'...</span></div>')
        msg='<p class="note">Dropdown opens on focus: built explainers plus a prompt to type. The ~200 name allowlist is in the page; nothing is fetched.</p>'
    elif state=="typing":
        dd=('<div class="wire" style="max-width:640px;margin-top:0"><a href="explainer.html"><b>bloo</b>m filter</a> <span class="tag">built</span><br><span style="color:#888"><b>bloo</b>m filter false positive rate</span> <span class="tag">no explainer</span></div>')
        msg='<p class="note">Matches from the allowlist appear as you type, built ones first. Full match on a built name opens the page (OQ-11).</p>'
    elif state=="notyet":
        dd=f'<div class="wire" style="max-width:640px;margin-top:0">Merkle tree is a real concept, but there is no explainer for it here yet. Built so far: {offer}</div>'
        msg='<p class="note">On the allowlist, no page. Says "real concept, no explainer here", not "coming soon". Built ones offered.</p>'
    else:
        dd=f'<div class="wire" style="max-width:640px;margin-top:0">No explainer for "{typed}" here. Built so far: {offer}</div>'
        msg='<p class="note">Not on the allowlist. Friendly "not supported", same offer. No input can end in a dead state, and nothing was fetched.</p>'
    return f'<div class="full"><h1>What do you want to understand?</h1>{box}{dd}{msg}</div>'
add("03-search-first-landing", "Search-first landing (fixed local list)",
 {"landing.html": page("Explainers", search_landing("focus")),
  "landing-typing.html": page("Explainers", search_landing("typing","bloo")),
  "landing-notyet.html": page("Explainers", search_landing("notyet","merkle tree")),
  "landing-unsupported.html": page("Explainers", search_landing("unsupported","quantum foam")),
  "explainer.html": D["01-single-scroll-playground-first"]["files"]["explainer.html"]},
 "The landing is one question and a search box, and every answer is decided on the reader's device against an allowlist of about 200 tech concepts shipped inside the page (content/allowlist.py). Focus shows the built explainers and a prompt to type. Typing shows matches, built first, and a full match on a built name opens the page. An allowlisted name with no page gets \"real concept, no explainer here yet\"; anything else gets \"not supported\"; both offer the built ones. No input can fail and nothing is fetched. The explainer is design 1.",
 "Three extra states and a typeahead over 200 names, roughly 20 minutes of the 2 hours. Under the facts rule each of the 200 names is a small claim, so the list needs its own verification check (checks/verify_allowlist.py) and entries that fail it are dropped, not shipped. Matching tolerance (plurals, aliases, typos) is where the reviewer experience is decided and it is not free.",
 "None. Section 4b said conventions not shared code; this landing needs a small concept list in the page, which is the one place a second explainer must register itself (name, aliases, path).",
 ["Focus the empty box: dropdown shows every built name and every recognised name, grouped, nothing else.",
  "Type each built name in full: page opens. Type a prefix: it highlights, Enter opens.",
  "Type five allowlisted names with no page, including one via an alias and one as a plural: real-concept message plus links to every built one. No dead end.",
  "Type gibberish, an empty string, 200 characters, an emoji: not supported message plus the same links. No console errors.",
  "Network off: all four behaviors identical, proving nothing is fetched.",
  "Second concept dry run: adding a concept is one entry in the list plus a folder. The dropdown and the not yet list update with no other edit.",
  "Explainer checks: same four as design 1."],
 dict(prose="1 para", facts=2, verify="Low", sixty="Yes", scale="Good, list-driven", cost="Fits, +15 min", hit="Medium"))

# 4 catalog landing
catalog = f"""
<h1>Explainers</h1>
<div class="row"><span class="tag">all</span><span class="tag">data structures</span><span class="tag">networks</span><span class="tag">under 2 min</span></div>
<div class="grid" style="margin-top:12px">
 <div class="card"><span class="tag">data structures</span><span class="tag">2 min</span><b>Bloom filter</b><p>Make it lie to you, then find out why.</p>{strip({4:COLORS[0],11:COLORS[0],19:COLORS[0],2:COLORS[1],22:COLORS[1]}, n=12)}<a class="btn" href="explainer.html">Open</a></div>
 <div class="card ghost"><span class="tag">networks</span><b>Consistent hashing</b><p>placeholder</p><div class="wire">thumbnail</div></div>
 <div class="card ghost"><span class="tag">data structures</span><b>Merkle tree</b><p>placeholder</p><div class="wire">thumbnail</div></div>
</div>"""
add("04-catalog-landing", "Catalog landing with tags",
 {"landing.html": page("Explainers", catalog),
  "explainer.html": D["01-single-scroll-playground-first"]["files"]["explainer.html"]},
 "A browsable catalog: tags, a time estimate, a thumbnail of each playground. Built for the day there are eight explainers. The explainer is the baseline.",
 "Tags and filters on a catalog of one look like a storefront with one product. The thumbnail per card is the only part that earns its place today; the filters cost build time and deliver nothing until concept three.",
 "None. It adds scope to the landing (tags, filters) that section 4b did not ask for.",
 ["With one card, all filters must be hidden or disabled, not shown as working controls that do nothing.",
  "Thumbnail on the card must be the real seeded strip, not a drawn approximation, so it never drifts from the explainer.",
  "Second concept dry run: adding a card requires only a folder and one card block.",
  "Explainer checks: same four as design 1."],
 dict(prose="1 para", facts=2, verify="Low", sixty="Yes", scale="Good at 3+", cost="Slightly over", hit="Medium"))

# 5 bouncer playful
bouncer = (sitenav() + "<div class='row'><div class='mascot'>bouncer sketch</div><div><h1>The bouncer with no memory</h1><p>He does not remember faces. He remembers three stamps per person, on a card with 24 squares. Ask him about anyone and he checks their three squares.</p></div></div>"
  + playground("seeded", "Yeah... probably? Not sure.", ring=[4,11,22], copy=("Not on my list. Certain.","Yeah... probably? Not sure."))
  + "<p class='note'>Verdict copy here is in character. Spec D9 requires plain copy; this design exists to show what plain buys you.</p><h2>Why he exists</h2>" + ORIGIN + sources(2))
add("05-bouncer-playful", "Bouncer-style playful",
 {"landing.html": page("The club", "<h1>The club</h1><p>Every idea in here is a person with a job. Pick a door.</p><div class='grid'><div class='card'><div class='mascot'>bouncer</div><b>The bouncer with no memory</b><p>Bloom filter</p><a class='btn' href='explainer.html'>Meet him</a></div><div class='card ghost'><div class='mascot'>?</div><b>Next character</b><p>next concept</p></div></div>"),
  "explainer.html": page("Bouncer", bouncer)},
 "Every concept becomes a character with a job. The Bloom filter is a bouncer who remembers stamps, not faces. Character metaphor scales naturally: concept two is another person at the club.",
 "The metaphor implies memory. A bouncer who \"remembers stamps\" is a step away from a reader believing the filter stores words. The in-character verdicts (\"probably? not sure\") blur the one asymmetry the page must protect: \"no\" is a promise, \"yes\" is a guess.",
 "D9 (plain verdict copy) and D10 (playfulness in visuals only) are both broken. This design is the argument for those two decisions, shown rather than asserted.",
 ["Reader test question after a false positive: if the answer mentions the bouncer \"forgetting\" or \"remembering\" a word, the metaphor has misled them and the design fails goal 1.",
  "Verdict copy must still make \"no\" read as certain and \"yes\" as uncertain to a cold reader. Ask three people which answer they would trust.",
  "Mascot art time is tracked separately; it does not count toward the 2 h build.",
  "Facts: same two as design 1. The metaphor sentences are not factual claims."],
 dict(prose="1 para + metaphor", facts=2, verify="Low", sixty="Yes", scale="Good", cost="Over (art)", hit="Medium, risk of wrong model"))

# 6 reference style
ref = sitenav() + """<div class="side"><aside><a href="#">Overview</a><a href="#">Playground</a><a href="#">Parameters</a><a href="#">The math</a><a href="#">History</a><a href="#">Applications</a><a href="#">Variants</a><a href="#">References</a><hr><b>Explainers</b><a href="#">Bloom filter</a><a href="#" style="color:#aaa">Merkle tree</a></aside><div>
<h1>Bloom filter</h1><p>A Bloom filter is a space-efficient probabilistic structure for set membership. It reports either that an element is definitely not in the set or that it may be.<sup>[1]</sup></p>
<h2>Parameters</h2><p>m bits, k hash functions, n inserted elements. With m = 24, k = 3, n = 8, about 64% of bits are set and the false positive rate is about 26%.<sup>[2]</sup></p>
<h2>Playground</h2>""" + playground("seeded", "Might be in the set", ring=[4,11,22], compact=True) + """
<h2>The math</h2><p>P(false positive) ≈ (1 − e^(−kn/m))^k.<sup>[2]</sup></p><div class="wire">table of n vs rate</div>
<h2>History</h2>""" + ORIGIN + """<h2>Applications</h2><div class="wire">3 to 6 named systems, each needs current docs</div><h2>Variants</h2><div class="wire">counting, cuckoo, blocked, each needs a paper</div></div></div>""" + sources(6)
add("06-reference-style", "Reference style, prose first",
 {"landing.html": page("Explainers", "<h1>Explainers</h1><div class='side'><aside><b>Contents</b><a href='explainer.html'>Bloom filter</a><a href='#' style='color:#aaa'>Merkle tree</a></aside><div><p>Reference pages with an embedded playground. Pick one on the left.</p></div></div>"),
  "explainer.html": page("Bloom filter", ref)},
 "A documentation page with a sidebar table of contents and the playground embedded a third of the way down. Reads as authoritative and links every claim. Scales to many concepts through the sidebar alone.",
 "Prose first means the reviewer scrolls past two sections to find the thing to click, and a generalist meets \"space-efficient probabilistic structure\" before they meet a bulb. It is also the most expensive design under the facts rule: parameters, math, applications and variants all carry claims.",
 "D21 broken. Goal 2 at risk. The tone drifts from generalist to practitioner, which is a different audience than section 2.",
 ["Cold reviewer must find the playground in under 15 s. Measure scroll distance at 375 wide.",
  "Every sup number resolves. Expect 15 to 20 claims; each is a lookup.",
  "Applications and Variants sections ship only if every named system or paper is sourced on deploy day; otherwise the section is cut, not the check.",
  "Reader test with a generalist: do they read the first paragraph or skip it? If they skip it, the design is paying for prose nobody reads."],
 dict(prose="7 sections", facts=18, verify="Very high", sixty="No", scale="Best", cost="Over", hit="Low for generalists"))

# 7 playground only
po = ("<nav class='site'><b>Explainers:</b> Bloom filter <span style='color:#aaa'>| next concept</span></nav><div class='full'><h1 style='font-size:20px'>Bloom filter</h1>"
      + playground("empty") + "<details><summary>Why does this exist?</summary>" + ORIGIN + sources(2) + "</details></div>")
add("07-playground-only", "Playground only",
 {"landing.html": page("Explainers", "<p class='note'>No separate landing. The root is the first explainer with a concept switcher in the corner. See explainer.html.</p><p><a class='btn' href='explainer.html'>Open</a></p>"),
  "explainer.html": page("Bloom filter", po)},
 "The whole page is the playground, empty on load, with one disclosure that reveals the origin paragraph and sources. The concept switcher in the corner is the landing. Nothing to read until you ask.",
 "No framing sentence means a cold reviewer sees bulbs and boxes with no idea what they are for. The disclosure hides the only prose, so the facts rule is nearly free but the page gives the reader no reason to care before they click.",
 "Section 4b (a landing page at the root listing explainers) is bent: the root is the first explainer. Otherwise inside every Decided line.",
 ["Cold reviewer with no instructions: do they click Seed within 10 s? If not, the empty state needs a prompt, which becomes the framing sentence this design removed.",
  "Disclosure open and closed states both pass R12.",
  "Concept switcher dry run: adding a concept is one link.",
  "Above the fold at 375 wide: strip, both boxes, three buttons all visible with the disclosure closed."],
 dict(prose="hidden", facts=2, verify="Lowest", sixty="Yes, if they click", scale="Weak (no landing)", cost="Fits easily", hit="Medium"))

# 8 guided tour
def coach(done):
    items = ["Seed 8 words.", "Check a word that is not in the list. Try penguin.", "It said might be? Ring shows the 3 bulbs it looked at.", "Hover cat, dog, fig. Whose bulbs are those?", "Now say it in one sentence: why did it say might be?"]
    return "<div class='coach'><b>Try this</b><ol>" + "".join(f"<li class='{'done' if i<done else ''}'>{t}</li>" for i,t in enumerate(items)) + "</ol><span class='btn secondary'>Skip the tour</span></div>"
gt_start = sitenav() + "<h1>Bloom filter</h1><p>A list that can say \"definitely not\" or \"might be\", and nothing else.</p><div class='side'><div style='flex:1'>" + playground("empty", compact=True) + "</div>" + coach(0) + "</div><h2>Why this exists</h2>" + ORIGIN + sources(2)
gt_caught = sitenav() + "<h1>Bloom filter</h1><p>A list that can say \"definitely not\" or \"might be\", and nothing else.</p><div class='side'><div style='flex:1'>" + playground("seeded", "Might be in the set", ring=[4,11,22], compact=True) + "</div>" + coach(3) + "</div><h2>Why this exists</h2>" + ORIGIN + sources(2)
add("08-guided-tour", "Guided tour beside the playground",
 {"landing.html": page("Explainers", landing_cards.replace("explainer.html","explainer-start.html")),
  "explainer-start.html": page("Bloom filter", gt_start),
  "explainer-caught.html": page("Bloom filter", gt_caught)},
 "Design 1 plus a side panel of five prompts that tick off as the reader does them. The prompts do the scaffolding D7 declined to do, but as optional nudges rather than a written explanation. The last prompt asks the reader to say why, which is goal 1 verbatim.",
 "It costs a small state machine (detect seed, detect false positive, detect hover) and a second column that has to collapse under the strip on phones. It also nudges toward one path, so the discovery is less the reader's own than in design 1.",
 "Nothing Decided is broken. D5 and D7's spirit (discovery is the reader's) is softened; the panel is skippable so goal 2 holds.",
 ["Skip the tour, then run the full reviewer path. Everything works without the panel.",
  "Each prompt ticks only on the real event: prompt 3 must not tick on a \"Definitely not\" result.",
  "375 wide: the panel sits under the strip, and the strip is still above the fold.",
  "Reader test comparing design 1 and design 8 with one person each: record both answers verbatim.",
  "Facts: same two as design 1. Prompts are instructions, not claims."],
 dict(prose="1 para + 5 prompts", facts=2, verify="Low", sixty="Yes (skippable)", scale="Good, prompts per concept", cost="Borderline (+20 min)", hit="High"))

# ---------- write ----------
os.makedirs(OUT, exist_ok=True)
for slug, d in D.items():
    folder = os.path.join(OUT, slug); os.makedirs(folder, exist_ok=True)
    for fn, html in d["files"].items():
        open(os.path.join(folder, fn), "w").write(html)
    open(os.path.join(folder, "README.md"), "w").write(textwrap.dedent(f"""\
    # {d['title']}

    Screens: {", ".join(d['files'].keys())}

    ## Rationale
    {d['rationale']}

    ## Main trade-off
    {d['tradeoff']}

    ## Spec lines this design bends
    {d['bends']}

    ## For a second concept
    {d['meta']['scale']}. See checks.md for the dry run.
    """))
    open(os.path.join(folder, "checks.md"), "w").write("# Checks for " + d["title"] + "\n\nRun before this design is called finished. Each line is pass/fail.\n\n" + "".join(f"- [ ] {c}\n" for c in d["checks"]))

rows = "\n".join(f"| {i+1} | [{d['title']}]({slug}/README.md) | {d['meta']['prose']} | {d['meta']['facts']} | {d['meta']['verify']} | {d['meta']['sixty']} | {d['meta']['hit']} | {d['meta']['scale']} | {d['meta']['cost']} |" for i,(slug,d) in enumerate(D.items()))
open(os.path.join(OUT, "README.md"), "w").write(f"""# Design explorations: Bloom filter explainer

Eight low-fidelity layouts. Each folder has the screens as HTML, a README with rationale, trade-off and the spec lines it bends, and a checks.md. Wireframes are deliberately grey; the only color is the bulbs, because the bulbs are the subject. The playground in every screen is static, not functional, so these compare layout and not behavior.

Every design was generated from one script (`gen_designs.py`) so the strip, word list and boxes are identical across them and the differences you see are the differences that matter.

## Comparison

"How hard to verify" counts the factual sentences the layout invites and rates the cost of sourcing them under the facts rule (section 8 of the spec). "Hit" is my estimate of how many generalists leave able to say why the false positive happened; it is a judgment, and the reader test in the definition of done is what actually measures it.

| # | Design | Prose | Claims | Hard to verify | 60 s path | Hit on goal 1 | Second concept | Build in 2 h |
|---|---|---|---|---|---|---|---|---|
{rows}

## Observations

- Verification cost tracks prose almost linearly. Designs 2 and 6 are the only ones that reach double-digit claims, and both do it in a "where it's used today" section. That section is where the facts rule bites, because those claims go stale silently.
- Design 4 is a landing for a site that does not exist yet. Design 3 was in the same bucket until it was rebuilt around a fixed list where no input can fail; that turns the search box from theatre into a real front door, at the cost of three extra states.
- Design 5 is the argument for D9 and D10. Written down it sounds like a nice metaphor; drawn, the bouncer plainly "remembers" things, and that is the one wrong idea the page must not plant.
- Designs 1, 7 and 8 are the same explainer at three levels of scaffolding: none, one sentence, five prompts. The spec's recorded risk (bulbs-only may leave generalists with a light show and no insight) is what separates them.

## Recommendation

Take design 1 as the explainer, and the revised design 3 as the landing (your call on 2026-09-04: free text, decided on device against a fixed list, no input can fail). Design 1 is inside every Decided line and carries exactly two claims. Design 3's landing costs about 15 minutes more than a card list and buys a front door that already behaves like a site with many concepts.

Take design 8 as the second one to develop. It is design 1 plus a skippable side panel, so the two share almost all of their code, and it directly hedges the one risk the spec logged against D7. The reader test in the definition of done can then be run once per design with one person each, and the verbatim answers decide which ships.

Not taken further: 2 and 6 (prose-first, over budget, expensive to verify), 4 (a catalog is right at concept three, not today), 5 (breaks D9 and D10 for a metaphor that teaches the wrong model), 7 (drops the one framing sentence and the landing, and the empty-on-load state gives a cold reviewer nothing to grab).

## What is still a guess

The "Hit" column. Nothing here has been shown to a reader. The two designs taken forward are chosen so that the first reader test compares them directly.
""")
print("\n".join(sorted(os.path.join(dp, f) for dp,_,fs in os.walk(OUT) for f in fs)))
