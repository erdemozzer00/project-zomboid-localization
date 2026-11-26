# Project A-Life – Jeem Extension Türkçe yaması

21 Kasım 2026 · Jeem 0.8.3 · incelenen paket 0.8.3-tr1 · düzeltilen paket 0.8.3-tr2 · yerel oyun günlüğünde Build 42.22.2.

## Uygulanan düzeltmeler · 0.8.3-tr2

Erdem’in onayıyla ayrı Jeem projesindeki çalışma dosyaları ve dağıtım klasörü güncellendi. **265 sözlük değeri** değişti (218 IG, 45 Sandbox, 2 sağ tık). Aşağıdaki ilk inceleme ve satır dizini tr1 bulgularını gösterir.

- Beş Sandbox ipucu ve dizindeki 73 geliştirici test satırı düzeltildi. Konuş sekmesinin oyuncuya görünen adı, ana A-Life yamasının replikleri ve kurulu oyunun Sandbox adları kullanıldı. Teknik konsol alıntıları korundu.
- A-Life NPC fraksiyonları, oyuncunun itibarı ve NPC görüşleri için ortak terimler uygulandı. Oyunun çok oyunculu Grup özelliğine yapılan atıflar ve gerçek grup hitapları ayrı değerlendirildi. Telsizde adıyla çağrılan tek sakinin yanıtı düzeltildi.
- İncelemedeki sekiz durum adı güncellendi. Jeem’in stres eşikleriyle oyunun dört durum kademesi karşılaştırılınca ilk ve son kademe de eşlendi. Sıra **Gergin → Huzursuz → Stresli → Cinnet Eşiğinde** oldu.
- Türkçe istemci eki Günlük içindeki Ekibim başlıklarını ve yazılı komutların büyük İ eşleştirmesini düzenliyor. Paketleme aracı, sürüm bilgisi, BENIOKU ve Jeem rehberi de güncellendi.
- Son dağıtım klasöründe yedi dosya, 4.354 anahtar ve 3.817 IG yer tutucu açılımı doğrulandı. Paket denetimi **0 hata, 0 uyarı** verdi. Oyunun Kahlua çalışma zamanında 39 komut yazımının her biri hem kayıtlı hem Türkçe büyük harfli biçimiyle doğru eyleme bağlandı. Yedi Günlük başlığı, rozet, yan menüde normal yazım ve İngilizce dilinde özgün davranış doğrulandı. Takas düğmesi ve tıklama yankısı **Takas yapalım.**, komut **ASK_TRADE** olarak kaldı.
- Yama oyun kurulumuna kopyalanmadı. Gerçek oyun penceresinde mod yüklemesi, görüntü yerleşimi, takas penceresinin açılması ve çok oyunculu deneme açık.

## İlk inceleme · 0.8.3-tr1

**Paket, oyun içi denemeye hazır.** Beklenen takas çevirisi dosyada ve düğme ile tıklama denemesinden geçti. Yayımdan önce oyuncuya yanlış ekran adı gösteren ayar açıklamaları, Ekibim başlıkları ve telsizdeki tekil hitap ele alınmalı. İnceleme sırasında yama kurulmadı veya yeniden paketlenmedi.

## Paket bütünlüğü

| Dosya | Benzersiz anahtar |
|---|---:|
| IG_UI.json | 3.817 |
| ContextMenu.json | 179 |
| Sandbox.json | 358 |
| **Toplam** | **4.354** |

Üç EN sözlüğünün anahtarları ve değerleri kurulu Workshop 3806944055 ile birebir aynı. Her Türkçe çalışma sözlüğünün içeriği paketteki karşılığıyla eşleşiyor. UTF-8 ve JSON geçerli. Yinelenen, eksik, fazladan veya kaynağı dolu olduğu halde boş bırakılmış anahtar bulunmadı. Numaralı yer tutucuların tekrar sayıları ve satır sonları korundu. Üç sözlükteki anahtarlar ana Türkçe yamanın teslimiyle çakışmıyor.

