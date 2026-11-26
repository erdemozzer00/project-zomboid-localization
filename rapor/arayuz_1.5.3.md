# Project A-Life 1.5.3 arayüz taraması

23 Kasım 2026. Tarama kurulu 1.5.3 Lua dosyaları ve yerel 2.00 teslimiyle yapıldı. Erdem’in onayıyla [UI153](../paketler/UI153.md) ve istemci bağlantıları yerel Workshop paketine aktarıldı. Son kontrol temiz, 15 paket dosyası doğrulandı.

| Ekran | Yeni satır | Görünen metin |
|---|---:|---|
| Konuşma penceresi | 9 | Altı işlenmeyen tıklama bildirimi, fare ve kumanda onayı, NPC sorusu durumu |
| Konuşma tuşu | 2 | Uygun NPC’ye bakarken tuş ipucu ve konuşmayı engelleyen doğrultulmuş silah bildirimi |
| ESC A-Life paneli | 7 | Tanılama aç/kapat, kara kutu klasörü ve dosya bildirimi, uzak sunucu kopyasının konumu |
| A-Life ayarları | 4 | Tanılama, kayıt ve hata bildirimi açıklamaları |
| Klasik NPC oluşturma | 1 | Bir işlemde oluşturulan NPC sayısının ipucu |

Konuşma penceresi durum bildirimine büyük harf dönüşümü uyguluyor. Türkçe ek, tıklama bildirimi gerçekten gösterildiğinde cümle biçimini koruyor. Böylece Türkçe karakterler bozulmadan görünüyor. Kumandanın A tuşu etiketinde düz kesme işareti kullanıldı. Kara kutu metinlerindeki `{path}` yerel dosyanın tam yolu, `{where}` sunucu konumunun hazır açıklaması.

Performans laboratuvarı ve 1.5.3’te sağ tık menüsünden kaldırılan test araçları etkin `diag_menu_min` ayarıyla görünmüyor. `Say`, `Topic` ve `Hold {n}` alanları konuşma tablosuna kuruluyor. 1.5.3 çizim kodunda bunların bir kullanımına rastlanmadı. Tanılama ayarındaki resmî açıklama dökümleri hâlâ sağ tık menüsünde anıyor. Aynı sürüm bunların bir kısmını ESC paneline taşıyor. UI153 resmî açıklamayı çeviriyor.

## Önceden çevrilen yönetici metinleri

AD1 ekine 160 eski anahtar daha bağlandı. Betiğin bağladığı toplam 343 anahtar mevcut Türkçe sözlükte doğrulandı. Bağlantılar yönetici konsolunun yerleşik panelleri, oluşturma ve karakol listeleri, Temizlik, Kurucu ve Damga, Dünya durumu, sürüş haritası, rota şablonları ve sürüş ayarlarına ait. Komut kimlikleri, geri çağırma işlevleri, dosya yolları ve kullanıcı verileri özgün değerleriyle işleniyor. Dar sürüş düğmelerinde Türkçe etiket verilen genişliğe sığmazsa kaynak etiket kullanılıyor.

AD1 haritasında bu bağlantıların dışında kalan 53 kayıt incelendi.

- Üç kayıt mevcut sunum yolunda Türkçe. Dünya durumu başlığı L152 ekine, Hızlı Oluştur’daki İmleç ve 30 ileride düğmeleri ana modun sözlük aramasına bağlı.
- İlk taramada 34 kayıt ana akış dışındaydı. Bunların 21’i klasik Karşılaşma Konsolu’nun yedek açılış yoluna daha sonra bağlandı. Sekiz kayıt Hızlı Oluştur planlarının ekrana verilmeyen veri alanlarında, ikisi çağrısı tespit edilemeyen geliştirici menüsü kayıtlarında. İki kayıt Lua birleştirme ifadesinden yakalanmış, biri zengin metin biçim etiketi.
- Kalan 16 kayıt ikinci geçişte incelendi. Temizlik kaydı 75, kullanılmayan eski `CleanupWindow.tab` tanımı. Güncel Temizlik sekmesini `ALifeAdminTabCleanup` kuruyor.

## Son 15 görünür kayıt

