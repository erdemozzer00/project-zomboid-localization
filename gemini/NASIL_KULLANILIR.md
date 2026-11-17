# Fable 5.2 ile çeviri: nasıl kullanılır

> **Güncel akış:** Büyük çeviri paketlerini Fable 5.2 yapıyor. K61'e göre bir mod güncellemesindeki toplam yeni çevrilecek metin 50 satır veya azsa Codex, aynı skill'le kullanıcı incelemesi için taslak hazırlar. Fable'da kullanılacak istemler `gemini/PROMPTLAR.md`'dedir (G, SB1, M2 ve M3); aşağıdaki eski istem numaraları geçerli değildir.

> **2026-11-12 (K56): skill yeniden yazıldı (deneme kazananı B).** O tarihte skill `SKILL.md` ve `YER_TUTUCULAR.md` dosyalarından oluşuyordu. Güncel skill dosyaları `gemini/alife-ceviri/` altındadır; eski ZIP yükleme adımı geçerli değildir. İstem: `PROMPTLAR.md` 0. istem (G ve SN için iki ayrı metin).
>
> **2026-11-10 (K54): skill yeniden yazıldı.** Devam etmeden önce Gemini'deki (ve kullanıyorsan Claude'daki) `alife-ceviri` skill'ini güncel `gemini/alife-ceviri/SKILL.md` ile yeniden yükle. Yeni yön: anlam aynı kalır, söyleyiş serbest; dublaj Türkçesi yasak. İstemlerin numaraları aynı, metinleri güncellendi (`PROMPTLAR.md`).

> **2026-11-15: Codex devri.** Claude'un kullandığı paket/çıktı biçimi ve K38 akışı sürer. Güncel iş sırası `notlar/ILERLEME.md` başındadır. Codex çeviri kalitesini incelemez; teknik denetim yapar. G4+M2 için K60'ta kayıtlı koşullu yetki geçerlidir: tüm teknik kapılar temizse tekrar onay istemeden işler. `workshop_kur.py` yerel Workshop hazırlık klasörünü günceller; Steam'e yayınlamaz.

## Bir kez: kuralları skill olarak yükle

1. Fable 5.2'yi aç ve güncel `alife-ceviri` skill'ini etkinleştir.
2. Skill yüklü değilse `gemini/alife-ceviri/SKILL.md` dosyasını Fable'ın skill ekleme akışıyla yükle; yer tutucu dosyası `gemini/alife-ceviri/YER_TUTUCULAR.md`'dir.
3. Skill ekleme desteklenmiyorsa iki dosyayı da yeni sohbete ekleyip talimat olarak kullan.

## Her parça için

1. Fable 5.2'de yeni sohbet aç ve mevcut en güçlü modeli kullan.
2. Kutuya `/alife-ceviri` yaz ve skill'i seç (skill'siz kullanıyorsan `SKILL.md`'yi ekle). Aynı anda birkaç sohbet açıyorsan model ve skill'i her birinde ayrı ayrı kontrol et.
3. Girdi dosyasını ekle (ör. `gemini/girdi/D6n_1.txt`) ve `gemini/PROMPTLAR.md`'de o set için yazan istemi gönder.
4. Çıktı yarıda kesilirse 2. istemi, satır atladıysa 3. istemi kullan.
5. **Kaydetmeden önce 10 saniyelik kontrol:** (a) Satırların sonunda nokta, ünlem ya da soru işareti var mı? Çoğu satır noktasız bitiyorsa skill uygulanmamıştır ve çeviri birebirdir (SNE_5–19 böyle geldi). (b) Kaynakta feet, mile ya da derece varsa metreye, kilometreye, °C'ye çevrilmiş mi? (c) Birkaç satırı sesli oku. Kötüyse aynı sohbette düzelttirmeye çalışma: yeni sohbet aç, Pro + skill seç, dosyayı yeniden gönder. (Diyalog paketlerinde, haritada kapatılmadıysa ve en az 20 cümle varsa `al`, noktalama oranı %50'nin altındaki dosyayı varsayılan olarak reddeder; gerekirse `--zorla` kullanılır. Arayüz paketlerinin haritası bu eşiği kapatabilir.)
6. Çıktıyı kopyala, UTF-8 olarak kaydet. G1–G5/SB1 gibi mevcut paketlerde çıktı `gemini/cikti/` altına girdi adıyla; M2/M3 gibi yeni mod güncellemelerinde `gemini/yeni/cikti/` altına girdinin aynı adıyla kaydedilir. Birden çok mesajda geldiyse hepsini aynı dosyada birleştir.
7. Paketin bütün parçaları bitince Codex'a "D6n çıktısı hazır" de.

