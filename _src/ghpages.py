"""Turn build.py's flat dist/ into the GitHub Pages tree the site is indexed as.

Two jobs, and both matter:
  1. services.html -> services/index.html, so the live URL is /services/ with the slash.
  2. every internal link, canonical, og:url and sitemap <loc> gets that same trailing slash.

Google has these pages in its index WITH the slash. Deploying without this step
rewrites every canonical to a slash-less URL and points them at addresses Google
does not have. That happened once, on 12 October, and was caught before the commit.

vercel.json is dropped: the site is on GitHub Pages, not Vercel.
The old Wix redirect folders (about-6, book-online, home, team-3, visit-us-1)
live only in the repo and are never touched from here.
"""
import os, re, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "dist"
DST = sys.argv[2] if len(sys.argv) > 2 else "stage"

SITE = "https://www.antisystem.com.au"
# Pages that become folders. index.html and 404.html stay at the root.
SLUGS = ["services", "about", "visit",
         "mens-haircut-bondi", "skin-fade-bondi", "italian-shave-bondi", "kids-haircut-bondi"]
DROP = {"vercel.json"}


def slashify(text):
    for slug in SLUGS:
        text = text.replace('href="/%s"' % slug, 'href="/%s/"' % slug)
        text = text.replace('%s/%s"' % (SITE, slug), '%s/%s/"' % (SITE, slug))
        text = text.replace('<loc>%s/%s</loc>' % (SITE, slug), '<loc>%s/%s/</loc>' % (SITE, slug))
    return text


if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(DST)

for name in sorted(os.listdir(SRC)):
    path = os.path.join(SRC, name)
    if name in DROP:
        continue
    if os.path.isdir(path):
        shutil.copytree(path, os.path.join(DST, name))
        continue

    stem, ext = os.path.splitext(name)
    if ext in (".html", ".xml", ".txt"):
        text = slashify(open(path, encoding="utf-8").read())
        if ext == ".html" and stem in SLUGS:
            os.makedirs(os.path.join(DST, stem), exist_ok=True)
            out = os.path.join(DST, stem, "index.html")
        else:
            out = os.path.join(DST, name)
        open(out, "w", encoding="utf-8").write(text)
    else:
        shutil.copy2(path, os.path.join(DST, name))

# Nothing may leave here still pointing at a slash-less page URL.
bad = []
for root, _dirs, files in os.walk(DST):
    for f in files:
        if not f.endswith((".html", ".xml", ".txt")):
            continue
        body = open(os.path.join(root, f), encoding="utf-8").read()
        for slug in SLUGS:
            if 'href="/%s"' % slug in body or '%s/%s"' % (SITE, slug) in body:
                bad.append((os.path.join(root, f), slug))
if bad:
    raise SystemExit("slash-less links survived: %r" % bad[:5])

print("staged ->", DST)
