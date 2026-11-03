import json, os, shutil, sys, base64, mimetypes

INLINE = "--inline" in sys.argv
OUT = "preview" if INLINE else "dist"

SITE = "https://www.antisystem.com.au"
BOOK = "https://www.fresha.com/a/antisystem-barbershop-bondi-beach-124b-roscoe-st-eo3zz9kd/all-offer?venue=true"
FRESHA = "https://www.fresha.com/a/antisystem-barbershop-bondi-beach-124b-roscoe-st-eo3zz9kd"
IG = "https://www.instagram.com/antisystem_barbershop/"
TT = "https://www.tiktok.com/@antisystembarbershop"
MAPS = "https://www.google.com/maps/search/?api=1&query=Antisystem%20Barbershop%2C%20124B%20Roscoe%20St%2C%20Bondi%20Beach%20NSW%202026"
PHONE = "0452 137 237"
TEL = "+61452137237"
EMAIL = "andrea@antisystem.com.au"
LASTMOD = "2026-10-06"

HOURS = [("Monday", "12pm – 7pm"), ("Tuesday", "9am – 7pm"), ("Wednesday", "9am – 7pm"),
         ("Thursday", "9am – 7pm"), ("Friday", "9am – 7pm"), ("Saturday", "8am – 4pm"), ("Sunday", "Closed")]

SERVICES = [
    ("Hair", [("Men's Cut", "30 min", 66, "/mens-haircut-bondi"), ("Restyle", "45 min", 80, "/mens-haircut-bondi"),
              ("Skin fade only", "30 min", 55, "/skin-fade-bondi"), ("Buzz cut", "20 min", 40, "/mens-haircut-bondi"),
              ("Under 18 Cuts", "30 min", 50, "/kids-haircut-bondi")]),
    ("Beard", [("Beard Trim", "15 min", 35, "/italian-shave-bondi"),
               ("The Italian beard trim with shave", "30 min", 65, "/italian-shave-bondi")]),
    ("Combo", [("Men's Cut + Beard Trim", "45 min", 90, "/mens-haircut-bondi")]),
]

def offer_catalog():
    """The real menu, machine-readable, from the same table the pages are built from."""
    return {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
        {"@type": "Offer", "price": str(price), "priceCurrency": "AUD", "url": BOOK,
         "availability": "https://schema.org/InStock",
         "itemOffered": {"@type": "Service", "name": name, "serviceType": "Barber",
                         "provider": {"@id": SITE + "/#business"}}}
        for _, rows in SERVICES for name, _dur, price, _path in rows]}


BUSINESS = {
    # BarberShop is the narrower schema.org type and matches the Google category.
    "@context": "https://schema.org", "@type": "BarberShop", "@id": SITE + "/#business",
    "name": "Antisystem Barbershop", "alternateName": "Antisystem",
    "description": "Italian barbershop in Bondi Beach. Men's cuts, skin fades, beard trims and the Italian beard trim with shave on Roscoe Street.",
    "url": SITE + "/", "telephone": TEL, "email": EMAIL, "priceRange": "$$",
    "address": {"@type": "PostalAddress", "streetAddress": "124B Roscoe St", "addressLocality": "Bondi Beach",
                "addressRegion": "NSW", "postalCode": "2026", "addressCountry": "AU"},
    # Same coordinates as the pin on Google and Apple, to the metre.
    "geo": {"@type": "GeoCoordinates", "latitude": -33.8899213, "longitude": 151.2741044},
    "areaServed": [{"@type": "Place", "name": "Bondi Beach"}, {"@type": "Place", "name": "Bondi"},
                   {"@type": "Place", "name": "North Bondi"}, {"@type": "Place", "name": "Bondi Junction"},
                   {"@type": "Place", "name": "Tamarama"}, {"@type": "Place", "name": "Bronte"}],
    "currenciesAccepted": "AUD",
    "paymentAccepted": "Cash, Credit Card, Debit Card, Mobile payments",
    "publicAccess": True,
    "hasMap": MAPS,
    # The shopfront leads: it is the one image that lets somebody on Roscoe St
    # recognise the door they are standing in front of.
    "image": [SITE + "/img/og.jpg", SITE + "/img/shop-front-960.webp",
              SITE + "/img/shop-wide-940.webp", SITE + "/img/shop-chair-900.webp",
              SITE + "/img/work-design-leaf-960.webp"],
    "logo": SITE + "/img/logo-1600.png",
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "12:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "16:00"}],
    "award": "Waverley Council Brightest and Best Business Awards",
    "founder": {"@type": "Person", "name": "Andrea"},
    "sameAs": [IG, TT, FRESHA],
}
# No aggregateRating here on purpose: Google requires the ratings it marks up to be
# visible on the same page, and inventing one risks a manual action on the whole site.
BUSINESS["hasOfferCatalog"] = offer_catalog()


def img(name):
    if INLINE:
        mt = mimetypes.guess_type(name)[0] or "image/webp"
        return "data:%s;base64,%s" % (mt, base64.b64encode(open("img/" + name, "rb").read()).decode())
    return "/img/" + name


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


