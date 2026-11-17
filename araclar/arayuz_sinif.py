"""1.5.0 IG_UI'nin hâlâ çevirisiz metinlerini Lua kullanım yoluna göre üç sınıfa ayırır (2026-11-09).

Kullanım: python -X utf8 araclar/arayuz_sinif.py
Girdi : rapor/arayuz_1.5.0_IG_UI.json (tür "yeni"), rapor/Y*_harita.json (Y3 hariç; bunlardaki anahtarlar zaten pakette)
        ve modun Lua kaynağı (lua_cikar.MOD).
Çıktı : rapor/arayuz_siniflar_1.5.0.json {anahtar: {en, sinif, alt, konu, dosya, satir, alan, neden}}
        rapor/arayuz_siniflar_1.5.0.md (sayılar). `harici_paket.py hazirla-arayuz-diyalog Y3` a sınıfını bu dosyadan okur.

Sınıflar:
  a  diyalog niteliği: bir karakterin söylediği/yazdığı metin (alt: oyuncu_satiri, npc_soz, yazili_not) -> Gemini (Y3)
  b  arayüz, menü, etiket, bildirim, ipucu (konu: B paketi gruplaması) -> Claude (B paketleri)
  c  oyunda görünmeyen: Text.ui yolu bulunamayan iç kimlik/enum (alt: kesin | belirsiz)
Kural: alan adı (text/ask/say/report/variants/liste) + dosya. Anahtar hash'i Text.ui ile aynı: kaynak/IG_UI_lua gibi, rapor yaparken hesaplanmaz.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
from lua_cikar import MOD  # noqa: E402
from lua_dize import dizeler  # noqa: E402

STR = r'"((?:[^"\\\n]|\\.)*)"'

# --- a sınıfı: dosya -> (alt, kural). kural: "hepsi" | "alanlar:..." (yalnız bu alan adları) | "haric:..." (bu alanlar hariç hepsi)
A_DOSYA = {
    # NPC'nin ağzından çıkan tek tek sözler (havuzlar)
    "ALifeNoveltyMoodData": ("npc_soz", "hepsi"),
    "ALifeNoveltyRumorsData": ("npc_soz", "haric:title,label"),
    "ALifeWorldHunt": ("npc_soz", "hepsi"),
    "ALifeScout": ("npc_soz", "haric:title"),
    "ALifeNoveltyLostData": ("npc_soz", "alanlar:offer,offerText,done,doneText,liste"),
    # yazılı notlar ve anıt yazıları
    "ALifeNoveltyNotesData": ("yazili_not", "alanlar:liste"),
    "ALifeNoveltyMemorialsData": ("yazili_not", "alanlar:liste,friend,alone"),
    # oyuncunun seçtiği/söylediği satırlar
    "ALifeFactionTalkData": ("oyuncu_satiri", "alanlar:text"),
    "ALifeTaskBoardData": ("oyuncu_satiri", "alanlar:ask,report"),
    "ALifeTaskBoardText": ("oyuncu_satiri", "alanlar:text"),
    "ALifeTalk6": ("oyuncu_satiri", "alanlar:text"),
    "ALifeTalkGeneral": ("oyuncu_satiri", "alanlar:text,var"),
    "ALifeTalkIntents": ("oyuncu_satiri", "alanlar:text,var"),
    "ALifeTalk3React": ("oyuncu_satiri", "alanlar:text"),
    "ALifeCars2Talk": ("oyuncu_satiri", "alanlar:text"),
    "ALifeTaskTalk": ("oyuncu_satiri", "alanlar:text_id"),
    "ALifeFactionTalk": ("oyuncu_satiri", "alanlar:text"),
    "ALifeRadioTalk": ("oyuncu_satiri", "alanlar:text"),
    "ALifeUI2TalkStyle": ("oyuncu_satiri", "alanlar:ui_say"),
    "ALifeAnswerChannel": ("oyuncu_satiri", "hepsi"),
    "ALifeEndingCallData": ("oyuncu_satiri", "alanlar:label"),
    "ALifeEndingVerdict": ("oyuncu_satiri", "alanlar:every,ask,stayed,no"),
}

# --- b sınıfı konuları: dosya adı (başlangıç) -> konu
KONU = [
    ("ALifeRepView|ALifeRepTab|ALifeRepIcons|ALifeUI2Rep", "İtibar sekmesi"),
    ("ALifeSquadMap", "Harita ipuçları"),
    ("ALifeRaid|ALifeUI2RaidCard", "Baskın kartı"),
    ("ALifeEnding|ALifeCredits", "Bitiş ekranı ve jenerik"),
    ("ALifeCompanion|ALifeInjured", "Yoldaş sayfası"),
    ("ALifeTaskBoard|ALifeMissionDefs|ALifeUI2Missions|ALifeUI2Tracker|ALifeTaskTalk|ALifeTaskBoardRows", "Görevler"),
    ("ALifeFactionTalk|ALifeTalk|ALifeUI2Talk|ALifeUI2Answer|ALifeUI2Contacts|ALifeUI2CaptiveCard|ALifeFollowB|ALifeCars2Talk|ALifeRadioTalk|ALifeAnswerChannel", "Konuşma arayüzü"),
    ("ALifeUI2StartPick|ALifeStartApply|ALifeUI2Intro|ALifeUI2Journal|ALifeUI2LoadBar|ALifeUI2Notify|ALifeUI2Read|ALifePauseMenu|ALifeUI2Streamer", "Başlangıç, günlük ve bildirimler"),
    ("ALifeDriveHere|ALifeDrivingCrew|ALifeCars|ALifeCarLife|ALifeCarOffline", "Sürüş"),
    ("ALifeCreator", "Oluşturucu"),
    ("ALifeAdmin|ALifeGm|ALifeUI2Gm|ALifeTools|ALifeMarks|ALifeManeuver|ALifeShinto|ALifeDebug|ALifeBlackBox|ALifeBugReport|ALifeDiag|ALifeBuild|ALifeMenu|ALifeStatusWindow|ALifeSpawnPlan|ALifePlanData|ALifeEncounters|ALifeTestCompanions|ALifeDev", "Yönetici ve geliştirici"),
    ("ALifeNovelty|ALifeOutpost|ALifeCaptives|ALifeRadio|ALifeSafehouse|ALifeAudio|ALifeTreeServer|ALifeVisitor|ALifeOffline|ALifeRevenge|ALifeModule|ALifeActivity|ALifeGossip", "Dünya olayları ve bildirimler"),
]


def konu_bul(dosya):
    ad = dosya.rsplit("/", 1)[-1].replace(".lua", "")
    for desen, k in KONU:
        if re.match("(" + desen + ")", ad):
            return k
    return "Diğer"


def un(s):
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")


def alan_bul(satir, en):
    """Dizenin hemen önündeki 'alan =' adı, ya da variants/Text.ui/liste."""
    e = re.escape(en.replace('"', '\\"'))
    m = re.search(r'(\w+)\s*=\s*(?:[\w.:]+\(\s*)?\{?\s*"' + e + '"', satir)
    if m:
        return m.group(1)
    m = re.search(r'variants\s*=\s*\{[^}]*"' + e + '"', satir)
    if m:
        return "var"
    if re.search(r'(?:ui|forPlayer|show)\(\s*"' + e + '"', satir):
        return "ui"
    return "liste"


def a_mi(dosya_ad, alan, satir):
    if dosya_ad.startswith("ALifeTrees_"):
        return "oyuncu_satiri"  # konuşma ağacı seçeneği (Y4'te RD_ALifeLine_ anahtarıyla da var)
    if dosya_ad.startswith("ALifeDialogue_"):
        return "npc_soz"
    if dosya_ad not in A_DOSYA:
        return None
    alt, kural = A_DOSYA[dosya_ad]
    if kural == "hepsi":
        return alt
    tur, _, liste = kural.partition(":")
    alanlar = set(liste.split(","))
    if tur == "haric":
        return None if alan in alanlar else alt
    # alanlar
    if "text_id" in alanlar and alan == "text" and 'id = "' in satir:
        return alt
    if "ui_say" in alanlar and alan == "ui" and "say =" in satir:
        return alt
    if alan in alanlar:
        return alt
    return None


# Lua'da bulunamayan (JSON'da olan, ama .alife/oluşturucu verisinden gelen) 102 metin için kurallar
SORU_A = {
    "I'm police. Look at this badge": "oyuncu_satiri", "What do you folks make of me": "oyuncu_satiri",
    "Who is behind it?": "oyuncu_satiri", "Ran with {faction} until this week": "npc_soz",
}
SORU_B_KONUSMA = {"Opens a trade if they have stock", "Learn if you can cross their ground", "They point out a real danger",
                  "1-{n} answer   MMB or Esc close", "1-{n} answer   MMB, {key} or Esc close",
                  "{key} or 1-{n} answer   wheel select   RMB close", "{up} up  {down} down"}

IC_KIMLIK = {"text", "person", "people", "in", "min", "h", "attack", "defend", "disband", "alert", "unknown", "hunting", "camping",
             "foraging", "fighting", "fleeing", "hiding", "patrolling", "Blood", "of", "east", "south", "north", "west",
             "north-east", "south-east", "south-west", "north-west"}


def main():
    jr = json.loads((KOK / "rapor" / "arayuz_1.5.0_IG_UI.json").read_text(encoding="utf-8"))
    yeni = {k: v for k, v in jr.items() if v["tur"] == "yeni"}
    kapsanan = set()
    for f in (KOK / "rapor").glob("Y*_harita.json"):
        if f.name.startswith("Y3_"):
            continue
        for v in json.loads(f.read_text(encoding="utf-8"))["satirlar"].values():
            kapsanan.add(v[0])
    kalan = {k: v for k, v in yeni.items() if k not in kapsanan}

    ihtiyac = defaultdict(list)
    for k, v in kalan.items():
        ihtiyac[v["en"]].append(k)
    yerler = defaultdict(list)       # en -> [(rel, satır no, satır metni)]
    dogrudan = set()                 # Text.ui/forPlayer/show("...") ile doğrudan çağrılan metinler
    dogrudan_re = re.compile(r'(?:\b[Tt]ext\.(?:ui|forPlayer|show|msg|radio)|FieldRadio\.\w+)\(\s*' + STR)
    for f in sorted(MOD.rglob("*.lua")):
        s = f.read_text(encoding="utf-8", errors="ignore")
        rel = f.relative_to(MOD).as_posix()
        for m in dogrudan_re.finditer(s):
            dogrudan.add(un(m.group(1)))
        satirlar = s.split("\n")
        bas = [0]
        for ln in satirlar:
            bas.append(bas[-1] + len(ln) + 1)
        import bisect
        for i, t in dizeler(s):
            if t in ihtiyac:
                no = bisect.bisect_right(bas, i)
                yerler[t].append((rel, no, satirlar[no - 1].strip()))

    sonuc, sayac = {}, Counter()
    for k, v in kalan.items():
        en = v["en"]
        ad_dosya = v["dosya"].rsplit("/", 1)[-1].replace(".lua", "")
        yer = [y for y in yerler.get(en, []) if y[0].endswith(v["dosya"].rsplit("/", 1)[-1])] or yerler.get(en, [])
        r = dict(en=en, dosya=v["dosya"], satir=None, alan=None)
        if not yer:
            r["neden"] = "Lua'da dize olarak yok (oluşturucu/ayar verisi ya da birleşik yazı)"
            if en in SORU_A:
                r.update(sinif="a", alt=SORU_A[en], konu="Konuşma satırı")
            elif en in SORU_B_KONUSMA:
                r.update(sinif="b", alt="ipucu", konu="Konuşma arayüzü")
            else:
                r.update(sinif="b", alt="oluşturucu/ayar verisi", konu="Oluşturucu")
        else:
            rel, no, satir = yer[0]
            alan = alan_bul(satir, en)
            r.update(satir=f"{rel}:{no}", alan=alan)
            if rel.rsplit("/", 1)[-1].startswith("ALifeDialogue_intents"):
                r.update(sinif="c", alt="kesin", konu="-", neden="serbest metin eşleştirme sözcüğü (intents), ekrana basılmaz")
                sonuc[k] = r
                sayac[(r["sinif"], r["alt"])] += 1
                continue
            alt = a_mi(rel.rsplit("/", 1)[-1].replace(".lua", ""), alan, satir)
            if alt:
                r.update(sinif="a", alt=alt, konu="Konuşma satırı", neden=f"{alan}= alanı, {rel.rsplit('/', 1)[-1]}")
            elif en not in dogrudan and re.fullmatch(r"[A-Za-z][A-Za-z-]*", en) and alan == "liste" and not re.search(r"add\(|label\s*=", satir):
                r.update(sinif="c", alt="belirsiz", konu="-",
                         neden="tek sözcük, Text.ui çağrısında geçmiyor, yalnız kimlik/enum listesinde; tabloyu Text.ui'ye veren kod bulunamadı")
            else:
                r.update(sinif="b", alt="arayüz", konu=konu_bul(rel), neden="menü/etiket/bildirim/ipucu")
        sonuc[k] = r
        sayac[(r["sinif"], r["alt"])] += 1

    (KOK / "rapor" / "arayuz_siniflar_1.5.0.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    toplam = Counter(r["sinif"] for r in sonuc.values())
    konu = Counter(r["konu"] for r in sonuc.values() if r["sinif"] == "b")
    md = [f"# IG_UI 1.5.0 kalan metinlerin sınıfı ({len(sonuc)} metin)", "",
          "Üretici: `araclar/arayuz_sinif.py` (salt okuma). Ayrıntı: `rapor/arayuz_siniflar_1.5.0.json`.", "",
          "| Sınıf | Metin |", "|---|---:|"]
    for s_, ad in (("a", "a — diyalog (Gemini, Y3)"), ("b", "b — arayüz (Claude, B paketleri)"), ("c", "c — oyunda görünmeyen")):
        md.append(f"| {ad} | {toplam[s_]} |")
    md += ["", "## Alt sınıflar", "", "| Sınıf | Alt | Metin |", "|---|---|---:|"]
    for (s_, a_), n in sorted(sayac.items()):
        md.append(f"| {s_} | {a_} | {n} |")
    md += ["", "## b sınıfı konular", "", "| Konu | Metin |", "|---|---:|"]
    for k_, n in konu.most_common():
        md.append(f"| {k_} | {n} |")
    yer_say = defaultdict(Counter)
    for r in sonuc.values():
        yer_say[r["sinif"] + ("/" + r["alt"] if r["sinif"] == "a" else "")][(r["satir"] or "?").split("/")[0] if r["satir"] else "Lua dışı veri"] += 1
    md += ["", "## Oyunda görünür mü? (kod okuması, oyunda denenmedi)", "",
           "Metin kaynak klasörüne göre dağılımı (client/shared/server). Görünürlük kuralları:", "",
           "- `Text.ui` istemcide (client) çalışır: IG_UI.json'daki Türkçe tek oyuncuda da özel sunucuda da görünür.",
           "- `Text.forPlayer` sunucuda (`isServer()`) İngilizce metni doldurur, tek oyuncuda `Text.ui`'ye düşer: **özel sunucuda sunucunun diliyle gider**; NPC sözüyse istemcide `AudioPolicy.caption` → konuşma eki yalnız `RD_ALifeLine_` anahtarıyla çevirir (IG_UI çevirisi o yolda kullanılmaz).",
           "- Bu yüzden a sınıfındaki NPC sözleri/notlar/anıt yazıları tek oyuncuda IG_UI çevirisiyle görünür; özel sunucuda ancak aynı Türkçe `RD_ALifeLine_` anahtarıyla da teslim edilirse (K52'deki 'ikinci anahtar' ekiyle, kalan iş sırası madde 6) görünür.",
           "- a/oyuncu_satiri menü düğmesidir (istemci `Text.ui`): her iki durumda görünür; oyuncu söyleyince çıkan söz ayrı yoldan (`RD_ALifeLine_`) gider.",
           "- b sınıfında client/ klasöründekiler her durumda görünür; shared/ ve server/ olanlar (görev panosu, baskın kartı, ipuçları) çoğunlukla `Text.msg` ile istemciye anahtarıyla gidip istemcide `Text.show` ile çevrilir, ama bu tek tek doğrulanmadı.",
           "- c sınıfı (7): `Text.ui`/`forPlayer` çağrısında geçmeyen tekil sözcük ya da eşleştirme anahtarı; çevirmeye değmez.", "",
           "| Sınıf | Dağılım |", "|---|---|"]
    for k_, c_ in sorted(yer_say.items()):
        md.append(f"| {k_} | " + ", ".join(f"{a_} {n_}" for a_, n_ in c_.most_common()) + " |")
    (KOK / "rapor" / "arayuz_siniflar_1.5.0.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(dict(toplam), dict(konu))
    for (s_, a_), n in sorted(sayac.items()):
        print(s_, a_, n)


if __name__ == "__main__":
    main()
