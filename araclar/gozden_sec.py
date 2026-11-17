"""Gemini öncesi diyalogları gözden geçirme için seçer (K47). rapor/G1_anahtarlar.json yazar.

Kullanım: python -X utf8 araclar/gozden_sec.py
Alınmaz: kullanıcının kendi metinleri (K1d, K2b kullanıcı satırları, K3'ün geri getirdiği K1 düzeltmeleri, D6m),
onayli/ değişmez. (Çevirmen sitesi 2026-11-13'te kaldırıldı.)
"""
import json
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))

SIRA = "D0 D1 D2 D3a D3b D3c D3d D3e D4a D4b D4c K1d K2a K2b D5a K3 D6a D6b D6c D6d D6e D6f D6g D6h D6i D6j D6k D6l D6m D7a".split()


TASIMA = {}  # ana mod güncellemelerinde noktalaması değişip anahtarı taşınan satırlar (anahtar_tasi.py)
for _f in sorted((KOK / "rapor").glob("anahtar_tasima_*.json")):
    for _eski, _yeni in json.loads(_f.read_text(encoding="utf-8")).items():
        TASIMA[_eski] = _yeni[0]


def guncel_anahtar(k):
    while k in TASIMA:
        k = TASIMA[k]
    return k


def paket(ad):
    satirlar = json.loads((KOK / "paketler" / f"{ad}.json").read_text(encoding="utf-8"))["satirlar"]
    return {guncel_anahtar(k): r for k, r in satirlar.items()}


def main():
    onayli = json.loads((KOK / "onayli" / "RadioData_lua.json").read_text(encoding="utf-8"))
    kaynak = json.loads((KOK / "kaynak" / "RadioData_lua.json").read_text(encoding="utf-8"))
    son, ilk = {}, {}
    for ad in SIRA:
        for k in paket(ad):
            son[k] = ad
            if not ad.startswith("K"):
                ilk.setdefault(k, ad)
    k1 = paket("K1d")
    k2b = paket("K2b")
    kullanici = {k for k, ad in son.items() if ad in ("K1d", "D6m")}
    kullanici |= {k for k, r in k2b.items() if r.get("kim") == "Kullanıcı"}
    kullanici |= {k for k, r in paket("K3").items() if k in k1 and r["tr"] == k1[k]["tr"]}
    site, okundu = set(), set()  # çevirmen sitesi kapandı (2026-11-13)

    def kaynagi(k):
        if son[k] == "K2a":
            return "Codex (K2a)"
        return {"D5a": "gladium (D5a)", "D7a": "baska AI (D7a)"}.get(ilk.get(k), "Claude")

    secili, atlanan = {}, Counter()
    for k in son:
        if k not in onayli or k not in kaynak:
            atlanan["kaynakta yok"] += 1
        elif k in kullanici:
            atlanan["kullanicinin kendi metni"] += 1
        elif k in site:
            atlanan["sitede bekleyen duzeltme"] += 1
        elif k in okundu:
            atlanan["okundu isaretli"] += 1
        else:
            secili[k] = kaynagi(k)
    (KOK / "rapor" / "G1_anahtarlar.json").write_text(json.dumps(secili, ensure_ascii=False, indent=0) + "\n", encoding="utf-8", newline="\n")
    print("secili", len(secili), dict(Counter(secili.values())))
    print("atlanan", dict(atlanan))


if __name__ == "__main__":
    main()
