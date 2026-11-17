# Kaçan metinler için çeviri eki: fizibilite ve sonuç (1.5.0, 2026-11-09)

Girdi: `rapor/kacan_1.5.0.md` / `.json` (`araclar/kacan_tara.py`), görünür 791 aday: 321 diyalog, 408 yönetici arayüzü, 62 oyuncu arayüzü.
Mod Lua kaynağı satır satır okundu. Hiçbir metin çevrilmedi; `onayli/`, `paketler/`, `kaynak/en/` değişmedi; `workshop_kur` çalıştırılmadı.

## Özet

| | Satır | Ne yapıldı |
|---|---:|---|
| **Alındı, ek gerekmez** | 287 | Metin oyunda zaten `Text.ui` (`IGUI_ALifeUI_` + hash) yolundan çiziliyor; tarayıcı yalnız `Text.ui("…")` gibi doğrudan çağrıları gördüğü için "kaçan" saydı. Eksik olan yalnız JSON satırı. |
| **Alındı, dar ek yazıldı** | 16 + 3 | Görev satırı ipucu (`UI2Talk.statusText`) ve bitiş pilotunun sorusu (`UI2Answer.clean`): ikisi gerçekten ham çiziliyordu. |
| **Bırakıldı** | 535 aday | 408 yönetici arayüzü, 26 yer tutuculu ağaç satırı, 22 görünmeyen esir sorusu, parti/ağaç görevleri, şablonlu görev ve bitiş metinleri, yer adları vb. (aşağıda). |

Kaynak: `kaynak/IG_UI_kacan.json` (**306 metin**: 219 diyalog → Y6, 87 arayüz → B paketi önerisi). 791 adaydan **256'sı** bu 306'nın içinde. Kalan 50 metni tarayıcı hiç görmemişti (değer adları `names`, aşama açıklaması `detail` gibi alanları taramıyordu).

## 1. Fizibilite: gruplar

"Güvenli" ölçütü dört koşul: yalnız gösterim anında çalışacak, mantıkta kullanılmayacak, `pcall` korumalı olacak, çeviri yoksa İngilizceye düşecek ve kayıt dosyasına ya da ağa Türkçe yazmayacak. Emin olunamayan grup bırakıldı.