CSS = r"""
/* Layout: black ground, the white wordmark is the only bright object; deep-green panels echo the shop wall */
:root{
  --ink:#0A0A0A; --surface:#131313; --verde:#16291B; --verde-2:#1E3A25;
  --paper:#F3F1EC; --muted:#8E8B85; --line:rgba(243,241,236,.14);
  --tri-g:#0BA32B; --tri-r:#EC0E10;
  --display:"Saira","Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --font:"Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --ease:cubic-bezier(.16,.84,.2,1);
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 70px);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ink);color:var(--paper);font:400 1.0625rem/1.6 var(--font);letter-spacing:-.005em;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--tri-r);outline-offset:4px;border-radius:3px}
.wrap{width:100%;max-width:1140px;margin:0 auto;padding:0 clamp(1.25rem,4vw,2.5rem)}
.wide{max-width:1340px}
.center{text-align:center}
.skip{position:absolute;left:-999px;top:0;background:var(--paper);color:var(--ink);padding:.6rem 1rem;z-index:99}
.skip:focus{left:1rem;top:1rem}
p{margin:0 0 1em;max-width:58ch}
.center p{margin-left:auto;margin-right:auto}
.muted{color:var(--muted)}

/* nav */
.gnav{position:sticky;top:0;z-index:30;background:rgba(10,10,10,.82);backdrop-filter:saturate(180%) blur(18px);-webkit-backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(243,241,236,.07)}
.gnav .wrap{display:flex;align-items:center;gap:2rem;min-height:64px;max-width:1340px}
.gnav .brand{margin-right:auto;display:block;line-height:0}
.gnav .brand img{width:clamp(130px,17vw,178px)}
.gnav nav{display:flex;gap:2rem;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase}
.gnav nav a{color:var(--muted);transition:color .2s}
.gnav nav a:hover,.gnav nav a[aria-current="page"]{color:var(--paper)}
@media (max-width:760px){.gnav .wrap{flex-wrap:wrap;gap:0 1rem;padding-top:.6rem;min-height:0}.gnav nav{order:3;width:100%;overflow-x:auto;white-space:nowrap;padding:.6rem 0 .7rem;gap:1.4rem;scrollbar-width:none}.gnav nav::-webkit-scrollbar{display:none}}

/* buttons */
.pill{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:.85rem 1.8rem;border-radius:999px;background:var(--paper);color:var(--ink);font-weight:600;font-size:.95rem;letter-spacing:.01em;transition:background .25s,color .25s,transform .25s var(--ease)}
.pill:hover{background:#fff;transform:translateY(-1px)}
.gnav .pill{min-height:36px;padding:.4rem 1.1rem;font-size:.8rem}
.more{font-weight:600;font-size:.95rem;display:inline-flex;align-items:center;gap:.4rem;color:var(--paper)}
.more::after{content:"";width:.42em;height:.42em;border-right:1.6px solid currentColor;border-top:1.6px solid currentColor;transform:rotate(45deg);transition:transform .25s var(--ease)}
.more:hover::after{transform:translateX(3px) rotate(45deg)}
.actions{display:flex;flex-wrap:wrap;gap:1rem 1.75rem;align-items:center}
.center .actions{justify-content:center}

/* type */
h1,h2,h3{margin:0;line-height:1.04;font-weight:500}
.display{font:500 clamp(2.1rem,5.4vw,4.4rem)/1.02 var(--display);text-transform:uppercase;letter-spacing:.04em}
.h2{font:500 clamp(1.9rem,4.4vw,3.4rem)/1.05 var(--display);text-transform:uppercase;letter-spacing:.05em}
.h3{font:500 clamp(1.25rem,2.2vw,1.75rem)/1.15 var(--display);text-transform:uppercase;letter-spacing:.05em}
.sub{font-size:clamp(1.02rem,1.6vw,1.2rem);font-weight:400;line-height:1.5;color:var(--muted);margin:1.2rem 0 0;max-width:40ch}
.center .sub{margin-left:auto;margin-right:auto}
.tag{display:inline-flex;align-items:center;gap:.6rem;font-size:.74rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:1.4rem}
.tag::before{content:"";width:26px;height:2px;background:linear-gradient(90deg,var(--tri-g) 0 33.3%,var(--paper) 33.3% 66.6%,var(--tri-r) 66.6%)}

/* sections */
.sec{padding:clamp(4.5rem,10vw,8.5rem) 0}
.green{background:var(--verde)}
.surface{background:var(--surface)}
.status{margin:1.1rem 0 0;font-size:.9rem;color:var(--muted)}
.status b{color:var(--paper);font-weight:600}
.status b::before{content:"";display:inline-block;width:.46em;height:.46em;border-radius:50%;background:var(--tri-g);margin-right:.5em;vertical-align:.1em}
.status.closed b::before{background:var(--tri-r)}

@media (prefers-reduced-motion:no-preference){
 .rv{opacity:0;transform:translateY(26px);transition:opacity 1s var(--ease),transform 1s var(--ease)}
 .rv.in{opacity:1;transform:none}
 .rv.d1{transition-delay:.1s}.rv.d2{transition-delay:.2s}.rv.d3{transition-delay:.3s}
}

/* hero */
.hero{padding:clamp(3.5rem,9vw,7rem) 0 clamp(3rem,7vw,5rem);text-align:center;position:relative;overflow:hidden}
.hero .mark{width:min(84vw,860px);margin:0 auto}
.hero .mark img{width:100%}
.hero .pay{margin-top:clamp(1.75rem,4vw,2.5rem);font:500 clamp(.95rem,2vw,1.3rem)/1.4 var(--display);text-transform:uppercase;letter-spacing:.22em;color:var(--paper)}
.hero p{margin-left:auto;margin-right:auto}
.hero .actions{margin-top:2.25rem;justify-content:center}
.hero .glow{position:absolute;left:50%;top:38%;width:min(120vw,1100px);aspect-ratio:2/1;transform:translate(-50%,-50%);background:radial-gradient(ellipse,rgba(243,241,236,.07),transparent 65%);pointer-events:none}
@media (prefers-reduced-motion:no-preference){
 .hero .mark{animation:markin 1.4s var(--ease) both}
 @keyframes markin{from{opacity:0;transform:translateY(18px) scale(.97);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
 .hero .pay,.hero .actions,.hero .status{animation:fade .9s var(--ease) both}
 .hero .pay{animation-delay:.5s}.hero .actions{animation-delay:.65s}.hero .status{animation-delay:.75s}
 @keyframes fade{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
}

/* tricolore rule */
.tri{height:2px;background:linear-gradient(90deg,var(--tri-g) 0 33.33%,var(--paper) 33.33% 66.66%,var(--tri-r) 66.66%);transform-origin:left}
@media (prefers-reduced-motion:no-preference){.tri{transform:scaleX(0);transition:transform 1.5s var(--ease)}.tri.in{transform:scaleX(1)}}

/* manifesto band */
.band{overflow:hidden;padding:clamp(3.5rem,8vw,6.5rem) 0;background:var(--ink)}
.band .big{font:500 clamp(2.4rem,8vw,7rem)/1.08 var(--display);text-transform:uppercase;letter-spacing:.04em;white-space:nowrap;will-change:transform;display:flex;gap:.6em}
.band .big span{display:inline-flex;align-items:center;gap:.6em;flex:none}
.band .big i{width:.14em;height:.14em;border-radius:50%;background:var(--tri-r);flex:none}
.band .big.b{color:transparent;-webkit-text-stroke:1px rgba(243,241,236,.5)}
.band .big.b i{background:var(--tri-g)}
.band p{margin:clamp(2rem,4vw,3rem) auto 0;text-align:center;max-width:46ch}

/* shop zoom */
.zoom{position:relative;height:200vh;background:var(--ink)}
.zoom-stick{position:sticky;top:64px;height:calc(100vh - 64px);display:grid;place-items:center;overflow:hidden}
.zoom-frame{position:relative;width:100%;height:100%;overflow:hidden;will-change:clip-path}
.zoom-frame img{width:100%;height:100%;object-fit:cover}
.zoom-cap{position:absolute;left:0;right:0;bottom:0;padding:clamp(1.5rem,4vw,3rem) 0;background:linear-gradient(0deg,rgba(0,0,0,.78),transparent);opacity:0;transition:opacity .6s}
.zoom-cap.on{opacity:1}
@media (max-width:860px),(prefers-reduced-motion:reduce){.zoom{height:auto}.zoom-stick{position:static;height:auto}.zoom-frame{height:auto;aspect-ratio:4/5;clip-path:none!important}.zoom-cap{opacity:1}}

/* services */
.svc{list-style:none;margin:clamp(2.5rem,5vw,3.5rem) 0 0;padding:0;border-top:1px solid var(--line)}
.svc li{border-bottom:1px solid var(--line)}
.svc a{display:grid;grid-template-columns:1fr auto 5.5rem;gap:1.5rem;align-items:center;padding:1.4rem 0;transition:padding .4s var(--ease),background .3s}
.svc .nm{font:500 clamp(1.1rem,2.2vw,1.6rem)/1.15 var(--display);text-transform:uppercase;letter-spacing:.05em}
.svc .tm{font-size:.85rem;color:var(--muted);letter-spacing:.02em}
.svc .pr{font:500 1.25rem/1 var(--display);text-align:right;letter-spacing:.02em}
.svc .pr.ask{font:600 .8rem/1.2 var(--font);color:var(--muted);letter-spacing:.04em}
.svc a:hover{padding-left:1rem;padding-right:1rem;background:var(--verde)}
@media (max-width:580px){.svc a{grid-template-columns:1fr auto}.svc .tm{grid-row:2;grid-column:1}}

/* numbers */
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.nums div{background:var(--verde);padding:clamp(1.75rem,3.5vw,2.75rem)}
.nums strong{display:block;font:500 clamp(2.4rem,6vw,4.4rem)/1 var(--display);letter-spacing:.02em}
.nums span{display:block;margin-top:.7rem;font-size:.88rem;color:rgba(243,241,236,.6);max-width:24ch}
@media (max-width:760px){.nums{grid-template-columns:1fr}}

/* reviews */
.rq{display:grid;min-height:12rem;margin-top:1rem}
.rq blockquote{grid-area:1/1;margin:0;opacity:0;transform:translateY(14px);transition:opacity .8s var(--ease),transform .8s var(--ease);pointer-events:none}
.rq blockquote.on{opacity:1;transform:none;pointer-events:auto}
.rq p{font:500 clamp(1.5rem,4vw,3rem)/1.12 var(--display);text-transform:uppercase;letter-spacing:.03em;max-width:21ch;margin:0 auto 1.5rem}
.rq cite{font-style:normal;font-size:.85rem;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.rq-dots{display:flex;gap:.45rem;justify-content:center;margin-top:1.75rem}
.rq-dots button{width:34px;height:18px;border:0;padding:0;background:transparent;cursor:pointer;position:relative}
.rq-dots button::before{content:"";position:absolute;left:0;right:0;top:8px;height:2px;background:rgba(243,241,236,.25)}
.rq-dots button.on::before{background:var(--paper)}

/* team */
.team{list-style:none;margin:clamp(2.5rem,5vw,3.5rem) 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.team li{background:var(--ink);padding:2.25rem 1.5rem;text-align:center}
.team .face{width:clamp(130px,16vw,168px);height:clamp(130px,16vw,168px);border-radius:50%;margin:0 auto 1.3rem;object-fit:cover;background:var(--verde);outline:1px solid var(--line);outline-offset:4px}
.team .who{display:block;font:500 1.35rem/1.1 var(--display);text-transform:uppercase;letter-spacing:.06em}
.team .role{display:block;color:var(--muted);font-size:.88rem;margin-top:.45rem}
@media (max-width:760px){.team{grid-template-columns:1fr}}

/* work gallery */
.work-rail{margin-top:clamp(2.25rem,5vw,3.25rem);display:flex;gap:clamp(.6rem,1.4vw,1rem);overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:0 clamp(1.25rem,4vw,2.5rem)}
.work-rail::-webkit-scrollbar{display:none}
.work-rail figure{flex:0 0 clamp(16rem,26vw,22rem);margin:0;scroll-snap-align:center;position:relative;overflow:hidden;background:var(--surface)}
.work-rail img{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;transition:transform .9s var(--ease);filter:saturate(.92)}
.work-rail figure:hover img{transform:scale(1.04)}
.work-rail figcaption{position:absolute;left:0;right:0;bottom:0;padding:2.5rem .95rem .9rem;font-size:.74rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;background:linear-gradient(0deg,rgba(0,0,0,.8),transparent)}
.work-hint{display:flex;align-items:center;gap:.6rem;margin:1.4rem 0 0;font-size:.74rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.work-hint::after{content:"";width:34px;height:2px;background:linear-gradient(90deg,var(--tri-g) 0 33.3%,var(--paper) 33.3% 66.6%,var(--tri-r) 66.6%)}
@media (max-width:580px){.work-rail figure{flex-basis:76vw}}

/* service page shot */
.shot{margin:0;background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:grid;place-items:center;padding:clamp(2rem,5vw,4rem) clamp(1.25rem,4vw,2.5rem)}
.shot img{display:block;width:100%;max-width:30rem;height:auto;aspect-ratio:3/4;object-fit:cover;filter:saturate(.92)}

/* visit */
.v-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,6vw,5rem);margin-top:clamp(2.5rem,5vw,3.5rem)}
@media (max-width:760px){.v-grid{grid-template-columns:1fr}}
.addr{font:500 clamp(1.5rem,3.2vw,2.2rem)/1.15 var(--display);text-transform:uppercase;letter-spacing:.04em;font-style:normal;margin:.4rem 0 1.4rem}
.hours{width:100%;border-collapse:collapse}
.hours caption{text-align:left;font-size:.74rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-bottom:.75rem}
.hours th,.hours td{padding:.7rem 0;border-bottom:1px solid var(--line);font-weight:400;text-align:left;font-size:.98rem}
.hours td{text-align:right;font-variant-numeric:tabular-nums}
.hours tr:last-child th,.hours tr:last-child td{border-bottom:0}
.hours tr.today th,.hours tr.today td{font-weight:700}
.hours tr.today th::after{content:"Today";margin-left:.6rem;font-size:.65rem;font-weight:700;letter-spacing:.08em;background:var(--paper);color:var(--ink);border-radius:999px;padding:.18rem .5rem;vertical-align:.18em}
.chips{list-style:none;padding:0;margin:1.5rem 0 0;display:flex;flex-wrap:wrap;gap:.5rem}
.center .chips{justify-content:center}
.chips li{border:1px solid var(--line);border-radius:999px;padding:.4rem .95rem;font-size:.85rem;color:var(--muted)}

/* price list page */
.list{border-top:1px solid var(--line);margin-top:clamp(2rem,4vw,3rem)}
.list h3{font-size:.74rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin:2.25rem 0 .5rem;font-family:var(--font)}
.list ul{list-style:none;margin:0;padding:0}
.list li{display:grid;grid-template-columns:1fr auto auto;gap:1.25rem;align-items:center;padding:1.1rem 0;border-bottom:1px solid var(--line)}
.list .n{font:500 1.15rem/1.2 var(--display);text-transform:uppercase;letter-spacing:.04em}
.list .t{color:var(--muted);font-size:.85rem}
.list .p{font:500 1.15rem/1 var(--display);text-align:right}
.list .ask{font-size:.82rem;font-weight:600;color:var(--muted)}
@media (max-width:580px){.list li{grid-template-columns:1fr auto}.list .t{grid-row:2;grid-column:1}}

/* subpages */
.crumbs{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding-top:1.5rem}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}
.crumbs li+li::before{content:"/";margin-right:.5rem;opacity:.5}
.spec{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin:clamp(2.5rem,5vw,3.5rem) auto 0;max-width:720px}
.spec div{background:var(--verde);padding:1.5rem}
.spec dt{color:rgba(243,241,236,.6);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase}
.spec dd{margin:.5rem 0 0;font:500 clamp(1.5rem,3vw,2.1rem)/1.05 var(--display);letter-spacing:.03em}
.faq details{border-bottom:1px solid var(--line)}
.faq details:last-child{border-bottom:0}
.faq summary{cursor:pointer;list-style:none;padding:1.2rem 2.2rem 1.2rem 0;font:500 1.05rem/1.3 var(--display);text-transform:uppercase;letter-spacing:.04em;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:0;top:1rem;font:300 1.5rem/1 var(--font);color:var(--muted);transition:transform .3s var(--ease)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{color:var(--muted);padding-bottom:1.2rem;margin:0;font-size:.98rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,6vw,4.5rem)}
@media (max-width:860px){.two{grid-template-columns:1fr}}

/* big cta */
.bigcta{display:inline-block;font:500 clamp(2rem,7vw,6rem)/1 var(--display);text-transform:uppercase;letter-spacing:.05em;position:relative;padding-bottom:.12em}
.bigcta::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--tri-g) 0 33.3%,var(--paper) 33.3% 66.6%,var(--tri-r) 66.6%);transform:scaleX(0);transform-origin:left;transition:transform .9s var(--ease)}
.bigcta:hover::after,.bigcta.in::after{transform:scaleX(1)}

/* footer */
.foot{background:var(--ink);border-top:1px solid var(--line);color:var(--muted);font-size:.85rem;line-height:1.7}
.foot .wrap{padding-top:3.5rem;padding-bottom:2.5rem;max-width:1340px}
.foot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:2.5rem;padding-bottom:2rem;border-bottom:1px solid var(--line)}
.foot .fmark{width:150px;margin-bottom:1.25rem}
.foot h4{margin:0 0 .8rem;font-size:.72rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--paper)}
.foot ul{list-style:none;margin:0;padding:0}
.foot li{padding:.2rem 0}
.foot a:hover{color:var(--paper)}
.foot .legal{padding-top:1.5rem;margin:0;max-width:none;font-size:.78rem}
@media (max-width:760px){.foot .cols{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
 var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
 try{
  var parts=new Intl.DateTimeFormat('en-AU',{timeZone:'Australia/Sydney',weekday:'long',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());
  var get=function(t){for(var i=0;i<parts.length;i++){if(parts[i].type===t)return parts[i].value}return''};
  var day=get('weekday'),mins=(parseInt(get('hour'),10)%24)*60+parseInt(get('minute'),10);
  var H={Monday:[720,1140],Tuesday:[540,1140],Wednesday:[540,1140],Thursday:[540,1140],Friday:[540,1140],Saturday:[480,960],Sunday:null};
  var order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
  var fmt=function(m){var h=Math.floor(m/60),mm=m%60,s=h>=12?'pm':'am',h12=h%12||12;return h12+(mm?':'+(mm<10?'0':'')+mm:'')+s};
  document.querySelectorAll('.hours tr[data-day="'+day+'"]').forEach(function(r){r.classList.add('today')});
  var msg,open=false,t=H[day];
  if(t&&mins>=t[0]&&mins<t[1]){msg='<b>Open now</b> until '+fmt(t[1])+' today.';open=true}
  else if(t&&mins<t[0]){msg='<b>Closed now.</b> Opens '+fmt(t[0])+' today.'}
  else{var i=order.indexOf(day);for(var k=1;k<=7;k++){var d=order[(i+k)%7];if(H[d]){msg='<b>Closed now.</b> Opens '+fmt(H[d][0])+' '+(k===1?'tomorrow':d)+'.';break}}}
  document.querySelectorAll('[data-status]').forEach(function(el){el.innerHTML=msg;el.hidden=false;if(!open)el.classList.add('closed')});
 }catch(e){}

 var qs=document.querySelectorAll('.rq blockquote'),dots=document.querySelectorAll('.rq-dots button'),qi=0,qt;
 var show=function(i){qi=i;qs.forEach(function(q,k){q.classList.toggle('on',k===i)});dots.forEach(function(d,k){d.classList.toggle('on',k===i);d.setAttribute('aria-pressed',k===i?'true':'false')})};
 if(qs.length){show(0);dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);clearInterval(qt)})});if(!RM)qt=setInterval(function(){show((qi+1)%qs.length)},5000)}

 var run=function(el){var to=parseFloat(el.dataset.count),dec=(el.dataset.count.split('.')[1]||'').length,t0=null;
  if(RM){el.textContent=to.toFixed(dec);return}
  var step=function(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1500),e=1-Math.pow(1-p,4);el.textContent=(to*e).toFixed(dec);if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)};
 var targets=document.querySelectorAll('.rv,[data-count],.bigcta,.tri');
 if('IntersectionObserver' in window){var ob=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var el=e.target;if(el.dataset.count!==undefined)run(el);el.classList.add('in');ob.unobserve(el)})},{threshold:.2,rootMargin:'0px 0px -8% 0px'});
  targets.forEach(function(el){if(el.dataset.count!==undefined&&!RM)el.textContent='0';ob.observe(el)})}
 else targets.forEach(function(el){el.classList.add('in');if(el.dataset.count!==undefined)run(el)});
 if(RM)return;

 var rows=document.querySelectorAll('.band .big'),zoom=document.querySelector('.zoom'),frame=zoom&&zoom.querySelector('.zoom-frame'),cap=zoom&&zoom.querySelector('.zoom-cap'),tick=false;
 var wide=function(){return innerWidth>860};
 var f=function(){tick=false;var vh=innerHeight;
  rows.forEach(function(r){var b=r.parentNode.getBoundingClientRect(),p=(vh-b.top)/(vh+b.height),dir=r.classList.contains('b')?1:-1;r.style.transform='translate3d('+(dir*(p*22-11)+(dir>0?-16:3))+'%,0,0)'});
  if(zoom&&wide()){var r=zoom.getBoundingClientRect(),p=Math.max(0,Math.min(1,(64-r.top)/(r.height-(vh-64))));var e=Math.min(1,p/.7);var ix=(1-e)*20,iy=(1-e)*15,rad=(1-e)*10;frame.style.clipPath='inset('+iy+'% '+ix+'% '+iy+'% '+ix+'% round '+rad+'px)';cap.classList.toggle('on',p>.7)}
 };
 var on=function(){if(!tick){tick=true;requestAnimationFrame(f)}};
 addEventListener('scroll',on,{passive:true});addEventListener('resize',on);f();
})();
"""

