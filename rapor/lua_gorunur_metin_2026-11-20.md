# Project A-Life 1.5.2 · Görev alma, NPC Oluşturucusu ve yol arkadaşı menüleri

20 Kasım 2026. Kurulu ana modda, Türkçe teslimde karşılığı olmayan 73 İngilizce metni oyuncuya gösterildikleri Lua çağrılarıyla eşleştirdim. 53 satır mevcut sözlük aramasıyla çalışıyor. Kalan 20 satır için çalışma alanındaki NPC Oluşturucusu ekini güncelledim. İnceleme dosya ve bellek içi Lua düzeyinde yapıldı. Yorum sahiplerinin hangi ekranı, sürümü ve mod listesini kullandığı bilinmiyor.

| Fable girdisi | Satır | Görüldüğü yer | Kaynak konumları |
|---|---:|---|---|
| [AL_GOREV_IZ](../notlar/arsiv/2026-11-23/fable-dosyalari/girdi/AL_GOREV_IZ_1.txt) | 20 | Geride Kalanlar görevinde 4 günlük kaydı ve 2 kısa bildirim, Günlük → Ayarlar altında 1 ipucu, sinematik konuşma penceresinde 13 görüş gerekçesi | [Görev haritası](../paketler/haritalar/AL_GOREV_IZ_harita.json) |
| [AL_YOL_ARKADASI](../notlar/arsiv/2026-11-23/fable-dosyalari/girdi/AL_YOL_ARKADASI_1.txt) | 33 | 27 emir, 3 sağ tık etiketi veya ipucu, “Benimle gel” seçeneği için 3 kilit nedeni | [Yol arkadaşı haritası](../paketler/haritalar/AL_YOL_ARKADASI_harita.json) |
| [AL_OLUSTURUCU_KURAL](../notlar/arsiv/2026-11-23/fable-dosyalari/girdi/AL_OLUSTURUCU_KURAL_1.txt) | 20 | NPC ve fraksiyon davranış kartlarında 15 ayara dağılan 19 sabit açıklama ve ortak `RULES:` başlığı | [Oluşturucu haritası](../paketler/haritalar/AL_OLUSTURUCU_KURAL_harita.json) |

### Görevi kabul edince günlük neden İngilizce kalabiliyor?

Dell’in teklifindeki `Alright. I'll get your bags back` düğmesinin teslimdeki karşılığı **Peki. Çantalarını alıp getiririm**. Oyuncu bunu seçtiğinde sunucu uygun hedef bulursa günlüğe ayrı bir dize yazıyor: `Took the job from Dell Tolliver`. Günlük kendi anahtarını aradığı için düğmenin çevrilmiş olması yetmiyor. Çanta Six Mile Boys’a verilince de günlüğe `Gave the bag to the Six Mile Boys` yazılıyor, kısa bildirimde ise `The bag is gone. Tell Dell` gösteriliyor.

- `ALifeMissionDefs.lua:25–46` seçenekleri tanımlıyor. `ALifeMissionService.lua:461–469,574–593,623–652` kayıt ve bildirimleri oluşturuyor ve 792–813'te istemciye aktarıyor. `ALifeUI2Missions.lua:32,105–110,438–441,851–859` gövdeyi `M.text → Text.ui` üzerinden alıyor. Günlük, yer elverdiğinde son altı kaydı gösteriyor. Aynı İngilizceyi taşıyan eski kayıtlar da bu okumadan geçiyor.
- Bir NPC oyuncuyu Dell’in işine yönlendirince `They pointed you at work` görüş gerekçesi olabiliyor. `ALifeTaskTalkServer.lua:193–196` ve `ALifeFactionTalkServer.lua:104–108` etkiyi iletiyor. Koşullar ve etkinin ağırlığı uygunsa `ALifeNpcOpinion.lua:220–234` nedeni saklıyor. `Opinion.payload` (176–180) nedeni istemciye veriyor. Sinematik pencerede `ALifeTalkCinema.lua:696–714` fare ipucu için `Text.ui(reason)` çağırıyor.
- Doğrudan `Text.ui("…")` çağrıları ve önceden seçilmiş dolaylı kaynaklar üzerinden çalışan çıkarıcı, `M.text(log[index])` veya `Text.ui(reason)` satırına bakarak başka dosyada üretilen İngilizceyi bulamıyor. Görev ekinin konumları ve sayıları çözmesi de bu sabitlere karşılık sağlamıyor. [Lua çıkarıcısı](../araclar/lua_cikar.py) · [Görev eki](../araclar/lua/ALifeTR_L152.lua)