Teslimdeki `denetle.py` gerçekten **0 hata, 0 uyarı** veriyor. Ayrıca 3.817 IG metnini Jeem’in gerçek `J.t` fonksiyonundan, numaraları birbirinden ayırt edilen dokuz deneme değeriyle geçirdim. Her çıktı beklenen yer tutucu açılımına eşitti. Bu denemede sözlük aramasını paket JSON’u sağladı.

Çıktıdaki mod kimliği `ProjectALifeJimmyTR`, bağımlılık ve yükleme sırası `ProjectALifeJimmy`, minimum sürüm 42.21.0. Sürüm klasöründeki TR yolu, üç JSON ve `common` dizini mevcut. Gelen pakette Lua eki yok. BENIOKU ve rehberde ana modun yalnız İngilizce olduğu yazıyor. Bu bilgi, ana Türkçe yamayı da açan oyuncunun kurulumuna uymuyor.

## Takas ve birlikte çalışma

- Konuş sekmesindeki `IGUI_ALJ_Trade_AskChoice` **Takas yapalım.** Kapıdaki ayrı `IGUI_ALJ_Traders_DoorTrade` da **Takas yapalım.** Jeem’in kendi tüccarı için `IGUI_ALJ_Trade_AskTrader` metni **Elinde ne var, göster bakalım.** Tüccar dalındaki farklı ifade kaynakta da var.
- Paket sözlüğü, Jeem’in gerçek Choice ve TalkPool modülleri, A-Life’ın düğme oluşturma ve tıklama işlevleriyle yapılan Lua denemesinde ilk düğme ve oyuncunun konuşma yankısı **Takas yapalım.** oldu. Gönderilen komut `talkChoose`, seçim `ASK_TRADE`. Oyuncu, pencere ve komut alıcısı test ikamesiydi. Gerçek takas penceresinin açılışı ve çok oyunculu akış canlı deneme bekliyor. Ana Türkçe yamaya aynı Jeem anahtarını ayrıca eklemek gerekmiyor.
- **Maybe we can work together?** ana modda `ALifeTalkIntents.lua:279` içinde, `JOIN_REQUEST` oyuncu seçeneği. Jeem, `Friendlies.lua:834` sonrasında kabul akışına takip davranışı ekliyor. Mevcut Türkçe teslimde `IGUI_ALifeUI_06012a9255a9d734` değeri **Belki birlikte çalışabiliriz?** Jeem’in `FriendliesEnabled_tooltip` açıklamasında oyuncuya gösterilecek alıntı bununla eşleşmeli.

## İngilizce ekran atıfları

Rehberde sayılan adlar ve Transmission için Türkçe değerlerde sözcük sınırıyla arama, **5 Sandbox ipucu ve 73 farklı geliştirici test satırı** buldu. Bu, seçili ifadelerin geçtiği satırların sayısı. Bir satırda birden fazla ad olabiliyor. İngilizce metnin özellik, teknik kimlik, konsol alıntısı veya oyuncunun görmesi gereken etiket olup olmadığı bağlamıyla değerlendirilmeli. Aşağıda tüm eşleşmeler anahtarlarıyla kayıtlı.

| Öncelikli Sandbox ipucu | Oyuncuya bağlanacak karşılık |
|---|---|
| `ResidentsJoinFaction_tooltip` | Ana yamadaki menü eylemi **Fraksiyon ve NPC Oluşturucusunu Aç**. Cümlede araca atıf yapılıyor. |
| `FriendliesEnabled_tooltip` | **Belki birlikte çalışabiliriz?** |
| `NamesCreatorDisplayName_tooltip` | **NPC adı**, **Sabit ad**, **Görünen ad**, **Rastgele ad (cinsiyete göre)**, **Rastgele erkek adı**, **Rastgele kadın adı**. Tek ipucunda birden fazla seçim adı geçiyor. |
| `ResidentsHomeCalm_tooltip` | Ana A-Life sözlüğündeki **Stealth → Gizlilik**. Jeem’deki ayrı uzmanlık etiketi de ayrıca bağlamıyla okunmalı. |
| `ZombieBitesEnabled_tooltip` | A-Life simülasyonu `SandboxVars.ZombieLore` değerlerini okuyor. Kurulu oyunun ayar adları **Virüsün Öldürücülüğü** ve **Virüsün Bulaşması**. |

