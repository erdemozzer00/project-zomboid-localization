"""Workshop çeviri modunu kurar / günceller.

Kullanım: python araclar/workshop_kur.py
Hedef: C:\\Users\\Erdem\\Zomboid\\Workshop\\ProjectALife_TR
teslim/ klasöründeki çeviri dosyaları her çalıştırmada yeniden kopyalanır.
Görseller yalnızca yoksa üretilir (sonradan kendi görselini koyarsan ezilmez).
"""
import json
import math
import re
import shutil
import struct
import zlib
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF = Path.home() / "Zomboid" / "Workshop" / "ProjectALife_TR"
MOD = HEDEF / "Contents" / "mods" / "ProjectALifeTR"
SURUM = MOD / "42"
TR = MOD / "common" / "media" / "lua" / "shared" / "Translate" / "TR"

MOD_INFO = """name=Project A-Life - Türkçe Çeviri
id=ProjectALifeNPCs_TR
require=\\ProjectALifeNPCs
author=Erdem, gladium, kebab, Nalbarkar
modversion=1.4.5-tr2
versionMin=42.21.0
poster=poster.png
icon=icon.png
description=Project A-Life [ALIFE NPCS] için Türkçe çeviri. Orijinal mod gerekir. Oyun dili Türkçe olunca kendiliğinden devreye girer.
"""

ACIKLAMA_TR = [
    '[h1]Project A-Life - Türkçe Çeviri[/h1]',
    '[url=https://steamcommunity.com/sharedfiles/filedetails/?id=3803984183]Project A-Life [ALIFE NPCS][/url] modunun Türkçe çevirisi.',
    '',
    "[b]Modun yapımcısı Vice'ın onayıyla hazırlanan tek Türkçe çeviri budur.[/b] Diğer Türkçe çeviri modları yapımcı onaylı değildir, onlara itibar etme. Birlikte kurarsan da aynı yazıları birbirinin üstüne yazar, oyunda karışıklık çıkar.",
    '',
    '[h2]Nasıl kullanılır?[/h2]',
    '[list]',
    '[*]Orijinal moda ve bu moda abone ol.',
    '[*]Mods menüsünde ikisini de etkinleştir.',
    '[*]Oyun dilin Türkçe olsun, gerisi kendiliğinden gelir.',
    '[/list]',
    '',
    '[h2]Neler Türkçe?[/h2]',
    "Bütün sandbox ayarları, konuşma penceresi, kapı ve ziyaretçiler, yaralanma ve itibar ekranları, menüler, fraksiyon adları, NPC unvanları, Oluşturucu ve NPC'lerin sık söylediği laflar (selamlaşma, yoldan geçerken laf, kısa tepkiler).",
    '',
    '[h2]Bilinen sınırlar[/h2]',
    "Bazı yazılar şimdilik İngilizce: NPC diyaloglarının bir kısmı, radyo yayınları ve Oluşturucu'daki birkaç onay penceresi. Oyun deneyimini bozmaz; çeviri güncellemelerle tamamlanacak.",
    '',
    '[h2]Çok oyunculu[/h2]',
    'Sunucuda çevirinin görünmesi için çeviri modunu da sunucunun mod listesine ekle.',
    '',
    '[h2]Emeği geçenler[/h2]',
    'Çeviri ve düzenleme: Erdem · Çevirmenler: gladium, kebab, Nalbarkar',
    "Modu yapan ve çeviriye izin veren Vice'a teşekkürler.",
    '',
    '--------------------',
    'Workshop ID: 3833513956',
    'Mod ID: ProjectALifeNPCs_TR',
]


def png(yol, boyut):
    """Kırmızı zemin üstünde ay yıldız (geçici görsel; Pillow gerekmez)."""
    w = h = boyut
    cx, cy = w * 0.40, h * 0.5
    r1, r2 = w * 0.24, w * 0.19
    ox = w * 0.06
    sx, sy, sr = w * 0.69, h * 0.5, w * 0.09
    yildiz = [(sx + sr * math.cos(math.radians(-90 + 72 * i)),
               sy + sr * math.sin(math.radians(-90 + 72 * i))) for i in range(5)]
    sira = [yildiz[i * 2 % 5] for i in range(5)]

    def yildizda(x, y):
        # sarılma sayısı (nonzero) kuralı: yıldızın ortası da dolu
        sayi = 0
        for i in range(5):
            x1, y1 = sira[i]
            x2, y2 = sira[(i + 1) % 5]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                sayi += 1 if y2 > y1 else -1
        return sayi != 0

    satirlar = bytearray()
    for y in range(h):
        satirlar.append(0)
        for x in range(w):
            ay = (x - cx) ** 2 + (y - cy) ** 2 <= r1 ** 2 and (x - cx - ox) ** 2 + (y - cy) ** 2 > r2 ** 2
            beyaz = ay or yildizda(x + 0.5, y + 0.5)
            satirlar += bytes((255, 255, 255) if beyaz else (227, 10, 23))
    veri = zlib.compress(bytes(satirlar), 9)

    def parca(tip, icerik):
        return struct.pack(">I", len(icerik)) + tip + icerik + struct.pack(">I", zlib.crc32(tip + icerik) & 0xFFFFFFFF)

    yol.write_bytes(b"\x89PNG\r\n\x1a\n" + parca(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                    + parca(b"IDAT", veri) + parca(b"IEND", b""))


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
    for ad, onay in (("ALifeTR_Creator.lua", "Creator_lua.json"), ("ALifeTR_Konusma.lua", "RadioData_lua.json"), ("ALifeTR_Bilgi.lua", "Bilgi_UI.json")):
        if not (KOK / "onayli" / onay).exists():
            continue
        (hedef / ad).write_text(ek_metni(ad), encoding="ascii", newline="\n")


def bilgi_metni():
    """K55: ana menü bilgi kutusunun metni (onayli/Bilgi_UI.json) yalnızca mod klasöründeki UI.json'a eklenir.

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
    for yol, boyut in ((HEDEF / "preview.png", 256), (SURUM / "poster.png", 512), (SURUM / "icon.png", 64)):
        if not yol.exists():
            png(yol, boyut)
    ws = HEDEF / "workshop.txt"
    if not ws.exists():  # yükleyici id ekleyince ezilmesin
        satir = ["version=1", "title=Project A-Life - Türkçe Çeviri"]
        satir += [f"description={s}" for s in ACIKLAMA_TR]
        satir += ["tags=", "visibility=public"]
        ws.write_text("\n".join(satir) + "\n", encoding="utf-8", newline="\n")
    for p in sorted(HEDEF.rglob("*")):
        if p.is_file():
            print(p.relative_to(HEDEF.parent), p.stat().st_size)


if __name__ == "__main__":
    main()
