"""Onaylanan paketi onayli/<dosya>.json'a işler (anahtar sırası yeni EN ile aynı).

Kullanim: python araclar/onayla.py S1
Önce paket_kontrol.py temiz olmalı; değilse işlemez.
"""
import json, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent


def main(kod):
    md = (KOK / 'paketler' / f'{kod}.md').read_text(encoding='utf-8')
    if 'Otomatik kontrol: temiz' not in md:
        sys.exit(f'{kod}: otomatik kontrol temiz değil, önce paket_kontrol.py çalıştır.')
    paket = json.loads((KOK / 'paketler' / f'{kod}.json').read_text(encoding='utf-8'))
    dosya = paket['_dosya']
    kaynak = KOK / ('kaynak' if dosya.endswith('_lua') else 'kaynak/en')  # _lua: araclar/lua_cikar.py
    yeni = json.loads((kaynak / f'{dosya}.json').read_text(encoding='utf-8'))
    hedef = KOK / 'onayli' / f'{dosya}.json'
    hedef.parent.mkdir(exist_ok=True)
    mevcut = json.loads(hedef.read_text(encoding='utf-8')) if hedef.exists() else {}
    cakisan = [k for k, r in paket['satirlar'].items() if k in mevcut and mevcut[k] != r['tr']]
    for k, r in paket['satirlar'].items():
        mevcut[k] = r['tr']
    sirali = {k: mevcut[k] for k in yeni if k in mevcut}
    hedef.write_text(json.dumps(sirali, ensure_ascii=False, indent=4) + '\n', encoding='utf-8', newline='\n')
    print(f'{kod}: {len(paket["satirlar"])} satır işlendi → {hedef.name} ({len(sirali)}/{len(yeni)} hazır)')
    if cakisan:
        print('Önceden onaylı değeri değişen anahtarlar:', cakisan)


if __name__ == '__main__':
    main(sys.argv[1])
