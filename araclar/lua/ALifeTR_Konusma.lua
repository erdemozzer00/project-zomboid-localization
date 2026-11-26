-- Project A-Life Türkçe Çeviri: NPC konuşmaları (K28).
--
-- Mod, NPC repliklerini ekrana basmadan önce her zaman AudioPolicy.caption(text)'ten geçirir
-- (baş üstü yazı, konuşma kutusu, konuşma penceresi). Bu ek yalnızca o fonksiyonun döndürdüğü
-- metni, modun kendi diyalog anahtarıyla (RD_ALifeLine_ + hash, Text.lineKey) çeviri dosyasına sorar.
-- Modun hazırlayıp bağlamadığı Text.spoken yolunun aynısı; Vice bağlarsa bu ek silinir.
--
-- K46 ekleri: rastgele yer tutuculu şablonlar (aşağıda SABLONLAR), kapı/ziyaretçi eylem satırları (DoLines)
-- ve başın üstündeki grup/sığınak bildirimleri (SafehouseClient.notice).
-- 1.5.0: konuşma ağacı düğmeleri, görev satırı ipucu ve bitiş sorusu (kaçan metinler, rapor/kacan_ek_1.5.0.md).
-- İkisi de modun fonksiyonu yoksa ya da değişmişse sessizce devre dışı kalır; satır İngilizce görünür.
--
-- Türkçe metin bu dosyada yok (TR RadioData.json'da). Çevirisi olmayan replik İngilizce kalır.
-- Oyun dili Türkçe değilse hiçbir şey yapmaz. Hata olursa kendini kapatır.
-- Bu dosya araclar/workshop_kur.py tarafından ASCII'ye çevrilip mod klasörüne kopyalanır.

-- Baş üstü yazı (K31): Dialogue fontunda olmayan Türkçe harfler için Small seçilir.
-- Metin değiştirilmez. Renk, 30 karelik mesafe ve "default" etiketi oyunun varsayılanıyla aynıdır.
-- Yalnızca A-Life'ın engineLine yolu sarılır; kutulu konuşmalar kendi fontlarını kullanır.

require "ProjectALife/Audio/ALifeAudioPolicy"
require "ProjectALife/Core/ALifeText"
require "ProjectALife/Talk/ALifeSpeech"

local Ek = { kapali = false, basUstuKapali = false }
ALifeTurkce_Konusma = Ek

local function turkce()
    if Ek.turkce == nil then
        local ok, ad = pcall(function() return tostring(Translator.getLanguage():name()) end)
        Ek.turkce = ok and ad == "TR"
    end
    return Ek.turkce
end

-- Rastgele dolan yer tutuculu şablonlar (K46): {town}, {den}, {name}, {time}… oyunda Speech.render ile
-- doldurulur, caption'a dolu metin gelir; hash'i tutmaz. Ek, dolu metni İngilizce şablonun Lua desenine
-- uydurur, şablonun Türkçesini (anahtar: çıplak şablonun hash'i) alır ve yakalanan değerleri yerine koyar.
-- d = desen, k = anahtar, s = "m"/"f" (şablon cinsiyetle çözüldüyse; Türkçedeki {g:a|b} buna göre), a = yer tutucu adları.
-- Kaynak: araclar/sablon_varyant.py rastgele_sablonlar (workshop_kur.py doldurur).
local SABLONLAR = __SABLONLAR__

-- Bilinen İngilizce dolgu değerlerinin Türkçesi de RadioData'da (RD_ALifeTR_Deger_ + hash(küçük harf));
-- sığınak tarifi, saat ve tarih RD_ALifeTR_Kalip_ biçimleriyle kurulur. Bilinmeyen değer (kasaba, kişi adı) aynen kalır.
local KOVA = nil

local function kovaAnahtari(s)
    return string.lower(string.sub(s, 1, 2))
end

local function kovalar()
    if KOVA ~= nil then return KOVA end
    KOVA = {}
    for i = 1, #SABLONLAR do
        local e = SABLONLAR[i]
        local b = e.b or ""
        KOVA[b] = KOVA[b] or {}
        table.insert(KOVA[b], e)
    end
    return KOVA
end

local function bak(text, anahtar)
    local t = text.lookup(anahtar)
    if type(t) ~= "string" or t == "" then return nil end
    return t
end

local function degerBak(text, v)
    return bak(text, "RD_ALifeTR_Deger_" .. text.hash(string.lower(v)))
end

local function bicim(text, ad, alanlar)
    local b = bak(text, "RD_ALifeTR_Kalip_" .. ad)
    if b == nil then return nil end
    return (string.gsub(b, "{(%a+)}", function(k) return alanlar[k] or ("{" .. k .. "}") end))
end

local ekDeger  -- aşağıda tanımlı (deger ile karşılıklı çağrılır)
local cevirIleri  -- cevir; "what"/"event" gibi başka bir konuşma satırı olan değerler için

local function deger(text, ad, v)
    local d = degerBak(text, v)
    if d ~= nil then return d end
    if ad == "den" then
        local isim, yan, kasaba = string.match(v, "^(.-) on the (%a+) side of (.+)$")
        if isim ~= nil then
            return bicim(text, "den_yan", { noun = degerBak(text, isim) or isim, side = degerBak(text, yan) or yan, town = kasaba }) or v
        end
        isim, kasaba = string.match(v, "^(.-) in the middle of (.+)$")
        if isim ~= nil then
            return bicim(text, "den_orta", { noun = degerBak(text, isim) or isim, town = kasaba }) or v
        end
        isim = string.match(v, "^(.-) out past the county road$")
        if isim ~= nil then
            return bicim(text, "den_disari", { noun = degerBak(text, isim) or isim }) or v
        end
    elseif ad == "time" then
        local saat, yarim = string.match(v, "^(%d+) ([AP]M)$")
        if saat ~= nil then
            local tur = "saat_sabah"
            if yarim == "PM" then
                if tonumber(saat) < 6 then tur = "saat_ogleden_sonra" else tur = "saat_aksam" end
            end
            return bicim(text, tur, { n = saat }) or v
        end
    elseif ad == "date" then
        local ay, gun = string.match(v, "^(%a+) (%d+)%a%a$")
        if ay ~= nil then
            return bicim(text, "tarih", { m = degerBak(text, ay) or ay, d = gun }) or v
        end
    end
    return ekDeger(text, ad, v)
end

-- E1 (1.5.0 Talk/General ve Talk5Home satırları): oyunun İngilizce kurduğu yer ("in the northeast side of X"),
-- süre ("3 days"), konut ("a camp in X"), olay ("X hit somebody ... a while back") değerleri. Kaynak:
-- ALifeTalk5Home.lua areaOf, ALifeTalkGeneralServer.lua span/ago/describe, ALifeTreeServer.lua vars.
local AGOLAR = { "a little while ago", "earlier today", "yesterday", "a couple days back", "a while back" }

local function kacis(s)
    return (string.gsub(s, "%p", "%%%0"))
end

local function yerCevir(text, v)
    local kasaba = string.match(v, "^in the middle of (.+)$")
    if kasaba ~= nil then return bicim(text, "at_orta", { town = kasaba }) end
    local yon
    yon, kasaba = string.match(v, "^in the (%a+) side of (.+)$")
    if yon ~= nil then return bicim(text, "at_yan", { town = kasaba, side = degerBak(text, yon) or yon }) end
    yon, kasaba = string.match(v, "^in the (%a+) end of (.+)$")
    if yon ~= nil then return bicim(text, "at_uc", { town = kasaba, side = degerBak(text, yon) or yon }) end
    kasaba = string.match(v, "^on the edge of (.+)$")
    if kasaba ~= nil then return bicim(text, "at_kenar", { town = kasaba }) end
    kasaba = string.match(v, "^out past (.+)$")
    if kasaba ~= nil then return bicim(text, "at_otesi", { town = kasaba }) end
    return nil
end

local function olayCevir(text, v)
    local crew, yer, ago, kasaba, cok
    for _, a in ipairs(AGOLAR) do
        local ka = kacis(a)
        crew = string.match(v, "^(.-) came after you " .. ka .. ", the whole county heard it$")
        if crew ~= nil then
            return bicim(text, "ev_sana", { crew = degerBak(text, crew) or crew, ago = degerBak(text, a) })
        end
        crew, yer = string.match(v, "^(.-) hit somebody (.+) " .. ka .. "$")
        if crew ~= nil then
            return bicim(text, "ev_baskin", { crew = degerBak(text, crew) or crew, at = yerCevir(text, yer) or degerBak(text, yer) or yer, ago = degerBak(text, a) })
        end
        kasaba = string.match(v, "^a helicopter came over (.+) " .. ka .. "$")
        if kasaba ~= nil then
            return bicim(text, "ev_heli", { town = degerBak(text, kasaba) or kasaba, ago = degerBak(text, a) })
        end
        yer, cok = string.match(v, "^there was shooting (.+) " .. ka .. ", (.+)$")
        if yer ~= nil then
            return bicim(text, "ev_silah", { at = yerCevir(text, yer) or degerBak(text, yer) or yer, ago = degerBak(text, a), many = degerBak(text, cok) or cok })
        end
    end
    yer = string.match(v, "^somebody's been taking prisoners (.+)$")
    if yer ~= nil then return bicim(text, "ev_esir", { at = yerCevir(text, yer) or degerBak(text, yer) or yer }) end
    return nil
end

ekDeger = function(text, ad, v0)
    local v = string.lower(string.sub(v0, 1, 1)) .. string.sub(v0, 2)  -- cümle başındaki değerin ilk harfi büyümüş olabilir
    local t = yerCevir(text, v)
    if t ~= nil then return t end
    local n, birim = string.match(v, "^(%d+) (%a+)$")
    if n ~= nil then
        local k = ({ days = "span_gun", weeks = "span_hafta", months = "span_ay" })[birim]
        if k ~= nil then return bicim(text, k, { n = n }) or v0 end
    end
    local kasaba = string.match(v, "^a camp in (.+)$")
    if kasaba ~= nil then return bicim(text, "kamp_in", { town = kasaba }) or v0 end
    kasaba = string.match(v, "^a house in (.+)$")
    if kasaba ~= nil then return bicim(text, "ev_in", { town = kasaba }) or v0 end
    t = olayCevir(text, v)
    if t ~= nil then return t end
    if cevirIleri ~= nil and (ad == "what" or ad == "event") then  -- {what}: radyonun son söylediği satır; kendi çevirisi varsa o
        local c = cevirIleri(v0)
        if c ~= nil and c ~= v0 then return c end
    end
    return v0
end

-- Yakalanan değer gerçekten o türden mi? Yalnızca "{time}" ya da "{weekday}, {date}" gibi neredeyse tamamı yer
-- tutucu olan şablonlar alakasız cümleleri yakalamasın diye. Türü bilinen değerler oyunun kendi listeleriyle
-- (Speech.months/weekdays/names/streets, TownRegions) denetlenir; liste yoksa değer kabul edilir.
-- Türü bilinmeyen ({den}, {weapon}…) değerler için şablonun sabit yazısı yeterince uzun olmalı (e.serbest).
local function listede(liste, v)
    if type(liste) ~= "table" then return true end
    v = string.lower(v)
    for _, x in pairs(liste) do
        if type(x) == "string" and string.lower(x) == v then return true end
    end
    return false
end

local EKIP = { ["some families"] = true, ["some workers"] = true, ["some medics"] = true, ["cops"] = true,
    ["swat guys"] = true, ["soldiers"] = true, ["outlaws"] = true, ["bikers"] = true, ["gangsters"] = true,
    ["raiders"] = true, ["gangbangers"] = true, ["escaped cons"] = true, ["some people"] = true }
local DEGER_YERADI = { ["the gas station"] = true, ["the warehouse"] = true, ["the house"] = true, ["the motel"] = true,
    ["the diner"] = true, ["the store"] = true, ["the church"] = true, ["the school"] = true }
local KIPLER = { camp = true, house = true, outpost = true, post = true, stall = true, place = true }
local SEZON = { spring = true, summer = true, autumn = true, fall = true, winter = true,
    ["and this heat.. it's killing us"] = true, ["and it's getting cold already"] = true,
    ["and this cold, God, the cold"] = true, ["at least it's warming up"] = true, ["every day's the same now"] = true }

-- Talk5Home.areaOf'un ürettiği yer biçimleri ("out past here" ayrıca denetlenir)
local function yerBicimi(v)
    return string.match(v, "^in the middle of .+$") ~= nil or string.match(v, "^in the %a+ side of .+$") ~= nil
        or string.match(v, "^in the %a+ end of .+$") ~= nil or string.match(v, "^on the edge of .+$") ~= nil
        or string.match(v, "^out past .+$") ~= nil
end

local function kasabaMi(v)
    local bolge = ProjectALife.TownRegions
    if string.lower(v) == "this county" then return true end
    if type(bolge) ~= "table" or type(bolge.definitions) ~= "table" then return true end
    for _, t in pairs(bolge.definitions) do
        if type(t) == "table" and type(t.label) == "string" and string.lower(t.label) == string.lower(v) then return true end
    end
    return false
end

local function gecerli(ad, v)
    ad = string.lower(ad)
    local v0 = v
    v = string.lower(string.sub(v, 1, 1)) .. string.sub(v, 2)  -- cümle başındaki değerin ilk harfi büyümüş olabilir
    local konusma = ProjectALife.Speech or {}
    if ad == "time" then
        local k = string.lower(v)
        return string.match(v, "^%d+ [AP]M$") ~= nil or k == "midnight" or k == "noon"
    elseif ad == "weekday" then
        return listede(konusma.weekdays, v)
    elseif ad == "date" then
        local ay = string.match(v, "^(%a+) %d+%a%a$")
        return ay ~= nil and listede(konusma.months, ay)
    elseif ad == "day" then
        return string.match(v, "^%d+$") ~= nil
    elseif ad == "at" or ad == "badat" or ad == "goodat" or ad == "contactat" or ad == "placeat" then
        return v == "out past here" or yerBicimi(v)
    elseif ad == "bad" or ad == "good" then
        return EKIP[string.lower(v)] == true
    elseif ad == "place" then
        return DEGER_YERADI[v] == true
    elseif ad == "kind" then
        return KIPLER[v] == true
    elseif ad == "home" or ad == "outpost" then
        return string.match(v, "^a camp in .+$") ~= nil or string.match(v, "^a house in .+$") ~= nil
    elseif ad == "span" then
        return v == "since this morning" or v == "a day" or string.match(v, "^%d+ [dwm]%a+s$") ~= nil
    elseif ad == "season" then
        return SEZON[string.lower(v)] == true
    elseif ad == "neartown" then
        return kasabaMi(v)
    elseif ad == "name" then
        return listede(konusma.names, v)
    elseif ad == "street" then
        return listede(konusma.streets, v)
    elseif ad == "town" then
        return kasabaMi(v)
    elseif ad == "destination" then
        return kasabaMi(v) or string.lower(v) == "somewhere quieter"
    elseif ad == "den" then  -- ALifeRumors.describe biçimleri ya da Speech.render varsayılanı
        local k = string.lower(v)
        if k == "a place i won't go back to" then return true end
        local kasaba = string.match(v, "^.- on the %a+ side of (.+)$") or string.match(v, "^.- in the middle of (.+)$")
        if kasaba ~= nil then return kasabaMi(kasaba) end
        return string.match(v, "^.- out past the county road$") ~= nil
    end
    return v ~= ""
end

-- "{bad} {badat}", "{good} {goodat}", "{place} {placeat}" yan yana: (.-) (.-) deseni sözcük sınırında bölünce yanlış
-- yerden keser ("some" + "families in …"). İki yakalamayı birleştirip bilinen kümeyle yeniden böler.
local YER_ADLARI = { "the gas station", "the warehouse", "the house", "the motel", "the diner", "the store",
    "the church", "the school" }

local function yenidenBol(ad, birlesik)
    local kume = {}
    if ad == "place" then
        kume = YER_ADLARI
    else
        for k in pairs(EKIP) do kume[#kume + 1] = k end
    end
    local en, enUzun = nil, 0
    local alt = string.lower(birlesik)
    for _, k in ipairs(kume) do
        if #k > enUzun and string.sub(alt, 1, #k + 1) == k .. " " then en, enUzun = k, #k end
    end
    if en == nil then return nil end
    return string.sub(birlesik, 1, enUzun), string.sub(birlesik, enUzun + 2)
end

local function sablonCevir(text, s)
    local liste = kovalar()
    for _, b in ipairs({ kovaAnahtari(s), "" }) do
        local aday = liste[b]
        if aday ~= nil then
            for i = 1, #aday do
                local e = aday[i]
                local yakalanan = { string.match(s, e.d) }
                local uygun = #yakalanan > 0
                for j = 1, #yakalanan - 1 do
                    local a = string.lower(e.a[j])
                    if (a == "bad" or a == "good" or a == "place") and string.lower(e.a[j + 1]) == a .. "at" then
                        local ilk, kalan = yenidenBol(a, yakalanan[j] .. " " .. yakalanan[j + 1])
                        if ilk ~= nil then yakalanan[j], yakalanan[j + 1] = ilk, kalan end
                    end
                end
                for j = 1, #yakalanan do
                    if uygun and not gecerli(e.a[j], yakalanan[j]) then uygun = false end
                end
                if uygun then
                    local tr = bak(text, e.k)
                    if tr ~= nil then
                        local kadin = e.s == "f"
                        tr = string.gsub(tr, "{g:([^{}|]*|[^{}|]*)}", function(bicimler)
                            local ayrac = string.find(bicimler, "|", 1, true)
                            if kadin then return string.sub(bicimler, ayrac + 1) end
                            return string.sub(bicimler, 1, ayrac - 1)
                        end)
                        local degerler = {}
                        for j = 1, #e.a do
                            local dg = deger(text, e.a[j], yakalanan[j])
                            degerler[e.a[j]] = dg
                            degerler[string.lower(e.a[j])] = dg  -- EN'de {At}, Türkçede {at}
                        end
                        tr = string.gsub(tr, "{(%a+)}", function(k) return degerler[k] or degerler[string.lower(k)] or ("{" .. k .. "}") end)
                        return tr
                    end
                end
            end
        end
    end
    return nil
end

local function cevir(s)
    local text = ProjectALife and ProjectALife.Text
    if text == nil or type(text.lookup) ~= "function" or type(text.lineKey) ~= "function" then return s end
    local t = text.lookup(text.lineKey(s))
    if type(t) == "string" and t ~= "" then return t end
    local l152 = ALifeTurkce_L152
    if l152 ~= nil then
        if type(l152.doorSpeech) == "function" then
            t = l152.doorSpeech(s)
            if t ~= nil then return t end
        end
        t = l152.missionSpeech(s)
        if t ~= nil then return t end
    end
    if type(text.hash) == "function" and #SABLONLAR > 0 then
        t = sablonCevir(text, s)
        if t ~= nil then return t end
    end
    return s
end

cevirIleri = cevir

local function kapat(hata)
    if Ek.kapali then return end
    Ek.kapali = true
    print("[ProjectALife TR] Konusma cevirisi kapatildi: " .. tostring(hata))
end

local function fontluYaz(shell, text, color)
    if UIFont == nil or UIFont.Small == nil then error("UIFont.Small bulunamadi") end
    return shell:addLineChatElement(text, color[1], color[2], color[3], UIFont.Small, 30, "default")
end

local function basUstuSar(asil)
    return function(shell, text, color, ...)
        if not Ek.kapali and not Ek.basUstuKapali and turkce() then
            local ok, sonuc = pcall(fontluYaz, shell, text, color)
            if ok then return sonuc end
            Ek.basUstuKapali = true
            print("[ProjectALife TR] Bas ustu fontu degistirilemedi; varsayilan font kullaniliyor: " .. tostring(sonuc))
        end
        return asil(shell, text, color, ...)
    end
end

local function kurBasUstu()
    local konusma = ProjectALife and ProjectALife.Speech
    if type(konusma) ~= "table" or type(konusma.engineLine) ~= "function" then return false end
    if konusma.ALifeTurkceBasUstu then return true end
    konusma.ALifeTurkceBasUstu = true
    konusma.engineLine = basUstuSar(konusma.engineLine)
    return true
end

-- Kapı/ziyaretçi eylem satırları (DoLines, "*{v:He} glances at your hands*", K46): caption'dan geçmeden
-- konuşma penceresine yazılır. pick ilk değer olarak, lines liste olarak cinsiyetle çözülmüş metni döndürür;
-- ikisi de aynı anahtarla (çözülmüş metnin hash'i) çevrilir. Diğer dönüş değerleri olduğu gibi geçer.
local function guvenliCevir(s)
    if Ek.kapali or type(s) ~= "string" or s == "" or not turkce() then return s end
    local ok, t = pcall(cevir, s)
    if not ok then kapat(t) return s end
    return t
end

local function ilkiniCevir(ilk, ...)
    return guvenliCevir(ilk), ...
end

local function listeyiCevir(liste, ...)
    if type(liste) ~= "table" then return liste, ... end
    local kopya = {}
    for i, v in ipairs(liste) do kopya[i] = guvenliCevir(v) end
    return kopya, ...
end

local function kurDoLines()
    local satirlar = ProjectALife and ProjectALife.VisitorDoLines
    if type(satirlar) ~= "table" then return false end
    if satirlar.ALifeTurkceKurulu then return true end
    satirlar.ALifeTurkceKurulu = true
    if type(satirlar.pick) == "function" then
        local asil = satirlar.pick
        satirlar.pick = function(...) return ilkiniCevir(asil(...)) end
    end
    if type(satirlar.lines) == "function" then
        local asil = satirlar.lines
        satirlar.lines = function(...) return listeyiCevir(asil(...)) end
    end
    return true
end

-- Speech.sayLine (panik, kapı baskını, karakol, namlu uyarıları, K46) caption'dan geçmeden balona ya da Say'e
-- yazar; metin burada aynı anahtarla çevrilir. Say yolunda font verilemez (K31), balon kapalıysa harfler sadeleşebilir.
local function kurSayLine()
    local konusma = ProjectALife and ProjectALife.Speech
    if type(konusma) ~= "table" or type(konusma.sayLine) ~= "function" then return false end
    if konusma.ALifeTurkceSayLine then return true end
    konusma.ALifeTurkceSayLine = true
    local asil = konusma.sayLine
    konusma.sayLine = function(shell, text, ...)
        return asil(shell, guvenliCevir(text), ...)
    end
    return true
end

-- Başın üstündeki bildirimler (grup: "You left the group.", sığınak, K46): SafehouseClient.notice metni
-- HaloTextHelper'a çeviri yolundan geçirmeden verir. Metin Text.ui anahtarıyla (IGUI_ALifeUI_ + hash) çevrilip
-- yükün içine yazılır; böylece notice'i sonradan saran telsiz paneli de Türkçesini görür.
local function bildirimCevir(yuk)
    if Ek.kapali or type(yuk) ~= "table" or type(yuk.text) ~= "string" or yuk.text == "" or not turkce() then return end
    local ok, t = pcall(function()
        local text = ProjectALife.Text
        return text.lookup(text.key("IGUI_ALifeUI_", yuk.text))
    end)
    if not ok then kapat(t) return end
    if type(t) == "string" and t ~= "" then yuk.text = t end
end

local function kurBildirim()
    local istemci = ProjectALife and ProjectALife.SafehouseClient
    if type(istemci) ~= "table" or type(istemci.notice) ~= "function" then return false end
    if istemci.ALifeTurkceKurulu then return true end
    istemci.ALifeTurkceKurulu = true
    local asil = istemci.notice
    istemci.notice = function(yuk, ...)
        bildirimCevir(yuk)
        return asil(yuk, ...)
    end
    return true
end

-- Uzaktan duyulan uyarılar (Careful.heardWords, K46): Careful.relay metni setHaloNote'a çeviri yolu olmadan verir.
-- Modül server klasöründe olduğu için istemci açılışında yoktur, oyun başlarken bağlanır; sunucu tarafında çağrılmaz.
local function kurDuyulan()
    local dikkat = ProjectALife and ProjectALife.ModuleCareful
    if type(dikkat) ~= "table" or type(dikkat.relay) ~= "function" or dikkat.ALifeTurkceKurulu then return end
    dikkat.ALifeTurkceKurulu = true
    local asil = dikkat.relay
    dikkat.relay = function(shell, player, text, ...)
        local yuk = { text = text }
        bildirimCevir(yuk)
        return asil(shell, player, yuk.text, ...)
    end
end

-- Ziyaretçi paneli (K46): soru düğmeleri, olay sorusu/seçenekleri ve kişi tarifi sunucudan İngilizce gelir ve
-- Panel.clean'den geçip çeviri yolu olmadan çizilir; "bildiklerin" notları Panel.notes'tan.
-- Metin konuşma anahtarıyla (RD_ALifeLine_ + hash) çevrilir. Türkçe, modun bayt sınırını aşarsa İngilizce kalır
-- (string.sub çok baytlı harfi ortadan bölmesin).
-- Sekme adları (cleanTabs, sınır 24) burada çevrilmez: Menu.groupLabel onları Text.ui'den geçirir. Burada çevrilse
-- "Talk", "Now", "Closer" aynı yazılı konuşma satırının çevirisini alırdı ("Konuş bakalım", "Şimdi.", "Daha yakınız.").
local SEKME_SINIRI = 24

local function kurZiyaretci()
    local panel = ProjectALife and ProjectALife.VisitorPanel
    if type(panel) ~= "table" then return false end
    if panel.ALifeTurkceKurulu then return true end
    panel.ALifeTurkceKurulu = true
    if type(panel.clean) == "function" then
        local asil = panel.clean
        panel.clean = function(text, limit, ...)
            if limit == SEKME_SINIRI then return asil(text, limit, ...) end
            local t = guvenliCevir(text)
            if t ~= text and type(limit) == "number" and #t > limit then t = text end
            return asil(t, limit, ...)
        end
    end
    if type(panel.notes) == "function" then
        local asil = panel.notes
        panel.notes = function(...) return listeyiCevir(asil(...)) end
    end
    return true
end

-- A-Life 1.5.2 ağaç verisi: düğme kalıpları ağaç kimliğine bağlıdır. NPC altyazılarında ağaç kimliği
-- gelmez, bu yüzden yalnız doğrulanan cümle kalıpları ve motorun birleştirdiği satır dizileri eşleştirilir.
local AGAC_DUGMELER = {
    crime_d14_whose_town = { "Who runs {town}" },
    law_census_d0 = { "Put me down. {playerName}" },
    law_courthouse_ledger_d14 = { "Me. {playerName}" },
    law_groups_d14 = { "What do you know about {faction}?" },
    law_name_any = { "Nice to meet you, {name}", "I'm {playerName}" },
    law_season_d30 = { "How are you getting ready for {season}?" },
    military_any_checkpoint_hands = { "Day {day}. Okay? Day {day}", "Day {day}. I think", "A house near {town}. Alone, with the door nailed" },
    military_any_info_dead_convoy = { "I found dead soldiers in a truck near {nearTown}" },
    military_d0_info_panic_town = { "People in {town} are losing it" },
    military_d0_trade_tip = { "Where the dead are thickest around {town}" },
    military_d14_info_raid_farm = { "Raiders hit a farm near {town}" },
    military_d30_info_horde = { "There's a horde moving through {nearTown}" },
    military_d30_raid_heard = { "The one on the settlement near {town}" },
    military_d60_raid_report = { "Raiders are gathering near {town}" },
    military_d60_real_name = { "Nice to meet you, {name}" },
    military_d7_info_heli_down = { "Near {nearTown}. Big smoke" },
    military_d7_info_survivors = { "There are survivors holed up in {town}" },
    military_d7_order_share = { "People in {town} are starving. Share your food" },
    rescue_order_come_with = { "There's people near {town} who need a medic. Come help" },
    rescue_season_talk = { "How's the {season} treating everyone?" },
    social_any_headed = { "Watch out near {town}" },
    social_vis_house_before = { "I was a {profession}" },
    social_vis_kos_test = { "I was a {profession}" },
    surv_d30_season = { "How are you getting ready for {season}?" },
    surv_d60_date = { "It's around day {day}" },
    surv_d7_news = { "Anything new around {town}?" },
    surv_joke_name = { "Nice to meet you, {name}", "I'm {playerName}" },
}

local AGAC_SOZLERI = {
    { "Maybe. You any good at sneaking? There's a house up the street. Old guy had a gun cabinet. Dead things in the yard now", { "Maybe. You any good at sneaking?", "There's a house up the street. Old guy had a gun cabinet. Dead things in the yard now" } }, -- crime_d0_quick_job_window:start
    { "Hell yeah! Big houses up on the hill, man, wine cellars, generators. Rich folks stocked up. Bunkers, guns, all that prepper shit", { "Hell yeah! Big houses up on the hill, man, wine cellars, generators", "Rich folks stocked up. Bunkers, guns, all that prepper shit" } }, -- crime_d0_rob_the_rich:start
    { "I AM tough. ..is it that obvious?", { "I AM tough", "..is it that obvious?" } }, -- crime_d0_scared_tough:start
    { "Dead keep piling up by our wall. Somebody's gotta thin the herd. My boys are tired. You go kill some dead by the marked spot, I'll pay", { "Dead keep piling up by our wall. Somebody's gotta thin the herd", "My boys are tired. You go kill some dead by the marked spot, I'll pay" } }, -- crime_d14_kill_zeds_turf:start
    { "Why, you planning a visit? We got a place. Walls, beds, a guy who cooks okay", { "Why, you planning a visit?", "We got a place. Walls, beds, a guy who cooks okay" } }, -- crime_d14_outpost_invite:start
    { "Look at the jacket, genius. Bones on the back. We're what came after the crews. Bigger teeth", { "Look at the jacket, genius. Bones on the back", "We're what came after the crews. Bigger teeth" } }, -- crime_d30_bone_raiders_meet:start
    { "They do. Boss says you got a head on your shoulders. Wants you closer. You've done right by us. There's a place for you, if you want it", { "They do. Boss says you got a head on your shoulders. Wants you closer", "You've done right by us. There's a place for you, if you want it" } }, -- crime_d30_promote_offer:start
    { "Why? You looking to sell or you looking to rob? Ha. That's the question everybody's asking and nobody's answering", { "Why? You looking to sell or you looking to rob?", "Ha. That's the question everybody's asking and nobody's answering" } }, -- crime_d7_ammo_count:start
    { "Prospects run errands. Want to be a prospect for a day? Club needs gas. Club always needs gas. Bring some and we'll remember you", { "Prospects run errands. Want to be a prospect for a day?", "Club needs gas. Club always needs gas. Bring some and we'll remember you" } }, -- crime_d7_biker_prospect_job:start
    { "Not anymore. Three crews merged last night. Big party. Somebody got stabbed. We're getting bigger every day. Small crews join or get eaten", { "Not anymore. Three crews merged last night. Big party. Somebody got stabbed", "We're getting bigger every day. Small crews join or get eaten" } }, -- crime_d7_crews_merging:start
    { "You I believe. Two cans, and you do pay me back, {playerName}" }, -- law_ask_food_d0:two
    { "{playerName}. Got it. If somebody comes asking, I'll know you were alive today" }, -- law_census_d0:named
    { "{playerName}. I'll remember. I'm good with names, it was the job" }, -- law_name_any:me
    { "*Smiles* yeah. Nice to meet you too, {playerName}" }, -- military_d60_real_name:nice
    { "Set's dying. If command calls and we're dead air, that's it. We're forgotten. I need batteries. If the set dies we can't even hear the static", { "Set's dying. If command calls and we're dead air, that's it. We're forgotten", "I need batteries. If the set dies we can't even hear the static" } }, -- military_d7_task_batteries:start
    { "Then lower the {weapon}. Talking doesn't need a {weapon}" }, -- rescue_anti_kos_lower:start
    { "Real help.. *laughs* I AM the real help. That's the joke. Dispatch keeps saying hold position. Hold it where? The position's on fire", { "Real help.. *laughs* I AM the real help. That's the joke", "Dispatch keeps saying hold position. Hold it where? The position's on fire" } }, -- rescue_ems_dispatch_d0:start
    { "Inmates, guards, whoever. Behind that door they're all just patients. There's a locked wing and two of us and a doctor who hasn't left the building since Tuesday", { "Inmates, guards, whoever. Behind that door they're all just patients", "There's a locked wing and two of us and a doctor who hasn't left the building since Tuesday" } }, -- rescue_med_infirmary_d0:start
    { "Here. Bandages, wipes, painkillers, the good drawer like I promised. Thank you, {playerName}" }, -- rescue_q_abx_turnin:base
    { "Cots, water purification tabs, blankets and a satellite phone nobody answers. Three trucks. One's broken, one's for the cots, one's mostly paperwork. Sorry. That's honest", { "Cots, water purification tabs, blankets and a satellite phone nobody answers", "Three trucks. One's broken, one's for the cots, one's mostly paperwork. Sorry. That's honest" } }, -- rescue_relief_redcross_tent_d0:start
    { "Safe? Nowhere's safe. Safer, maybe. *Thinks* There's people. Decent ones, last I heard. That's as close to safe as it gets", { "Safe? Nowhere's safe. Safer, maybe", "*Thinks* There's people. Decent ones, last I heard. That's as close to safe as it gets" } }, -- rescue_safe_places:start
    { "{faction}, yeah, why" }, -- social_any_group:start
    { "{playerName}.. nice to meet you, I guess, weird times to meet people" }, -- social_any_name:me
    { "Before? Feels like a different life.. I was a {profession}" }, -- social_any_profession:start
    { "They drove past yesterday, didn't even slow down. Didn't even look at us. I heard helicopters. Nobody came. Nobody's coming, are they?", { "They drove past yesterday, didn't even slow down. Didn't even look at us", "I heard helicopters. Nobody came. Nobody's coming, are they?" } }, -- surv_d0_news:army
    { "I don't KNOW, okay?! The TV just says stay inside and then it's the same loop again. People are biting people, that's what's going on. Biting! In {town}! My neighbour was standing in his yard for an hour. Just standing. Then he went for the mailman", { "I don't KNOW, okay?! The TV just says stay inside and then it's the same loop again", "People are biting people, that's what's going on. Biting! In {town}!", "My neighbour was standing in his yard for an hour. Just standing. Then he went for the mailman" } }, -- surv_d0_news:start
    { "People are forming groups. Good ones, bad ones. You can tell by how they greet you. Power flickered last night. Lights everywhere for one second and then black. I almost cried. Some crew took over the hardware store. They shoot at anyone who gets close", { "People are forming groups. Good ones, bad ones. You can tell by how they greet you", "Power flickered last night. Lights everywhere for one second and then black. I almost cried", "Some crew took over the hardware store. They shoot at anyone who gets close" } }, -- surv_d14_news:start
    { "Groups are setting up proper camps now. Walls, guards, rules. Like little towns. The dead are thinning in the open. They gather in buildings now. Big buildings scare me. Saw a guy trading cigarettes for ammo. Cigarettes are money now. Who'd have thought", { "Groups are setting up proper camps now. Walls, guards, rules. Like little towns", "The dead are thinning in the open. They gather in buildings now. Big buildings scare me", "Saw a guy trading cigarettes for ammo. Cigarettes are money now. Who'd have thought" } }, -- surv_d30_news:start
    { "Found him in a car. Windows cracked. He was so thirsty. Now he won't leave my side. This is Buster. He barks at them and then hides behind me. Brave boy. Bravest coward I know", { "Found him in a car. Windows cracked. He was so thirsty. Now he won't leave my side", "This is Buster. He barks at them and then hides behind me. Brave boy. Bravest coward I know" } }, -- surv_hope_dog:start
    { "The big store. Don't. There's like a hundred in there. I counted from the roof and then stopped. A pack of them moves through every couple days. Like a wave. Hide when you hear them", { "The big store. Don't. There's like a hundred in there. I counted from the roof and then stopped", "A pack of them moves through every couple days. Like a wave. Hide when you hear them" } }, -- surv_info_danger:start
    { "Some are good, some'll smile and take everything you have. The smile is the tell. There's a lot of people with guns and opinions. Avoid the ones who wear matching stuff", { "Some are good, some'll smile and take everything you have. The smile is the tell", "There's a lot of people with guns and opinions. Avoid the ones who wear matching stuff" } }, -- surv_info_groups:start
    { "Routine. Same time, same places. Surprises kill you. Not caring too much. About stuff, I mean. Stuff can be found. People can't", { "Routine. Same time, same places. Surprises kill you", "Not caring too much. About stuff, I mean. Stuff can be found. People can't" } }, -- surv_info_tips_d60:start
    { "{playerName}. Okay. I'll remember that. I don't remember much anymore but I'll remember that" }, -- surv_joke_name:me
    { "Twenty-two years. The dead can't stop us, they're just one more thing to argue about. She's my wife. I'm hers. We're a team. She's the brains, I'm the bait", { "Twenty-two years. The dead can't stop us, they're just one more thing to argue about", "She's my wife. I'm hers. We're a team. She's the brains, I'm the bait" } }, -- surv_married_pair:start
    { "Stopped calling myself that. I amputated a guy's finger with garden shears last week. Busy. Everyone gets hurt. Nobody pays. Just like the old job actually", { "Stopped calling myself that. I amputated a guy's finger with garden shears last week", "Busy. Everyone gets hurt. Nobody pays. Just like the old job actually" } }, -- surv_nurse_d14:start
    { "Cars are full of stuff. People packed to run and never made it. Sad. Useful. Both. Suitcases, coolers, a guitar once. You'd be amazed what people tried to save", { "Cars are full of stuff. People packed to run and never made it. Sad. Useful. Both", "Suitcases, coolers, a guitar once. You'd be amazed what people tried to save" } }, -- surv_pickers:start
    { "Most of us. Neighbours. We grabbed what we could and stuck together. We're just people from {town}. Teachers, a dentist, a guy who sold insurance. Real fighting force", { "Most of us. Neighbours. We grabbed what we could and stuck together", "We're just people from {town}. Teachers, a dentist, a guy who sold insurance. Real fighting force" } }, -- surv_riverside_d0:start
    { "Holding together. Barely. Votes on everything. We argued an hour about who washes the pots. We lost two on a supply run. We don't talk about it. We just set the table for less", { "Holding together. Barely. Votes on everything. We argued an hour about who washes the pots", "We lost two on a supply run. We don't talk about it. We just set the table for less" } }, -- surv_riverside_d14:start
}

local function agacDeseni(en)
    local desen, adlar, bas = { "^" }, {}, 1
    for ilk, ad, son in string.gmatch(en, "()({%a+})()") do
        desen[#desen + 1] = kacis(string.sub(en, bas, ilk - 1))
        ad = string.sub(ad, 2, -2)
        adlar[#adlar + 1] = ad
        desen[#desen + 1] = ad == "day" and "(%d+)" or "(.+)"
        bas = son
    end
    desen[#desen + 1] = kacis(string.sub(en, bas)) .. "$"
    return table.concat(desen), adlar
end

local function agacDegerleri(s, desen, adlar)
    local yakalanan = { string.match(s, desen) }
    if #yakalanan == 0 then return nil end
    local degerler = {}
    for i, ad in ipairs(adlar) do
        local v = yakalanan[i]
        if degerler[ad] ~= nil and degerler[ad] ~= v then return nil end
        if (ad == "season" or ad == "town" or ad == "nearTown") and not gecerli(ad, v) then return nil end
        degerler[ad] = v
    end
    return degerler
end

local function agacDoldur(s, degerler)
    return (string.gsub(s, "{(%a+)}", function(ad) return degerler[ad] end))
end

local function agacBuyut(s)
    return (string.gsub(s, "%a", string.upper, 1))
end

local function agacSatiri(text, en, degerler, npc)
    local tr = bak(text, text.lineKey(en))
    if tr == nil and npc then tr = bak(text, text.lineKey(agacBuyut(en))) end
    if tr == nil then return nil end
    local sonuc = string.gsub(tr, "{(%a+)}", function(ad)
        local v = degerler[ad]
        if v == nil or ad == "playerName" or ad == "name" or ad == "weapon" then return v end
        return deger(text, ad, v)
    end)
    if string.find(sonuc, "{%a+}") ~= nil then return nil end
    return sonuc
end

local function agacParcalari(text, parcalar, degerler)
    local sonuc = {}
    for i, en in ipairs(parcalar) do
        local tr = agacSatiri(text, en, degerler, true)
        if tr == nil then
            local soz = agacBuyut(agacDoldur(en, degerler))
            tr = cevir(soz)
            if tr == soz or string.find(tr, "{%a+}") ~= nil then return nil end
        end
        if i < #parcalar and string.find(tr, "[%w]$") ~= nil then tr = tr .. "." end
        sonuc[#sonuc + 1] = tr
    end
    return table.concat(sonuc, " ")
end

local AGAC_NPC_TAM, AGAC_NPC_DESEN = {}, {}
for _, satir in ipairs(AGAC_SOZLERI) do
    local en = satir[1]
    local desen, adlar = agacDeseni(en)
    if #adlar == 0 then
        AGAC_NPC_TAM[en] = satir[2]
    else
        -- Speech.render, başta sabit yazı olduğunda ilk harfi büyütür.
        local sabit = string.match(en, "^[^{]*")
        desen, adlar = agacDeseni(agacBuyut(sabit) .. string.sub(en, #sabit + 1))
        AGAC_NPC_DESEN[#AGAC_NPC_DESEN + 1] = { desen, adlar, satir }
    end
end

local function agacAltyazi(s)
    local text = ProjectALife.Text
    local parcalar = AGAC_NPC_TAM[s]
    if parcalar ~= nil then return agacParcalari(text, parcalar, {}) end
    for _, kalip in ipairs(AGAC_NPC_DESEN) do
        local degerler = agacDegerleri(s, kalip[1], kalip[2])
        if degerler ~= nil then
            local satir = kalip[3]
            if satir[2] ~= nil then return agacParcalari(text, satir[2], degerler) end
            local sonuc = agacSatiri(text, satir[1], degerler, true)
            if sonuc ~= nil then
                if string.find(satir[1], "^{faction}") then
                    sonuc = string.gsub(sonuc, "^%l", string.upper)
                end
                return sonuc
            end
        end
    end
end

-- [Charm] önekini oyun seçilen satırı yankılarken söker. Sözlükte hem önekli hem öneksiz kayıtlar var.
local function dugmeCevir(s, agac)
    if Ek.kapali or type(s) ~= "string" or s == "" or not turkce() then return s end
    local onek, govde = string.match(s, "^(%[Charm%] )(.*)$")
    if govde == nil then onek, govde = "", s end
    local ok, t = pcall(function()
        local text = ProjectALife.Text
        local tr = bak(text, text.lineKey(govde))
        if tr == nil and onek ~= "" then tr = bak(text, text.lineKey(s)) end
        if tr ~= nil then return tr end
        for _, en in ipairs(AGAC_DUGMELER[agac] or {}) do
            local desen, adlar = agacDeseni(en)
            local degerler = agacDegerleri(govde, desen, adlar)
            if degerler ~= nil then
                tr = agacSatiri(text, en, degerler, false)
                if tr ~= nil then return tr end
            end
        end
    end)
    if not ok then kapat(t) return s end
    if type(t) ~= "string" or t == "" then return s end
    if string.find(t, "[^%.]%.$") ~= nil and string.find(govde, "%.$") == nil then t = string.sub(t, 1, #t - 1) end
    return onek .. t
end

local function satirlariCevir(agac, satirlar, ...)
    if type(satirlar) == "table" then
        for _, satir in ipairs(satirlar) do
            if type(satir) == "table" and type(satir.text) == "string" then
                satir.text = dugmeCevir(satir.text, satir.treePrompt or agac)
            end
        end
    end
    return satirlar, ...
end

local function kurAgac()
    local agac = ProjectALife and ProjectALife.UI2TalkTrees
    if type(agac) ~= "table" then return false end
    if agac.ALifeTurkceKurulu then return true end
    agac.ALifeTurkceKurulu = true
    for _, ad in ipairs({ "promptRows", "runRows" }) do
        if type(agac[ad]) == "function" then
            local asil = agac[ad]
            agac[ad] = function(win, ...)
                local run = type(win) == "table" and win.treeRun or nil
                local tree = type(run) == "table" and run.tree or nil
                return satirlariCevir(tree, asil(win, ...))
            end
        end
    end
    return true
end

-- Kaçan metinler (1.5.0, rapor/kacan_ek_1.5.0.md): iki yol çeviri yolundan geçmeden çizilir.
-- Metin arayüz anahtarıyla (IGUI_ALifeUI_ + hash, Text.ui'nin anahtarı; kaynak/IG_UI_kacan.json) çevrilir.
-- Yalnız ekrana dönen kopya değişir: modun tuttuğu veri (win.hoverTip, görev satırı) ve sunucuya giden hiçbir şey değişmez.
local function arayuzCevir(s)
    if Ek.kapali or type(s) ~= "string" or s == "" or not turkce() then return s end
    local ok, t = pcall(function()
        local text = ProjectALife.Text
        return text.lookup(text.key("IGUI_ALifeUI_", s))
    end)
    if not ok then kapat(t) return s end
    if type(t) ~= "string" or t == "" then return s end
    return t
end

-- Konuşma penceresinin alt satırı (UI2Talk.statusText): fare bir konuşma satırının üstündeyken satırın ipucunu
-- (Dell görevi "tip"leri: "Ask what happened to him") ham çizer. Yalnız dönen tablo ipucu gösteriyorsa (text == win.hoverTip)
-- kopyası Türkçeyle döner; "bekleniyor" gibi diğer durum yazıları ve win.hoverTip dokunulmadan kalır.
local function kurIpucu()
    local konusma = ProjectALife and ProjectALife.UI2Talk
    if type(konusma) ~= "table" or type(konusma.statusText) ~= "function" then return false end
    if type(konusma.clickNote) == "function" and not konusma.ALifeTurkceTiklamaBildirimi then
        local tiklamaBildirimi = konusma.clickNote
        konusma.clickNote = function(win, ...)
            local sonuc = tiklamaBildirimi(win, ...)
            local notMetni = type(win) == "table" and type(win.clickNote) == "table" and win.clickNote.text
            if type(sonuc) == "table" and type(notMetni) == "string" and turkce()
                    and sonuc.text == string.upper(notMetni) then
                local kopya = {}
                for k, v in pairs(sonuc) do kopya[k] = v end
                kopya.text = notMetni
                return kopya
            end
            return sonuc
        end
        konusma.ALifeTurkceTiklamaBildirimi = true
    end
    if konusma.ALifeTurkceIpucu then return true end
    konusma.ALifeTurkceIpucu = true
    local asil = konusma.statusText
    konusma.statusText = function(win, ...)
        local sonuc = asil(win, ...)
        if type(sonuc) ~= "table" or type(win) ~= "table" or type(sonuc.text) ~= "string" or sonuc.text ~= win.hoverTip then
            return sonuc
        end
        local t = arayuzCevir(sonuc.text)
        if t == sonuc.text then return sonuc end
        local kopya = {}
        for k, v in pairs(sonuc) do kopya[k] = v end
        kopya.text = t
        return kopya
    end
    return true
end

-- Soru-cevap şeridi (UI2Answer.clean): sunucudan gelen sorunun metni (bitiş pilotunun soruları) ham çizilir; seçenekler
-- zaten Text.ui'den geçer. clean'in döndürdüğü yeni tablonun text'i önce konuşma anahtarıyla (RD_ALifeLine_, NPC sözü),
-- yoksa arayüz anahtarıyla çevrilir. Cevap sunucuya seçenek kimliğiyle gider; text geri gönderilmez.
local function kurSoru()
    local cevap = ProjectALife and ProjectALife.UI2Answer
    if type(cevap) ~= "table" or type(cevap.clean) ~= "function" then return false end
    if cevap.ALifeTurkceKurulu then return true end
    cevap.ALifeTurkceKurulu = true
    local asil = cevap.clean
    cevap.clean = function(...)
        local soru = asil(...)
        if type(soru) == "table" and type(soru.text) == "string" and soru.text ~= "" then
            local t = guvenliCevir(soru.text)
            if t == soru.text then t = arayuzCevir(soru.text) end
            soru.text = t
        end
        return soru
    end
    return true
end

-- Bitiş telsizi ve pilot (1.5.0, rapor/kacan_listeler_1.5.0.md bölüm 4): sunucudan İngilizce gelen iki istemci yolu ham çizer.
-- Telsiz kartı (RadioClient.card, "ad: metin"): kartın metni yayının ilk satırı ya da oyuncunun seçtiği satır.
-- Pilotun sözü (EndingClient.say): sinematik altyazı ya da bildirim. İkisinde de yalnız istemciye gelen tablonun kopyası
-- Türkçe metinle verilir: önce konuşma anahtarı (RD_ALifeLine_), yoksa arayüz anahtarı (IGUI_ALifeUI_; seçenek etiketi).
-- Sunucudaki radyo yayını (Java RadioLine) ve pilot gövdesinin Say'i ağa gider: bilerek sarılmaz.
local function sozCevir(s)
    local t = guvenliCevir(s)
    if t == s then t = arayuzCevir(s) end
    return t
end

local function metniCevrilmis(args)
    if type(args) ~= "table" or type(args.text) ~= "string" or args.text == "" then return args end
    local t = sozCevir(args.text)
    if t == args.text then return args end
    local kopya = {}
    for k, v in pairs(args) do kopya[k] = v end
    kopya.text = t
    return kopya
end

local KART_DISI = { hint = true, mark = true, drop = true, notice = true }  -- bunlar kendi Text.ui yolunda ya da metinsiz

local function kurKart()
    local radyo = ProjectALife and ProjectALife.RadioClient
    if type(radyo) ~= "table" or type(radyo.card) ~= "function" then return false end
    if radyo.ALifeTurkceKart then return true end
    radyo.ALifeTurkceKart = true
    local asil = radyo.card
    radyo.card = function(args, ...)
        if type(args) == "table" and not KART_DISI[args.kind] then return asil(metniCevrilmis(args), ...) end
        return asil(args, ...)
    end
    return true
end

local function kurPilot()
    local bitis = ProjectALife and ProjectALife.EndingClient
    if type(bitis) ~= "table" or type(bitis.say) ~= "function" then return false end
    if bitis.ALifeTurkcePilot then return true end
    bitis.ALifeTurkcePilot = true
    local asil = bitis.say
    bitis.say = function(args, ...) return asil(metniCevrilmis(args), ...) end
    return true
end

local function kur()
    pcall(kurAgac)  -- istemci modülü; sunucuda ve erken yüklemede yoktur, OnGameStart'ta yeniden denenir
    pcall(kurIpucu)
    pcall(kurSoru)
    pcall(kurKart)
    pcall(kurPilot)
    local basUstuHazir = kurBasUstu()
    local ziyaretciHazir = kurZiyaretci()
    local doLinesHazir = kurDoLines()
    local bildirimHazir = kurBildirim()
    local sayLineHazir = kurSayLine()
    local politika = ProjectALife and ProjectALife.AudioPolicy
    if type(politika) ~= "table" or type(politika.caption) ~= "function" then return false end
    if not politika.ALifeTurkceKurulu then
        politika.ALifeTurkceKurulu = true
        local asil = politika.caption
        politika.caption = function(text, ...)
            local s = asil(text, ...)
            if Ek.kapali or type(s) ~= "string" or s == "" or not turkce() then return s end
            local ok, t = pcall(cevir, s)
            if not ok then kapat(t) return s end
            if t ~= s then return t end
            local agacOk, agacTr = pcall(agacAltyazi, s)
            return agacOk and agacTr or s
        end
    end
    return basUstuHazir and doLinesHazir and bildirimHazir and ziyaretciHazir and sayLineHazir
end

-- Ek, modun dosyalarından sonra yüklenir; yine de tablo hazır değilse oyun başlarken bir kez daha dener
if type(Events) == "table" and Events.OnGameStart then
    Events.OnGameStart.Add(function()
        local ok2, hata = pcall(kurDuyulan)
        if not ok2 then kapat(hata) end
        ok2, hata = pcall(kurAgac)
        if not ok2 then kapat(hata) end
        ok2, hata = pcall(kurIpucu)
        if not ok2 then kapat(hata) end
        ok2, hata = pcall(kurSoru)
        if not ok2 then kapat(hata) end
        ok2, hata = pcall(kurKart)
        if not ok2 then kapat(hata) end
        ok2, hata = pcall(kurPilot)
        if not ok2 then kapat(hata) end
    end)
end
local ok, kuruldu = pcall(kur)
if not ok then kapat(kuruldu) end
if (not ok or not kuruldu) and type(Events) == "table" and Events.OnGameBoot then
    Events.OnGameBoot.Add(function()
        local ok2, hata = pcall(kur)
        if not ok2 then kapat(hata) end
    end)
end
