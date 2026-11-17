# Fable istemi — eski Y paketlerini sıfırdan yeniden çevir

Bu, Project A-Life 1.5.0 döneminde çevrilip oyuna alınmış Y serisi metinlerinin Fable turudur. Eski Y4 paketi 12.785 satırla Y4R olarak tamamlandı; bu dosya yalnızca kalan **5.406 satırı** kapsar. Eski Türkçe karşılıklar girdilere bilerek konmadı.

**Fable bu workspace'i ve buradaki dosya yollarını göremez.** Her dosya için açtığın Fable sohbetine şu dört dosyayı gerçekten ekle: `gemini/alife-ceviri/SKILL.md`, `notlar/SOZLUK.md`, `gemini/alife-ceviri/YER_TUTUCULAR.md` ve çevireceğin tek Y girdisi (ör. `Y1R_1.txt` veya `Y1SR_1.txt`). Skill yüklü olsa bile sözlük ve yer tutucuların ekli olduğunu kontrol et. Bir ek ulaşmadıysa onu okumuş gibi davranma; çeviriye başlamadan eksik eki belirt. Girdi içindeki başlık, `NEREDE`, sahne notları, etiketler ve dosyaya özel `TERİMLER` de o dosyayla birlikte Fable'a ulaşır.

Her girdi dosyasını Fable 5.2'de ayrı bir sohbette işle. Girdi `gemini/yeni/girdi/`, çıktı aynı adla `gemini/yeni/cikti/` içine kaydedilir. Yeni 23 parça başlık/olay sınırlarında bölündü: Y1R parçaları 334–343 satır, Y2R ise olayları bölmeden 300 ve 245 satırdır. Paket toplamı 300'ün altındaysa tek, doğal paket halinde kalır.

## Paketler

| Paket | Satır | Dosya | Oyundaki yeri / içerik |
|---|---:|---:|---|
| Y1R | 2.702 | 8 | NPC konuşmaları ve kısa sözleri; karşılaşma, kapı ve diğer sahneler |
| Y1SR | 6 | 1 | Sahneye bağlı NPC sözleri |
| Y2R | 545 | 2 | Radyo olayları ve telsiz sohbeti |
| Y3R | 303 | 1 | Oyuncu seçenekleri/görev soruları, NPC'nin hava-söylenti-kayıp eşya sözleri, el yazısı notlar ve anıt yazıları |
| Y5R | 159 | 1 | Konuşma penceresi sekmeleri, soru düğmeleri ve kısa açıklamalar |
| Y6R | 219 | 1 | Konuşma penceresinde kaçırılmış seçenekler ve alt notlar: durum, esir, Dell'in çantaları, bitiş telsiz/helikopter soruları |
| Y7R | 264 | 1 | Karşılaşma ve durum cevapları, esir cevapları, bitiş telsiz çağrısı |
| Y8R | 243 | 1 | Baskın kartı gözcü sözleri/etiketleri ve bitiş anlatısı |
| Y9R | 28 | 1 | Bitiş telsiz kartının giriş sözleri ve helikopter pilotunun sözleri |
| Y10R | 240 | 1 | Yol arkadaşı sayfası ve harita ipuçları |
| Y11R | 76 | 1 | İlan panosu, radyo ve dünya olayı bildirimleri |
| Y12R | 117 | 1 | Oluşturucu ekranı ve ayar ipuçları |
| Y13R | 156 | 1 | Oluşturucu ekranının sabit yazıları |
| Y14R | 261 | 1 | İtibar, başlangıç, günlük, sürüş, bitiş ve jenerik ekranları |
| Y15R | 87 | 1 | Ayarlar, görev aşamaları ve emir çarkı |

## Diyalog paketleri: Y1R–Y3R, Y5R–Y9R ve Y1SR

