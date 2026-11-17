"""Bir terimin her kaynakta (kullanıcı, çevirmenler, vanilla PZ) nasıl çevrildiğini listeler.

Kullanim: python araclar/terim_tara.py <ingilizce_regex> [en_fazla_ornek]
Ornek:    python araclar/terim_tara.py "\\bspawn" 8
"""
import json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VAN = Path(r'C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media\lua\shared\Translate')


def pairs(p):
    s = p.read_text(encoding='utf-8').strip()
    if not s.startswith('{'):
        s = '{' + s.rstrip().rstrip(',') + '\n}'
    return json.loads(s)


def kaynaklar():
    yeni = {}
    for a in ['IG_UI', 'Sandbox']:
        yeni.update(pairs(KOK / 'yeni jsonlar' / f'{a}.json'))
    eski = {}
    kul = {}
    for a in ['IG_UI', 'Sandbox']:
        eski.update(pairs(KOK / f'{a}-updated.json'))
        kul.update(pairs(KOK / f'{a}-updated-translated.json'))
    out = {'kullanıcı': (eski, kul)}
    for d in sorted((KOK / 'çevirmenler').iterdir()):
        for f in d.iterdir():
            if f.name == "NOTLAR.txt": continue
            out[d.name] = (yeni, pairs(f))
    ven, vtr = {}, {}
    for f in (VAN / 'EN').glob('*.json'):
        try:
            ven.update(pairs(f))
        except Exception:
            pass
    for f in (VAN / 'TR').glob('*.json'):
        try:
            vtr.update(pairs(f))
        except Exception:
            pass
    out['vanilla'] = (ven, vtr)
    return out


def main():
    pat = re.compile(sys.argv[1], re.I)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for ad, (en, tr) in kaynaklar().items():
        hits = [(en[k], tr[k]) for k in tr if k in en and isinstance(en[k], str) and pat.search(en[k])]
        print(f'--- {ad}: {len(hits)}')
        hits.sort(key=lambda h: len(h[0]))
        for e, t in hits[:n]:
            print(f'    {e[:90]!r}\n      -> {t[:110]!r}')


if __name__ == '__main__':
    main()