| AD1 sıra numarası | Görüldüğü yer | Bağlantı |
|---|---|---|
| 3–5 | Oluşturucu araç özeti, katalog hatası ve silaha takılı parça sayacı | Araç özeti mevcut ön eki ve boya adını kullanıyor. Hata ve parça sayacı mevcut Oluşturucu kalıplarından çevriliyor. |
| 22, 188 | Araç ek teçhizat başlığı ve sürüş ayarları | Araç kimliği, zengin metin etiketleri ve bilinmeyen hata ayrıntısı korunuyor. |
| 47, 82 | Sabitleme yıldızı ve test üssü etkinliği | Araç çubuğu sınırı ve etkinlik kimliği, görünür ipucuna değişken olarak yerleştiriliyor. |
| 76–78 | Klasik NPC oluşturma | Karakol adı, gelişmiş menü ipucu ve oluşturulan NPC sayacı çevriliyor. Seçenek kimliği ve bildirimin ek gerekçesi korunuyor. |
| 111–113 | Kurucu aracı | Not türünün ipucu, kaydetme hatası ve klasör açma hatası çevriliyor. Dosya yolu ve özgün iç günlük aynı kalıyor. |
| 137–138 | Damga | Önizleme gereksinimi düğme ipucunda ve durum bildiriminde çevriliyor. Yerleştirilecek, mevcut, atlanan ve kaldırılacak nesne sayıları korunuyor. |

Bu bağlantılar için hazırlanan 27 bileşik arayüz metni [AD153](../paketler/AD153.md) paketinde. Erdem’in onayıyla Türkçe metinler ve iki istemci eki yerel Workshop paketine aktarıldı. Son kontrol temiz. 27 metin ve 15 Workshop dosyası doğrulandı.

## Doğrulama

23 yeni sözlük anahtarı modun Lua sözlük işleviyle, dosya yolu değişkenleri ve İngilizce geri dönüşüyle sınandı. Konuşma penceresinin altı bildirimi, üç durum etiketi ve kara kutu yolu hesaplamaları gerçek 1.5.3 işlevlerinden geçirildi. Yönetici bağlantılarında dış sekmeler, eylem işleyicileri, açılır liste kimlikleri, Türkçe etiket ölçümü ve dar sürüş düğmesi için geri dönüş sınandı. Otomatik testler ekran çizimini canlı oyun oturumunda doğrulamıyor.

## Klasik Karşılaşma Konsolu

`EncounterConsole.open`, klasik NPC oluşturma penceresinin `open` işlevine erişemediğinde `openLegacy` kullanıyor. AD1’in 194–214 numaralı onaylı karşılıkları bu pencerenin düğme başlığı ve metin çizimi katmanına bağlandı. Türkçe düğme başlığı sığmadığında, sözlük erişimi hata verdiğinde veya çeviri eksik olduğunda kaynak etiket kullanılır. İstemcinin gönderdiği komut, fraksiyon ve karşılaşma kimliği, koordinatlar ve sunucudan gelen gerekçe özgün değerleriyle işlenir.

Çizim çağrılarından başlayan ek tarama, `1  SQUAD`, `2  ENCOUNTER`, `3  DEPLOY` ve `ON THE MAP` gibi başlıkların pencereye doğrudan verildiğini, mevcut kaynak sözlüklerinde bu dizelerin bulunmadığını gösterdi. Bunlar yedek konsola ait yeni çeviri adayları. Oyunda bu pencerenin olağan bir oturumda açıldığı doğrulanmadı.

Kurulu 1.5.3 konsoluyla arayüz ikameleri üzerinden düğme eylemi, gelişmiş görünüm, sunucuya giden parametreler, hata metninin çizimi ve İngilizce geri dönüş sınandı. 117 test geçti. Son kontrol temiz. Yerel Workshop paketindeki 15 dosyadan yalnızca `ALifeTR_AD1.lua` değişti.

## Oyun oturumu ve yayın paketi

Erdem 23 Kasım’daki oyun içi denemede sorun görmedi. `console.txt` 17.59’da başlayan 42.22.2 oturumunda önce `ProjectALifeNPCs`, ardından `ProjectALifeNPCs_TR` modunun ve Türkçe sözlüklerin yüklendiğini gösteriyor. Türkçe Lua eklerine bağlanan hata bulunmadı. Günlük mod kimliğini kaydediyor, yüklenen kopyanın yolunu göstermiyor. Ana modun `ALife.Combat_BulletPenetration` ayarındaki `false` değeri ile `ALifeWhizAudioReady` ses modülüne ilişkin uyarıları kayıtta yer alıyor.

Temiz son kontrolden sonra yerel Workshop paketi yeniden oluşturuldu. Beş Türkçe sözlük, beş Lua eki ve harita işaretinin İngilizce karşılığı dahil 15 dosya doğrulandı. N153, S153R, UI153 ve AD153’te işlenen 668 karşılık onaylı paketlerle eşleşti. Steam abonelik önbelleğine göre üç sözlük ve üç Lua eki güncel. Dosya listesi, Workshop kimliği `3833513956`, yama sürümü `2.00` ve gereken en düşük oyun sürümü `42.21.0` aynı. Steam yüklemesi Erdem’de.