Her başlığın altındaki `NEREDE`, `SAHNE`, `KİM`, olay ve etiket bilgilerini oku. Her satırı bağlama göre doğal Türkçe diyalog olarak yeniden kur; İngilizce cümle iskeletini taşıma. Kaynaktaki olguları, karakter adlarını, özel adları ve yer tutucuları koru. `·` ile başlayan numarasız satırlar bağlamdır: çevirme ve çıktıya yazma. Girdinin kendi satır biçimi ve başındaki özel kurallar da geçerlidir. Satır etiketleri (`reg`, `faction`, `role`, `st`, `tmp`, `mood`, `rep`, `sex`, `psex`, `fact`, `day`, `hour`, `world`, `wp`, `grp`, `cb`, `wd`) ile sahne başlığındaki `r1/r2/r3` gibi alanlar skill'de açıklandığı ölçüde bağlam ipucudur; etiketi çıktıya yazma, anlamı belirsiz olandan yeni bilgi çıkarma.

Kullanılacak istem:

```text
Ekteki diyalog setini alife-ceviri skill'ine göre İngilizceden sıfırdan Türkçe kur. Eski Türkçe çeviriler girdide özellikle gösterilmiyor. Önce dosyanın başındaki kuralları; sonra her başlığın altındaki NEREDE, SAHNE, KİM, olay notları ve etiketleri oku. Her satırı o kişinin o sahnede Türkçe ağzından doğalca çıkacak biçimde yaz; İngilizcenin cümle iskeletini izleme. Kaynaktaki anlamı, oyun bilgilerini, özel adları ve yer tutucuları koru. `·` ile başlayan numarasız satırlar yalnızca bağlamdır; çevirme ve çıktıya yazma. Girdideki başlık/etiket biçimi ve diğer özel kurallar bağlayıcıdır.

Çıktı: yalnızca numaralı satırlar; her numara tam bir kez ve sırayla `N | Türkçe` biçiminde, tek kod bloğunda. Başlıkları ve etiketleri yazma. Kod bloğunun dışında yalnızca `Son numara: N` yaz.
```

## Arayüz paketleri: Y10R–Y15R

Her dosyanın başındaki ARAYÜZ kuralları, her başlığın `EKRAN` notu ve dosyaya özel `TERİMLER` listesi bağlayıcıdır; genel sözlükteki karşılıklarla açıkça çelişirse bunu bildir. Sahne/karakter canlandırması yapma. Eski Türkçe karşılıklar girdide yok; İngilizceden baştan çevir. Başlıkları, `ui`/`tip` gibi etiketleri ve notları çıktıya yazma. Yer tutucuları, `%%`, `%1`, `\n`, etiketleri, renk kodlarını, büyük-küçük harf kuralını, noktalama ve boşluk talimatlarını her girdinin belirttiği şekilde koru.

Kullanılacak istem:

```text
Ekteki arayüz dosyasını alife-ceviri skill'inin Arayüz bölümüne göre baştan çevir. Eski Türkçe karşılıklar girdide bilerek gösterilmiyor. Dosyanın başındaki ARAYÜZ kurallarını, her başlığın EKRAN notunu ve TERİMLER listesini uygula; arayüz metnini kısa, açık ve tutarlı yaz. Başlıkları, etiketleri ve notları çıktıya yazma. Yer tutucuları, renk kodlarını, özel adları, boşluk ve noktalama kurallarını girdide belirtildiği gibi koru.

Çıktı: her numara için tam bir satır, `N | Türkçe`, tek kod bloğunda ve sırası değişmeden. Kod bloğunun dışında yalnızca `Son numara: N` yaz.
```

## Çıktıları getirme

Bir paketin bütün parçaları tamamlanınca `python -X utf8 araclar/harici_paket.py al Y5R --yeni` biçiminde, paket adını ver. Ardından `paket_kontrol <paket>` çalıştırılır; tüm paketler hazır olunca teknik sonuçlar tek özetle sunulur ve ana çevirilere aktarım için tek onay beklenir. Bu hazırlık, hiçbir çeviriyi `onayli/` veya teslim dosyalarına kendiliğinden aktarmaz.
