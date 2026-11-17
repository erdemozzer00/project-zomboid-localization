"""Oluşturucu (Creator) ekranındaki sabit (Text.ui'den geçmeyen) yazıları çıkarır.

Kullanım: python araclar/creator_cikar.py
Çıktı: kaynak/Creator_lua.json (anahtar → EN), kaynak/Creator_lua_baglam.json (anahtar → dosya:satır),
       kaynak/Creator_onek.json (sonuna sayı/ad eklenen ön ekler, Lua ekine gömülür),
       kaynak/Creator_kalip.json ({x}/{n} yer tutuculu birleşik yazı kalıpları, Lua ekine gömülür)

İki geçiş: 1) C1'in çağrı kalıpları (anahtarlar sabit kalsın diye aynen), 2) C3: bütün dize sabitleri
(araclar/lua_dize.py); kimlikler, günlük mesajları, karşılaştırmalar ve parça dizeler ayıklanır.
Parça dizeler (" MAGS", "World: "…) KALIPLAR'la, sekme ve giysi yuvası adları koddan üretilir.

Anahtar Text.ui ile aynı: "IGUI_ALifeUI_" + Text.hash(en). Mod bu yazıları Text.ui'den geçirmiyor;
çeviri modundaki Lua eki (ALifeTR_Creator.lua) Oluşturucu'da çizilen yazıyı Text.ui'ye sorar (K27).
Türkçe metin Lua'ya yazılmaz (Lua dosyasındaki ş/ğ/ı oyunda bozuk çıkar), TR IG_UI.json'da durur.
Vice ileride bu yazıları Text.ui'ye bağlarsa aynı çeviriler ek olmadan çalışır.
EN JSON'da ya da kaynak/IG_UI_lua.json'da zaten olan anahtarlar alınmaz (çeviri oradan gelir).
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
D = Path(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3803984183/mods/ProjectALifeNPCs/42.20/media/lua/client/ProjectALife/Interface/Creator")
STR = r'"((?:[^"\\\n]|\\.)*)"'
CAGRI = [
    r'\baddButton\([^"\n]*?,\s*' + STR,
    r'\badd(?:Centered)?Label\([^"\n]*?,\s*' + STR,
    r'drawText(?:Centre|Right)?\(\s*' + STR,
    r'\btooltip\s*=\s*' + STR,
    r'\b(?:title|label|heading|text)\s*=\s*' + STR,
    r'addOption(?:Value)?\(\s*' + STR,
    r'set(?:Title|Name|Tooltip)\(\s*' + STR,
    r'\{\s*"[a-z_]+"\s*,\s*' + STR,  # sekme tabloları: { "overview", "IDENTITY" }
]
# C3: ekranda görünmeyen ya da oyunun kendi çevirisinden gelen dizeler
HARIC = {
    # saç/sakal kimlikleri (ekrana vanilla getText ile gelir), eşya kodları, vücut yeri grupları
    "Bald", "Spike", "Braids", "Cornrows", "Grungey", "Chops", "Moustache", "Goatee", "Chin", "Full", "Long",
    "Shotgun", "Handgun", "Molotov", "Human", "Shirt", "Jersey", "Dress", "Boilersuit", "Skirt", "Satchel",
    # dosya biçimi, hata ayıklama, veri adları (kayda EN yazılır)
    "name = ", "collapsed = ", "factions = ", "Folder", "New Faction", "New Folder", "Imported folder", "WT",
    # klasör adları veri() bölümünden gelir (iki yazımıyla)
    "ALife Law Enforcement", "ALife Government", "ALife Families", "ALife Businesses", "ALife Lone Survivors",
    "ALife Outlaws", "ALife Commonwealth", "Visitors",
    # ISModalDialog (UIManager'a ayrı eklenir, ek erişemez)
    "Delete this NPC?", "Delete this faction and all its NPC presets?",
    "Are you sure?\nBuilt-in factions go back to default and deleted ones come back.\nFactions you made yourself stay.",
    # alan adıyla birleşen doğrulama mesajları
    "enter a value.", "maximum must be at least the minimum.",
}
# Birleşik yazılar: {n} {m} {k} {w} sayı, {x} {y} yazı (yazı kısmı da ayrıca çevrilir)
KALIPLAR = [
    "{x} choices", "Open the icon catalog for {x}. Select up to four spawn choices.",
    "{x} COLOR: CUSTOM", "{x} COLOR: NATIVE ITEM COLOR", "{x} makeup",
    "Everything is listed ({n}). Amber groups are off-season, off-role or novelty.",
    "{x} (CONTINUED)", "{n} item", "{n} items", "COLLIDES WITH {x}",
    "Base HP, 0-200. Zero uses the standard NPC HP. The NPC health option and the world health multiplier scale it"
    " on spawn, like stock NPCs; the summary shows the result. Default: {n} HP. Other skills use 1-10 ratings.",
    "Custom ({x})", "{n} weight", "{n} SPAWN OPTIONS", "{n} ATTACHED TO THIS WEAPON", "{n} audio",
    "Faction voice sample: {x}", "{n} recordings + contextual text. Preview a reaction below.",
    "AUDIO {x}", "AUDIO UNAVAILABLE {x}", "TEXT {x}", "World: {n}", "{x} CLEARED",
    "Click to edit {x}. Right-click to clear.",
    "Lone survivors: {x}", "Groups: {n}-{m}", "Lone {x} / Groups {n}-{m}",
    "Lone size (1-{n})", "Group size ({n}-{m})",
    "Relative faction selection weight, 0 to {n}, not a percentage. Zero disables natural spawning."
    " Sandbox settings control overall encounter frequency.",
    "{n} of {m} outpost kinds", "{n} selected",
    "{n} MAG", "{n} MAGS", "{n} each", "{n} total", "{n} preset", "{n} presets",
    "{n}, NPCS: {m}", "FACTIONS: {n}, NPCS: {m}", "{n} NPCS", "{n} FAILED", "{n} ITEMS MISSING",
    "APPLY {x} TO FACTION", "APPLIED {x} TO ALL MEMBERS", "MOVE TO {x}",
    "{n} TEMPLATES", "{n} RANDOM WEIGHT", "{n}/4 seasons",
    "{n} factions, {m} NPCs change; {k} NPCs keep their own outfits; {w} warnings",
    "{x}: no clothing data", "CATALOG ERROR: {x}",
    "{x} Use NPC profile leaves the choice to each member's behavior profile. Individual NPC overrides take precedence.",
    "{x} Use faction follows its default, then the NPC behavior profile when the faction has no override.",
    "{x} World switches and valid task conditions always apply.",
    "{x} Click to open the full vanilla and modded icon catalog. Right-click to clear this slot.",
]
# Birleşik yazı ayraçla (" / ", " - "…) bölününce kalan düz parçalar ve "Click to edit {x}" için küçük harfli adlar
PARCALAR = [
    "Custom", "Built-in override", "NPC Preset", "CODE COPIED", "PASTE IT ON DISCORD", "FULL LIST IN CONSOLE.TXT",
    "MISSING ITEMS", "FACTION PACK IMPORTED", "four distinct seasonal outfits", "incomplete or fewer distinct outfits",
    "PREVIEW ONLY", "events still follow sandbox triggers", "primary firearm", "secondary firearm", "melee weapon",
]
BUYUK = re.compile(r'"([A-Z][A-Z0-9 &/+\-\'.,:()]*[A-Z)])"')  # BÜYÜK HARFLİ etiket literalleri


def uygun(s, i, t):
    """İkinci geçiş: dize ekranda görünecek bir yazı mı (kimlik, günlük, karşılaştırma, desen değil)?"""
    once = s[s.rfind("\n", 0, i) + 1:i]
    j = i + 1
    while j < len(s) and s[j] not in (s[i], "\n"):
        j += 2 if s[j] == "\\" else 1
    sonra = s[j + 1:s.find("\n", j)]
    if not re.search(r"[A-Za-z]{2}", t) or t in HARIC:
        return False
    if t != t.strip() or t[0] in ".,;:)'/" or t[-1] in "('-@|":  # parça: KALIPLAR karşılar
        return False
    if re.search(r"\b(print|log\w*|Log\w*|debug\w*)\s*\(", once):
        return False
    if re.search(r"(==|~=)\s*$", once) or re.match(r"\s*(==|~=)", sonra):
        return False
    if once.rstrip().endswith("[") or sonra.startswith("]"):
        return False
    if re.search(r"\b(find|match|gsub|gmatch|format|require|getText\w*|getTexture|instanceItem)\s*\(\s*([^()]*,\s*)?$", once):
        return False
    if re.search(r"<[A-Z]|%[0-9.\-]*[a-zA-Z%]|[\^$]", t) or ("=" in t and "\n" in t):
        return False
    if re.fullmatch(r"[A-Za-z0-9_.:/\\-]+", t) and not re.fullmatch(r"[A-Z][a-z]+|[A-Z][A-Z]+", t):
        return False
    return True


def tablo(s, ad):
    """`local AD = { "a", "b", ... }` tablosundaki dizeleri verir."""
    m = re.search(r"local " + ad + r" = \{(.*?)\}", s, re.S)
    if not m:
        raise SystemExit(f"{ad} tablosu bulunamadı (mod değişmiş olabilir)")
    return re.findall(r'"([^"]+)"', m.group(1))


def un(s):
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")


def veri(ekle):
    """C3b: Oluşturucu'da görünen ama Lua'da değil veri dosyalarında duran adlar."""
    lua = D.parents[3]  # .../media/lua
    katalog = (lua.parents[2] / "common" / "alife_runtime" / "catalog" / "faction_registry.alife").read_text(encoding="utf-8")
    # Klasör adları: başlıkta string.upper ile, ilişki kartında olduğu gibi çizilir
    s = (D / "ALifeCreatorFolders.lua").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"Folders\.defaults = \{(.*?)\n\}", s, re.S)
    adlar = re.findall(r'name = "([^"]+)"', m.group(1)) if m else []
    adlar += re.findall(r'Folders\.visitorsName = "([^"]+)"', s)
    if len(adlar) < 8:
        raise SystemExit("ALifeCreatorFolders.lua: klasör adları bulunamadı (mod değişmiş olabilir)")
    for t in adlar:
        ekle(t, "ALifeCreatorFolders.lua: klasör adı (ilişki kartı)")
        ekle(t.upper(), "ALifeCreatorFolders.lua: klasör başlığı (string.upper)")
    # Kadro dengesi fraksiyonun adını bu başlıkla değiştirir (general.name; kart, liste, üye satırı)
    s = (lua / "shared" / "ProjectALife" / "Records" / "ALifeRosterBalance.lua").read_text(encoding="utf-8")
    for t in re.findall(r'title = "([^"]+)"', s):
        ekle(t, "ALifeRosterBalance.lua: kadro başlığı (fraksiyon adının yerine)")
    # about.heading → general.category: fraksiyon kartında "Bölüm  -  N presets"
    for t in dict.fromkeys(re.findall(r"^\s*about\.heading (.+?)\s*$", katalog, re.M)):
        ekle(t, "faction_registry.alife: about.heading (fraksiyon kartı alt satırı)")
    # Kıyafet takımı adı "Fraksiyon - açıklama": ek " - "den böler, fraksiyon kısmı ayrı anahtar
    for t in dict.fromkeys(re.findall(r"^\s*attireNames\.\w+ (.+?) - ", katalog, re.M)):
        ekle(t, "faction_registry.alife: attireNames fraksiyon kısmı (kıyafet takımı adı)")
    # C3b-2: " - "den sonraki açıklama kısmı (kıyafet dolabı satırı, fitText ile kırpılır)
    for harf, t in dict.fromkeys(re.findall(r"^\s*attireNames\.(\w+) .+? - (.+?)\s*$", katalog, re.M)):
        ekle(t, f"faction_registry.alife: attireNames.{harf} açıklama (kıyafet dolabı satırı)")


def main():
    sys.path.insert(0, str(KOK / "araclar"))
    from lua_cikar import h
    var = set(json.loads((KOK / "kaynak" / "en" / "IG_UI.json").read_text(encoding="utf-8")))
    var |= set(json.loads((KOK / "kaynak" / "IG_UI_lua.json").read_text(encoding="utf-8")))
    cikti, baglam, onek = {}, {}, []

    def ekle(t, yer):
        t = un(t)
        if not re.search(r"[A-Za-z]{2}", t) or t.startswith(("ISUI/", "ProjectALife", "media/", "Base.")):
            return
        if re.fullmatch(r"[a-z0-9_.]+", t):  # kimlik
            return
        if t != t.strip() or t.endswith("("):  # sonuna değer eklenen ön ek
            if t not in onek:
                onek.append(t)
        k = "IGUI_ALifeUI_" + h(t)
        if k in var:
            return
        cikti.setdefault(k, t)
        baglam.setdefault(k, [yer])

    for f in sorted(D.glob("*.lua")):
        s = f.read_text(encoding="utf-8", errors="ignore")
        satir = lambda i: f"{f.name}:{s.count(chr(10), 0, i) + 1}"
        for p in CAGRI:
            for m in re.finditer(p, s):
                ekle(m.group(1), satir(m.start()))
        for m in BUYUK.finditer(s):
            if len(m.group(1)) >= 3:
                ekle(m.group(1), satir(m.start()))
    # İkinci geçiş (C3)
    from lua_dize import dizeler
    butun = set()
    for f in sorted(D.glob("*.lua")):
        s = f.read_text(encoding="utf-8", errors="ignore")
        for i, t in dizeler(s):
            butun.add(t)
            if uygun(s, i, t):
                k = "IGUI_ALifeUI_" + h(t)
                if k not in var:
                    cikti.setdefault(k, t)
                    baglam.setdefault(k, [f"{f.name}:{s.count(chr(10), 0, i) + 1}"])
    cekirdek = (D / "ALifeCreatorCore.lua").read_text(encoding="utf-8", errors="ignore")
    # Sekme düğmeleri string.upper(id) ile yazılıyor; giysi yuvası kutuları "AmmoStrap" → "AMMO STRAP"
    for t in tablo(cekirdek, "tabs"):
        ekle(t.upper(), "ALifeCreatorCore.lua: sekme (string.upper)")
    for t in tablo(cekirdek, "CLOTHING_ORDER"):
        ekle(t, "ALifeCreatorCore.lua: giysi yuvası (ipucu, seçici başlığı)")
        ekle(re.sub(r"([a-z])([A-Z])", r"\1 \2", t).upper(), "ALifeCreatorAppearance.lua: giysi yuvası kutusu")
    for t in PARCALAR:
        if not any(t.lower() in b.lower() for b in butun):  # "primary firearm": string.lower ile
            raise SystemExit(f"parça kaynakta yok (mod değişmiş olabilir): {t!r}")
        ekle(t, "parça (ayraçla bölünen birleşik yazı)")
    kelimeler = {k for b in butun for k in re.findall(r"[A-Za-z']{3,}", b)}
    for t in KALIPLAR:
        # Kalıbın sabit kısmı birkaç dizeden birleşebilir ("COLOR: " .. "CUSTOM"): kelime kelime denetlenir
        for kelime in re.findall(r"[A-Za-z']{3,}", re.sub(r"\{[a-z]\}", " ", t)):
            if kelime not in kelimeler:
                raise SystemExit(f"kalıp kelimesi kaynakta yok (mod değişmiş olabilir): {kelime!r} ← {t!r}")
        ekle(t, "kalıp (birleşik yazı)")
    # Ana menüdeki Project A-Life kartının alt yazısı (Creator.menuSubtitle; ek bu fonksiyonu sarar)
    for ad, t in (("ALifeCreatorCore.lua", "Factions & NPC settings"), ("ALifeCreatorSaveQueue.lua", "Saving NPC...")):
        s = (D / ad).read_text(encoding="utf-8", errors="ignore")
        i = s.find('"' + t + '"')
        if i < 0:
            raise SystemExit(f"{ad}: bulunamadı (mod değişmiş olabilir): {t!r}")
        ekle(t, f"{ad}:{s.count(chr(10), 0, i) + 1}")
    veri(ekle)
    hedef = KOK / "kaynak"
    hedef.mkdir(exist_ok=True)
    (hedef / "Creator_lua.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")
    (hedef / "Creator_lua_baglam.json").write_text(json.dumps(baglam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    (hedef / "Creator_kalip.json").write_text(json.dumps(KALIPLAR, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    onek.sort(key=len, reverse=True)
    (hedef / "Creator_onek.json").write_text(json.dumps(onek, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(len(cikti), "metin -> kaynak/Creator_lua.json;", len(onek), "on ek;", len(KALIPLAR), "kalip")


if __name__ == "__main__":
    main()
