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
    local boya = string.match(s, "^Saved: default car, (.+)%.$")
    if boya ~= nil then
        local onek = sor("Saved: default car, ")
        if onek ~= "Saved: default car, " then return onek .. sor(boya) .. "." end
    end
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
-- Only Creator tooltips contain these rule blocks. Read the same ordered notes as the
-- card builder, including opt-in notes; keep the underlying module and combo data raw.
local function kuralIpucu(s, bas, son)
    local creator, rules = ProjectALife.CreatorScreen, ProjectALife.ModuleRules
    if not rules or type(rules.notes) ~= "function" then return cevir(s) end
    local tam = sor(s)
    if tam ~= s then return tam end
    local govde, kalan = string.sub(s, 1, bas - 1), string.sub(s, son + 1)
    for _, spec in ipairs(creator.memberModules or {}) do
        local notlar = rules.notes(spec[2])
        local blok = table.concat(notlar, " ")
        if blok ~= "" and string.sub(kalan, 1, #blok) == blok then
            local ek = string.sub(kalan, #blok + 1)
            if ek == "" or string.sub(ek, 1, 5) == " Use " then
                -- A disabled combo repeats its rule in a warning before the base help.
                local uyari, yardim = string.match(govde, "^(Disabled.-) | (.*)$")
                local cevrilen = {}
                for i, notMetni in ipairs(notlar) do
                    cevrilen[i] = sor(notMetni)
                    if uyari and string.sub(uyari, -(#notMetni + 1)) == " " .. notMetni then
                        uyari = string.sub(uyari, 1, #uyari - #notMetni) .. cevrilen[i]
                    end
                end
                local metin = cevir(yardim or govde) .. " " .. sor("RULES:") .. " " .. table.concat(cevrilen, " ")
                if ek ~= "" then metin = cevir(metin .. ek) end
                return uyari and (uyari .. " | " .. metin) or metin
            end
        end
    end
    return cevir(s)
end

local function ipucuCevir(s)
    local bas, son = string.find(s, " RULES: ", 1, true)
    if bas then
        local ok, metin = pcall(kuralIpucu, s, bas, son)
        if ok then return metin end
    end
    return cevir(s)
end

local function yerinde(tablo, alan, cevirici)
    local s = tablo[alan]
    if type(s) ~= "string" or s == "" or s == tablo["ALifeTR_" .. alan] then return end
    local t = (cevirici or cevir)(s)
    tablo[alan] = t
    tablo["ALifeTR_" .. alan] = t
end

local function alanlar(oge)
    if type(oge.tooltip) == "table" then
        yerinde(oge.tooltip, "defaultTooltip", ipucuCevir)
    else
        yerinde(oge, "tooltip", ipucuCevir)
    end
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

local function sarKiyafetKatalogu(asil)
    return function(window, kind, slot, combo, title, ...)
        local onceki = window.itemPicker
        asil(window, kind, slot, combo, title, ...)
        local katalog = window.itemPicker
        if Ek.kapali or not turkce() or kind ~= "clothing" or slot ~= "Back"
                or title ~= "Back choices" or katalog == nil or katalog == onceki then return end
        local kalip, yuva = sor("{x} choices"), sor("BACK")
        if kalip == "{x} choices" or yuva == "BACK" then return end
        for _, oge in pairs(katalog.children or {}) do
            if oge.name == "BACK CHOICES" and type(oge.setNameWithoutMoving) == "function" then
                oge:setNameWithoutMoving(ProjectALife.Text.fill(kalip, { x = yuva }))
                return
            end
        end
    end
end

local function sigdirUtf8(text, font, room)
    if genislik(font, text) <= room then return text end
    local index = #text
    while index > 0 do
        local byte = string.byte(text, index)
        if byte < 128 or byte >= 192 then
            local clipped = string.sub(text, 1, index - 1) .. "..."
            if genislik(font, clipped) <= room then return clipped end
        end
        index = index - 1
    end
    return ""
end

local function kiyafetRozetiniBagla(Creator)
    local badge = Creator.outfitHealth
    if type(badge) ~= "table" or badge.ALifeTurkceRozet or type(badge.install) ~= "function" then return end
    local install = badge.install
    badge.install = function(window, page, ...)
        local previous = window.healthBadge
        install(window, page, ...)
        local control, fix = window.healthBadge, window.healthFixButton
        if not turkce() or Ek.kapali or previous == control or control == nil or fix == nil then return end
        local caption, px = sor("OUTFIT SETS"), Creator.px
        for _, label in pairs(page.children or {}) do
            if label.name == caption and type(label.setName) == "function" then
                local gap = px(8)
                local right = fix.x - gap
                local room = math.max(0, right - label.x - gap - px(60))
                local title = sigdirUtf8(caption, label.font, room)
                label:setName(title)
                local x = math.min(right, math.max(control.x, label.x + genislik(label.font, title) + gap))
                control:setX(x)
                control:setWidth(math.max(0, right - x))
                return
            end
        end
    end
    badge.ALifeTurkceRozet = true
end

local function kur()
    local Creator = ProjectALife and ProjectALife.CreatorScreen
    if type(Creator) ~= "table" or Creator.ALifeTurkceKurulu or type(Creator.open) ~= "function" then return end
    Creator.ALifeTurkceKurulu = true
    -- refreshModuleRuleHints rewrites the combo tooltip immediately on a state change.
    local asilIpucu = Creator.addTooltip
    if type(asilIpucu) == "function" then
        Creator.addTooltip = function(control, text, ...)
            if not Ek.kapali and type(control) == "table" and control.ruleTip and type(text) == "string"
                    and string.find(text, " RULES: ", 1, true) and turkce() then
                local ok, metin = pcall(ipucuCevir, text)
                if ok then text = metin end
            end
            return asilIpucu(control, text, ...)
        end
    end
    local asilEtiket = Creator.addLabel
    if type(asilEtiket) == "function" then
        Creator.addLabel = function(panel, x, y, label, ...)
            if not Ek.kapali and turkce() and (label == "Eyeshadow" or label == "OUTFIT SETS") then
                label = sor(label)
            end
            return asilEtiket(panel, x, y, label, ...)
        end
    end
    if type(Creator.openItemPicker) == "function" then
        Creator.openItemPicker = sarKiyafetKatalogu(Creator.openItemPicker)
    end
    local asilEsyaAdi = Creator.shortItemName
    if type(asilEsyaAdi) == "function" then
        Creator.shortItemName = function(fullType)
            if not Ek.kapali and turkce() and type(fullType) == "string" and fullType:match("^[%w_]+%.[%w_]+$")
                    and type(getItemNameFromFullType) == "function" then
                local ok, name = pcall(getItemNameFromFullType, fullType)
                if ok and type(name) == "string" and name ~= "" and name ~= fullType then return name end
            end
            return asilEsyaAdi(fullType)
        end
    end
    local asilAc = Creator.open
    Creator.open = function(...)
        kiyafetRozetiniBagla(Creator)
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
        Creator.fitText = function(s, font, room, ...)
            if not Ek.kapali and type(s) == "string" and turkce() then
                local ok, t = pcall(cevir, s)
                if ok then
                    s = t
                    if type(room) == "number" and string.find(s, "[\128-\255]") then
                        return sigdirUtf8(s, font, room)
                    end
                else kapat(t) end
            end
            return asilSigdir(s, font, room, ...)
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

local menuTitle = "A-LIFE CREATOR"
local function kartBasligi(s)
    if s == menuTitle and not Ek.kapali and turkce() then return sor(s) end
    return s
end

local function kartiSigdir(chrome, font, title, room)
    if chrome.boldWidth(font, title, 0) <= room then return title end
    local index = #title
    while index > 0 do
        local b = string.byte(title, index)
        if b < 128 or b >= 192 then
            local partial = string.sub(title, 1, index - 1) .. ".."
            if chrome.boldWidth(font, partial, 0) <= room then return partial end
        end
        index = index - 1
    end
    return ""
end

local function kartiKur()
    local creator = ProjectALife and ProjectALife.CreatorScreen
    local tile, chrome = creator and creator.menuTile, ProjectALife and ProjectALife.UI2Chrome
    if tile ~= nil and not tile.ALifeTurkceBaslik
            and type(tile.title) == "function" and type(tile.titleWidth) == "function" then
        local title, width = tile.title, tile.titleWidth
        -- The tracked renderer measures and draws byte by byte, which splits Turkish characters.
        tile.title = function(self, s, x, y, font, color, track, ...)
            local tr = kartBasligi(s)
            return title(self, tr, x, y, font, color, tr ~= s and 0 or track, ...)
        end
        tile.titleWidth = function(s, font, track, ...)
            local tr = kartBasligi(s)
            return width(tr, font, tr ~= s and 0 or track, ...)
        end
        tile.ALifeTurkceBaslik = true
    end
    if chrome ~= nil and not chrome.ALifeTurkceKartSigdirma and type(chrome.capsFit) == "function"
            and type(chrome.boldWidth) == "function" then
        local fit = chrome.capsFit
        chrome.capsFit = function(font, s, track, room, ...)
            local tr = kartBasligi(s)
            if tr ~= s and type(room) == "number" then return kartiSigdir(chrome, font, tr, room) end
            return fit(font, s, track, room, ...)
        end
        chrome.ALifeTurkceKartSigdirma = true
    end
end

local ok, hata = pcall(kur)
if not ok then kapat(hata) end
kartiKur()
if type(Events) == "table" and Events.OnGameBoot ~= nil then Events.OnGameBoot.Add(kartiKur) end