Her parça için ayrı sohbet aç; uzun sohbette model kuralları unutmaya başlar.

Bir paketin bütün parçalarını bitirmen gerekmez: bitirdiğin parçalar işlenir, kalanları sonra getirirsin. Yalnızca bir parçanın içi eksik olmasın (her numara bir kez).

## Eski Y çevirilerinin Fable turu (R)

Y1–Y15'in ilk çevirileri 9–10 Kasım 2026'da Gemini ile yapılmıştı; bu tarih Fable akışının projede kayda geçmesinden önce. Y4, 17 Kasım'da Y4R olarak yenilendi. Kalan **5.406 satır**, Y1R, Y1SR, Y2R, Y3R ve Y5R–Y15R paketlerine bölündü; girdiler `gemini/yeni/girdi/` içinde başlık/olay sınırlarına göre 23 parçaya düzenlendi, çıktılar aynı adla `gemini/yeni/cikti/` içindedir. Y1R parçaları 334–343 satırdır; Y2R 300 ve 245 satırdır, olaylar bölünmez. Toplamı 300'den az paketler tek parça kalır. Eski Türkçe değerler girdilere konmadı.

Fable 5.2'de `alife-ceviri` skill'ini kullan. Fable workspace'i ve yerel dosya yollarını göremez. **Her Y parçasının ayrı sohbetine** skill dosyasını, `notlar/SOZLUK.md`'nin ekli kopyasını `SOZLUK.md` adıyla, `gemini/alife-ceviri/YER_TUTUCULAR.md` dosyasını ve çevrilecek tek Y girdisini (ör. `Y1R_1.txt` veya `Y1SR_1.txt`) ekle. Bir ek görünmüyorsa Fable'dan okumuş gibi davranmamasını iste. Diyalog (Y1R–Y3R, Y5R–Y9R/Y1SR) ve arayüz (Y10R–Y15R) istemleri, paket listesi ve oyun içi yerleri [`gemini/yeni/Y1R-Y15R_FABLE_ISTEMI.md`](yeni/Y1R-Y15R_FABLE_ISTEMI.md) dosyasında. Bütün parçalar bitince örneğin `python -X utf8 araclar/harici_paket.py al Y5R --yeni`, ardından `python -X utf8 araclar/paket_kontrol.py Y5R` kullanılır. Önce teknik özet çıkarılır; çeviriler ana dosyalara aktarılmadan önce tek onay alınır.

## G1R — G1 eski diyaloglarının Fable turu

Kullanıcı Fable'a güvendiği için pilot yapılmıyor. Tam paket 12.335 satırdır; eski G1 listesindeki güncel modda bulunmayan 342 anahtar çıkarılmıştır. 35 dosya vardır: 31 kafa üstü, 4 konuşma penceresi; her biri 300–400 satır. Girdiler `gemini/girdi/G1R_1..35.txt`, çıktılar aynı adla `gemini/cikti/` içindedir. Eski Türkçe çeviriler girdiye eklenmedi.

`gemini/G1R_FABLE_ISTEMI.md` dosyasındaki skill/rehber adımlarını ve istemi kullan. Her girdi için ayrı sohbet aç; çıktıdaki numaraları sırayla ve eksiksiz koru. Tüm parçalar bitince “G1R çıktıları hazır” de. Codex teknik kontrol ve toplu özet yapacak; kullanıcı onayı gelmeden paket onaylı çevirilere aktarılmayacak.

## Yeni satırlar (mod 1.5.0) — Y1: 2.702 satır, 21 dosya + Y1S (6 sahne satırı)

Mod güncellemesiyle gelen, hiç çevrilmemiş satırlar ayrı klasörde: girdi `gemini/yeni/girdi/`, çıktı `gemini/yeni/cikti/`. G1 akışının aynısı: her dosya yeni sohbet, Pro, `/alife-ceviri`, `PROMPTLAR.md` **9. istem** (Y1S için 6. istem). Çıktıyı `gemini/yeni/cikti/Y1_N.txt` olarak kaydet. Getirdiğin kadarı işlenir; bir dosyanın içi eksik olmasın.