NAV = [("/services", "Services"), ("/about", "The brand"), ("/visit", "Visit")]


def page(path, title, desc, body, schemas=(), current=None, noindex=False):
    canon = SITE + (path if path != "/" else "/")
    # a 404 is not a page to index, and canonicalising it to itself is noise
    head_extra = ('<meta name="robots" content="noindex">' if noindex
                  else f'<link rel="canonical" href="{canon}">')
    CUR = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in NAV)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                 for s in (BUSINESS,) + tuple(schemas))
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{head_extra}
<meta name="theme-color" content="#0A0A0A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Antisystem Barbershop">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="en_AU">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="{img('favicon-96.png')}" type="image/png" sizes="96x96">
<link rel="icon" href="{img('favicon-144.png')}" type="image/png" sizes="144x144">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Saira:wght@400;500;600&display=swap">
<style>{CSS}</style>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="gnav"><div class="wrap">
 <a class="brand" href="/"><img src="{img('logo-520.webp')}" width="520" height="82" alt="Antisystem Barber Shop"></a>
 <nav aria-label="Main">{nav}</nav>
 <a class="pill" href="{BOOK}" rel="noopener">Book</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
 <div class="cols">
  <div><img class="fmark" src="{img('logo-520.webp')}" width="520" height="82" alt="Antisystem Barber Shop" loading="lazy">
   <p style="margin:0">Italian barbershop in Bondi Beach.<br>La dolce vita meets rebellion.</p></div>
  <div><h4>Visit</h4><address style="font-style:normal">124B Roscoe St<br>Bondi Beach NSW 2026</address>
   <ul style="margin-top:.6rem"><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
   <li><a href="{IG}" rel="noopener">Instagram</a></li><li><a href="{TT}" rel="noopener">TikTok</a></li></ul></div>
  <div><h4>Services</h4><ul>
   <li><a href="/services">Services and prices</a></li><li><a href="/mens-haircut-bondi">Men's haircuts</a></li>
   <li><a href="/skin-fade-bondi">Skin fades</a></li><li><a href="/italian-shave-bondi">Beard trims and shave</a></li>
   <li><a href="/kids-haircut-bondi">Kids' haircuts</a></li></ul></div>
 </div>
 <p class="legal">© 2026 Antisystem Pty Ltd. Winner, Waverley Council Brightest and Best Business Awards.</p>
