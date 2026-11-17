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
- `gemini/` + `araclar/harici_paket.py`: diyalog çevirisi Gemini'de yapılır (K38). `gemini/alife-ceviri/SKILL.md` kurallar (Gemini skill'i), `gemini/girdi/` Codex'un hazırladığı numaralı İngilizce, `gemini/cikti/` kullanıcının getirdiği Türkçe, `gemini/sahne/` sahne notları, `gemini/NASIL_KULLANILIR.md` ve `gemini/PROMPTLAR.md` kullanıcı için

## Kurallar
- Diyalogları varsayılan olarak Codex çevirmez (K38; Fable 5.2 akışı). **K61 istisnası:** Bir mod güncellemesindeki toplam yeni çevrilecek metin 50 satır veya azsa Codex, `gemini/alife-ceviri/SKILL.md` ve geçerli arayüz/diyalog kurallarıyla taslak çevirir; kullanıcı inceleyip açıkça onaylamadan pakete veya ana dosyalara aktarmaz. 50 satırı aşan yeni metinler Fable akışında kalır; eski G serileri küçük parçalara ayrılarak bu istisnaya sokulmaz. Diğer paketlerde Codex girdiyi hazırlar, çıktıyı alır, teknik kontrol ve toplu özet yapar. Rehber, sözlük ya da kararlar değişirse skill'i de güncelle. G4+M2 için koşullu ön yetki K60'ta kayıtlıdır.
- Yapımcı/kurulu modun kaynak dosyalarına dokunma. `kaynak/en` sürüm tabanı, yalnızca kaydedilmiş resmi EN kaynağından güncellenir. Hiçbir şeyi kullanıcı onayı olmadan birleştirme; yalnızca açıkça belgelenmiş kapsamlı ön yetki varsa o kapsamda uygula (G4+M2: K60).
- `harici_paket.py al`, hedef `_lua` ise eksik EN anahtarlarını ve bağlamlarını türetilmiş `kaynak/<dosya>.json` / `_baglam.json` haritalarına ekler. Bu davranışı kontrol et; kurulu modun Lua dosyalarını değiştirme.
- Anahtarlara, `{yer_tutucu}`, `%%`, `\n` dizilerine dokunma.
- Kullanıcının mevcut çevirilerinde zayıf yer görürsen gerekçesiyle öner, kendiliğinden değiştirme.
- NPC diyaloglarında K33 ve yerelleştirme rehberini uygula; kaynak ve gerçek oyun bağlamının desteklemediği ayrıntı ekleme.
- Codex bir diyalog satırı yazarsa (ör. teknik düzeltme) **birebir çeviri yapma** (K36): her satırı önce sahnede o karakter söylüyormuş gibi düşün, Türkçesini yerelleştir, sesli oku. "Hiçbir Türk böyle konuşmaz" dediğin çeviriyi düzelt. `paket_kontrol` temiz olması Türkçenin doğru olduğunu göstermez; araç uyarısı yüzünden doğru çoğulu/ifadeyi bozma, istisna ve gerekçe yaz. Ayrıntı: rehberdeki "Her satırdan önce zorunlu süreç".
- Atölye akışı: kullanıcı onayı veya belgelenmiş koşullu ön yetki ve temiz `son_kontrol` sonrasında `araclar/workshop_kur.py` yerel Workshop hazırlık klasörünü günceller. Bu betik Steam'e yayın yapmaz; eski hedef dosyalarını da otomatik temizlemez. Yayın öncesi paket içeriğini ve `modversion` değerini ayrıca kontrol et.
