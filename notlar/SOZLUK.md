# Terim sözlüğü

Bağlayıcıdır. Kaynak kısaltmaları: **K** = kullanıcının eski çevirisi · **G** = gladium · **Kb** = kebab · **N** = Nalbarkar · **V** = vanilla PZ Türkçesi.
Durum: ✅ onaylı · 🟡 öneri, onay bekliyor · 💡 K9 adayı (özgün terim, son kararı kullanıcı verir)

Taramayı yenilemek için: `python araclar/terim_tara.py "<regex>"`

## A. Tutarlı olanlar (onaylandı 2026-10-16)

| EN | TR | Kaynak | Durum | Not |
|---|---|---|---|---|
| tile(s) | kare | K, G, Kb, N, V | ✅ | "{n} kare" |
| reputation | itibar | G, Kb, N | ✅ | |
| visitor | ziyaretçi | G, Kb, N | ✅ | |
| encounter | karşılaşma | K, Kb | ✅ | |
| raid | baskın | K, N, V | ✅ | K4 |
| diagnostics | tanılama | K, G, Kb | ✅ | |
| [Expert] | [Uzman] | N | ✅ | Sandbox'ta 133 yerde önek |
| default | varsayılan | herkes | ✅ | Tooltip sonu: "Varsayılan: açık." / "Varsayılan olarak kapalı." (K5: "-dır" yok) |
| camp | kamp | K, G, V | ✅ | "Camp Boss" → "Kamp Reisi" (K) |
| looter | yağmacı | K, G, Kb | ✅ | |
| profile | profil | K, G, Kb | ✅ | |
| guest | misafir | Y (S1) | ✅ | Ziyaretçi (visitor) evine girip ağırlandığında "guest" deniyor. |
| peephole | kapı dürbünü | Y (S5) | 🟡 | |
| walled compound | surlu yerleşke | Y (S5) | 🟡 | Etrafı duvarla çevrili büyük karakol. |
| dedicated server | özel sunucu | Y (S5) | 🟡 | N "bağımsız sunucu" demişti. |
| co-op | ortak oyun | Y (S5) | 🟡 | |
| reputation / faction standing / opinion | itibar / fraksiyonla aran / görüş | Y (S4) | ✅ | Üç ayrı kavram. |
| reanimate | yeniden canlanma | V (S3) | ✅ | Oyunun kendi terimi. |
| forage / foraging | doğadan yiyecek toplama | Y (S6) | ✅ | V "Araştırma" der; modda "araştırma" investigate'e ayrıldığı için kullanılmadı. |
| offline (NPC etkinliği) | arka planda | Y (S2, S6) | ✅ | "Offline only" → "Yalnızca arka planda". |
| hotwire | düz kontak | V (S6) | ✅ | |
| investigate / clues | araştırma / iz | Y (S6) | ✅ | |
| adapter (uyumluluk) | uyum yaması | Y (S7) | ✅ | "[Expert] X adapter" → "[Uzman] X uyum yaması" |
| Sister / Brother (radyodaki koro unvanı) | Kardeş | Y (B7, 2026-11-09) | ✅ | "Sister Wren" → "Kardeş Wren", "Brother Ansel" → "Kardeş Ansel"; ad aynen. Aile bağı ("Kid Brother") ayrı: "Küçük Kardeş". |
| searchlight | projektör | Y (S1, S7) | ✅ | |
| Survivor | Hayatta Kalan | K, G, Kb, N, V | ✅ | K23: kesinleşti ("Olayzede" adayı kullanılmadı: vanilla ile tutarlılık, "-zede" edilgen). |

## B. Çelişenler (2026-10-16: kullanıcı kararı Claude'a bıraktı, sütundaki "Karar" uygulanır)

