# B5a — 1.5.0 farkları: Sandbox değişen 19 (8 sayfa başlığı, 11 açıklama/seçenek); kalkan PresetWorld 8 onayla'da düşer

Dağılım: Claude (EN değişmiş): 15, Claude (yeni): 4 · Toplam: 19

**Otomatik kontrol: temiz** ✅

### 1. `Sandbox_ProjectALife.PresetDifficulty_tooltip` — Claude (EN değişmiş)
- **EN:** 'How hard NPCs fight and how often raids come. Only default-valued options change. Reload for full effect. Details are on the EXPERT preset page.\nDefault Normal (2). The single player start cards still open on Easy.'
- **Eski EN:** 'Light: 50 damage, 80 health, raids day 60. Only default-valued options change; density is separate. Reload for full effect. Hostile cap affects new admissions only.\nDefault Standard (2).'
- **Eski TR:** "NPC'lerin ne kadar sert dövüştüğü ve baskınların ne sıklıkla geldiği. Yalnızca varsayılan değerinde duran ayarlar değişir. Tam etki için oyunu yeniden yükle. Ayrıntılar UZMAN ön ayar değerleri sayfasında.\nVarsayılan: Normal (2). Tek oyunculuda başlangıç kartları yine de Kolay seçili açılır."
- **TR:** "NPC'lerin ne kadar sert dövüştüğü ve baskınların ne sıklıkla geldiği. Yalnızca varsayılan değerinde duran ayarlar değişir. Tam etki için oyunu yeniden yükle. Ayrıntılar UZMAN ön ayar değerleri sayfasında.\nVarsayılan: Normal (2). Tek oyunculuda başlangıç kartları yine de Kolay seçili açılır."
- *Not: Sayfa atfı: yeni sayfa 'A-Life: EXPERT - Preset values (Difficulty and Population)' B6'da 'A-Life: UZMAN - Ön ayar değerleri (Zorluk ve Nüfus)' olacak; atıf ona göre.*

### 2. `Sandbox_ProjectALife.PresetDifficulty_option2` — Claude (EN değişmiş)
- **EN:** 'Normal'
- **Eski EN:** 'Standard'
- **Eski TR:** 'Normal'
- **TR:** 'Normal'
- *Not: Medium → Normal oldu; 'Orta' yerine.*

### 3. `Sandbox_ProjectALife.AimPlayerPercent_tooltip` — Claude (EN değişmiş)
- **EN:** "Global multiplier on how often NPC gunfire hits players, applied on top of the NPC aim setting and each character's own accuracy. 100 is unchanged. NPCs also aim worse in the first seconds of a fight, at long range and against a moving target. Default 85."
- **Eski EN:** "Global multiplier on how often NPC gunfire hits players, applied on top of the NPC aim setting and each character's own accuracy. 100 is unchanged. NPCs also aim worse in the first seconds of a fight, at long range and against a moving target."
- **Eski TR:** "NPC ateşinin oyunculara ne sıklıkla isabet ettiğine uygulanan genel çarpan; NPC'lerin oyunculara karşı nişan becerisi ayarının ve her karakterin kendi isabetinin üstüne eklenir. 100 değiştirmez. NPC'ler çatışmanın ilk saniyelerinde, uzak mesafede ve hareket eden hedefe karşı da daha kötü nişan alır."…
- **TR:** "NPC ateşinin oyunculara ne sıklıkla isabet ettiğine uygulanan genel çarpan; NPC'lerin oyunculara karşı nişan becerisi ayarının ve her karakterin kendi isabetinin üstüne eklenir. 100 değiştirmez. NPC'ler çatışmanın ilk saniyelerinde, uzak mesafede ve hareket eden hedefe karşı da daha kötü nişan alır. Varsayılan: 85."
- *Not: Yalnız sona varsayılan eklendi; metnin geri kalanı aynı.*

