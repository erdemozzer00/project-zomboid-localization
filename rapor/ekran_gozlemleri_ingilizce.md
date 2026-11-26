# Project A-Life 1.5.2 · Ekranda kalan üç İngilizce dize

19 Kasım 2026 · İki ekran görüntüsü, kurulu A-Life Lua kodu, L152 sonrası teslim ve iki yerel TR kopyası incelendi. Görüntülerdeki metinler doğrulandı. Görüntülerin çekildiği mod kopyası, ayarlar ve varsa sunucu sürümü bilinmiyor.

Takip incelemesinde noktalı takas düğmesi kurulu **Project A-Life - Jeem Extension** eklentisinde yeniden üretildi. Eklenti son oyun günlüğünde ve son iki yerel tek oyunculu kaydın mod listesinde etkin.

| Görüntü | Kaynak ve neden | Mevcut Türkçe | Teslim yöntemi ve oyun kontrolü |
|---|---|---|---|
| Stephanie Porter · **Bring me cloth, the cleaner the better** | `ALifeTaskBoardText.lua:243`, `TB_FIND_CLOTH.pitch / any`. İki olası açılış repliğinden biri. Eski ham taramada var, E1 seçkisinde ve L152'de yok. | **Bana bez getir. Ne kadar temiz olursa o kadar iyi.** `RD_ALifeLine_3eea49c114c68909` yerel yamaya eklendi. | Genel görevden temiz bez isteğini açıp bu repliği panelde ve konuşma balonunda kontrol et. |
| Juan Reed · **No problem, we'll ration** | `ALifeTaskBoardText.lua:57`, `TB_BRING_WATER.no / any`. Su teklifini reddedince çağrılıyor. Eski ham taramada var, E1 seçkisinde ve L152'de yok. | **Sorun değil, suyu idareli kullanırız.** `RD_ALifeLine_21c8289d75fa3bc7` yerel yamaya eklendi. | Su teklifinde yardım edememe seçeneğine bas. Oyuncu yankısını ve NPC'nin cevabını panelde ve balonda kontrol et. |
| Juan Reed · **Let's trade.** | Jeem Extension 0.8.3, `HandGifts/Choice.lua:105–113`. `ASK_TRADE` seçeneğini kendi metniyle değiştiriyor. `Services/TalkPool.lua` satırı Konuş sekmesinin başına alıyor. | Jeem'in `IGUI_ALJ_Trade_AskChoice` anahtarı için Türkçe eksik. Ana A-Life'ın noktasız ağaç satırında **Takas yapalım** mevcut. | Jeem'in özgün IG anahtarıyla Türkçe ver. Jeem etkin ve Türkçe seçiliyken Konuş sekmesinin ilk düğmesini, tıklama yankısını ve açılan takas penceresini kontrol et. |

## İki NPC repliği nasıl gösteriliyor?

