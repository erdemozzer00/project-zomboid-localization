"""Tablo içi liste değerlerindeki NPC sözlerini (kacan_tara.py'nin görmediği `lines = { "…" }`) modun kendi Lua'sıyla okur.

Rapor: rapor/kacan_listeler_1.5.0.md. Girdiler: python -X utf8 araclar/harici_paket.py hazirla-liste-soz Y7
(durum/esir/çağrı sorusu) ve hazirla-bitis-soz Y9 --yeni (telsiz kartı + pilot)

Gösterim yolları (kod okuması, 2026-11-09, mod 1.5.0):
  durum    SituationsData.situations[].lines  S.lineRecords {t} -> Talk.speak -> Speech.render -> Speech.say -> AudioPolicy.caption
           -> ek: RD_ALifeLine_ + hash(gösterilen)                                                        ÇEVRİLEBİLİR
  esir     CaptivesData.lines[anahtar][grup]  FactionTalkLines.sets -> FS.say -> FT.recordsFor {t} -> Talk.speak -> render
           -> caption -> RD_ALifeLine_                                                                      ÇEVRİLEBİLİR
  çağrı    EndingCallData.nodes[].lines/alt/again  Run.offerNode: d.offer(…, concat(Call.fill(satır), ", ")) -> standoffAsk
           -> UI2Answer.clean -> ek kurSoru: RD_ALifeLine_ + hash(BİRLEŞİK metin)                         ÇEVRİLEBİLİR (birleşik)
           aynı satırlar ayrıca Run.airLines -> RadioChannel.air (Java RadioLine) ve Run.card -> RadioClient.card
           (args.text ham) yolundan da çıkar: ikisinde çeviri yolu YOK
  çağrı    leaves/reminders/failure/arrival/cut lines  telsiz yayını (Java RadioLine, sunucu)               YOL YOK (sarılmaz)
  bitiş    EndingData.lines broadcast/reply/missed  Director.airLines -> yayın                               YOL YOK (sarılmaz)
  kart     yayının İLK satırı -> RadioClient.card (args.text) -> ek kurKart: RD_ALifeLine_, yoksa IGUI_ALifeUI_  ÇEVRİLEBİLİR (Y9)
  pilot    EndingData.talk intro/outro/beats reply, lines.pilot  Director.pilotSay -> "endingSay" -> EndingClient.say
           (altyazı ya da bildirim) -> ek kurPilot                                                           ÇEVRİLEBİLİR (Y9)
           aynı söz World.crewSay -> body:Say ile pilotun başı üstünde de çıkar (sunucu, ağa gider)          sarılmaz
"""
import json
import sys
from pathlib import Path

from lupa.lua51 import LuaRuntime

KOK = Path(__file__).resolve().parent.parent
MOD_LUA = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\108600"
               r"\3803984183\mods\ProjectALifeNPCs\42.20\media\lua")
MOD_DOSYALARI = (
    "shared/ProjectALife/Core/ALifeText.lua",
    "shared/ProjectALife/Audio/ALifeAudioPolicy.lua",
    "shared/ProjectALife/Talk/ALifeSpeech.lua",
    "shared/ProjectALife/Situations/ALifeSituationsData.lua",
    "shared/ProjectALife/Captives/ALifeCaptivesData.lua",
    "shared/ProjectALife/Ending/ALifeEndingData.lua",
    "shared/ProjectALife/Ending/ALifeEndingRules.lua",
    "shared/ProjectALife/Ending/ALifeEndingCallData.lua",
    "shared/ProjectALife/Ending/ALifeEndingCall.lua",
)
YARDIMCI = r"""
function L_gosterilen(s)  -- Talk.speak yolu: Speech.render (değişkensiz, shell yok) -> AudioPolicy.caption
    local t = ProjectALife.Speech.render(s, {}, nil, nil)
    if t == nil then return nil end
    return ProjectALife.AudioPolicy.caption(t)
end
function L_cagri(liste)  -- Run.offerNode: Call.fill(satır, Call.vars(ad)) ", " ile birleşir; ad bilinmez -> "\1"
    local vars = ProjectALife.EndingCall.vars("\1")
    local out = {}
    for i = 1, #liste do out[i] = ProjectALife.EndingCall.fill(liste[i], vars) end
    return table.concat(out, ", ")
end
"""
YER = ("durum", "esir", "cagri_soru", "kart", "pilot", "cagri_yolsuz", "bitis_yolsuz")