### Karakter oluşturma ekranı

Oyuncunun kendi karakterini oluşturduğu vanilla formunda kontrol edilen ad, rastgele seçim ve marangoz mesleği anahtarları oyunun TR sözlüğünde **Ad**, **Rastgele**, **Marangoz**. A-Life’ın yeni oyun zorluk ve nüfus kartları ayrı bir ekran. Kurulu `ALifeUI2StartPick.lua` içindeki 9 ve `ALifeUI2StartPickData.lua` içindeki 48 benzersiz doğrudan `Text.ui` girdisinin hepsine teslimde anahtar bulundu. Örneğin **Zorluğu seç** ve **Nüfusu seç**. Bu sayım yalnız doğrudan İngilizce sabitleri kapsıyor. Tanıtım galerisinde ayrıca A-Life’ın NPC Oluşturucusu görülüyor. [Galeri ve ekran ayrımı](ingilizce_metin_ve_guvenli_ceviri_yollari.md)

**NPC Oluşturucusunda güncel bir açık doğrulandı.** Örneğin **Ölülerden korkma** ayarında davranış açıklaması, ` RULES: ` ve iki kural cümlesi birleşiyor. Bunlardan biri `Military factions do not use fear.`, diğeri ilk üç güne uzanan dönemde korkunun her tim için nasıl belirlendiğini anlatıyor. `ALifeModuleRules.lua:241–255` notları seçiyor. `ALifeCreatorModuleRules.lua:8–14` onları birleştiriyor. `ALifeCreatorCore.lua:1158–1170` sonucu etiket, açılır liste ve bilgi simgesinin ipucuna katıyor. Birleşik dizenin anahtarı ile tek tek cümlelerin anahtarları farklı. İlk taramada düzeltme öncesindeki ek ve deneme sözlüğüyle 15 ayarın tamamında kural kısmı İngilizce kaldı. [Oluşturucu eki](../araclar/lua/ALifeTR_Creator.lua)

**Çalışma alanındaki düzeltme.** Oluşturucu eki, kartın gösterdiği İngilizce kural dizisini modun o ayar için verdiği sıralı notlarla eşleştiriyor. Ana yardım metnini, başlığı ve kuralları kendi anahtarlarından okuyup ipucunu oluşturuyor. Açılır liste seçimi değişip `refreshModuleRuleHints` yeni uyarıyı yazdığında aynı işlem anında uygulanıyor. 20 anahtar Fable paketindekilerle eşleşiyor. Koşullu uyarının kuraldan önce gelen dinamik İngilizce ön eki bu 20 metnin dışında.

Kurulu 1.5.2 kart oluşturma işlevi ve kural modülleriyle, Lua 5.1 altında hem NPC hem fraksiyon kartları sınandı. Etiketin, bilgi simgesinin ve listenin 20 deneme değerini göstermesi, uyarının seçimle açılıp kapanması, eksik sözlük girdisinin özgün İngilizceye dönmesi, İngilizce oyun dili, başka modun eklediği not ve ham seçenek değerleri kontrol edildi. Workshop paketi gerçek Fable metinlerinin kontrolünü ve aktarım onayını bekliyor. [Oluşturucu testi](../araclar/test_l152.py)

### Yol arkadaşı menüleri

`ALifeCompanionClient.lua:20–55` komut kimliği ile görünen etiketi ayrı tutuyor. Örneğin `watch_there` kimliğinin ekrandaki adı `Watch there`. Dairesel menü `fillSub` (280–289) ile çevrilmiş etiketi dilime, özgün kimliği tıklama işleyicisine veriyor. Sağ tık menüsündeki karşılığı 449–468. Kullanılabilir emirler yol arkadaşına, araç durumuna ve etkin menü seçeneklerine bağlı.

