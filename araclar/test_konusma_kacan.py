"""Kaçan metinler (1.5.0, rapor/kacan_ek_1.5.0.md): çıkarıcı anahtarları, Text.ui yolu ve konuşma ekinin iki yeni sarması.

Çalıştırma: python -B -X utf8 araclar/test_konusma_kacan.py
Gereksinim: lupa. Çeviriler sahtedir ("TR<...>"). Modun gerçek dosyaları yüklenir: ALifeText, AudioPolicy, Speech, UI2Talk
(statusText, Talk2.text), UI2Answer (clean); menü/tema/tuş modülleri sahte. Denetlenen:
  - kaynak/IG_UI_kacan.json'daki her anahtar Lua'nın Text.key("IGUI_ALifeUI_", en) değeriyle aynı; Talk2.text onu bulur.
  - Veri dosyaları Lua'da yüklenip satır/ipucu/aşama alanları gezilir: yer tutucusuz her metnin bir çeviri yolu var
    (IG_UI_kacan, mod EN IG_UI, IG_UI_lua ya da bekleyen harita): çıkarıcı bir satırı kaçırmamış.
  - statusText: ipucu Türkçe döner, çevirisi yoksa İngilizce, başka durum yazısı ve win.hoverTip değişmez,
    hata olursa orijinal sonuç döner ve ek kapanır, dil Türkçe değilse dokunmaz.
  - UI2Answer.clean: soru metni önce RD_ALifeLine_, sonra IGUI_ALifeUI_ ile çevrilir; seçenekler ve kimlikler aynen kalır;
    hata olursa orijinal sonuç; modüller ekten sonra yüklenirse OnGameStart'ta bağlanır.
  - Y6 haritası (varsa) yalnız IG_UI_kacan'daki diyalog anahtarlarını taşır.
Oyun içi çizimi doğrulamaz.
"""
import json
import sys
import unittest
from pathlib import Path

from lupa.lua51 import LuaRuntime

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import kacan_cikar  # noqa: E402
import workshop_kur  # noqa: E402
from lua_cikar import MOD  # noqa: E402

EK = workshop_kur.ek_metni("ALifeTR_Konusma.lua")
KACAN = json.loads((KOK / "kaynak" / "IG_UI_kacan.json").read_text(encoding="utf-8"))
BAGLAM = json.loads((KOK / "kaynak" / "IG_UI_kacan_baglam.json").read_text(encoding="utf-8"))
TEMEL = ("shared/ProjectALife/Core/ALifeText.lua", "shared/ProjectALife/Audio/ALifeAudioPolicy.lua",
         "shared/ProjectALife/Talk/ALifeSpeech.lua")
TALK = "client/ProjectALife/UI2/ALifeUI2Talk.lua"
ANSWER = "client/ProjectALife/UI2/ALifeUI2Answer.lua"


def ilk(tur, alan=None):
    for k, v in BAGLAM.items():
        if v[2] == tur and (alan is None or v[1] == alan):
            return k, KACAN[k]
    raise AssertionError(f"{tur}/{alan} yok")


class Oyun:
    def __init__(self, dil="TR", moduller_once=True):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        g = self.g = self.lua.globals()
        g.DIL = dil
        self.lua.execute("""
            require = function() return nil end
            ProjectALife = {}
            CEVIRILER, LOG, BASLA, BOOT = {}, {}, {}, {}
            UIFont = { Small = "Small", Medium = "Medium" }
            Translator = { getLanguage = function() return { name = function() return DIL end } end }
            getTextOrNull = function(key) return CEVIRILER[key] end
            print = function(s) LOG[#LOG + 1] = tostring(s) end
            Events = { OnGameBoot = { Add = function(f) BOOT[#BOOT + 1] = f end },
                       OnGameStart = { Add = function(f) BASLA[#BASLA + 1] = f end },
                       OnServerCommand = { Add = function() end }, OnTick = { Add = function() end },
                       OnKeyPressed = { Add = function() end } }
        """)
        for ad in TEMEL:
            self.lua.execute((MOD / ad).read_text(encoding="utf-8-sig"))
        if moduller_once:
            self.moduller()
        self.lua.execute(EK)

    def moduller(self):
        """UI2Talk ve UI2Answer, sahte menü/tema/tuş modülleriyle (gerçek dosyalar)."""
        self.lua.execute("""
            local Pencere = {}
            function Pencere:derive(ad) local t = {}; t.__index = t; return setmetatable(t, { __index = self }) end
            ProjectALife.TalkMenu = { Window = Pencere, open = function() end }
            ProjectALife.UI2Theme = { skin = function() return { dim = "dim", faint = "faint", amber = "amber", accent = "accent" } end }
            ProjectALife.UI2TalkTone = { kinds = { important = true, risky = true } }
            ProjectALife.UI2Keys = { register = function() return true end }
            ProjectALife.UI2Hud = { register = function() end }
        """)
        self.lua.execute((MOD / TALK).read_text(encoding="utf-8-sig"))
        self.lua.execute((MOD / ANSWER).read_text(encoding="utf-8-sig"))

    def oyun_basla(self):
        self.lua.execute("for _, f in ipairs(BASLA) do f() end")

    def cevir(self, anahtar, tr):
        self.g.CEVIRILER[anahtar] = tr

    def durum(self, **win):
        w = self.lua.table_from(win)
        return self.g.ProjectALife.UI2Talk.statusText(w, 0), w

    def soru(self, metin):
        args = self.lua.table_from({"id": "end_talk", "name": "Pilot", "text": metin, "kind": "talk",
                                    "options": self.lua.table_from([self.lua.table_from({"id": "a", "label": "Every second"}),
                                                                    self.lua.table_from({"id": "b", "label": "No"})])})
        return self.g.ProjectALife.UI2Answer.clean(args)


