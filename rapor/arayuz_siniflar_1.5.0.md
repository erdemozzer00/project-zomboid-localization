# IG_UI 1.5.0 kalan metinlerin sınıfı (1909 metin)

Üretici: `araclar/arayuz_sinif.py` (salt okuma). Ayrıntı: `rapor/arayuz_siniflar_1.5.0.json`.

| Sınıf | Metin |
|---|---:|
| a — diyalog (Gemini, Y3) | 303 |
| b — arayüz (Claude, B paketleri) | 1599 |
| c — oyunda görünmeyen | 7 |

## Alt sınıflar

| Sınıf | Alt | Metin |
|---|---|---:|
| a | npc_soz | 68 |
| a | oyuncu_satiri | 188 |
| a | yazili_not | 47 |
| b | arayüz | 1499 |
| b | ipucu | 7 |
| b | oluşturucu/ayar verisi | 93 |
| c | belirsiz | 6 |
| c | kesin | 1 |

## b sınıfı konular

| Konu | Metin |
|---|---:|
| Yönetici ve geliştirici | 323 |
| Baskın kartı | 181 |
| Konuşma arayüzü | 168 |
| Yoldaş sayfası | 150 |
| Görevler | 123 |
| Oluşturucu | 119 |
| Bitiş ekranı ve jenerik | 115 |
| İtibar sekmesi | 103 |
| Dünya olayları ve bildirimler | 93 |
| Başlangıç, günlük ve bildirimler | 93 |
| Harita ipuçları | 91 |
| Sürüş | 31 |
| Diğer | 9 |

## Oyunda görünür mü? (kod okuması, oyunda denenmedi)

Metin kaynak klasörüne göre dağılımı (client/shared/server). Görünürlük kuralları:

- `Text.ui` istemcide (client) çalışır: IG_UI.json'daki Türkçe tek oyuncuda da özel sunucuda da görünür.
- `Text.forPlayer` sunucuda (`isServer()`) İngilizce metni doldurur, tek oyuncuda `Text.ui`'ye düşer: **özel sunucuda sunucunun diliyle gider**; NPC sözüyse istemcide `AudioPolicy.caption` → konuşma eki yalnız `RD_ALifeLine_` anahtarıyla çevirir (IG_UI çevirisi o yolda kullanılmaz).
- Bu yüzden a sınıfındaki NPC sözleri/notlar/anıt yazıları tek oyuncuda IG_UI çevirisiyle görünür; özel sunucuda ancak aynı Türkçe `RD_ALifeLine_` anahtarıyla da teslim edilirse (K52'deki 'ikinci anahtar' ekiyle, kalan iş sırası madde 6) görünür.
- a/oyuncu_satiri menü düğmesidir (istemci `Text.ui`): her iki durumda görünür; oyuncu söyleyince çıkan söz ayrı yoldan (`RD_ALifeLine_`) gider.
- b sınıfında client/ klasöründekiler her durumda görünür; shared/ ve server/ olanlar (görev panosu, baskın kartı, ipuçları) çoğunlukla `Text.msg` ile istemciye anahtarıyla gidip istemcide `Text.show` ile çevrilir, ama bu tek tek doğrulanmadı.
- c sınıfı (7): `Text.ui`/`forPlayer` çağrısında geçmeyen tekil sözcük ya da eşleştirme anahtarı; çevirmeye değmez.

| Sınıf | Dağılım |
|---|---|
| a/npc_soz | shared 48, server 19, Lua dışı veri 1 |
| a/oyuncu_satiri | shared 167, client 11, server 7, Lua dışı veri 3 |
| a/yazili_not | shared 47 |
| b | shared 785, client 701, Lua dışı veri 100, server 13 |
| c | shared 7 |