Ana Türkçe teslimde **Journal → Günlük**, **Tasks → Görevler**, **Contacts → Tanıdıklar**, **Companions → Yol arkadaşları**, **Leave → Ayrıl**, **Cinematic → Sinematik**, **Classic → Klasik**. Konuşma ekranında sekmenin hangi sürümünün gösterildiği, özellikle `Personal` ve `Orders` gibi iç kimliklerde, her atıf için ayrıca önemli. Geliştirici testi oyuncunun duyacağı **Not me! Shoot them!** repliğini İngilizce alıntılıyor. Ana yamanın RD karşılığı **Ben değilim! Onları vur!**. Bu örnek, sözcük aramasındaki 78 satırın dışındadır. `SafetySystem` gibi gerçek yapılandırma adları ve `console.txt` günlük çıktıları ayrı değerlendirilmeli.

## Ekibim ve yazılı komutlar

Yan menü (`FactionNav.lua:181` civarı) sözlük etiketini doğrudan çizer. Günlük içindeki Ekibim sekmeleri (`JournalTab.lua:237,245`) aynı etiket ve varsa rozet üstünde `string.upper` çalıştırır. Oyunun `LocaleManager.initialise` işlevi JVM dil ayarını ROOT yapıyor, Kahlua dize işlevleri Java’nın büyük/küçük harf dönüşümünü kullanıyor. Kurulu oyunun JAR’ı, kendi Java çalışma zamanı ve gerçek Kahlua dize kitaplığıyla alınan sonuçlar aşağıda.

| Sözlük | Günlükte üretilen | Türkçe yazım |
|---|---|---|
| Kişiler | KIŞILER | KİŞİLER |
| Çizelge | ÇIZELGE | ÇİZELGE |
| İtibar | İTIBAR | İTİBAR |

Diğer dördü doğru çıktı: ANA SAYFA, ÜSLER, GÖREVLER, HABERLER. Üç başlığın yazım hatası yeniden üretildi. Görsel taşma ve yazı tipi canlı ekranda kontrol edilmeli. Aynı etiketlerin normal yazımı yan menüde kullanıldığından düzeltmeyi Günlük başlıklarına özgü tutmak iki görünümü korur.

`TypedPhrases.lua` dokuz İngilizce komut için dikey çizgiyle ayrılmış Türkçe yazımları birebir arıyor. Gerçek Jeem modülü ve oyunun Kahlua kitaplığında **39 kayıtlı yazımın tamamı** doğru komuta döndü. **Beni takip et**, **Şunu al**, **Lütfen beni takip et!** ve **Takas yapalım lütfen.** tanındı. **BENİ TAKİP ET** tanınmadı; büyük İ küçülünce oluşan i ve birleşen nokta, kayıtlı diziden farklı. **TAKAS YAPALIM** tanındı, çünkü noktasız ve ASCII yazımları listede mevcut. Listede İ ile başlayan bir yazım yok. **İzle beni** başlı başına kayıtlı bir eş anlamlı da değil. Başındaki İ’yi değiştirmek tek başına bu ifadeyi geçerli komut yapmaz.

## Durum adları, telsiz ve ortak sözlük

Kurulu oyunun EN durum anahtarlarıyla eşleşen sekiz Jeem etiketi, aynı anahtarların güncel TR değerinden ayrılıyor. Oyunun TR dosyasında eski küçük harfli anahtarlarla güncel büyük harfli tür adları yan yana duruyor. Örneğin `Moodles_thirst_lvl3` eski **Kavrulmuş**, EN’in kullandığı `Moodles_Thirst_lvl3` **Çok Susamış**. Jeem’in `Needs.lua` sözlüğü bu adları kendi NPC’lerine bağlıyor.

