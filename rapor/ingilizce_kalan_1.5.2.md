# Project A-Life 1.5.2 — ekranda görünen İngilizce metin taraması

**Durum:** Salt okunur kaynak incelemesi; çeviri, onaylı dosya, teslim paketi veya mod kaynağı değiştirilmedi. Genişletilmiş ham döküm: `rapor/ingilizce_kalan_1.5.2.json`.

## Kapsam ve sınırlar

Kurulu ana modun `mod.info` sürümü 1.5.2 (`Workshop 3803984183`, `42.20/media/lua`). `kacan_tara.py`, `lua_cikar.py` ve `creator_cikar.py` eski tarama dosyalarını ezmeden, geçici kaynak kopyalarıyla incelendi. Kaynak Lua dosyaları salt okunur kaldı. Bu rapor gerçek oyun oturumu veya ekran görüntüsü testi değildir. Salt dize eşleşmesi, görünürlük kanıtı sayılmaz; görünürlük bilgisi yalnızca aşağıda çağrı yolu izlenen metinlerde doğrulandı.

## Çıkarıcılarla karşılaştırma

| Yol | Güncel çıkarım | Mevcut kaynak haritası | Onaylı / teslimde eksik |
|---|---:|---:|---:|
| `Text.ui` / arayüz (`IG_UI_lua`) | 1.333 anahtar | 1.333 | 0 / 0 |
| A-Life Oluşturucu (`Creator_lua`) | 1.838 anahtar | 1.889 | 0 / 0 |

`lua_cikar.py` ile 1.5.2 Lua'sından yeni bir eksik anahtar çıkmadı. Çıkarıcının `ALifeNpcOpinion.lua` için tuttuğu üç dolaylı kaynak satırı güncel dosyada bulunmadı; tarama `--devam` ile sürdürüldü. Bu eski liste uyarısı, mevcut onaylı/teslim anahtarlarında eksik göstermez.

`creator_cikar.py`'nin güncel bulduğu bütün anahtarlar onaylı ve `teslim/IG_UI.json` içinde. Haritadaki 51 fazla anahtar artık çıkarıcının güncel seçkisinde yok; kullanılmadığı doğrulanmadan silinmemeli. Bu sonuç Oluşturucu'daki bütün İngilizcenin çevrildiğini kanıtlamaz: çıkarıcı ve `ALifeTR_Creator.lua` yalnızca yakaladığı metin yollarını kapsar.

## Lua taraması ve kaynak izleme

İlk otomatik taramada 17.195 ekran/metin çağrısı eşleşmesinden 5.373 benzersiz, teslim haritasında olmayan dize çıktı. İlk sınıflandırma şuydu:

| İlk otomatik sınıf | Aday |
|---|---:|
| Ses altyazısı | 2.998 |
| İç not / kimlik / günlük | 1.938 |
| Özel ad | 124 |
| Yönetici arayüzü | 5 |
| Oyuncu arayüzü | 24 |
| Belirsiz | 284 |

Sonraki kaynak yolu incelemesi; telefon tablolarını, görev ekranı metinlerini ve görev konuşmalarını doğrulayıp döküme ekledi. Bir yorum satırından gelen `yellow toast` hatalı eşleşmesi çıkarıldı; `talk closed why=` günlük satırı olarak sınıflandırıldı; Lua tablo anahtarları olan `abandoned` ve `party_fail` metin sayımından çıkarıldı. Genişletilmiş JSON'da 5.662 benzersiz kayıt var. Bu sayı çeviri satırı sayısı değildir; etkin olmayan ses metinlerini, özel adları, 46 belirsiz kaydı, yalnızca geliştirici önizleme başlıklarını ve çevrilmesi gereken metin/kalıp kayıtlarını birlikte içerir.