| Grup (dosya, alan) | Ekrana çıktığı fonksiyon | İstemci/sunucu | Dar nokta | Birleştirme/biçim | Davranış riski | Karar |
|---|---|---|---|---|---|---|
| Durum satırları (`SituationsData` rows `text/impact/risk`), durum soruları (`TalkSituation` `text/impact`), esir satırları (`CaptivesData` `D.rows`) | Düğme: `Talk2.text(Intents.choiceLabel(choice))`. Klasik pencerede `TalkMenu`/`TalkCinema` aynı `Text.ui` çağrısını yapar. Alt not: `Pool.lines → Talk2.text(meta.impact/risk)` (`FT.byId` üzerinden) | Kayıt ortak (shared, `TalkRowHook.register`/`FactionTalkData.rows`), çizim istemcide | Gerek yok, zaten `Text.ui` | Yok, metin olduğu gibi | Yok: veri değişmiyor, yalnız JSON satırı ekleniyor. Mod kendi EN dosyasında aynı yoldaki `FactionTalkData` satırlarını aynı anahtarla tutuyor (ör. `IGUI_ALifeUI_6fa1c3481a3e32b3`) | **Alındı (ek yok)** |
| Görev satırları (`MissionDefs` `Defs.rows` `text`, çip `label`) | Düğme aynı yol, çip `Talk2.text(chip.label)` | İstemci | Gerek yok | Yok | Yok | **Alındı (ek yok)** |
| Görev satırı ipucu (`MissionDefs` `tip`, 16) | `button.tip → win.hoverTip → Talk2.statusText → Kit.text`, **ham** | İstemci | Var: `UI2Talk.statusText` tabloda, çağrı `Talk2.statusText(win, now)` ile çalışma anında tablodan | Yok | Dönen tablo her çağrıda yeni ve yalnız çizimde kullanılıyor. Ek kopyasını döndürüyor; `win.hoverTip`'e dokunmuyor | **Alındı (ek)** |
| Bitiş telsiz çağrısı seçenekleri (`EndingCallData` opts `label`), helikopter cevapları (`EndingData.talk.beats` options `label`) | Sunucu `d.offer(..., rows)` → istemci `UI2Answer.rowsFor → Text.ui(option.label)` | Sunucu doldurur (`Call.fill(label, {name})`), istemci çizer | Gerek yok | `{name}`'li 4 seçenek sunucuda dolduğu için anahtar tutmaz | Yok: seçim kimlikle (`id`) geri gidiyor | **Alındı (ek yok)**; `{name}`'li 4 seçenek bırakıldı |
| Helikopter pilotunun sorusu (`beats` `ask`, 3); aynı yoldan geçen bütün soru-cevap şeridi soruları | `UI2Answer.clean(args)` → `ask.text` → `A.questionLines → Kit.wrap`, **ham**; gömülü yolda `win:append(ask.text)` | Sunucudan gelir, istemcide çizilir | Var: `UI2Answer.clean` tabloda, `A.receive` onu tablodan çağırır | Telsiz çağrısında sorular `table.concat(lines, ", ")` ile birleşir; tam metin eşleşmez, İngilizce kalır | `clean`'in döndürdüğü tablo istemcide yerel; sunucuya yalnız soru ve seçenek kimliği gider (`A.sendChoice`: `id`, `uid`, `option`) | **Alındı (ek)** |
| Görev aşamaları (`Defs.missions` stages `text/detail`) | `M.text(stage.text/detail)` (`UI2Missions`, `UI2JournalUi`) | Sunucu `fill` ile doldurur, istemci `Text.ui` | Gerek yok | `{place}`'li 2 aşama ve özet sunucuda dolar, anahtar tutmaz | Mod istemcide `current.text == "Get out alive"` karşılaştırması yapıyor: veriyi değiştiren bir ek bunu bozardı. Bu yüzden veriye dokunulmadı, yalnız JSON | **Alındı (ek yok)**, yer tutuculular bırakıldı. Görev izleyicide `info.detail` ham çizilir, orada İngilizce kalır |
| Oyuncu ayarları (`UI2Prefs` rows ve `addRow` ile eklenenler: Tracker, TaskArrow, CreditsRoll, StreamerBubble), grup başlıkları (`JournalSettings` `S.groups`), arkadaş çarkı (`CompanionClient.WHEEL` `label`) | `M.text(row.label/names[...]/tip)`, `Client.text(slot.label)`, `Client.submenu → Client.text(title)` | İstemci | Gerek yok | Yok | Yok | **Alındı (ek yok)** |
| Yönetici/geliştirici/Oluşturucu arayüzü (408) | 45 dosyada doğrudan `drawText`, `ISButton`, `addOption`, `UI.fit(row.label)`, `"Staffed outpost: " .. label` gibi birleştirmeler. Yönetici dosyalarının neredeyse hiçbiri `Text.ui` çağırmıyor | İstemci; bir kısmı sunucu eylem kaydı (`AdminActions.register`, `"Spawn situation: " .. def.label`) | **Yok.** Tek ortak çizim noktası yok; `drawText`/`ISButton` gibi genel sınıfları sarmak K24'te kaçınılan global yama olur | Çok sayıda birleştirme | Eylem etiketi arama/eşleşmede de kullanılıyor (`Actions.match`, `haystack`) | **Bırakıldı** |
| Parti görevleri (`ALifeParty` `text/label`, 6) | Sunucuda `"Bring the group " .. count .. " " .. noun` ile kurulup görev durumuna (kayıt) yazılıyor | Sunucu | Yok | Birleştirme | Görev durumu kaydediliyor | **Bırakıldı** |
| Ağaç görevi başlıkları (`ALifeTreeTasks` `title`, 7) | Başlık görev kaydına kopyalanıyor, `title .. " (" .. count .. ")"` ile birleşiyor | Ortak/sunucu | Yok | Birleştirme | Kayıtta | **Bırakıldı** |
| Yer tutuculu ağaç satırları (`ALifeTrees_*`, 26: `Who runs {town}`, `I'm {playerName}`) | Sunucu doldurur, düğmede `dugmeCevir` tam metinle arar; şablon eşlemesi yalnız NPC sözünde (`caption`) var | Sunucu → istemci | Var (`dugmeCevir`), ama şablon eşlemesini düğmelere açmak ayrı ve daha riskli bir iş | Yer tutucu | Bu turda değil | **Bırakıldı (sonraki iş adayı)** |
| Esir ağacı soruları (`CaptiveTreesData` `ask`, 22) | Hiçbir yerde çizilmiyor: `DialogueTrees.register` yalnız uzunluğunu denetliyor. Oyunda görünen soru `CaptiveTrees.asks` (zaten kapsamda) | — | — | — | — | **Bırakıldı (görünmez)** |
| Durum adları ve yönetici eylemleri (`SituationsData` `label/tip`, 12) | Yönetici eylem listesi (`AdminActions`), birleştirmeli | — | Yok | Var | — | **Bırakıldı** (yönetici) |
| Animasyon adları (`ALifeAnimations` `label`, 10) | Yalnız yönetici oluşturucu listeleri (`DebugSpawner`, `SpawnerPanel`, `SpawnerBrowser`) | İstemci | Yok | — | — | **Bırakıldı** (yönetici) |
| Sığınak mektubu başlıkları (`SafehouseEvents` `title`, 10) | Tüketicisi bu turda doğrulanamadı; çoğu `{faction}`'lı | — | ? | Yer tutucu | ? | **Bırakıldı (emin değil)** |
| Bitiş yer adları ve görev başlığı (`EndingData` `label/title/subtitle/summary`, 12) | Yer adı `{place}`'e girer (sunucu doldurur), başlık ve özetin istemci yolu doğrulanmadı | — | ? | Yer tutucu | ? | **Bırakıldı** |
| Çağrı konuşmacı adları ve iç not (`EndingCallData` `name/note`, 3) | "US Military", "Captain Ruiz": konuşmacı adı. Not, geliştirici notu | — | — | — | — | **Bırakıldı** (ad / iç) |
| Bölük haritası (`SquadMap` `Say`/caption, `SquadMapOverlay` sağ tık menüsü, 11) | `SquadMap.toggle`'ı çağıran yer yok; harita geliştirici aracı. Menüde `"Delete this squad (" .. n .. ")"` birleştirmesi var | İstemci | `Overlay.menuEntries` dar, ama erişim yolu bulunamadı | Kısmen | — | **Bırakıldı** (erişilemiyor) |
| "Marla" (`JournalSettings`, 1) | Örnek kutusundaki kişi adı | — | — | — | — | **Bırakıldı** (özel ad) |