</div></footer>
<script>{JS}</script>
</body>
</html>
"""


def svc_rows():
    out = []
    for g, items in SERVICES:
        for name, time, price, link in items:
            pr = (f'<span class="pr">${price}</span>' if price is not None
                  else '<span class="pr ask">On Fresha</span>')
            out.append(f'<li><a href="{link or BOOK}"><span class="nm">{esc(name)}</span>'
                       f'<span class="tm">{time or ""}</span>{pr}</a></li>')
    return "".join(out)


def price_list():
    out = []
    for g, items in SERVICES:
        lis = []
        for name, time, price, link in items:
            n = f'<a href="{link}">{esc(name)}</a>' if link else esc(name)
            p = (f'<span class="p">${price}</span>' if price is not None
                 else f'<a class="ask" href="{BOOK}" rel="noopener">Price on Fresha</a>')
            lis.append(f'<li><span class="n">{n}</span><span class="t">{time or ""}</span>{p}</li>')
        out.append(f'<h3>{g}</h3><ul>{"".join(lis)}</ul>')
    return f'<div class="list">{"".join(out)}</div>'


def hours_table():
    rows = "".join(f'<tr data-day="{d}"><th scope="row">{d}</th><td>{h}</td></tr>' for d, h in HOURS)
    return f'<table class="hours"><caption>Opening hours</caption>{rows}</table>'


def marq(text, n):
    return "".join(f"<span>{text}<i></i></span>" for _ in range(n))


# Real client work, shot in the shop. (stem, alt, caption)
WORK = [
    ("work-design-leaf", "Skin fade with a freehand razor pattern cut into the side, Antisystem Bondi Beach", "Freehand design"),
    ("work-textured-back", "Textured mid-length men's cut, back view, Antisystem Bondi Beach", "Textured cut"),
    ("work-design-blonde", "Bleached blonde crop with a low fade and razor lines, Antisystem Bondi Beach", "Blonde + lines"),
    ("work-taper", "Flow haircut swept back and blended into the neckline, back view, Antisystem Bondi Beach", "Flow"),
    ("work-mullet", "Curly modern mullet with a short back and sides, Antisystem Bondi Beach", "Modern mullet"),
    ("work-flow-back", "Long flow haircut layered through the back and over the nape, Antisystem Bondi Beach", "Long flow"),
    ("work-crop-side", "Short crop with a sharp fringe line and skin fade, side view, Antisystem Bondi Beach", "Sharp crop"),
]


def rail():
    figs = []
    for stem, alt, cap in WORK:
        figs.append(
            f'<figure><img src="{img(stem + "-640.webp")}" '
            f'srcset="{img(stem + "-640.webp")} 640w, {img(stem + "-960.webp")} 960w" '
            f'sizes="(max-width:580px) 76vw, 22rem" width="640" height="853" '
            f'loading="lazy" decoding="async" alt="{esc(alt)}">'
            f'<figcaption>{esc(cap)}</figcaption></figure>')
    return f'<div class="work-rail">{"".join(figs)}</div>'


def shot(stem, alt):
    """Full-width photo band for a service page. Picks the largest rendition."""
    import glob
    sizes = sorted(int(f.rsplit("-", 1)[1].split(".")[0])
                   for f in glob.glob("img/%s-*.webp" % stem))
    if not sizes:
        raise SystemExit("no renditions for %s" % stem)
    big, small = sizes[-1], sizes[0]
    from PIL import Image
    w, h = Image.open("img/%s-%d.webp" % (stem, big)).size
    return (f'<figure class="shot"><img src="{img("%s-%d.webp" % (stem, small))}" '
            f'srcset="{img("%s-%d.webp" % (stem, small))} {small}w, '
            f'{img("%s-%d.webp" % (stem, big))} {big}w" sizes="100vw" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'alt="{esc(alt)}"></figure>')


def visit():
    return f"""