class AnahtarTesti(unittest.TestCase):
    def test_anahtarlar_lua_ile_ayni(self):
        o = Oyun()
        T = o.g.ProjectALife.Text
        self.assertGreater(len(KACAN), 200)
        for k, en in KACAN.items():
            self.assertTrue(k.startswith("IGUI_ALifeUI_"))
            self.assertEqual(T.key("IGUI_ALifeUI_", en), k, en)

    def test_text_ui_yolu_bulur(self):
        """Ek gerekmeyen gruplar: konuşma satırı/alt notu Talk2.text, ayar/aşama M.text = Text.ui."""
        o = Oyun()
        for tur, alan in (("durum_satiri", "text"), ("durum_satiri", "impact"), ("esir_satiri", "risk"),
                          ("bitis_cagri", "label"), ("ayar", "tip"), ("gorev_asamasi", "detail")):
            k, en = ilk(tur, alan)
            o.cevir(k, f"TR<{tur}>")
            self.assertEqual(o.g.ProjectALife.UI2Talk.text(en), f"TR<{tur}>")
            self.assertEqual(o.g.ProjectALife.Text.ui(en), f"TR<{tur}>")

    def test_veri_dosyalarinda_kacan_yok(self):
        """Mod verisi Lua'da yüklenir; çıkarıcının kapsadığı alanlarda yer tutucusuz her metnin bir anahtarı var."""
        bil = kacan_cikar.bilinen() | set(KACAN)
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua.execute("require = function() end; ProjectALife = {}")
        for ad in ("shared/ProjectALife/Situations/ALifeSituationsData.lua", "shared/ProjectALife/Captives/ALifeCaptivesData.lua",
                   "shared/ProjectALife/Missions/ALifeMissionDefs.lua", "shared/ProjectALife/Ending/ALifeEndingCallData.lua",
                   "shared/ProjectALife/Ending/ALifeEndingData.lua", "client/ProjectALife/UI2/ALifeUI2Prefs.lua"):
            lua.execute((MOD / ad).read_text(encoding="utf-8-sig"))
        P = lua.globals().ProjectALife

        def liste(t):
            return [] if t is None else [t[i] for i in range(1, len(t) + 1)]

        metinler = []
        for sit in liste(P.SituationsData.situations):
            for r in liste(sit.rows):
                metinler += [r.text, r.impact, r.risk]
        for r in liste(P.CaptivesData.rows):
            metinler += [r.text, r.impact, r.risk]
        for r in liste(P.MissionDefs.rows):
            metinler += [r.text, r.tip] + [c.label for c in liste(r.chips)]
        for m in P.MissionDefs.missions.values():
            for s in liste(m.stages):
                metinler += [s.text, s.detail]
        for dugum in P.EndingCallData.nodes.values() if P.EndingCallData.nodes else []:
            metinler += [o.label for o in liste(dugum.opts)]
        for b in liste(P.EndingData.talk.beats) if P.EndingData.talk else []:
            metinler += [b.ask] + [o.label for o in liste(b.options)]
        for r in liste(P.UI2Prefs.rows):
            metinler += [r.label, r.tip] + list(r.names.values())
        metinler = [m for m in metinler if isinstance(m, str) and any(c.isalpha() for c in m) and "{" not in m]
        self.assertGreater(len(metinler), 250)
        eksik = [m for m in metinler if kacan_cikar.anahtar(m) not in bil]
        self.assertEqual(eksik, [])

    def test_y6_haritasi_kacan_diyalog(self):
        harita = KOK / "rapor" / "Y6_harita.json"
        if not harita.exists():
            self.skipTest("Y6 haritası yok")
        h = json.loads(harita.read_text(encoding="utf-8"))
        self.assertEqual(h["_dosya"], "IG_UI_lua")
        diyalog = {k for k, v in BAGLAM.items() if v[3] == "diyalog"}
        self.assertEqual({v[0] for v in h["satirlar"].values()}, diyalog)
        for k, en, _ in h["satirlar"].values():
            self.assertEqual(KACAN[k], en)