## 2. Yapılanlar

- **Ek** (`araclar/lua/ALifeTR_Konusma.lua`, aynı dosya, aynı desen):
  - `kurIpucu`: `UI2Talk.statusText`'i sarar. Dönen metin `win.hoverTip` ise `IGUI_ALifeUI_` anahtarıyla bakar ve Türkçeyi tablonun **kopyasında** döndürür. "bekleniyor" gibi diğer durum yazılarına ve modun verisine dokunmaz.
  - `kurSoru`: `UI2Answer.clean`'i sarar. Yeni `ask` tablosunun `text`'ini önce konuşma anahtarıyla (`RD_ALifeLine_`, şablonlar dahil, NPC sözü), bulamazsa arayüz anahtarıyla çevirir. Seçenekler ve kimlikler aynı kalır.
    **Kapsam pilotla sınırlı değil:** `clean` bütün `standoffAsk` mesajlarından geçer. Bunlar kapı/yol karşılaşması, soygun ve çağrı şeritleri (`AnswerChannel`), radyo olayı soruları (`RadioWorld.ask`) ve bitiş (`EndingWorld`). Bu soruların metni şimdiye kadar hep ham çiziliyordu. Artık metni İngilizce gelen ve bir `RD_ALifeLine_`/`IGUI_ALifeUI_` çevirisi olan her soru Türkçe görünür; sunucuda zaten Türkçeleşmiş olan (K52, radyo) aranır, bulunmaz ve aynen kalır. Telsiz çağrısında birleştirilmiş (`, `) sorular eşleşmez, İngilizce kalır. Oyuncunun gördüğü bir değişiklik: oyunda denenmeli (§3).
  - İkisi de `pcall` korumalı, dil Türkçe değilse çalışmaz, çeviri yoksa İngilizce döner, hata olursa orijinal sonucu döndürüp eki kapatır. İstemci modülleri sonradan yüklenirse `OnGameStart`'ta bağlanır; ikinci kez sarmaz.
