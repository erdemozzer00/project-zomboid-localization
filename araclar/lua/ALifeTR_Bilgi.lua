-- Project A-Life Turkce Ceviri: ana menu bilgi kutusu (K55).
--
-- Ana menuye bir kez, sag alttaki dugmelerin (Hata Bildir, Modlar...) ustune kucuk bir kutu ekler.
-- Oyunun hicbir fonksiyonunu sarmaz ve degistirmez: OnMainMenuEnter'da kendi paneli MainScreen'e
-- cocuk olarak eklenir. A-Life'a bagimli degildir (menude A-Life dosyalari yuklu olmayabilir).
--
-- Metinler TR UI.json'da (UI_ALifeTR_Bilgi_*), getText ile okunur; Lua'ya Turkce harf yazilmaz.
-- Metin yoksa (getText anahtarin kendisini dondururse) kutu gosterilmez.
-- Kapat'a basilinca mesajin surumu Lua/ALifeTR_Bilgi.txt dosyasina yazilir; surum degisince yeniden cikar.
-- Oyun dili Turkce degilse hicbir sey yapmaz. Hata olursa kendini kapatir.

require "ISUI/ISPanel"
require "ISUI/ISButton"
require "ISUI/ISRichTextPanel"

local Ek = { kapali = false }
ALifeTurkce_Bilgi = Ek

local DOSYA = "ALifeTR_Bilgi.txt"
local K_BASLIK, K_METIN, K_KAPAT, K_SURUM =
    "UI_ALifeTR_Bilgi_Baslik", "UI_ALifeTR_Bilgi_Metin", "UI_ALifeTR_Bilgi_Kapat", "UI_ALifeTR_Bilgi_Surum"

local function turkce()
    if Ek.turkce == nil then
        local ok, ad = pcall(function() return tostring(Translator.getLanguage():name()) end)
        Ek.turkce = ok and ad == "TR"
    end
    return Ek.turkce
end

local function metin(anahtar)
    local ok, t = pcall(getText, anahtar)
    if not ok or type(t) ~= "string" or t == "" or t == anahtar then return nil end
    return t
end

local function gorulenSurum()
    local ok, s = pcall(function()
        local okuyucu = getFileReader(DOSYA, false)
        if not okuyucu then return nil end
        local satir = okuyucu:readLine()
        okuyucu:close()
        return satir
    end)
    if ok then return s end
    return nil
end

local function surumYaz(surum)
    pcall(function()
        local yazici = getFileWriter(DOSYA, true, false)
        if not yazici then return end
        yazici:write(surum)
        yazici:close()
    end)
end

-- Kutu: zift zemin, ince mavi neon kenar, hafif dis parilti. Her kare yalnizca birkac dikdortgen cizer.
local Kutu = ISPanel:derive("ALifeTurkce_BilgiKutu")

function Kutu:prerender()
    local g = self.neon
    -- dis parilti
    self:drawRect(-2, -2, self.width + 4, self.height + 4, 0.10, g.r, g.g, g.b)
    self:drawRect(-1, -1, self.width + 2, self.height + 2, 0.18, g.r, g.g, g.b)
    -- zemin
    self:drawRect(0, 0, self.width, self.height, 0.96, 0.03, 0.035, 0.04)
    self:drawRectBorder(0, 0, self.width, self.height, 0.95, g.r, g.g, g.b)
    self:drawText(self.baslik, self.kenar, self.kenar - 2, g.r, g.g, g.b, 1, UIFont.Small)
end

-- Gorunmez eleman cizilmez ve prerender'i cagrilmaz; bu yuzden gorunurluk disaridan esitlenir.
-- Ana menunun alt paneli (Ayarlar, Mods, Solo...) acilinca kutu, oyunun kendi dugmeleri gibi gizlenir.
local function esitle()
    local kutu = Ek.kutu
    if kutu == nil then
        Events.OnTick.Remove(esitle)
        return
    end
    local ana = kutu.parent
    if ana == nil or ana.bottomPanel == nil then return end
    local gorunur = ana.bottomPanel:isVisible()
    if kutu:getIsVisible() ~= gorunur then kutu:setVisible(gorunur) end
