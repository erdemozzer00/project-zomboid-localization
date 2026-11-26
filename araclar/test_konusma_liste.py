"""Tablo içi listelerdeki NPC sözleri (rapor/kacan_listeler_1.5.0.md, araclar/liste_cikar.py, Y7).

Çalıştırma: python -B -X utf8 araclar/test_konusma_liste.py
Gereksinim: lupa. Çeviriler sahtedir ("TR<...>"). Modun gerçek dosyaları yüklenir (ALifeText, AudioPolicy, Speech, UI2Answer,
EndingData/Rules/CallData/Call) ve konuşma eki (ALifeTR_Konusma.lua, workshop_kur.ek_metni) üstüne kurulur. Denetlenen:
  - durum ve esir sözü: liste_cikar'ın anahtarı, ham metin Speech.render -> (ekli) AudioPolicy.caption yolundan Türkçe çıkar.
  - telsiz çağrısı: düğüm sözleri Call.fill + ", " ile birleşir (Run.offerNode), (ekli) UI2Answer.clean soru metnini Türkçe döndürür.
  - Y7 haritası (varsa): her anahtar Text.lineKey(en), yalnız çevrilebilir türlerden (durum/esir/çağrı sorusu), yer tutucusuz,
    ve liste_cikar'ın şimdiki çıktısında var.
  - telsiz kartı ve pilot (ek kurKart/kurPilot; gerçek RadioClient/EndingClient, ekten sonra yüklenip OnGameStart'ta bağlanır):
    Türkçe çizilir, sunucudan gelen tablo değişmez, seçenek etiketi arayüz anahtarıyla bulunur, çevirisiz/başka dilde/hata
    olursa İngilizce.
  - Y9 haritası (varsa): yalnız kart ve pilot türleri.
  - yolu olmayan türler (sunucudaki telsiz yayını) anahtarsız.
Oyun içi çizimi doğrulamaz.
"""
import json
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import liste_cikar  # noqa: E402
from lua_cikar import MOD  # noqa: E402
from test_konusma_kacan import Oyun  # noqa: E402

SATIRLAR = liste_cikar.cikar()
BITIS = ("shared/ProjectALife/Ending/ALifeEndingData.lua", "shared/ProjectALife/Ending/ALifeEndingRules.lua",
         "shared/ProjectALife/Ending/ALifeEndingCallData.lua", "shared/ProjectALife/Ending/ALifeEndingCall.lua")


def ilk(tur, kosul=lambda s: True):
    for s in SATIRLAR:
        if s["tur"] == tur and s["anahtar"] and kosul(s):
            return s
    raise AssertionError(f"{tur} yok")


class Yol(unittest.TestCase):
    def soz(self, s):
        o = Oyun()
        o.cevir(s["anahtar"], "TR<soz>")
        PA = o.g.ProjectALife
        gosterilen = PA.AudioPolicy.caption(PA.Speech.render(s["en"], o.lua.table(), None, None))
        self.assertEqual(gosterilen, "TR<soz>", s["en"])

    def test_durum_sozu(self):
        self.soz(ilk("durum"))
        self.soz(ilk("durum", lambda s: s["yer"][2] == "enter"))

    def test_esir_sozu(self):
        self.soz(ilk("esir", lambda s: s["yer"][1] == "mil"))

    def test_cevirisiz_soz_ingilizce(self):
        s = ilk("esir")
        o = Oyun()
        PA = o.g.ProjectALife
        self.assertEqual(PA.AudioPolicy.caption(PA.Speech.render(s["en"], o.lua.table(), None, None)), s["goster"])

    def test_cagri_birlesik_soru(self):
        s = ilk("cagri_soru", lambda s: s["yer"][0] == "open" and s["yer"][1] == "lines")
        o = Oyun()
        for ad in BITIS:
            o.lua.execute((MOD / ad).read_text(encoding="utf-8-sig"))
        PA = o.g.ProjectALife
        vars_ = PA.EndingCall.vars("Kim")
        ham = PA.EndingCallData.nodes.open.lines
        metin = ", ".join(PA.EndingCall.fill(ham[i], vars_) for i in range(1, len(ham) + 1))
        self.assertEqual(metin, s["goster"])
        o.cevir(s["anahtar"], "TR<cagri>")
        self.assertEqual(o.soru(metin).text, "TR<cagri>")
        tek = PA.EndingCall.fill(ham[1], vars_)  # tek düğüm sözü (kart/yayın) bu anahtarla bulunmaz
        self.assertEqual(o.soru(tek).text, tek)


ISTEMCI = ("shared/ProjectALife/Ending/ALifeEndingData.lua", "shared/ProjectALife/Ending/ALifeEndingRules.lua",
           "client/ProjectALife/Radio/ALifeRadioClient.lua", "client/ProjectALife/Ending/ALifeEndingClient.lua")


