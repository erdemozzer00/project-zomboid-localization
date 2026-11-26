"""Workshop çeviri modunu kurar / günceller.

Kullanım: python araclar/workshop_kur.py
Hedef: C:\\Users\\Erdem\\Zomboid\\Workshop\\ProjectALife_TR
teslim/ klasöründeki çeviri dosyaları her çalıştırmada yeniden kopyalanır.
Workshop açıklaması güncellenir; mevcut preview.png korunur ve oyun içi poster onunla eşitlenir. Yeni görsel üretilmez.
"""
import json
import re
import shutil
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF = Path.home() / "Zomboid" / "Workshop" / "ProjectALife_TR"
MOD = HEDEF / "Contents" / "mods" / "ProjectALifeTR"
SURUM = MOD / "42"
TR = MOD / "common" / "media" / "lua" / "shared" / "Translate" / "TR"

MOD_ADI = "Project A-Life - Türkçe Çeviri"
MOD_YAZARLARI = "Ozzer, Nalbarlkarl"
MOD_ACIKLAMASI = "Project A-Life [ALIFE NPCS] için Türkçe çeviri. Orijinal mod gerekir. İki mod da etkin olmalı; oyun dilin Türkçe olunca çeviri kendiliğinden devreye girer. Çok oyunculuda çevirinin görünmesi için sunucunun mod listesine bu çeviri modunu da ekle. Baş çevirmen: Ozzer. Yardımcı çevirmen: Nalbarlkarl."
ATOLYE_ID = "3833513956"
ATOLYE_ETIKETLERI = "Build 42;Language/Translation;Literature;Military;Multiplayer"

MOD_INFO = f"""name={MOD_ADI}
id=ProjectALifeNPCs_TR
require=\\ProjectALifeNPCs
author={MOD_YAZARLARI}
modversion=2.00
versionMin=42.21.0
poster=poster.png
icon=poster.png
description={MOD_ACIKLAMASI}
"""

ACIKLAMA_TR = [
    MOD_ACIKLAMASI,
]


def workshop_metaverisi_yaz(ws):
    """Başlık/açıklamayı güncel tut; atölye kimliği, etiket ve görünürlüğü koru."""
    mevcut = {}
    if ws.exists():
        for satir in ws.read_text(encoding="utf-8").splitlines():
            if "=" in satir:
                anahtar, deger = satir.split("=", 1)
                if anahtar != "description":
                    mevcut[anahtar] = deger

    satirlar = [
        f"version={mevcut.get('version', '1')}",
        f"id={mevcut.get('id', ATOLYE_ID)}",
        f"title={MOD_ADI}",
    ]
    satirlar.extend(f"description={metin}" for metin in ACIKLAMA_TR)
    satirlar.extend([
        f"tags={mevcut.get('tags', ATOLYE_ETIKETLERI)}",
        f"visibility={mevcut.get('visibility', 'public')}",
    ])
    ws.write_text("\n".join(satirlar) + "\n", encoding="utf-8", newline="\n")


ASCII = str.maketrans({**dict(zip("şŞğĞıİçÇöÖüÜâÂ", "sSgGiIcCoOuUaA")), "…": "...", "→": "->", "—": "-"})


def lua_kaliplar(kaliplar):
    """"{n} MAGS" → { desen = "^([%-]?[%d%.]+) MAGS$", en = "{n} MAGS", adlar = { "n" } } (Lua deseni).

    {n} {m} {k} {w} sayı yakalar; {x} {y} herhangi bir yazı (ek onu ayrıca çevirir).
    """
    satirlar = []
    # Sabit kısmı uzun olan önce denensin ("AUDIO UNAVAILABLE {x}", "AUDIO {x}"'ten önce)
    for en in sorted(kaliplar, key=lambda k: -len(re.sub(r"\{[a-z]\}", "", k))):
        desen, adlar = "^", []
        for parca in re.split(r"(\{[a-z]\})", en):
            if re.fullmatch(r"\{[a-z]\}", parca):
                adlar.append(parca[1])
                desen += "([%-]?[%d%.]+)" if parca[1] in "nmkw" else "(.-)"
            else:
                desen += "".join("%" + c if c in "^$()%.[]*+-?" else c for c in parca)
        desen += "$"
        satirlar.append("    { desen = %s, en = %s, adlar = { %s } },\n" % (
            json.dumps(desen), json.dumps(en), ", ".join(json.dumps(a) for a in adlar)))
    return "{\n" + "".join(satirlar) + "}"