| EN | Kullanılanlar | Karar ✅ | Gerekçe |
|---|---|---|---|
| **Creator** | Oluşturucu (K, G, N) · **Düzenleyici** (Kb, 11 yerde) | **Oluşturucu** | Çoğunluk ve eski çeviri; Kb'nin metinleri düzeltilir. |
| **spawn** | oluşturma (K, V) · doğurma (G) · doğma / ortaya çıkma / oluşma (Kb) | Anlama göre üçe ayır: **yönetici eylemi** "oluştur" (Spawn NPC → NPC oluştur) · **dünyada kendiliğinden belirme** "ortaya çıkma" · **spawn point** "doğma noktası" (V) | "Doğurma" yanlış çağrışım. Vanilla da eylem için "Oluştur", nokta için "doğma" kullanıyor. |
| **outpost** | üs (K, N) · karakol (G) | **karakol** | "Üs" oyuncunun kendi üssü (base) için gerekli; ikisi aynı kelime olursa karışır. Karakol, fraksiyonun tuttuğu ileri mevzi anlamını tam veriyor. K'nin "Üs telsizi" → "Karakol telsizi". |
| **base** (oyuncunun) | üs (N, Kb) | **üs** | Outpost karakol olunca çakışma kalkar. |
| **safehouse** | sığınak (K, G, N) · güvenli ev (Kb, V) | **güvenli ev** | PZ oyuncuları çok oyunculu "Safehouse" özelliğini vanilla Türkçede "Güvenli Ev" olarak görüyor; mod da aynı özelliğe bağlanıyor. "Sığınak" → **shelter** için kalır. |
| **squad** | tim (K) · manga (K, G) · ekip (K) · grup (Kb) | **tim** · askerî unvanda **manga** ("Squad Leader" → "Manga Komutanı", katalogda yalnızca askerî fraksiyonlarda) | Tim polis, asker ve çeteye birlikte uyuyor. |
| **crew** | ekip (K, G, Kb) · tayfa (K, N) | Genel kullanımda **ekip** · haydut/çete adlarında **tayfa** serbest ("Kül Tayfası") | N'nin "Yakın dövüş tayfası" (ayar adı) → "yakın dövüş ekibi". |
| **group** | grup (herkes) | **grup** | Squad ve crew'dan ayrı tutulmalı (Kb'de "Spawn faction squad" → "fraksiyon grubu" olmuş). |
| **faction** | fraksiyon (K, Kb, N) · grup (G, 2 yerde) · V: "Grup"/"Klan" | **fraksiyon** | Modda "group" ayrı bir kavram; faction = grup olursa ikisi karışır. |
| **hostile** | düşmanca (K, G: tutum etiketi) · düşman (sıfat) | Tutum etiketi **Düşman** · sıfat **düşman** | Etiketler kısa olmalı: Dost / Tarafsız / Düşman (stance listesi paketlerde netleşecek). |
| **preset** | ön ayar (K, V) · şablon (Kb) · hazır ayar (K) | Dünya/zorluk ön ayarı **ön ayar** (V) · Oluşturucu'daki üye şablonu (member preset) **şablon** | İki ayrı kavram; Kb'nin "şablon"u kendi bağlamında doğru. |
| **traveller** | yolcu (K) · gezgin (N) | **yolcu** · "roaming/roamer" için **gezgin** (K: "Gezgin grup") | İkisi modda farklı kavram. |
| **scavenge** (eylem) | malzeme toplama (K, N) · yağma (G) · aranmış (N) | **malzeme toplama** | "Yağma" looting'e ayrılmalı. |
| **Scavenger** (NPC unvanı) | Toplayıcı (K) · Hurdacı (G) · "Yağma/toplama Yapan Kişi" (Kb) | **Leşçi** (K23) | Katalogda haydut fraksiyonlarında (Bone Raiders, Knob Stalkers). Kb'ninki unvan değil açıklama. V'de "The Scavenger" → "Leşçil". Sivil "Picker"lar Toplayıcı kalır. |
| **Hired Hand** | Çiftlik İşçisi (K) · Tarla İşçisi (G) · Yevmiyeli İşçi (Kb) | **Çiftlik İşçisi** | Katalogda tamamı çiftlik/ahır/mandıra fraksiyonlarında. |
| **loot** (isim) | ganimet (N, V) · malzeme | **ganimet** | |

## C. Genel kurallar (onaylandı)

- **Arayüz etiketine atıf:** Yardım metinleri bir sekme ya da buton adını anarken ("SPAWNING tab", "NEW FOLDER") Türkçesi o etiketin çevirisiyle **birebir** aynı olmalı. Paketlerde otomatik kontrol edilecek. (Kb'de "OLUŞMA sekmesi", G'de "Tanılama'yı işaretleyin" gibi atıflar var.)
- **Büyük harf:** EN'de büyük harfle yazılmış etiketler (NEW FOLDER) TR'de de büyük harf (YENİ KLASÖR), Türkçe İ/ı kurallarıyla.
- **Yüzde:** Sandbox'ta `%%` kalır, Türkçe sırayla yazılır: "%%40" (K'nin mevcut kullanımı).
