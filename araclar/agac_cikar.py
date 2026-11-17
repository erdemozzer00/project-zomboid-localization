"""1.5.0 konuşma ağaçlarını modun kendi Lua koduyla (lupa) okur; harici_paket.py hazirla-agac bunu kullanır.

Kaynaklar (ana mod, kurulu Workshop kopyası):
  shared/ProjectALife/Talk/Trees/Data/ALifeTrees_*.lua   ağaçlar (tab: Personal/World/Orders/Info/Trade/Tasks) + barks (lines)
  shared/ProjectALife/Talk/ALifeTalkTreesData.lua         eski konuşma ekranındaki zincirli sorular (TT_*)
  shared/ProjectALife/Captives/ALifeCaptiveTreesData.lua  esir sorgusu cevapları

Anahtarlar oyunun ekrana bastığı metnin hash'i; hepsi modun gerçek fonksiyonlarıyla hesaplanır (2026-11-09, kod okuması):
  NPC düğüm sözü   TreeServer.say: Speech.render(E.clean(satır)) -> AudioPolicy.caption -> RD_ALifeLine_ (ek)
  bark (lines)     TreeLines.records {t = E.clean} -> Talk.speak -> Speech.render -> caption -> RD_ALifeLine_
  oyuncu sorusu    E.offer: E.clean(E.fill(prompt)) düğmede ham çizilir -> ek, RD_ALifeLine_ + hash (büyük harf YOK)
  oyuncu seçeneği  nodeView: E.label(E.clean(text)) ("[Charm] " öneki) -> ek öneki söküp gövdeyi çevirir; anahtar gövdenin
  TT_* düğmesi/impact/risk ve esir sorusu/impact   Talk2.text = Text.ui -> IGUI_ALifeUI_ (arayüz, IG_UI_lua)
  TT_* NPC cevabı ve esir cevapları   FactionTalkLines.sets -> Talk.speak -> render -> caption -> RD_ALifeLine_
Oyunda dolan yer tutuculu metinler ({name}, {town}, {playerName}…) hash'i tutmaz: dışarıda, sayısı raporlanır.
Esirlerin gün tablosundaki 'ask' alanı oyunda gösterilmiyor (düğme CT.asks'tan): alınmaz.
"""
from pathlib import Path

from lupa.lua51 import LuaRuntime

MOD_LUA = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\108600"
               r"\3803984183\mods\ProjectALifeNPCs\42.20\media\lua")
VERI = MOD_LUA / "shared/ProjectALife/Talk/Trees/Data"
MOD_DOSYALARI = (
    "shared/ProjectALife/Core/ALifeText.lua",
    "shared/ProjectALife/Audio/ALifeAudioPolicy.lua",
    "shared/ProjectALife/Talk/ALifeSpeech.lua",
    "shared/ProjectALife/Talk/Trees/ALifeTreeRegistry.lua",
    "shared/ProjectALife/Talk/Trees/ALifeTreeEngine.lua",
    "shared/ProjectALife/Talk/ALifeTalkTreesData.lua",
    "shared/ProjectALife/Talk/ALifeTalkTrees.lua",
    "shared/ProjectALife/Captives/ALifeCaptiveTreesData.lua",
    "shared/ProjectALife/Captives/ALifeCaptiveTrees.lua",
)