**Y2_1..4 (radyo olayları + telsiz sohbeti, 545 satır):** aynı akış, 9. istem + PROMPTLAR'daki Y2 ek cümlesi. Çıktı `gemini/yeni/cikti/Y2_N.txt`.

**Y4_1..96 (konuşma ağaçları, 12.785 satır) ve Y5_1..2 (ağaçların arayüzü, 159 satır):** 1.5.0'ın yeni konuşma penceresi (sorular, seçenekler, "Info"/"Trade" sekmeleri, NPC cevapları). Aynı akış: 9. istem + PROMPTLAR'daki Y4 (ya da Y5) ek cümlesi. Çıktı `gemini/yeni/cikti/Y4_N.txt` / `Y5_N.txt`. Her ağaç tek dosyada bütün; "·" ile başlayan satırlar bağlam, çıktıya yazılmaz.

**Y3_1..3 (arayüzden gelen diyalog, 303 satır):** oyuncu seçenekleri/görev soruları, NPC'nin hava-söylenti-kayıp eşya sözleri, el yazısı notlar ve anıt yazıları. Aynı akış: 9. istem + PROMPTLAR'daki Y3 ek cümlesi. Çıktı `gemini/yeni/cikti/Y3_N.txt`. Çeviri IG_UI'ye yazılır (Y2 gibi); `al Y3 --yeni` ve `paket_kontrol` hazır. Etiketler: OYUNCU SORUSU/SEÇENEĞİ/RAPORU, NPC, NOT.

