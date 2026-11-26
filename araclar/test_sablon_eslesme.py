"""Konuşma ekinin K46 eklerini oyunun kendi Lua koduyla denetler: rastgele yer tutuculu şablon eşleme ve DoLines.

Çalıştırma: python -B -X utf8 araclar/test_sablon_eslesme.py
Gereksinim: lupa (Lua 5.1). Şablonlar gerçek Speech.render ile doldurulur, caption'dan geçirilir; Türkçe şablonun
değerlerle doldurulduğu, değerlerin çevrildiği ve şablon olmayan satırların yanlışlıkla eşleşmediği doğrulanır.
Oyun içi çizimi doğrulamaz.
"""
import json
import re
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import test_konusma_font as t  # noqa: E402
import sablon_varyant as sv  # noqa: E402

EN = t.EN
ONAYLI = json.loads((KOK / "onayli/RadioData_lua.json").read_text(encoding="utf-8"))
SABLON = sv.rastgele_sablonlar(EN, ONAYLI)
# Modun kendi hatası: Talk5Home "{At}" yazar ama Speech.render yalnız küçük harfli {ad}'ı doldurur; oyunda "{At}" olduğu gibi
# kalır, değer yakalanamaz (gecerli reddeder). Bu 4 satır oyunda İngilizce kalır; yapımcıya bildirilecek.
AT_BOZUK = {k for k in EN if "{At}" in EN[k]}
SABLON_ANAHTAR = {e["k"] for e in SABLON} - AT_BOZUK
DEGERLER = {"town": "Rosewood", "name": "Earl", "street": "Main Street", "den": "a house on the north side of Rosewood",
            "weapon": "that gun", "day": "12", "time": "3 PM", "date": "July 4th", "weekday": "Monday",
            "destination": "somewhere quieter", "faction": "some crew", "group": "some crew", "where": "not far from here",
            "kind": "place", "count": "a few", "unit": "4-Adam-22", "callsign": "4-Adam-22", "from": "down the road",
            "to": "down the road",
            # E1: Talk/General, Talk5Home ve ağaç değerleri (oyunun ürettiği biçimler)
            "At": "in the northeast side of Rosewood", "at": "in the northeast side of Rosewood",
            "badat": "on the edge of Muldraugh", "goodat": "in the middle of West Point",
            "contactat": "out past Riverside", "placeat": "in the north end of Louisville",
            "bad": "cops", "good": "soldiers", "place": "the warehouse", "contact": "Dell",
            "home": "a house in Rosewood", "outpost": "a camp in Muldraugh", "season": "winter",
            "span": "3 weeks", "nearTown": "Riverside", "playerName": "Sam", "who": "Earl", "n": "7",
            "job": "deputy", "profession": "mechanic", "what": "You, stop, what do you want",
            "event": "cops hit somebody in the middle of Rosewood a while back"}
BEKLENEN = {"Rosewood", "Earl", "Main Street", "Rosewood kuzey yakasındaki bir ev", "o silah", "12",
            "öğleden sonra 3", "4 Temmuz", "Pazartesi", "daha sakin bir yer", "bir tayfa", "buraya yakın bir yer",
            "yer", "birkaç", "4-Adam-22", "yolun ilerisi"}
# E1: yer tutucu başına beklenen Türkçe (küçük harfli ad). Burada olan her yer tutucu için Türkçesi satırda geçmeli.
BEKLENEN_AD = {
    "at": "Rosewood kuzeydoğu yakasında", "badat": "Muldraugh kenarında", "goodat": "West Point merkezinde",
    "contactat": "Riverside dışında, biraz ötede", "placeat": "Louisville kuzey ucunda",
    "bad": "polisler", "good": "askerler", "place": "depo", "home": "Rosewood bölgesinde bir ev",
    "outpost": "Muldraugh bölgesinde bir kamp", "season": "kış", "span": "3 hafta", "neartown": "Riverside",
    "playername": "Sam", "who": "Earl", "contact": "Dell", "n": "7",
    "job": "şerif yardımcısı", "profession": "tamirci", "what": "Dur bakalım. Ne istiyorsun?",
    "event": "Rosewood merkezinde bir süre önce polisler birilerine saldırmış"}


