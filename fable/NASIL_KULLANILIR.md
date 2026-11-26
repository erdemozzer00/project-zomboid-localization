# Fable çeviri akışı

1. Fable'a repo erişimi isteğe bağlıdır. Repo görünüyorsa önce [genel Türkçe yerelleştirme skill'ini](oyun-yerellestirme-tr/SKILL.md) oku. Verilen TXT tek başına da yeterlidir; dosya başındaki proje talimatlarını uygula.
2. Yalnızca Erdem'in o iş için verdiği paketi çevir. Depodaki örnekler ve tarihli arşivler iş kuyruğu değildir. [Örnek N153_2 girdisi](../notlar/arsiv/2026-11-23/fable-dosyalari/girdi/N153_2.txt) ile [onaylı çıktısı](../notlar/arsiv/2026-11-23/fable-dosyalari/cikti/N153_2.txt) biçim örneğidir.
3. Yeni ve yeniden çevrilecek paketler `fable/girdi/` içinde. Paket TXT olarak hazırlandıysa o dosyayı Fable'a yükle. Paket bir `SKILL.md` olarak hazırlandıysa o tek dosya İngilizce metni, bağlamı ve talimatları içerir.
4. Türkçe TXT'yi `fable/cikti/` içine koy. TXT girdisinde aynı dosya adını kullan. `SKILL.md` için dosya içinde yazan çıktı adını kullan. Örneğin `girdi/U2R/SKILL.md` için çıktı `cikti/U2R_1.txt`.
5. Paketin kodunu Erdem/Codex'e bildir. Codex çıktıyı teknik olarak kontrol eder. Erdem'in açık aktarım onayından sonra çeviri işlenir. Paket kapanınca Codex girdiyi ve varsa çıktıyı [tarihli arşive](../notlar/arsiv/) taşır.

`araclar/sahne/` paket hazırlama aracının bağlam notlarını içerir. Satır eşlemeleri `paketler/haritalar/<PAKET>_harita.json` dosyalarındadır. Açık işler [İlerleme](../notlar/ILERLEME.md) sayfasında listelenir; bu sayfa bile Fable'a verilmiş paket talimatının yerine geçmez.

## TXT dosyaları için ortak istem

> /oyun-yerellestirme-tr skill'ine uyarak ekteki TXT'yi çevir.
