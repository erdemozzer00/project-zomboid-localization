# Fable istemi — Y4 konuşma ağaçlarını yeniden çevir

Bu, önceden çevrilip oyuna alınmış Y4 konuşma ağacı satırlarının yeni turudur. Kaynak ve sahne bağlamı Project A-Life 1.5.2'den yeniden çıkarıldı. `Y4R_1.txt`–`Y4R_96.txt` dosyalarının tamamı birlikte 12.785 çevrilecek satır içerir.

`gemini/alife-ceviri/SKILL.md`, `gemini/alife-ceviri/YER_TUTUCULAR.md`, `notlar/SOZLUK.md`, `notlar/KARARLAR.md` ve `notlar/YERELLESTIRME_REHBERI.md` dosyalarını bağlayıcı kabul et. Özellikle ağaç diyaloglarında kimin konuştuğunu, oyuncu seçeneği ile NPC cevabını ve her ağacın sahnesini ayırt et. Doğal, konuşulur Türkçe yaz; birebir çeviri yapma. Kaynaktaki olguları, özel adları ve yer tutucuları koru.

Her `Y4R_N.txt` için karşılığında `Y4R_N.txt` adlı çıktı ver. Yalnızca numaralı satırları çevir; `·` ile başlayan satırlar bağlam içindir ve çıktıya girmez. Her numarayı tam bir kez ve sırasını koruyarak `N | Türkçe` biçiminde yaz. Satır atlama, birleştirme veya yeni satır ekleme. Dosyaları parça parça yanıtlayabilirsin; her yanıtta hangi girdi dosyalarının tamamlandığını belirt ve bir dosyanın bütün satırları bittiğinde o dosyanın çıktı metnini eksiksiz ver.

Bu aşamada dosyalara veya projeye yazma; yalnızca çıktı metinlerini üret. Eski Türkçe karşılıklar girdiye konmadı, çeviriyi İngilizce kaynak ve sahne bağlamından kur.