YARDIMCI = r"""
function A_gosterilen(s)  -- NPC sözü / bark: oyunun ekrana bastığı metin, yoksa nil
    local t = ProjectALife.TreeEngine.fill(s, {})
    if t == nil then return nil end
    t = ProjectALife.Speech.render(ProjectALife.TreeEngine.clean(t), {}, nil, nil)
    return ProjectALife.AudioPolicy.caption(t)
end
function A_dugme(s)  -- soru / seçenek: E.clean(E.fill(s)), büyük harf yok
    local t = ProjectALife.TreeEngine.fill(s, {})
    if t == nil then return nil end
    return ProjectALife.TreeEngine.clean(t)
end
function A_sira(tree)  -- düğümler start'tan genişlik öncelikli (oyuncunun karşılaşma sırası), ulaşılmayanlar sonda
    local out, seen, q, i = {}, { start = true }, { "start" }, 1
    while i <= #q do
        local id = q[i]; i = i + 1
        out[#out + 1] = id
        local n = tree.nodes[id]
        local t = {}
        for _, c in ipairs(n._choices or {}) do
            if c.go then t[#t + 1] = c.go end
            local d = type(c.effect) == "table" and c.effect.negotiate or nil
            if type(d) == "table" then t[#t + 1] = d.win or c.go; t[#t + 1] = d.lose or c.go end
        end
        local d = type(n.effect) == "table" and n.effect.negotiate or nil
        if type(d) == "table" then t[#t + 1] = d.win; t[#t + 1] = d.lose end
        if n.next then t[#t + 1] = n.next end
        for _, x in ipairs(t) do if x and not seen[x] and tree.nodes[x] then seen[x] = true; q[#q + 1] = x end end
    end
    local rest = {}
    for id in pairs(tree.nodes) do if not seen[id] then rest[#rest + 1] = id end end
    table.sort(rest)
    for _, id in ipairs(rest) do out[#out + 1] = id end
    return out
end
"""


def _lua():
    lua = LuaRuntime(unpack_returned_tuples=True)
    g = lua.globals()
    dosyalar = {f.stem[len("ALifeTrees_"):]: f for f in VERI.glob("ALifeTrees_*.lua")}

    def yukle(yol):
        yol = str(yol)
        onek = "ProjectALife/Talk/Trees/Data/ALifeTrees_"
        if yol.startswith(onek) and yol[len(onek):] in dosyalar:
            return lua.execute(dosyalar[yol[len(onek):]].read_text(encoding="utf-8-sig"))
        return None

    g.A_yukle = yukle
    lua.execute("""
        require = function(p) return A_yukle(p) end
        ProjectALife = {}
        print = function() end
    """)
    for ad in MOD_DOSYALARI:
        lua.execute((MOD_LUA / ad).read_text(encoding="utf-8-sig"))
    lua.execute(YARDIMCI)
    g.ProjectALife.TreeRegistry.load()
    return lua, g


def _liste(t):
    return [] if t is None else [t[i] for i in range(1, len(t) + 1)]


def _kume(t):
    return sorted(str(k) for k, v in t.items() if v) if t is not None else []


