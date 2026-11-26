-- Project A-Life Turkce Ceviri: ana menu bilgi kutusu (K55, gosterim K64).
--
-- Ana menuye her giriste, sag alttaki dugmelerin (Hata Bildir, Modlar...) ustune kucuk bir kutu ekler.
-- Oyunun hicbir fonksiyonunu sarmaz ve degistirmez: OnMainMenuEnter'da kendi paneli MainScreen'e
-- cocuk olarak eklenir. A-Life'a bagimli degildir (menude A-Life dosyalari yuklu olmayabilir).
--
-- Metinler TR UI.json'da (UI_ALifeTR_Bilgi_*), getText ile okunur; Lua'ya Turkce harf yazilmaz.
-- Metin yoksa (getText anahtarin kendisini dondururse) kutu gosterilmez.
-- Kapat dugmesi yalnizca o anki kutuyu kaldirir; okundu bilgisi kalici olarak kaydedilmez.
-- Oyun dili Turkce degilse hicbir sey yapmaz. Hata olursa kendini kapatir.

require "ISUI/ISPanel"
require "ISUI/ISButton"
require "ISUI/ISRichTextPanel"

local Ek = { kapali = false }
ALifeTurkce_Bilgi = Ek

local K_BASLIK, K_METIN, K_KAPAT =
    "UI_ALifeTR_Bilgi_Baslik", "UI_ALifeTR_Bilgi_Metin", "UI_ALifeTR_Bilgi_Kapat"
local K_SITE_DAVET = "UI_ALifeTR_Bilgi_SiteDavet"
local K_SITE_BAGLANTI = "UI_ALifeTR_Bilgi_SiteBaglanti"
local K_SITE_KOPYALANDI = "UI_ALifeTR_Bilgi_SiteKopyalandi"
local SITE_ADRESI = "https://ozzer-yerellestirme.netlify.app/"

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
    if self.parent then self.parent:removeChild(self) end
    Ek.kutu = nil
end

local function kur()
    if Ek.kapali or not turkce() then return end
    local ana = MainScreen and MainScreen.instance
    if ana == nil or ana.inGame or ana.bottomPanel == nil then return end
    if Ek.kutu ~= nil and Ek.kutu.parent == ana then return end

    local baslik, govde, kapat = metin(K_BASLIK), metin(K_METIN), metin(K_KAPAT)
    if baslik == nil or govde == nil or kapat == nil then return end

    local tm = getTextManager()
    local satir = tm:getFontHeight(UIFont.Small)
    local kenar = math.max(10, math.floor(satir * 0.8))
    local dugmeBoy = satir + 8
    local dugmeEn = math.max(80, tm:MeasureStringX(UIFont.Small, kapat) + kenar * 2)

    -- sag alttaki oyun dugmelerinin (Hata Bildir, Modlar, Kullanim Sartlari, Lua sifirla) hemen ustu
    local sag, ust = nil, nil
    for _, ad in ipairs({ "reportBug", "modListDetail", "termsOfService", "resetLua" }) do
        local d = ana[ad]
        if d ~= nil then
            ust = ust and math.min(ust, d:getY()) or d:getY()
            sag = sag or (d:getX() + d:getWidth())
        end
    end
    sag = math.min(sag or (ana.width - kenar * 4), ana.width - kenar)
    ust = math.min(ust or (ana.height - kenar * 4), ana.height - kenar)
    local genislik = math.min(math.max(280, satir * 24), sag - kenar)
    local icerikEn = genislik - kenar * 2
    local yaziY = satir + kenar
    local yaziBoySiniri = ust - yaziY - dugmeBoy - kenar * 4
    if icerikEn < dugmeEn or yaziBoySiniri < satir then return end

    local davet, baglanti = metin(K_SITE_DAVET), metin(K_SITE_BAGLANTI)
    local kopyalandi = metin(K_SITE_KOPYALANDI)
    local baglantiEn = baglanti and kopyalandi and math.max(
        tm:MeasureStringX(UIFont.Small, baglanti), tm:MeasureStringX(UIFont.Small, kopyalandi)
    ) + kenar * 2
    local baglantiBoy = dugmeBoy + kenar
    local siteGorunur = Clipboard and Clipboard.setClipboard and davet and baglantiEn and baglantiEn <= icerikEn
        and yaziBoySiniri - baglantiBoy >= satir
    if siteGorunur then
        govde = govde .. "\n\n" .. davet
        yaziBoySiniri = yaziBoySiniri - baglantiBoy
    end

    local yazi = ISRichTextPanel:new(kenar, yaziY, icerikEn, 10)
    yazi.defaultFont = UIFont.Small
    yazi.backgroundColor = { r = 0, g = 0, b = 0, a = 0 }
    yazi.borderColor = { r = 0, g = 0, b = 0, a = 0 }
    yazi.marginLeft, yazi.marginTop, yazi.marginRight, yazi.marginBottom = 0, 0, 0, 0
    yazi.autosetheight = true
    yazi:initialise()
    yazi:instantiate()
    yazi.text = govde
    yazi:paginate()
    local kaydir = yazi:getHeight() > yaziBoySiniri
    if kaydir then
        yazi.clip = true
        yazi.autosetheight = false
        yazi.marginRight = 17
        yazi:setHeight(yaziBoySiniri)
        yazi:paginate()
    end

    local baglantiY = yaziY + yazi:getHeight() + kenar
    local dugmeY = baglantiY + (siteGorunur and baglantiBoy or 0)
    local yukseklik = dugmeY + dugmeBoy + kenar
    local x = sag - genislik
    local y = math.max(kenar, ust - kenar - yukseklik)

    local kutu = Kutu:new(x, y, genislik, yukseklik)
    kutu.backgroundColor = { r = 0, g = 0, b = 0, a = 0 }
    kutu.borderColor = { r = 0, g = 0, b = 0, a = 0 }
    kutu.neon = { r = 0.20, g = 0.62, b = 1.0 }
    kutu.baslik, kutu.kenar = baslik, kenar
    kutu.anchorLeft, kutu.anchorRight, kutu.anchorTop, kutu.anchorBottom = false, true, false, true
    kutu:initialise()
    kutu:addChild(yazi)
    if kaydir then yazi:addScrollBars() end

    local dugme = ISButton:new(genislik - kenar - dugmeEn, dugmeY, dugmeEn, dugmeBoy, kapat, kutu, Kutu.kapat)
    dugme.borderColor = { r = 0.20, g = 0.62, b = 1.0, a = 0.9 }
    dugme.backgroundColor = { r = 0.03, g = 0.035, b = 0.04, a = 1 }
    dugme.backgroundColorMouseOver = { r = 0.06, g = 0.14, b = 0.22, a = 1 }
    dugme:initialise()
    kutu:addChild(dugme)

    if siteGorunur then
        local site = ISButton:new(kenar, baglantiY, baglantiEn, dugmeBoy, baglanti, kutu, function(_, dugme)
            local ok = pcall(function() Clipboard.setClipboard(SITE_ADRESI) end)
            dugme:setTitle(ok and kopyalandi or baglanti)
        end)
        site.font = UIFont.Small
        site.textColor = { r = 0.45, g = 0.76, b = 1, a = 1 }
        site.borderColor = { r = 0.20, g = 0.62, b = 1.0, a = 0.9 }
        site.backgroundColor = { r = 0.03, g = 0.035, b = 0.04, a = 1 }
        site.backgroundColorMouseOver = { r = 0.06, g = 0.14, b = 0.22, a = 1 }
        site:initialise()
        kutu:addChild(site)
    end

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
