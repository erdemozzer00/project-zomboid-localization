"""Yer tutuculu diyalog şablonlarından (yalnızca cinsiyetli hitap içerenler) oyundaki iki hâli (m/f) türetir.

Konuşma eki (ALifeTR_Konusma.lua) `AudioPolicy.caption`'a gelen, doldurulmuş ve ilk harfi büyütülmüş İngilizce metnin
hash'ine bakar. `{g:a|b}`, `{sir}`, `{he}` gibi cinsiyet yer tutucuları oyunda tek bir cinsiyet seçilerek doldurulur
(Speech.gendered), yani şablon İngilizce'de tam iki metin üretir. Burada ikisini de üretip her birine, aynı cinsiyetle
çözülmüş Türkçe metni eşleriz. Türkçe satırda süslü parantez kalmaz (Voice yolunda caption'dan sonra çözen yok).
{den}/{town}/{name}/{street}/{weapon} gibi rastgele dolan yer tutucular varsa şablon atlanır.

Python karşılığı oyunun kendi Lua kodu ile `araclar/test_sablon_varyant.py` içinde karşılaştırılır.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lua_cikar import h  # noqa: E402

ADDRESS_FORMS = {
    "sir": ("sir", "ma'am"), "mister": ("mister", "miss"), "he": ("he", "she"), "him": ("him", "her"),
    "his": ("his", "her"), "hers": ("his", "hers"), "himself": ("himself", "herself"),
}
G = re.compile(r"\{g:([^{}]*)\}")
ADDR = re.compile(r"\{([A-Za-z]+)\}")


def gender_style(key, value):
    if len(key) > 1 and key == key.upper():
        return value.upper()
    if key[0] != key[0].lower():
        return value[:1].upper() + value[1:]
    return value


def gendered(text, female):
    """Speech.gendered; sex bilinen durumda."""
    def g(m):
        body = m.group(1)
        bar = body.find("|")
        if bar < 0 or body.find("|", bar + 1) >= 0:
            return m.group(0)
        return body[bar + 1:] if female else body[:bar]

    def a(m):
        forms = ADDRESS_FORMS.get(m.group(1).lower())
        if forms is None:
            return m.group(0)
        return gender_style(m.group(1), forms[1 if female else 0])

    return ADDR.sub(a, G.sub(g, text))


def capitalize(text):
    """Speech.render sonu: ilk ASCII harfi büyütür."""
    m = re.search(r"[A-Za-z]", text)
    return text if m is None else text[:m.start()] + text[m.start()].upper() + text[m.start() + 1:]


# Kapı/ziyaretçi eylem satırları (DoLines.tokens, K46): "*{v:He} glances*"; DoLines.render ilk harfi büyütmez
V_FORMS = {"He": ("He", "She"), "he": ("he", "she"), "His": ("His", "Her"), "his": ("his", "her"),
           "him": ("him", "her"), "Him": ("Him", "Her"), "himself": ("himself", "herself")}
V = re.compile(r"\{v:([A-Za-z]+)\}")


def v_render(text, female):
    """DoLines.render; bilinmeyen sözcük olduğu gibi kalır."""
    return V.sub(lambda m: V_FORMS[m.group(1)][1 if female else 0] if m.group(1) in V_FORMS else m.group(0), text)


def varyantlar(en, tr):
    """[(en_hâli, tr_hâli), ...] ya da şablon uygun değilse None."""
    if "{" not in en:
        return None
    cikti = []
    for female in (False, True):
        if V.search(en):
            e, t = v_render(en, female), v_render(tr, female)
        else:
            e, t = capitalize(gendered(en, female)), gendered(tr, female)
        if "{" in e or "}" in e or "{" in t or "}" in t:
            return None
        cikti.append((e, t))
    return cikti


def anahtar(en):
    return "RD_ALifeLine_" + h(en)


def turet(kaynak, onayli, mevcut):
    """kaynak/onayli: anahtar → metin. mevcut: teslimde zaten olan anahtarlar.
    Döner: (satırlar {anahtar: tr}, atlanan [(şablon anahtarı, neden)], şablon sayısı)."""
    satirlar, atlanan, sablon = {}, [], 0
    for k, tr in onayli.items():
        en = kaynak.get(k)
        if en is None or "{" not in en:
            continue
        v = varyantlar(en, tr)
        if v is None:
            atlanan.append((k, "rastgele yer tutucu"))
            continue
        sablon += 1
        for e, t in v:
            ak = anahtar(e)
            if ak in mevcut:
                if mevcut[ak] != t:
                    atlanan.append((k, f"{ak} başka bir satırla çakışıyor"))
                continue
            if ak in satirlar and satirlar[ak] != t:
                atlanan.append((k, f"{ak} başka bir şablonla çakışıyor"))
                satirlar.pop(ak)
                continue
            satirlar[ak] = t
    return satirlar, atlanan, sablon


YT = re.compile(r"\{([A-Za-z]+)\}")
LUA_OZEL = "^$()%.[]*+-?"
# Konuşma eki (gecerli) değerini oyunun listesiyle denetleyebildiği yer tutucular
TURLU = {"time", "weekday", "date", "day", "name", "street", "town", "destination", "den",
         # E1: Talk/General ve Talk5Home değerleri de ekte biçimiyle doğrulanır (gecerli, ALifeTR_Konusma.lua)
         "at", "At", "badat", "goodat", "contactat", "placeat", "bad", "good", "season", "span", "home", "outpost",
         "kind", "nearTown", "place"}

# The door caption hook validates numeric counts and requires at least two visitors in the group reply.
KAPI_SABLONLARI = {"RD_ALifeLine_5359b13d505dae1c", "RD_ALifeLine_4697c88d71172cab"}


def rastgele_sablonlar(kaynak, onayli):
    """Rastgele dolan yer tutuculu, çevirisi onaylı şablonlar → konuşma ekinin SABLONLAR listesi (K46).

    Her cinsiyet hâli için Speech.render'ın üreteceği metnin Lua deseni: yer tutucu "(.-)" ({day} "(%d+)"),
    sabit kısım kaçışlı, iki uçtan sabitli. Metin bir yer tutucuyla başlıyorsa ilk harfi oyunda değer alır,
    desen büyütülmez. Yan yana iki yer tutucu (arada sabit yazı yok) belirsiz olduğundan atlanır.
    Döner: [{"d": desen, "k": anahtar, "s": "m"/"f"/None, "a": [adlar], "b": kova}], sabit kısmı uzun olan önce."""
    cikti = []
    for k, tr in onayli.items():
        en = kaynak.get(k)
        if en is None or "{" not in en or V.search(en) or k in KAPI_SABLONLARI:
            continue
        # MissionRules fills Dell's directions. The L152 handler validates
        # those three values and preserves the optional tail.
        if set(YT.findall(en)) == {"place", "dist", "dir"}:
            continue
        hal = []
        for female in (False, True):
            e = gendered(en, female)
            if not YT.search(e) or "{" in YT.sub("", e) or "}" in YT.sub("", e):
                hal = []
                break
            # Speech.render ilk harfi büyütür; sayı olan {day} ile başlıyorsa büyüyen harf ondan sonraki sabit yazıdadır
            bas = e[len("{day}"):] if e.startswith("{day}") else e
            m = re.search(r"[A-Za-z{]", bas)
            if m is not None and bas[m.start()] != "{":
                bas = bas[:m.start()] + bas[m.start()].upper() + bas[m.start() + 1:]
            e = ("{day}" if e.startswith("{day}") else "") + bas
            hal.append(e)
        if not hal or re.search(r"\}\{", hal[0]):
            continue
        # Türü denetlenemeyen yer tutucu ({weapon}, {faction}…) alakasız cümleyi yakalamasın: sabit yazı kısa olmamalı
        # ve yer tutucu cümlenin başında ya da sonunda durmamalı (iki yanı sabit yazıyla sınırlı olmalı)
        serbest = set(YT.findall(hal[0])) - TURLU
        if serbest and (len(re.sub(r"[^A-Za-z]", "", YT.sub("", hal[0]))) < 12
                        or any(hal[0].startswith("{" + a + "}") or hal[0].endswith("{" + a + "}") for a in serbest)):
            continue
        cinsler = [(hal[0], None)] if hal[0] == hal[1] else [(hal[0], "m"), (hal[1], "f")]
        for e, s in cinsler:
            desen, adlar = "^", []
            for parca in re.split(r"(\{[A-Za-z]+\})", e):
                y = YT.fullmatch(parca)
                if y:
                    adlar.append(y.group(1))
                    desen += "(%d+)" if y.group(1) == "day" else "(.-)"
                else:
                    desen += "".join("%" + c if c in LUA_OZEL else c for c in parca)
            desen += "$"
            onek = YT.split(e)[0]
            kova = onek[:2].lower() if len(onek) >= 2 else ""
            cikti.append({"d": desen, "k": k, "s": s, "a": adlar, "b": kova, "sabit": len(YT.sub("", e))})
    cikti.sort(key=lambda x: -x["sabit"])
    return cikti


def lua_sablonlar(liste):
    import json
    satir = []
    for e in liste:
        s = "nil" if e["s"] is None else json.dumps(e["s"])
        satir.append("    { d = %s, k = %s, s = %s, b = %s, a = { %s } },\n" % (
            json.dumps(e["d"], ensure_ascii=True), json.dumps(e["k"]), s, json.dumps(e["b"], ensure_ascii=True),
            ", ".join(json.dumps(a) for a in e["a"])))
    return "{\n" + "".join(satir) + "}"