# {weapon} şablonuna da uyan düz satırlar: kendi çevirisi olduğu için oyunda doğrudan anahtar kazanır.
# 1.5.0 Y1 ile gelen {name}/{faction} şablonları bu düz satırların doldurulmuş hâlini de karşılıyor;
# düz satırların kendi çevirisi var ve oyunda doğrudan anahtar önce kazanır (aşağıdaki son assert bunu sınar).
KENDI_CEVIRISI_KAZANIR = {
    "RD_ALifeLine_7210a3c323538383",
    "RD_ALifeLine_37f555cf6e726e80",
    "RD_ALifeLine_019e5be12225fd34",
    "RD_ALifeLine_05ddb73a732f7560",
    "RD_ALifeLine_087df99c23d72807",
    "RD_ALifeLine_1015a20e105bfcf3",
    "RD_ALifeLine_7631e03215f17b71",
    "RD_ALifeLine_7e5896ff5d4e817c",
    "RD_ALifeLine_5e90a5c86d8fbad8",
    "RD_ALifeLine_10146c5872a4633c",
    "RD_ALifeLine_41a18f663d9691f5",
    # E1: kendi çevirisi olan düz satırlar; "It's {weekday}" ve "What do you know about {…}?" şablonları doldurulmuş hâllerini de karşılıyor
    "RD_ALifeLine_37947cab053c0959",
    "RD_ALifeLine_1dfbcbc6748d55ad",
}


class SablonEslesmeTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oyun = t.Oyun()
        cls.lua = cls.oyun.g.ProjectALife

    def render(self, en, cinsiyet, degerler=DEGERLER):
        # Speech.render yalnız küçük harfli {ad}'ı doldurur; {playerName}/{nearTown} gibi büyük harfli adları ağaç motoru
        # ({%a+}) doldurur. Oyundaki sırayı taklit ederek önce onları dolduruyoruz.
        en = re.sub(r"\{([A-Za-z]*[A-Z][A-Za-z]*)\}", lambda m: degerler.get(m.group(1), m.group(0)) if m.group(1) != "At" else m.group(0), en)
        return self.lua.Speech.render(en, self.oyun.lua.table_from(degerler), None, cinsiyet)

    def test_onayli_her_sablon_cevrilir_ve_degerler_yerlesir(self):
        self.assertGreaterEqual(len(SABLON_ANAHTAR), 80)
        for k in sorted(SABLON_ANAHTAR):
            for cinsiyet in ("m", "f"):
                with self.subTest(anahtar=k, cinsiyet=cinsiyet):
                    en = self.render(EN[k], cinsiyet)
                    tr = self.oyun.cevir(en)
                    self.assertNotEqual(tr, en)
                    self.assertNotIn("{", tr)
                    beklenen = sv.gendered(ONAYLI[k], cinsiyet == "f")
                    for ad in sv.YT.findall(beklenen):
                        ozel = BEKLENEN_AD.get(ad.lower())
                        if ozel is not None:
                            self.assertIn(ozel, tr)
                        else:
                            self.assertTrue(any(b in tr for b in BEKLENEN), tr)
                    self.assertTrue(tr.startswith(beklenen.split("{")[0]))

    def test_ornek_den_ve_varsayilan_dolgu(self):
        k = "RD_ALifeLine_682fc1eb2b2f9d77"
        tr = self.oyun.cevir(self.render(EN[k], "m"))
        self.assertIn("Rosewood kuzey yakasındaki bir ev tarafında", tr)
        tr = self.oyun.cevir(self.render(EN[k], "m", {}))  # değişken verilmezse Speech.render'ın kendi dolgusu
        self.assertIn("bir daha dönmeyeceğim bir yer tarafında", tr)

    def test_sigınak_tarifinin_uc_bicimi(self):
        k = "RD_ALifeLine_682fc1eb2b2f9d77"
        for den, parca in (("the motel in the middle of Muldraugh", "Muldraugh merkezindeki motel"),
                           ("a diner out past the county road", "ilçe yolunun ötesindeki bir lokanta"),
                           ("a store on the southwest side of West Point", "West Point güneybatı yakasındaki bir dükkân")):
            with self.subTest(den=den):
                tr = self.oyun.cevir(self.render(EN[k], "m", {"den": den}))
                self.assertIn(parca, tr)

    def test_saat_ve_tarih_bicimleri(self):
        g = self.oyun.lua.eval
        for en, tr in (("midnight", "gece yarısı"), ("noon", "öğle vakti"), ("9 AM", "sabah 9"), ("8 PM", "akşam 8")):
            with self.subTest(en=en):
                self.assertEqual(self.lua.Text.lookup("RD_ALifeTR_Deger_" + self.lua.Text.hash(en.lower())) or g(
                    "nil"), tr if en in ("midnight", "noon") else None)

    def test_sablon_olmayan_satirlar_eslesmez(self):
        """Şablon dışındaki bütün kaynak satırları, çevirisi yokmuş gibi denenir: hiçbiri bir şablona uymamalı."""
        cev = self.oyun.g.CEVIRILER
        yanlis = []
        for k, en in EN.items():
            if "{" in en:
                continue
            metin = sv.capitalize(en)
            anahtar = self.lua.Text.lineKey(metin)
            sakla = cev[anahtar]
            cev[anahtar] = None
            self.lua.Text.flush()
            sonuc = self.oyun.cevir(metin)
            cev[anahtar] = sakla
            if sonuc != metin and k not in KENDI_CEVIRISI_KAZANIR:
                yanlis.append((k, en, sonuc))
        self.lua.Text.flush()
        self.assertEqual(yanlis[:5], [])
        for k in sorted(KENDI_CEVIRISI_KAZANIR):
            with self.subTest(anahtar=k):
                self.assertEqual(self.oyun.cevir(sv.capitalize(EN[k])), ONAYLI[k])

    def test_cevirisi_olmayan_sablon_ingilizce_kalir(self):
        en = "Somebody in {town} still owes me {count} dollars, tell {name} I said hi"
        metin = self.render(en, "m")
        self.assertEqual(self.oyun.cevir(metin), metin)


