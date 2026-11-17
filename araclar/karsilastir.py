"""Yeni EN JSON'lari, eski EN + mevcut TR temeliyle karsilastirir.

Kullanim: python araclar/karsilastir.py
Cikti: rapor/ klasoru (rapor.md + cevrilecek JSON'lar). Kaynak dosyalara dokunmaz.
"""
import json, re, difflib, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
YENI = KOK / 'yeni jsonlar'
CIKTI = KOK / 'rapor'
DOSYALAR = ['IG_UI', 'Sandbox']
YT = re.compile(r'\{[^{}]*\}|(?<!%)%\d|<[A-Za-z]+[^>]*>|\[nt"]')

def yukle(p):
    raw = p.read_bytes()
    pairs = json.loads(raw.decode('utf-8'), object_pairs_hook=lambda kv: kv)
    dup = [k for k, c in Counter(k for k, _ in pairs).items() if c > 1]
    bad = [k for k, v in pairs if not isinstance(v, str)]
    if dup or bad:
        sys.exit(f'HATA {p.name}: tekrar eden={dup} metin olmayan={bad}')
    return dict(pairs)

def kelime(s): return len(re.findall(r'\w+', s))

CIKTI.mkdir(exist_ok=True)
md = ['# Güncelleme karşılaştırma raporu\n']
for ad in DOSYALAR:
    eskiEN = yukle(KOK / f'{ad}-updated.json')
    TR = yukle(KOK / f'{ad}-updated-translated.json')
    yeniEN = yukle(YENI / f'{ad}.json')
    assert set(eskiEN) == set(TR), f'{ad}: eski EN ve TR anahtarlari esit degil'

    yeni = [k for k in yeniEN if k not in eskiEN]
    silinen = [k for k in eskiEN if k not in yeniEN]
    degisen = [k for k in yeniEN if k in eskiEN and yeniEN[k] != eskiEN[k]]
    ayni = [k for k in yeniEN if k in eskiEN and yeniEN[k] == eskiEN[k]]
    assert len(ayni) + len(degisen) + len(yeni) == len(yeniEN)
    assert len(ayni) + len(degisen) + len(silinen) == len(eskiEN)

    # Yeni anahtarin metni eskiden birebir varsa mevcut TR yeniden kullanilabilir
    eski_metin = {}
    for k, v in eskiEN.items(): eski_metin.setdefault(v, k)
    birebir = {k: eski_metin[yeniEN[k]] for k in yeni if yeniEN[k] in eski_metin}
    # Silinen anahtarlarla benzerlik: metni duzenlenmis olabilir (anahtarlar metin hash'i olabilir)
    benzer = {}
    for k in yeni:
        if k in birebir: continue
        best, br = None, 0.0
        for s in silinen:
            r = difflib.SequenceMatcher(None, yeniEN[k], eskiEN[s]).ratio()
            if r > br: best, br = s, r
        if br >= 0.6: benzer[k] = (best, br)

    yeni_sirali = [k for k in yeniEN if k in set(yeni)]
    (CIKTI / f'{ad}-cevrilecek-EN.json').write_text(
        json.dumps({k: yeniEN[k] for k in yeni_sirali if k not in birebir} | {k: yeniEN[k] for k in degisen},
                   ensure_ascii=False, indent=4) + '\n', encoding='utf-8')

    md.append(f'\n## {ad}\n')
    md.append(f'| | Anahtar | Kelime (EN) |\n|---|---:|---:|')
    md.append(f'| Eski EN / TR | {len(eskiEN)} | |')
    md.append(f'| Yeni EN | {len(yeniEN)} | |')
    md.append(f'| Aynen kalan (TR hazır) | {len(ayni)} | |')
    md.append(f'| **Yeni eklenen** | {len(yeni)} | {sum(kelime(yeniEN[k]) for k in yeni)} |')
    md.append(f'| — metni eskiden birebir var (bağlama göre kontrol edilmeli) | {len(birebir)} | |')
    md.append(f'| — eski bir metne benziyor (düzenlenmiş olabilir) | {len(benzer)} | |')
    md.append(f'| **Metni değişen** (anahtar aynı) | {len(degisen)} | {sum(kelime(yeniEN[k]) for k in degisen)} |')
    md.append(f'| Silinen | {len(silinen)} | |')
    if degisen:
        md.append('\n### Metni değişen\n')
        for k in degisen:
            md.append(f'- `{k}`\n  - Eski EN: {eskiEN[k]!r}\n  - Yeni EN: {yeniEN[k]!r}\n  - Mevcut TR: {TR[k]!r}')
    if benzer:
        md.append('\n### Yeni ama eski bir metne benzeyenler\n')
        for k, (s, r) in benzer.items():
            md.append(f'- `{k}` (benzerlik %{r*100:.0f}, eski `{s}`)\n  - Yeni EN: {yeniEN[k]!r}\n  - Eski EN: {eskiEN[s]!r}\n  - Eski TR: {TR[s]!r}')
    if birebir:
        md.append('\n### Yeni anahtar, metni eskiden birebir var (bağlam farklı olabilir, körü körüne kopyalanmamalı)\n')
        for k, s in birebir.items():
            md.append(f'- `{k}` ← `{s}`: {yeniEN[k]!r} → TR: {TR[s]!r}')
    if silinen:
        md.append('\n### Silinen\n')
        for k in silinen: md.append(f'- `{k}`: {eskiEN[k]!r}')
    print(f'{ad}: eski={len(eskiEN)} yeni={len(yeniEN)} ayni={len(ayni)} YENI={len(yeni)} (birebir={len(birebir)}, benzer={len(benzer)}) DEGISEN={len(degisen)} SILINEN={len(silinen)}')

(CIKTI / 'rapor.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