def _lua():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("require = function() end; ProjectALife = {}; print = function() end")
    for ad in MOD_DOSYALARI:
        lua.execute((MOD_LUA / ad).read_text(encoding="utf-8-sig"))
    lua.execute(YARDIMCI)
    return lua, lua.globals()


def _liste(t):
    return [] if t is None else [t[i] for i in range(1, len(t) + 1)]


def _sirali(t):
    return sorted(((str(k), v) for k, v in t.items()), key=lambda x: x[0]) if t is not None else []


def cikar():
    """[{"tur", "kaynak", "yer", "en" (ham), "goster" (oyunda), "anahtar" (RD_ALifeLine_ | None), "neden"}]"""
    lua, g = _lua()
    PA = g.ProjectALife
    Text = PA.Text
    out = []

    def ekle(tur, kaynak, yer, en, goster=None, neden=""):
        k = None
        if goster is not None:
            if "{" in goster or "\1" in goster:
                neden, goster = "yer tutuculu (oyunda dolar, hash tutmaz)", goster.replace("\1", "{name}")
            else:
                k = Text.lineKey(goster)
        out.append({"tur": tur, "kaynak": kaynak, "yer": yer, "en": str(en), "goster": goster, "anahtar": k, "neden": neden})

    for sit in _liste(PA.SituationsData.situations):
        for key, liste in _sirali(sit.lines):
            for s in _liste(liste):
                ekle("durum", "ALifeSituationsData.lua", [str(sit.id), str(sit.label), key], s, g.L_gosterilen(s))

    for key, grup_tablo in _sirali(PA.CaptivesData.lines):
        for grup, liste in _sirali(grup_tablo):
            for s in _liste(liste):
                ekle("esir", "ALifeCaptivesData.lua", [key, grup], s, g.L_gosterilen(s))

    C = PA.EndingCallData
    for nid, node in _sirali(C.nodes):
        cesitler = [("lines", node.lines)] + [(f"alt{i}", a.lines) for i, a in enumerate(_liste(node.alt), 1)]
        if node.again is not None:
            cesitler.append(("again", node.again))
        soru = node.opts is not None and len(_liste(node.opts)) > 0
        for ad, liste in cesitler:
            satirlar = _liste(liste)
            if not satirlar:
                continue
            if soru:
                ekle("cagri_soru", "ALifeEndingCallData.lua", [nid, ad, "birleşik"], ", ".join(map(str, satirlar)),
                     g.L_cagri(liste))
            for s in satirlar:
                ekle("cagri_yolsuz", "ALifeEndingCallData.lua", [nid, ad], s, neden="telsiz yayını (Java RadioLine) + kart, ham")
    for alan in ("leaves", "arrival"):
        for nid, x in _sirali(C[alan]):
            for s in _liste(x.lines):
                ekle("cagri_yolsuz", "ALifeEndingCallData.lua", [alan, nid], s, neden="telsiz yayını (Java RadioLine), ham")
    for alan in ("reminders", "failure"):
        for i, x in enumerate(_liste(C[alan]), 1):
            for s in _liste(x.lines):
                ekle("cagri_yolsuz", "ALifeEndingCallData.lua", [alan, str(x.id or i)], s, neden="telsiz yayını (Java RadioLine), ham")
    for s in _liste(C.cut.lines):
        ekle("cagri_yolsuz", "ALifeEndingCallData.lua", ["cut"], s, neden="telsiz yayını (Java RadioLine), ham")

    # Telsiz kartı (ek kurKart): kart metni yayının İLK satırı (Run.card / Director.airLines: lines[1].text). Yapraklarda ilk
    # satır oyuncunun seçtiği etiket (Run.finish lead = label; Y6, IGUI_ALifeUI_), düğümlerde kart yok (offerNode yalnız yayın).
    E = PA.EndingData
    kart = [(["arrival", k], x.lines) for k, x in _sirali(C.arrival)]
    kart += [(["reminders", str(x.id)], x.lines) for x in _liste(C.reminders)]
    kart += [(["failure", str(i)], x.lines) for i, x in enumerate(_liste(C.failure), 1)]
    kart += [(["cut"], C.cut.lines), (["nodes", "open", "alt1 (geri dönüş, startLines)"], C.nodes.open.alt[1].lines)]
    kart += [(["lines", tur], E.lines[tur]) for tur in ("broadcast", "reply", "missed")]
    for yer, liste in kart:
        s = _liste(liste)[0]
        ekle("kart", "ALifeEndingData.lua" if yer[0] == "lines" else "ALifeEndingCallData.lua", yer + ["1"], s, g.L_cagri(lua.table_from([s])))

    for tur in ("broadcast", "reply", "missed"):
        for s in _liste(E.lines[tur]):
            ekle("bitis_yolsuz", "ALifeEndingData.lua", ["lines", tur], s, neden="telsiz yayını (Java RadioLine), ham")

    # Pilot (ek kurPilot): Director.pilotSay -> endingSay -> EndingClient.say (altyazı/bildirim). board/ready/waiting ayrıca
    # Director.offer ile cevap şeridinin sorusu (kurSoru), aynı metin. waiting {minutes} = numbers.waitMoreMinutes ile dolar.
    for ad, s in _sirali(E.lines.pilot):
        goster = g.ProjectALife.EndingRules.fill(s, lua.table_from({"minutes": E.numbers.waitMoreMinutes})) if ad == "waiting" else s
        ekle("pilot", "ALifeEndingData.lua", ["lines.pilot", ad], s, goster)
    for ad in ("intro", "outro"):
        ekle("pilot", "ALifeEndingData.lua", ["talk", ad], E.talk[ad], E.talk[ad])
    for b in _liste(E.talk.beats):
        ekle("pilot", "ALifeEndingData.lua", ["talk.beats", str(b.id), "silent"], b.silent.reply, b.silent.reply)
        for o in _liste(b.options):
            ekle("pilot", "ALifeEndingData.lua", ["talk.beats", str(b.id), str(o.id)], o.reply, o.reply)
    return out