class DoLinesTesti(unittest.TestCase):
    def kur(self, ceviriler):
        oyun = t.Oyun(ek=False)
        for k, v in ceviriler.items():
            oyun.g.CEVIRILER[k] = v
        oyun.lua.execute("""
            ProjectALife.VisitorDoLines = {
                pick = function(record, ctx) return PICK_METIN, "durum", "ham" end,
                lines = function(record, ctx) return { LISTE_1, LISTE_2 }, "ikinci" end,
            }
        """)
        oyun.lua.execute(t.ek_metni())
        return oyun

    def test_pick_ve_lines_cevrilir_diger_degerler_korunur(self):
        ham = "*{v:He} glances at your hands, then the house, then away*"
        tr = "*Önce ellerine, sonra eve bakıyor, sonra başını çeviriyor*"
        erkek, kadin = sv.v_render(ham, False), sv.v_render(ham, True)
        oyun = self.kur({sv.anahtar(erkek): tr, sv.anahtar(kadin): tr})
        oyun.g.PICK_METIN, oyun.g.LISTE_1, oyun.g.LISTE_2 = kadin, erkek, "Cevirisi olmayan satir"
        metin, durum, ham_donen = oyun.g.ProjectALife.VisitorDoLines.pick(None, None)
        self.assertEqual((metin, durum, ham_donen), (tr, "durum", "ham"))
        liste, ikinci = oyun.g.ProjectALife.VisitorDoLines.lines(None, None)
        self.assertEqual((liste[1], liste[2], ikinci), (tr, "Cevirisi olmayan satir", "ikinci"))

    def test_ingilizce_dilinde_dokunulmaz(self):
        oyun = t.Oyun(dil="EN", ek=False)
        oyun.lua.execute('ProjectALife.VisitorDoLines = { pick = function() return "*He waits*", 1 end }')
        oyun.lua.execute(t.ek_metni())
        self.assertEqual(tuple(oyun.g.ProjectALife.VisitorDoLines.pick()), ("*He waits*", 1))

    def test_dolines_yoksa_ek_calismaya_devam_eder(self):
        oyun = t.Oyun()
        self.assertEqual(oyun.cevir(EN[t.ORNEK_ANAHTAR]), t.TR[t.ORNEK_ANAHTAR])
        self.assertEqual(list(oyun.g.LOG.values()), [])


