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
    function o:paginate() self.height = 60 end
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
    local o = eleman(x, y, w, h); o.baslik, o.hedef, o.tikla = baslik, hedef, tikla; return o
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

    def test_gorulen_surum_tekrar_gosterilmez_yeni_surum_gosterilir(self):
        o = Oyun(gorulen=METIN["UI_ALifeTR_Bilgi_Surum"])
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 0)
        o = Oyun(gorulen="0")
        o.gir()
        self.assertEqual(len(o.menu.cocuklar), 1)

    def test_kapat_surumu_yazar_ve_kutuyu_kaldirir(self):
        o = Oyun()
        o.gir()
        kutu = o.menu.cocuklar[1]
        dugme = kutu.cocuklar[2]
        dugme.tikla(dugme.hedef, dugme)
        self.assertEqual(len(o.menu.cocuklar), 0)
        self.assertEqual(o.g.DOSYA_ICERIK, METIN["UI_ALifeTR_Bilgi_Surum"])

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

    def test_metin_turkce_harfli_ve_satirlari_var(self):
        t = METIN["UI_ALifeTR_Bilgi_Metin"]
        self.assertIn("\n", t)
        self.assertIn("Türkçe", t)


if __name__ == "__main__":
    unittest.main()
