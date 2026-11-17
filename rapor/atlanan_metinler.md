# Çeviri yoluna alınmamış metinler (2026-11-03 taraması)

**Önemli (sonradan doğrulandı):** A grubu (ses kütüphaneleri) ve ses profili altyazıları şu an oyunda görünmez: `AudioPolicy.npcAudioEnabled = false` sabit; ses kapalıyken altyazı Talk/Data satırından (çevrili) ya da VoiceTextFallback'ten gelir. Görünen açık: B grubu, VoiceTextFallback, C grubu ve 2 eşya adı. Bu tabloda B/C sayıları alt sınırdır; kesin sayım: B 389 benzersiz (8 yer tutuculu, birkaçı log satırı).

Yöntem: modun Lua dosyalarındaki büyük harfle başlayan, en az iki sözcüklü dizgeler; `kaynak/` altındaki hiçbir EN metinle (IG_UI, IG_UI_lua, Creator, RadioData_lua) eşleşmeyenler. Talk/Data, ses profilleri, harita/plan verisi, Admin/Debug/Driving hariç. Tek sözcüklü ya da küçük harfle başlayan satırlar sayılmadı; sayılar alt sınırdır.


## A. Ses altyazıları (caption yolu, ek çevirir): 1229

- `Audio/ALifeFactionVoiceStyles.lua` 647: Hey, somebody's out there. Keep an eye on them · Live one. Might be carrying food. · Somebody there. Wonder what they want
- `Audio/ALifeReactionLibrary.lua` 438: We're taking fire! · Shots incoming! · They're firing on us!
- `Audio/ALifeVoiceDialogue.lua` 72: Hey! Don't point that at me! · Easy. Lower it. Nobody needs to die here. · Keep your head down! I'll cover you!
- `Audio/ALifeVoiceTextFallback.lua` 42: Someone there. Easy now · Dead ones. Keep your distance · Careful with that one. Don't rush closer
- `Audio/ALifeVoiceExtraEvents.lua` 19: Suppressing. Keep your heads down. · I'll keep them pinned. · Stay down! Eat this!
- `Audio/ALifeVoiceLootEvents.lua` 11: Got a {found} here. · Found a tool. · There's a tool in this one.

## B. Diğer NPC konuşmaları (Speech.say → caption, ek çevirir): 412

- `Audio/ALifeGossip.lua` 103: Let's move out- how's your day going? · Shit, same as always- you? · Could be better, y'know
- `World/ALifePlanData.lua` 83: Bet nobody's been through {target} yet · I'd rather look in {target} than stand around wishing we'd tried · Yeah, that works
- `Behaviours/ALifeInjuryRules.lua` 41: Ughh.. my leg.. · Somebody.. help me.. · It hurts.. oh God it hurts..
- `Fear/ALifeModulePanic.lua` 39: Someone there! · Get down! · Cover! Cover!
- `Talk/ALifeTalk.lua` 22: Don't like strangers, but we're in deep shit here, eh? Stay back and w · Don't like you being here, but they don't care who you are - keep off  · Strangers make me jumpy, the dead make me worse - stay off me, cover m
- `Talk/ALifeTalkSocial.lua` 22: Already answered that one · We did this one already, remember? · Ask me something else, I said my piece
- `Behaviours/ALifeModuleRobbery.lua` 18: Hey you! Stop right there! · Hands up! Don't you move! · Last time! HANDS UP!
- `Decisions/ALifeReputationPersonal.lua` 18: Wait, you were a cop, weren't you? You've still got the look · Ranger, right? You walk like you know the woods · Security, right? I'd know that walk anywhere
- `Behaviours/ALifeModuleCareful.lua` 13: This area's closed, go back out the way you came · We're busy here, stay back till it's over · Last warning, get out of here, NOW
- `Records/ALifeNames.lua` 12: Name's {myfirst}. {myfirst} {mylast}. · I'm {myfirst} {mylast}. Was, anyway. Still am, I suppose. · Folks call me {myfirst}. You can too.
- `Activities/ALifeHavens.lua` 9: Where I sleep? Not telling you that · Oh... you again · You're back, huh- hands where I can see 'em
- `Behaviours/ALifeModuleBreach.lua` 9: Stack up on the door! · Everybody on the wall by the door, quiet · Get on the wall by the door and shut up
- `Behaviours/ALifeModuleStances.lua` 8: Lower that weapon... slowly · Back off, give us some room · House is taken, turn around and walk
- `Fear/ALifeThreatWatch.lua` 4: Don't aim at me, aim at them! · Not me! Shoot them! · Hey! Point that at the dead, not at me!
- `Decisions/ALifeStandoff.lua` 3: They are calling you out. Answer or come out · Someone is outside your place, calling you out · They want an answer
- `Offline/ALifeRevenge.lua` 3: Word is {faction} people are asking around about you · Somebody saw {faction} folks near {town}, asking about you · Caught a scrap of radio chatter, {faction} are hunting whoever hurt th
- `Talk/ALifeTalkSupplies.lua` 3: Didn't you just ask one of ours? Word gets around... we're short too,  · Sorry, nothing to spare, we gotta stretch what we've got · Uhh... fine, take this, it's all I can spare
- `Outposts/ALifeOutpostExpeditions.lua` 2: Heard a big armed group is coming down the road, get somewhere safe · Three groups just left together, keep your eyes on the road

