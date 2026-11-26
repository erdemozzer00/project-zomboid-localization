# Fable 5.2 — G1R yeniden çeviri

## Kapsam ve karar

G1, Fable 5.2 akışından önce çevrilmiş kafa üstü ve NPC diyalog satırlarının yeniden çevirisidir. Kayıtlar önceki üretimin Gemini ile yapıldığını güçlü biçimde destekliyor; her eski çıktı dosyasında model/skill bilgisi tutulmamış. Kullanıcı Fable'a güvendiği için pilot yapılmıyor; bütün güncel satırlar aynı akışla çevrilecek.

- **12.335 satır, 35 girdi dosyası:** `G1R_1`–`G1R_31` kafa üstü sözler; `G1R_32`–`G1R_35` konuşma penceresi replikleri. Her dosya 300–400 satır.
- İçerik karışık: 11.026 satır (~%89) kafa üstü kısa söz, 1.309 satır (~%11) konuşma penceresi repliğidir.
- Önceki G1 listesindeki **342 anahtar**, güncel modun 39 diyalog grubunda bulunmadığı için çıkarıldı.
- Girdilerde eski Türkçe yok; kaynak İngilizceden sıfırdan çeviri yapılacak.
- Fable çıktıları aynı adla `gemini/cikti/` içine kaydedilecek.
- G1 sahne notları her girdide kullanılmak üzere G1R kopyasına aktarıldı.

Önce `gemini/alife-ceviri/SKILL.md` ile `YER_TUTUCULAR.md` dosyalarını etkinleştir. Bağlayıcı kararlar ve Türkçe standardı: `notlar/KARARLAR.md`, `notlar/YERELLESTIRME_REHBERI.md`, `notlar/SOZLUK.md`.

## Her dosyada

1. Fable 5.2'de yeni sohbet aç; güncel `alife-ceviri` skill'ini, ilgili proje rehberlerini ve bir `G1R_N.txt` dosyasını ekle.
2. Aşağıdaki istemi gönder. Her `#####` başlığındaki olay, `NEREDE`, sahne ve koşul notlarını dikkate al.
3. Çıktıyı yalnızca numaralı Türkçe satırlar olarak, aynı dosya adıyla UTF-8 kaydet. Bir dosyada bütün numaralar bir kez ve sırayla bulunmalı.
4. Bir parçanın çevirisi tamamlanınca çıktı `gemini/cikti/G1R_N.txt` konumunda olmalı. Bütün parçalar tamamlanınca Codex'a **“G1R çıktıları hazır”** de.

## Fable istemi

```text
Ekteki G1R diyalog dosyasını güncel alife-ceviri skill'ine ve ekli proje kararları, yerelleştirme rehberi ve sözlüğe göre İngilizceden sıfırdan Türkçe kur. Eski Türkçe çeviriler girdide bilerek gösterilmiyor.

Önce dosyanın başındaki kuralları oku. Her ##### başlığında olay ve konuşanları; NEREDE, SAHNE ve koşul notlarını dikkate al. Her satırı, o kişinin o anda Türkçe ağzından çıkacak söz gibi kur. İngilizce cümle iskeletini taşıma. Kaynakta olmayan bilgi veya sahne ayrıntısı ekleme. Anlamı ve karakter sesini koru; satırları doğal, kısa ve oyunda okunur yaz. Kişi/yer adlarını ve yer tutucuları koru.

`#` ile başlayan bağlam notları çevrilmez ve çıktıya yazılmaz. Girdideki her numara için tam bir çıktı satırı ver; numaraları aynen ve sırayla kullan. Çıktı tek kod bloğunda `N | Türkçe` biçiminde olsun. Kod bloğunun dışına yalnızca `Son numara: N` yaz.
```

## Çıktı geldikten sonra

Çıktılar teknik olarak `al G1R` ve `paket_kontrol G1R` adımlarından geçirilecek. Ardından eksik/biçim/yer tutucu özeti sunulacak. Paket, kullanıcı açıkça onaylamadan `onayli/` dosyalarına aktarılmayacak.
