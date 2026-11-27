#!/usr/bin/env python3
"""A-Life Lokalizasyon kataloğunu repodan üretir.

Kullanım:  python arac/katalog_uret.py --repo /yol/project-zomboid-localization --cikti site/veri
Repo hangi commit'te duruyorsa katalog o sürümden üretilir (git checkout <commit> sonra bu aracı çalıştır).
"""
import argparse, collections, datetime, hashlib, json, os, re, shutil, subprocess

def L(p):
    with open(p, encoding='utf-8') as f: return json.load(f)
def LO(p): return L(p) if os.path.exists(p) else {}
def W(p, d):
    with open(p, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, separators=(',', ':'))

NPC_GRUP = [
 ('npc-barks', 'Kendiliğinden söylenen sözler', 'Selam, yoldan geçerken atılan laf, panik, çatışma.', 'ALifeDialogue_barks_*', 'rastgele'),
 ('npc-cevap', 'Konuşma penceresindeki cevaplar', 'Oyuncu bir şey sordu ya da söyledi; NPC cevap veriyor.', 'ALifeDialogue_replies_*', 'rastgele'),
 ('npc-evethayir', 'Evet / hayır cevapları', 'NPC sordu, oyuncu evet ya da hayır dedi; NPC tepki veriyor.', 'ALifeDialogue_yes_* / _no_*', 'rastgele'),
 ('npc-sahne', 'Sahneler', 'Belirli bir yere ve duruma bağlı kısa sahneler.', 'ALifeDialogue_scenes_*', 'belirsiz'),
 ('npc-agac', 'Konuşma ağaçları', 'Dallanan konuşmaların düğümleri.', 'ALifeTrees_*', 'belirsiz'),
 ('npc-dugum', 'Düğüm kayıtları', 'Bağlam kaydında dosya adı yerine "nodes" yazan satırlar.', 'nodes', 'belirsiz'),
 ('npc-diger', 'Diğer konuşma ve görev dosyaları', 'Yukarıdaki dosya adı kalıplarına uymayan Lua dosyaları.', 'diğer', 'belirsiz'),
]
def npc_grup(f):
    if f.startswith('ALifeDialogue_barks_'): return 'npc-barks'
    if f.startswith('ALifeDialogue_replies_'): return 'npc-cevap'
    if f.startswith('ALifeDialogue_yes_') or f.startswith('ALifeDialogue_no_'): return 'npc-evethayir'
    if f.startswith('ALifeDialogue_scenes_'): return 'npc-sahne'
    if f.startswith('ALifeTrees_'): return 'npc-agac'
    if f == 'nodes': return 'npc-dugum'
    return 'npc-diger'

def not_bul(d, ev):
    if not d or not ev: return None
    v = d.get(ev)
    if isinstance(v, str): return v
    best = None
    for k in d:
        if k.endswith('*') and not k.startswith('_') and ev.startswith(k[:-1]) and (best is None or len(k) > len(best)): best = k
    return d[best] if best and isinstance(d[best], str) else None

def insan(f):
    b = os.path.basename(f)
    if not b.endswith('.lua'): return b
    b = b[:-4]
    if b.startswith('ALife') and len(b) > 5: b = b[5:]
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', b).replace('_', ' ').strip()

