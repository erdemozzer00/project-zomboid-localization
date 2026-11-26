# Terim sözlüğü

Bu sözlük yerel çalışma içindir. Girdide sabit bir karşılık gerekiyorsa ilgili terimi doğrudan TXT'ye yaz.
Durum: ✅ onaylı · 🟡 öneri, onay bekliyor · 💡 aday (özgün terim, son kararı kullanıcı verir)

Taramayı yenilemek için: `python araclar/terim_tara.py "<regex>"`

## Terimler

| EN | TR | Durum | Not |
|---|---|---|---|
| tile(s) | kare | ✅ | "{n} kare" |
| reputation | itibar | ✅ | |
| visitor | ziyaretçi | ✅ | |
| encounter | karşılaşma | ✅ | |
| raid | baskın | ✅ | |
| diagnostics | tanılama | ✅ | |
| [Expert] | [Uzman] | ✅ | Sandbox'ta 133 yerde önek |
| default | varsayılan | ✅ | İpucu örnekleri: "Varsayılan: açık." / "Varsayılan olarak kapalı." |
| camp | kamp | ✅ | "Camp Boss" → "Kamp Reisi" |
| looter | yağmacı | ✅ | |
| profile | profil | ✅ | |
| guest | misafir | ✅ | Ziyaretçi (visitor) evine girip ağırlandığında "guest" deniyor. |
| peephole | kapı dürbünü | 🟡 | |
| walled compound | surlu yerleşke | 🟡 | Etrafı duvarla çevrili büyük karakol. |
| dedicated server | özel sunucu | 🟡 | |
| co-op | ortak oyun | 🟡 | |
| reputation / faction standing / opinion | itibar / fraksiyonla aran / görüş | ✅ | Üç ayrı kavram. |
| reanimate | yeniden canlanma | ✅ | Oyunun kendi terimi. |
| forage / foraging | doğadan yiyecek toplama | ✅ | Modda "araştırma" investigate için kullanılır. |
| offline (NPC etkinliği) | arka planda | ✅ | "Offline only" → "Yalnızca arka planda". |
| hotwire | düz kontak | ✅ | |
| investigate / clues | araştırma / iz | ✅ | |
| adapter (uyumluluk) | uyum yaması | ✅ | "[Expert] X adapter" → "[Uzman] X uyum yaması" |
| Sister / Brother (radyodaki koro unvanı) | Kardeş | ✅ | "Sister Wren" → "Kardeş Wren", "Brother Ansel" → "Kardeş Ansel"; ad aynen. Aile bağı ("Kid Brother") ayrı: "Küçük Kardeş". |
| searchlight | projektör | ✅ | |
| Survivor | Hayatta Kalan | ✅ | Oyunun Türkçesiyle uyumlu. |

## Bağlama göre karşılıklar

| EN | Karar ✅ | Gerekçe |
|---|---|---|
| **Creator** | **Oluşturucu** | Oluşturucu ekranının sabit adı. |
| **spawn** | **Yönetici eylemi** "oluştur" (Spawn NPC → NPC oluştur) · **dünyada kendiliğinden belirme** "ortaya çıkma" · **spawn point** "doğma noktası" | Oyunun Türkçesi de eylem için "Oluştur", nokta için "doğma" kullanır. |
| **outpost** | **karakol** | "Üs" oyuncunun kendi üssü (base) için gerekli; ikisi aynı kelime olursa karışır. Karakol, fraksiyonun tuttuğu ileri mevzi anlamını tam veriyor. "Outpost radio" → "Karakol telsizi". |
| **base** (oyuncunun) | **üs** | Outpost karakol olunca çakışma kalkar. |
| **safehouse** | **güvenli ev** | PZ oyuncuları çok oyunculu "Safehouse" özelliğini vanilla Türkçede "Güvenli Ev" olarak görüyor; mod da aynı özelliğe bağlanıyor. "Sığınak" → **shelter** için kalır. |
| **squad** | **tim** · askerî unvanda **manga** ("Squad Leader" → "Manga Komutanı", katalogda yalnızca askerî fraksiyonlarda) | Tim polis, asker ve çeteye birlikte uyuyor. |
| **crew** | Genel kullanımda **ekip** · haydut/çete adlarında **tayfa** serbest ("Kül Tayfası") | "Melee crew" (ayar adı) → "yakın dövüş ekibi". |
| **group** | **grup** | Squad ve crew'dan ayrı tutulur. |
| **faction** | **fraksiyon** | Modda "group" ayrı bir kavram; faction = grup olursa ikisi karışır. |
| **hostile** | Tutum etiketi **Düşman** · sıfat **düşman** | Dost / Tarafsız / Düşman. |
| **preset** | Dünya veya zorluk seçimi için **ön ayar** · Oluşturucu'daki üye şablonu için **şablon** | Bağlama göre iki ayrı kavram. |
| **traveller** | **yolcu** · "roaming/roamer" için **gezgin** | İkisi modda farklı kavram. |
| **scavenge** (eylem) | **malzeme toplama** | "Yağma" looting'e ayrılmalı. |
| **Scavenger** (NPC unvanı) | **Leşçi** | Katalogda haydut fraksiyonlarında (Bone Raiders, Knob Stalkers). Sivil "Picker"lar Toplayıcı kalır. |
| **Hired Hand** | **Çiftlik İşçisi** | Katalogda tamamı çiftlik/ahır/mandıra fraksiyonlarında. |
| **loot** (isim) | **ganimet** | |

## Kullanım kuralları

- **Arayüz etiketine atıf:** Yardım metinleri bir sekme ya da buton adını anarken ("SPAWNING tab", "NEW FOLDER") Türkçesi o etiketin çevirisiyle **birebir** aynı olmalı. Paketlerde otomatik kontrol edilecek.
- **Büyük harf:** EN'de büyük harfle yazılmış etiketler (NEW FOLDER) TR'de de büyük harf (YENİ KLASÖR), Türkçe İ/ı kurallarıyla.
- **Yüzde:** Sandbox'ta `%%` kalır, Türkçe sırayla yazılır: "%%40".
