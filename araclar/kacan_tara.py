"""Lua'da ekrana çıkan ama hiçbir kaynak JSON'da (ve bekleyen pakette) karşılığı olmayan İngilizce metinleri arar (2026-11-09).

Kullanım: python -X utf8 araclar/kacan_tara.py
Çıktı : rapor/kacan_1.5.0.json (aday listesi), rapor/kacan_1.5.0.md (özet sayılar; elle sınıflama notları ayrıdır)

Yöntem: modun bütün Lua dizeleri (lua_dize) alınır; ekran çağrısı bağlamındaki olanlar seçilir:
  sink  = :addOption/addButton/ISButton:new/ISLabel:new/drawText*/setName/setTitle/setTooltip/Say/HaloTextHelper/setHaloNote
          çağrısının dize argümanı ya da text/label/title/tip/tooltip/hint/desc/summary/caption/message/note/impact/risk/ask/report/heading
          alanının değeri.
Aday = İngilizce görünümlü (harf, en az 2 sözcük ya da büyük harfle başlayan 4+ harfli tek sözcük), Text.ui/forPlayer/show/msg/radio
çağrısının İÇİNDE DEĞİL (oradakilerin anahtarı lua_cikar.py ile zaten kapsanır) ve bilinen kümelerde olmayan dize.
Bilinen kümeler (normalize: küçük harf, harf/rakam/{} dışı çıkar): modun EN IG_UI/Sandbox/UI/ItemName JSON'u, kaynak/IG_UI_lua.json,
kaynak/Creator_lua.json, kaynak/RadioData_lua.json, paketler/haritalar/*_harita.json (bekleyen paketler: Y1-Y5, G1…), Creator_kalip.json kalıpları.
"""
import bisect
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
EN_DIR = MOD / "shared/Translate/EN"
ALAN = r"(?:text|label|title|tip|tooltip|hint|desc|description|summary|caption|message|msg|note|impact|risk|ask|report|heading|name|sub|subtitle|header|footer|prompt|question|answer|line|lines)"
SINK = [
    ("addOption", r":addOption\(\s*$S"),
    ("addButton", r"(?:addButton|ISButton:new|W\.button|button)\([^\"\n]*?,\s*$S"),
    ("label", r"(?:ISLabel:new|addLabel|addCenteredLabel|:setName|:setTitle|setTooltip|setText)\([^\"\n]*?$S"),
    ("drawText", r"drawText(?:Centre|Right|Wrap)?\(\s*$S"),
    ("say", r"(?::Say|\.Say|HaloTextHelper\.\w+|setHaloNote|addLineToChat|processSayMessage)\([^\"\n]*?$S"),
    ("alan", r"\b" + ALAN + r"\s*=\s*$S"),
]
WRAP = re.compile(r"(?:\b[Tt]ext\.(?:ui|forPlayer|show|msg|radio|line|lineKey)|Text\.get|getText|getTextOrNull|FieldRadio\.\w+)\(\s*[^()\"]*$")