def lua_ek():
    """Lua ekleri → mod klasörü: Oluşturucu (K27) ve konuşma (K28), araclar/lua/ altından.

    Dosyalar tamamen ASCII yazılır (Lua dosyasındaki Türkçe harf oyunda bozuk çıkar); çeviriler JSON'da.
    Klasör adı "ALifeTurkce": başka bir çeviri modunun "ProjectALifeTR" Lua klasörüyle çakışmasın.
    Bir ek, ona ait onaylı çeviri dosyası yoksa kopyalanmaz.
    """
    hedef = MOD / "common" / "media" / "lua" / "client" / "ALifeTurkce"
    hedef.mkdir(parents=True, exist_ok=True)
    ekler = (
        ("ALifeTR_Creator.lua", "Creator_lua.json"),
        ("ALifeTR_Konusma.lua", "RadioData_lua.json"),
        ("ALifeTR_Bilgi.lua", "Bilgi_UI.json"),
        ("ALifeTR_L152.lua", "IG_UI_lua.json"),
        ("ALifeTR_AD1.lua", "IG_UI_lua.json"),
    )
    for ad, onay in ekler:
        if not (KOK / "onayli" / onay).exists():
            continue
        (hedef / ad).write_text(ek_metni(ad), encoding="ascii", newline="\n")