## C. Oyuncuya mesaj / arayüz: 59

- `Talk/ALifeParty.lua` 18: You left the group. · The group moved on without you. · The group doesn't want you around any more.
- `Interface/ALifeSquadMapOverlay.lua` 16: Send a squad out now · Delay next squad by 1 hour · Delay next squad by 24 hours
- `Interface/ALifeWoundPanelData.lua` 10: Slight damage · Very Minor damage · Minor damage
- `Shells/ALifeAnimations.lua` 6: Thumbs up · Thumbs down · Heavy breathing
- `Interface/ALifeFieldRadioData.lua` 3: Knox County Radio · Knox County Radio: · Knox County Radio
- `Outposts/ALifeOutpostTheft.lua` 2: Hey! HEY! Put that down! · Hey! HEY! Put that down!
- `Talk/ALifeKnoxCountyRadio.lua` 2: Knox County Radio:  · Knox County Radio
- `Outposts/ALifeOutpostRadio.lua` 1: They cut the radio!
- `Talk/ALifeKnoxRadioPreset.lua` 1: Knox County Radio

## D. Ziyaretçi / sığınak sistemi (K37 kapsam dışı): 624

- `World/ALifeDoorEncounters.lua` 253: Two days, maybe three.. I lost count · Still two days, nothing's changed since you asked · Same answer, please, I'm too tired for more questions
- `World/ALifeSafehouseVisit.lua` 209: Thanks for opening up, wasn't sure you would · Thanks, I'll come in and stay out from underfoot · Bless you, I'll keep to myself, gone by morning
- `World/ALifeSafehouseEvents.lua` 50: Planks pried off the windows and glass on the ground. Someone worked o · The fuel tank is lower than you left it. Someone has been at it. · Your garden has been picked over. Someone took the ripe crops.
- `World/ALifeSafehouseDirector.lua` 37: Fresh paint by the front door: a big X at eye level. Someone marked th · Tally marks scratched by the door. Someone is counting how many live h · Blood smeared on the wall by the front door. It is fresh.
- `Interface/ALifeSafehouseClient.lua` 36: Letters and gifts · Signs and marks · Night and radio
- `Visitors/ALifeVisitorReact.lua` 30: You fed them. · You gave them something to drink. · You got them medicine.
- `Visitors/ALifeVisitorLife.lua` 5: Thanks for the roof, I mean it · I'll get my things, thank you again · Appreciate it, really, take care
- `Visitors/ALifeVisitorDirector.lua` 1: You have met before
- `Visitors/ALifeVisitorEvents.lua` 1: Your guest
- `Visitors/ALifeVisitorWardrobe.lua` 1: You walked in on them.
- `World/ALifeSafehouseScript.lua` 1: The radio has no power.