- `ALifeTaskBoardData.lua:135–143,325–331` su ve bez isteklerini tanımlıyor. `ALifeTaskBoardRows.lua:31–49,78–88,122–154` bunların konuşma satırlarını kaydediyor. `dialogue5_lines` açıkken ikisi de `request`. Bez teklifi `TB_ASK_FIND_CLOTH → Board.handleAsk → TB_FIND_CLOTH.pitch`. Su teklifi, `TB_REQ_CANT → Board.handleDecline → TB_BRING_WATER.no` ile kapanır. Ayrım kapalıyken genel `TB_NO` da aynı reddetme işleyicisine gider. Görevi verenin grubu, itibar, açık teklif ve süre seçim koşullarının parçası.
- `ALifeTaskBoardText.lua:291–310` içindeki `Text.merge`, konuşma bankasını `FactionTalkLines.sets` içine kaydeder. `ALifeTaskBoard.lua:421–427` anahtarı kurar, `Board.say → HS.say → FactionTalkServer.say → FactionTalk.recordsFor → Talk.speak` çalışır. `HS.say` düşük itibarda önce `.low` arar. Bu bankada `.low` girdisi yok. `recordsFor` grup havuzu varsa onu, öbür durumda `any` havuzunu kullanır. `Talk.speak`, seçilen ham metni `Speech.render` ile doldurur, `Speech.say` çağırır ve doldurulmuş metni döndürür. Kaynaklar `ALifeTalkRowHookServer.lua:39–45,97–122`, `ALifeFactionTalk.lua:223–230`, `ALifeFactionTalkServer.lua:52–59` ve `ALifeTalk.lua:518–543`.
- **NPC altyazısı ve balon.** `Speech.say → AudioPolicy.caption` ve yerel `draw` yolu RD anahtarına ulaşır. MP'de `speech` yükü istemcide `Speech.onServerCommand → draw → caption` yoluna gider. Konuşma sonucu ayrıca `Talk.choose → talkResult → TalkMenu.receive → panel:append` hattından paneli besler. UI2'nin `W:append` metodu da `caption` çağırır ve `npcLine` üzerinden altyazıyı gösterir. `ALifeTR_Konusma.lua:338–352,669–679` o anda gelen dizenin tam RD anahtarını arar. Kaynaklar `ALifeSpeech.lua:845–858,1295–1389,1480–1490`, `ALifeTalk.lua:1274–1279,1652–1663`, `ALifeTalkMenu.lua:1020–1029,1084` ve `ALifeUI2Talk.lua:304–326,1159–1235`.
- **Oyuncunun görev seçeneği.** `Hook.register → TalkIntents.addChoice` satır metnini kaydeder. Sunucudan açılan kimlikler `UI2TalkHook.rowsFor` ile seçkiye girer. `W:buildButtons` normal satır için `Intents.choiceLabel → Talk2.text → Text.ui` ile IG anahtarını kullanır. Seçim tıklanınca temel `Window:choose` düğmenin çevrilmiş `spokenText` değerini yankılar ve `talkChoose` ile kimliği gönderir. Örneğin kurulu sürümün `TB_REQ_WORTH` satırındaki `What's it worth to you?` teslimde **Karşılığında ne verirsin?**. Ekran görüntüsündeki **Bunun için ne verirsin?** metni güncel teslimde birebir bulunmadı. Türkçe düğmelerin varlığı NPC repliğinin RD anahtarını doğrulamaz. Kaynaklar `ALifeTalkRowHook.lua:41–56`, `ALifeUI2TalkHook.lua:16–30,62–81`, `ALifeUI2Talk.lua:165–204`, `ALifeTalkIntents.lua:391–394` ve `ALifeTalkMenu.lua:650–679`.

## Ham taramadan teslimata nerede elendiler?

`ceviri_bosluk_tara2.json` her iki dizenin dosyasını ve güncel karşılaştırmada da tutan 57 ve 243 konumlarını kaydetmiş. İkinci tarama bilinen metinleri normalleştirilmiş dizeyle eliyor. Bu aşama arama dizini üretiyor. E1'i hazırlayan `hazirla_bosluk.gorunur` ise yol beyaz listesi kullanıyor. `Talk/Data`, ağaçlar, doğrudan `Talk/` altındaki bazı dosyalar ve `ALifeFollowBLines.lua` içeri alınıyor. `shared/ProjectALife/Missions/ALifeTaskBoardText.lua` bu kuralların hiçbirine girmiyor. E1 haritasında bankayla dört tam eşleşme, **hepsi `ALifeTalkRowLines.lua` üzerinden**, var. Bunların ikisi bugün çağrılan `TB_GEN.none` replikleri, ikisi çağrısını bulamadığım `TB_GEN.busy` replikleri. Bez ve su ekran replikleri E1 haritasında hiç yok. [Paket seçici](../araclar/harici_paket.py#L864) · [E1 haritası](../paketler/haritalar/E1_harita.json) · [10 Kasım arşivi](../notlar/arsiv/2026-11-19/ILERLEME.md#L51)