| EN | Jeem TR | Kurulu oyundaki eşdeğer durum |
|---|---|---|
| Peckish | Hafif Aç | Acıkmış |
| Parched | Kavrulmuş | Çok Susamış |
| Drowsy | Hafif Yorgun | Uykulu |
| Agitated | Tedirgin | Huzursuz |
| Queasy | Midesi Bulanmış | Halsiz |
| Nauseous | Kusacak Gibi | Midesi Bulanıyor |
| Tipsy | Çakır Keyif | Çakırkeyif |
| Agony | Istırap | Acı İçinde |

**Telsizde tek kişi.** `RadioCalls.lua:132–158` içinde oyuncu adıyla bir sakini seçtiğinde yalnız o NPC’nin kimliği aranıyor. Gelemezse `IGUI_ALJ_Radio_NotFree` çağrılıyor ve `%1` yerine **üssün adı** konuyor. Türkçe metin **“%1: şu an gelemezler.”** diyor. Burada tekil yüklem gerekli. Serbest kimse bulunamayan genel çağrının anahtarı ayrı.

**Ortak terimler.** Jeem rehberi faction için **grup**, opinion için **kanaat**, A-Life reputation için **ün** seçmiş. Ana yamanın onaylı karşılıkları sırasıyla **fraksiyon**, **görüş**, **itibar**. Örneğin Jeem’in `Rep_HeadFaction` sütununda **Grup** yazıyor, `Faction_ResetAlifeTip` ise üç kavramı aynı işlem içinde anıyor. Birlikte oynanacak sürümde iki sözlük uzlaştırılmalı. Serbest diyalogdaki “grup” ile teknik fraksiyon adı aynı işlemle değiştirilemez. Ana proje üslubu Jeem’e de uygulanacaksa 58 IG ve 5 Sandbox değerinde şapkalı harf var. Bu bir üslup tercihi.

## Parçalar, bulunamayanlar ve canlı doğrulama

427 sayısı Türkçede küçük harfle başlayan **420 IG ve 7 sağ tık** değeriyle örtüşüyor. Bu grupta, dokuz komutun kabul listeleri gibi, cümleye eklenmeyen değerler de var. İngilizcede başında veya sonunda boşluk olan 32 değer var. Ölüm haberlerinde iki ek parçanın başındaki virgül Türkçede boşluk ve paranteze dönüştürülmüş. `News.lua:112–127` ile `J.t` üzerinden örnekler **“Wade öldü (kan kaybından).”** ve **“Wade öldü (öldüren: Erdem).”** olarak birleşti. Bu iki istisna sözcükleri bitiştirmiyor. 4.354 satırın tamamı elle ikinci kez okunmadı ve 427 değerin her kullanım yolu ayrı ayrı çalıştırılmadı.

`Gift_Becomes`, `Faction_OnWatch`, `Faction_ToNext`, `Faction_Highest`, `Faction_PersonSub` çeviride mevcut. Jeem 0.8.3 Lua dosyalarında bu beş tam anahtara doğrudan başvuru bulunmadı. Benzer işlevlerde `Trade_Why_Becomes`, `Standing_ToNext` ve `Roster_RoleWhyOnWatch` gibi farklı anahtarlar kullanılıyor. Dinamik anahtar üretimi olasılığı açık olduğundan mevcut beş satırı korumak uygun.

Son canlı kontrolde Türkçe dil ve iki yama etkinken sıradan bir NPC’de ilk takas seçimi, konuşma yankısı, açılan pencere ve geri dönüş birlikte denenmeli. Ardından bir isimle telsiz çağrısı, Günlük > Ekibim’in dar pencere görünümü ve Sandbox’taki Jeem ayarları kontrol edilebilir.

## İngilizce atıfların satır dizini

Aşağıdaki adlar paket JSON’undaki anahtarlardır. Parantezdeki sayı çıktı dosyasındaki satırdır. Birden fazla İngilizce ada rastlanan satır bir kez listelenir.

