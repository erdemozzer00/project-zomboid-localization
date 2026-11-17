import json,re,sys,glob,collections
sys.path.insert(0,'araclar')
from lua_cikar import MOD,h
from lua_dize import dizeler
from diyalog_cikar import goster
keys=set()
for f in ['kaynak/RadioData_lua.json','kaynak/IG_UI_lua.json','kaynak/Creator_lua.json','kaynak/en/IG_UI.json','kaynak/en/UI.json','kaynak/en/Sandbox.json','kaynak/en/ItemName.json']:
    try: keys|=set(json.load(open(f,encoding='utf-8')).keys())
    except Exception as e: print('yok',f)
for f in glob.glob('rapor/*_harita.json'):
    try:
        x=json.load(open(f,encoding='utf-8'))
        for v in x['satirlar'].values(): keys.add(v[0])
    except: pass
print(len(keys))
eng=re.compile(r"[A-Za-z]{2,}")
rows=[]
for p in MOD.parent.parent.rglob('*.lua'):
    rel=p.relative_to(MOD).as_posix()
    if 'Translate' in rel or '/Audio/' in rel or '/Admin/' in rel or 'Experiments' in rel or 'Debug' in rel or 'Voice' in rel: continue
    s=p.read_text(encoding='utf-8',errors='replace')
    for pos,t in dizeler(s):
        if len(t)<4 or ' ' not in t.strip() or not re.search(r"[a-z]{2,}",t): continue
        if re.search(r'[=_<>/]|\.lua|\[|\]',t): continue
        cand={"RD_ALifeRadio_"+h(t),"RD_ALifeRadio_"+h(goster(t)),"RD_ALifeLine_"+h(goster(t)),"RD_ALifeLine_"+h(t),"IGUI_ALifeUI_"+h(t),"IGUI_ALifeUI_"+h(goster(t)),"IGUI_ALifeTR_"+h(t)}
        # sentence-ish punctuation variants
        for v in (t.rstrip('.!?'),t.rstrip('.')+'.',t.rstrip('.!?')+'.',t.rstrip('.!?')+'?'):
            cand.add("RD_ALifeLine_"+h(goster(v)))
        if cand & keys: continue
        line=s.count('\n',0,pos)+1
        rows.append((rel,line,t))
json.dump(rows,open('rapor/ceviri_bosluk_tara.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
c=collections.Counter(r[0] for r in rows)
print(len(rows))
for k,v in c.most_common(40): print(v,k)