class Bitis(unittest.TestCase):
    """Ek kurKart/kurPilot: modun gerçek RadioClient ve EndingClient dosyaları, ekten SONRA yüklenir (OnGameStart'ta bağlanır)."""

    def oyun(self, dil="TR"):
        o = Oyun(dil=dil)
        o.lua.execute("""
            ProjectALife.AdminConsole = { onReply = function() end, log = function() end }
            ProjectALife.Experiments = { enabled = function() return false end }
            ProjectALife.Radio3 = { on = function() return false end }
            ProjectALife.RadioFreq = { get = function() return 0 end }
            ITILAN = {}
            ProjectALife.UI2Notify = { ready = function() return true end, push = function(s) ITILAN[#ITILAN + 1] = s; return true end }
            ProjectALife.DeathGuard = { wrap = function(f) return f end }
            getSoundManager = function() return { playUISound = function() end } end
        """)
        for ad in ISTEMCI:
            o.lua.execute((MOD / ad).read_text(encoding="utf-8-sig"))
        o.oyun_basla()
        return o

    def kart(self, o, metin, kind="call"):
        args = o.lua.table_from({"id": "ending_broadcast", "kind": kind, "title": "US Military", "name": "US Military",
                                 "text": metin, "aired": True})
        o.g.ProjectALife.RadioClient.onServerCommand("ProjectALife", "radioCard", args)
        itilan = o.g.ITILAN
        return itilan[len(itilan)], args

    def test_kart_turkce_ve_veri_degismez(self):
        s = ilk("kart")
        o = self.oyun()
        o.cevir(s["anahtar"], "TR<kart>")
        bildirim, args = self.kart(o, s["goster"])
        self.assertEqual(bildirim.text, "US Military: TR<kart>")
        self.assertEqual(args.text, s["goster"])  # sunucudan gelen tablo değişmez

    def test_kart_secenek_etiketi_arayuz_anahtari(self):
        """Yaprakta kartın ilk satırı oyuncunun seçtiği etiket (Y6, IGUI_ALifeUI_)."""
        o = self.oyun()
        T = o.g.ProjectALife.Text
        o.cevir(T.key("IGUI_ALifeUI_", "Who is asking"), "TR<etiket>")
        self.assertEqual(self.kart(o, "Who is asking")[0].text, "US Military: TR<etiket>")

    def test_kart_cevirisiz_ve_baska_dil(self):
        s = ilk("kart")
        self.assertEqual(self.kart(self.oyun(), s["goster"])[0].text, "US Military: " + s["goster"])
        o = self.oyun(dil="EN")
        o.cevir(s["anahtar"], "TR<kart>")
        self.assertEqual(self.kart(o, s["goster"])[0].text, "US Military: " + s["goster"])

    def test_pilot_sozu(self):
        s = ilk("pilot", lambda s: s["yer"][0] == "talk.beats")
        o = self.oyun()
        o.cevir(s["anahtar"], "TR<pilot>")
        args = o.lua.table_from({"who": "pilot", "name": "Pilot", "text": s["goster"]})
        o.g.ProjectALife.EndingClient.say(args)
        self.assertEqual(o.g.ITILAN[len(o.g.ITILAN)].text, "TR<pilot>")
        self.assertEqual(args.text, s["goster"])

    def test_pilot_bekleme_dolu_metin(self):
        s = ilk("pilot", lambda s: s["yer"][1] == "waiting")
        self.assertNotIn("{", s["goster"])
        o = self.oyun()
        E = o.g.ProjectALife.EndingData
        metin = o.g.ProjectALife.EndingRules.fill(E.lines.pilot.waiting, o.lua.table_from({"minutes": E.numbers.waitMoreMinutes}))
        self.assertEqual(metin, s["goster"])

    def test_hata_olursa_ingilizce(self):
        s = ilk("pilot")
        o = self.oyun()
        o.lua.execute("ProjectALife.Text.lineKey = function() error('bozuk') end")  # yalnız ekin kullandığı
        args = o.lua.table_from({"name": "Pilot", "text": s["goster"]})
        o.g.ProjectALife.EndingClient.say(args)
        self.assertEqual(o.g.ITILAN[len(o.g.ITILAN)].text, s["goster"])
        self.assertTrue(o.g.ALifeTurkce_Konusma.kapali)


class Harita(unittest.TestCase):
    def test_yolsuz_turler_anahtarsiz(self):
        for s in SATIRLAR:
            if s["tur"].endswith("_yolsuz"):
                self.assertIsNone(s["anahtar"], s)

    def test_yer_tutuculu_anahtarsiz(self):
        for s in SATIRLAR:
            if s["goster"] and "{" in s["goster"]:
                self.assertIsNone(s["anahtar"], s)

    def test_y7_haritasi(self):
        self.harita("Y7", ("durum", "esir", "cagri_soru"))

    def test_y9_haritasi(self):
        self.harita("Y9", ("kart", "pilot"))

    def harita(self, ad, turler):
        yol = KOK / "paketler/haritalar" / f"{ad}_harita.json"
        if not yol.exists():
            self.skipTest(f"{ad} haritası yok")
        harita = json.loads(yol.read_text(encoding="utf-8"))
        self.assertEqual(harita["_dosya"], "RadioData_lua")
        o = Oyun()
        T = o.g.ProjectALife.Text
        gecerli = {s["anahtar"]: s for s in SATIRLAR if s["anahtar"] and s["tur"] in turler}
        anahtarlar = [v[0] for v in harita["satirlar"].values()]
        self.assertEqual(len(anahtarlar), len(set(anahtarlar)))
        for no, (k, en, yer) in harita["satirlar"].items():
            self.assertEqual(T.lineKey(en), k, en)
            self.assertIn(k, gecerli, en)
            self.assertEqual(gecerli[k]["goster"], en)
            self.assertNotIn("{", en)


if __name__ == "__main__":
    unittest.main(verbosity=2)
