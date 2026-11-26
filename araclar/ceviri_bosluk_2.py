import json,re,sys,glob,collections
sys.path.insert(0,'araclar')
from lua_cikar import MOD
norm=lambda s: re.sub(r"[^a-z0-9{}]","",s.lower())
known=set()
for f in ['kaynak/RadioData_lua.json','kaynak/IG_UI_lua.json','kaynak/Creator_lua.json','kaynak/en/IG_UI.json','kaynak/en/UI.json','kaynak/en/Sandbox.json']:
    known|={norm(v) for v in json.load(open(f,encoding='utf-8')).values() if isinstance(v,str)}
for f in glob.glob('paketler/haritalar/*_harita.json'):
    try:
        for v in json.load(open(f,encoding='utf-8'))['satirlar'].values(): known.add(norm(v[1]))
    except: pass
rows=json.load(open('rapor/ceviri_bosluk_tara.json',encoding='utf-8'))
real=[r for r in rows if norm(r[2]) not in known]
print(len(rows),len(real))
c=collections.Counter(r[0] for r in real)
for k,v in c.most_common(45): print(v,k)
json.dump(real,open('rapor/ceviri_bosluk_tara2.json','w',encoding='utf-8'),ensure_ascii=False)