| Genişletilmiş sınıf | Kayıt | Değerlendirme |
|---|---:|---|
| Ses altyazısı | 2.998 | Bu kaynakta `npcAudioEnabled = false`; etkin değil. |
| İç not / kimlik / günlük | 1.939 | Oyuncuya gösterildiği doğrulanmadı; `talk closed why=` günlük metnidir. |
| Özel ad | 124 | Düz metin, çeviri adayı değil. |
| Yönetici arayüzü | 5 | Yönetici/QA görünümü. |
| Ek oyuncu arayüzü | 23 | Ekran metni; kaynak yolu ham dökümde. |
| Telefon konuşması / seçenek / sonuç | 406 | `P.line -> Text.ui` çağrı yolu doğrulandı; 408 kalıbın 2 anahtarı teslimde var. |
| Telefon arayan etiketi | 10 | Çağrı ekranında `ask.name` olarak gösteriliyor; `Text.ui` yolunu atlıyor. |
| Geliştirici önizleme başlığı | 10 | Yalnızca telefon diyalog önizleme menüsünde kullanılıyor. |
| Görev ekranı arayüzü | 18 | Eksik sabit/yer tutuculu `Text.ui` anahtarları. |
| Görev kartı metni | 3 | Kaynakta eksik anahtar; kart veya ayrıntıda gösteriliyor. |
| Görev sonucu metni | 7 | Görev bildiriminde kullanılan eksik metinler. |
| Görev teklifi seçenekleri | 14 | 16 metinden 14'ünün `RadioData` anahtarı eksik. |
| Görev veren NPC replikaları | 45 | İncelenen `RadioData` anahtarlarının tamamı eksik. |
| Görev metin kalıpları | 6 | Sayı/kişi bilgisi sonradan ekleniyor; kalıp uyarlaması gerekir. |
| Konuşma ağacı bildirimleri | 8 | `treeNote` alıcısında doğrudan gösteriliyor; `Text.ui` yok. |
| Belirsiz | 46 | Otomatik sınıflandırma yetmiyor; ayrıca kaynak yolu incelemesi gerekir. |

### Telefon görüşmesi ekranı

Telefon ağacındaki konuşmacı satırları, oyuncu yanıtları, kısa karşılıklar ve sonuç bildirimleri `ALifePhonesClient.lua` içindeki `P.line` üzerinden `ProjectALife.Text.ui(raw)` çağrısına gidiyor. 408 farklı metin kalıbından yalnızca ikisinin teslim anahtarı var; **406'sı çevrilmemiş**. Buna `Text.ui`'ye uğramadan çağrı adına konan **10 arayan etiketi** ekleniyor. Telefon ekranı için bulunan toplam **416 metin/etiket** bu.

`lua_cikar.py` bu konuşmaları bulmuyor; kaynak değerleri `ALifePhonesData.lua`'da, `Text.ui` çağrısı başka dosyadaki `P.line` içinde. Güvenli çıkarım, her Lua dizesini çevirmeye çalışmak değil; yalnızca `say`, `label`, `reply`, `impact` alanlarını bu çağrı yoluna bağlayan açık bir kaynak kuralı eklemek.

406 metin 50 satır sınırını aşıyor ve büyük bölümü karakter repliği; K38 gereği Fable akışında hazırlanmalı. K61 istisnası uygulanamaz. Çeviride `{lost}`, `{you}`, `{he}`, `{He}`, `{him}`, `{his}` yer tutucuları korunmalı. Ayrıca `Phones.fill` şu anda zamir yer tutucularını İngilizce değerlerle değiştiriyor (`he/she`, `him/her`); sadece Türkçe JSON satırları eklemek bazı cümlelerde İngilizce bırakır. Teslim öncesi yalnızca telefon doldurma yolunu etkileyen Türkçe zamir uyarlaması ve değişken kişi adlarının Türkçe cümlede doğal kullanımı çözülmeli.

### Görev alma, görev günlüğü ve bildirimler

Görevle ilgili **101 eksik metin/kalıp** sayılabildi:

- NPC görev verenin **45 repliği** ve **14 oyuncu yanıtı** (`RadioData` anahtarları eksik). Diğer 2 yanıt metni mevcut; 16 görev satırı ipucunun tamamı teslim haritasında.
- Görev günlüğü/başlık/etiket ekranında **18 eksik `Text.ui` girdisi** ve görev kartı verisinde **3 eksik metin**.
- Görev sonucu bildirimlerinde **7 sabit eksik metin**.
- Sayı veya kişi adı sonradan eklenen **6 kalıp** (ör. `Handed in {have} of {need}`, `For {who}`, `Talk to {who}`, süre bilgisi).
- Konuşma ağacı üzerinden gelen **8 `treeNote` bildirimi**; sunucudan gelen metin istemcide `Notice.line`/halo ile doğrudan gösteriliyor, `Text.ui` çağrısı yok.

Sabit görev metinleri `M.text(...)` üzerinden `Text.ui`'ye gittiği için eksik hash anahtarlarıyla çevrilebilir. Dinamik sayı/kişi metinlerinde her olası metni ayrı anahtarla çevirmek yerine görev metnine sınırlı kalıp eşlemesi gerekir. `treeNote` ise ayrı bir alıcı yolu olduğundan görev kartı çevirileri onu kapsamaz. Kaynakta bulunan `Report back to the one who asked`, kullanılan kısa `Report back` metninin anahtarı değildir.