def agaclar():
    """Y4 için: [{"tur": "agac"|"havuz"|"tt"|"esir", "baslik": [...], "satirlar": [(anahtar, en, etiket, yer)]}],
    sayac. Anahtar None ise satır yer tutuculu (çevrilemez); etiket bağlam için yine verilir."""
    lua, g = _lua()
    PA = g.ProjectALife
    R, Text = PA.TreeRegistry, PA.Text
    sayac = {"npc": 0, "soru": 0, "secenek": 0, "bark": 0, "tt_npc": 0, "esir": 0, "yer_tutuculu": 0,
             "reddedilen_agac": int(R.metrics.refused)}
    bloklar = []

    def satir(liste, tur, en, etiket, yer, dugme=False):
        goster = g.A_dugme(en) if dugme else g.A_gosterilen(en)
        if goster is None or "{" in goster:
            sayac["yer_tutuculu"] += 1
            liste.append((None, en, etiket, yer))
            return
        sayac[tur] += 1
        liste.append((Text.lineKey(goster), goster, etiket, yer))

    for tree in _liste(R.trees):
        tid, dosya = str(tree.id), f"ALifeTrees_{tree._file}.lua"
        who = tree.who
        kim = []
        if who is not None:
            for alan, ad in (("blocs", "blok"), ("roles", "rol"), ("professions", "meslek"), ("factions", "grup"),
                             ("temperaments", "huy"), ("names", "ad")):
                v = who[alan]
                if v is not None:
                    kim.append(f"{ad} " + ", ".join(_liste(v) if not isinstance(v, str) else [v]))
            if who.female is not None:
                kim.append("kadın" if who.female else "erkek")
        kosul = []
        if tree._dmin is not None or tree._dmax is not None:
            kosul.append(f"gün {tree._dmin or 0}-{tree._dmax if tree._dmax is not None else '…'}")
        if tree._stance is not None:
            kosul.append("tutum " + "/".join(_kume(tree._stance)))
        if tree.minRep is not None:
            kosul.append(f"itibar ≥ {tree.minRep}")
        if tree.once:
            kosul.append("tek seferlik")
        if tree.need is not None and tree.need.taskDone is not None:
            kosul.append("görev teslimi")
        baslik = [f"##### AĞAÇ {tid} · {tree._bloc} · sekme {tree._tab} #####",
                  "# KİM: " + ("; ".join(kim) or "herkes") + (" · " + " · ".join(kosul) if kosul else "")]
        satirlar = []
        satir(satirlar, "soru", tree.prompt, "OYUNCU SORUSU", [dosya, tid, "soru"], dugme=True)
        geldi = {}  # düğüm -> oraya götüren seçenek metni
        for nid in _liste(g.A_sira(tree)):
            node = tree.nodes[nid]
            npc = _liste(node._npc)
            ek = []
            if node.emote is not None:
                ek.append(f"ifade: {node.emote}")
            if node.finish is not None:
                ek.append("konuşma biter" + (f", ruh hâli {node.finish.mood}" if node.finish.mood is not None else ""))
            etiket = "NPC" + (f" ({'; '.join(ek)})" if ek else "")
            satirlar.append(("#", f"düğüm {nid}" + (f" ← \"{geldi[nid]}\"" if nid in geldi else ""), None, None))
            for j, s in enumerate(npc, 1):
                e = etiket if len(npc) == 1 else etiket.replace("NPC", f"NPC {j}/{len(npc)} (biri seçilir)", 1)
                satir(satirlar, "npc", s, e, [dosya, tid, f"npc:{nid}"])
            for c in _liste(node._choices):
                hedef = c.go
                d = c.effect.negotiate if c.effect is not None else None
                if d is not None:
                    hedef = f"{d.win or c.go}/{d.lose or c.go} (ikna)"
                charm = bool(PA.TreeEngine.charmTagged(c))
                e = "OYUNCU SEÇENEĞİ" + (" [Charm]" if charm else "") + (f" → {hedef}" if hedef else " → konuşma biter")
                satir(satirlar, "secenek", c.text, e, [dosya, tid, f"secenek:{nid}"], dugme=True)
                if c.go is not None and str(c.go) not in geldi:
                    geldi[str(c.go)] = str(c.text)
        bloklar.append({"tur": "agac", "baslik": baslik, "satirlar": satirlar})

    for bloc in sorted(R.lines.keys()):
        store = R.lines[bloc]
        for olay in sorted(store.keys()):
            satirlar = []
            for s in _liste(store[olay]):
                satir(satirlar, "bark", s, "NPC", [f"ALifeTrees_{bloc}*.lua", f"{bloc}.{olay}", "bark"])
            ad, _, faz = str(olay).partition("@")
            bloklar.append({"tur": "havuz", "olay": ad, "faz": faz, "bloc": str(bloc),
                            "baslik": [f"##### HAVUZ {bloc} · {olay} #####"], "satirlar": satirlar})

    kaynak = PA.TalkTreesData
    for tree in _liste(kaynak.trees):
        satirlar = []
        for node in _liste(tree.nodes):
            nid = str(node.id)
            satirlar.append(("#", f"oyuncu sorar: \"{node.text}\" (bu soru ve altındaki not arayüz paketinde)", None, None))
            for alan, ad in (("any", "sivil/işçi/kurtarıcı"), ("law", "polis/kolluk"), ("mil", "asker"), ("out", "kanun dışı/yağmacı")):
                for s in _liste(node[alan]):
                    satir(satirlar, "tt_npc", s, f"NPC ({ad})", ["ALifeTalkTreesData.lua", nid, alan])
        bloklar.append({"tur": "tt", "baslik": [f"##### SORU ZİNCİRİ {tree.id} #####"], "satirlar": satirlar})

    esir, CT = PA.CaptiveTreesData, PA.CaptiveTrees
    asks = _liste(CT.asks)
    birlesen = {str(v): str(k) for k, v in CT.merges.items()}
    for grup in _liste(CT.order):
        t = esir[grup]
        satirlar = []
        for gun, d in enumerate(_liste(t.days), 1):
            satirlar.append(("#", f"{gun}. gün, oyuncu sorar: \"{asks[gun - 1]}\"", None, None))
            for s in _liste(d.lines):
                satir(satirlar, "esir", s, f"ESİR ({gun}. gün)", ["ALifeCaptiveTreesData.lua", str(grup), f"gun{gun}"])
        for sonuc in ("strength_ok", "strength_fail", "talk_ok", "talk_fail", "silent"):
            for s in _liste(t.outcomes[sonuc]):
                satir(satirlar, "esir", s, f"ESİR ({ESIR_SONUC[sonuc]})", ["ALifeCaptiveTreesData.lua", str(grup), sonuc])
        bloklar.append({"tur": "esir", "baslik": [f"##### ESİR {grup} ({ESIR_GRUP.get(str(grup), grup)}) #####"],
                        "satirlar": satirlar})
    return bloklar, sayac


