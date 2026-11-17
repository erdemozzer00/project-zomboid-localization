"""Her çeviri anahtarının modun kaynak kodunda nerede kullanıldığını çıkarır.

IG_UI anahtarları, modun ALifeText.lua dosyasındaki hash ile üretiliyor:
    IGUI_ALifeUI_ + hash(en)            (bağlamsız)
    IGUI_ALifeUI_ + hash(ctx + "|" + en) (bağlamlı Text.ui çağrısı)
Kaynaktaki tüm metin sabitleri hash'lenip anahtarlarla eşlenir.
Sandbox anahtarları sandbox-options.txt'deki seçeneklerden eşlenir (sayfa, tür, varsayılan).

Kullanim: python araclar/baglam_haritasi.py  ->  rapor/baglam.json + ekrana özet
"""
import json, re
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
MOD = Path(r'C:\Program Files (x86)\Steam\steamapps\workshop\content\108600\3803984183\mods\ProjectALifeNPCs')
DIGITS = '0123456789abcdef'


def hex8(v):
    out = ''
    for _ in range(8):
        out = DIGITS[v % 16] + out
        v //= 16
    return out


def lua_hash(text):
    a, b = 5381, 52711
    for c in text.encode('utf-8'):
        a = (a * 33 + c) % 2147483647
        b = (b * 131 + c) % 2147483629
    return hex8(a) + hex8(b)


ESC = {'n': '\n', 't': '\t', '\\': '\\', '"': '"', "'": "'", 'r': '\r'}
LIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')


def unescape(s):
    return re.sub(r'\\(.)', lambda m: ESC.get(m.group(1), m.group(1)), s)


def kaynak_sabitleri():
    """(metin, dosya, satır, satırın kendisi) listesi."""
    out = []
    for p in sorted(MOD.rglob('*.lua')):
        rel = p.relative_to(MOD).as_posix()
        for no, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            if line.lstrip().startswith('--'):
                continue
            for m in LIT.finditer(line):
                s = unescape(m.group(1) if m.group(1) is not None else m.group(2))
                if s:
                    out.append((s, rel, no, line.strip()))
    return out


def katalog_kayitlari():
    """common/alife_runtime/catalog/*.alife: 'tür id' ... 'end' blokları."""
    kayitlar = []
    for p in sorted((MOD / 'common').rglob('*.alife')):
        rel = p.relative_to(MOD).as_posix()
        cur = None
        for no, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            s = line.strip()
            if not s or s.startswith('@') or s.startswith('#'):
                continue
            if not line.startswith(' ') and s != 'end':
                tur, _, kid = s.partition(' ')
                cur = {'tur': tur, 'id': kid, 'dosya': rel, 'satir': no, 'alanlar': {}}
                kayitlar.append(cur)
            elif s == 'end':
                cur = None
            elif cur is not None:
                alan, _, deger = s.partition(' ')
                cur['alanlar'].setdefault(alan, deger)
    return kayitlar


OZET_ALANLARI = {
    'faction': ['about.title', 'about.heading', 'about.blurb', 'stance.player', 'presence.routine'],
    'member': ['who.title', 'who.faction', 'who.role', 'who.rank', 'who.trade', 'who.tags', 'body.sex', 'mind.defaultTask'],
}