# Dosya -> kategori (ilk eşleşen). gorunur: oyunda oyuncuya/yöneticiye çizilir mi.
KATEGORI = [
    ("ses_altyazisi", False, r"Audio/ALifeVoice|Audio/ALifeFactionVoiceStyles|Audio/ALifeReactionLibrary",
     "ses profili/klip altyazısı: AudioPolicy.npcAudioEnabled = false (1.5.0'da da sabit), yalnız NPC sesi açılırsa görünür"),
    ("ic_not", False, r"Core/ALifeExperiments|Core/ALifeLifecycle|Combat/|Fear/|ModLoot/|Offline/ALifeAssassins|Compat/|Behaviours/ALifeModule|TowerWar|Experimental/|Eggs/|Fiesta/|Novelty/Core/ALifeNoveltyHub|"
     r"Ending/ALifeEndingStats|Ending/ALifeEndingDirector|Situations/ALifeSituationsServer|World/ALifeMetaEvents|Audio/ALifeAudioWire|"
     r"World/ALifeRoadGraph|World/ALifeMapCompat|Talk/ALifeDialogueRoles|Companions/ALifeTestCompanions|Admin/ALifeDebugService|"
     r"Admin/ALifeAdminConsoleService|Radio/ALifeRadioBoot|World/ALifeSafehouseDoor|World/ALifeSafehouseDirector|Admin/ALifeStartApplyAdmin|"
     r"Records/ALifeBehaviorProfiles|Records/ALifeCustomFactions|Outposts/ALifeOutpostStamps|Driving/ALifeCarsTool|Driving/ALifeCars2[.]lua",
     "geliştirici notu/iç kimlik/yönetici günlüğü satırı: oyuncuya çizilmez ya da yalnız konsol/log"),
    ("ozel_isim", False, r"Ending/ALifeCreditsData", "destekçi/katkı sahibi adları: çevrilmez"),
    ("yonetici_arayuzu", True, r"client/ProjectALife/(Admin|Builder|Driving|Interface/ALifeEncounterConsole|Interface/ALifeStatusWindow)|"
     r"Admin/ALifeSpawnPlan|Admin/ALifeAdminActions|Outposts/ALifeOutposts?Template|Companions/ALifeCompanionSheetAdmin|UI2/ALifeUI2QuickSpawn|"
     r"Interface/Creator/",
     "yönetici/geliştirici/Oluşturucu arayüzü (K52 kapsamı), Text.ui'den geçmeden çiziliyor"),
    ("diyalog", True, r"Situations/ALifeSituationsData|Ending/ALifeEndingCallData|Missions/ALifeMissionDefs|Talk/ALifeTalkSituation|"
     r"Captives/|Talk/Trees/|Talk/ALifeParty|World/ALifeSafehouseEvents|Ending/ALifeEndingData|Shells/ALifeAnimations",
     "oyuncu/NPC sözü, görev/olay metni ya da bitiş verisi"),
    ("oyuncu_arayuzu", True, r"client/ProjectALife/(UI2|Interface|Companions|Ending|Admin)|Ending/ALifeCredits",
     "oyuncu ayar/menü/bildirim metni"),
]


def kategori(yer):
    for ad, gorunur, desen, aciklama in KATEGORI:
        if re.search(desen, yer):
            return ad, gorunur, aciklama
    return "belirsiz", None, "elle bakılmalı"


def norm(t):
    return re.sub(r"[^a-z0-9{}]+", " ", t.lower()).strip()


