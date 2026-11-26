# L152 — 1.5.2 Lua metinleri için Fable girdileri

Bu hazırlık rapordaki **540 çeviri birimini** anlamlı dosyalara böler. 540 sayısı yalnızca numaralı kaynak satırlarını sayar; başlıklar ve kısa bağlam notları dahil değildir. Aynı İngilizce metin farklı çalışma yollarında geçiyorsa, ayrı anahtar/alıcı kontrolü için ayrı satır olarak korunmuştur.

## Dosya dağılımı

| Dosya | Satır | İçerik |
|---|---:|---|
| `L152_PHONE_01.txt` | 64 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_02.txt` | 38 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_03.txt` | 46 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_04.txt` | 37 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_05.txt` | 42 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_06.txt` | 48 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_07.txt` | 35 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_08.txt` | 41 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_09.txt` | 29 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_PHONE_10.txt` | 36 | Telefon ağacı: arayan etiketi ve görüşme metinleri |
| `L152_TASK_PLAYER.txt` | 14 | Left Behind görevinde oyuncu seçenekleri |
| `L152_TASK_NPC_01.txt` | 13 | Left Behind görev NPC replikleri; aşamaya göre |
| `L152_TASK_NPC_02.txt` | 14 | Left Behind görev NPC replikleri; aşamaya göre |
| `L152_TASK_NPC_03.txt` | 18 | Left Behind görev NPC replikleri; aşamaya göre |
| `L152_TASK_UI.txt` | 21 | Görev günlüğü, kartı ve görev ekranı |
| `L152_TASK_OUTCOMES.txt` | 13 | Görev sonuçları ve dinamik görev kalıpları |
| `L152_TASK_TREE_NOTES.txt` | 8 | Konuşma ağacı görev bildirimleri |
| `L152_UI_MAP.txt` | 4 | A-Life harita etiketleri |
| `L152_UI_SETTINGS.txt` | 19 | A-Life ayarları, yerleşim ve konuşma görünümü |

## Fable kullanımı

Her TXT'yi Fable 5.2'ye ver ve orada kullandığın çeviri skill'iyle çalış. Kısa bağlam, gerekli terimler ve özel kurallar TXT'nin içinde. Dosya başındaki `#` ve `#####` satırları bağlamdır. Türkçe çıktıyı aynı adla `gemini/cikti/` içine koy.

Telefon dosyalarının başındaki özel kural geçerli. Oyunun doldurduğu yer tutucular yazımları ve harf büyüklükleriyle korunur. Görev ve arayüz dosyalarındaki `{...}` yer tutucular yerel eşleme dosyasında satır satır kayıtlı.

Telefonlarda tekrarlanan iki kaynak cümlesi tek kez verildi: `I have to go` altı ağaçta, `Thanks, whoever you are` iki ağaçta kullanılıyor. Aynı kaynak metin aynı lookup anahtarını paylaşır; çoklu kaynak konumları manifestte tutuldu.

## Satır toplamı

- Telefon: 406 konuşma/yanıt/sonuç metni + 10 arayan etiketi = **416**
- Görev: 45 NPC repliği + 14 oyuncu seçeneği + 18 ekran metni + 3 görev kartı + 7 sabit bildirim + 6 dinamik kalıp + 8 treeNote = **101**
- Ek A-Life arayüzü: **23**
- **Toplam: 540 numaralı satır, 19 girdi dosyası.**

## Sonraki teknik kontrol için kayıt

Çeviriler gelince önce her dosyanın beklenen satır sayısı ve 1..N numaralarının tam/tekil olduğu doğrulanmalı. Ardından her satırın yer tutucu kümesi kaynak İngilizceyle birebir karşılaştırılmalı; telefon satırlarında özellikle `{lost}`, `{you}`, `{he}`, `{He}`, `{him}`, `{his}` harf büyüklüğüyle korunmalı. Kaynak metin, çağrı yeri, sink ve placeholder listesi `L152_HAZIRLIK_540.json` içinde tutulur.

Çeviriler doğrudan `onayli/`, `kaynak/`, `teslim/` veya Workshop’a aktarılmayacak. Anahtar üretimi/alımı öncesi her satırın gerçek çağrı yolu ve hedefi manifestteki `technical_route`, `sink` ve `source_locations` ile doğrulanmalı. Özellikle:

1. Telefon arayan etiketleri `ask.name` üzerinden `Text.ui` yolunu atlar; telefon zamir doldurma yolu da İngilizce değer üretir. Bunlar için dar kapsamlı telefon alıcısı/uyarlaması gerekir.
2. Görev statik UI, `RadioData_lua` diyalogları, dinamik görev kalıpları ve `treeNote` bildirimleri ayrı hedeflerdir; aynı hash/alım yoluna varsayımla sokulmamalı.
3. Ek 23 UI metni kaynakta alan/metin olarak bulunur; her çağrı yolu doğrulanmadan genel çizim sınıfı kancası eklenmemeli.
4. Teslim edilen Türkçe çıktılardan sonra teknik kontrol, `paket_kontrol` ve gerekli dar runtime/anahtar denetimleri yapılmalı. Ana paketlere aktarım ve oyun testi ayrı onaylı aşamadır.

**Kapsam dışı:** A-Life Oluşturucusu modal/doğrulama metinlerinin toplamı çıkarılmadı; vanilla Project Zomboid karakter oluşturma ekranı bu 540’a dahil değil; tanıtım görsellerindeki yazılar da ayrı medya işidir.

Kaynak satır eşlemesi: [`L152_HAZIRLIK_540.json`](L152_HAZIRLIK_540.json). Kaynak denetim raporu: [`../../../../rapor/ingilizce_kalan_1.5.2.md`](../../../../rapor/ingilizce_kalan_1.5.2.md).