L152'deki 45 NPC repliği Left Behind Dell/Wade akışından. Bankanın 302 metni ile 540'lık L152 manifesti arasında birebir EN eşleşmesi sıfır. Aktarılan 524 anahtarın haritalarıyla da eşleşme sıfır. L152'nin konuşma uyarlaması yalnız kendi Dell kalıplarını ve belirli eklerini tanır. Genel görev kartı ve sonuç bildirimi için yaptığı sunum değişiklikleri de `Board.say` havuzuna anahtar kazandırmaz. [L152 kapanışı](../notlar/arsiv/2026-11-26/ILERLEME.md) · [L152 manifesti](../notlar/arsiv/2026-11-19/fable-dosyalari/L152_HAZIRLIK_540.json) · [L152 Lua eki](../araclar/lua/ALifeTR_L152.lua#L115)

## Genel görev bankasında kalanlar

Kurulu 30 görev tanımı, `Board.say` çağrıları ve görevi verebilen gruplarla karşılaştırınca 302 tekil girdinin **296'sı** çağrıya bağlanıyor. Bunlar uygun oyun koşulunda seçilebilen havuz girdileri. Örneğin `own` tarzı görev türüne ve çantadaki eşyalara, rapor ve takip satırları açık bir göreve bağlı. `TB_GEN.busy`, `TB_GEN.quit`, `TB_GEN.sit` başına iki metin kayıtlı. Bu üç havuzun çağrısı bulunmadı. Görevi bırakma `TB_GEN.quit` yerine görev özelindeki `.lapse` havuzuna gidiyor. İlk incelemede bankanın tamamında yedi RD vardı. İkisi çağrısız `busy` grubunda, beşi çağrılan havuzlarda. [TB_EKRAN](../paketler/TB_EKRAN.md) ile çağrılan havuzlara iki RD daha eklendi. Bu 296 metin içinde IG'de bulunup RD'si eksik olan yok. Eski ham taramada bu dosyadan 297 banka metni var. Bunların 291'i bugün çağrılan havuzlarda.

| Dal | Yeni sabit RD | Yeni değişkenli | Mevcut RD | Ne zaman |
|---|---:|---:|---:|---|
| `pitch` | 26 | 39 | 1 | Teklifin açılışı, `any/law/mil`. Örneğin bez isteği ve `There's a house near {where} full of them, I can't use the road till it's empty`. |
| `yes` | 30 | 0 | 0 | Teklif kabulü. `own` yolu `TB_GEN.own` ile cevaplanır. |
| `no` | 29 | 0 | 1 | Teklif reddi. Su isteği dahil. |
| `nudge` | 59 | 1 | 0 | İşin durumunu sormak. Değişkenli örnek `Any sign of {name}`. |
| `done` | 57 | 0 | 3 | Görevi verene sonuç bildirmek veya teslim etmek. |
| `lapse` | 35 | 0 | 0 | Üstlenilmiş görevi konuşmada bırakmak. Otomatik sona erme ayrı bildirim yolu. |
| `TB_GEN` | 13 | 0 | 2 | `how` 4, `missing` 2, `own` 2, `stale` 2, `worth` 3. `none` grubundaki iki karşılık mevcut. |
| **Toplam** | **249** | **40** | **7** | **296 tekil çağrılabilir metin.** |

TB_EKRAN öncesinde mevcut beş karşılık `I'm glad they're safe`, `That's exactly what we needed, thank you`, `The kids will eat well tonight`, `Nothing right now, ask me later` ve `No work today, come back another time`. Bu beş satır ve TB_EKRAN'ın iki repliği yeni Fable paketine tekrar girmez.

