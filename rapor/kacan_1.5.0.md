# Kaçan metin taraması (Lua → JSON karşılığı olmayan, ekrana çıkan İngilizce)

Üretici: `araclar/kacan_tara.py` (salt okuma). Ayrıntı: `rapor/kacan_1.5.0.json`. Kapsam: ekran çağrısı bağlamındaki dizeler;
Text.ui/forPlayer/show içindekiler `lua_cikar.py` ile zaten kapsanır. **Aday** = bilinen kümelerde (mod EN JSON'ları, IG_UI_lua, Creator_lua,
RadioData_lua, bekleyen Y/G paketleri) olmayan dize; her aday gerçekten ekranda görünmez, kategoriye bakın.

**Önceki tarama (2026-11-03, 1.4.6, `rapor/atlanan_metinler.md`) ile fark:** o günün B grubu (≈412 NPC konuşması: Gossip, PlanData, InjuryRules, Panic…) ve
C grubu (≈59 arayüz mesajı) sonradan çeviri yoluna alınmış (RadioData_lua/IG_UI_lua kaynağında ya da D/G haritalarında), bu taramada aday değil. A grubu (ses altyazıları) hâlâ kapalı
(`npcAudioEnabled = false`). Yeni bulgular aşağıdaki `diyalog` ve `yonetici_arayuzu` kategorileridir: JSON'a girmemişler ve ilk bakışta
`Text.ui`'den geçmeden çiziliyor (ör. bitiş telsiz konuşması sunucuda `Call.fill` ile ham gönderiliyor). Çevirileri için konuşma eki
(`RD_ALifeLine_`) ya da yapımcıya bildirim gerekebilir; kod yolları tek tek doğrulanmadı, oyunda denenmedi.
`Talk/ALifeTalkOrderRows` ve `HomeLeaveRows` adayları `lua_cikar` çıktısıyla (rapor/cikarici_yeni_1.5.0.json) kapsanır.