<section class="sec" id="visit" aria-labelledby="visit-h"><div class="wrap wide">
 <span class="tag">Visit</span><h2 id="visit-h" class="h2">Come say ciao.</h2>
 <div class="v-grid">
  <div>
   <address class="addr">124B Roscoe St<br>Bondi Beach NSW 2026</address>
   <p style="margin:0"><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
   <div class="actions" style="margin-top:2rem"><a class="pill" href="{BOOK}" rel="noopener">Book now</a><a class="more" href="{MAPS}" rel="noopener">Get directions</a></div>
  </div>
  <div>{hours_table()}<p class="status" data-status hidden></p></div>
 </div>
</div></section>"""


def cta():
    return f"""<section class="sec center" style="padding-top:clamp(3rem,6vw,5rem)"><div class="wrap wide">
 <a class="bigcta" href="{BOOK}" rel="noopener">Book your chair</a>
 <p class="muted" style="margin-top:1.75rem">Instant confirmation on Fresha, or call <a href="tel:{TEL}" style="text-decoration:underline">{PHONE}</a>.</p>
</div></section>"""


def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for t, h in items)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": SITE + h} if h else {})}
        for i, (t, h) in enumerate(items)]}
    return f'<nav class="crumbs wrap wide" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', schema


def faq_block(faqs):
    """Accordion plus the FAQPage schema, so the same answers can show in search."""
    html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    return html, schema


def service_schema(name, desc, path, price=None):
    s = {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "serviceType": "Barber",
         "url": SITE + path, "provider": {"@id": SITE + "/#business"},
         "areaServed": {"@type": "Place", "name": "Bondi Beach, Sydney"}}
    if price:
        s["offers"] = {"@type": "Offer", "price": str(price), "priceCurrency": "AUD", "url": BOOK}
    return s


BARBERS = [
    ("Gracie", "barber-gracie", "Barber and store manager"),
    ("Dave", "barber-dave", "Barber"),
    ("Andrea", "barber-andrea", "Founder and barber"),
]


def team():
    lis = []
    for who, stem, role in BARBERS:
        alt = "%s, %s at Antisystem Barbershop, Bondi Beach" % (who, role[0].lower() + role[1:])
        lis.append(
            f'<li><img class="face" src="{img(stem + "-320.webp")}" '
            f'srcset="{img(stem + "-320.webp")} 320w, {img(stem + "-560.webp")} 560w" '
            f'sizes="168px" width="320" height="320" loading="lazy" decoding="async" '
            f'alt="{esc(alt)}">'
            f'<span class="who">{who}</span><span class="role">{role}</span></li>')
    return '<ul class="team">%s</ul>' % "".join(lis)


TEAM = team()

PAGES = {}

# ---------------- HOME ----------------
PAGES["index.html"] = page("/", "Antisystem Barbershop | Italian Barber in Bondi Beach",
    "Italian barbershop on Roscoe St, Bondi Beach. Men's cuts, skin fades, beard trims and the Italian beard trim with shave. Rated 5.0 on Fresha. Book online.",
    f"""
<section class="hero">
 <span class="glow" aria-hidden="true"></span>
 <div class="wrap">
  <h1 class="mark"><img src="{img('logo-1600.webp')}" width="1600" height="253" alt="Antisystem Barber Shop" fetchpriority="high"></h1>
  <p class="pay">Italian barbershop · Bondi Beach</p>
  <div class="actions"><a class="pill" href="{BOOK}" rel="noopener">Book now</a><a class="more" href="/services">See services</a></div>
  <p class="status" data-status hidden></p>
 </div>
</section>
<div class="tri" aria-hidden="true"></div>

<section class="band" aria-label="Manifesto">
 <div class="big a" aria-hidden="true">{marq("Defy convention", 4)}</div>
 <div class="big b" aria-hidden="true">{marq("Embrace individuality", 4)}</div>
 <p class="muted rv">We're not just a barbershop. We're a movement. Passion, creativity and self-expression, the Italian way.</p>
</section>

<section class="zoom" aria-labelledby="shop-h"><div class="zoom-stick"><div class="zoom-frame">
 <img src="{img('shop-wide-940.webp')}" width="940" height="626" loading="lazy" alt="Inside Antisystem Barbershop on Roscoe St, Bondi Beach: black barber chairs, tools laid out and the street through the open shopfront">
 <div class="zoom-cap"><div class="wrap wide"><span class="tag">124B Roscoe St</span><h2 id="shop-h" class="h2">Step inside.</h2></div></div>
</div></div></section>

<section class="sec" aria-labelledby="work-h">
 <div class="wrap wide rv"><span class="tag">The work</span><h2 id="work-h" class="h2">Off the chair.</h2>
 <p class="sub">Fades, crops, length and freehand. Every one of these walked out of Roscoe St.</p></div>
 {rail()}
 <div class="wrap wide"><p class="work-hint">Swipe</p></div>
</section>

<section class="sec" aria-labelledby="svc-h"><div class="wrap wide">
 <div class="rv"><span class="tag">Services</span><h2 id="svc-h" class="h2">Pick your cut.</h2><p class="sub">Every service books in seconds on Fresha.</p></div>
 <ul class="svc rv d1">{svc_rows()}</ul>
 <div class="actions rv" style="margin-top:2.5rem"><a class="pill" href="{BOOK}" rel="noopener">Book now</a><a class="more" href="/services">Full menu</a></div>
</div></section>

<section class="sec" style="padding-top:0" aria-label="Antisystem in numbers"><div class="wrap wide">
 <div class="nums">
  <div class="rv"><strong data-count="5.0">5.0</strong><span>Rating on Fresha</span></div>
  <div class="rv d1"><strong data-count="349">349</strong><span>Five-star client reviews</span></div>
  <div class="rv d2"><strong>Winner</strong><span>Waverley Council Brightest and Best Business Awards</span></div>
 </div>
</div></section>

<section class="sec center surface" aria-labelledby="team-h"><div class="wrap wide">
 <div class="rv"><span class="tag">The team</span><h2 id="team-h" class="h2">The chairs.</h2><p class="sub">Pick your barber when you book.</p></div>
 <div class="rv d1">{TEAM}</div>
</div></section>

<section class="sec center" aria-label="Client reviews"><div class="wrap">
 <span class="tag">349 reviews, all five stars</span>
 <div class="rq">
  <blockquote><p>I'm booking a session with Gracie, not just a haircut.</p><cite>Gal S., on Fresha</cite></blockquote>
  <blockquote><p>Outstanding service every time</p><cite>Andre P., on Fresha</cite></blockquote>
  <blockquote><p>Dave is the absolute best</p><cite>Jenny M., on Fresha</cite></blockquote>
 </div>
 <div class="rq-dots"><button type="button" aria-label="Review 1"></button><button type="button" aria-label="Review 2"></button><button type="button" aria-label="Review 3"></button></div>
 <p style="margin-top:2rem"><a class="more" href="{FRESHA}" rel="noopener">Read every review</a></p>