def bilinen():
    s = set()

    def ekle(d):
        if isinstance(d, str):
            s.add(norm(d))
        elif isinstance(d, dict):
            for v in d.values():
                ekle(v)
        elif isinstance(d, list):
            for v in d:
                ekle(v)
    for f in EN_DIR.glob("*.json"):
        ekle(json.loads(f.read_text(encoding="utf-8")))
    for ad in ("IG_UI_lua", "Creator_lua", "RadioData_lua", "Creator_onek"):
        ekle(json.loads((KOK / "kaynak" / f"{ad}.json").read_text(encoding="utf-8")))
    ekle(json.loads((KOK / "kaynak" / "Creator_kalip.json").read_text(encoding="utf-8")))
    for f in (KOK / "paketler/haritalar").glob("*_harita.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        for v in d.get("satirlar", {}).values():
            if isinstance(v, list) and len(v) > 1 and isinstance(v[1], str):
                s.add(norm(v[1]))
    return s


def ingilizce_mi(t):
    if not re.search(r"[A-Za-z]{3}", t) or len(t) > 400:
        return False
    if re.fullmatch(r"[a-z0-9_.:/\\-]+", t) and " " not in t:   # kimlik, dosya yolu, anahtar
        return False
    if re.search(r"\.(lua|png|ogg|txt|alife|json|xml)\b|^(base|Base)\.|^\w+_\w+$|^%[sdfi]|^#", t):
        return False
    return len(t.split()) >= 2 or bool(re.fullmatch(r"[A-Z][A-Za-z]{3,}", t))


def main():
    bil = bilinen()
    adaylar, bakildi = {}, 0
    for f in sorted(MOD.rglob("*.lua")):
        rel = f.relative_to(MOD).as_posix()
        if "/Translate/" in rel:
            continue
        s = f.read_text(encoding="utf-8", errors="ignore")
        satirlar = s.split("\n")
        bas = [0]
        for ln in satirlar:
            bas.append(bas[-1] + len(ln) + 1)
        for tur, kalip in SINK:
            for m in re.finditer(kalip.replace("$S", STR), s):
                bakildi += 1
                t = m.group(1).replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n")
                if not ingilizce_mi(t) or norm(t) in bil:
                    continue
                onu = s[max(0, m.start() - 60):m.start(1)]
                if WRAP.search(onu.split("\n")[-1] if "\n" in onu else onu):
                    continue  # Text.ui(...) içinde: lua_cikar kapsar
                no = bisect.bisect_right(bas, m.start())
                adaylar.setdefault(t, {"en": t, "yer": [], "sink": set()})
                a = adaylar[t]
                a["sink"].add(tur)
                if len(a["yer"]) < 3:
                    a["yer"].append(f"{rel}:{no}")
    cikti = []
    for a in adaylar.values():
        k, g, ac = kategori(a["yer"][0])
        cikti.append({"en": a["en"], "sink": sorted(a["sink"]), "yer": a["yer"], "kategori": k, "gorunur": g})
    (KOK / "rapor" / "kacan_1.5.0.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    sayac = Counter(c["kategori"] for c in cikti)
    md = ["# Kaçan metin taraması (Lua → JSON karşılığı olmayan, ekrana çıkan İngilizce)", "",
          "Üretici: `araclar/kacan_tara.py` (salt okuma). Ayrıntı: `rapor/kacan_1.5.0.json`. Kapsam: ekran çağrısı bağlamındaki dizeler;",
          "Text.ui/forPlayer/show içindekiler `lua_cikar.py` ile zaten kapsanır. **Aday** = bilinen kümelerde (mod EN JSON'ları, IG_UI_lua, Creator_lua,",
          "RadioData_lua, bekleyen Y/G paketleri) olmayan dize; her aday gerçekten ekranda görünmez, kategoriye bakın.", "",
          "**Önceki tarama (2026-11-03, 1.4.6, `rapor/atlanan_metinler.md`) ile fark:** o günün B grubu (≈412 NPC konuşması: Gossip, PlanData, InjuryRules, Panic…) ve",
          "C grubu (≈59 arayüz mesajı) sonradan çeviri yoluna alınmış (RadioData_lua/IG_UI_lua kaynağında ya da D/G haritalarında), bu taramada aday değil. A grubu (ses altyazıları) hâlâ kapalı",
          "(`npcAudioEnabled = false`). Yeni bulgular aşağıdaki `diyalog` ve `yonetici_arayuzu` kategorileridir: JSON'a girmemişler ve ilk bakışta",
          "`Text.ui`'den geçmeden çiziliyor (ör. bitiş telsiz konuşması sunucuda `Call.fill` ile ham gönderiliyor). Çevirileri için konuşma eki",
          "(`RD_ALifeLine_`) ya da yapımcıya bildirim gerekebilir; kod yolları tek tek doğrulanmadı, oyunda denenmedi.",
          "`Talk/ALifeTalkOrderRows` ve `HomeLeaveRows` adayları `lua_cikar` çıktısıyla (rapor/cikarici_yeni_1.5.0.json) kapsanır.", "",
          "| Kategori | Aday | Görünür mü | Açıklama |", "|---|---:|---|---|"]
    for ad, gorunur, _, ac in KATEGORI + [("belirsiz", None, "", "elle bakılmalı")]:
        md.append(f"| {ad} | {sayac.get(ad, 0)} | {'evet' if gorunur else ('hayır' if gorunur is False else '?')} | {ac} |")
    md += ["", "## Görünür kategorilerde dosya dökümü", ""]
    for ad in ("diyalog", "yonetici_arayuzu", "oyuncu_arayuzu", "belirsiz"):
        md += [f"### {ad}", "", "| Dosya | Aday | Örnek |", "|---|---:|---|"]
        dosyalar = defaultdict(list)
        for c in cikti:
            if c["kategori"] == ad:
                dosyalar[c["yer"][0].split(":")[0]].append(c["en"])
        for f, l in sorted(dosyalar.items(), key=lambda x: -len(x[1])):
            ornek = " · ".join(x[:40].replace("|", "/") for x in l[:2])
            md.append(f"| `{f.split('ProjectALife/', 1)[-1]}` | {len(l)} | {ornek} |")
        md.append("")
    (KOK / "rapor" / "kacan_1.5.0.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"{bakildi} sink eşleşmesi, {len(cikti)} aday:", dict(sayac))
    return cikti


if __name__ == "__main__":
    main()