def bilinen():
    """Çeviri yolunda olan RD_ALifeLine_ anahtarları: kaynak/RadioData_lua.json + bekleyen haritalar (Y7 hariç)."""
    k = set(json.loads((KOK / "kaynak" / "RadioData_lua.json").read_text(encoding="utf-8")))
    for f in (KOK / "paketler/haritalar").glob("*_harita.json"):
        if f.name == "Y7_harita.json":
            continue
        for v in json.loads(f.read_text(encoding="utf-8")).get("satirlar", {}).values():
            if isinstance(v, list) and v and isinstance(v[0], str):
                k.add(v[0])
    return k


ESIR_GRUP = {"civ": "sivil", "work": "işçi", "rescue": "kurtarıcı", "law": "kolluk", "mil": "asker", "out": "kanun dışı",
             "raid": "yağmacı", "any": "diğer"}
ESIR_SONUC = {
    "CAP_FEED.ok": "yemek ve su verilince", "CAP_FEED.again": "bugün zaten yemişken", "CAP_FEED.no": "oyuncunun verecek yiyeceği/suyu yokken",
    "CAP_INTEL.hit": "konuşur, bir yer söyler", "CAP_INTEL.miss": "söylemez", "CAP_INTEL.cold": "bugün zaten soruldu ya da küskün",
    "CAP_INTEL.done": "bildiği her şeyi söylemiş", "CAP_INTEL.none": "söyleyecek bir yer bilmiyor",
    "CAP_FORCE.hit": "zorla sorguda konuşur", "CAP_FORCE.miss": "zorla sorguda direnir",
    "CAP_RELEASE.ok": "serbest bırakılınca", "CAP_HAND.ok": "kolluğa teslim edilirken", "CAP_JOIN.ok": "katılmayı kabul eder",
    "CAP_JOIN.no": "henüz katılmaz", "CAP_KILL.ok": "öldürülmeden hemen önce",
}
DURUM_EK = {"again": "aynı satır yeniden seçilince", "none": "koşul tutmadığında"}
Y7_NEREDE = {
    "durum": ("oyuncu kuşatılmış, yolu kesmiş ya da işi başından aşkın bir grupla karşılaşır; NPC'lerden biri yaklaşınca konuşur "
              "(karşılaşınca), oyuncu konuşma penceresinden bir satır seçince cevap verir. Aynı etiketli satırlardan biri rastgele söylenir"),
    "esir": ("oyuncunun elindeki esir, oyuncu konuşma penceresinden bu satırı seçince cevap verir. Cevap esirin kim olduğuna "
             "(etiketteki grup) ve duruma göre seçilir; aynı etiketli satırlardan biri rastgele söylenir"),
    "cagri": ("bitiş görevinde ordu telsizden oyuncuyu arar. Bu satır, oyuncunun cevap seçtiği şeridin üstünde TEK bir soru metni "
              "olarak görünür: ordunun ayrı ayrı söylediği cümleler oyunda ', ' ile art arda eklenmiş. Cümleleri aynı sırayla çevir, "
              "aralarına yine ', ' koy (cümle sonuna nokta koyma, son cümle hariç)"),
}