class Grup:
    def __init__(s, gid, ad, aciklama, kalip, hedef, tur, iliski=''):
        s.d = dict(id=gid, ad=ad, aciklama=aciklama, kalip=kalip, hedef=hedef, tur=tur, iliski=iliski)
        s.sah = collections.OrderedDict(); s.paket = {}
    def ekle(s, baslik, key, en, tr, ctx):
        x = s.sah.setdefault(baslik, {'c': [], 'm': {}, 'r': []})
        ci = x['m'].get(ctx)
        if ci is None:
            ci = len(x['c']); x['m'][ctx] = ci; x['c'].append(list(ctx))
        x['r'].append([key, en, tr, ci])
    def yaz(s, out, sirala=True, parca=3500):
        items = list(s.sah.items())
        if sirala: items.sort(key=lambda kv: (kv[0].startswith('Bağlam kaydı yok'), -len(kv[1]['r']), kv[0]))
        idx, chunk, n, ci, duzey = [], {}, 0, 0, collections.Counter()
        def bosalt():
            nonlocal chunk, n, ci
            if chunk:
                W(os.path.join(out, 's', '%s-%d.json' % (s.d['id'], ci)), chunk); ci += 1; chunk = {}; n = 0
        for i, (baslik, x) in enumerate(items):
            lv = [c[3] for c in x['c']]
            for r in x['r']: duzey[x['c'][r[3]][3]] += 1
            idx.append([baslik, len(x['r']), ci, min(lv), max(lv)])
            chunk[str(i)] = {'c': x['c'], 'r': x['r']}; n += len(x['r'])
            if n >= parca: bosalt()
        bosalt()
        W(os.path.join(out, 'g', s.d['id'] + '.json'), dict(s.d, sahneler=idx, paketler=s.paket))
        return dict(s.d, satir=sum(len(x['r']) for _, x in items), sahne=len(items), duzey={str(k): v for k, v in sorted(duzey.items())})

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--repo', required=True); ap.add_argument('--cikti', default='site/veri')
    a = ap.parse_args(); R = a.repo; out = a.cikti
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out + '/g'); os.makedirs(out + '/s')
    P = lambda *x: os.path.join(R, *x)
    try: commit = subprocess.run(['git', '-C', R, 'rev-parse', '--short=7', 'HEAD'], capture_output=True, text=True).stdout.strip() or 'bilinmiyor'
    except Exception: commit = 'bilinmiyor'
    hedefler = ['RadioData_lua', 'IG_UI', 'IG_UI_lua', 'Creator_lua', 'Sandbox', 'UI', 'ItemName', 'Bilgi_UI']
    tr = {h: LO(P('onayli', h + '.json')) for h in hedefler}
    en = {'RadioData_lua': LO(P('kaynak', 'RadioData_lua.json')), 'IG_UI': LO(P('kaynak', 'en', 'IG_UI.json')),
          'IG_UI_lua': dict(LO(P('kaynak', 'IG_UI_kacan.json')), **LO(P('kaynak', 'IG_UI_lua.json'))),
          'Creator_lua': LO(P('kaynak', 'Creator_lua.json')), 'Sandbox': LO(P('kaynak', 'en', 'Sandbox.json')),
          'UI': LO(P('kaynak', 'en', 'UI.json')), 'ItemName': LO(P('kaynak', 'en', 'ItemName.json')), 'Bilgi_UI': {}}
    h = hashlib.sha1()
    for hd in hedefler:
        for k in sorted(tr[hd]): h.update(('%s\0%s\0%s\n' % (hd, k, tr[hd][k])).encode('utf-8'))
    surum = commit + '.' + h.hexdigest()[:8]
    # paket haritaları: anahtar -> paket
    k2p, pbas = {}, {}
    hd_dir = P('paketler', 'haritalar')
    for f in sorted(os.listdir(hd_dir)) if os.path.isdir(hd_dir) else []:
        if not f.endswith('_harita.json'): continue
        d = L(os.path.join(hd_dir, f)); pk = d.get('_paket') or f[:-12]; pbas[pk] = d.get('_baslik') or ''
        sat = d.get('satirlar')
        for v in (sat.values() if isinstance(sat, dict) else []):
            if isinstance(v, list) and v and isinstance(v[0], str): k2p.setdefault(v[0], []).append(pk)
    sahne = {}
    sd = P('araclar', 'sahne')
    for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
        if f.endswith('.json'): sahne[f[:-5]] = L(os.path.join(sd, f))
    olay = sahne.pop('_olaylar', {})
    olay_baska = {}
    for pk0, d0 in sahne.items():
        for k0, v0 in d0.items():
            if not k0.startswith('_') and not k0.endswith('*') and isinstance(v0, str): olay_baska.setdefault(k0, (v0, pk0))
    bolum_npc, bolum_ui, bolum_ayar, bolum_diger = [], [], [], []
    # --- NPC
    bg = LO(P('kaynak', 'RadioData_lua_baglam.json'))
    G = {g[0]: Grup(g[0], g[1], g[2], g[3], 'RadioData_lua', 'npc', g[4]) for g in NPC_GRUP}
    for key, t in tr['RadioData_lua'].items():
        v = bg.get(key) or ['(bağlam kaydı yok)']
        f = v[0]; ev = v[1] if len(v) > 1 and v[1] else '(olay adı yok)'; cond = ' | '.join(x for x in v[2:] if x)
        g = G[npc_grup(f)]; note, src, lv = None, '', 0
        for pk in reversed(k2p.get(key, [])):
            note = not_bul(sahne.get(pk), ev)
            if note:
                src, lv = pk, 2; s = sahne[pk]
                g.paket.setdefault(pk, [s.get('_baslik', ''), s.get('_genel', '')]); break
        if not note:
            note = not_bul(olay, ev)
            if note: src, lv = 'ortak', 1
        if not note and ev in olay_baska:
            note, src, lv = olay_baska[ev][0], '~' + olay_baska[ev][1], 1
        if not note:
            for pk in reversed(k2p.get(key, [])):
                s0 = sahne.get(pk)
                if s0 and s0.get('_genel'):
                    src, lv = '+' + pk, 1
                    g.paket.setdefault('+' + pk, [s0.get('_baslik', ''), s0.get('_genel', '')]); break
        g.ekle(ev, key, en['RadioData_lua'].get(key), t, (f, cond, note or '', lv, src))
    for g in NPC_GRUP: bolum_npc.append(G[g[0]].yaz(out))
    # --- Arayüz
    ui_bg = {'IG_UI': {}, 'IG_UI_lua': dict(LO(P('kaynak', 'IG_UI_kacan_baglam.json')), **LO(P('kaynak', 'IG_UI_lua_baglam.json'))), 'Creator_lua': LO(P('kaynak', 'Creator_lua_baglam.json'))}
    ui_ad = {'IG_UI': ('Oyun içi arayüz', 'Modun kendi çeviri dosyasından gelen arayüz metinleri.'), 'IG_UI_lua': ('Lua içinden çizilen arayüz', 'Lua dosyalarında anahtarsız yazılmış, yamayla çevrilen metinler.'), 'Creator_lua': ('Oluşturucu', 'NPC ve fraksiyon oluşturucu ekranları.')}
    for hd in ['IG_UI', 'IG_UI_lua', 'Creator_lua']:
        g = Grup('ui-' + hd, ui_ad[hd][0], ui_ad[hd][1], 'onayli/%s.json' % hd, hd, 'ui'); yok = 0
        for key, t in tr[hd].items():
            v = ui_bg[hd].get(key)
            if v:
                f, _, ln = v[0].partition(':'); extra = ' | '.join(x for x in v[1:] if x)
                g.ekle(insan(f), key, en[hd].get(key), t, (v[0], extra, '', 2, 'lua'))
            elif k2p.get(key) and pbas.get(k2p[key][-1]):
                pk = k2p[key][-1]; g.ekle(pbas[pk], key, en[hd].get(key), t, ('', '', '', 1, pk))
            else:
                g.ekle('Bağlam kaydı yok · %d–%d' % (yok // 150 * 150 + 1, yok // 150 * 150 + 150), key, en[hd].get(key), t, ('', '', '', 0, '')); yok += 1
        bolum_ui.append(g.yaz(out))
    # satır numarasını da sakla: bağlam dizisi ayrı dosyada tutulmaz, ctx[0] dosya adıdır
    # --- Sandbox
    g = Grup('ayar-Sandbox', 'Sandbox ayarları', 'Dünya ayarları ekranındaki seçenekler ve açıklamaları.', 'onayli/Sandbox.json', 'Sandbox', 'sandbox')
    for key, t in tr['Sandbox'].items():
        rest = key.split('.', 1)[1] if '.' in key else key.replace('Sandbox_', '', 1)
        g.ekle(rest.split('_')[0], key, en['Sandbox'].get(key), t, ('', '', '', 1, 'onek'))
    bolum_ayar.append(g.yaz(out, sirala=False))
    # --- Diğer
    dg = {'UI': ('Tuş atamaları', 'Seçenekler ekranındaki tuş atama satırları.'), 'ItemName': ('Eşya adları', 'Modun eklediği eşyalar.'), 'Bilgi_UI': ('Yama bilgi kutusu', 'Türkçe yamanın kendi bilgi penceresi. İngilizce kaynağı yok.')}
    for hd in ['UI', 'ItemName', 'Bilgi_UI']:
        g = Grup('diger-' + hd, dg[hd][0], dg[hd][1], 'onayli/%s.json' % hd, hd, 'duz')
        for key, t in tr[hd].items(): g.ekle(dg[hd][0], key, en[hd].get(key), t, ('', '', '', 0, ''))
        bolum_diger.append(g.yaz(out))
    kapsam, eslesmeyen = [], {'en_var_tr_yok': {}, 'tr_var_en_yok': {}}
    tum = {x['hedef']: 0 for x in bolum_npc + bolum_ui + bolum_ayar + bolum_diger}
    for x in bolum_npc + bolum_ui + bolum_ayar + bolum_diger: tum[x['hedef']] += x['satir']
    for hd in hedefler:
        a1 = [[k, en[hd][k]] for k in en[hd] if k not in tr[hd]] if hd != 'IG_UI_lua' else [[k, v] for k, v in LO(P('kaynak', 'IG_UI_lua.json')).items() if k not in tr[hd]]
        a2 = [k for k in tr[hd] if k not in en[hd]]
        if a1: eslesmeyen['en_var_tr_yok'][hd] = a1
        if a2: eslesmeyen['tr_var_en_yok'][hd] = a2
        kapsam.append(dict(hedef=hd, onayli=len(tr[hd]), katalogda=tum.get(hd, 0), disarida=len(tr[hd]) - tum.get(hd, 0), en_yok=len(a2), tr_yok=len(a1)))
    kat = dict(surum=surum, commit=commit, uretim=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        bolumler=[dict(id='npc', ad='NPC konuşmaları', gruplar=bolum_npc), dict(id='ui', ad='Arayüz', gruplar=bolum_ui),
                  dict(id='ayar', ad='Ayarlar', gruplar=bolum_ayar), dict(id='diger', ad='Diğer', gruplar=bolum_diger)],
        kapsam=kapsam, eslesmeyen=eslesmeyen)
    W(os.path.join(out, 'katalog.json'), kat)
    print('katalog', surum)
    for k in kapsam: print(' ', k)
    for b in kat['bolumler']:
        for g in b['gruplar']: print('  %-18s %-36s satır %6d sahne %5d düzey %s' % (g['id'], g['ad'], g['satir'], g['sahne'], g['duzey']))
    print('harita anahtarı', len(k2p), 'RD eşleşen', sum(1 for k in tr['RadioData_lua'] if k in k2p))

if __name__ == '__main__': main()