### 4. `Sandbox_ProjectALife.WarningEnabled_tooltip` — Claude (EN değişmiş)
- **EN:** 'Off: hostile crews attack on sight. On: reputation sets how many attack on sight (Expert page); the rest demand surrender or warn first. Careful factions keep their own rules.\nDefault on.'
- **Eski EN:** 'Enables warnings for crews set to warn; others attack on sight unless a chance below allows a warning. Off: hostile crews attack on sight. Careful factions keep their own rules.\nDefault on.'
- **Eski TR:** 'Kapalı: düşman ekipler gördükleri yerde saldırır. Açık: kaç ekibin gördüğü yerde saldıracağını itibarın belirler (Uzman sayfası); geri kalanlar önce teslim olmanı ister ya da uyarır. Temkinli fraksiyonlar kendi kurallarını uygular.\nVarsayılan: açık.'
- **TR:** 'Kapalı: düşman ekipler gördükleri yerde saldırır. Açık: kaç ekibin gördüğü yerde saldıracağını itibarın belirler (Uzman sayfası); geri kalanlar önce teslim olmanı ister ya da uyarır. Temkinli fraksiyonlar kendi kurallarını uygular.\nVarsayılan: açık.'

### 5. `Sandbox_ProjectALife.WarningChance_tooltip` — Claude (EN değişmiş)
- **EN:** 'Share of crews set to attack on sight that warn anyway. Each group rolls once and keeps its result. 0 means none; 100 means all. Reputation does not change this; raids use their own chance.\nDefault 15.'
- **Eski EN:** 'Sets the share of normally kill-on-sight crews that warn anyway. Each group rolls once and keeps its result. 0 means none; 100 means all. Raids use their separate chance.\nDefault 15.'
- **Eski TR:** 'Gördüğü yerde saldırmaya ayarlı ekiplerin yine de uyarma oranı. Her grup bir kez zar atar ve sonucu değişmez. 0 hiçbiri, 100 hepsi demek. İtibar bunu değiştirmez; baskınların kendi olasılığı var.\nVarsayılan: 15.'
- **TR:** 'Gördüğü yerde saldırmaya ayarlı ekiplerin yine de uyarma oranı. Her grup bir kez zar atar ve sonucu değişmez. 0 hiçbiri, 100 hepsi demek. İtibar bunu değiştirmez; baskınların kendi olasılığı var.\nVarsayılan: 15.'

### 6. `Sandbox_ProjectALife.WarningRaidChance_tooltip` — Claude (EN değişmiş)
- **EN:** 'Sets the share of raids, assassins, highway ambushers and admin-spawned attackers that warn first. A bad reputation lowers it, a good one raises it. 0 makes all of them attack on sight.\nDefault 10.'
- **Eski EN:** 'Sets the share of raids, assassins, highway ambushers and admin-spawned attackers that warn first. 0 makes all of these crews attack on sight.\nDefault 10.'
- **Eski TR:** "Baskıncıların, suikastçıların, yol pusucularının ve yöneticinin oluşturduğu saldırganların önce uyarma oranını belirler. Kötü itibar bu oranı düşürür, iyi itibar yükseltir. 0'da hepsi gördüğü yerde saldırır.\nVarsayılan: 10."
- **TR:** "Yağmacıların, suikastçıların, yol pusucularının ve yöneticinin oluşturduğu saldırganların önce uyarma oranını belirler. Kötü itibar bu oranı düşürür, iyi itibar yükseltir. 0'da hepsi gördüğü yerde saldırır.\nVarsayılan: 10."