ESIR_SONUC = {"strength_ok": "zorla sorgu, konuşuyor", "strength_fail": "zorla sorgu, direniyor",
              "talk_ok": "ikna, konuşuyor", "talk_fail": "ikna, direniyor", "silent": "susuyor"}
ESIR_GRUP = {"civ": "sivil", "work": "işçi", "rescue": "kurtarıcı", "law": "kolluk", "mil": "asker",
             "out": "kanun dışı", "raid": "yağmacı"}


def arayuz():
    """Y5 için: [(anahtar, en, etiket, yer)] IGUI_ALifeUI_ anahtarlı düğme/not metinleri, bloklar hâlinde."""
    lua, g = _lua()
    PA = g.ProjectALife
    Text, Trees = PA.Text, PA.TalkTrees
    bloklar = []

    def ui(en):
        return Text.key("IGUI_ALifeUI_", en)

    bloklar.append({"tur": "sekme", "baslik": ["##### KONUŞMA PENCERESİ SEKME ADLARI #####",
                    "# Konuşma penceresinin üstündeki sekme düğmeleri (yanlarında 'Personal', 'World', 'Tasks'). Tek sözcük, kısa."],
                    "satirlar": [(ui(s), s, "SEKME", ["ALifeUI2TalkTrees.lua", "labels", s]) for s in ("Info", "Trade")]})
    for tree in _liste(PA.TalkTreesData.trees):
        satirlar = []
        for node in _liste(tree.nodes):
            nid = str(node.id)
            satirlar.append((ui(node.text), str(node.text), "OYUNCU SORUSU (düğme)", ["ALifeTalkTreesData.lua", nid, "text"]))
            satirlar.append((ui(node.impact), str(node.impact), "NOT (düğmenin altındaki kısa açıklama)",
                             ["ALifeTalkTreesData.lua", nid, "impact"]))
            risk = Trees.riskOf(node.need)
            if risk is not None:
                satirlar.append((ui(risk), str(risk), "KOŞUL NOTU", ["ALifeTalkTreesData.lua", nid, "risk"]))
        bloklar.append({"tur": "tt", "baslik": [f"##### SORU ZİNCİRİ {tree.id} #####",
                        "# Oyuncunun konuşma penceresinde seçtiği sorular; her soru bir öncekine cevap gelince açılır."],
                        "satirlar": satirlar})
    CT = PA.CaptiveTrees
    satirlar = []
    for gun, (a, i) in enumerate(zip(_liste(CT.asks), _liste(CT.impacts)), 1):
        satirlar.append((ui(a), str(a), f"OYUNCU SORUSU ({gun}. gün, düğme)", ["ALifeCaptiveTrees.lua", "asks", str(gun)]))
        satirlar.append((ui(i), str(i), "NOT (düğmenin altındaki kısa açıklama)", ["ALifeCaptiveTrees.lua", "impacts", str(gun)]))
    bloklar.append({"tur": "esir", "baslik": ["##### ESİR SORGUSU #####",
                    "# Esir alınmış NPC'ye her gün bir yenisi açılan sorular (düğme) ve altlarındaki not."], "satirlar": satirlar})
    return bloklar


if __name__ == "__main__":
    b, s = agaclar()
    print(len(b), "blok", s)
    print(sum(len(x["satirlar"]) for x in arayuz()), "arayüz satırı")