class BildirimTesti(unittest.TestCase):
    def test_bildirim_cevrilir_yuk_guncellenir_digerleri_korunur(self):
        oyun = t.Oyun(ek=False)
        anahtar = oyun.g.ProjectALife.Text.key("IGUI_ALifeUI_", "You left the group.")
        oyun.g.CEVIRILER[anahtar] = "Gruptan ayrıldın."
        oyun.lua.execute("""
            ProjectALife.SafehouseClient = { notice = function(yuk, oyuncu) GORULEN = yuk.text; return true, oyuncu end }
        """)
        oyun.lua.execute(t.ek_metni())
        yuk = oyun.lua.table_from({"text": "You left the group.", "mark": "x"})
        sonuc = oyun.g.ProjectALife.SafehouseClient.notice(yuk, "oyuncu")
        self.assertEqual((oyun.g.GORULEN, yuk["text"], yuk["mark"]), ("Gruptan ayrıldın.", "Gruptan ayrıldın.", "x"))
        self.assertEqual(tuple(sonuc), (True, "oyuncu"))
        yuk = oyun.lua.table_from({"text": "Ceviri yok"})
        oyun.g.ProjectALife.SafehouseClient.notice(yuk)
        self.assertEqual(oyun.g.GORULEN, "Ceviri yok")


class ZiyaretciPaneliTesti(unittest.TestCase):
    def test_clean_ve_notes_cevrilir_sinir_asilirsa_ingilizce_kalir(self):
        oyun = t.Oyun(ek=False)
        L = oyun.g.ProjectALife
        oyun.g.CEVIRILER[L.Text.lineKey("What's it about?")] = "Ne anlatıyor?"
        oyun.g.CEVIRILER[L.Text.lineKey("Promised Elmer help")] = "Elmer'a yardım sözü verdi"
        oyun.g.CEVIRILER[L.Text.lineKey("Long one")] = "Çok çok uzun bir çeviri"
        oyun.lua.execute("""
            ProjectALife.VisitorPanel = {
                clean = function(text, limit)
                    if type(text) ~= "string" then return nil end
                    if #text > limit then return string.sub(text, 1, limit) end
                    return text
                end,
                notes = function() return { "Promised Elmer help", "Unknown note" } end,
            }
        """)
        oyun.lua.execute(t.ek_metni())
        P = L.VisitorPanel
        self.assertEqual(P.clean("What's it about?", 80), "Ne anlatıyor?")
        self.assertEqual(P.clean("Long one", 10), "Long one")  # Türkçe 10 baytı aşıyor
        self.assertEqual(P.clean("Otis", 80), "Otis")
        self.assertIsNone(P.clean(None, 80))
        notlar = P.notes(None, None)
        self.assertEqual((notlar[1], notlar[2]), ("Elmer'a yardım sözü verdi", "Unknown note"))

    def test_sekme_adi_konusma_satirinin_cevirisini_almaz(self):
        oyun = t.Oyun(ek=False)
        L = oyun.g.ProjectALife
        oyun.g.CEVIRILER[L.Text.lineKey("Talk")] = "Konuş bakalım"
        oyun.lua.execute("""
            ProjectALife.VisitorPanel = {
                clean = function(text, limit) return text end,
                cleanTabs = function(liste) return { ProjectALife.VisitorPanel.clean(liste[1], 24) } end,
            }
        """)
        oyun.lua.execute(t.ek_metni())
        P = L.VisitorPanel
        self.assertEqual(P.cleanTabs(oyun.lua.table_from(["Talk"]))[1], "Talk")  # Menu.groupLabel Text.ui'den geçirir
        self.assertEqual(P.clean("Talk", 80), "Konuş bakalım")


if __name__ == "__main__":
    unittest.main()