def main():
    yeni = {a: json.loads((KOK / 'yeni jsonlar' / f'{a}.json').read_text(encoding='utf-8')) for a in ['IG_UI', 'Sandbox']}
    sabitler = kaynak_sabitleri()

    # Text.ui(..., ..., "ctx") çağrılarındaki olası bağlam etiketleri
    ctxler = set()
    for p in MOD.rglob('*.lua'):
        for m in re.finditer(r'Text\.(?:ui|key|msg|forPlayer)\(\s*"(?:[^"\\]|\\.)*"\s*,\s*[^,()]*,\s*"([^"]+)"', p.read_text(encoding='utf-8', errors='replace')):
            ctxler.add(m.group(1))

    yerler = defaultdict(list)
    for s, rel, no, line in sabitler:
        yerler['IGUI_ALifeUI_' + lua_hash(s)].append({'dosya': rel, 'satir': no, 'kod': line[:200]})
    ctx_of = {}
    metinler = {s for s, *_ in sabitler}
    for ctx in ctxler:
        for s in metinler:
            k = 'IGUI_ALifeUI_' + lua_hash(ctx + '|' + s)
            if k in yeni['IG_UI']:
                ctx_of[k] = ctx

    kayitlar = katalog_kayitlari()
    fraksiyon_adi = {r['id']: r['alanlar'].get('about.title') for r in kayitlar if r['tur'] == 'faction'}
    katalog = defaultdict(list)
    for r in kayitlar:
        ozet = {a: r['alanlar'][a] for a in OZET_ALANLARI.get(r['tur'], []) if a in r['alanlar']}
        if 'who.faction' in ozet:
            ozet['fraksiyon_adi'] = fraksiyon_adi.get(ozet['who.faction'])
        for alan, deger in r['alanlar'].items():
            if deger and re.search('[A-Za-z]', deger):
                katalog['IGUI_ALifeUI_' + lua_hash(deger)].append(
                    {'dosya': r['dosya'], 'satir': r['satir'], 'kayit': f"{r['tur']} {r['id']}", 'alan': alan, 'ozet': ozet})

    harita = {}
    bulunan = 0
    for k, en in yeni['IG_UI'].items():
        kayit = {'en': en, 'yerler': yerler.get(k, [])[:5]}
        if k in katalog:
            kayit['katalog'] = katalog[k][:3]
            kayit['katalog_sayisi'] = len(katalog[k])
        if k in ctx_of:
            kayit['ctx'] = ctx_of[k]
        if kayit['yerler'] or 'ctx' in kayit or 'katalog' in kayit:
            bulunan += 1
        # hash doğrulama: bağlamsız anahtar metnin kendi hash'i mi?
        kayit['hash_eslesir'] = (k == 'IGUI_ALifeUI_' + lua_hash(en))
        harita[k] = kayit
    dogru_hash = sum(1 for v in harita.values() if v['hash_eslesir'])

    # Sandbox: sandbox-options.txt
    opts = (MOD / '42.20/media/sandbox-options.txt').read_text(encoding='utf-8')
    sb = {}
    for m in re.finditer(r'option\s+([\w.]+)\s*=\s*\{(.*?)\}', opts, re.S):
        body = m.group(2)
        f = dict(re.findall(r'(\w+)\s*=\s*([^,\n]+)', body))
        tr = f.get('translation', '').strip()
        if tr:
            sb[tr] = {k: f.get(k, '').strip() for k in ['page', 'type', 'default', 'min', 'max', 'numValues'] if f.get(k)}
    sb_harita = {}
    for k, en in yeni['Sandbox'].items():
        base = k[len('Sandbox_'):]
        base = re.sub(r'_(tooltip|option\d+)$', '', base)
        sb_harita[k] = {'en': en, 'secenek': sb.get(base)}
    sb_bulunan = sum(1 for v in sb_harita.values() if v['secenek'])

    (KOK / 'rapor').mkdir(exist_ok=True)
    (KOK / 'rapor' / 'baglam.json').write_text(
        json.dumps({'IG_UI': harita, 'Sandbox': sb_harita}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    kat = sum(1 for v in harita.values() if 'katalog' in v)
    kod = sum(1 for v in harita.values() if v['yerler'])
    print(f'IG_UI: {len(harita)} anahtar | bağlamsız hash doğru: {dogru_hash} | kodda bulunan: {kod} | katalogda bulunan: {kat} | toplam bağlamı bulunan: {bulunan} | bağlamlı (ctx): {len(ctx_of)}')
    print('  bağlamı bulunamayanlar:', [v['en'] for v in harita.values() if not (v['yerler'] or 'katalog' in v or 'ctx' in v)][:40])
    print(f'Sandbox: {len(sb_harita)} anahtar | seçenek tanımı bulunan: {sb_bulunan}')


if __name__ == '__main__':
    main()
