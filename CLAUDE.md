# Project A-Life — Türkçe yerelleştirme

Project Zomboid modu Project A-Life'ın (Workshop 3803984183, Build 42) EN→TR yerelleştirmesi.

Her oturumda önce şunları oku, hafızaya güvenme:
- `notlar/KARARLAR.md` — verilmiş kararlar ve ton rehberi (bağlayıcı)
- `notlar/YERELLESTIRME_REHBERI.md` — diyaloglarda sahne, karakter sesi ve doğal Türkçe standardı (K33)
- `notlar/SOZLUK.md` — terim sözlüğü (bağlayıcı)
- `notlar/ILERLEME.md` — en üstteki "GÜNCEL DURUM" bölümü: nerede kaldık, sıradaki iş (altındaki tarihli kayıtlar geçmiştir)

## Dosyalar
- `*-updated.json` / `*-updated-translated.json`: eski EN ve kullanıcının TR çevirisi (temel, değiştirme)
- `yeni jsonlar/`: yapımcının gönderdiği yeni EN dosyaları (değiştirme)
- `araclar/karsilastir.py`: yeni EN'i temelle karşılaştırır, `rapor/` üretir
- `paketler/`: onaya sunulan çeviri paketleri
- `gemini/` + `araclar/harici_paket.py`: diyalog çevirisi Gemini'de yapılır (K38). `gemini/alife-ceviri/SKILL.md` kurallar (Gemini skill'i), `gemini/girdi/` Claude'un hazırladığı numaralı İngilizce, `gemini/cikti/` kullanıcının getirdiği Türkçe, `gemini/sahne/` sahne notları, `gemini/NASIL_KULLANILIR.md` ve `gemini/PROMPTLAR.md` kullanıcı için

## Kurallar
- Diyalogları Claude çevirmez (K38; çeviri kullanıcı tarafından Gemini/Fable'da `alife-ceviri` skill'iyle yapılır). Claude: girdiyi hazırlar, çıktıyı alır, yalnızca teknik kontrol yapar (kalite incelemesi yok), toplu özet + tek onayla işler. Rehber, sözlük ya da kararlar değişirse `gemini/alife-ceviri/SKILL.md`'yi de güncelle.
- Kaynak dosyalara dokunma; hiçbir şeyi kullanıcı onayı olmadan birleştirme.
- Anahtarlara, `{yer_tutucu}`, `%%`, `\n` dizilerine dokunma.
- Kullanıcının mevcut çevirilerinde zayıf yer görürsen gerekçesiyle öner, kendiliğinden değiştirme.
- NPC diyaloglarında K33 ve yerelleştirme rehberini uygula; kaynak ve gerçek oyun bağlamının desteklemediği ayrıntı ekleme.
- Claude bir diyalog satırı yazarsa (ör. teknik düzeltme) **birebir çeviri yapma** (K36): her satırı önce sahnede o karakter söylüyormuş gibi düşün, Türkçesini yerelleştir, sesli oku. "Hiçbir Türk böyle konuşmaz" dediğin çeviriyi düzelt. `paket_kontrol` temiz olması Türkçenin doğru olduğunu göstermez; araç uyarısı yüzünden doğru çoğulu/ifadeyi bozma, istisna ve gerekçe yaz. Ayrıntı: rehberdeki "Her satırdan önce zorunlu süreç".