def _y7_satir(s, yazilan, bilinenler, etiket):
    """(k, en, etiket, yer) | ("·", etiket, en): bilinen ya da tekrar anahtar bağlam olur, yer tutuculu hiç yazılmaz."""
    k = s["anahtar"]
    if k is None:
        return None
    if k in bilinenler or k in yazilan:
        return ("·", etiket, s["goster"])
    yazilan.add(k)
    return (k, s["goster"], etiket, [s["kaynak"]] + s["yer"])


def y7_bloklari(bilinenler):
    """harici_paket._bloklari_yaz biçiminde Y7 blokları: [(başlık satırları, [satır | ("#", not) | ("·", etiket, en)])]."""
    lua, g = _lua()
    PA = g.ProjectALife
    satirlar = cikar()
    yazilan, bloklar = set(), []

    def ust(baslik, nerede):
        return [f"##### {baslik} #####", "# NEREDE: " + Y7_NEREDE[nerede]]

    # Durumlar: durum başına blok; karşılaşma sözü, sonra her satır için oyuncunun seçeneği (bağlam) ve NPC cevapları
    durum = {}
    for s in satirlar:
        if s["tur"] == "durum":
            durum.setdefault(s["yer"][0], []).append(s)
    for sit in _liste(PA.SituationsData.situations):
        liste = durum.get(str(sit.id), [])
        sira = ["enter"] + [str(r.key) for r in _liste(sit.rows)]
        secenek = {str(r.key): str(r.text) for r in _liste(sit.rows)}
        govde = []

        def ekle(anahtar):
            taban, _, ek = anahtar.partition(".")
            et = "NPC (karşılaşınca)" if taban == "enter" else "NPC (cevap" + (f", {DURUM_EK.get(ek, ek)}" if ek else "") + ")"
            for s in liste:
                if s["yer"][2] == anahtar:
                    x = _y7_satir(s, yazilan, bilinenler, et)
                    if x:
                        govde.append(x)

        anahtarlar = sorted({s["yer"][2] for s in liste})
        for taban in sira:
            if taban != "enter":
                govde.append(("·", "OYUNCU SEÇENEĞİ", secenek[taban]))
            for a in [a for a in anahtarlar if a == taban or a.startswith(taban + ".")]:
                ekle(a)
        for a in anahtarlar:  # satırı olmayan anahtar (olmamalı) sona
            if a.partition(".")[0] not in sira:
                ekle(a)
        if any(x[0] != "·" for x in govde):
            bloklar.append((ust(f"DURUM · {sit.label} · NPC SÖZLERİ", "durum"), govde))

    # Esir: oyuncunun satırı (CAP_FEED…) başına blok; aynı listeyi paylaşan gruplar tek etikette
    esir_satir = {str(r.id): str(r.text) for r in _liste(PA.CaptivesData.rows)}
    esir = {}
    for s in satirlar:
        if s["tur"] == "esir":
            esir.setdefault(s["yer"][0], {}).setdefault(s["yer"][1], []).append(s)
    for rid in [str(r.id) for r in _liste(PA.CaptivesData.rows)]:
        govde = [("·", "OYUNCU SEÇENEĞİ", esir_satir[rid])]
        for anahtar in sorted(a for a in esir if a.partition(".")[0] == rid):
            gruplar = esir[anahtar]
            sonuc = ESIR_SONUC.get(anahtar)
            if sonuc is None and anahtar.startswith("CAP_CHAT.t"):
                n = anahtar[len("CAP_CHAT.t"):]
                sonuc = f"hâl hatır, {n}. kademe ({'küskün ya da hiç beslenmemiş' if n == '0' else f'{n} gün beslenmiş'})"
            paylasan = {}
            for grup in ESIR_GRUP:
                if grup in gruplar:
                    paylasan.setdefault(tuple(s["en"] for s in gruplar[grup]), []).append(grup)
            for _, adlar in paylasan.items():
                et = f"ESİR ({'/'.join(ESIR_GRUP[a] for a in adlar)} · {sonuc})"
                for s in gruplar[adlar[0]]:
                    x = _y7_satir(s, yazilan, bilinenler, et)
                    if x:
                        govde.append(x)
        if any(x[0] != "·" for x in govde):
            bloklar.append((ust(f"ESİR · {esir_satir[rid]}", "esir"), govde))

    # Telsiz çağrısı: düğüm başına blok, oyuncunun karşılaşma sırasıyla (open'dan opts[].to genişlik öncelikli)
    C = PA.EndingCallData
    sira, gor, i = [str(C.numbers.startNode)], {str(C.numbers.startNode)}, 0
    while i < len(sira):
        node = C.nodes[sira[i]]
        i += 1
        for o in _liste(node.opts):
            if o.to is not None and str(o.to) not in gor and C.nodes[o.to] is not None:
                gor.add(str(o.to))
                sira.append(str(o.to))
    sira += sorted(str(k) for k in C.nodes.keys() if str(k) not in gor)
    cagri = {}
    for s in satirlar:
        if s["tur"] == "cagri_soru":
            cagri.setdefault(s["yer"][0], []).append(s)
    for nid in sira:
        node = C.nodes[nid]
        kim = str(C.who[node.who].name)
        govde = []
        for s in cagri.get(nid, []):
            ad = s["yer"][1]
            durum_notu = "" if ad == "lines" else (", aynı düğüme yeniden gelince" if ad == "again" else ", koşullu çeşit")
            x = _y7_satir(s, yazilan, bilinenler, f"TELSİZ ({kim}, cevap şeridinin sorusu{durum_notu})")
            if x:
                govde.append(x)
        if any(x[0] != "·" for x in govde):
            govde += [("·", "OYUNCU SEÇENEĞİ", str(o.label)) for o in _liste(node.opts)]
            bloklar.append((ust(f"BİTİŞ · TELSİZ ÇAĞRISI · {nid}", "cagri"), govde))
    return bloklar


