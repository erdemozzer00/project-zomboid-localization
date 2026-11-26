# B paket bölme önerisi (1.5.0 IG_UI kalanı, çeviri yok)

Kaynak: `rapor/arayuz_siniflar_1.5.0.json` (üretici `araclar/arayuz_sinif.py`), anahtar listeleri `rapor/B_paket_plani_1.5.0.json`.
Bu planın dışında kalanlar: Y1/Y1S/Y2/Y4/Y5 (Gemini'de), **Y3** (303 satır diyalog, Gemini), B5/B6 (işlendi), B7 (aşağıdaki ek dahil).

Kalan 1.909 çevirisiz IG_UI metninin dökümü: **303 a (Y3), 1.599 b (Claude), 7 c (görünmez)**. b'nin 43'ü mevcut çeviriden doldurulur (B7 eki), kalan **1.556** B paketlerine gider; üstüne çıkarıcıların yeni bulduğu **161** satır (Creator_lua 160 + IG_UI_lua 1) eklenir.

## B7'ye ek (otomatik, çeviri yok)

B7 şimdiki kapsam: 97 doldurma (29 harf farkı + 68 diyalog metni), Sister/Brother, radyonun 17 kişi adı. **Ek: 43 satır** (b sınıfından, noktalama/büyük-küçük harf farkıyla onaylı bir çevirisi olan metinler; ör. "REPUTATION", "{n} more", "Default", "Diagnostics", "WHO IS IT"). Liste: `rapor/arayuz_b_mevcut_esdeger_1.5.0.json` (anahtar → eski kaynak, eski anahtar). Kısa tek sözcüklü olanlar ("neutral", "wary", "hostile", "outpost") bağlam kontrolüyle doldurulmalı: aynı sözcük farklı yerde farklı çevrilmiş olabilir. Ek olarak `lua_cikar_tasima_oneri_1.5.0.json`'daki 28 taşıma (noktalama farkıyla yeni anahtara giden onaylı çeviri) B7'ye alınabilir.

## Paketler (her biri tek sohbet, en çok ≈400 satır, konuya göre)

| Paket | Satır | Konu | Başlıca dosyalar |
|---|---:|---|---|
| **B8** | 315 | Yönetici, GM, araçlar ve geliştirici kaydedicileri (K52) | GmClient 31, UI2GmStatus 30, MenuPrefs 27, GmMenu 26, MenuBuilder 23, ToolsMenu 21, MarksWindow 20, BugReport(+Window) 31, DiagTools 16, AdminActions, SpawnPlan, ManeuverRecorder |
| **B9** | 287 | Konuşma penceresi ipuçları (etki/risk notları) ve görev panosu başlık/özetleri | TaskBoardData 90 (başlık, özet, etki), FactionTalkData 68 (etki/risk), FollowBData 20, TaskTalk 15, Cars2Talk 12, Talk6, TalkGeneral |
| **B10** | 240 | Yoldaş sayfası ve harita ipuçları | CompanionSheetData 87, SquadMapTooltip 76, CompanionInventory 19, SheetGear 17, SquadMapOverlay 13 |
| **B11** | 274 | Baskın kartı ve dünya olayı bildirimleri (radyo kalanı: 30 satır dahil) | RaidText 181 (kısa uyarı cümleleri, ses tonu önemli), NoveltyBoardData 16, RadioClient 9, CaptivesClient 9, NoveltyNotesData 7 (item adları), OutpostPresets 6 |
| **B12** | 279 | Oluşturucu (Creator) ekranı: **B12a** IG_UI 119 (+ `?` 93: Oluşturucu ayar ipuçları, `.alife` verisi) ve **B12b** Creator_lua 160 (`creator_cikar` yeni) | CreatorDense 11, WardrobeCard 8, ayar ipuçları ("Strength, 1 to 10…"), 25 `faction_registry.alife` etiketi |
| **B13** | 321 | İtibar sekmesi, başlangıç seçimi/günlük/bildirimler, sürüş, bitiş ekranı ve jenerik başlıkları | UI2StartPickData 37, UI2RepTabModel 28, DriveHereClient 26, CreditsData 25 (başlıklar; 124 destekçi adı çevrilmez), EndingStory 24, EndingVerdict 18, EndingPolish 18 |

Toplam B8–B13 = **1.716 satır** (1.556 + 160). B12a ve B12b aynı sohbette, ayrı paket dosyası (`_dosya` farklı). Sıralama önerisi: B8 (K52 kapsamı, çok satır ama kısa/teknik) → B9, B10 (oyuncunun sürekli gördüğü yerler; B9 ve B10 oyuncuya en çok görünen) → B11, B13, B12.

Not: IG_UI_lua'daki tek yeni satır ("I'm a cop, you can talk to me", `ALifeTalkOrderRows`) bir oyuncu seçeneği; ya B9'a ekle ya Y3 ile birlikte Gemini'ye ver (anahtarı `kaynak/IG_UI_lua.json` kaynaklı, `_dosya: IG_UI_lua`).

## Dikkat çeken noktalar

- **B11 / RaidText (181 satır):** "Armed locals are running off", "Soldiers opened fire, find cover" gibi gözcü ağzıyla yazılmış kısa uyarılar; kart başlığı olarak çiziliyor (`raidtext_lines` deneyi açık). Çok kısa ve ton ağırlıklı: Claude yerine Y3-benzeri Gemini turuna da gidebilir (karar).
- **B13 / bitiş anlatısı (EndingStory 24 + Polish 18 + Verdict 18 = 60 satır):** düz anlatı/edebi metin, diyalog değil; B13'ten ayrılıp Gemini'ye verilebilir (karar).
- Etki/risk ipuçları (B9: TaskBoardData 30 + FactionTalkData 67 + diğerleri) çok kısa ("Needs a bond with them"); K36 gibi birebir olmayan, ama sığma sınırı var (düğme altı notu): Y5 ek cümlesindeki "kısa tut, nokta yok" kuralı burada da geçerli.
- Her paketten önce `paket_kontrol` ve ek (`ALifeTR_Konusma.lua`) kapsamına bakılır; tüm b metinleri `Text.ui` yolunda (JSON anahtarı), konuşma eki gerekmez.

## Kaçan metinlerin arayüz grubu (2026-11-09, öneri: B14 ya da B13'e ek, 87 satır)

Kaynak: `kaynak/IG_UI_kacan.json` (üretici `araclar/kacan_cikar.py`; `kaynak/IG_UI_kacan_baglam.json` tür `arayuz`). Gerekçe ve kod yolları: `rapor/kacan_ek_1.5.0.md`.
Hepsi oyunda `Text.ui` yolundan çizilir (anahtar `IGUI_ALifeUI_` + hash), konuşma eki gerekmez; yalnız JSON'da yoktu.

| Grup | Satır | Nerede |
|---|---:|---|
| ayar | 68 | Günlük > Ayarlar: konuşma penceresi, altyazı, görev izleyici, ok, jenerik hızı, yayıncı modu satırları; ad, değer adı (On/Off dışı: "Old cinematic", "Bottom right"…) ve fareyle çıkan ipucu |
| ayar_grubu | 4 | Aynı ekranın grup başlıkları ("Text and motion", "Subtitles", "Tasks and popups", "Intro") |
| gorev_asamasi | 7 | Dell'in çanta görevi (Left Behind) günlükte aşama ve alt açıklaması ("Find Earl's bag", "Kill the dead inside"); `{place}`'li aşamalar sunucuda doldurulduğu için alınmadı |
| gorev_cipi | 5 | Aynı görevin konuşma satırlarındaki küçük etiket ("Reward", "Comply", "Fight") |
| arkadas_carki | 3 | Grup emir çarkının alt menüleri ("Tactics", "Items", "Rooms") |

Paket `_dosya: IG_UI_lua` olmalı: paket hazırlanırken anahtarlar (`kaynak/IG_UI_kacan.json`'dan) `kaynak/IG_UI_lua.json`'a eklenir, yoksa `onayla` anahtarı bulamaz (`al Y6` aynısını diyalog grubu için kendisi yapar). Kısa tek sözcüklerde ("Right", "Left", "Auto", "Strong") aynı İngilizce başka bir `Text.ui` yerinde de aynı anahtarı paylaşır; çeviri iki yere de uymalı.

## Y adları: B10–B14 Gemini'de (2026-11-09, K53, kullanıcı kararı; sebep Claude limiti)

B10–B14 Claude yerine Gemini'de çevrilir; her plan paketi kendi Y adını alır. RaidText gözcü cümleleri ve bitiş anlatısı diyalog sayılıp Y8'e ayrıldı. O tarihteki girdi yolu `gemini/yeni/girdi/`, harita `paketler/haritalar/<Y>_harita.json`, istem PROMPTLAR 10. (Y8 için 9. + Y8 ek cümlesi).

| Y | Plan | Konu | Satır | Dosya | `_dosya` | Komut |
|---|---|---|---:|---:|---|---|
| **Y8** | B11 + B12 + B13'ten | RaidText gözcü cümleleri ve kart etiketleri (181) + bitiş anlatısı (60) + veri kaynaklı 2 bitiş cümlesi | 243 | 2 | IG_UI | `hazirla-baskin Y8 --yeni` |
| **Y10** | B10 | Yoldaş sayfası ve harita ipuçları | 240 | 2 | IG_UI | `hazirla-arayuz Y10 --plan B10 --yeni` |
| **Y11** | B11 | İlan panosu, radyo ve dünya olayı bildirimleri (RaidText hariç) | 76 | 1 | IG_UI | `hazirla-arayuz Y11 --plan B11 --yeni` |
| **Y12** | B12a | Oluşturucu ekranı (IG_UI) ve ayar ipuçları | 117 | 1 | IG_UI | `hazirla-arayuz Y12 --plan B12a --yeni` |
| **Y13** | B12b | Oluşturucu sabit yazıları | 156 | 2 | Creator_lua | `hazirla-arayuz Y13 --plan B12b --yeni` |
| **Y14** | B13 | İtibar, başlangıç, günlük, sürüş, bitiş ekranı, jenerik (bitiş anlatısı hariç) | 261 | 2 | IG_UI | `hazirla-arayuz Y14 --plan B13 --yeni` |
| **Y15** | B14 | Kaçan metinlerin arayüz grubu (`rapor/kacan_ek_1.5.0.md`, 87) | 87 | 1 | IG_UI_lua | `hazirla-arayuz Y15 --plan B14 --yeni` |

Plan sayılarından farklar: B11 274 → 76 (RaidText 181 Y8'e; 17 radyo kişi adı B7'de onaylı); B12a 119 → 117 (bitiş anlatısı 2 satır Y8'e); B12b 160 → 156 (4 anahtar B7c ile `Creator_lua`'da); B13 321 → 261 (EndingStory/Polish/Verdict 60 satır Y8'e).

Not: B9'dan ayrılan 8 diyalog satırı için ILERLEME'de "Y10" adı geçiyordu; Y10 artık B10. Bu 8 satır ve IG_UI_lua'daki "I'm a cop, you can talk to me" için ayrı bir ad gerekir (öneri: Y16).