</div></section>
{visit()}
{cta()}""")

# ---------------- SERVICES ----------------
nav_html, bc = crumbs([("Home", "/"), ("Services", None)])
svc_faq_html, svc_faq_schema = faq_block([
    ("Do I need to book, or can I walk in?",
     "Both work. Walk in and if a chair is free it is yours. Booking on Fresha just means you are not waiting, which matters on Saturdays and after five."),
    ("Can I choose my barber?",
     "Yes. Pick Gracie, Dave or Andrea when you book on Fresha, or ask at the counter if someone is free."),
    ("What should I book if I'm not sure?",
     "A Men's Cut, and tell your barber what you are after when you sit down. If it turns out you want a bigger change we will sort it from there."),
    ("Do you cut kids' hair?",
     "Yes, anyone under eighteen is the Under 18 Cut at $50. Booking the whole family at once works through group booking on Fresha."),
])
PAGES["services.html"] = page("/services", "Barber Services and Prices, Bondi Beach | Antisystem",
    "Men's Cut $66, Restyle $80, Skin fade $55, Buzz cut $40, Under 18 Cut $50, Beard Trim $35, Italian beard trim with shave $65 at Antisystem, Bondi Beach.",
    f"""{nav_html}
<section class="sec" style="padding-top:clamp(2.5rem,6vw,4rem)"><div class="wrap wide">
 <div class="center"><h1 class="display">Services and prices.</h1>
 <p class="sub">Cuts, fades, beards and the Italian beard trim with shave. Instant confirmation on Fresha.</p>
 <div class="actions" style="margin-top:2rem"><a class="pill" href="{BOOK}" rel="noopener">Book a service</a></div></div>
 {price_list()}
</div></section>
<section class="sec"><div class="wrap two">
 <div class="rv">
  <h2 class="h3">What each one is.</h2>
  <p><strong>Men's Cut — $66, thirty minutes.</strong> Your regular haircut done properly: a consultation first, then the cut, the finish and the style. The booking most people want.</p>
  <p><strong>Restyle — $80, forty-five minutes.</strong> For changing the shape rather than keeping it. Growing it out, going shorter, trying something you have not had before. The extra fifteen minutes is there so the conversation does not get rushed.</p>
  <p><strong>Skin fade only — $55, thirty minutes.</strong> The fade on its own: back and sides taken down to the skin and blended up into your length. If you want the top cut and styled as well, book a Men's Cut and tell your barber you want it faded.</p>
  <p><strong>Buzz cut — $40, twenty minutes.</strong> One grade all over, top and sides, no fade and no fuss.</p>
  <p><strong>Under 18 Cuts — $50, thirty minutes.</strong> Anyone under eighteen, from a first proper barbershop cut to a teenager who already knows exactly which fade he wants. Same chair, same barbers, same standard as every adult cut.</p>
  <p><strong>Beard Trim — $35, fifteen minutes.</strong> Clippers and scissors. Shaped and refined, lines cleaned up, kept in proportion with your face. No razor.</p>
  <p><strong>The Italian beard trim with shave — $65, thirty minutes.</strong> This is the razor booking, and it covers all of it: a <a href="/italian-shave-bondi" style="text-decoration:underline">hot towel shave</a>, a full straight razor shave, a razor head shave, or a razor finish on the cheeks and neck. One price whichever you pick.</p>
  <p><strong>Men's Cut + Beard Trim — $90, forty-five minutes.</strong> Both in one visit, which is cheaper and quicker than booking them separately.</p>
  <h2 class="h3">Walk in or book.</h2>
  <p>Walk-ins are welcome whenever there is a chair free, and on a quiet weekday morning there usually is. Saturdays and weekday evenings fill up, so if you are coming then, book. Instant confirmation on Fresha, or call {PHONE} and we will put you in.</p>
 </div>
 <div class="faq rv d1"><span class="tag">Questions</span>{svc_faq_html}</div>
</div></section>
{visit()}
{cta()}""", schemas=(bc, svc_faq_schema), current="/services")

# ---------------- ABOUT ----------------
nav_html, bc = crumbs([("Home", "/"), ("The brand", None)])
PAGES["about.html"] = page("/about", "The Brand | Antisystem Barbershop, Bondi Beach",
    "Antisystem is an Italian barbershop in Bondi Beach where la dolce vita meets rebellion. Meet the team and the story behind the brand.",
    f"""{nav_html}
<section class="sec center" style="padding-top:clamp(2.5rem,6vw,4rem)"><div class="wrap">
 <h1 class="display">La dolce vita<br>meets rebellion.</h1>
 <p class="sub">We bring the Italian vibe to Bondi Beach, with a barbershop built on individuality and defying convention.</p>
</div></section>
<div class="tri" aria-hidden="true"></div>
<section class="sec"><div class="wrap two">
 <div class="rv"><p>Antisystem is inspired by the Italian culture of passion, creativity and self-expression. We're not just a barbershop, we're a movement.</p>
 <p>At Antisystem, everyone feels good, and it's not only the haircuts and styling that make it happen. It's the collective vibe of people coming together to celebrate individuality, creativity and the joy of living life to the fullest.</p></div>
 <div class="rv d1"><span class="tag">Recognised locally</span><p class="muted">Winner of the Waverley Council Brightest and Best Business Awards, and rated 5.0 on Fresha from 349 client reviews.</p>
 <p style="margin-top:1.25rem"><a class="more" href="{FRESHA}" rel="noopener">Read the reviews</a></p></div>
</div></section>
<section class="sec center surface" style="padding-top:clamp(3rem,6vw,5rem)" aria-labelledby="team-h"><div class="wrap wide">
 <span class="tag">The team</span><h2 id="team-h" class="h2">The chairs.</h2><p class="sub">Pick your barber when you book on Fresha.</p>{TEAM}
</div></section>
{visit()}
{cta()}""", schemas=(bc,), current="/about")

# ---------------- VISIT ----------------
nav_html, bc = crumbs([("Home", "/"), ("Visit", None)])
visit_fq, visit_faq_schema = faq_block([
    ("Do you take walk-ins?",
     "Yes, whenever a chair is free. Booking on Fresha is the only way to be sure of a "
     "time and a barber, and Saturdays fill up, but you are welcome to come and ask."),
    ("Where exactly is the shop?",
     "124B Roscoe St, a few steps off Hall St in Bondi Beach. There is one step up at the "
     "door. Street parking on Roscoe and the surrounding streets, and the 333 and 380 stop "
     "on Campbell Parade, about four minutes away."),
    ("Can I bring my kids, or my dog?",
     "Both. Kids get the Under 18 Cut, and dogs are welcome to wait with you."),
    ("How do I pay?",
     "Card, phone or cash. You can also pay through Fresha when you book."),
])
PAGES["visit.html"] = page("/visit", "Visit Antisystem Barbershop | 124B Roscoe St, Bondi Beach",
    "Find Antisystem Barbershop at 124B Roscoe St, Bondi Beach NSW 2026. Walk-ins welcome when a chair is free. Open Mon 12–7, Tue–Fri 9–7, Sat 8–4.",
    f"""{nav_html}
<section class="sec center" style="padding-top:clamp(2.5rem,6vw,4rem);padding-bottom:clamp(2rem,4vw,3rem)"><div class="wrap">
 <h1 class="display">124B Roscoe St.<br>Bondi Beach.</h1>
 <p class="sub">Open six days. Closed Sundays. Walk-ins welcome when a chair is free.</p>
 <ul class="chips"><li>Walk-ins welcome</li><li>Near public transport</li><li>Street parking</li><li>Kid-friendly</li><li>Pet-friendly</li><li>Pay by app</li></ul>
</div></section>
{shot("shop-front", "The Antisystem Barbershop window on Roscoe St, Bondi Beach, with a barber at work inside")}
{visit()}
<section class="sec" style="padding-top:0"><div class="wrap">
 <div class="faq rv"><span class="tag">Questions</span>{visit_fq}</div>
</div></section>
{cta()}""", schemas=(bc, visit_faq_schema), current="/visit")


# ---------------- SERVICE PAGES ----------------
def svc(fname, path, title, desc, crumb, h1a, h1b, lede, spec, body, faqs, related, sname, sdesc, price, pic=None,
        faq_schema=False):
    nav_html, bc = crumbs([("Home", "/"), ("Services", "/services"), (crumb, None)])
    specs = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in spec)
    fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    rel = "".join(f'<li><a href="{h}"><span class="nm">{t}</span><span class="tm"></span><span class="pr ask">{s}</span></a></li>' for t, h, s in related)
    PAGES[fname] = page(path, title, desc, f"""{nav_html}
