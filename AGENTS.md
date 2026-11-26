# Project A-Life — Türkçe yerelleştirme

Project Zomboid Build 42 için Project A-Life Türkçe yaması. Ana modun Workshop ID'si `3803984183`, Türkçe yamanınki `3833513956`.

Erdem çeviriyi ayrı bir ortamda Fable 5.2 ile yapar. Codex bu çalışma alanında İngilizce girdiyi hazırlar, gelen Türkçeyi teknik olarak kontrol eder ve onayla işler. Erdem'in istediği rötuşları uygular. Yeni çeviriler, kısa arayüz metinleri dahil, Fable'da hazırlanır.

Her oturumun başında [İlerleme](notlar/ILERLEME.md), [Kararlar](notlar/KARARLAR.md), [Yerelleştirme rehberi](notlar/YERELLESTIRME_REHBERI.md) ve [Sözlük](notlar/SOZLUK.md) dosyalarını oku.

## Girdiyi hazırla

1. Oyuncuya görünen metni, oyun içindeki yerini ve anlamını doğrula. Resmî EN sürüm tabanı `kaynak/en/` dizinidir. Yalnızca doğrulanmış resmî EN kaynağından güncellenir. Kurulu modun özgün dosyaları, `yeni jsonlar/` ve eski `*-updated*.json` karşılaştırma dosyaları salt okunur kullanılır.
2. Yeni metinler ve yeniden çeviriler için tek girdi dizini `fable/girdi/`. İngilizceyi paket koduyla başlayan numaralı TXT olarak hazırla. Erdem tek `SKILL.md` istediğinde talimatları, bağlamı, numaralı İngilizceyi ve çıktı dosya adını `fable/girdi/<PAKET>/SKILL.md` içine koy. Sahneyi veya ekranı, kimin kime konuştuğunu, sabit karşılıkları ve özel yer tutucu kurallarını kaynakla doğrula. Çeviri gerektirmeyen bağlamı numarasız tut.
3. Fable yalnızca Erdem'in genel `oyun-yerellestirme-tr` skill'ini ve o sefer verilen girdiyi görür. Skill'in depoda tutulan kopyası `fable/oyun-yerellestirme-tr/SKILL.md`; Fable'a repo erişimi isteğe bağlıdır ve yalnızca verilen paket iş kuyruğudur. Repo bağlantıları için kök [README](README.md) kullanılır. Her parçayı tek başına kullanılabilir hazırla. Dosya başındaki `#` notlarında ilgili dünya ve ekran bilgisini, satır etiketlerinin anlamını, gereken onaylı karşılıkları ve çıktı adını ver. Sahneye özgü bilgiyi `##### ... #####` başlığının altına yaz. Oyuncu seçeneği ile NPC cevabının ilişkisini, sırayla söylenen sözleri ve rastgele seçilen alternatifleri kaynaktaki işleyişe göre belirt. Çevrilecek satır `N | etiket | İngilizce`, çıktı `N | Türkçe` biçimindedir.
4. Her yer tutucu için oyunun hangi değeri koyduğunu çağrı yerinden doğrula. Tekrarlanan `%s` gibi sıralı alanlarda her konumun anlamını ayrı ver. Girdide geçen özel dizilerin (`%%`, `\n` gibi) nasıl korunacağını ve varsa projeye özgü istisnaları açıkla. Kaynakta çözülemeyen anlamı tahmin etme, belirsizliği ilgili satırda belirt.
5. Teslimden önce Fable'a gidecek her dosyayı açıp bu bilgilerle okunabildiğini kontrol et. Hazırlama aracı eski bir skill'e, başka bir parçaya veya yerel bir dosyaya atıf bıraktıysa gereken bilgiyi o girdiye koy. Genel üslup kuralları skill'de bulunur. Projeye özgü kararları ilgili oldukları yerde uygula.

## Çıktıyı işle

1. Erdem Türkçe TXT'yi `fable/cikti/` içine koyar. TXT girdisinde dosya adı aynıdır. Tek `SKILL.md` girdisinde skill'in belirttiği çıktı adı kullanılır. [Kısa kullanım notu](fable/NASIL_KULLANILIR.md)
2. Dosyaların ve numaraların tamlığını, sırayı, anahtar ve hedef eşleşmesini, yer tutucuları, `%%` ve `\n` gibi özel dizileri doğrula. `paketler/haritalar/<PAKET>_harita.json` varsa `araclar/harici_paket.py al` ve ardından `araclar/paket_kontrol.py` kullan. `al`, Lua hedeflerinde eksik EN anahtarı ve bağlamı türetilmiş `kaynak/<hedef>.json` ve `kaynak/<hedef>_baglam.json` dosyalarına ekleyebilir. Aynı paket adını kullanmadan önce mevcut paketi ezme riskini kontrol et.
3. Teknik bulguları ve uygulanacak rötuşları tek özette göster. Oyuncu grubuna gerçek çoğul hitap gibi bilinçli kullanımları gerekçesiyle koru. Mevcut onaylı Türkçeyi veya Fable'ın metnini kendiliğinden yeniden yazma. Raporun sonucunu oku.
4. Erdem'in açık aktarım onayı ya da bu pakete özel belgelenmiş ön yetki varsa `onayla.py` ile işle. `son_kontrol.py` raporu temizse `workshop_kur.py` ile yerel Workshop paketini hazırla ve içeriği, sürümü, eski/fazla dosyaları karşılaştır. Steam yüklemesini Erdem yapar.