end

function Kutu:kapat()
    surumYaz(self.surum)
    if self.parent then self.parent:removeChild(self) end
    Ek.kutu = nil
end

local function kur()
    if Ek.kapali or not turkce() then return end
    local ana = MainScreen and MainScreen.instance
    if ana == nil or ana.inGame or ana.bottomPanel == nil then return end
    if Ek.kutu ~= nil and Ek.kutu.parent == ana then return end

    local baslik, govde, kapat, surum = metin(K_BASLIK), metin(K_METIN), metin(K_KAPAT), metin(K_SURUM)
    if baslik == nil or govde == nil or kapat == nil or surum == nil then return end
    if gorulenSurum() == surum then return end

    local tm = getTextManager()
    local satir = tm:getFontHeight(UIFont.Small)
    local kenar = math.max(10, math.floor(satir * 0.8))
    local genislik = math.max(280, satir * 24)

    local yazi = ISRichTextPanel:new(kenar, satir + kenar, genislik - kenar * 2, 10)
    yazi.defaultFont = UIFont.Small
    yazi.backgroundColor = { r = 0, g = 0, b = 0, a = 0 }
    yazi.borderColor = { r = 0, g = 0, b = 0, a = 0 }
    yazi.marginLeft, yazi.marginTop, yazi.marginRight, yazi.marginBottom = 0, 0, 0, 0
    yazi.autosetheight = true
    yazi:initialise()
    yazi:instantiate()
    yazi.text = govde
    yazi:paginate()

    local dugmeY = yazi:getY() + yazi:getHeight() + kenar
    local dugmeEn = math.max(80, tm:MeasureStringX(UIFont.Small, kapat) + kenar * 2)
    local yukseklik = dugmeY + satir + 8 + kenar

    -- sag alttaki oyun dugmelerinin (Hata Bildir, Modlar, Kullanim Sartlari, Lua sifirla) hemen ustu
    local sag, ust = nil, nil
    for _, ad in ipairs({ "reportBug", "modListDetail", "termsOfService", "resetLua" }) do
        local d = ana[ad]
        if d ~= nil then
            ust = ust and math.min(ust, d:getY()) or d:getY()
            sag = sag or (d:getX() + d:getWidth())
        end
    end
    sag = sag or (ana.width - kenar * 4)
    ust = ust or (ana.height - kenar * 4)
    local x = sag - genislik
    local y = math.max(kenar, ust - kenar - yukseklik)

    local kutu = Kutu:new(x, y, genislik, yukseklik)
    kutu.backgroundColor = { r = 0, g = 0, b = 0, a = 0 }
    kutu.borderColor = { r = 0, g = 0, b = 0, a = 0 }
    kutu.neon = { r = 0.20, g = 0.62, b = 1.0 }
    kutu.baslik, kutu.surum, kutu.kenar = baslik, surum, kenar
    kutu.anchorLeft, kutu.anchorRight, kutu.anchorTop, kutu.anchorBottom = false, true, false, true
    kutu:initialise()
    kutu:addChild(yazi)

    local dugme = ISButton:new(genislik - kenar - dugmeEn, dugmeY, dugmeEn, satir + 8, kapat, kutu, Kutu.kapat)
    dugme.borderColor = { r = 0.20, g = 0.62, b = 1.0, a = 0.9 }
    dugme.backgroundColor = { r = 0.03, g = 0.035, b = 0.04, a = 1 }
    dugme.backgroundColorMouseOver = { r = 0.06, g = 0.14, b = 0.22, a = 1 }
    dugme:initialise()
    kutu:addChild(dugme)

    ana:addChild(kutu)
    Ek.kutu = kutu
    Events.OnTick.Remove(esitle)
    Events.OnTick.Add(esitle)
end

local function guvenliKur()
    local ok = pcall(kur)
    if not ok then
        Ek.kapali = true
        print("[ALifeTurkce] Bilgi kutusu hata verdi, kapatildi.")
    end
end

Events.OnMainMenuEnter.Add(guvenliKur)
