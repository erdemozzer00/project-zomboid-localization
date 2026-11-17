"""Aşama 2: onaylı çevirilerden teslim dosyalarını üretir ve hepsini birlikte denetler.

Kullanım: python araclar/son_kontrol.py
Çıktı: teslim/IG_UI.json, teslim/Sandbox.json, teslim/UI.json, teslim/RadioData.json, rapor/son_kontrol.md
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
from paket_kontrol import YT, SIZ, DIR, EMIR, CINS, G  # aynı kurallar
from sablon_varyant import turet
from lua_cikar import h

# Sözlük kararlarından sonra kalmaması gereken karşılıklar
YASAK = {
    r"(?<!\w\s)(Düzenleyici|DÜZENLEYİCİ)": "Creator → Oluşturucu",
    r"Seçenekler\s*>": "Options → Ayarlar (vanilla)",
    r"^(Düşmanca|Dost canlısı)$": "tutum etiketi: Düşman / Dost (düz yazıda serbest)",
    r"[Üü]s telsizi": "outpost → karakol",
    r"[Dd]oğurma|[Dd]oğurucu": "spawn → oluşturma / ortaya çıkma",
    r"[Yy]ağma seferi": "scavenge → malzeme toplama",
    r"Varsayılan olarak (açık|kapalı)tır": "-dır",
    r"Varsayılan \d+'?[dt][ıiuü]r": "-dır",
}

# Paketlerdeki gerekçeli üslup istisnaları (K36): IG_UI'ye diyalog da giriyor (Y2, Y3…), "siz"/-dır uyarısı orada da susturulabilsin
ISTISNA = {}
for _p in (KOK / "paketler").glob("*.json"):
    try:
        for _k, _r in json.loads(_p.read_text(encoding="utf-8")).get("satirlar", {}).items():
            _i = _r.get("onayli_uslup_istisnalari") if isinstance(_r, dict) else None
            if isinstance(_i, dict):
                ISTISNA.setdefault(_k, set()).update(t for t, g in _i.items() if isinstance(g, str) and g.strip())
    except (ValueError, AttributeError):
        pass

satirlar = []
genel_sorun = 0
for ad in ("IG_UI", "Sandbox", "UI", "ItemName"):  # UI: K22; ItemName: K46, modun eşya adları
    if not (KOK / "onayli" / f"{ad}.json").exists():
        continue
    en = json.loads((KOK / "kaynak" / "en" / f"{ad}.json").read_text(encoding="utf-8"))
    tr = json.loads((KOK / "onayli" / f"{ad}.json").read_text(encoding="utf-8"))
    eksik = [k for k in en if k not in tr]
    fazla = [k for k in tr if k not in en]
    sorunlar, ayni = [], []
    for k, e in en.items():
        t = tr.get(k)
        if t is None:
            continue
        if not t.strip():
            sorunlar.append(f"{k}: boş")
        if t != t.strip():
            sorunlar.append(f"{k}: baş/son boşluk")
        if Counter(YT.findall(e)) != Counter(YT.findall(t)):
            sorunlar.append(f"{k}: yer tutucu farkı EN={sorted(YT.findall(e))} TR={sorted(YT.findall(t))}")
        t_siz = re.sub(r"\b[A-Z][A-Z0-9]+\b", "", t)
        if SIZ.search(t_siz) and "hitap" not in ISTISNA.get(k, ()):
            sorunlar.append(f'{k}: "siz"? → {SIZ.search(t_siz).group(0)}')
        for s in t.split("\n"):
            s = s.strip()
            if DIR.search(s) and not EMIR.search(s) and s not in ("Nadir", "Çok nadir") and "dir" not in ISTISNA.get(k, ()):
                sorunlar.append(f'{k}: "-dır"? → {s[-30:]}')
        for pat, neden in YASAK.items():
            if re.search(pat, t):
                sorunlar.append(f"{k}: {neden} → {re.search(pat, t).group(0)}")
        if t == e and re.search(r"[a-z]{3}", e):
            ayni.append(f"{k}: {e}")

    # Teslim dosyası: yeni EN sırası, UTF-8 BOM'suz, LF, 4 boşluk girinti (K14)
    cikti = {k: tr[k] for k in en if k in tr}
    # Lua'dan çıkarılan metinler (araclar/lua_cikar.py) yapımcının anahtarlarından sonra eklenir
    lua_say = 0
    for lua_ad in ((f"{ad}_lua", "Creator_lua") if ad == "IG_UI" else ()):  # Creator_lua: Oluşturucu eki (K27)
        lua_en_yol, lua_tr_yol = KOK / "kaynak" / f"{lua_ad}.json", KOK / "onayli" / f"{lua_ad}.json"
        if not lua_tr_yol.exists():
            continue
        lua_en = json.loads(lua_en_yol.read_text(encoding="utf-8"))
        lua_tr = json.loads(lua_tr_yol.read_text(encoding="utf-8"))
        for k, e in lua_en.items():
            t = lua_tr.get(k)
            if t is None or k in cikti:
                continue
            if not t.strip() or t[len(t.rstrip()):] != e[len(e.rstrip()):] or t[:len(t) - len(t.lstrip())] != e[:len(e) - len(e.lstrip())]:
                sorunlar.append(f"{k} (lua): boş / baş-son boşluk")
            if Counter(YT.findall(e)) != Counter(YT.findall(t)):
                sorunlar.append(f"{k} (lua): yer tutucu farkı EN={sorted(YT.findall(e))} TR={sorted(YT.findall(t))}")
            cikti[k] = t
            lua_say += 1
    hedef = KOK / "teslim" / f"{ad}.json"
    hedef.parent.mkdir(exist_ok=True)
    # 1.5.0 (2026-11-09): mod güncellemesinde çevirisi henüz olmayan anahtarlar oyunda İngilizce görünür; sorun sayılmaz,
    # raporlanır. Önceki teslimde çevirisi olup bu çalıştırmada kaybolan anahtar ise sorundur (yanlışlıkla silinmiş çeviri).
    eksik = [k for k in en if k not in cikti]
    onceki = json.loads(hedef.read_bytes().decode("utf-8")) if hedef.exists() else {}
    kaybolan = [k for k in onceki if k in en and k not in cikti]
    sorunlar += [f"{k}: önceki teslimde çevirisi vardı, şimdi yok" for k in kaybolan]
    metin = json.dumps(cikti, ensure_ascii=False, indent=4) + "\n"
    hedef.write_bytes(metin.encode("utf-8"))
    geri = json.loads(hedef.read_bytes().decode("utf-8"))
    bicim_ok = list(geri)[:len(cikti) - lua_say] == [k for k in en if k in tr] and not hedef.read_bytes().startswith(b"\xef\xbb\xbf") and b"\r" not in hedef.read_bytes()

    genel_sorun += len(fazla) + len(sorunlar) + (0 if bicim_ok else 1)
    satirlar += [f"## {ad}.json", "",
                 f"- Anahtar: EN {len(en)} · TR {len(cikti) - lua_say} · çevrilmemiş (İngilizce görünür, sorun sayılmaz) {len(eksik)} · fazla (çıkarıldı) {len(fazla)} · Lua'dan ek {lua_say}",
                 f"- Biçim (sıra, BOM yok, LF): {'tamam' if bicim_ok else 'SORUN'}",
                 f"- Sorun: {len(sorunlar)}"]
    satirlar += [f"  - {s}" for s in sorunlar]
    satirlar += [f"- Çıkarılan anahtarlar: {', '.join(fazla) if fazla else 'yok'}"]
    satirlar += [f"- EN ile aynı kalanlar ({len(ayni)}, özel ad/kısaltma olmalı):"] + [f"  - {s}" for s in ayni] + [""]

# NPC diyalogları (K28): onaylı RD_ALifeLine_ satırları → teslim/RadioData.json (kaynak sırasıyla)
rd_tr_yol = KOK / "onayli" / "RadioData_lua.json"
if rd_tr_yol.exists():
    rd_en = json.loads((KOK / "kaynak" / "RadioData_lua.json").read_text(encoding="utf-8"))
    rd_tr = json.loads(rd_tr_yol.read_text(encoding="utf-8"))
    rd_sorun = []
    for k, t in rd_tr.items():
        e = rd_en.get(k)
        if e is None:
            rd_sorun.append(f"{k}: kaynakta yok")
        elif not t.strip() or t != t.strip():
            rd_sorun.append(f"{k}: boş / baş-son boşluk")
        elif Counter(x.lower() for x in YT.findall(e) if not CINS.fullmatch(x)) != Counter(x.lower() for x in YT.findall(t) if not CINS.fullmatch(x)):  # {At}/{at}: cümle başı büyük harf
            rd_sorun.append(f"{k}: yer tutucu farkı")  # cinsiyetli hitap ({he}, {sir}…) Türkçede kalkabilir ya da {g:a|b} olabilir
        elif any(g.count("|") != 1 for g in G.findall(t)):
            rd_sorun.append(f"{k}: bozuk {{g:a|b}}")
    cikti = {k: rd_tr[k] for k in rd_en if k in rd_tr}
    # Yalnızca cinsiyetli hitap içeren şablonlar oyunda iki İngilizce metne dönüşür; her birine çözülmüş Türkçe eşlenir
    # (satır başına tek düzenlenebilir kayıt: kaynakta ve çevirmen sitesinde yalnızca şablon durur)
    varyant, atlanan, sablon = turet(rd_en, rd_tr, cikti)
    cikti.update(dict(sorted(varyant.items())))
    # K46: rastgele yer tutucu değerlerinin Türkçesi (konuşma ekinin şablon eşlemesi kullanır)
    degerler = json.loads((KOK / "kaynak" / "sablon_degerleri.json").read_text(encoding="utf-8"))
    ek_deger = {"RD_ALifeTR_Deger_" + h(en.lower()): tr for en, tr in degerler["deger"].items()}
    ek_deger.update({"RD_ALifeTR_Kalip_" + ad: tr for ad, tr in degerler["kalip"].items()})
    cikti.update(ek_deger)
    hedef = KOK / "teslim" / "RadioData.json"
    hedef.write_bytes((json.dumps(cikti, ensure_ascii=False, indent=4) + "\n").encode("utf-8"))
    json.loads(hedef.read_bytes().decode("utf-8"))
    genel_sorun += len(rd_sorun)
    satirlar += ["## RadioData.json (NPC diyalogları)", "",
                 f"- Satır: {len(cikti) - len(varyant) - len(ek_deger)} (kaynakta {len(rd_en)})", f"- Yer tutucu değeri (K46): {len(ek_deger)}", f"- Sorun: {len(rd_sorun)}",
                 f"- Şablon varyantı: {sablon} cinsiyetli şablon → {len(varyant)} ek satır (m/f); rastgele yer tutuculu (konuşma eki şablonla eşler, K46): {sum(1 for _, n in atlanan if n == 'rastgele yer tutucu')}",
                 f"- Varyant çakışması: {sum(1 for _, n in atlanan if n != 'rastgele yer tutucu')}"]
    satirlar += [f"  - {a}: {n}" for a, n in atlanan if n != "rastgele yer tutucu"]
    genel_sorun += sum(1 for _, n in atlanan if n != "rastgele yer tutucu")
    satirlar += [f"  - {s}" for s in rd_sorun] + [""]

(KOK / "rapor" / "son_kontrol.md").write_text(
    "# Son kontrol\n\n" + ("Sonuç: temiz\n\n" if genel_sorun == 0 else f"Sonuç: {genel_sorun} SORUN\n\n") + "\n".join(satirlar) + "\n",
    encoding="utf-8", newline="\n")
print("\n".join(satirlar))
print("TEMİZ" if genel_sorun == 0 else f"{genel_sorun} SORUN")