### 7. `Sandbox_ProjectALife.GunsVsZombiesPercent_tooltip` — Claude (EN değişmiş)
- **EN:** 'How often an NPC that could shoot a zombie does so. Gunfire draws more zombies, so lowering this makes NPCs walk around zombies, use melee on a lone one, and keep their guns for NPCs and players. They still shoot when cornered, hurt, defending a hurt player, on a horde that blocks the way, or on duty as military or police. 0 means never unless cornered. 100 is the old behaviour. Default 70. A stored 50 from an older save still acts as 70 in the first 14 days.'
- **Eski EN:** 'How often an NPC that could shoot a zombie does so. Gunfire draws more zombies, so by default NPCs walk around zombies, use melee on a lone one, and keep their guns for NPCs and players. They still shoot when cornered, hurt, defending a hurt player, on a horde that blocks the way, or on duty as mili'…
- **Eski TR:** "Bir zombiyi vurabilecek durumdaki NPC'nin bunu ne sıklıkla yaptığı. Silah sesi daha çok zombi çeker; bu yüzden değeri düşürürsen NPC'ler zombilerin etrafından dolanır, tek zombiye yakın dövüşle girişir ve silahlarını NPC'lerle oyunculara saklar. Köşeye sıkıştıklarında, yaralandıklarında, yaralı bir "…
- **TR:** "Bir zombiyi vurabilecek durumdaki NPC'nin bunu ne sıklıkla yaptığı. Silah sesi daha çok zombi çeker; bu yüzden değeri düşürürsen NPC'ler zombilerin etrafından dolanır, tek zombiye yakın dövüşle girişir ve silahlarını NPC'lerle oyunculara saklar. Köşeye sıkıştıklarında, yaralandıklarında, yaralı bir oyuncuyu korurken, yolu tıkayan bir sürüye karşı ya da asker veya polis olarak görevdeyken yine ateş ederler. 0, köşeye sıkışmadıkça asla demek. 100 eski davranış. Varsayılan: 70. Eski bir kayıtta saklı kalmış 50 değeri ilk 14 gün yine 70 gibi davranır."
- *Not: Yalnız son iki cümle değişti.*

### 8. `Sandbox_ProjectALife.GunNoiseZombies_tooltip` — Claude (EN değişmiş)
- **EN:** 'An NPC holds fire when more than this many zombies are within 25 tiles, unless it is cornered, hurt or defending a hurt player. 0 turns the check off. Default 24 (a stored 8, the old default, counts as 24).'
- **Eski EN:** 'An NPC holds fire when more than this many zombies are within 25 tiles, unless it is cornered, hurt or defending a hurt player. 0 turns the check off. Default 8.'
- **Eski TR:** '25 kare içinde bundan fazla zombi varsa NPC; köşeye sıkışmadıkça, yaralı değilse ya da yaralı bir oyuncuyu korumuyorsa ateş etmez. 0 bu kontrolü kapatır. Varsayılan: 24 (eski kayıtlarda saklı kalmış eski varsayılan 8, 24 sayılır).'
- **TR:** '25 kare içinde bundan fazla zombi varsa NPC; köşeye sıkışmadıkça, yaralı değilse ya da yaralı bir oyuncuyu korumuyorsa ateş etmez. 0 bu kontrolü kapatır. Varsayılan: 24 (eski kayıtlarda saklı kalmış eski varsayılan 8, 24 sayılır).'

### 9. `Sandbox_ProjectALife.Outposts_TrioMaxActive_tooltip` — Claude (yeni)
- **EN:** 'Maximum outposts with a coordinated group away at once. Set 0 to stop departures.\nDefault 2.'
- **Eski TR:** 'Ortak grubu aynı anda dışarıda olabilecek en fazla karakol sayısı. 0 yaparsan çıkışlar durur.\nVarsayılan: 2.'
- **TR:** 'Ortak grubu aynı anda dışarıda olabilecek en fazla karakol sayısı. 0 yaparsan çıkışlar durur.\nVarsayılan: 2.'
- *Not: Savaş Sınavı cümlesi kalktı (ön ayar moddan çıktı).*

### 10. `Sandbox_ProjectALife.Outposts_MegaEnabled_tooltip` — Claude (yeni)
- **EN:** 'Automatic keeps these groups off on Easy difficulty and on otherwise. Choose Off or On to override that rule at any difficulty.\nDefault Automatic: off on Easy, on otherwise (1).'
- **Eski TR:** "Otomatik, bu grupları Kolay zorlukta kapalı, diğerlerinde açık tutar. Bu kuralı her zorlukta geçersiz kılmak için Kapalı ya da Açık seç.\nVarsayılan: Otomatik: Kolay'da kapalı, diğerlerinde açık (1)."
- **TR:** "Otomatik, bu grupları Kolay zorlukta kapalı, diğerlerinde açık tutar. Bu kuralı her zorlukta geçersiz kılmak için Kapalı ya da Açık seç.\nVarsayılan: Otomatik: Kolay'da kapalı, diğerlerinde açık (1)."

