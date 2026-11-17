"""Kaçan metin taramasının (rapor/kacan_1.5.0.md) çeviri yolu doğrulanmış gruplarının İngilizce kaynağını çıkarır (2026-11-09).

Kullanım: python -X utf8 araclar/kacan_cikar.py
Çıktı : kaynak/IG_UI_kacan.json (anahtar -> İngilizce), kaynak/IG_UI_kacan_baglam.json (anahtar -> [dosya:satır, alan, grup, tür])
Ayrıntı ve gerekçe: rapor/kacan_ek_1.5.0.md.

Anahtar = "IGUI_ALifeUI_" + Text.hash(en) (ALifeText.lua, ctx yok). Buradaki metinler oyunda şu yollardan çizilir:
  - Text.ui'ye tablo alanından gider (ek gerekmez, yalnız çeviri): konuşma satırı düğmesi Talk2.text(Intents.choiceLabel),
    satırın alt notu Pool.lines -> Talk2.text(meta.impact/risk), görev çipi Talk2.text(chip.label), bitiş soru-cevap
    seçeneği UI2Answer.rowsFor -> Text.ui(option.label), görev aşaması M.text(stage.text/detail), ayar satırı
    M.text(row.label/names/tip), arkadaş çarkı Client.text(slot.label).
  - Konuşma ekiyle (araclar/lua/ALifeTR_Konusma.lua): görev satırı ipucu (Talk2.statusText, "tip" alanı) ve bitiş
    sorusu (UI2Answer.clean, "ask" alanı).
Süslü yer tutuculu ({place}, {name}…) metin alınmaz: sunucu doldurup gönderdiği için anahtar tutmaz.
Mod EN IG_UI'de, kaynak/IG_UI_lua'da ya da bekleyen bir haritada (rapor/*_harita.json) anahtarı olan metin alınmaz.
Kaynağa ve mod dosyalarına yazmaz; yalnız kaynak/IG_UI_kacan*.json'u üretir.
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
from lua_cikar import MOD  # noqa: E402

ONEK = "IGUI_ALifeUI_"
STR = r'"((?:[^"\\\n]|\\.)*)"'

# (dosya, bölüm başı deseni ya da None = bütün dosya, alanlar, grup, tür, satır süzgeci ya da None)
# tür: "diyalog" -> Y6 Gemini girdisi; "arayuz" -> B paketi önerisi (rapor/B_paket_plani_1.5.0.md).
KURALLAR = [
    ("shared/ProjectALife/Situations/ALifeSituationsData.lua", r"^Data\.situations = \{", ("text", "impact", "risk"),
     "durum_satiri", "diyalog", r'\bkey = "'),
    ("shared/ProjectALife/Talk/ALifeTalkSituation.lua", r"^Sit\.rows = \{", ("text", "impact"), "durum_sorusu", "diyalog", None),
    ("shared/ProjectALife/Captives/ALifeCaptivesData.lua", r"^D\.rows = \{", ("text", "impact", "risk"), "esir_satiri", "diyalog", None),
    ("shared/ProjectALife/Missions/ALifeMissionDefs.lua", r"^Defs\.rows = \{", ("text", "tip"), "gorev_satiri", "diyalog", None),
    ("shared/ProjectALife/Ending/ALifeEndingCallData.lua", None, ("label",), "bitis_cagri", "diyalog", r'\{ id = "'),
    ("shared/ProjectALife/Ending/ALifeEndingData.lua", r"^    beats = \{", ("ask", "label"), "bitis_soru", "diyalog", None),
    ("shared/ProjectALife/Missions/ALifeMissionDefs.lua", r"^Defs\.rows = \{", ("label",), "gorev_cipi", "arayuz", r"chips = "),
    ("shared/ProjectALife/Missions/ALifeMissionDefs.lua", r"^Defs\.missions = \{", ("text", "detail"), "gorev_asamasi", "arayuz", r'\{ id = "'),
    ("client/ProjectALife/UI2/ALifeUI2Prefs.lua", r"^Prefs\.rows = \{", ("label", "tip", "names"), "ayar", "arayuz", None),
    ("client/ProjectALife/UI2/ALifeUI2Tracker.lua", None, ("label", "tip", "names"), "ayar", "arayuz", r"addRow|names = |tip = "),
    ("client/ProjectALife/UI2/ALifeUI2TaskArrow.lua", None, ("label", "tip", "names"), "ayar", "arayuz", r"addRow|names = |tip = "),
    ("client/ProjectALife/Ending/ALifeCreditsRoll.lua", None, ("label", "tip", "names"), "ayar", "arayuz", r"speedRow|names = |tip = "),
    ("client/ProjectALife/UI2/ALifeUI2StreamerBubble.lua", None, ("label", "tip", "names"), "ayar", "arayuz", r"addRow|names = |tip = "),
    ("client/ProjectALife/UI2/ALifeUI2JournalSettings.lua", r"^S\.groups = \{", ("label",), "ayar_grubu", "arayuz", None),
    ("client/ProjectALife/Companions/ALifeCompanionClient.lua", r"^Client\.WHEEL = \{", ("label",), "arkadas_carki", "arayuz", None),
]


def lua_hash(text):
    a, b = 5381, 52711
    for c in text.encode("utf-8"):
        a = (a * 33 + c) % 2147483647
        b = (b * 131 + c) % 2147483629
    return "".join("0123456789abcdef"[(v // 16 ** i) % 16] for v in (a, b) for i in range(7, -1, -1))


def anahtar(en):
    return ONEK + lua_hash(en)


def bolum(satirlar, bas):
    """Bölüm başı desenine uyan satırdan, aynı ya da daha az girintili ilk "}" satırına kadar (1 tabanlı satır no)."""
    if bas is None:
        return list(enumerate(satirlar, 1))
    for i, s in enumerate(satirlar):
        if re.search(bas, s):
            girinti = len(s) - len(s.lstrip())
            for j in range(i + 1, len(satirlar)):
                t = satirlar[j]
                if t.strip().startswith("}") and len(t) - len(t.lstrip()) <= girinti:
                    return list(enumerate(satirlar[i:j + 1], i + 1))
            break
    raise SystemExit(f"bölüm bulunamadı: {bas}")


def degerler(satir, alanlar):
    """Satırdaki alan = "metin" değerleri; names = { a = "x", b = "y" } içindekiler 'names' alanı olarak."""
    out = []
    for alan in alanlar:
        if alan == "names":
            m = re.search(r"\bnames = \{([^}]*)\}", satir)
            if m:
                out += [("names", v) for v in re.findall(r"\w+ = " + STR, m.group(1))]
            continue
        out += [(alan, v) for v in re.findall(r"(?<![\w.])" + alan + r" = " + STR, satir)]
    return out


def bilinen():
    """Zaten bir çeviri yolu olan anahtarlar: mod EN IG_UI, kaynak/IG_UI_lua, bekleyen haritalar (Y6 hariç).
    Bu aracın önceki çıktısındaki anahtarlar sayılmaz: `al Y6` ve B paketi onları IG_UI_lua'ya ekledikten sonra da
    yeniden çalıştırınca aynı liste çıksın (Y6 haritası ve test kaynakla tutarlı kalsın)."""
    onceki = KOK / "kaynak" / "IG_UI_kacan.json"
    kendi = set(json.loads(onceki.read_text(encoding="utf-8"))) if onceki.exists() else set()
    s = set(json.loads((KOK / "kaynak" / "en" / "IG_UI.json").read_text(encoding="utf-8")))
    s |= set(json.loads((KOK / "kaynak" / "IG_UI_lua.json").read_text(encoding="utf-8"))) - kendi
    for f in (KOK / "rapor").glob("*_harita.json"):
        if f.name != "Y6_harita.json":
            s |= {v[0] for v in json.loads(f.read_text(encoding="utf-8"))["satirlar"].values()}
    return s


def cikar():
    """[(anahtar, en, yer, alan, grup, tür)] kural sırasıyla; aynı anahtar bir kez."""
    bil, out, gorulen = bilinen(), [], set()
    for dosya, bas, alanlar, grup, tur, suzgec in KURALLAR:
        satirlar = (MOD / dosya).read_text(encoding="utf-8-sig").split("\n")
        for no, satir in bolum(satirlar, bas):
            if suzgec and not re.search(suzgec, satir):
                continue
            for alan, en in degerler(satir, alanlar):
                en = en.replace('\\"', '"').replace("\\'", "'")
                k = anahtar(en)
                if "{" in en or not re.search(r"[A-Za-z]{2}", en) or k in bil or k in gorulen:
                    continue
                gorulen.add(k)
                out.append((k, en, f"{dosya}:{no}", alan, grup, tur))
    return out


def main():
    satirlar = cikar()
    kaynak = {k: en for k, en, *_ in satirlar}
    baglam = {k: [yer, alan, grup, tur] for k, _, yer, alan, grup, tur in satirlar}
    for ad, veri, girinti in (("IG_UI_kacan", kaynak, 4), ("IG_UI_kacan_baglam", baglam, 1)):
        (KOK / "kaynak" / f"{ad}.json").write_text(json.dumps(veri, ensure_ascii=False, indent=girinti) + "\n",
                                                   encoding="utf-8", newline="\n")
    say = {}
    for *_, grup, tur in satirlar:
        say[(tur, grup)] = say.get((tur, grup), 0) + 1
    print(f"{len(satirlar)} metin -> kaynak/IG_UI_kacan.json:",
          ", ".join(f"{t}/{g} {n}" for (t, g), n in say.items()))


if __name__ == "__main__":
    main()