**Y6_1..2 (kaçan konuşma satırları, 219 satır):** oyuncunun konuşma penceresinde seçtiği satırlar ve altlarındaki kısa notlar (durumlar, esir, Dell'in çantaları, bitiş telsiz çağrısı ve helikopter soruları). Aynı akış: 9. istem + PROMPTLAR'daki Y6 ek cümlesi. Çıktı `gemini/yeni/cikti/Y6_N.txt`. Çeviri `IG_UI_lua`'ya yazılır (Y5 gibi); `al Y6 --yeni` ve `paket_kontrol` hazır. Etiketler: OYUNCU SEÇENEĞİ, ALT NOT (sonuç/risk/ipucu), NPC (soru); "·" satırları bağlam.

**Y7_1..3 (durum, esir ve telsiz çağrısı sözleri, 264 satır):** NPC'lerin karşılaşma ve cevap sözleri (durumlar), esirin cevapları, bitiş telsiz çağrısında cevap şeridinin üstündeki soru. Aynı akış: 9. istem + PROMPTLAR'daki Y7 ek cümlesi. Çıktı `gemini/yeni/cikti/Y7_N.txt`. Çeviri `RadioData_lua`'ya yazılır (Y4 gibi); `al Y7 --yeni` ve `paket_kontrol` hazır. Etiketler: NPC (karşılaşınca/cevap), ESİR (grup · durum), TELSİZ; "·" satırları bağlam.

**Y9_1 (bitiş telsiz kartı ve helikopter pilotu, 28 satır):** ordunun telsiz kartında görünen ilk cümleler ve pilotun helikopterdeki sözleri. Aynı akış: 9. istem + PROMPTLAR'daki Y9 ek cümlesi. Çıktı `gemini/yeni/cikti/Y9_1.txt`. Çeviri `RadioData_lua`'ya yazılır; `al Y9 --yeni` ve `paket_kontrol` hazır. Etiketler: TELSİZ KARTI, PİLOT; "·" satırları bağlam. (Y8 adı RaidText'e ayrılı.)

**Y8_1..2 (baskın kartı gözcü cümleleri ve bitiş anlatısı, 243 satır):** baskın kartında çıkan kısa gözcü uyarıları (ses: çete, asker, kolluk, yerel halk), kartın etiketleri ve oyun sonunda akan bitiş hikâyesi. Normal diyalog akışı: 9. istem + PROMPTLAR'daki Y8 ek cümlesi. Çıktı `gemini/yeni/cikti/Y8_N.txt`. Çeviri IG_UI'ye yazılır; `al Y8 --yeni` ve `paket_kontrol` hazır.

**Y10–Y15 (arayüz dosyaları, 937 satır, 9 dosya; K53):** ekran metni: yoldaş sayfası ve harita ipuçları (Y10_1..2, 240), ilan panosu/radyo/dünya olayı bildirimleri (Y11_1, 76), Oluşturucu ekranı ve ayar ipuçları (Y12_1, 117), Oluşturucu sabit yazıları (Y13_1..2, 156), itibar/başlangıç/günlük/sürüş/bitiş ekranı/jenerik (Y14_1..2, 261), ayarlar/görev aşamaları/emir çarkı (Y15_1, 87). Akış: yeni sohbet, Fable 5.2, `PROMPTLAR.md` **10. istem** (9. istem değil) ve her Y sohbetinde yukarıda sayılan dört eki kullan. Arayüzde de skill'in arayüz ve yer tutucu kuralları geçerlidir; girdinin dosyaya özel ARAYÜZ kuralları, `TERİMLER` listesi ve her başlıktaki `EKRAN:` notu önceliklidir. Çıktıda `ui`, `tip` gibi etiketler olmasın ve numaralar tam olsun. Çıktı `gemini/yeni/cikti/Y10_1.txt` gibi, girdiyle aynı adla. Codex `al Y10 --yeni`, `paket_kontrol` ve terim uyarılarını özetle gösterir.

## M2 — 1.5.2 girdileri ve üç erişilemeyen ağaç repliği

Bu dosyalar `gemini/yeni/girdi/` içindedir. Her parça için Fable 5.2 ile yeni sohbet aç, `/alife-ceviri` skill'ini seç ve `PROMPTLAR.md` içindeki M2a, M2b, M2c ya da M2d istemini kullan. Çıktıyı aynı dosya adıyla `gemini/yeni/cikti/` içine kaydet.

- M2a: `M2a_1..3.txt`, 114 arayüz/telsiz/telefon/ses satırı.
- M2b: `M2b_1..3.txt`, 124 yeni Sandbox satırı.
- M2c: `M2c_1.txt`, 2 eşya adı; ikisi de “Cell Phone” olduğundan aynı Türkçe karşılığı kullan.
- M2d: `M2d_1.txt`, eski D12/D14 haritalarında olup girdi dosyası kalmamış 3 ağaç repliği. Bunlar 1.5.2'de eklenmedi; bağlamları dosyada verildi.

M2d satırları mevcut `kaynak/RadioData_lua.json` içinde yok. Çeviri çıktısını teknik olarak alabiliriz ama hedef anahtarlar ve oyundaki kaynak yolu doğrulanmadan onaylı dosyalara birleştirilmemeli.

`SB1_1..9.txt` içindeki 4 değişmiş Sandbox İngilizcesi 1.5.2'ye göre güncellendi. Çıktı geldikten sonra `al`/`paket_kontrol` aşamasından önce `kaynak/en/` 1.5.2'ye alınmalı; bunu yapmadan paketleri işleme.

## M3 — 1.5.2 güncellemesinden yeni arayüz metinleri

Bu girdiler `gemini/yeni/girdi/` içindedir. Toplam 14 satır olduğu için K61 uyarınca Codex skill'i uygulayıp inceleme taslaklarını `gemini/yeni/cikti/` içine yazdı. İstersen alternatif Fable çevirisi almak için her dosyayı ayrı Fable sohbetinde, ilgili M3 istemiyle de çevirebilirsin:

- M3a: `M3a_1.txt`, 5 UI2 tracker satırı. 1. satırdaki `Chevalier Cossette` özel araç adını aynen bırakıp çıktıya dahil et; `{name}`, `{dist}`, `{dir}` yer tutucularını koru.
- M3b: `M3b_1.txt`, 8 Sandbox satırı. Yedi yeni metin ve anlamı değişmiş bir ipucu var; eski Türkçe yalnızca karşılaştırma içindir. `\n` ve varsayılan seçenek eşleşmesini koru.
- M3c: `M3c_1.txt`, 1 yönetici bildirimi; `{what}`, `{where}`, `{file}` yer tutucularını koru.

Toplam 14 satırdır. Taslakların onaylanıp onaylanmadığı kullanıcıya bağlıdır; onay gelmeden paketlere aktarılmaz. Yeni sürümde diyalog girdisi çıkmadı; `ZombieHitFloor_tooltip` değişikliği yalnızca kaynak noktalaması olduğu için bu pakete alınmadı ve mevcut Türkçe anlamca hâlâ karşılıyor.

Üç çıktı da hazır olunca Codex'a “M3 çıktıları hazır” de. Paketler `al M3a --yeni`, `al M3b --yeni`, `al M3c --yeni` ile ayrı alınır; ardından her paket için teknik kontrol ve toplu özet yapılır.

## G1 (tamamlandı; K47 tarihsel kayıt) — Gemini öncesi diyalogların yeniden çevirisi

> Bu paket tamamlandı. Güncel Fable kuyruğu ve sıradaki iş için `notlar/ILERLEME.md` başındaki GÜNCEL DURUM bölümünü izle.

1. Bir kez: skill'i güncel `gemini/alife-ceviri/SKILL.md` ile yeniden yükle (eskisini sil ya da üzerine yükle).
2. Her dosya (`gemini/girdi/G1_1.txt` … `G1_100.txt`, 126–127 satır) için yeni sohbet, güçlü model (Pro ya da high thinking), `/alife-ceviri`, `PROMPTLAR.md` **7. istem**.
3. Çıktıyı `gemini/cikti/G1_N.txt` olarak kaydet (UTF-8). Hepsini bitirmen gerekmez; 20-30 dosya birikince Codex'a "G1 çıktıları hazır" de.

Senin kendi çevirdiğin ya da düzelttiğin 901 satır bu dosyalarda yok; onlara dokunulmaz.

## Sıra (K37) — sahneler: 100 dosya, 32.288 satır

Sahne dosyaları farklı biçimde: her sahne bir blok (`##### SAHNE ... #####`), satırlar `N | K1 | metin`, `·` ile başlayan satırlar numarasız bağlamdır. **Bu paketler için `PROMPTLAR.md` 5. istemi kullan.** Skill'i güncel (birleşik) sürümle yeniden yüklemek önerilir ama şart değil: her SN dosyasının başında sahne açıklaması var; Gemini'de senin sürümün çalışıyorsa yalnızca 3-4 kişilik sahnede hitap, `→` açıklaması ve "sonraki satırın vuruşunu çalma" cümlesi eksik kalır (`{sir}/{him}/{he}` kuralı sahnelerde gerekmez). Sahne parçalar arasında bölünmez (parça 300-330 satır).

| Sıra | Paket | İçerik | Satır | Dosyalar |
|---:|---|---|---:|---|
| 1 | SNA | Genel sahneler (any): gündelik sohbet, tartışma, anı | 16.738 | SNA_1–51 |
| 2 | SNB | Plan ve iş konuşmaları | 3.537 | SNB_1–11 |
| 3 | SNC | Sığınak sahneleri | 3.380 | SNC_1–11 |
| 4 | SND | Salgının ilk günleri (panik) | 2.098 | SND_1–7 |
| 5 | SNE | Karma: yürüyüş, karşılaşma, hikâye, karakol, nöbet, fraksiyon sohbetleri | 6.535 | SNE_1–20 |

Çıktıyı `gemini/cikti/<ad>_TR.txt` olarak kaydet (ör. `SNA_1_TR.txt`). Getirdiğin kadarı işlenir; her paket için en az bir tam parça yeter.

Sahneler (≈32 bin) şimdilik İngilizce (K37).

## Codex'in tarafı (Claude'un paket biçimiyle)

- Hazırlama: `python -X utf8 araclar/harici_paket.py hazirla <PAKET> <grup>` → `gemini/girdi/` + `rapor/<PAKET>_harita.json`
- Yeni satırlar (mod güncellemesi): `hazirla-yeni Y1 --yeni` ve `hazirla-sahne Y1S --yeni` → `gemini/yeni/girdi/`; almak için `al Y1 --yeni`
- Alma: `python -X utf8 araclar/harici_paket.py al <PAKET>` (gemini/cikti/<PAKET>_*_TR.txt hepsi; tamamlanmış parçalar) → `paketler/<PAKET>.json`
- Sonra: `paket_kontrol` → kullanıcı onayı → `onayla` → `son_kontrol` → `workshop_kur` → commit.