class IpucuTesti(unittest.TestCase):
    def test_ipucu_cevrilir_veri_degismez(self):
        o = Oyun()
        k, en = ilk("gorev_satiri", "tip")
        o.cevir(k, "TR<ipucu>")
        sonuc, win = o.durum(hoverTip=en)
        self.assertEqual(sonuc.text, "TR<ipucu>")
        self.assertEqual(sonuc.color, "dim")
        self.assertEqual(win.hoverTip, en)

    def test_cevirisi_yoksa_ingilizce(self):
        o = Oyun()
        sonuc, _ = o.durum(hoverTip="Zzz no translation")
        self.assertEqual(sonuc.text, "Zzz no translation")

    def test_baska_durum_yazisina_dokunmaz(self):
        o = Oyun()
        o.cevir(o.g.ProjectALife.Text.key("IGUI_ALifeUI_", "WAITING"), "TR<yanlis>")
        sonuc, _ = o.durum(waitingAt=1, s=o.lua.table_from({"waiting": "waiting"}))
        self.assertEqual(sonuc.text, "WAITING")
        sonuc, _ = o.durum()
        self.assertIsNone(sonuc)

    def test_hata_olursa_orijinal(self):
        o = Oyun()
        k, en = ilk("gorev_satiri", "tip")
        o.cevir(k, "TR<ipucu>")
        o.lua.execute("ProjectALife.Text.lookup = function() error('bozuk') end")
        sonuc, _ = o.durum(hoverTip=en)
        self.assertEqual(sonuc.text, en)
        self.assertTrue(o.g.ALifeTurkce_Konusma.kapali)
        self.assertTrue(any("kapatildi" in str(s) for s in o.g.LOG.values()))

    def test_dil_turkce_degilse_dokunmaz(self):
        o = Oyun(dil="EN")
        k, en = ilk("gorev_satiri", "tip")
        o.cevir(k, "TR<ipucu>")
        sonuc, _ = o.durum(hoverTip=en)
        self.assertEqual(sonuc.text, en)


class SoruTesti(unittest.TestCase):
    def test_soru_arayuz_anahtariyla(self):
        o = Oyun()
        k, en = ilk("bitis_soru", "ask")
        o.cevir(k, "TR<soru>")
        soru = o.soru(en)
        self.assertEqual(soru.text, "TR<soru>")
        self.assertEqual([soru.options[i].id for i in (1, 2)], ["a", "b"])
        self.assertEqual(soru.options[1].label, "Every second")  # seçenek Text.ui'ye çizimde gider, veride değişmez

    def test_konusma_anahtari_once(self):
        o = Oyun()
        T = o.g.ProjectALife.Text
        o.cevir(T.lineKey("Hold still"), "TR<npc>")
        o.cevir(T.key("IGUI_ALifeUI_", "Hold still"), "TR<arayuz>")
        self.assertEqual(o.soru("Hold still").text, "TR<npc>")

    def test_cevirisi_yoksa_ingilizce(self):
        o = Oyun()
        self.assertEqual(o.soru("Zzz no translation").text, "Zzz no translation")

    def test_hata_olursa_orijinal(self):
        o = Oyun()
        k, en = ilk("bitis_soru", "ask")
        o.cevir(k, "TR<soru>")
        o.lua.execute("ProjectALife.Text.lookup = function() error('bozuk') end")
        soru = o.soru(en)
        self.assertEqual(soru.text, en)
        self.assertEqual(soru.id, "end_talk")
        self.assertTrue(o.g.ALifeTurkce_Konusma.kapali)

    def test_gecersiz_soru_aynen(self):
        o = Oyun()
        self.assertIsNone(o.g.ProjectALife.UI2Answer.clean(o.lua.table_from({"text": "x"})))  # id yok: mod nil döner


class YuklemeTesti(unittest.TestCase):
    def test_moduller_sonradan_yuklenir(self):
        o = Oyun(moduller_once=False)
        self.assertFalse(o.g.ALifeTurkce_Konusma.kapali)
        o.moduller()
        o.oyun_basla()
        self.assertTrue(o.g.ProjectALife.UI2Talk.ALifeTurkceIpucu)
        self.assertTrue(o.g.ProjectALife.UI2Answer.ALifeTurkceKurulu)
        k, en = ilk("gorev_satiri", "tip")
        o.cevir(k, "TR<ipucu>")
        self.assertEqual(o.durum(hoverTip=en)[0].text, "TR<ipucu>")

    def test_iki_kez_sarmaz(self):
        o = Oyun()
        o.oyun_basla()
        o.oyun_basla()
        k, en = ilk("bitis_soru", "ask")
        o.cevir(k, "TR<soru>")
        self.assertEqual(o.soru(en).text, "TR<soru>")


if __name__ == "__main__":
    unittest.main(verbosity=1)