<section class="sec center" style="padding-top:clamp(2.5rem,6vw,4rem);padding-bottom:clamp(2rem,4vw,3rem)"><div class="wrap">
 <h1 class="display">{h1a}<br>{h1b}</h1>
 <p class="sub">{lede}</p>
 <div class="actions" style="margin-top:2rem"><a class="pill" href="{BOOK}" rel="noopener">Book on Fresha</a><a class="more" href="tel:{TEL}">Call {PHONE}</a></div>
 <dl class="spec">{specs}</dl>
</div></section>
{shot(*pic) if pic else '<div class="tri" aria-hidden="true"></div>'}
<section class="sec"><div class="wrap two">
 <div class="rv">{body}</div>
 <div class="faq rv d1"><span class="tag">Questions</span>{fq}</div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap wide">
 <h2 class="h2 center">More at Antisystem.</h2>
 <ul class="svc">{rel}</ul>
</div></section>
{visit()}
{cta()}""", schemas=((bc, service_schema(sname, sdesc, path, price), faq_block(faqs)[1]) if faq_schema
                     else (bc, service_schema(sname, sdesc, path, price))), current="/services")


svc("mens-haircut-bondi.html", "/mens-haircut-bondi", "Men's Haircut Bondi Beach | Antisystem Barbershop",
    "Men's cuts ($66) and restyles ($80) at Antisystem, an Italian barbershop on Roscoe St, Bondi Beach. Pick your barber and book online on Fresha.",
    "Men's haircuts", "Men's haircuts.", "Bondi Beach.",
    "Your regular cut kept sharp, or a new direction with time to get it right.",
    [("Men's Cut", "$66"), ("Restyle", "$80"), ("Buzz cut", "$40")],
    """<h2 class="h3">Which one to book.</h2>
<p><strong>Men's Cut.</strong> Your regular haircut, done properly: consultation, cut, finish and style. Thirty minutes.</p>
<p><strong>Restyle.</strong> For a change. Growing it out, going shorter, trying something new. Forty-five minutes to talk it through and reshape it.</p>
<p><strong>Buzz cut.</strong> One grade all over, top and sides, no fade. Twenty minutes.</p>
<p><strong>Men's Cut + Beard Trim.</strong> Both in one visit, forty-five minutes, $90.</p>""",
    [("Should I book a Men's Cut or a Restyle?", "Same shape tidied up: Men's Cut. Shape changing: Restyle, so there's time to do it right."),
     ("Can I choose my barber?", "Yes. Pick Gracie, Dave or Andrea when you book on Fresha."),
     ("How often should I get a haircut?", "Short styles and fades usually need a tidy every two to four weeks. Longer styles can go four to eight.")],
    [("Skin fade only", "/skin-fade-bondi", "$55"), ("Beard and shave", "/italian-shave-bondi", "From $35"), ("All services", "/services", "Full menu")],
    "Men's haircut", "Men's cuts and restyles at Antisystem Barbershop, Bondi Beach.", 66,
    pic=("work-flow-back", "Longer layered men's haircut finished at Antisystem Barbershop, Bondi Beach"))

svc("skin-fade-bondi.html", "/skin-fade-bondi", "Skin Fade Bondi Beach | Antisystem Barbershop",
    "Skin fades in Bondi Beach for $55. Taken down to the skin and blended clean at Antisystem Barbershop, 124B Roscoe St. Book online on Fresha.",
    "Skin fades", "Skin fades.", "Bondi Beach.",
    "Down to the skin, blended clean, sharp from every angle.",
    [("Price", "$55"), ("Time", "30 min")],
    """<h2 class="h3">The fade, on its own.</h2>
<p>This booking is the fade itself: taken down to the skin at the back and sides and blended up into your length.</p>
<p>Want the top cut and styled too? Book a <a href="/mens-haircut-bondi" style="text-decoration:underline">Men's Cut or a Restyle</a> and tell your barber you want it faded.</p>""",
    [("How long does a skin fade last?", "A fade grows out fast. Most clients come back every two to three weeks to keep the line clean."),
     ("Low, mid or high fade?", "Low starts just above the ear, mid around the temple, high near the crown. Not sure? Your barber will tell you what suits your head shape."),
     ("Can I choose my barber?", "Yes. Pick Gracie, Dave or Andrea when you book on Fresha.")],
    [("Men's haircuts", "/mens-haircut-bondi", "From $66"), ("Under 18 Cuts", "/kids-haircut-bondi", "$50"), ("All services", "/services", "Full menu")],
    "Skin fade", "Skin fade haircut at Antisystem Barbershop, Bondi Beach.", 55,
    pic=("work-crop-side", "Skin fade taken down to the skin at the side and blended up into the length, Antisystem Barbershop, Bondi Beach"))

svc("italian-shave-bondi.html", "/italian-shave-bondi", "Hot Towel Shave and Straight Razor, Bondi Beach | Antisystem",
    "Hot towel shave, straight razor shave and razor head shave in Bondi Beach, $65. Beard trim $35. Antisystem Barbershop, 124B Roscoe St. Book on Fresha.",
    "Shaves and beards", "Hot towel shaves", "and the straight razor.",
    "The towels, the blade, and thirty minutes where nobody needs anything from you. The Italian way, in Bondi Beach.",
    [("Shave", "$65"), ("Beard Trim", "$35"), ("Time", "15 or 30 min")],
    """<h2 class="h3">The razor work, by name.</h2>
<p>Every shave on this page is the same booking: <strong>The Italian beard trim with shave</strong>, thirty minutes, $65. You tell your barber which one you want when you sit down. One price, whichever you pick, and nobody is going to try to sell you something else.</p>

<h3>Hot towel shave — $65</h3>
<p>Hot towels first, to soften the beard and open up the skin. Then lather, then the razor, then a cold towel at the end to close everything back down. Thirty minutes flat on your back with a towel over your face. It is the oldest thing we do and still the best thing we do.</p>

<h3>Straight razor shave — $65</h3>
<p>A full face shave with the straight razor, free hand. With the grain first, then across it, the way you were taught if you were taught properly. Closer than any machine gets, and it holds for longer because of it.</p>

<h3>Razor head shave — $65</h3>
<p>Head taken to the skin with the blade, not the clippers. Hot towels, lather, razor, finished smooth. If you shave your own head in the shower you already know what the difference feels like.</p>

<h3>Razor finish on the beard — $65</h3>
<p>You keep the beard, the razor does the edges. Cheeks and neck taken clean and straight so the shape reads from across the room instead of fading out into stubble.</p>

<h2 class="h3">Or just the trim — $35</h2>
<p><strong>Beard Trim.</strong> Fifteen minutes, clippers and scissors, no razor and no towels. Shaped and refined, lines cleaned up, kept in proportion with your face. This is the one to book if you want maintenance rather than an experience.</p>
<p>Want the cut as well? <strong>Men's Cut + Beard Trim</strong> does both in one visit, forty-five minutes, $90.</p>

<h2 class="h3">How to book a shave.</h2>
<p>On Fresha there is one booking for all of the razor work, and it is called <strong>The Italian beard trim with shave</strong>. Pick it, pick your barber, and if you already know what you want, put it in the notes — hot towel, full face, head. If you would rather just say it in the chair, that works too.</p>
<p>Ask for the razor when you book and we will put you in the right chair for it.</p>

<h2 class="h3">Before a wedding.</h2>
<p>The morning of, or the day before. Not three days before — the point of a razor shave is that it is fresh. Book early for Saturdays, the first hour goes first. If there are a few of you, use group booking on Fresha and we will run the whole party through together.</p>

<h2 class="h3">Afterwards.</h2>
<p>Your skin stays warm for an hour or so. Leave it alone: nothing with alcohol in it, nothing heavily scented, and skip the gym that morning if you can. Most men get two to four days out of a razor shave before the shadow comes back, which is longer than you will get out of your own razor at home.</p>""",
    [("Do you do a hot towel shave?", "Yes, and it is the one we do most. Book The Italian beard trim with shave, thirty minutes, $65, and ask for the hot towel."),
     ("Do you do a straight razor shave?", "Yes. Free hand, full face, with the grain and then across it. Same booking, same $65."),
     ("Do you shave heads with a razor?", "Yes. Hot towels, lather and the blade, taken down to the skin. Not the clippers."),
     ("What's the difference between the $35 and the $65?", "The $35 Beard Trim is clippers and scissors, fifteen minutes, no razor. The $65 brings in the straight razor and the hot towels and takes thirty minutes."),
     ("Is it good before a wedding or event?", "It's the best way to arrive. The morning of or the day before, and book early for Saturdays."),
     ("How long does a shave last?", "Two to four days for most men before the shadow comes back. A razor shave cuts closer than a machine, so it holds longer."),
     ("Can I add a haircut?", "Yes. Men's Cut + Beard Trim does both in one visit, forty-five minutes, $90.")],
    [("Men's haircuts", "/mens-haircut-bondi", "From $66"), ("Skin fade only", "/skin-fade-bondi", "$55"), ("All services", "/services", "Full menu")],
    "Hot towel shave and straight razor shave",
    "Hot towel shave, straight razor shave and razor head shave at Antisystem Barbershop, Bondi Beach.", 65,
    pic=("work-crop-front", "Beard shaped and lined with a razor on the cheeks and neck, Antisystem Barbershop, Bondi Beach"),
    faq_schema=True)

