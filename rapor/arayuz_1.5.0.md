# 1.5.0 arayüz farkları (kurulu mod 1.5.0 ↔ `kaynak/en/` 1.4.6)

Salt okuma; `kaynak/en/` ve `onayli/` değişmedi. Ayrıntı: `rapor/arayuz_1.5.0_IG_UI.json` (anahtar → EN, tür, kaynak dosya).

| Dosya | Eski | Yeni | Eklenen | Silinen | Değişen |
|---|---:|---:|---:|---:|---:|
| IG_UI | 2609 | 5226 | 2617 | 0 | 0 |
| Sandbox | 1119 | 1513 | 402 | 8 | 19 |
| UI | 4 | 11 | 7 | 0 | 0 |
| ItemName | 2 | 4 | 4 | 2 | 0 |

## IG_UI +2.617

- **66** zaten bizde: aynı anahtar ve metinle `IG_UI_lua`/`Creator_lua`'da, onaylı çevirisi var (mod artık bunları JSON'a da koyuyor).
- **29** yalnız büyük/küçük harf ya da noktalama farkıyla bizim Lua çevirilerimizde var (TAG/Tag, MOVING/Moving): mevcut çeviriden doldurulabilir (Claude, teknik).
- **68** metni onaylı bir diyalog satırıyla aynı (ziyaretçi paneli, sahne satırları…): mevcut Türkçeden doldurulabilir, bağlam kontrolüyle.
- **2454** gerçekten çevirisiz. Kaynak klasöre göre:

| Klasör | Satır | Örnek |
|---|---:|---|
| shared/ProjectALife/Radio | 559 | You brought Doctor Solheim her antibiotics · shhhh ... a voice, very far, counting ... shh · A woman called Ellie wants help for her husba |
| client/ProjectALife/Interface | 255 | Left behind · Sound: distant scream · frozen with fear |
| client/ProjectALife/UI2 | 238 | Nothing to copy · Last change · We suffer more often in imagination than in r |
| shared/ProjectALife/World | 201 | RAID ARRIVED · They are waiting outside, nervous · A helicopter with a crew aboard that circles  |
| shared/ProjectALife/Talk | 197 | Was it worth it · Strangers say no · Tell your friend to stay where I can see him |
| shared/ProjectALife/Missions | 194 | Walk out and report what is on the road · Find wire and a screwdriver to get a generato · They find someone else |
| shared/ProjectALife/Novelty | 128 | Folks say one of that crew went down {where}. · Those people lost somebody {where} this week, · Raid on, {waves} waves left |
| shared/ProjectALife/Companions | 121 | Now sees you as: {level} · Given · Urgent |
| ? (Lua'da birebir bulunamadı: birleşik/biçimli yazı) | 102 | {name}, {faction} · The whole baseline behavior package: prioriti · Optional |
| shared/ProjectALife/Ending | 97 | They marched you through the base under guard · You were executed. By morning, the courtyard  · Special Thanks to the Following |
| client/ProjectALife/Admin | 63 | Remove the selected batch · {n} h · Squad: free fire |
| client/ProjectALife/Tools | 41 | Clear marks · Nothing to copy yet · Builder: open window |
| shared/ProjectALife/Admin | 37 | QA dump · N · Blackbox dump |
| client/ProjectALife/Driving | 27 | In car · A player drives this car. · The straight line crosses {n} blocked or unlo |
| client/ProjectALife/Companions | 26 | Give · Complaints · Back to their items |
| shared/ProjectALife/Driving | 24 | Which way are you headed? I know the road · Pop the hood, I'll jump that battery · Costs standing |
| client/ProjectALife/Ending | 22 | Your record does not point to one clear role. · Animals killed: {animals}. · Factions met |
| shared/ProjectALife/Factions | 20 | Swap something with me · Do it before the offer lapses · Workers |
| server/ProjectALife/Offline | 17 | Heard {faction} sent people to find you · Engines, more than one, {faction} most likely · {faction} haven't forgotten what you did |
| client/ProjectALife/Dev | 13 | REC is for admins · SHINTO records single player only · REC saved {file} |
| client/ProjectALife/Radio | 9 | A call is going out on {mhz} MHz. You need a  · Voices on the air at {mhz} MHz. Turn your rad · Find a ham or military radio and turn it on |
| client/ProjectALife/Captives | 9 | They are marking it, give it a moment · Their tip led nowhere · You lost a prisoner |
| server/ProjectALife/Talk | 8 | Need another pair of hands · Take what you need · There are more of us |
| shared/ProjectALife/Outposts | 6 | Trader market yard · Military fort · Raider stronghold |
| shared/ProjectALife/Records | 5 | killed someone who went for you first, in sel · Doyle · Start settings applied |
| server/ProjectALife/Admin | 4 | patrolling · planned place · Blood |
| server/ProjectALife/World | 4 | Eyes on {place}, {dist} steps {dir} of you, g · You're almost on it, {place} is {dist} steps  · Movement at {place}, they're up and about, mi |
| client/ProjectALife/Builder | 3 | Open folder · Text · Role |
| client/ProjectALife/Talk | 3 | They're waiting at your gate, go out to it · Your fence has no gate they can reach · Talk to someone nearby |
| client/ProjectALife/Novelty | 3 | NOTE · Read the notice board · Read the note |
| server/ProjectALife/Novelty | 3 | Handwritten note · the locals · {name}'s bag |
| shared/ProjectALife/Audio | 2 | BREACH · text |
| shared/ProjectALife/Behaviours | 2 | east · south |
| client/ProjectALife/Audio | 2 | Silence phone · Take phone |
| server/ProjectALife/Behaviours | 1 | Insult them |
| server/ProjectALife/Activities | 1 | fleeing |
| shared/ProjectALife/ModLoot | 1 | hunting |
| server/ProjectALife/Combat | 1 | hiding |
| shared/ProjectALife/Visitors | 1 | person |
| shared/ProjectALife/Builder | 1 | h |
| shared/ProjectALife/Shells | 1 | hold fire |
| shared/ProjectALife/Captives | 1 | Come with me |
| shared/ProjectALife/Evolution | 1 | Tank |

Kapsam (K52, kullanıcı 2026-11-09): **hepsi çevrilir**, Radio ve Admin/Dev/Tools/Driving dahil.

Radyo kod yolu (1.5.0, okundu, oyunda denenmedi):
- Olay verisi (471, `Radio/Data/ALifeRadioEvent_*`) ve sohbet (84, `ALifeRadioChatter`) sunucuda `RadioRules.text → Text.ui` ile işlenir. Sonra dört yoldan oyuncuya gider: radyo cihazında yayın (`RadioLine`, Java), çağrı kartı (`radioCard`; istemci yalnız başlığı yeniden çevirir), olay sırasında NPC'nin sözü (`Speech.say` → istemcide `AudioPolicy.caption`), oyuncunun seçenekleri (`standoffAsk`).
- **Tek oyunculu:** sunucu ile istemci aynı; IG_UI.json'daki Türkçe dört yolda da görünür.
- **Özel sunucu:** bu metinler sunucunun dilinde işlenir. İstemcide çevrilen yalnız kart başlıkları ve `ALifeRadioClient`'ın 9 bildirimi. Ek seçenek: NPC sözü için aynı Türkçeyi `RD_ALifeLine_` anahtarıyla da teslim etmek (mevcut konuşma eki yakalar, {dist}/{dir}'li satırlar şablonla), kart metni ve seçenekler için istemci sarması. Radyo cihazındaki yayın yazısı büyük olasılıkla İngilizce kalır.
- Admin/Tools/Dev/Driving metinleri büyük ölçüde istemcide `Text.ui` ile çiziliyor (client klasörlerinde 171 çağrı); sunucu tarafındaki birkaç satır yine sunucunun dilinde.

