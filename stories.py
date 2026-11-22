"""The day's news. Every row was checked against a public source dated 21 Nov 2026.

Fields
------
n        : number printed on the card, in the list and on the map
region   : one of the seven legend regions
place    : dateline printed on the card
lat/lon  : exact location used for the map dot
kicker   : small coloured strip on an illustrated card
headline : big type on a card
body     : one or two short lines on a card
source   : the outlet named beside the story
status   : CONFIRMED / OFFICIAL / REPORTED / CLAIM
size     : "main" (3 cards), "small" (8 cards), "brief" (list only)
scene    : key used by render.py to draw the vignette
brief    : the one-line entry used in the list beside the map
"""

DAY = "2026-11-21"  # every row below was first reported on this UTC day

STORIES = [
    dict(n=1, region="Europe", place="ANTALYA, TÜRKIYE", lat=36.90, lon=30.71,
         kicker="CLIMATE · DAY 13", headline="Climate talks run into Saturday",
         body="Fossil-fuel fight stalls a third draft; the summit misses its Friday close.",
         source="BBC / AFP", status="CONFIRMED", size="main", scene="cop",
         brief="Antalya: COP31 deadlocked over fossil fuels, talks into day 13"),

    dict(n=2, region="Middle East", place="RIYADH, SAUDI ARABIA", lat=24.71, lon=46.68,
         kicker="WAR · 03:00 LOCAL", headline="Three missiles downed over Riyadh",
         body="Coalition says it destroyed three Houthi ballistic missiles after alerts.",
         source="AFP", status="OFFICIAL", size="main", scene="missiles",
         brief="Riyadh: three Houthi missiles intercepted before dawn"),

    dict(n=3, region="Americas", place="JUNÍN, PERU", lat=-10.97, lon=-76.19,
         kicker="QUAKE · 00:09 UTC", headline="Magnitude 6.7 quake shakes Peru",
         body="Deep tremor felt in Lima; officials count 15 hurt and 127 homes damaged.",
         source="USGS / AP", status="OFFICIAL", size="main", scene="quake",
         brief="Junín: M6.7 at 108 km depth, 15 injured, 127 homes hit"),

    dict(n=4, region="Europe", place="KRYVYI RIH, UKRAINE", lat=47.90, lon=33.39,
         kicker="WAR · DOUBLE TAP", headline="Child and medic killed in repeat strike",
         body="Two missiles hit, then drones struck rescuers; 60 wounded, officials say.",
         source="AP / BBC", status="CONFIRMED", size="small", scene="bridge",
         brief="Kryvyi Rih: double-tap strike kills child and paramedic, 60 hurt"),

    dict(n=5, region="Middle East", place="TEHRAN, IRAN", lat=35.69, lon=51.39,
         kicker="DIPLOMACY · STATEMENT", headline="Iran: enriched uranium stays home",
         body="Araghchi says the stock will serve national needs; US gap remains wide.",
         source="TOI / TT", status="OFFICIAL", size="small", scene="uranium",
         brief="Tehran: uranium will not be sent abroad, minister says"),

    dict(n=6, region="Americas", place="WASHINGTON, USA", lat=38.90, lon=-77.04,
         kicker="TECH · TAX THREAT", headline="Trump vows tax on data centres abroad",
         body="US firms building AI capacity overseas face a 'tremendous' penalty.",
         source="NYT", status="REPORTED", size="small", scene="tax",
         brief="Washington: threatens 'tremendous tax' on overseas AI data centres"),

    dict(n=7, region="Asia", place="BEIJING, CHINA", lat=39.90, lon=116.41,
         kicker="DIPLOMACY · PRESSURE", headline="China urges Japan to retract remarks",
         body="Military media renew the call over Takaichi's Taiwan comments.",
         source="AFP", status="OFFICIAL", size="small", scene="flags",
         brief="Beijing: military press urges Tokyo to retract Taiwan remarks"),

    dict(n=8, region="World", place="GLOBAL MARKETS", lat=40.71, lon=-74.01,
         kicker="MARKETS · 09:00 ET", headline="Bitcoin climbs back above $60,000",
         body="Coin gains 9% from a two-year low as forced selling eases.",
         source="CoinDesk", status="CONFIRMED", size="small", scene="btc",
         brief="Markets: Bitcoin reclaims $60k, up 9% off two-year low"),

    dict(n=9, region="World", place="GENEVA, SWITZERLAND", lat=46.20, lon=6.14,
         kicker="UN · DEADLINE", headline="Killer-robot rules pushed to 2028",
         body="128 states extend talks but agree no binding ban yet.",
         source="Reuters", status="CONFIRMED", size="small", scene="robot",
         brief="Geneva: 128 states extend autonomous-weapons talks to 2028"),

    dict(n=10, region="Oceania", place="WELLINGTON, NZ", lat=-41.29, lon=174.78,
         kicker="CRICKET · DAY 3", headline="Rahul 136 puts India in charge",
         body="Gill misses a ton by two; India lead the first Test.",
         source="ANI", status="CONFIRMED", size="small", scene="cricket",
         brief="Wellington: Rahul 136, Gill 98, India control first Test"),

    dict(n=11, region="Americas", place="LAS VEGAS, USA", lat=36.17, lon=-115.14,
         kicker="F1 · QUALIFYING", headline="Verstappen inherits Vegas pole",
         body="Antonelli is fastest but drops to sixth after a penalty.",
         source="Formula 1", status="OFFICIAL", size="small", scene="f1",
         brief="Las Vegas: Antonelli quickest, Verstappen starts on pole"),

    dict(n=12, region="Europe", place="ZAGREB, CROATIA", lat=45.81, lon=15.98,
         kicker="PROTEST · JUSTICE", headline="Croatians rally over hospital death",
         body="Demonstrators demand answers in a psychiatric-hospital case.",
         source="U.S. News", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=13, region="Middle East", place="JAZAN, SAUDI ARABIA", lat=16.88, lon=42.56,
         kicker="WAR · INTERCEPT", headline="Two missiles downed over Jazan",
         body="Debris falls at Shuqaiq, the coalition says.",
         source="Arab News", status="OFFICIAL", size="brief", scene="pin", brief=""),

    dict(n=14, region="Middle East", place="GAZA CITY", lat=31.50, lon=34.47,
         kicker="CONFLICT · STRIKE", headline="Vehicle strike kills three",
         body="Gaza Health Ministry reports the casualties.",
         source="Reuters", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=15, region="Middle East", place="STRAIT OF HORMUZ", lat=26.57, lon=56.25,
         kicker="SHIPPING · ALERT", headline="Two tankers attacked near Hormuz",
         body="Iran displays a launcher as alerts go out to shipping.",
         source="AFP", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=16, region="Middle East", place="MANAMA, BAHRAIN", lat=26.23, lon=50.58,
         kicker="INCIDENT · FIRE", headline="Industrial site fire reported",
         body="Blaze at a civilian site after an Iranian strike claim.",
         source="Il Sole 24 Ore", status="CLAIM", size="brief", scene="pin", brief=""),

    dict(n=17, region="Africa", place="PRETORIA, SOUTH AFRICA", lat=-25.75, lon=28.23,
         kicker="OBITUARY", headline="Mlambo-Ngcuka dies at 71",
         body="First female deputy president and head of UN Women.",
         source="Reuters / AP", status="CONFIRMED", size="brief", scene="pin", brief=""),

    dict(n=18, region="Africa", place="TRIPOLI, LIBYA", lat=32.89, lon=13.19,
         kicker="DIPLOMACY", headline="Ceasefire plan would empower Haftar",
         body="Analysts warn the proposed truce shifts the balance east.",
         source="Yeni Safak", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=19, region="Africa", place="EL FASHER, SUDAN", lat=13.63, lon=25.35,
         kicker="POLITICS", headline="Darfur votes on its administrative fate",
         body="Ballot asks residents to choose the region's future status.",
         source="Yeni Safak", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=20, region="Asia", place="SINGAPORE", lat=1.35, lon=103.82,
         kicker="TECH · RULES", headline="New US chip rules threaten SE Asia",
         body="Malaysia, Thailand and Singapore face new scrutiny.",
         source="Bloomberg", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=21, region="Asia", place="TAIPEI, TAIWAN", lat=25.03, lon=121.57,
         kicker="INCIDENT", headline="Train blast injures 25",
         body="Police rule out terrorism after the carriage explosion.",
         source="CNA", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=22, region="Asia", place="CHANDEL, INDIA", lat=24.30, lon=94.00,
         kicker="PUBLIC HEALTH", headline="Illicit alcohol kills 15",
         body="Another 180 hospitalised in Manipur after drinking it.",
         source="CNA", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=23, region="Asia", place="ISLAMABAD, PAKISTAN", lat=33.68, lon=73.05,
         kicker="WEATHER", headline="Monsoon rains kill dozens",
         body="Flooding and landslides hit several districts.",
         source="Yeni Safak", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=24, region="Asia", place="JAKARTA, INDONESIA", lat=-6.21, lon=106.85,
         kicker="ACCIDENT", headline="Eight dead as boat capsizes",
         body="Rescue teams search for missing passengers.",
         source="Yeni Safak", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=25, region="Americas", place="MEXICO", lat=23.63, lon=-102.55,
         kicker="SECURITY · RAID", headline="'El Chapo Isidro' arrested",
         body="Special forces capture the alleged cartel boss.",
         source="The Guardian", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=26, region="Americas", place="BRASÍLIA, BRAZIL", lat=-15.79, lon=-47.88,
         kicker="HEALTH", headline="Bolsonaro taken to intensive care",
         body="Former president hospitalised, his family says.",
         source="UPI", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=27, region="Americas", place="WASHINGTON, USA", lat=38.90, lon=-77.04,
         kicker="POLICY · RATES", headline="Trump vows a 10% credit-card rate cap",
         body="He says he will work with Democrats on the measure.",
         source="Audacy", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=28, region="Oceania", place="SYDNEY, AUSTRALIA", lat=-33.87, lon=151.21,
         kicker="CRICKET", headline="Cummins keeps the captaincy",
         body="Cricket Australia gives its skipper unanimous support.",
         source="AP", status="OFFICIAL", size="brief", scene="pin", brief=""),

    dict(n=29, region="Oceania", place="AUCKLAND, NZ", lat=-36.85, lon=174.76,
         kicker="SAFETY", headline="Coloured-sand recall raises alarm",
         body="Regulator warns the imported batches may be unsafe.",
         source="ABC", status="REPORTED", size="brief", scene="pin", brief=""),

    dict(n=30, region="Europe", place="DUBLIN, IRELAND", lat=53.35, lon=-6.26,
         kicker="RUGBY", headline="Ireland edge South Africa 20-17",
         body="The Springboks still reach the inaugural final.",
         source="Reuters", status="CONFIRMED", size="brief", scene="pin", brief=""),
]

DATE_CHECK = (
    "Left out as Friday 20 November's news: Wall Street's fall into a correction, the Russian "
    "barrage on Kyiv's bridges, the missile that landed in Poland, the UK–EU deal and Cyclone "
    "Akvari's landfill, older still: Voyager 1's fight-day (18 Nov). Not confirmed when drawn, "
    "so not shown: BepiColombo entering Mercury orbit, a final COP31 text."
)

SOURCES_LINE = (
    "Sources named beside each story · Original drawings · HOW WE CHECKED: CONFIRMED = two or "
    "more outlets · OFFICIAL = on the record · REPORTED = one outlet · CLAIM = one side's account."
)

REGIONS = ["Europe", "Middle East", "Africa", "Asia", "Americas", "Oceania", "World"]

REGION_COLORS = {
    "Europe": "#2E5FA3",
    "Middle East": "#C25B1B",
    "Africa": "#2E7D45",
    "Asia": "#B22A2A",
    "Americas": "#6A3D96",
    "Oceania": "#158A87",
    "World": "#6E6E6E",
}