- **Tek başına gelen sabit replik.** Tam EN dize ile `RD_ALifeLine_` anahtarı oluştur. Yeni anahtarı `RadioData_lua` ve kaynak konumu ile `harici_paket.py al → paket_kontrol.py` akışına bağla. Aktarım onayı sonrası `onayla.py → son_kontrol.py → workshop_kur.py`. Bu iki ekran repliğine IG kopyası eklemek gerekmiyor.
- **Birleştirilen sabit parçalar.** `dialogue5_lines` açıkken 11 sabit ve 38 değişkenli **iş** teklifi `TB_GEN.how` ile birleşebilir. `Board.handleAsk` iki parçayı ayrı ayrı söyletir, paneldeki sonuç için `pitch .. "... " .. how` döndürür. Parçaların RD anahtarı balon yolunu karşılar. Birleşik panel cevabı için genel görev teklifinin çıkışında ya da o sonuca özel istemci sunumunda aynı iki parçayı ayrı çevirmek gerekir. 16 sabit ve bir değişkenli **istek** teklifi bu birleşimi kullanmaz. [Önceki görev raporu](ingilizce_metin_ve_guvenli_ceviri_yollari.md#L33)
- **Önceden doldurulan kalıplar.** 36 yalnız `{where}`, iki yalnız `{name}`, iki ikisini birden içeriyor. `ALifeTaskBoardRules.lua:396–411` yer türünü, yaklaşık mesafeyi, yönü ve varsa kasaba tarifini `{where}` içine İngilizce yerleştiriyor. Yer bulunmazsa `out there` geliyor. `Talk.speak` ardından bunu gövdeye dolduruyor. Dolu metnin hash'i ham kalıptan farklı. Yalnız genel görev replikleri için, seçilmiş kalıp ve alanları henüz ayırmak mümkünken işaretleyip istemcide RD kalıbını doldurmak güvenli bir sonraki adım. Panel ve balon alıcıları aynı kalıp kimliği ve alanları kullanabilmeli. Konum, NPC adı, koşul, istemci dili ve EN geri dönüşü korunmalı. `{where}` içinde İngilizce kalmaması için yer/yön kalıbını da ele almak gerekiyor. Mevcut genel şablon eşlemesi kimi `{name}` kalıplarını yakalayabilir. `{where}` için doğrulanmış bir yer tarifi işleyicisi sağlamıyor, serbest yakalama İngilizce yer bilgisini geri koyabilir ve alanın satır başı/sonunda olduğu örnekleri çıkarıcı atlayabilir. [Şablon üreticisi](../araclar/sablon_varyant.py#L119) · [Mevcut konuşma eşleyicisi](../araclar/lua/ALifeTR_Konusma.lua#L228)

### Tekrar üretme

Proje kökünde Python ve Lupa ile çalıştır. `MOD` kurulu ana modun Lua kökü. Özgün tabloyu Lua'da çalıştırır, kullanım koşullarını çağrılardan çıkarır, ardından her metni konumu, çağrı havuzu, grup, hash ve durumu ile yazdırır. Sonuç standart çıktıya gider. Raporun anlık sayıları yukarıda.

```python
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

from lupa import LuaRuntime

sys.path.insert(0, "araclar")
from lua_cikar import MOD
from lua_dize import dizeler

def read(path):
    return Path(path).read_text(encoding="utf-8-sig")

def read_json(path):
    return json.loads(read(path))

missions = MOD / "shared/ProjectALife/Missions"
bank = missions / "ALifeTaskBoardText.lua"
source = read(bank)
board = read(MOD / "server/ProjectALife/Missions/ALifeTaskBoard.lua")
per_task = set(re.findall(r'Board\.say\(ctx, Board\.keyFor\([^,]+, "(\w+)"\)', board))
general = set(re.findall(r'Board\.say\(ctx, "(TB_GEN\.\w+)"', board))

lua = LuaRuntime()
lua.execute("require=function() end; ProjectALife={FactionTalkLines={sets={}}}")
for path in (MOD / "shared/ProjectALife/Core/ALifeText.lua",
             missions / "ALifeTaskBoardData.lua", bank):
    lua.execute(read(path))
p = lua.globals().ProjectALife
tasks = {"TB_" + task.id.upper(): task for task in p.TaskBoardData.tasks.values()}
uses = defaultdict(list)
for pool, variants in p.FactionTalkLines.sets.items():
    prefix, branch = pool.split(".")
    task = tasks.get(prefix)
    groups = set(task.giver.values()) if task is not None else set()
    for variant, lines in variants.items():
        if variant == "any":
            eligible = any(variants[group] is None for group in groups)
        else:
            eligible = variant in groups
        called = pool in general or (branch in per_task and eligible)
        for text in lines.values():
            uses[text].append((pool, variant, called))

approved = {key for f in Path("onayli").glob("*.json") for key in read_json(f)}
rd = read_json("teslim/RadioData.json")
ig = read_json("teslim/IG_UI.json")
l152 = {row["en"] for row in read_json("notlar/arsiv/2026-11-19/fable-dosyalari/L152_HAZIRLIK_540.json")["rows"]}
l152_keys = {row[0] for kind in ("IG", "RD") for row in
             read_json(f"paketler/haritalar/L152_{kind}_harita.json")["satirlar"].values()}
locations = defaultdict(list)
for pos, text in dizeler(source):
    if text in uses:
        locations[text].append(source.count("\n", 0, pos) + 1)

counts = Counter()
for text, refs in sorted(uses.items(), key=lambda item: min(locations[item[0]])):
    digest = p.Text.hash(text)
    rd_key, ig_key = "RD_ALifeLine_" + digest, "IGUI_ALifeUI_" + digest
    active = [f"{pool}/{group}" for pool, group, called in sorted(refs) if called]
    if not active:
        status = "cagrisiz"
    elif text in l152 or {rd_key, ig_key} & l152_keys:
        status = "L152"
    elif rd_key in approved or rd_key in rd:
        status = "RD mevcut"
    elif ig_key in approved or ig_key in ig:
        status = "IG mevcut - baglam kontrolu"
    else:
        status = "yeni kalip" if "{" in text else "yeni sabit"
    counts[status] += 1
    pools = active or [f"{pool}/{group}" for pool, group, _ in sorted(refs)]
    print(*locations[text], "|", ", ".join(pools), "|", status, "|", rd_key, "|", text)

print(len(uses), dict(counts))
```

## Noktalı takas seçeneği

### Kaynak doğrulaması

Steam Workshop `3806944055` altındaki **Project A-Life - Jeem Extension**, mod kimliği `ProjectALifeJimmy`, sürüm `0.8.3`. `Features/HandGifts/Choice.lua:33–42,105–113` mevcut `ASK_TRADE` satırını değiştirip etiketi `J.t("IGUI_ALJ_Trade_AskChoice")` ile alıyor. EN sözlüğündeki 2635. satırın değeri **Let's trade.**. `Services/TalkPool.lua:22–23,68–76,84–99,118–128` uygun NPC için bu satırı `Personal` yani Konuş seçkisinin başına taşıyor. Böylece hem nokta hem görüntüdeki ilk sıra açıklanıyor. `console.txt:2006` modun yüklendiğini gösteriyor. Son Outbreak ve Sandbox kayıtlarının `mods.txt` dosyalarında da ana A-Life ve TR yamasının yanında Jeem var. 10 Kasım'daki eski gözlemin mod kopyası ayrıca doğrulanmadı.

Jeem'in kurulu sözlüğünde TR dizini yok ve `IGUI_ALJ_Trade_AskChoice` mevcut Türkçe teslimde bulunmuyor. `Core.lua:2476–2509` bu sabit anahtarı oyun çeviri aramasından alıyor. Güvenli uyumluluk yolu Türkçe IG sözlüğüne doğrudan **`IGUI_ALJ_Trade_AskChoice`** karşılığını vermek. A-Life metin hash'i veya konuşma kancası değişikliği gerekmiyor. Kapıda görülen aynı İngilizce etiketi `JIMMY_DOOR_TRADE` ve `IGUI_ALJ_Traders_DoorTrade` kullanıyor. Görüntüdeki düğmenin anahtarı `Trade_AskChoice`. [Seçenek kaydı](<C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3806944055/mods/ProjectALifeJimmy/42/media/lua/shared/ProjectALifeJimmy/Features/HandGifts/Choice.lua:105>) · [Sekme yerleşimi](<C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3806944055/mods/ProjectALifeJimmy/42/media/lua/client/ProjectALifeJimmy/Services/TalkPool.lua:118>)

### Ana A-Life karşılaştırması

1. **Kurulu ağaçta kaynak ve normalizasyon.** `social_trade_suspicious` temkinli bir tüccar için `tab = "trade"`. `TreeRegistry.tabs` bunu `Trade` yapar. Sunucu `TreeServer.offerFor → E.offer` ile `prompt` metnini doldurur, `E.clean` ile uç boşlukları ve tek son noktayı kaldırır. Ardından `dlgTrees.offer` içine temiz metin ve kimliği koyar. Ağaç içi oyuncu seçiminde `E.nodeView` aynı temizliği önce yapar, gerekirse `[Charm] ` önekini sonra ekler. `.. / ...` bu tek-nokta temizliğinin kapsamı dışında. Kaynaklar `ALifeTreeRegistry.lua:16,492`, `ALifeTreeServer.lua:344–356,1561–1565` ve `ALifeTreeEngine.lua:383–428,478–499`.
2. **UI2 düğmesi, çizim ve yankı.** `UI2TalkTrees.receive → C.takeOffer → C.promptRows` teklifleri sekmesiyle alır. Ağaç içi seçim `runRows` üzerinden gelir. İki yol `visitor=true` verir ve TR eki yalnız bu satırların EN gövdesinde tam RD anahtarını arar. `W:buildButtons` bu satırın `text` değerini doğrudan etiket ve `spokenText` yapar. `UI2Talk.measureRows → TalkLook.layout` metni sarar. Bu zincirde tek son nokta ekleyen işlem bulunmadı. `C.choose` çevrilmiş `choice.text` değerinden varsa `[Charm] ` önekini çıkarıp `append(..., "You")` ile yankılar. `treeStep` ile metin yerine ağaç kimliği ve gerekiyorsa seçim indeksi gider. Normal genel görev düğmesi farklıdır ve `Text.ui` ile IG kullanır. [Mevcut ağaç eki](../araclar/lua/ALifeTR_Konusma.lua#L509)
3. **Benzer takas satırları.** Güncel genel görev satırlarında noktalı seçenek yok. `T6_TRADE` “Got anything to trade?”, `ASK_TRADE` “Have you got anything to trade?” ve kapı takası `DOOR_TRADE` “What have you got to trade?” ile farklı kimliklere ve metinlere sahip. Örneğin `REPL_TRADE` üslup seçeneği “People say I deal straight, so let's trade fair” diye başlıyor. Ağaç fırsatları `Trade` sekmesine eklenir. Classic'in `classicRows` yolu bazı başka sekme tekliflerini `Personal` içine taşıyabilir, ancak aynı temizlenmiş metni kullanır. Bazı ziyaretçi/kapı karşılaşmalarında UI2 zaten Classic'e yönlendirir. Görüntüdeki dört seçenekli UI2 görünümünde Konuş sekmesinin seçili olması ve son nokta, aday ağacı o satırla eşleştirmeye yetmiyor.
4. **İlk incelemedeki TR kopyaları.** İki yerel TR kopyası `2.00` yazmasına rağmen abone önbelleği 8.502 IG ve 117.125 RD anahtar, yükleme klasörü 8.981 IG ve 117.170 RD anahtar içeriyordu. Abone kopyasında L152 eki yoktu. Noktasız takas karşılığı ikisinde de vardı, Jeem anahtarı ikisinde de eksikti.

## Denemeler ve ilk Fable paketi

- **Bellek içi Lua.** Gerçek `Board.handleAsk/handleDecline`, `HS.say`, grup havuzu, `Talk.speak`, metin doldurma ve UI2 `append` ile iki NPC metni İngilizce çıktı. Oyun nesneleri, replik seçimi ve balon çıkışı test ikamesiydi. Yalnız ilgili iki RD anahtarına geçici test değeri verince hem balonun çeviri girişinde hem panelde değer değişti. `{where}` örneğinde yalnız ham kalıba geçici anahtar ekleyince doldurulmuş çıktı İngilizce kaldı. L152 konuşma kalıbı bu örneğe eşleşmedi.
- **Takas denemesi.** Jeem'in gerçek `Choice` ve `TalkPool` modüllerini, özgün `J.t` fonksiyonunu ve A-Life'ın UI2 düğme/tıklama işleyicilerini test ortamında birlikte çalıştırdım. Temel liste ve oyun nesneleri test ikamesiydi. Noktalı **Let's trade.** Konuş sekmesindeki ilk satırda çıktı ve tıklama yankısında aynı kaldı. `talkChoose` komutunun seçimi `ASK_TRADE` oldu. Yalnız `IGUI_ALJ_Trade_AskChoice` anahtarına geçici test değeri verilince düğme ve yankı birlikte değişti, seçim kimliği korundu. Ayrı ana A-Life ağaç denemesinde noktasız seçenek mevcut Türkçe karşılığını kullandı. Takas penceresi canlı oyunda açılmadı.
- **L152 kontrolü.** Mevcut beş L152 Lua testi geçti. Bu incelemede canlı oyun oturumu ve MP açılmadı. Oyun doğrulamasında iki istek için Türkçe düğme/yankı, NPC panel altyazısı ve balon, ardından EN geri dönüşü kontrol edilmeli. MP'de ayrıca sunucu `speech` ve `talkResult` yüklerinin Türkçe istemcideki iki yüzeyi denenmeli.
- **Genel görev paketleri.** Ekrandaki iki repliği Erdem'in isteğiyle Codex çevirdi ve [TB_EKRAN](../paketler/TB_EKRAN.md) olarak yerel Workshop paketine işledi. Bez ve su görevlerinin diğer 16 repliği dahil kalan **289 metin**, dört Fable TXT'siyle **TB_GENEL** paketine alındı. Hedef `RadioData_lua`. [Paket haritası ve teknik satır işaretleri](../paketler/haritalar/TB_GENEL_harita.json)

## Eski tahliye harita sembolü

| Gösterim | Neden İngilizce kalıyordu | Lua bağlantısı ve Türkçe |
|---|---|---|
| Harita simgeleri kapalıyken tahliye hedefinin turuncu metin sembolü | `ALifeEndingDirector.lua:447` özgün metni `ending_zone` kartıyla gönderiyor. `ALifeRadioClient.lua:224–232` bunu `SafehouseClient.mark` işlevine geçiriyor. `ALifeSafehouseClient.lua:654–678` simgeler kapalıyken doğrudan vanilla sembolü ekliyor. Simgeler açıkken kullanılan `MapLabels.tipLines` bu çizime uğramıyor. | Yalnız `ending_zone` ve özgün `Extraction zone` eşleşince eski sembolün metni için `IGUI_ALifeUI_475db47e671e428c` kullanılıyor. Mevcut karşılık **Tahliye bölgesi**. Sembolün ham anahtarı kaldırma işleminde de kullanılıyor. Paket yapıcısı bu tek anahtara doğrulanmış İngilizce geri dönüşü ekliyor. |

Semboller iki gösterim biçiminde de özgün konumlarıyla oluşturulur. Aynı tahliye kartı tekrar işlendiğinde aynı konumdaki önceki biçim temizlenir. Diğer radyo kartları özgün yoldan gider. Harita açıldığında önceki kayıttaki ham İngilizce işaret, yalnızca bilinen tahliye konumu, özgün başlık, turuncu renk ve ölçek eşleşirse çeviri anahtarına taşınır. Testte aynı adlı ve aynı konumdaki farklı biçimli oyuncu notu korundu.

Kurulu `RadioClient`, `SafehouseClient` ve `MapLabels` Lua modülleriyle bellek içi testte tekrar gönderim, iki yönde simge geçişi, eski kayıt, tahliye işaretinin kaldırılması ve İngilizce geri dönüş sınandı. Java sembol API'si test ikamesiydi. Kurulu oyunun `WorldMapTextSymbol` sınıfında çeviri araması `Translator.getText` kullanıyor. 14 dosyalık deneme paketi üretildi. Yerel yayın klasörü onay öncesinde güncellenmedi.