Y9_NEREDE = {
    "kart": ("bitiş görevinde ordu telsizden yayın yapar; ekranın köşesinde 'Ad: metin' biçiminde kısa bir telsiz kartı çıkar. "
             "Kartta yayının yalnız İLK cümlesi görünür. Sesli telsiz anonsu gibi, kısa ve resmî"),
    "pilot": ("kurtarma helikopterinde pilot oyuncuyla konuşur: söz ekranın altında altyazı (ya da köşede bildirim) olarak çıkar. "
              "Pilotun sorusu ve oyuncunun cevabı '·' bağlam; satır pilotun o cevaba karşılığı"),
}


def y9_bloklari(bilinenler):
    """Telsiz kartı ve pilot sözleri (ek kurKart/kurPilot) -> harici_paket._bloklari_yaz blokları."""
    lua, g = _lua()
    E = g.ProjectALife.EndingData
    satirlar = {(s["tur"], tuple(s["yer"])): s for s in cikar() if s["tur"] in ("kart", "pilot")}
    yazilan, bloklar = set(), []

    def ust(baslik, nerede):
        return [f"##### {baslik} #####", "# NEREDE: " + Y9_NEREDE[nerede]]

    kart = {"failure": "pencere kapandı, kimse çatıda değil", "cut": "gün sonu, telsiz kesiliyor",
            "nodes": "ordu aynı kanaldan yeniden arıyor", "broadcast": "ilk yayın, bitiş görevi başlar",
            "reply": "oyuncu telsize cevap verince", "missed": "helikopter kaçırılınca"}
    govde = []
    for (tur, yer), s in satirlar.items():
        if tur == "kart":
            konu = kart.get(yer[1] if yer[0] == "lines" else yer[0], "")
            x = _y7_satir(s, yazilan, bilinenler, f"TELSİZ KARTI ({konu})")
            if x:
                govde.append(x)
    if any(x[0] != "·" for x in govde):
        bloklar.append((ust("BİTİŞ · TELSİZ KARTI", "kart"), govde))

    def pilot(yer, etiket, onceki=()):
        x = _y7_satir(satirlar[("pilot", yer)], yazilan, bilinenler, etiket)
        return list(onceki) + ([x] if x else [])

    govde = pilot(("lines.pilot", "board"), "PİLOT (helikopter indi, oyuncuyu çağırır)")
    govde += pilot(("lines.pilot", "ready"), "PİLOT (oyuncu bindi, kalkmadan sorar; cevap şeridinde de görünür)")
    govde += pilot(("lines.pilot", "waiting"), "PİLOT (oyuncu 'bekle' deyince)")
    govde += pilot(("lines.pilot", "go"), "PİLOT (kalkış)")
    govde += pilot(("talk", "intro"), "PİLOT (havalanınca, aşağıdaki yangına bakarak)")
    for b in _liste(E.talk.beats):
        govde.append(("·", "PİLOT (soru)", str(b.ask)))
        for o in _liste(b.options):
            govde += pilot(("talk.beats", str(b.id), str(o.id)), "PİLOT (cevaba karşılık)", [("·", "OYUNCU", str(o.label))])
        govde += pilot(("talk.beats", str(b.id), "silent"), "PİLOT (oyuncu cevap vermezse)")
    govde += pilot(("talk", "outro"), "PİLOT (konuşma biter, varışa yakın)")
    if any(x[0] != "·" for x in govde):
        bloklar.append((ust("BİTİŞ · HELİKOPTER PİLOTU", "pilot"), govde))
    return bloklar


def ozet(satirlar, bilinenler):
    sayac = {}
    for s in satirlar:
        d = sayac.setdefault(s["tur"], {"satir": 0, "anahtarli": 0, "bilinen": 0, "yeni_tekil": set()})
        d["satir"] += 1
        if s["anahtar"]:
            d["anahtarli"] += 1
            if s["anahtar"] in bilinenler:
                d["bilinen"] += 1
            else:
                d["yeni_tekil"].add(s["anahtar"])
    return {t: {**v, "yeni_tekil": len(v["yeni_tekil"])} for t, v in sayac.items()}


if __name__ == "__main__":
    s = cikar()
    b = bilinen()
    for t, v in ozet(s, b).items():
        print(t, v)
    if "--json" in sys.argv:
        print(json.dumps(s, ensure_ascii=False, indent=1))