- **Anahtar önekleri:** yeni önek yok. Metinlerin hepsi modun kendi `Text.ui` anahtarını (`IGUI_ALifeUI_`) kullanır, diyalog nitelikli olanlar dahil. Gerekçe: oyun bunları zaten `Text.ui` ile arıyor. `RD_ALifeLine_` verilseydi ekin her birini ayrıca sarması gerekirdi. Y3 de aynı gerekçeyle IG_UI anahtarlı diyalogdu. Pilotun sorusu iki anahtara da bakar (önce `RD_ALifeLine_`).
- **Çıkarıcı:** `araclar/kacan_cikar.py` → `kaynak/IG_UI_kacan.json` (306) + `kaynak/IG_UI_kacan_baglam.json` (anahtar → dosya:satır, alan, grup, tür). Yer tutuculu metinleri ve zaten bir çeviri yolu olanları (mod EN IG_UI, `IG_UI_lua`, bekleyen haritalar) almaz.
- **Y6** (diyalog, 219 satır): `harici_paket.py hazirla-kacan Y6 --yeni` → `gemini/yeni/girdi/Y6_1..2.txt`, `rapor/Y6_harita.json` (`_dosya: IG_UI_lua`, Y5 gibi; `al` anahtarları `kaynak/IG_UI_lua.json`'a ekler). Etiketler: OYUNCU SEÇENEĞİ, ALT NOT (sonuç/risk/ipucu), NPC (soru). Her durum ve çağrı düğümü ayrı blokta, NPC'nin o sahnedeki sözleri "·" bağlam satırı. `PROMPTLAR.md` (Y6 ek cümlesi) ve `NASIL_KULLANILIR.md` güncellendi.
  - **Kuru deneme:** proje kopyasında (scratchpad), sahte çıktıyla `al Y6 --yeni` çalıştırıldı: 219 satır `paketler/Y6.json`'a (`_dosya IG_UI_lua`) girdi, 219 anahtar `IG_UI_lua`'ya eklendi, `paket_kontrol Y6` temiz. Gerçek dosyalara dokunulmadı.
- **Çıkarıcı yeniden çalışınca:** `al Y6` ve B paketi anahtarları `kaynak/IG_UI_lua.json`'a ekler. Çıkarıcı kendi önceki çıktısını "bilinen" saymaz, yani sonradan çalıştırılsa da aynı 306'yı verir. Bu, `al Y6` sonrası kopyada denendi: çıkarıcı 306 verdi, test geçti. **Dikkat (eskiden beri, Y5 için de geçerli):** `lua_cikar.py` `kaynak/IG_UI_lua.json`'u baştan yazar. `al` ile eklenmiş Y5/Y6 anahtarları o zaman düşer; yeniden çalıştırılırsa `al Y5`/`al Y6` tekrarlanmalı. `kacan_tara.py`'nin bilinen kümesine `IG_UI_kacan` eklenmedi: bir sonraki taramada bu 256 aday yine listelenir.
- **Arayüz grubu** (87 satır): çeviri yok; B14 ya da B13'e ek önerisi `rapor/B_paket_plani_1.5.0.md`'nin sonunda.
- **Test:** `araclar/test_konusma_kacan.py` (16 test). Modun gerçek `ALifeText`, `AudioPolicy`, `Speech`, `UI2Talk` ve `UI2Answer` dosyaları yükleniyor. Denetlenenler:
  - 306 anahtar Lua'nın `Text.key`'iyle aynı ve `Talk2.text` bu anahtarları buluyor.
  - Veri dosyaları Lua'da yüklenip gezildiğinde yer tutucusuz her satır/ipucu/aşama/ayar metninin bir çeviri yolu var.
  - İki ek için: çevirili metin dönüyor, çeviri yoksa İngilizce, hata olursa orijinal sonuç, dil başkaysa dokunmuyor, sonradan yükleme çalışıyor.
  - Y6 haritası yalnız bu diyalog anahtarlarını taşıyor.
  - Bütün `araclar/test_*.py` geçiyor (agac 9, font 17, kacan 16, sablon_eslesme 12, sablon_varyant 3).

## 3. Oyunda nasıl denenir

Y6 çevrilip `al` + onay + `workshop_kur` sonrası (ek, `workshop_kur` ile kopyalanan `ALifeTR_Konusma.lua`'nın içinde):

1. **Durum satırı:** Bir durum grubuyla konuş; Sandbox'ta durum deneyi açık olmalı (`factionscript_talk`; yönetici: Admin > World > "Spawn situation: Encircled depot"). Kişisel sekmedeki "What happened here" gibi satırlar Türkçe olmalı. Fare satırın üstündeyken alttaki not da Türkçe olmalı.
2. **Durum sorusu:** Yağmurda, gece ya da yaralıyken bir NPC'yle konuş (`dialogue_situation_questions`). "Any dry place nearby…" satırı ve notu Türkçe olmalı.
3. **Esir:** Teslim olmuş birini esir al. Yedir, sorgula, bırak satırları ve notları Türkçe olmalı.
4. **Dell'in çantaları:** Dell Tolliver'la konuş. Satırlar Türkçe olmalı. Fare satırın üstündeyken pencerenin altındaki ipucu ("Ask what happened to him") Türkçe olmalı: **yeni ek, burada sınanır.** Günlükte "Find Earl's bag" aşaması Türkçe olmalı (B önerisi işlenince); "Get to the {yer}" İngilizce kalır.
5. **Soru-cevap şeridi (yeni ek):** Bir kapı ya da yol karşılaşmasında, soygunda ya da radyo olayında alttaki şeritte çıkan soru, çevirisi varsa Türkçe olmalı; seçenekler eskisi gibi. Cevap verince oyunun tepkisi değişmemeli (cevap kimlikle gider).
6. **Bitiş:** Telsiz çağrısında seçenekler Türkçe olmalı ("{ad}, that's me" İngilizce kalır). Helikopterde pilotun üç sorusu ve cevaplar Türkçe olmalı: **yeni ek, ikinci sınama yeri.**
7. **Ayarlar:** Günlük > Ayarlar'da satır adları, değerler ve fareyle çıkan ipucu Türkçe olmalı (B önerisi işlenince).
8. Konsolda `[ProjectALife TR] Konusma cevirisi kapatildi` görünmemeli. Dil İngilizce seçiliyken hiçbir şey değişmemeli.

## 4. Tarayıcı boşluğu (doğrulanmadı, kapsam dışı)

`kacan_tara.py` tablo içindeki liste değerlerini (`lines = { "…", "…" }`) taramıyor. Bu yüzden şu NPC sözleri hiç sayılmadı:

- durumların giriş ve cevap sözleri (≈55),
- telsiz çağrısında ordunun sözleri (≈57),
- pilotun cevapları (≈17),
- bitişin yayın satırları (≈11),
- esirlerin cevapları (≈179).

Bunlar ham hâlleriyle hiçbir kaynakta ya da haritada yok. Ancak oyunda `Speech.render` sonrası (baş harf, noktalama) başka bir metinle `caption`'dan geçiyor olabilirler; o durumda anahtarları farklıdır. Ayrı bir iş olarak, `diyalog_cikar`'ın yöntemiyle (`render` + `caption` yolu) bakılmalı.

## 5. Yapımcıya bildirim taslağı (gönderilmedi)

> Hi Vice, a few strings in 1.5.0 can't be localized from the translation files. We're working on a Turkish translation and found these by reading the Lua:
>
> 1. **Admin/dev/Creator windows** (`client/ProjectALife/Admin/*`, `Builder/*`, `Driving/*Panel*`, `Interface/ALifeEncounterConsole`, `ALifeStatusWindow`, `Admin/ALifeSpawnPlan`, ~400 strings) draw text directly (`drawText`, `ISButton`, `addOption`, `"Staffed outpost: " .. label`) without `Text.ui`.
> 2. **Mission tips** (`MissionDefs.rows[].tip`) are drawn raw in the talk window status line (`Talk2.statusText` returns `win.hoverTip` as is). The ending standoff question text (`UI2Answer` `ask.text`) is also drawn raw. We patch both on our side for now.
> 3. **Server-filled templates** reach the client already filled, so the client `Text.ui` lookup can't match them. Examples: mission summary and stages with `{place}`, `ALifeEndingCallData` option labels with `{name}`, tree prompts with `{town}`/`{playerName}`/`{day}`, and party task texts built by concatenation (`"Bring the group " .. count .. " " .. noun`). Sending the template plus vars (like `Text.msg`) would fix these.
> 4. `ALifeTreeTasks` titles are copied into the saved task and concatenated with counts (`title .. " (" .. count .. ")"`).
> 5. Many `Text.ui` rows exist only in Lua and not in `IG_UI.json`, e.g. `SituationsData` rows (text/impact/risk), `TalkSituation`, `CaptivesData.rows`, `MissionDefs.rows`, ending call/talk options, `UI2Prefs` rows. They work if a translator adds the hash key, but having them in the EN JSON would make them visible to every translation.
>
> Thanks for the great mod!
