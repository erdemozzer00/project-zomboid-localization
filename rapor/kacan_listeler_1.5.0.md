# 1.5.0 kaçan metinler, ek: tablo içi listelerdeki NPC sözleri

2026-11-09, ayrı oturum. `rapor/kacan_ek_1.5.0.md` §4'teki tarayıcı boşluğunu kapatır. `kacan_tara.py`, tablo içindeki liste değerlerini (`lines = { "…", "…" }`) görmüyordu. Bu dört listenin oyundaki gösterim yolu kodda izlendi. Gösterilen metin modun kendi Lua'sıyla (lupa) üretildi: `araclar/liste_cikar.py`.

## 0. Bitiş telsizi ve pilot: ek yazıldı (Y9)

Kullanıcının kuralı: "güvenliyse ve çalışacağına inanıyorsan eke al, değilse bırak". Ölçüt: yalnız ekranda görünen metni değiştirir, `pcall` korumalı, çeviri yoksa İngilizce kalır, kayda ve ağa Türkçe yazmaz. Dört yere ayrı ayrı bakıldı (ayrıntı §4):

- **Alındı:** telsiz kartı (`RadioClient.card`, ek `kurKart`) ve pilotun altyazısı/bildirimi (`EndingClient.say`, ek `kurPilot`). İkisi de istemcide, sunucudan gelen tablonun kopyasını çizer.
- **Bırakıldı:** sunucudaki telsiz yayını (`EndingWorld.air` → Java `RadioLine`) ve pilot gövdesinin baş üstü yazısı (`World.crewSay` → `body:Say`). İkisi de sunucuda metni oyun nesnesine yazar. Barındırılan çok oyunculu oyunda o metin başka oyunculara gider; "ağa Türkçe yazmaz" ölçütü sağlanamıyor.

**Y9** (28 satır, `gemini/yeni/girdi/Y9_1.txt`, harita `rapor/Y9_harita.json`): kartta görünen 7 ilk satır ve pilotun 21 sözü. Yayının geri kalan 143 satırı oyunda yalnız radyo yayınında geçer; Türkçe görünmeyeceği için alınmadı (K46).

## 1. Özet