### 11. `Sandbox_ProjectALife.Outposts_MegaMaxActive_tooltip` — Claude (yeni)
- **EN:** 'Maximum large marching groups away at once, with one per faction. Set 0 to stop departures.\nDefault 1.'
- **Eski TR:** 'Aynı anda dışarıda olabilecek en fazla büyük yürüyüş grubu, fraksiyon başına bir tane. 0 yaparsan çıkışlar durur.\nVarsayılan: 1.'
- **TR:** 'Aynı anda dışarıda olabilecek en fazla büyük yürüyüş grubu, fraksiyon başına bir tane. 0 yaparsan çıkışlar durur.\nVarsayılan: 1.'
- *Not: Savaş Sınavı cümlesi kalktı.*

### 12. `Sandbox_ProjectALife_1People` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - People and spawning'
- **Eski EN:** 'A-Life: People and groups'
- **Eski TR:** 'A-Life: UZMAN - İnsanlar ve ortaya çıkma'
- **TR:** 'A-Life: UZMAN - İnsanlar ve ortaya çıkma'
- *Not: Sayfa başlıkları mevcut 'A-Life: UZMAN - …' biçiminde (7ExpertBehavior gibi). spawning = dünyada belirme → ortaya çıkma (SOZLUK B).*

### 13. `Sandbox_ProjectALife_2Danger` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - Danger, raids and injuries'
- **Eski EN:** 'A-Life: Danger and combat'
- **Eski TR:** 'A-Life: UZMAN - Tehlike, baskınlar ve yaralanmalar'
- **TR:** 'A-Life: UZMAN - Tehlike, baskınlar ve yaralanmalar'

### 14. `Sandbox_ProjectALife_3Talk` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - Conversations and reputation'
- **Eski EN:** 'A-Life: Conversations and reputation'
- **Eski TR:** 'A-Life: UZMAN - Sohbet ve itibar'
- **TR:** 'A-Life: UZMAN - Sohbet ve itibar'

### 15. `Sandbox_ProjectALife_4Bases` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - Bases and outposts'
- **Eski EN:** 'A-Life: Bases and visitors'
- **Eski TR:** 'A-Life: UZMAN - Üsler ve karakollar'
- **TR:** 'A-Life: UZMAN - Üsler ve karakollar'

### 16. `Sandbox_ProjectALife_4Visitors` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - Visitors and companions'
- **Eski EN:** 'A-Life: Visitors as people'
- **Eski TR:** 'A-Life: UZMAN - Ziyaretçiler ve yol arkadaşları'
- **TR:** 'A-Life: UZMAN - Ziyaretçiler ve yol arkadaşları'
- *Not: companion = Yol Arkadaşı (IG_UI'deki mevcut kullanım).*

### 17. `Sandbox_ProjectALife_5World` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - World and activities'
- **Eski EN:** 'A-Life: World and activities'
- **Eski TR:** 'A-Life: UZMAN - Dünya ve etkinlikler'
- **TR:** 'A-Life: UZMAN - Dünya ve etkinlikler'

### 18. `Sandbox_ProjectALife_6Sound` — Claude (EN değişmiş)
- **EN:** 'A-Life: EXPERT - Sound, helicopters and performance'
- **Eski EN:** 'A-Life: Sound and performance'
- **Eski TR:** 'A-Life: UZMAN - Ses, helikopterler ve performans'
- **TR:** 'A-Life: UZMAN - Ses, helikopterler ve performans'

### 19. `Sandbox_ProjectALife_2War` — Claude (yeni)
- **EN:** 'A-Life: EXPERT - War, cars and factions'
- **Eski TR:** 'A-Life: UZMAN - Savaş, arabalar ve fraksiyonlar'
- **TR:** 'A-Life: UZMAN - Savaş, arabalar ve fraksiyonlar'
