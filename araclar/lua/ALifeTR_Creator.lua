-- Project A-Life Türkçe Çeviri: Oluşturucu (Creator) ekranındaki sabit yazılar (K24, K27).
--
-- Modun dosyalarına dokunmaz, oyunun genel arayüz sınıflarını (ISButton, ISLabel…) değiştirmez.
-- Yalnızca Oluşturucu penceresinin kendi öğelerinde, yazı ekrana çizilirken metni modun
-- Text.ui çeviri kanalına sorar (anahtar: IGUI_ALifeUI_ + hash, çeviriler TR IG_UI.json'da).
-- Çevirisi olmayan yazı İngilizce kalır. Oyun dili Türkçe değilse hiçbir şey yapmaz.
-- Bir hata olursa kendini kapatır ve Oluşturucu İngilizce çalışmaya devam eder.
--
-- Bu dosya araclar/workshop_kur.py tarafından üretilir; ön ek listesi kaynak/Creator_onek.json'dan gelir.
-- Not: Türkçe harfler bu dosyaya yazılmaz (Lua dosyasındaki ş/ğ/ı oyunda bozuk çıkar).

require "ProjectALife/Interface/Creator/ALifeCreatorCore"

local Ek = { kapali = false, kare = 0, onbellek = {} }
ALifeTurkce_Creator = Ek

-- Sonuna sayı ya da ad eklenen yazılar ("PAGE 2 / 5", "ID: x"): ön ek çevrilir, kalan ayrıca çevrilir.
local ONEKLER = __ONEKLER__

-- Parçalardan birleşen yazılar ("3 MAGS", "Hat choices"): kalıp çevrilir, {x} yerine gelen yazı da ayrıca
-- çevrilir, sayılar ({n} {m} {k} {w}) aynen kalır. Kaynak: kaynak/Creator_kalip.json (C3).
local KALIPLAR = __KALIPLAR__

-- Hiçbiri tutmazsa yazı bu ayraçlardan bölünüp parça parça çevrilir ("ID: x  /  CUSTOM")
local AYRACLAR = { "  /  ", "  -  ", " / ", " - ", " | " }

-- Dil değişikliği oyunu yeniden başlatmayı gerektirir; sonuç bir kez hesaplanır
local function turkce()
    if Ek.turkce == nil then
        local ok, ad = pcall(function() return tostring(Translator.getLanguage():name()) end)
        Ek.turkce = ok and ad == "TR"
    end
    return Ek.turkce
end

local function sor(s)
    local text = ProjectALife and ProjectALife.Text
    if text == nil or type(text.ui) ~= "function" then return s end
    local t = text.ui(s)
    if type(t) ~= "string" or t == "" then return s end
    return t
end

local cevir

local function kalip(s, derinlik)
    for i = 1, #KALIPLAR do
        local k = KALIPLAR[i]
        local yakalanan = { string.match(s, k.desen) }
        if yakalanan[1] ~= nil then
            local t = sor(k.en)
            if t == k.en then return s end
            for j, ad in ipairs(k.adlar) do
                local deger = yakalanan[j] or ""
                if not string.find("nmkw", ad, 1, true) then deger = cevir(deger, derinlik + 1) end
                t = string.gsub(t, "{" .. ad .. "}", (string.gsub(deger, "%%", "%%%%")))
            end
            return t
        end
    end
    return s
end

local function bol(s, derinlik)
    for _, ayrac in ipairs(AYRACLAR) do
        if string.find(s, ayrac, 1, true) then
            local parcalar, degisti, bas = {}, false, 1
            while true do
                local i, j = string.find(s, ayrac, bas, true)
                local parca = string.sub(s, bas, (i or 0) - 1)
                local t = cevir(parca, derinlik + 1)
                if t ~= parca then degisti = true end
                parcalar[#parcalar + 1] = t
                if i == nil then break end
                bas = j + 1
            end
            if degisti then return table.concat(parcalar, ayrac) end
            return s
        end
    end
    return s
end

local function bul(s, derinlik)
    local t = sor(s)
    if t ~= s or derinlik > 4 then return t end
    t = kalip(s, derinlik)
    if t ~= s then return t end
    for i = 1, #ONEKLER do
        local onek = ONEKLER[i]
        if #s > #onek and string.sub(s, 1, #onek) == onek then
            local ceviri = sor(onek)
            if ceviri ~= onek then return ceviri .. cevir(string.sub(s, #onek + 1), derinlik + 1) end
            break
        end
    end
    return bol(s, derinlik)
end

cevir = function(s, derinlik)
    if type(s) ~= "string" or s == "" then return s end
    local hazir = Ek.onbellek[s]
    if hazir ~= nil then return hazir end
    local t = bul(s, derinlik or 0)
    -- Oluşturucu yazıları büyük ölçüde sabit; önbellek yine de sınırsız büyümesin
    if Ek.onbellekSay == nil or Ek.onbellekSay > 4000 then Ek.onbellek, Ek.onbellekSay = {}, 0 end
    Ek.onbellek[s] = t
    Ek.onbellekSay = Ek.onbellekSay + 1
    return t
end

local function genislik(font, s)
    local ok, w = pcall(function() return getTextManager():MeasureStringX(font or UIFont.Small, s) end)
    return ok and w or 0
end

local function kapat(hata)
    if Ek.kapali then return end
    Ek.kapali = true
    print("[ProjectALife TR] Olusturucu cevirisi kapatildi: " .. tostring(hata))
end

local function sar(oge)
    -- İşaret öğenin üstünde durur (ayrı tablo tutulursa kapanan pencereler bellekte kalır)
    if oge.ALifeTurkceSarili then return end
    oge.ALifeTurkceSarili = true
    for _, ad in ipairs({ "drawText", "drawTextCentre", "drawTextRight" }) do
        local asil = oge[ad]
        if type(asil) == "function" then
            oge[ad] = function(self, s, x, y, r, g, b, a, font, ...)
                if not Ek.kapali and type(s) == "string" then
                    local ok, t = pcall(cevir, s)
                    if not ok then
                        kapat(t)
                    elseif t ~= s then
                        -- ISButton başlığı İngilizce genişliğe göre ortalanmış; Türkçe için yeniden ortala
                        if ad == "drawText" and s == self.title and not self.titleLeft and self.iconTexture == nil
                            and not self.isJoypad and type(self.width) == "number" then
                            x = math.max(2, self.width / 2 - genislik(font, t) / 2)
                        end
                        s = t
                    end
                end
                return asil(self, s, x, y, r, g, b, a, font, ...)
            end
        end
    end
end

-- drawText'ten geçmeyen yazılar öğenin alanında durur: ipucu (ayrı ISToolTip penceresinde çizilir),
-- açılır liste seçenekleri (açılan liste UIManager'da, pencerenin çocuğu değil), bölüm kartının başlık ve
-- açıklaması (çizilmeden önce kırpılır), arama kutusu ipucu. Bunlar yerinde çevrilir; mod bu yazıları
-- yalnızca gösterir, seçenekler veriyle (getOptionData) okunur. Mod alanı yeniden yazarsa yeniden çevrilir.
local function yerinde(tablo, alan)
    local s = tablo[alan]
    if type(s) ~= "string" or s == "" or s == tablo["ALifeTR_" .. alan] then return end
    local t = cevir(s)
    tablo[alan] = t
    tablo["ALifeTR_" .. alan] = t
end

local function alanlar(oge)
    if type(oge.tooltip) == "table" then yerinde(oge.tooltip, "defaultTooltip") else yerinde(oge, "tooltip") end
    yerinde(oge, "sectionTitle")
    yerinde(oge, "sectionSummary")
    if type(oge.options) == "table" and type(oge.addOptionWithData) == "function" then
        for _, secenek in ipairs(oge.options) do
            if type(secenek) == "table" then
                yerinde(secenek, "text")
                yerinde(secenek, "tooltip")
            end
        end
    end
    if type(oge.getPlaceholderText) == "function" and type(oge.setPlaceholderText) == "function" then
        local ok, s = pcall(oge.getPlaceholderText, oge)
        if ok and type(s) == "string" and s ~= "" and s ~= oge.ALifeTR_ipucu then
            local t = cevir(s)
            oge.ALifeTR_ipucu = t
            if t ~= s then oge:setPlaceholderText(t) end
        end
    end
end

local function gez(oge, derinlik)
    if type(oge) ~= "table" or derinlik > 60 then return end
    sar(oge)
    alanlar(oge)
    local cocuklar = oge.children
    if type(cocuklar) == "table" then
        for _, cocuk in pairs(cocuklar) do gez(cocuk, derinlik + 1) end
    end
end

local function pencere(w)
    if type(w) ~= "table" or w.ALifeTurkcePencere then return end
    w.ALifeTurkcePencere = true
    gez(w, 0)
    local asil = w.prerender
    if type(asil) ~= "function" then return end
    -- Sekme değişince yeni öğeler eklenir: birkaç karede bir yeni öğeleri de sar
    w.prerender = function(self, ...)
        if not Ek.kapali then
            Ek.kare = Ek.kare + 1
            if Ek.kare % 15 == 0 then
                local ok, hata = pcall(gez, self, 0)
                if not ok then kapat(hata) end
            end
        end
        return asil(self, ...)
    end
end

local function kur()
    local Creator = ProjectALife and ProjectALife.CreatorScreen
    if type(Creator) ~= "table" or Creator.ALifeTurkceKurulu or type(Creator.open) ~= "function" then return end
    Creator.ALifeTurkceKurulu = true
    local asilAc = Creator.open
    Creator.open = function(...)
        local sonuc = { asilAc(...) }
        if not Ek.kapali and turkce() then
            local ok, hata = pcall(pencere, Creator.window)
            if not ok then kapat(hata) end
        end
        return unpack(sonuc)
    end
    -- Diğer Oluşturucu dosyaları yazıyı Creator.fitText ile kırpıp öyle veriyor ("Visitor-only facti...");
    -- kırpılmış İngilizce bulunamaz, o yüzden kırpmadan önce çevrilir.
    local asilSigdir = Creator.fitText
    if type(asilSigdir) == "function" then
        Creator.fitText = function(s, ...)
            if not Ek.kapali and type(s) == "string" and turkce() then
                local ok, t = pcall(cevir, s)
                if ok then s = t else kapat(t) end
            end
            return asilSigdir(s, ...)
        end
    end
    -- Ana menüdeki Project A-Life kartının alt yazısı ("Factions & NPC settings"):
    -- kart her karede Creator.menuSubtitle()'ı çağırır; yalnızca dönen yazı çevrilir.
    local asilAlt = Creator.menuSubtitle
    if type(asilAlt) == "function" then
        Creator.menuSubtitle = function(...)
            local s = asilAlt(...)
            if Ek.kapali or not turkce() then return s end
            local ok, t = pcall(cevir, s)
            if not ok then kapat(t) return s end
            return t
        end
    end
end

local ok, hata = pcall(kur)
if not ok then kapat(hata) end