| Liste | Girdi | Gösterim yolu | Çeviri yolu | Sonuç |
|---|---|---|---|---|
| Durumlar `SituationsData.situations[].lines` (giriş + cevap) | 55 | `Talk.speak → Speech.render → Speech.say → AudioPolicy.caption` | Var (ek, `RD_ALifeLine_`) | **Y7: 55** |
| Esirler `CaptivesData.lines[anahtar][grup]` | 336 (220 tekil) | `FS.say → FT.recordsFor → Talk.speak → render → caption` | Var (ek, `RD_ALifeLine_`) | **Y7: 181**. 39 tekil anahtar zaten kaynakta ("Not yet", "Thanks" gibi kısa sözler, başka yerlerden), Y7'de "·" bağlam |
| Telsiz çağrısı düğümleri `EndingCallData.nodes[].lines/alt/again`: **cevap şeridi sorusu** | 37 çeşit | `Run.offerNode → d.offer(…, concat(Call.fill(satır), ", ")) → standoffAsk → UI2Answer.clean` | Var (ek `kurSoru`, birleşik metnin `RD_ALifeLine_`'ı) | **Y7: 28**. `{name}` içeren 9 çeşit bırakıldı (§5) |
| Aynı düğümlerin tek tek sözleri (telsiz yayını) | 74 | `Run.airLines → RadioChannel.air` (Java `RadioLine`); `offerNode` kart göndermez | **Yok** (sunucu, sarılmadı) | Alınmadı (§4) |
| Çağrının yaprakları, hatırlatma, başarısızlık, varış, kesilme (`leaves/reminders/failure/arrival/cut`) | 65 | Yayın + kart | Kart: ek `kurKart` | Yayın alınmadı. Kartın ilk satırı **Y9** (aşağıda) |
| Bitiş yayını `EndingData.lines` `broadcast/reply/missed` | 11 | `Director.airLines → air` + kart (`lines[1].text`) | Kart: ek `kurKart` | Yayın alınmadı. Kartın ilk satırı **Y9** |
| **Telsiz kartı** (her yayının ilk satırı; yaprakta oyuncunun seçtiği etiket) | 14 ilk satır | `Run.card`/`Director.airLines → radioCard → RadioClient.card` | Ek `kurKart`: `RD_ALifeLine_`, yoksa `IGUI_ALifeUI_` (etiket, Y6) | **Y9: 7**. `{name}`'li 7 ilk satır İngilizce kalır (hatırlatma, varış, bir başarısızlık) |
| Pilot `EndingData.talk` `intro/outro`, `beats[].options[].reply`, `beats[].silent.reply`, `lines.pilot` | 21 | `Director.pilotSay → "endingSay" → EndingClient.say` (altyazı ya da `RadioClient.push`) + `World.crewSay → body:Say`; `board/ready/waiting` ayrıca `Director.offer` (cevap şeridi) | Ek `kurPilot` (+ mevcut `kurSoru`); `body:Say` sarılmadı | **Y9: 21** |

Y9 toplamı: **28 satır**, 2 blok (telsiz kartı, helikopter pilotu), `_dosya: RadioData_lua`. Komut: `python -X utf8 araclar/harici_paket.py hazirla-bitis-soz Y9 --yeni`.

Y7 toplamı: **264 satır**, 37 blok, 3 dosya (`gemini/yeni/girdi/Y7_1..3.txt`, harita `rapor/Y7_harita.json`, `_dosya: RadioData_lua`).

## 2. Yollar (kod okuması, mod 1.5.0)

- **Durum.** Sunucu `ALifeSituationsServer` (`react` ve satır cevabı) `api.say(record, shell, player, S.lineRecords(def, key))` çağırır. `S.lineRecords` `{ t = satır }` kayıtları kurar; `.again`/`.none` yoksa taban anahtara düşer. `W.say → Talk.speak` (Talk4Ask ve Talk6 sarmaları metni değiştirmez) `Speech.render(t, vars, shell, psex)` ile baş harfi büyütür, `Speech.say` gönderir. İstemci `AudioPolicy.caption`'dan geçirir; ek orada `Text.lineKey(gösterilen)` arar. Satırlarda yer tutucu yok.
- **Esir.** `CTK.merge` `D.lines`'ı `FactionTalkLines.sets`'e koyar. `CS.*` işleyicileri `HS.say(ctx, "CAP_…")` çağırır, o da `FS.say → FT.recordsFor(key, grup)` (grubun listesi, yoksa `any`) `→ Talk.speak` ile durumdakiyle aynı yoldan geçer. `CAP_FORCE/INTEL` anahtarlarına oyunda esir ağacının sonuçları da eklenir (`CT.merges`); onlar Y4'te. Yer tutucu yok.
- **Telsiz çağrısı sorusu.** `Run.offerNode` düğümün o anki çeşidini (`Call.lines`: koşulu tutan `alt`, yeniden gelişte `again`, yoksa `lines`) `Call.fill(satır, Call.vars(oyuncu adı))` ile doldurur ve `table.concat(…, ", ")` ile **tek soru metni** yapar. `Director.offer → World.ask → standoffAsk` istemcide `UI2Answer.clean`'e gelir; ek `kurSoru` metni önce `RD_ALifeLine_` ile arar. Birleşik metnin anahtarı üretilince bu yol çalışır (test: §6).
- **Telsiz yayını ve kartı.** `Run.airLines` her satırı `{name, text}` yapar; `World.air → RadioChannel.air` sunucuda Java `RadioLine` olarak `"ad: metin"` yazar. Çeviri yok (K52'deki radyo olaylarının aksine `Text.ui`'den geçmez). `Run.card`/`Director.airLines` kartı `text = lines[1].text` ile gönderir; `RadioClient.card` yalnız başlığı `Text.ui`'den geçirir, metni ham çizer.
- **Pilot.** `Director.pilotSay` `endingSay` gönderir; `EndingClient.say` metni ya altyazıya (`Client.subtitle` → `drawTextCentre(line.text)`) ya da `RadioClient.push → UI2Notify.push` ile bildirime ham koyar. Pilot gövdesi oturuyorsa `World.crewSay → body:Say(text)` da ham. Hiçbiri `caption`, `Text.spoken` ya da `Text.ui`'den geçmez.

## 3. Y7

- Komut: `python -X utf8 araclar/harici_paket.py hazirla-liste-soz Y7 --yeni`. Blokları `liste_cikar.y7_bloklari` kurar.
- **Durum** blokları: önce karşılaşma sözü (NPC (karşılaşınca)), sonra her oyuncu satırı "·" bağlam olarak ve altında NPC cevapları (`.again` = aynı satır yeniden seçilince, `.none` = koşul tutmadığında).
- **Esir** blokları: oyuncunun satırı (CAP_FEED…) başına bir blok. Etikette grup ve durum var, ör. "ESİR (sivil/işçi/kurtarıcı · bugün zaten yemişken)". Aynı listeyi paylaşan gruplar tek etikette. Kaynakta olan söz "·" bağlam.
- **Telsiz** blokları: düğüm başına bir blok, `open`'dan seçeneklerin `to`'suna genişlik öncelikli sırayla. Konuşan etikette (US Military / Captain Ruiz). Altında oyuncunun o düğümdeki seçenekleri "·" bağlam. NEREDE notu, metnin oyunda ", " ile birleşmiş tek soru olduğunu ve cümlelerin aynı sırayla, ", " ile çevrileceğini söyler.
- Anahtar: `RD_ALifeLine_` + `Text.hash(gösterilen)`. `al Y7 --yeni` anahtarları `kaynak/RadioData_lua.json`'a ekler (Y4 gibi).
- "Bilinen" sayılanlar: çalışma ağacındaki `kaynak/RadioData_lua.json` ve bekleyen haritalar. **Dikkat:** başka bir oturumun henüz commit edilmemiş eklemesi (barks) 3 esir sözünü kapsıyor: "What do you want from me", "Not a word", "I'll remember this". O değişiklik geri alınırsa bu üçü Y7'ye girmeli: `hazirla-liste-soz Y7` yeniden çalıştırılır.

## 4. Bitiş telsizi ve pilot: dört yerin değerlendirmesi

| Yer | Nerede çalışır | Karar | Neden |
|---|---|---|---|
| Telsiz kartı `RadioClient.card(args)` | İstemci | **Alındı** (`kurKart`) | `args`'ın kopyası Türkçe `text` ile çizilir; sunucuya yalnız `args.id` gider (`radioHeard`), değişmez. `hint/mark/drop/notice` kartlarına dokunulmaz (kendi `Text.ui` yolları var). Önce `RD_ALifeLine_`, yoksa `IGUI_ALifeUI_`: yaprakta kartın ilk satırı oyuncunun seçtiği etiket, onun çevirisi Y6'da. Radyo olayı kartları (K52) tek oyunculukta sunucuda zaten Türkçe gelir; aranır, bulunmaz, aynen kalır. |
| Pilot `EndingClient.say(args)` | İstemci | **Alındı** (`kurPilot`) | Kopya Türkçe `text` ile verilir; altyazı listesi (`Client.subs`) ve bildirim yalnız istemcide, kaydedilmez. `Client.hint`'in son çaresi de buradan geçer. |
| Telsiz yayını `EndingWorld.air(lines)` → `RadioChannel.air` | Sunucu | **Bırakıldı** | Metin Java `RadioBroadcast`'a yazılır. Barındırılan çok oyunculu oyunda bu yayın her dinleyiciye gider; sunucunun dili Türkçeyse Türkçe metin ağa çıkar. Özel sunucuda zaten İngilizce kalırdı. |
| Pilot gövdesi `World.crewSay` → `body:Say` | Sunucu | **Bırakıldı** | Karakterin `Say`'i çok oyunculuda eşitlenir. Aynı söz `kurPilot` ile altyazıda zaten Türkçe. |

Ek, iki modül yoksa ya da işlevleri değişmişse kurulmaz; satır İngilizce görünür. Çeviri ararken hata olursa ek kendini kapatır (`kapat`), metin İngilizce çizilir. Dil Türkçe değilse hiçbir şey yapmaz. İstemci modülleri ekten sonra yüklendiği için bağlantı `OnGameStart`'ta da denenir (testte bu sıra sınanıyor).

**Bilinen sınırlar:** kart ve hatırlatmalardaki `{name}`'li ilk satırlar (7) ve pilotun beklerken söylediği sözün `20` dakikası sabit (`numbers.waitMoreMinutes`) değerine bağlı. Kartın konuşan adı (`US Military`, `Captain Ruiz`) çevrilmez; ad olarak kalır.

## 5. Bırakılanlar ve riskler

- **`{name}`'li 9 çağrı sorusu** (`found`, `offer`, `think`, `decide`, `accept1`, `bargain.again`…): oyuncunun adı sunucuda dolar. Ekin şablon eşleşmesi `{name}`'i yalnız `Speech.names`'teki NPC adlarıyla kabul eder (`gecerli("name")`), oyuncu adını tutmaz. İngilizce kalır.
- **Varsayılan ayarlara bağlı anahtarlar:** çağrı sorularında `{place}` `Oris Tower`, `{time}` `14:00`, `{days}` `3`, `{minutes}` `30` ile doldu (`EndingCallData.numbers.place`, `EndingData.numbers.landHour/leadDays/stayMinutes`). Bu değerleri kodda yeniden yazan bir yer bulunmadı (grep). Bir sürüm ya da ayar bunları değiştirirse bu satırların anahtarı tutmaz, İngilizce kalır. Y7'de bu değerleri içeren tek soru `refuse1`; diğerleri `{name}`'li olduğu için zaten bırakıldı.
- `Speech.render` sonda `DialogueGuard.strip` çağırır; lupa'da bu modül yüklenmedi (`agac_cikar` de yüklemiyor). Etkisi yok: `strip` yalnız sondaki tek noktayı siler, durum ve esir sözlerinin hiçbiri tek noktayla bitmiyor. `RadioFreq.relabel` de atlanıyor; sözlerde frekans geçmiyor.
- Çağrı sorusu kırpılmıyor: bitiş `AnswerChannel.send` kullanıyor; 240 baytlık kırpma yalnız `Channel.offer`'da. En uzun Y7 sorusu 148 bayt. `UI2Answer.clean` metni değiştirmiyor.
- Talk3'ün ek havuzunda (`R.extra`) `CAP_` anahtarı yok: oyunda esire başka söz eklenmiyor.
- `Speech.render`'ın `shell`'e bağlı kısmı (cinsiyet `{g:…}`, `{town}`) bu listelerde yok; `shell = nil` ile üretilen metin oyundakiyle aynı.

## 6. `kacan_ek_1.5.0.md` düzeltmesi

O raporun §2 tablosundaki "Helikopter pilotunun sorusu" satırı ve §3'teki `kurSoru` notu, telsiz çağrısında birleşik soruların "tam metin eşleşmez, İngilizce kalır" diyordu. Bu doğru değil: birleşik metin oyunda değişkensiz ve sabit (varsayılan ayarlarla). Anahtarı birleşik metinden üretilince `kurSoru` onu bulur. Y7 bu 28 soruyu alır; `{name}`'li 9'u yine İngilizce kalır.

## 7. Testler

`araclar/test_konusma_liste.py` (15 test). Modun gerçek `ALifeText`, `AudioPolicy`, `Speech`, `UI2Answer` ve `EndingData/Rules/CallData/Call` dosyaları ile konuşma eki yükleniyor. Denetlenenler:
- Durum (cevap ve giriş) ve esir (asker) sözü: ham metin `render` ve ekli `caption`'dan Türkçe çıkıyor; çevirisi yoksa İngilizce.
- Çağrı: `open` düğümünün sözleri `Call.fill` ve `", "` ile birleşip ekli `UI2Answer.clean`'den Türkçe çıkıyor. Tek düğüm sözü bu anahtarla bulunmuyor.
- Yolu olmayan ve yer tutuculu girdiler anahtarsız. Y7 haritasındaki her anahtar `Text.lineKey(en)` değerinde, tekil ve yalnız çevrilebilir türlerden.

- Telsiz kartı ve pilot: modun gerçek `ALifeRadioClient` ve `ALifeEndingClient` dosyaları ekten sonra yüklenir, `OnGameStart`'ta bağlanır. Kart ve pilot sözü Türkçe çizilir, sunucudan gelen tablo değişmez. Seçenek etiketi arayüz anahtarıyla bulunur. Çevirisiz, dil Türkçe değil ya da arama hata verirse İngilizce kalır; hatada ek kapanır. Y9 haritası yalnız kart ve pilot satırları taşır.

Bütün `araclar/test_*.py` (6 dosya) geçti. Oyun içi çizim doğrulanmadı.

## 8. Oyunda denenecek

1. Bir durumla karşılaş (ör. Tolliver deposu): giriş sözü ve satır seçince gelen cevap Türkçe mi?
2. Esir al, yemek ver, hâl hatır sor, sorgula: cevaplar Türkçe mi?
3. Bitiş telsiz çağrısında cevap şeridinin üstündeki soru metni Türkçe mi? `{name}`'li düğümlerde İngilizce kalması bekleniyor. 
4. Bitişte telsiz kartı (ilk yayın: "This is the United States military") ve helikopterde pilotun altyazısı Türkçe mi (Y9 işlendikten sonra)? Radyo cihazındaki yayın ve pilotun başı üstündeki yazı İngilizce kalır.
