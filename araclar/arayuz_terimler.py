"""Arayüz girdilerinin (Y10-Y15) terim listesi ve terim tutarlılık uyarısı.

Kaynaklar: (1) SOZLUK.md / KARARLAR / ILERLEME'deki bağlayıcı karşılıklar (aşağıdaki SOZLUK), (2) onaylı çeviriler:
onayli/IG_UI.json, onayli/IG_UI_lua.json, onayli/Creator_lua.json ve paketler/B9.json (B5-B9 dahil) içinden, İngilizcesi
kısa (≤3 sözcük) etiket olan ve hep aynı Türkçeyle çevrilmiş olanlar (madenle).
`harici_paket.py hazirla-arayuz` her dosyaya yalnız o dosyada geçen en çok 40 terimi yazar ve haritaya (`_terimler`) koyar;
`paket_kontrol.py` aynı listeyle UYARI üretir (hata değil): İngilizce terim satırda geçiyor, Türkçe karşılığı geçmiyor.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ENCOK = 40  # dosya başına terim sınırı
# Plana göre geçersiz kılma (SOZLUK B: Oluşturucu'daki üye ön ayarı "şablon", dünya/zorluk ön ayarı "ön ayar")
PLAN_EK = {"B12a": {"Preset": "Şablon"}, "B12b": {"Preset": "Şablon"}}

# (İngilizce, Türkçe[, regex]) bağlayıcı karşılıklar; regex verilmişse eşleşme onunla yapılır (İngilizce metin küçük harfe bakılmaz)
SOZLUK = [
    # Bağlama bağlı olanlar dar regex'le: yalnız o anlamda (satır başı etiket, belirli kalıp) terim sayılır
    ("Hold", "Dur", r"^hold here"), ("Hold fire", "Ateş kes"), ("Wait", "Bekle", r"^wait\b"), ("Gear", "Teçhizat"),
    ("order wheel", "emir çarkı"), ("Animated text", "Hareketli yazı"), ("static text", "sabit yazı"),
    ("easter egg", "sürpriz"), ("Get in the car", "Arabaya bin"), ("Drive here", "Buraya sür"),
    ("Sister", "Kardeş"), ("Brother", "Kardeş", r"\bbrother\b(?! \w+ ?:)"), ("Reputation", "İtibar"),
    ("Rep", "İtibar", r"(?<![{\w])rep(?![\w}])"), ("Infamy", "Kötü şöhret"), ("Menace", "Tehdit"), ("Fitness", "Fitness"),
    ("faction standing", "fraksiyonla aran", r"\bfaction standings?\b"), ("Faction", "Fraksiyon"),
    ("Safehouse", "Güvenli ev"), ("Shelter", "Sığınak"), ("Outpost", "Karakol"), ("Squad", "Tim"), ("Crew", "Ekip"),
    ("Group", "Grup", r"(?<!tighter )\bgroups?\b"), ("Visitor", "Ziyaretçi"), ("Guest", "Misafir"),
    ("Encounter", "Karşılaşma"), ("Raid", "Baskın"), ("Diagnostics", "Tanılama"), ("Default", "Varsayılan"),
    ("Creator", "Oluşturucu", r"(?<!content )\bcreators?\b"), ("Companion", "Yol arkadaşı", r"\bcompanions?\b"),
    ("Blueprint", "Yapı planı"), ("Preset", "Ön ayar"), ("Profile", "Profil"),
    ("Looter", "Yağmacı"), ("Scavenger", "Leşçi"), ("Scavenging", "Malzeme topluyor", r"^scavenging$"), ("Loot", "Ganimet"),
    ("Hostile", "Düşman"), ("Friendly", "Dost", r"^friendly\b"), ("Neutral", "Tarafsız"), ("Wary", "Temkinli"),
    ("Roaming", "Geziniyor", r"^roaming$"), ("Moving", "Yolda", r"^moving$"), ("Streamer Mode", "Yayıncı modu"),
    ("Report a bug", "Hata bildir"), ("Survivor", "Hayatta kalan"), ("Marksman", "Keskin Nişancı"),
    ("Juggernaut", "Ağır Zırhlı"), ("Searchlight", "Projektör"), ("tile", "kare"), ("Spawn point", "Doğma noktası"),
    ("Cancel orders", "Emirleri iptal et"), ("standing", "aran", r"\bstandings?\b(?! guard| orders)"),
    ("MMB", "Orta tık"), ("RMB", "Sağ tık"), ("horde", "sürü"), ("crew den", "çete yatağı"),
]

# madenden çıkarılacak, tek başına karışık/çok genel sözcükler (bağlama göre değişir)
GENEL = {
    "back", "left", "right", "up", "down", "on", "off", "yes", "no", "ok", "all", "any", "new", "one", "more", "less",
    "none", "other", "someone", "unknown", "done", "next", "close", "open", "live", "tag", "select", "high", "low",
    "auto", "set", "end", "start", "stop", "name", "type", "text", "time", "day", "days", "level", "item", "items",
    "this", "that", "here", "there", "with", "from", "your", "you", "the", "and", "for", "not", "can", "now",
    # bağlama göre anlamı/sözcük türü değişen ya da çok genel: terim listesine girmez
    "where", "when", "work", "head", "light", "cover", "call", "look", "closer", "heavy", "hands", "always", "home", "help",
    "world", "door", "page", "support", "clear", "choose", "leave", "place", "window", "previous", "empty", "dead", "talk",
    "voice", "hard", "offer", "everyone", "east", "west", "north", "south", "mark", "order", "orders", "guard", "standing",
    "scout", "military", "class", "role", "world", "normal", "always", "bleeding", "camp", "task", "confirm", "member",
    # denetimde yanlış anlamda eşleşenler (2026-11-09): "Mechanics" beceri adı ≠ meslek, "dropped"/"condition" eşya durumu vb.
    "past", "condition", "hide", "any time", "mechanic", "visit", "dropped", "holding", "apply", "remove", "large", "larger",
    "small", "engineer", "how many", "healing", "wardrobe by season", "stranger", "friend", "supplies", "careful",
}


def tr_kucuk(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def _buyuk_mu(s):
    return s.upper() == s and s.lower() != s


def madenle():
    """{ingilizce_küçük: (türkçe, onay_sayısı)}; yalnız kısa, yer tutucusuz, hep aynı Türkçeyle çevrilmiş etiketler."""
    def oku(p):
        p = KOK / p
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    cift = []
    for en_p, tr_p in (("kaynak/en/IG_UI.json", "onayli/IG_UI.json"), ("kaynak/IG_UI_lua.json", "onayli/IG_UI_lua.json"),
                       ("kaynak/Creator_lua.json", "onayli/Creator_lua.json")):
        en, tr = oku(en_p), oku(tr_p)
        cift += [(en[k], v) for k, v in tr.items() if k in en]
    b9 = oku("paketler/B9.json").get("satirlar", {})
    en = oku("kaynak/en/IG_UI.json")
    cift += [(en[k], r["tr"]) for k, r in b9.items() if k in en]
    sayac, gorunum = defaultdict(Counter), defaultdict(Counter)
    for e, t in cift:
        e, t = e.strip(), t.strip()
        if len(e.split()) > 3 or len(e) > 28 or re.search(r"[{%<\n|]", e + t) or not re.search(r"[A-Za-z]", e):
            continue
        a = e.lower().rstrip(".:!?")
        if a in GENEL or (" " not in a and len(a) < 4):
            continue
        if re.match(r"(a|an|the|they|you|it|is|are)\b", a) and len(a.split()) <= 2:
            continue  # "a radio", "the army": belirtme/zamir öbeği, terim değil
        t0 = t.rstrip(".:!?")
        sayac[a][tr_kucuk(t0)] += 1
        if not _buyuk_mu(t0):
            gorunum[a][t0] += 1
    cikti = {}
    for a, c in sayac.items():
        (tr, n), toplam = c.most_common(1)[0], sum(c.values())
        if n / toplam < 0.75:
            continue
        goster = gorunum[a].most_common(1)[0][0] if gorunum[a] else tr[:1].upper() + tr[1:]
        if tr_kucuk(goster) != tr:
            goster = tr
        cikti[a] = (goster, toplam)
    return cikti


def _eslesme(en, kalip=None):
    return re.compile(kalip or r"\b" + re.escape(en.lower()) + r"(?:s|es)?\b", re.I | re.M)


def dosya_terimleri(metinler, maden=None, plan=None):
    """Bu dosyanın İngilizce satırlarında geçen terimler: [(ingilizce, türkçe)] (en çok ENCOK; önce sözlük, sonra madenden sık geçenler)."""
    maden = madenle() if maden is None else maden
    birlesik = "\n".join(metinler)
    sec, gorulen = [], set()
    for girdi in SOZLUK:
        en, tr = girdi[0], PLAN_EK.get(plan, {}).get(girdi[0], girdi[1])
        if _eslesme(en, girdi[2] if len(girdi) > 2 else None).search(birlesik):
            sec.append((en, tr))
            gorulen.add(en.lower())
    aday = []
    for en, (tr, onay) in maden.items():
        if en in gorulen or any(en in g.lower() or g.lower() in en for g in gorulen):
            continue
        n = len(_eslesme(en).findall(birlesik))
        if n:
            aday.append((-n, -onay, en, tr))
    aday.sort()
    for _, _, en, tr in aday[: max(0, ENCOK - len(sec))]:
        sec.append((en, tr))
    return sec[:ENCOK] if len(sec) > ENCOK else sec


def kok(tr):
    """Türkçe karşılığın ek almaya dayanıklı kökü (küçük harf): kısa terim aynen, uzun terim son 2 harfi atılmış."""
    t = tr_kucuk(tr)
    return " ".join(w if len(w) <= 4 else w[: len(w) - 2] for w in t.split())


def uyarilar(satirlar, terimler):
    """satirlar: [(anahtar, en, tr)], terimler: [[en, tr], ...] -> ['anahtar: ...'] (hata değil, uyarı)."""
    cikti = []
    girdi = {t[0]: t for t in SOZLUK}
    for k, en, tr in satirlar:
        tl = tr_kucuk(tr)
        for e, t in terimler:
            g = girdi.get(e)
            kalip = _eslesme(e, g[2] if g and len(g) > 2 else None)
            if not kalip.search(en):
                continue
            if all(w in tl for w in kok(t).split()):
                continue
            cikti.append(f"{k}: terim '{e}' → '{t}' bekleniyordu; TR: {tr[:60]}")
    return cikti