### Sandbox.json

- `Sandbox_ALifeJimmy_ResidentsJoinFaction_tooltip` (60) · Faction & NPC Creator
- `Sandbox_ALifeJimmy_FriendliesEnabled_tooltip` (212) · Maybe we can work together?
- `Sandbox_ALifeJimmy_NamesCreatorDisplayName_tooltip` (231) · Set name, Display name
- `Sandbox_ALifeJimmy_ResidentsHomeCalm_tooltip` (264) · Stealth
- `Sandbox_ALifeJimmy_ZombieBitesEnabled_tooltip` (303) · Mortality, Transmission

### IG_UI.json

- `IGUI_ALJ_RelCheck_073_TalkQuick_Title` (455) · Leave
- `IGUI_ALJ_RelCheck_073_TalkQuick_Todo` (456) · Leave, Cinematic, Classic
- `IGUI_ALJ_RelCheck_073_TalkQuick_Expect` (457) · Leave, Cinematic, Classic
- `IGUI_ALJ_RelCheck_073_TalkBack_Todo` (459) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_073_TalkBack_Expect` (460) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_073_ResOrders_Title` (461) · Orders
- `IGUI_ALJ_RelCheck_073_ResOrders_Todo` (462) · Orders
- `IGUI_ALJ_RelCheck_073_EquipTalk_Expect` (469) · Cinematic
- `IGUI_ALJ_RelCheck_075_HomeSneak_Todo` (492) · Stealth
- `IGUI_ALJ_RelCheck_075_HomeSneak_Expect` (493) · Stealth
- `IGUI_ALJ_RelCheck_076_Generator_Todo` (495) · Stealth
- `IGUI_ALJ_RelCheck_076_Generator_Expect` (496) · Stealth
- `IGUI_ALJ_RelCheck_081_CompanionGo_Todo` (609) · Personal, Come with me
- `IGUI_ALJ_RelCheck_081_CompanionAway_Todo` (612) · Orders
- `IGUI_ALJ_RelCheck_081_CompanionAway_Expect` (613) · Orders, Personal, Come with me
- `IGUI_ALJ_RelCheck_081_CompanionHome_Todo` (615) · Orders
- `IGUI_ALJ_RelCheck_081_CompanionDismissed_Todo` (618) · Come with me
- `IGUI_ALJ_RelCheck_081_CompanionFollower_Todo` (621) · Come with me
- `IGUI_ALJ_RelCheck_081_CompanionMoveIn_Todo` (627) · Come with me
- `IGUI_ALJ_RelCheck_081_CompanionMp_Todo` (630) · Come with me
- `IGUI_ALJ_RelCheck_NoCreatorPreset` (2213) · Set name
- `IGUI_ALJ_RelCheck_Setup_CreatorNpc` (2236) · Set name
- `IGUI_ALJ_RelCheck_Setup_MakeStealth` (2259) · Stealth
- `IGUI_ALJ_RelCheck_SetupDone_Stealth` (2299) · Stealth
- `IGUI_ALJ_RelCheck_SetupDone_StealthHad` (2300) · Stealth
- `IGUI_ALJ_RelCheck_Check_CreatorName` (2329) · Set name
- `IGUI_ALJ_RelCheck_Check_HomeCalm` (2335) · Stealth
- `IGUI_ALJ_RelCheck_071_DoorTrader_Todo` (2381) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_071_DoorTrader_Expect` (2382) · Talk to, Cinematic, Classic
- `IGUI_ALJ_RelCheck_071_TradeTalk_Todo` (2384) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_071_TradeTalk_Expect` (2385) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_071_CreatorNames_Todo` (2417) · Set name
- `IGUI_ALJ_RelCheck_073_HoldupQ_Title` (2449) · Orders
- `IGUI_ALJ_RelCheck_073_HoldupQ_Todo` (2450) · Cinematic, Classic
- `IGUI_ALJ_RelCheck_073_HoldupQ_Expect` (2451) · Orders
- `IGUI_ALJ_RelCheck_073_HoldupMercy_Todo` (2459) · Hands up
- `IGUI_ALJ_RelCheck_073_HoldupRefused_Todo` (2465) · Hands up
- `IGUI_ALJ_RelCheck_Check_JournalNotice` (3695) · Log
- `IGUI_ALJ_RelCheck_080_Alife15Trade_Todo` (3698) · Personal
- `IGUI_ALJ_RelCheck_080_Alife15Trade_Expect` (3699) · Orders, Personal
- `IGUI_ALJ_RelCheck_080_Alife15Journal_Todo` (3701) · Log
- `IGUI_ALJ_RelCheck_080_Alife15Journal_Expect` (3702) · Log
- `IGUI_ALJ_RelCheck_080_Alife15Menu_Expect` (3711) · Talk to
- `IGUI_ALJ_RelCheck_Check_JournalTab` (3727) · Journal
- `IGUI_ALJ_RelCheck_Check_JournalSection` (3728) · Journal, Companions
- `IGUI_ALJ_RelCheck_Check_JournalSize` (3729) · Journal
- `IGUI_ALJ_RelCheck_081_JournalTab_Title` (3732) · Journal
- `IGUI_ALJ_RelCheck_081_JournalTab_Todo` (3733) · Journal
- `IGUI_ALJ_RelCheck_081_JournalTab_Expect` (3734) · Journal
- `IGUI_ALJ_RelCheck_081_JournalHome_Title` (3735) · Journal
- `IGUI_ALJ_RelCheck_081_JournalHome_Expect` (3737) · Journal
- `IGUI_ALJ_RelCheck_081_JournalPeople_Title` (3738) · Companions
- `IGUI_ALJ_RelCheck_081_JournalPeople_Expect` (3740) · Journal, Companions
- `IGUI_ALJ_RelCheck_081_JournalPortrait_Todo` (3742) · Journal
- `IGUI_ALJ_RelCheck_081_JournalPortrait_Expect` (3743) · Journal
- `IGUI_ALJ_RelCheck_081_JournalSchedule_Title` (3744) · Journal
- `IGUI_ALJ_RelCheck_081_JournalSchedule_Todo` (3745) · Tasks
- `IGUI_ALJ_RelCheck_081_JournalSchedule_Expect` (3746) · Journal
- `IGUI_ALJ_RelCheck_081_JournalBases_Title` (3747) · Journal
- `IGUI_ALJ_RelCheck_081_JournalBases_Expect` (3749) · Journal
- `IGUI_ALJ_RelCheck_081_JournalMissions_Title` (3750) · Journal
- `IGUI_ALJ_RelCheck_081_JournalMissions_Expect` (3752) · Journal
- `IGUI_ALJ_RelCheck_081_JournalReputation_Title` (3753) · Journal
- `IGUI_ALJ_RelCheck_081_JournalReputation_Expect` (3755) · Journal
- `IGUI_ALJ_RelCheck_081_JournalNews_Title` (3756) · Journal
- `IGUI_ALJ_RelCheck_081_JournalResize_Title` (3759) · Journal
- `IGUI_ALJ_RelCheck_081_JournalResize_Todo` (3760) · Journal
- `IGUI_ALJ_RelCheck_081_JournalRelayout_Title` (3762) · Journal
- `IGUI_ALJ_RelCheck_081_JournalRelayout_Todo` (3763) · Journal
- `IGUI_ALJ_RelCheck_081_JournalAlifeTabs_Todo` (3766) · Journal, Tasks, Contacts, Companions, Log, Settings
- `IGUI_ALJ_RelCheck_081_JournalAlifeTabs_Expect` (3767) · Journal
- `IGUI_ALJ_RelCheck_081_TalkOwnRows_Expect` (3775) · Come with me
- `IGUI_ALJ_RelCheck_081_CompanionRide_Todo` (3797) · Personal, Come with me