| Kategori | Aday | Görünür mü | Açıklama |
|---|---:|---|---|
| ses_altyazisi | 2998 | hayır | ses profili/klip altyazısı: AudioPolicy.npcAudioEnabled = false (1.5.0'da da sabit), yalnız NPC sesi açılırsa görünür |
| ic_not | 1445 | hayır | geliştirici notu/iç kimlik/yönetici günlüğü satırı: oyuncuya çizilmez ya da yalnız konsol/log |
| ozel_isim | 124 | hayır | destekçi/katkı sahibi adları: çevrilmez |
| yonetici_arayuzu | 396 | evet | yönetici/geliştirici/Oluşturucu arayüzü (K52 kapsamı), Text.ui'den geçmeden çiziliyor |
| diyalog | 60 | evet | oyuncu/NPC sözü, görev/olay metni ya da bitiş verisi |
| oyuncu_arayuzu | 12 | evet | oyuncu ayar/menü/bildirim metni |
| belirsiz | 40 | ? | elle bakılmalı |

## Görünür kategorilerde dosya dökümü

### diyalog

| Dosya | Aday | Örnek |
|---|---:|---|
| `Ending/ALifeEndingData.lua` | 12 | Louisville hospital · Louisville General Hospital |
| `Situations/ALifeSituationsData.lua` | 12 | Encircled depot · Sheriff checkpoint |
| `Shells/ALifeAnimations.lua` | 10 | Surrender · Wave |
| `World/ALifeSafehouseEvents.lua` | 10 | A note from {faction} · A warning |
| `Ending/ALifeEndingCallData.lua` | 7 | US Military · Captain Ruiz |
| `Talk/ALifeParty.lua` | 6 | Scout the building marked on your map, t · Bring the group  |
| `Missions/ALifeMissionDefs.lua` | 3 | Dell Tolliver's crew dropped their bags  · Get to the {place} |

### yonetici_arayuzu

| Dosya | Aday | Örnek |
|---|---:|---|
| `Admin/ALifeSpawnPlan.lua` | 113 | Faction squad · A squad drawn from one faction's members |
| `Admin/ALifeSpawnerPanel.lua` | 26 | Back to Spawn · Reset to defaults |
| `Driving/ALifeDrivingPanel.lua` | 26 | Center on me · Center on car |
| `Admin/ALifeCleanupWindow.lua` | 25 | CLEANUP A-LIFE · What to remove |
| `Builder/ALifeBuildWindow.lua` | 22 | Drag area in world · Pick anchor |
| `Interface/ALifeEncounterConsole.lua` | 21 | SPAWN ENCOUNTER + SQUAD · ADVANCED OPTIONS  > |
| `Admin/ALifeAdminActions.lua` | 21 | Status, quick actions, recent spawns · Full spawn form |
| `Outposts/ALifeOutpostTemplateData.lua` | 19 | Toll chain · Toll gate |
| `Driving/ALifeDrivingCrewPicker.lua` | 17 | Get in & drive · Detach crew |
| `Builder/ALifeStampWindow.lua` | 13 | Refresh list · Load file |
| `Outposts/ALifeOutpostTemplateV2Raid.lua` | 9 | Chain gate · Chain gate with booth |
| `Driving/ALifeDrivingPresetPanel.lua` | 8 | Save as new · Update saved preset |
| `Driving/ALifeDrivingTuningPanel.lua` | 7 | Applied to this car. Planner changes may · <TEXT> Car  |
| `Admin/ALifeAdminTabOverview.lua` | 6 | QUICK SPAWN · QUICK ACTIONS |
| `Outposts/ALifeOutpostTemplateV2State.lua` | 6 | Guard-shack post · Walled forward post |
| `Admin/ALifeAdminTabReputation.lua` | 5 | Make hostile · Back to baseline |
| `Interface/ALifeStatusWindow.lua` | 4 | Project A-Life Status · Heaviest per tick (ms):  |
| `Outposts/ALifeOutpostTemplateV2Folk.lua` | 4 | Homestead · Farm with barn |
| `Outposts/ALifeOutpostTemplateV2Grand.lua` | 4 | Walled base · Walk-in clinic |
| `Admin/ALifeAdminWindow.lua` | 3 | A-Life Admin · Find any control. Click a result to run  |
| `Admin/ALifeDebugSpawner.lua` | 3 | Staffed outpost:  · More advanced spawning: Admin Console >  |
| `Admin/ALifeSpawnerBrowser.lua` | 3 | Let the server pick the cast. · Click to fold or unfold this group. |
| `Builder/ALifeBuildSession.lua` | 3 | A free text note for whoever reads the b · Save failed:  |
| `Admin/ALifeAdminConsole.lua` | 2 | Opens the read-only settings browser wit · Opens the spawn tab with this search in  |
| `Admin/ALifeAdminTabCars.lua` | 2 | Advanced · NEW CAR |
| `Admin/ALifeAdminTabDiagnostics.lua` | 2 | STATE · Module table:  |
| `Admin/ALifeAdminTabPopulation.lua` | 2 | NEAREST NPCS · CENSUS |
| `Admin/ALifeAdminTabSettings.lua` | 2 | Sandbox options browser · Every A-Life option with its value, defa |
| `Admin/ALifeAdminTabWorld.lua` | 2 | WORLD STATE · BASE VISIT |
| `Builder/ALifeStampClient.lua` | 2 | Preview this exact target first (step 3) · Will place  |
| `Companions/ALifeCompanionSheetAdmin.lua` | 2 | Open the companion sheet: stats, tasks,  · The companion sheet lists the survivors  |
| `Interface/Creator/ALifeCreatorCore.lua` | 2 | CATALOG ERROR:  ·  ATTACHED TO THIS WEAPON |
| `UI2/ALifeUI2QuickSpawn.lua` | 2 | Cursor · 30 ahead |
| `Admin/ALifeAdminTabCleanup.lua` | 1 | Scan first. Nothing is deleted until you |
| `Admin/ALifeAdminUI.lua` | 1 | Pin to the toolbar (up to  |
| `Admin/ALifeGmPlan.lua` | 1 |  .. tostring(entry.note or  |
| `Admin/ALifeStartApplyClient.lua` | 1 | Start settings request finished |
| `Builder/ALifeBuildCapture.lua` | 1 |  .. spec.stem ..  |
| `Builder/ALifeBuildTools.lua` | 1 | [DEV] A-Life Tools |
| `Driving/ALifeDrivingPerformancePanel.lua` | 1 | Starts a new bounded capture, replacing  |
| `Interface/Creator/ALifeCreatorFactionSupport.lua` | 1 | Saved: default car,  |

### oyuncu_arayuzu

| Dosya | Aday | Örnek |
|---|---:|---|
| `Interface/ALifeSquadMapOverlay.lua` | 8 | Send a squad out now · Delay next squad by 1 hour |
| `Interface/ALifeSquadMap.lua` | 3 | A-Life: squad map ON (open the world map · A-Life: squad map off |
| `UI2/ALifeUI2JournalSettings.lua` | 1 | Marla |

### belirsiz

| Dosya | Aday | Örnek |
|---|---:|---|
| `Offline/ALifeWorldHunt.lua` | 2 | holding the border · return home |
| `Radio/ALifeRadioDirector.lua` | 2 | your radio hears it ( · your radio does NOT hear it ( |
| `Senses/ALifeCaution.lua` | 2 | Zombie avoidance · On: steers clear of zombies and leaves t |
| `Admin/ALifeSpawnDoctor.lua` | 2 | Living Factions · Companion Dogs |
| `Core/ALifePerfLog.lua` | 2 | I sid= ·  .. tostring(PerfLog.metrics.lines) ..  |
| `Shells/ALifeAnimationClient.lua` | 1 | appearanceFix=20260915 list= |
| `Talk/ALifeKnoxRadioPreset.lua` | 1 | Knox County Radio |
| `Tools/ALifeToolsAdmin.lua` | 1 | MARKS AND BUILDER |
| `World/ALifeMetaMeme.lua` | 1 | PALWorldTrainer |
| `Activities/ALifeHavens.lua` | 1 | May keep a house or camp that the crew r |
| `Decisions/ALifeGroupAsk.lua` | 1 |  .. m.lines ..  |
| `Decisions/ALifeReputationPersonal.lua` | 1 | People around here call you  |
| `Driving/ALifeDrivingDemoServer.lua` | 1 | Test trooper spawn failed:  |
| `Missions/ALifeTaskBoard.lua` | 1 | Report back |
| `Missions/ALifeTaskGiverWatch.lua` | 1 | The one who asked is gone |
| `Novelty/Memorials/ALifeNoveltyMemorials.lua` | 1 | Marcus Hale |
| `Novelty/Notes/ALifeNoveltyNotes.lua` | 1 | Marcus |
| `Offline/ALifeOfflineDirector.lua` | 1 | drift toward  |
| `Talk/ALifeFactionTalkServer.lua` | 1 | Crew den |
| `Talk/ALifeTalk5HomeServer.lua` | 1 | I set up most days around here |
| `Talk/ALifeTreeServer.lua` | 1 | somewhere in  |
| `Visitors/ALifeVisitorEvents.lua` | 1 | Your guest |
| `World/ALifeEncounterDirector.lua` | 1 | [ALIFE-ENCOUNTER] roll= |
| `World/ALifePopulateDirector.lua` | 1 | holding out at the  |
| `Admin/ALifeStartApplyActions.lua` | 1 | START SETTINGS |
| `Admin/ALifeTestFacActions.lua` | 1 | TEST FACTIONS |
| `Core/ALifeExecutor.lua` | 1 | [ALIFE-MP] body uid= |
| `Core/ALifeHandlers.lua` | 1 | handlers events= |
| `Driving/ALifeCarOffline.lua` | 1 | out of fuel |
| `Driving/ALifeCars6.lua` | 1 | where a crew parks when shot at has no m |
| `Driving/ALifeDrivingLog.lua` | 1 | A-Life driving lab  |
| `Driving/ALifeDrivingRoute.lua` | 1 | A-Life NPC |
| `Records/ALifeCustomProfiles.lua` | 1 | Custom NPC |
| `Records/ALifeFactionShare.lua` | 1 | @alife-pack 1 |
| `World/ALifeRenderWatch.lua` | 1 | [ALIFE-RENDER] square mismatch  |