def bilgi_metni():
    """Ana menü bilgi kutusunun metni (onayli/Bilgi_UI.json) yalnızca mod klasöründeki UI.json'a eklenir.

    teslim/UI.json (yapımcıya giden, EN anahtarlarıyla birebir dosya) değişmez.
    """
    kaynak = KOK / "onayli" / "Bilgi_UI.json"
    hedef = TR / "UI.json"
    if not kaynak.exists() or not hedef.exists():
        return
    ui = json.loads(hedef.read_text(encoding="utf-8"))
    ui.update(json.loads(kaynak.read_text(encoding="utf-8")))
    hedef.write_text(json.dumps(ui, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")


def ek_metni(ad):
    """araclar/lua/<ad> → yer tutucuları doldurulmuş, ASCII Lua metni (testler de bunu çalıştırır)."""
    metin = (KOK / "araclar" / "lua" / ad).read_text(encoding="utf-8")
    if "__AD1_METINLERI__" in metin:
        ad1 = json.loads((KOK / "paketler/haritalar/AD1_harita.json").read_text(encoding="utf-8"))["satirlar"]
        driving154 = json.loads((KOK / "paketler/haritalar/DR154_harita.json").read_text(encoding="utf-8"))["satirlar"]
        gruplar = {
            "driving": range(6, 22),
            "tabs": [1, 2, 43, 44, *range(221, 233)],
            "search": [23, 24, *range(92, 109)],
            "spawn": range(83, 90),
            "choices": range(242, 295),
            "advanced": range(295, 347),
            "cleanup": [*range(51, 67), *range(69, 73)],
            "adminLabels": [25, 28, 31, 32, 36, 37, 42, 45, 46, *range(236, 242)],
            "adminButtons": [26, 30, 38, 39, 40, 41],
            "adminWindow": [48, 49, 50, 109, 233, 234, 235],
            "adminWorld": [29, 33, 34, 35],
            "spawnDetails": [80, 81, 90, 91, *range(105, 109)],
            "cleanupDetails": [27, 67, 68, 73, 74],
            "build": [*range(115, 137), *range(139, 151)],
            "status": [215, 216, 217],
            "drivingRoute": [152, 153, *range(155, 178), 179],
            "routePresets": range(180, 187),
            "drivingPerformance": [178],
            "drivingTuning": [187, *range(189, 194)],
            "outpostNames": range(355, 397),
            "classicDetails": [76, 77],
            "classicEncounter": range(194, 215),
            "builderDetails": [111, 137],
            "crewTitle": [22],
        }
        tablolar = []
        for grup, numaralar in gruplar.items():
            satirlar = []
            for numara in numaralar:
                anahtar, en, _ = ad1[str(numara)]
                satirlar.append(f"        [{json.dumps(en)}] = {json.dumps(anahtar)},")
            if grup == "driving":
                for anahtar, en, _ in driving154.values():
                    satirlar.append(f"        [{json.dumps(en)}] = {json.dumps(anahtar)},")
            tablolar.append(f"    {grup} = {{\n" + "\n".join(satirlar) + "\n    },")
        metin = metin.replace("__AD1_METINLERI__", "{\n" + "\n".join(tablolar) + "\n}")
    if "__GOREV_METINLERI__" in metin:
        def satirlar(paket, grup):
            rapor = json.loads((KOK / "paketler/haritalar" / f"{paket}_harita.json").read_text(encoding="utf-8"))
            return [rapor["satirlar"][str(no)][1] for no in rapor["_teknik"][grup]]

        ek = json.loads((KOK / "paketler/haritalar/AL_EK_UI_harita.json").read_text(encoding="utf-8"))["satirlar"]

        def ek_araligi(bas, son):
            return [ek[str(no)][1] for no in range(bas, son + 1)]

        gruplar = {
            "speech": satirlar("TB_GENEL", "kalip_satirlari"),
            "pitch": satirlar("TB_GENEL", "birlesen_teklif_satirlari"),
            "how": satirlar("TB_GENEL", "yaklasim_sorusu_satirlari"),
            "stage": satirlar("TB_ASAMA", "kalip_satirlari") + ["Get to the {place}", "Clear the {place}"],
            "tree": ek_araligi(1, 15),
            "modal": ek_araligi(26, 29),
            "number": ek_araligi(30, 34),
            "share": ek_araligi(35, 42),
        }
        metin = metin.replace("__GOREV_METINLERI__", "{\n" + "\n".join(
            f"    {grup} = {{ " + ", ".join(json.dumps(en) for en in metinler) + " },"
            for grup, metinler in gruplar.items()
        ) + "\n}")
    if "__ONEKLER__" in metin:
        onekler = json.loads((KOK / "kaynak" / "Creator_onek.json").read_text(encoding="utf-8"))
        lua_dizi = "{\n" + "".join("    " + json.dumps(o, ensure_ascii=True) + ",\n" for o in onekler) + "}"
        metin = metin.replace("__ONEKLER__", lua_dizi)
    if "__KALIPLAR__" in metin:
        kaliplar = json.loads((KOK / "kaynak" / "Creator_kalip.json").read_text(encoding="utf-8"))
        metin = metin.replace("__KALIPLAR__", lua_kaliplar(kaliplar))
    if "__SABLONLAR__" in metin:  # K46: rastgele yer tutuculu, çevirisi onaylı şablonlar
        from sablon_varyant import rastgele_sablonlar, lua_sablonlar
        kaynak = json.loads((KOK / "kaynak" / "RadioData_lua.json").read_text(encoding="utf-8"))
        onayli = json.loads((KOK / "onayli" / "RadioData_lua.json").read_text(encoding="utf-8"))
        metin = metin.replace("__SABLONLAR__", lua_sablonlar(rastgele_sablonlar(kaynak, onayli)))
    metin = metin.translate(ASCII)
    metin.encode("ascii")  # ASCII dışı karakter kalmasın
    return metin


def main():
    for d in (SURUM, TR):
        d.mkdir(parents=True, exist_ok=True)
    (SURUM / "mod.info").write_text(MOD_INFO, encoding="utf-8", newline="\n")
    for ad in ("IG_UI.json", "Sandbox.json", "UI.json", "RadioData.json", "ItemName.json"):
        kaynak = KOK / "teslim" / ad
        if not kaynak.exists():  # RadioData.json yalnızca diyalog çevirisi onaylanınca oluşur
            continue
        json.loads(kaynak.read_text(encoding="utf-8"))  # bozuk dosya kopyalanmasın
        shutil.copyfile(kaynak, TR / ad)
    bilgi_metni()
    lua_ek()
    # Vanilla map symbols persist the translation key across language changes.
    from lua_cikar import h
    name = "Extraction zone"
    fallback = TR.parent / "EN" / "IG_UI.json"
    fallback.parent.mkdir(parents=True, exist_ok=True)
    fallback.write_text(json.dumps({"IGUI_ALifeUI_" + h("alifetr.map.tip|" + name): name}, indent=4) + "\n",
                        encoding="utf-8", newline="\n")
    preview = HEDEF / "preview.png"
    poster = SURUM / "poster.png"
    if not preview.is_file():
        raise FileNotFoundError(f"Mevcut Workshop bannerı bulunamadı; yeni görsel oluşturulmadı: {preview}")
    shutil.copyfile(preview, poster)
    # Eski bağımsız simge dosyasını kaldır; mod.info küçük simge olarak poster.png'yi kullanır.
    icon = SURUM / "icon.png"
    if icon.exists():
        icon.unlink()
    ws = HEDEF / "workshop.txt"
    workshop_metaverisi_yaz(ws)
    for p in sorted(HEDEF.rglob("*")):
        if p.is_file():
            print(p.relative_to(HEDEF.parent), p.stat().st_size)


if __name__ == "__main__":
    main()
