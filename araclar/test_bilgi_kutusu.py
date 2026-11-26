"""Ana menü bilgi kutusu ekini (araclar/lua/ALifeTR_Bilgi.lua) sahte oyun çağrılarıyla denetler (K55).

Çalıştırma: python -B -X utf8 araclar/test_bilgi_kutusu.py
Gereksinim: lupa (Lua 5.1). Oyun içi çizimi ve yerleşimi doğrulamaz; görsel kontrol oyunda yapılır.
"""

import json
import sys
import unittest
from pathlib import Path

from lupa.lua51 import LuaRuntime

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import workshop_kur  # noqa: E402

METIN = json.loads((KOK / "onayli/Bilgi_UI.json").read_text(encoding="utf-8"))

HAZIRLIK = """
require = function() end
UIFont = { Small = "Small" }
LOG, DOSYA_ICERIK = {}, nil
print = function(s) LOG[#LOG + 1] = tostring(s) end
Clipboard = { setClipboard = function(url) PANO = url end }
Translator = { getLanguage = function() return { name = function() return DIL end } end }
getText = function(k) return METIN[k] or k end
getTextManager = function() return {
    getFontHeight = function() return 14 end,
    MeasureStringX = function(_, _, s) return #s * 7 end } end
getFileReader = function(ad, olustur)
    if DOSYA_ICERIK == nil then return nil end
    return { readLine = function() return DOSYA_ICERIK end, close = function() end }
end
getFileWriter = function(ad, olustur, ekle)
    return { write = function(_, s) DOSYA_ICERIK = s end, close = function() end }
end
Events = {
    OnMainMenuEnter = { Add = function(f) MENU = f end },
    OnTick = { Add = function(f) TICK = f end, Remove = function(f) if TICK == f then TICK = nil end end },
}
local function eleman(x, y, w, h)
    local o = { x = x, y = y, width = w, height = h, gorunur = true, cocuklar = {} }
    function o:getX() return self.x end
    function o:getY() return self.y end
    function o:getWidth() return self.width end
    function o:getHeight() return self.height end
    function o:setHeight(v) self.height = v end
    function o:isVisible() return self.gorunur end
    function o:getIsVisible() return self.gorunur end
    function o:setVisible(v) self.gorunur = v end
    function o:initialise() end
    function o:instantiate() end
    function o:addChild(c) c.parent = self; self.cocuklar[#self.cocuklar + 1] = c end
    function o:removeChild(c)
        for i, v in ipairs(self.cocuklar) do if v == c then table.remove(self.cocuklar, i); c.parent = nil end end
    end
    function o:paginate() if self.autosetheight then self.height = 60 end end
    function o:addScrollBars() self.kaydirma = true end
    return o
end
ISPanel = {}
function ISPanel:derive() local t = {}; t.__index = t; setmetatable(t, { __index = ISPanel }); return t end
function ISPanel:new(x, y, w, h)
    local o = eleman(x, y, w, h); setmetatable(o, self); self.__index = self; return o
end
ISRichTextPanel = ISPanel
ISButton = {}
function ISButton:new(x, y, w, h, baslik, hedef, tikla)
    local o = eleman(x, y, w, h)
    o.baslik, o.hedef, o.tikla = baslik, hedef, tikla
    function o:setTitle(title) self.baslik = title end
    return o
end
CIZIM = 0
function ISPanel:drawRect() CIZIM = CIZIM + 1 end
function ISPanel:drawRectBorder() CIZIM = CIZIM + 1 end
function ISPanel:drawText() CIZIM = CIZIM + 1 end
function menuKur(inGame)
    local m = eleman(0, 0, 1920, 1080)
    m.inGame = inGame
    m.bottomPanel = eleman(0, 800, 400, 200)
    m.reportBug = eleman(1700, 1030, 180, 24)
    m.modListDetail = eleman(1700, 996, 180, 24)
    m.termsOfService = eleman(1700, 962, 180, 24)
    MainScreen = { instance = m }
    return m
end
"""


class Oyun:
    def __init__(self, dil="TR", metin=None, gorulen=None, in_game=False):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.g = self.lua.globals()
        self.g.DIL = dil
        self.g.METIN = self.lua.table_from(METIN if metin is None else metin)
        self.lua.execute(HAZIRLIK)
        if gorulen is not None:
            self.g.DOSYA_ICERIK = gorulen
        self.menu = self.lua.eval("menuKur(%s)" % ("true" if in_game else "false"))
        self.lua.execute(workshop_kur.ek_metni("ALifeTR_Bilgi.lua"))

    def gir(self):
        self.lua.execute("MENU()")

    def kutular(self):
        return [c for c in self.menu.cocuklar.values() if c.baslik is not None] if self.menu.cocuklar else []