“Benimle gel” kilitliyken sunucu gerekçeyi kodla bildiriyor. İstemci `party full` gibi sabit metni çevirdikten sonra varsa `5/5` sayacını ve ayraçları ekliyor. Fable’a yalnız neden verildi. Türkçe ek alacak değişken bir ad veya korunması gereken sayısal yer tutucu bulunmuyor. Kaynaklar `ALifeTalkRowHookServer.lua:142–161` ve `ALifeUI2TalkHook.lua:33–45`.

### Kopyalar ve denemeler

- Ana modun `42.20/mod.info` sürümü **1.5.2**. Kurulu dört resmî EN JSON, `kaynak/en/` ile bayt bayt eşleşti. **5.351 IG_UI, 1.676 Sandbox, 9 UI ve 6 ItemName** anahtarının tamamı teslimde var. Yalnız resmî JSON anahtarlarını karşılaştırınca yukarıdaki açıklar görünmüyor.
- Bu makinede Steam abone klasörü ile yerel Workshop hazırlığındaki 12 ortak mod dosyası birebir eşleşti. Yalnız yerel hazırlıkta bulunan dosya `ALifeTR_AD1.lua`. AD1’in 396 anahtarı iki kopyada da var. Yönetici ekranlarındaki bazı etiketlerin görünmesi yerel ekteki bağlantıya bağlı. Bu karşılaştırma yorum sahibinin kurulumunu göstermiyor.
- Kurulu Lua modülleri ve mevcut yama Lua 5.1 ile iki kez çalıştırıldı. Gerçek teslimle İngilizce kalan 53 satır, yalnız bellekte kendi anahtarlarına deneme değerleri verilince o değerleri döndürdü. Görevde `M.text`, görüşte `Window.opinionState`, emirlerde gerçek alt menü ve araç etiketi, sağ tık metinlerinde `Client.text`, kilitlerde `lockedRows` sınandı. Dolu grup sayacı ve kilit kimliği korundu. Oluşturucuda gerçek kural seçicisi ve birleşik araç ipucu mevcut TR ekinden geçirildi. Oyun pencereleri ve sözlük servisi testte temsil edildi. Canlı tek oyunculu veya çok oyunculu oturum açılmadı.
- Üç TXT’nin numarası, İngilizcesi, kaynak konumu ve anahtarı haritalarla eşleşti. Anahtarlar teslim, onaylı sözlükler ve diğer paket haritalarıyla çakışmıyor. Üçü de geçici bir klasörde deneme değerleriyle `harici_paket.py al` üzerinden okundu. Mevcut 15 L152 testi geçti.

### Tekrar çeviriye gönderilmeyen örnekler

- `Clear the warehouse` istemci kodunda aşama karşılaştırmasında geçiyor. Ekranda kullanılan Dell hedefi mevcut ekte yer adına göre işleniyor. Bu sabiti doğrudan değiştirmek ayrıntı gösterim koşulunu bozabilir. `Gave the job up` ise gerçek bir günlük satırı. Ayrı bildirimdeki **Görevden vazgeçtin** karşılığının günlük anlatımına da uyup uymadığı ayrıca değerlendirilebilir.
- Görev bankasındaki `TB_GEN.quit` ve `TB_GEN.sit` havuzlarının dört repliği için çağrı doğrulanamadı. Oluşturucuda da `Rules.notes` sekiz `raidCommit` kuralını açıkça atlıyor. Bu metinler 73’e dahil edilmedi.
- Yol arkadaşı menüsündeki `Hold there` işaretlenen konumda bekleme emri. Başka bağlamdaki `Hold there!` için onaylanmış **Olduğun yerde kal!** repliğini burada kullanmak, oyuncunun gösterdiği konumu kaybettirir. `Hold fire` için küçük harfli `hold fire` karşılığı da var. Bu iki etiketi yeni pakete almadım.