## E. Oluşturucu / yönetici / hata raporu / mod uyumu (kasıtlı İngilizce): 367

- `Audio/ALifeVoiceCatalog.lua` 84: Calm Male · Calm Female · Aggressive Male
- `World/ALifeEncounters.lua` 53: No lake or river bank within 32 tiles of the spot. Stand at the water' · No open ground within 36 tiles (no building, road or tree line). Move  · No paved road within 36 tiles. Stand on or beside a road.
- `Compat/ALifeModCompat.lua` 33: Immersive Driving · The Mutants · Cry of Fear
- `Talk/ALifeDialogueRoles.lua` 32: Family - Man · Family - Woman · Family - Elder
- `Behaviours/ALifeModuleRules.lua` 19: Military factions do not use fear. · Military factions do not flee from raised guns or shots. · Military factions do not use panic.
- `Interface/ALifePersonalReport.lua` 14: What happened: [describe the problem here] · Steps to reproduce: [add steps here] · Expected result: [describe what should happen]
- `Interface/ALifeEncounterConsole.lua` 10: Choose a squad and encounter, then deploy both with one action. · Module QA written to  · Black box written to 
- `Interface/ALifeStatusWindow.lua` 10: Waiting for server status... · Physical shells:  · Running actions: 
- `Records/ALifeBehaviorProfiles.lua` 9: Roaming hostile (Scout) · Roams between contacts, then hunts the nearest hostile and keeps press · Area patrol
- `Interface/Creator/ALifeCreatorCore.lua` 9: Custom ( · Faction voice sample:  · Delete folder '
- `Records/ALifeDropPolicy.lua` 8: Off (0%) · Very low (0-10%) · Low (10-20%)
- `Behaviours/ALifeModuleConducts.lua` 8: Stealth killer · Shadows a person from behind, sneaking, and opens with a backstab at d · Keeps distance, gives ground when the fight closes, and fires delibera
- `Behaviours/ALifeModuleMeleeCrew.lua` 6: Melee fighters step back and sideways between swings with their face t · Melee flanking pair · Intimidating approach
- `Records/ALifeClothingAdvisor.lua` 4: Not in the clothing guide (modded or new item): listed without a seaso · Role fit:  · Issued to: 
- `Records/ALifeSeasonalOutfitGenerator.lua` 4: Preserved missing or duplicate outfit  · Preserved different season tag  · Preserved authored uniform conflict 
- `Behaviours/ALifeModuleTravel.lua` 4: Investigate noises · Walks toward gunfire and other sounds it did not make. · Closes back up with the rest of the group when it drifts apart.
- `Records/ALifeClothingHealth.lua` 3: No torso garment in every variant of this outfit · No trousers, skirt or dress in every variant of this outfit · No shoes in every variant of this outfit
- `Records/ALifeFactionShare.lua` 3: This code uses items your game does not have. · Unknown items:  · Import it anyway?
- `Records/ALifeRecordMigration.lua` 3: The Creator file  · Project A-Life:  · Project A-Life: 
- `Behaviours/ALifeModuleIdleLife.lua` 3: Bar Stool · Blue Bar Stool · Eats, drinks and smokes between fights; at night a stance-less squad m
- `Interface/Creator/ALifeCreatorFactionSpawning.lua` 3: Relative faction selection weight, 0 to  · Lone size (1- · Group size (
- `Records/ALifeCustomFactions.lua` 2: New Faction · Hostile NPCs
- `Behaviours/ALifeModuleActivity.lua` 2: Squad activity · Runs the work steps of the activity the squad's planner picked; other 
- `Behaviours/ALifeModuleCover.lua` 2: Use cover · Shooters get out of the line of fire to reload, break contact when hur
- `Behaviours/ALifeModuleFlanking.lua` 2: Ranged flanking · Gives ranged actors stable approach lanes and wider wings at long rang
- `Behaviours/ALifeModuleLeader.lua` 2: Squad leader · Keeps the group together, deploys it on contact and rallies it after l
- `Behaviours/ALifeModuleRadioman.lua` 2: Radio call · An actor allowed to call backup goes to the group's radio on contact (
- `Behaviours/ALifeModuleStrafe.lua` 2: Aimed movement · Shooters keep the gun on the target, or where it was last seen, while 
- `Behaviours/ALifeModuleTalkPresence.lua` 2: Talk and presence · Answers a player who talks, greets without stopping, says a word when 
- `Interface/ALifeWoundPanel.lua` 2: Overall Body Status · Right click to show Treatment menu
- `Records/ALifeCustomProfiles.lua` 1: Custom NPC
- `Behaviours/ALifeModuleFortify.lua` 1: Fortify the building
- `Behaviours/ALifeModuleGunner.lua` 1: Gunner (suppression fire)
- `Behaviours/ALifeModuleHealing.lua` 1: Dress wounds
- `Behaviours/ALifeModuleNightHold.lua` 1: Hold the house at night
- `Behaviours/ALifeModulePatrolRest.lua` 1: The squad stops, takes a nearby house or cover and idles with roles: o
- `Behaviours/ALifeModuleScavengeRun.lua` 1: Works a nearby building end to end, falling back to loose containers.
- `Behaviours/ALifeModuleSearch.lua` 1: After combat, search up to two bodies for a bounded share of non-cloth
- `Behaviours/ALifeModuleVisitorLife.lua` 1: Visitor life
- `Combat/ALifeGunDiscipline.lua` 1: Switch to melee against zombies
- `Combat/ALifeSniperAwareness.lua` 1: Distant rifle! Get off that line!
- `Core/ALifeActorRegistry.lua` 1: Protected area
- `Decisions/ALifeNpcOpinion.lua` 1: Word reached them: 
- `Fear/ALifeModuleFear.lua` 1: Among eligible members, 40 percent have this fear during the first 5 w
- `Fear/ALifeModuleGunFear.lua` 1: An NPC that is not itself well armed backs away from a player or hosti
- `Fear/ALifeModuleSurvival.lua` 1: The badly wounded break off and a shaken gunman may rout; fear of guns
- `Fear/ALifeModuleWithdraw.lua` 1: Withdraw and re-engage
- `Records/ALifeCustomFactionAuthority.lua` 1: The world's Creator faction store
- `Records/ALifeCustomProfileAuthority.lua` 1: The world's Creator profile store
- `Senses/ALifeCaution.lua` 1: Zombie avoidance
- `Talk/ALifeSpeechBubbleLayout.lua` 1: The quick brown fox jumps over the
- `Talk/ALifeTalkInput.lua` 1: Toggle chat
- `Interface/Creator/ALifeCreatorAppearance.lua` 1: Open the icon catalog for 
- `Interface/Creator/ALifeCreatorClothingView.lua` 1: Everything is listed (
- `Interface/Creator/ALifeCreatorCombat.lua` 1: Base HP, 0-200. Zero uses the standard NPC HP. The NPC health option a
- `Interface/Creator/ALifeCreatorModuleRules.lua` 1: Disabled by 
- `Interface/Creator/ALifeCreatorSeasonalActions.lua` 1: The plan lists the NPC 

## F. Yer adları (yer tutucu dolgusu): 144

- `World/ALifeRoadGraphShipped.lua` 111: Ekron 2 · Irvington 10 · Valley Station 6
- `Talk/ALifeSpeech.lua` 21: Dixie Highway · Main Street · Railroad Avenue
- `World/ALifeRoadGraph.lua` 4: March Ridge · Valley Station · Fallas Lake
- `World/ALifeTownRegions.lua` 4: Echo Creek · Fallas Lake · March Ridge
- `World/ALifePopulateDirector.lua` 4: Police station · Fire house · Gun store