class BilgiKutusuTesti(unittest.TestCase):
    def test_ek_ascii_ve_kurulur(self):
        metin = workshop_kur.ek_metni("ALifeTR_Bilgi.lua")
        metin.encode("ascii")

    def test_turkce_menude_bir_kutu_eklenir_ve_tekrarlanmaz(self):
        o = Oyun()
        o.gir()
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 1)
        kutu = o.menu.cocuklar[1]
        self.assertEqual(kutu.baslik, METIN["UI_ALifeTR_Bilgi_Baslik"])
        # sağ alttaki düğmelerin üstünde, ekran içinde, sağ kenarları hizalı
        self.assertLess(kutu.y + kutu.height, 962)
        self.assertGreaterEqual(kutu.y, 0)
        self.assertEqual(kutu.x + kutu.width, 1880)

    def test_dil_turkce_degilse_hicbir_sey_yapmaz(self):
        o = Oyun(dil="EN")
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 0)

    def test_oyun_icindeki_menude_gosterilmez(self):
        o = Oyun(in_game=True)
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 0)

    def test_metin_yoksa_gosterilmez(self):
        o = Oyun(metin={})
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 0)

    def test_onceki_okundu_kaydi_olsa_da_her_menu_girisinde_gosterilir(self):
        o = Oyun(gorulen="2")
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 1)
        kutu = o.menu.cocuklar[1]
        dugme = kutu.cocuklar[2]
        dugme.tikla(dugme.hedef, dugme)
        self.assertEqual(len(o.menu.cocuklar), 0)
        self.assertEqual(o.g.DOSYA_ICERIK, "2")  # eski okundu kaydına dokunulmaz

        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 1)

    def test_kapat_kalici_kayit_tutmadan_kutuyu_kaldirir(self):
        o = Oyun()
        o.gir()
        kutu = o.menu.cocuklar[1]
        dugme = kutu.cocuklar[2]
        dugme.tikla(dugme.hedef, dugme)
        self.assertEqual(len(o.menu.cocuklar), 0)
        self.assertIsNone(o.g.DOSYA_ICERIK)

    def test_alt_panel_gizlenince_kutu_gizlenir(self):
        o = Oyun()
        o.gir()
        kutu = o.menu.cocuklar[1]
        o.menu.bottomPanel.gorunur = False
        o.lua.execute("TICK()")
        self.assertFalse(kutu.gorunur)
        o.menu.bottomPanel.gorunur = True
        o.lua.execute("TICK()")
        self.assertTrue(kutu.gorunur)

    def test_site_dugmesi_yalnizca_tiklaninca_adresi_kopyalar(self):
        o = Oyun()
        o.gir()
        kutu = o.menu.cocuklar[1]
        yazi, kapat, site = [kutu.cocuklar[i] for i in (1, 2, 3)]
        self.assertTrue(yazi.text.endswith("İyi oyunlar.\n\n" + METIN["UI_ALifeTR_Bilgi_SiteDavet"]))
        self.assertEqual(site.baslik, "Adresi kopyala")
        self.assertLessEqual(yazi.y + yazi.height, site.y)
        self.assertLessEqual(site.y + site.height, kapat.y)
        self.assertIsNone(o.g.PANO)
        site.tikla(site.hedef, site)
        self.assertEqual(o.g.PANO, "https://ozzer-yerellestirme.netlify.app/")
        self.assertEqual(site.baslik, "Kopyalandı")
        o.lua.execute("Clipboard.setClipboard = function() error('pano kullanilamiyor') end")
        site.tikla(site.hedef, site)
        self.assertEqual(site.baslik, "Adresi kopyala")
        self.assertEqual(len(o.menu.cocuklar), 1)

    def test_kucuk_pencerede_metin_kayar_ve_dugmeler_sigar(self):
        o = Oyun()
        o.menu.width, o.menu.height = 300, 200
        o.menu.reportBug.y, o.menu.modListDetail.y, o.menu.termsOfService.y = 185, 172, 156
        o.gir()
        kutu = o.menu.cocuklar[1]
        yazi, kapat, site = [kutu.cocuklar[i] for i in (1, 2, 3)]
        self.assertGreaterEqual(kutu.x, 0)
        self.assertLessEqual(kutu.x + kutu.width, o.menu.width)
        self.assertLess(kutu.y + kutu.height, 156)
        self.assertTrue(yazi.kaydirma)
        self.assertTrue(yazi.clip)
        self.assertLessEqual(site.x + site.width, kutu.width)
        self.assertLessEqual(kapat.y + kapat.height, kutu.height)

    def test_pano_islevi_yoksa_kutu_gosterilmeye_devam_eder(self):
        o = Oyun()
        o.g.Clipboard = None
        o.gir()
        kutu = o.menu.cocuklar[1]
        self.assertEqual(len(kutu.cocuklar), 2)
        self.assertEqual(kutu.cocuklar[1].text, METIN["UI_ALifeTR_Bilgi_Metin"])

    def test_hata_olursa_kendini_kapatir(self):
        o = Oyun()
        o.lua.execute("getTextManager = function() error('bozuk') end")
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 0)
        self.assertTrue(o.g.ALifeTurkce_Bilgi.kapali)
        o.lua.execute("getTextManager = nil")
        o.gir()  # kapalıyken bir daha denemez
        self.assertEqual(len(o.menu.cocuklar), 0)

    def test_menu_dugmesi_yoksa_koseye_konur(self):
        o = Oyun()
        for ad in ("reportBug", "modListDetail", "termsOfService"):
            o.menu[ad] = None
        o.gir()
        kutu = o.menu.cocuklar[1]
        self.assertLessEqual(kutu.x + kutu.width, 1920)
        self.assertLessEqual(kutu.y + kutu.height, 1080)

    def test_metin_kullanici_metniyle_birebir(self):
        self.assertEqual(METIN["UI_ALifeTR_Bilgi_Baslik"], "Selam,")
        self.assertEqual(
            METIN["UI_ALifeTR_Bilgi_Metin"],
            "A Life Yamasını kullandığın için teşekkür ederim. Yamayı daima güncel tutacağım; "
            "senin desteğin de bu emeğin önemli bir parçası.\n"
            "Steam'de bırakacağın bir beğeni, yamanın yıldız almasına katkıda bulunuyor. "
            "Birkaç saniyeni ayırıp beğeni bırakırsan sevinirim.\n\nİyi oyunlar.",
        )
        self.assertNotIn("UI_ALifeTR_Bilgi_Surum", METIN)


if __name__ == "__main__":
    unittest.main()