45 NPC repliği ve 14 oyuncu yanıtı görev verenle konuşma ekranında görünür; bunlar da diyalog olduğundan Fable akışında hazırlanmalı. 18 arayüz girdisi, 3 kart metni, 7 bildirim ve 6 kalıp ayrı `IG_UI` kapsamıdır.

### A-Life Oluşturucu / oyuncu karakteri oluşturma

A-Life'ın kendi Oluşturucusu, Project Zomboid'in oyuncu karakteri oluşturma ekranı değildir; NPC ve fraksiyon düzenleme ekranıdır. Kullanıcının kastı vanilla oyuncu oluşturma ekranıysa bu modun `Text.ui`/Creator yolu onu kapsamaz.

A-Life Oluşturucusu için güncel çıkarıcının bulduğu 1.838 anahtarın teslimde olması, kullanıcıya görünen her durumun Türkçe olduğu anlamına gelmiyor. Güncel kaynakta çıkarıcı/kanca sınırında kalan örnekler:

- `ALifeCreatorCore.lua` içindeki silme ve fraksiyon sıfırlama `ISModalDialog` pencereleri; modal ayrı `UIManager` penceresi olduğu için Creator ana penceresini gezen kancanın dışında kalabiliyor. Çıkarıcı silme/onay metinlerini açıkça hariç tutuyor.
- Klasör silme sorusu, klasör adı ve NPC/fraksiyon sayısıyla çalışma anında birleştiriliyor.
- `Creator.checkNumberRule` boş alan, sayı aralığı ve alt/üst değer hatalarını dinamik metin olarak üretiyor (`enter a value.`, `use whole numbers ...`, `maximum must be at least the minimum.`); alan adlarıyla birleştirilmiş biçim sabit anahtar listesine girmiyor.
- Paylaşılan fraksiyonda eksik mod/eşya listesini anlatan ayrı onay penceresi ve bazı durum etiketleri başka fonksiyonlardan oluşturuluyor.

Bunların tam sayısı çıkarılmadı; her birinin gerçek kullanıcı oturumunda görünmesi ayrıca doğrulanmalı. Bütün `ISModalDialog` sınıfını küresel çevirmek yerine A-Life'ın kendi pencere açma noktaları hedeflenmeli.

### Tanıtım görselleri

Görsel dosyasının içine yazılmış İngilizce, Lua/JSON çıkarımının dışında kalır. Görsel metinsiz kaynak dosyadan yeniden hazırlanmalı ya da oyunu Türkçe açıp ekran görüntüsü yeniden alınmalı. Bu ayrı medya işidir; sayısal döküme dahil değil.

## Sayıların özeti

Şu an **540 metin/kalıp birimi** kaynak yolu veya doğrudan ekran çağrısıyla sayılabildi: **416 telefon metni/etiketi + 101 görev metni/kalıbı + 23 ek oyuncu arayüzü adayı**. Bu tam proje toplamı değildir: Creator pencerelerinin kalan kapsamı çıkarılmadı, 46 kayıt belirsiz, promosyon görselleri sayılmadı. Ayrıca 5.662 ham JSON kaydının tamamı çevrilecek metin değildir.

## Güvenli uygulama sırası

1. Görev ekranı ve görev veren konuşmaları için 101 girdiyi sabit, diyalog ve dinamik kalıp olarak ayırıp kaynak bağlamıyla hazırlamak.
2. Telefon ağacı için çıkarım kuralını ekleyip 406 eksik metni bağlamlarıyla Fable girdisine hazırlamak; yer tutucu koruması ve Türkçe zamir doldurma uyarlamasını birlikte çözmek.
3. A-Life Oluşturucusu için modal, dinamik doğrulama ve birleştirilmiş durum metinlerini çağrı yeriyle eşleştirmek; vanilla oyuncu karakteri ekranını A-Life'dan ayrı tutmak.
4. Her paket için anahtar/yer tutucu denetimi ve oyunda ilgili ekran doğrulaması yapmak. `son_kontrol` olmadan ana dosyalara, teslim paketine veya Workshop hazırlığına aktarmamak.
5. Tanıtım görsellerini koddan ayrı medya olarak incelemek.

**Yapılmayanlar:** Türkçe metin yazılmadı; `kaynak/`, `onayli/`, `teslim/`, Workshop hazırlık paketi ve ana mod kaynakları değiştirilmedi. Oyun içi test çalıştırılmadı.