## Sandbox

- **+402** yeni seçenek (ayar adı, tooltip, seçenekler).
- **−8** `PresetWorld` (yerine `PresetPopulation` geldi): eski çeviri teslimde kalırsa zararsız, temizlenebilir.
- **~19** değişen: 11 tooltip/seçenek metni (K26: `_surum_farki`, yalnız sayı değiştiyse otomatik) + 8 bölüm başlığı ("A-Life: EXPERT - …").

## UI +7 (tuş atamaları), ItemName +4 / −2

- UI: konuşma tuşu, cevap şeridi, günlük, manevra/Shinto kaydedici (7).
- ItemName: JS-5 SMG ve şarjörü, M60 ve 100'lük şerit kutusu. Bizim L4'te çevirdiğimiz `Base.PALServiceRifle`/`PALServiceClip` (M16A2) modda artık yok.

## Önerilen paketler (Claude çevirisi, her biri ayrı sohbet, K26 B paketleri)

1. **B5 (küçük, ≈40):** UI 7 + ItemName 4 + araç adları 2 + Sandbox 19 değişen; Sandbox'tan kalkan 8 ve ItemName'den kalkan 2 temizliği.
2. **B6:** Sandbox +402.
3. **B7:** IG_UI'de mevcut çeviriden dolan 97 (29 harf farkı + 68 diyalog metni), teknik.
4. **B8…:** IG_UI 2.454 yeni, klasör gruplarıyla ≈300'lük paketler; Radio ve Admin/Dev/Tools kapsam kararından sonra.

**B8'den önce `lua_cikar` ve `creator_cikar` 1.5.0 için yeniden çalıştırılmalı:** IG_UI_lua'nın 31'i ve Creator_lua'nın ≈811'i 1.5.0 Lua'sında birebir bulunamadı; yeniden yazılmış hâlleri bu 2.454'ün içinde olabilir (aynı metin iki kez çevrilmesin, eski çeviri kullanılabilsin).

`kaynak/en/` 1.5.0'a ancak B5 onaylanırken yenilenir (son_kontrol yeni anahtarları eksik sayar).