svc("kids-haircut-bondi.html", "/kids-haircut-bondi", "Kids' Haircut Bondi Beach | Under 18 Cuts | Antisystem",
    "Kids' and teen haircuts in Bondi Beach for $50, for anyone under 18. A kid-friendly barbershop on Roscoe St. Book online on Fresha.",
    "Under 18 Cuts", "Kids' and teen haircuts.", "Bondi Beach.",
    "Same chair, same standard, same attention as every adult cut. For anyone under 18.",
    [("Under 18 Cuts", "$50"), ("Time", "30 min")],
    """<h2 class="h3">Under 18, one price.</h2>
<p>From a first proper barbershop cut to the teenager who already knows exactly which fade he wants, the Under 18 Cut covers it. Same thirty minutes, same barbers, $50.</p>
<p>Eighteen and over? Book a <a href="/mens-haircut-bondi" style="text-decoration:underline">Men's Cut</a> or a <a href="/skin-fade-bondi" style="text-decoration:underline">Skin fade</a> like everyone else.</p>
<p>Booking for the whole family? Use group booking on Fresha to book several people in one go.</p>""",
    [("What ages does it cover?", "Anyone under 18, from a toddler's first cut to a teen fade. From 18 up, book a Men's Cut or a Skin fade."),
     ("Can I book my kids and myself together?", "Yes. Choose group appointment on Fresha and add everyone to one booking."),
     ("Can my kid get a fade?", "Yes. Fades, buzz cuts and scissor cuts are all covered.")],
    [("Skin fade only", "/skin-fade-bondi", "$55"), ("Men's haircuts", "/mens-haircut-bondi", "From $66"), ("All services", "/services", "Full menu")],
    "Under 18 Cut", "Kids' and teen haircuts for anyone under 18 at Antisystem Barbershop, Bondi Beach.", 50)

PAGES["404.html"] = page("/404", "Page not found | Antisystem Barbershop", "This page doesn't exist.",
    f"""<section class="sec center" style="padding-top:clamp(4rem,10vw,7rem)"><div class="wrap">
 <h1 class="display">Wrong turn.</h1>
 <p class="sub">This page doesn't exist. Everything you need is one tap away.</p>
 <div class="actions" style="margin-top:2rem"><a class="pill" href="/">Go home</a><a class="more" href="{BOOK}" rel="noopener">Book on Fresha</a></div>
</div></section>""", noindex=True)

# ---------------- write ----------------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
for f, html in PAGES.items():
    open(os.path.join(OUT, f), "w").write(html)

urls = ["/", "/services", "/mens-haircut-bondi", "/skin-fade-bondi", "/italian-shave-bondi", "/kids-haircut-bondi", "/about", "/visit"]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls) + "</urlset>\n")
# The wildcard already allows the AI crawlers; naming them is a statement of intent,
# so nobody later assumes silence meant "no". Google-Extended is the one that decides
# whether Google's AI answers may quote this site at all.
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User",
           "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot", "Bingbot"]
open(os.path.join(OUT, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\n\n" +
    "".join("User-agent: %s\nAllow: /\n\n" % b for b in AI_BOTS) +
    f"Sitemap: {SITE}/sitemap.xml\n")


def llms_txt():
    """A plain-text brief for machines that read the site instead of ranking it.

    Everything here comes from the same constants the pages are built from, so it
    cannot drift from the live menu. It ends with what Antisystem does NOT do:
    the recurring error in third-party listings is a hot-towel straight razor
    shave that has never been on the menu, and stating the negative is the only
    way to correct a model that has already read it somewhere else.
    """
    menu = "\n".join("- %s — %s, $%d AUD" % (n, d, p)
                     for _, rows in SERVICES for n, d, p, _ in rows)
    hours = "\n".join("- %s: %s" % (d, h) for d, h in HOURS)
    return f"""# Antisystem Barbershop

> Italian barbershop at 124B Roscoe St, Bondi Beach NSW 2026, Australia.
> Men's cuts, skin fades, beard trims, and straight razor shaving — including
> a hot towel shave — under The Italian beard trim with shave.
> Opened by Andrea, an Italian barber. Walk-ins taken when a chair is free;
> booking is not required but is the only way to be sure of a time.

## Contact
- Phone: {PHONE} (+61 452 137 237)
- Email: {EMAIL}
- Website: {SITE}/
- Bookings: {FRESHA}
- Instagram: {IG}
- TikTok: {TT}

## Hours (Sydney time)
{hours}

## Services and prices
{menu}

## Barbers
Andrea, Gracie and Dave. Any of the three can be chosen when booking on Fresha.

## Area
Bondi Beach, Bondi, North Bondi, Bondi Junction, Tamarama and Bronte.

## Razor work and shaving
Antisystem does straight razor work, and all of it is done inside The Italian
beard trim with shave ($65, 30 min):
- a full face shave with a straight razor
- a hot towel shave
- a razor finish on the cheeks and neck after a beard trim
- a razor head shave

There is no separate shave line on the booking menu. Book the Italian beard
trim with shave and tell your barber which of these you want.

## What Antisystem does not offer
- The entrance has a step, so it is not wheelchair accessible.
- Closed on Sundays.

## Previous name
The shop at this address was formerly Bondi Barber Lounge, under different
ownership. Listings still carrying that name are out of date; the business
operating at 124B Roscoe St is Antisystem Barbershop.

## Pages
- [Services and prices]({SITE}/services/)
- [Men's haircuts]({SITE}/mens-haircut-bondi/)
- [Skin fades]({SITE}/skin-fade-bondi/)
- [Beard and Italian shave]({SITE}/italian-shave-bondi/)
- [Under 18 cuts]({SITE}/kids-haircut-bondi/)
- [The brand]({SITE}/about/)
- [Visit]({SITE}/visit/)
"""


open(os.path.join(OUT, "llms.txt"), "w").write(llms_txt())
if not INLINE:
    shutil.copytree("img", os.path.join(OUT, "img"))
    # Crawlers that ignore the markup fetch /favicon.ico at the root; without it
    # they get a 404 and keep whatever icon they already had cached.
    shutil.copy("favicon.ico", os.path.join(OUT, "favicon.ico"))
json.dump({"cleanUrls": True, "trailingSlash": False,
           "redirects": [{"source": "/about-6", "destination": "/about", "permanent": True},
                         {"source": "/team-3", "destination": "/about", "permanent": True},
                         {"source": "/visit-us-1", "destination": "/visit", "permanent": True},
                         {"source": "/home", "destination": "/", "permanent": True},
                         {"source": "/book-online", "destination": BOOK, "permanent": False}],
           "headers": [{"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"},
                                                      {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]}]},
          open(os.path.join(OUT, "vercel.json"), "w"), indent=2)
print("built", len(PAGES), "pages ->", OUT)
