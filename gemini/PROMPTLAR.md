# Çeviri istemleri (Fable 5.2 + `alife-ceviri` skill)

Her dosya için yeni sohbet: Fable 5.2, `/alife-ceviri` skill'i, girdi dosyası ve aşağıdaki ilgili istem. G1R/G1–G5/SB1 çıktıları `gemini/cikti/`; yeni mod güncellemesi M2/M3 çıktıları `gemini/yeni/cikti/` içine aynı adla kaydedilir (UTF-8).

K61 istisnası: Bir güncellemedeki toplam yeni çevrilecek metin 50 satır veya azsa Codex aynı skill ile kullanıcı incelemesi için taslak hazırlayabilir. M3'ün 14 satırlık taslakları çıktı klasöründedir; aşağıdaki M3 istemleri Fable'dan ayrıca çeviri istendiğinde kullanılabilir.

`gemini/girdi/` içindeki setler için istem:

| Girdi | Satır | İstem |
|---|---:|---|
| `G1R_1..35.txt` (G1 eski diyalogları, Fable yeniden çevirisi) | 12.335 | [G1R](#g1r) |
| `G2_143..156.txt` (G2'nin kalanı) | 1.780 | [G](#g-g2-g3-g4-g5) |
| `G3_1..22.txt` | 2.790 | [G](#g-g2-g3-g4-g5) |
| `G4_1..88.txt` | 11.233 | [G](#g-g2-g3-g4-g5) |
| `G5_1..22.txt` (kafa üstü yazılar, hiç yenilenmemişler) | 2.828 | [G](#g-g2-g3-g4-g5) |
| `SB1_1..9.txt` (ayar ekranı) | 1.469 | [SB1](#sb1-ayar-ekranı) |

`gemini/yeni/girdi/` içindeki yeni mod güncellemesi setleri (M2/M3 çıktıları `gemini/yeni/cikti/`):

| Girdi | Satır | İstem |
|---|---:|---|
| `M2a_1..3.txt` (arayüz, telsiz/telefon, ses ayarları) | 114 | [M2a](#m2a-arayüz) |
| `M2b_1..3.txt` (yeni Sandbox ayarları) | 124 | [M2b](#m2b-sandbox) |
| `M2c_1.txt` (eşya adları) | 2 | [M2c](#m2c-eşya-adları) |
| `M2d_1.txt` (önceden haritalanmış ağaç replikleri) | 3 | [M2d](#m2d-ağaç-replikleri) |

`gemini/yeni/girdi/` içindeki 1.5.2 güncelleme girdileri:

| Girdi | Satır | İstem |
|---|---:|---|
| `M3a_1.txt` (UI2 tracker kişi/konum metinleri) | 5 | [M3a](#m3a-ui2-tracker) |
| `M3b_1.txt` (yeni Sandbox ayarları + değişen ipucu) | 8 | [M3b](#m3b-sandbox) |
| `M3c_1.txt` (yönetici kaydetme bildirimi) | 1 | [M3c](#m3c-lua-arayüz-bildirimi) |

SB1 girdisindeki dört İngilizce satır, mod 1.5.2'de değiştiği için güncellendi (41, 687, 1075, 1076); numaralar aynı.

Yeni bir set gelirse (ya da bu liste değişirse) Codex bu tabloyu ve istemi birlikte günceller.

## Y1R–Y15R (Fable öncesi Y çevirileri)

Bu, Y4R'dan sonra kalan eski Y paketlerinin sıfırdan yeniden çevirisidir. Toplam 5.406 satır, 23 girdi parçası. Parçalar başlık/olay sınırlarında kuruldu; 300 satırdan küçük paketler başka içerikle birleştirilmeden tek parça bırakıldı. Çıktıları `gemini/yeni/cikti/` içine aynı adla kaydet. Y4R zaten tamamlandı ve bu kapsama dahil değil. Paket türüne göre ayrıntılı istem ve iş sırası: [`gemini/yeni/Y1R-Y15R_FABLE_ISTEMI.md`](yeni/Y1R-Y15R_FABLE_ISTEMI.md).

| Paket | Satır | Girdi parçaları | Kapsam |
|---|---:|---:|---|
| Y1R | 2.702 | 8 | NPC konuşmaları ve kısa sahne sözleri |
| Y1SR | 6 | 1 | Sahne sözleri |
| Y2R | 545 | 2 | Radyo olayları ve telsiz sohbeti |
| Y3R | 303 | 1 | Arayüz diyalogları, notlar ve anıtlar |
| Y5R | 159 | 1 | Konuşma penceresi düğmeleri ve kısa notları |
| Y6R | 219 | 1 | Konuşma seçenekleri ve alt notlar |
| Y7R | 264 | 1 | NPC durum/esir/telsiz cevapları |
| Y8R | 243 | 1 | Baskın kartı ve bitiş anlatısı |
| Y9R | 28 | 1 | Bitiş telsiz kartı ve pilot |
| Y10R | 240 | 1 | Yol arkadaşı sayfası ve harita ipuçları |
| Y11R | 76 | 1 | İlan panosu/radyo/dünya bildirimi |
| Y12R | 117 | 1 | Oluşturucu ve ayar ipuçları |
| Y13R | 156 | 1 | Oluşturucu sabit yazıları |
| Y14R | 261 | 1 | İtibar, başlangıç, günlük, sürüş ve bitiş ekranları |
| Y15R | 87 | 1 | Ayarlar, görev aşamaları ve emir çarkı |

Diyaloglar için istem set belgesindeki “Diyalog paketleri” metnidir; arayüzler için “Arayüz paketleri” metnidir. Eski Türkçe girdiye eklenmedi. `·` bağlam satırları çevrilmez ve çıktıya yazılmaz.

## G1R (G1 eski diyalogları, Fable ile yeniden çeviri)

G1R'nin 35 dosyasında 12.335 satır var: ilk 31 dosya kafa üstü sözler, son 4 dosya konuşma penceresi replikleri. Her dosya 300–400 satır. Güncel modda bulunmayan 342 eski anahtar çıkarıldı. Eski Türkçe karşılıklar girdide yok. Girdiler `gemini/girdi/`, Fable çıktıları aynı adla `gemini/cikti/` içindedir. Ayrıntılar ve kopyalanacak istem: [`G1R_FABLE_ISTEMI.md`](G1R_FABLE_ISTEMI.md).

```text
Ekteki G1R diyalog dosyasını güncel alife-ceviri skill'ine ve ekli proje kararları, yerelleştirme rehberi ve sözlüğe göre İngilizceden sıfırdan Türkçe kur. Eski Türkçe çeviriler girdide bilerek gösterilmiyor.

Önce dosyanın başındaki kuralları oku. Her ##### başlığında olay ve konuşanları; NEREDE, SAHNE ve koşul notlarını dikkate al. Her satırı, o kişinin o anda Türkçe ağzından çıkacak söz gibi kur. İngilizce cümle iskeletini taşıma. Kaynakta olmayan bilgi veya sahne ayrıntısı ekleme. Anlamı ve karakter sesini koru; satırları doğal, kısa ve oyunda okunur yaz. Kişi/yer adlarını ve yer tutucuları koru.

`#` ile başlayan bağlam notları çevrilmez ve çıktıya yazılmaz. Girdideki her numara için tam bir çıktı satırı ver; numaraları aynen ve sırayla kullan. Çıktı tek kod bloğunda `N | Türkçe` biçiminde olsun. Kod bloğunun dışına yalnızca `Son numara: N` yaz.
```

## G (G2, G3, G4, G5)

Eski bir çeviriyle oyunda duran diyalog satırlarının sıfırdan yeniden çevirisi. Her başlığın altında "NEREDE:" ve (varsa) olay notu var.

```
Ekteki dosyayı alife-ceviri skill'ine göre yaz.

Önce dosyanın başını ve her ##### başlığının altındaki "NEREDE:" ve olay notlarını oku. Sonra her satırı, o kişinin o anda Türkçe ağzından çıkacak sözle yaz; İngilizcenin iskeletini izleme. Skill'deki çıta tablosunun sağ sütunu gibi yaz.

Çıktı: girdideki her numara için tam bir satır, "N | Türkçe", tek kod bloğunda. Kod bloğunun dışına yalnızca en sonda "Son numara: N" yaz.
```

## SB1 (ayar ekranı)

Oyunun Sandbox ekranındaki Project A-Life ayarları: her ayar bir blok (ayar adı, ipucu, seçenekler). `·` ile başlayan satırlar senin kendi çevirin, çevrilmez.

```
Ekteki dosyayı alife-ceviri skill'ine göre yaz. Bu bir arayüz dosyası: oyunun ayar (Sandbox) ekranındaki Project A-Life seçenekleri. Şu anki Türkçesini beğenmedik, sıfırdan kur.

Önce dosyanın başındaki kuralları ve TERİMLER listesini, sonra her ##### bloğunu oku: bir blok tek bir ayardır (ayar adı, ipucu, seçenekler). Ayar adları kısa ve net olsun, ipuçları sade ve açık; aynı kavrama her yerde aynı sözcük. İpuçlarındaki "\n" satır sonudur, çıktıda da aynen "\n" (ters bölü ve n, iki karakter) kalsın; her satır tek satır olsun. Son satırdaki "Default X" → "Varsayılan: X"; X bir seçenek adıysa aynı bloktaki seçeneğin Türkçesiyle birebir aynı olsun. "·" satırlarını çevirme, çıktıya yazma.

Çıktı: girdideki her numara için tam bir satır, "N | Türkçe", tek kod bloğunda. Kod bloğunun dışına yalnızca en sonda "Son numara: N" yaz.
```

## M2a (1.5.2 arayüz metinleri)

Üç parça: genel ekran ve kullanım seçenekleri; telsiz/telefon; ses düzeyleri. `·` satırları onaylı çeviridir, aynen kullan ve çıktıya yazma.

```
Ekteki dosyayı alife-ceviri skill'ine göre yaz. Bu bir arayüz dosyasıdır; girdinin başındaki ARAYÜZ kuralları, EKRAN notları ve TERİMLER bağlayıcıdır. `·` ile başlayan onaylı çevirileri yeniden çevirme ve çıktıya yazma.

Çıktı: her çevrilecek numara için tam bir satır, “N | Türkçe”, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda “Son numara: N” yaz.
```

## M2b (1.5.2 yeni Sandbox ayarları)

Ayarlar, modun ayar sayfası ve tek tek seçenek bloklarına göre gruplandı. İpuçlarındaki `\\n` iki karakter olarak korunmalı; `Default` satırını `Varsayılan:` yap ve seçeneğe atfı aynı Türkçe karşılıkla tutarlı yaz.

```
Ekteki dosyayı alife-ceviri skill'ine göre yaz. Bu, Sandbox ayar ekranının 1.5.2 ile eklenen seçenekleridir. Dosya başındaki sabit karşılıkları ve TERİMLER listesini uygula; her ##### bloğu tek ayardır. Ayar adını kısa tut, ipucunu açık yaz. İpuçlarındaki “\\n” iki karakterli satır sonudur; çıktıda aynen koru. Varsayılan seçenek adlarını aynı bloktaki çevrilmiş seçenekle birebir eşleştir.

Çıktı: her numara için tam bir satır, “N | Türkçe”, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda “Son numara: N” yaz.
```

## M2c (eşya adları)

İki satırın İngilizcesi de `Cell Phone`; aynı çeviriyi kullan. Anahtarından hareketle “test” gibi ek bilgi üretme.

```
Ekteki iki envanter adını alife-ceviri skill'inin Arayüz dosyaları kurallarına göre çevir. İki satır da aynı İngilizce adı (“Cell Phone”) taşıyor; ikisine de aynı kısa Türkçe karşılığı ver. Kaynakta olmayan “test” gibi bir niteleme ekleme.

Çıktı: her numara için tam bir satır, “N | Türkçe”, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda “Son numara: N” yaz.
```

## M2d (önceden haritalanmış ağaç replikleri)

Bu üç metin 1.5.2 güncellemesiyle gelmedi; eski D12/D14 haritalarında kayıtlıydı ama çevirmene verilecek txt dosyaları yoktu. `NEREDE` notları üç farklı konuşma ağacındaki kullanımlarını gösterir.

```
Ekteki dosyayı alife-ceviri skill'inin diyalog kurallarına göre yaz. Her başlığı ve NEREDE notunu oku; aynı İngilizce ifade birden fazla ağaçta kullanılıyor, tek Türkçe karşılık bütün bağlamlara uysun. NPC cevabıyla OYUNCU SEÇENEĞİ etiketlerini ayırt et.

Çıktı: her numara için tam bir satır “N | Türkçe”, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda “Son numara: N” yaz.
```

## M3a (UI2 tracker)

Beş satırın ilki `Chevalier Cossette` araç model adıdır; aynen koruyup çıktıda da 1. satır olarak ver. Kalan dört tracker metnini çevir; `{name}`, `{dist}`, `{dir}` yer tutucularını aynen koru.

```
Ekteki UI2 tracker ekran metinlerini alife-ceviri skill'inin Arayüz bölümüne göre çevir. 1. satırdaki `Chevalier Cossette` özel araç model adıdır: İngilizcesini aynen bırak ve çıktıya `1 | Chevalier Cossette` olarak ekle. 2–5. satırları çevir; `{name}`, `{dist}` ve `{dir}` yer tutucularını yazımıyla birlikte aynen koru.

Çıktı: 1–5 arasındaki her numara için tam bir satır, `N | Türkçe`, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda `Son numara: 5` yaz.
```

## M3b (Sandbox)

Sekiz satır: yedi yeni ayar/seçenek metni ve anlamı değişmiş bir ipucu (8). Eski Türkçe yalnızca farkı gösterir; yeni İngilizce kaynak esastır. `\n` iki karakter olarak korunmalı. `Default By faction (1)` içindeki seçenek adı, 5. satırın Türkçesiyle birebir eşleşmeli.

```
Ekteki Sandbox ayarlarını alife-ceviri skill'inin Arayüz bölümüne göre çevir. Dosya başındaki ayar kurallarını, sabit karşılıkları ve TERİMLER listesini uygula. Her `#####` bloğu tek ayardır. 8. satırdaki eski Türkçe yalnızca değişikliği anlaman için verilmiştir; yeni İngilizce metni baştan çevir ve eski ifadeye bağlı kalma. İpuçlarındaki `\n` iki karakter olarak aynen korunsun. Varsayılanı `Varsayılan:` yap; `Default By faction (1)` satırındaki seçenek adı, 5. satırda çevirdiğin seçenekle birebir aynı olsun. Başlıkları, etiketleri ve `·` bağlam satırlarını çıktıya yazma.

Çıktı: 1–8 arasındaki her numara için tam bir satır, `N | Türkçe`, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda `Son numara: 8` yaz.
```

## M3c (Lua arayüz bildirimi)

Tek yönetici bildirimi; `{what}`, `{where}`, `{file}` yer tutucularını aynen koru.

```
Ekteki yönetici ekranı bildirimini alife-ceviri skill'inin Arayüz bölümüne göre çevir. `{what}`, `{where}` ve `{file}` yer tutucularının her birini aynen koru.

Çıktı: `1 | Türkçe` biçiminde tek satır, tek kod bloğunda. Kod bloğu dışında yalnızca en sonda `Son numara: 1` yaz.
```

## Yardımcı istemler (aynı sohbette)

**Yarıda kesildiyse:**

```
Kaldığın numaradan devam et. Aynı biçim, tek kod bloğu; önceki satırları tekrar etme. Sonda "Son numara: N" yaz.
```

**Satır atladıysa** (numaraları kendine göre yaz; gelen satırları çıktı dosyasının sonuna yapıştırman yeterli, sıra önemli değil):

```
Şu numaraları atlamışsın: 45, 46, 120. Yalnızca bu satırları aynı biçimde ("N | Türkçe") tek kod bloğunda ver.
```

**Çeviri birebir ya da yapay geldiyse:** önce bak: satırların çoğu noktasız bitiyor ve birimler çevrilmemişse skill o sohbette hiç uygulanmamıştır; bu istem işe yaramaz, yeni sohbet aç, skill'i seç, dosyayı yeniden gönder. Bu istem yalnızca skill'in çalıştığı ama tek tük satırın yapay kaldığı sohbetler için:

```
Bu satırlar çeviri gibi duruyor, Türkler böyle konuşmaz. Skill'in "Nasıl yazılır" ve "İki düşman" bölümlerine göre her satırı baştan yaz: sahneyi gör, İngilizceyi bırak, o adam Türk olsa ne derdi onu yaz; dublaj Türkçesi kalmasın. Anlam (olgu, iş, duruş) aynı kalsın, gerisinde serbestsin. Aynı biçimde tamamını tek kod bloğunda ver.
```

**Skill seçilemiyorsa:** `gemini/alife-ceviri/SKILL.md` (ve `YER_TUTUCULAR.md`) dosyalarını da ekle ve ilk istemin başına şunu yaz:

```
Ekteki SKILL.md dosyası çeviri kuralların; bu sohbet boyunca ona uy.
```
