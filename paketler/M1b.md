# M1b — Murlo'nun geliştirme sürümü (1.5.0 sonrası, 2026-11-10): Sandbox yeni 33 + metni değişen 2 satır (Claude, 50 altı kuralı)

Dağılım: Claude (yeni): 35 · Toplam: 35

**Otomatik kontrol: temiz** ✅

### 1. `Sandbox_ProjectALife.HeliFrequency_tooltip` — Claude (yeni)
- **EN:** 'How often A-Life helicopters show up: flybys and backup calls. Helicopters get rarer as the days pass. Low is half as often, High is twice as often, Off stops all flybys, patrols and first passes (backup helicopters follow their own switch). A-Life helicopters must be on.\nDefault Normal (2).'
- **Eski TR:** "A-Life helikopterlerinin ne sıklıkla geldiği: geçişler ve takviye çağrıları. Düşük yarı yarıya, Yüksek iki kat sık. 'A-Life helikopterleri' açık olmalı.\nVarsayılan: Normal (2)."
- **TR:** "A-Life helikopterlerinin ne sıklıkla geldiği: geçişler ve takviye çağrıları. Günler geçtikçe helikopterler seyrekleşir. Düşük yarı yarıya, Yüksek iki kat sık; Kapalı bütün geçişleri, devriyeleri ve ilk geçişleri durdurur (takviye helikopterleri kendi ayarına bağlıdır). 'A-Life helikopterleri' açık olmalı.\nVarsayılan: Normal (2)."
- *Not: Metni değişti: seyrekleşme ve Kapalı seçeneği eklendi.*

### 2. `Sandbox_ProjectALife.HeliFrequency_option4` — Claude (yeni)
- **EN:** 'Off'
- **TR:** 'Kapalı'

### 3. `Sandbox_ProjectALife.HeliHostile` — Claude (yeni)
- **EN:** 'Hostile and raid helicopters'
- **TR:** 'Düşman ve baskın helikopterleri'

### 4. `Sandbox_ProjectALife.HeliHostile_tooltip` — Claude (yeni)
- **EN:** 'Lets helicopters turn hostile and circle to attack, and lets full-scale raids bring a helicopter (raid gunship, helicopter drop). Off: no helicopter ever attacks and raids arrive on foot or by car.\nDefault on.'
- **TR:** 'Helikopterlerin düşmanlaşıp saldırmak için çevrende dönmesine ve büyük baskınların helikopterle gelmesine (silahlı baskın helikopteri, helikopter indirmesi) izin verir. Kapalı: hiçbir helikopter saldırmaz, baskınlar yaya ya da arabayla gelir.\nVarsayılan: açık.'
- *Not: 'helicopter drop' → mevcut 'helikopter indirmesi'.*

### 5. `Sandbox_ProjectALife.CarsTrafficFrequency_tooltip` — Claude (yeni)
- **EN:** 'How many NPC cars are on the roads: ambient traffic, drive-bys and pull-ups. Low is about 40 percent, High is 1.5 times, Off stops all ambient NPC car traffic (raid, police response and scripted cars follow their own switches). Enable NPC vehicles must be on.\nDefault Normal (2).'
- **Eski TR:** "NPC'lerin ne sıklıkla arabayla geldiği: yanından geçerek ateş açma ve yanında durma. Düşük yarı yarıya, Yüksek iki kat sık. 'NPC'ler araç kullanır' açık olmalı.\nVarsayılan: Normal (2)."
- **TR:** "Yollarda ne kadar NPC arabası olduğu: çevre trafiği, arabadan ateş açma ve yanaşma. Düşük yaklaşık yüzde 40, Yüksek 1,5 kat; Kapalı bütün çevre NPC trafiğini durdurur (baskın, polis müdahalesi ve senaryolu arabalar kendi ayarlarına bağlıdır). 'NPC'ler araç kullanır' açık olmalı.\nVarsayılan: Normal (2)."
- *Not: Metni değişti. drive-by/pull-up mevcut 'Arabadan geçerken ateş' / 'Arabayla yanaşma' ile uyumlu.*

### 6. `Sandbox_ProjectALife.CarsTrafficFrequency_option4` — Claude (yeni)
- **EN:** 'Off'
- **TR:** 'Kapalı'

### 7. `Sandbox_ProjectALife.TalkWindowStyle` — Claude (yeni)
- **EN:** 'Talk window style'
- **TR:** 'Konuşma penceresi türü'
- *Not: Mevcut 'Konuşma penceresi' kullanımı.*

### 8. `Sandbox_ProjectALife.TalkWindowStyle_tooltip` — Claude (yeni)
- **EN:** "Which conversation window players get. New is the side panel; Old cinematic is the earlier window with numbered answers. A player's Journal setting still wins unless you pick a forced value.\nDefault New."
- **TR:** "Oyunculara hangi konuşma penceresinin açılacağı. Yeni, yan paneldir; Eski sinematik, numaralı cevapları olan önceki penceredir. Zorunlu bir değer seçmezsen oyuncunun Günlük'teki ayarı geçerli olur.\nVarsayılan: Yeni."
- *Not: Journal → Günlük (UI.json ve IG_UI ile aynı).*

### 9. `Sandbox_ProjectALife.TalkWindowStyle_option1` — Claude (yeni)
- **EN:** 'New'
- **TR:** 'Yeni'

### 10. `Sandbox_ProjectALife.TalkWindowStyle_option2` — Claude (yeni)
- **EN:** 'Old cinematic'
- **TR:** 'Eski sinematik'

### 11. `Sandbox_ProjectALife.TalkWindowStyle_option3` — Claude (yeni)
- **EN:** 'New (forced)'
- **TR:** 'Yeni (zorunlu)'

### 12. `Sandbox_ProjectALife.TalkWindowStyle_option4` — Claude (yeni)
- **EN:** 'Old cinematic (forced)'
- **TR:** 'Eski sinematik (zorunlu)'

### 13. `Sandbox_ProjectALife_6Ambient` — Claude (yeni)
- **EN:** 'A-Life: Ambient sounds'
- **TR:** 'A-Life: Ortam sesleri'
- *Not: Sayfa başlığı (EN'de EXPERT öneki yok).*

### 14. `Sandbox_ProjectALife.MetaSoundEnabled` — Claude (yeni)
- **EN:** 'Ambient meta sounds'
- **TR:** 'Meta ortam sesleri'

### 15. `Sandbox_ProjectALife.MetaSoundEnabled_tooltip` — Claude (yeni)
- **EN:** 'Master switch for the ambient world sounds: phones, alarms, TV and radio noise, police chatter, distant gunfire and screams, bells and sirens, ocean and forest, the numbers station. Off silences all of them.\nDefault on.'
- **TR:** 'Ortam seslerinin ana şalteri: telefonlar, alarmlar, televizyon ve radyo cızırtısı, polis telsizi konuşmaları, uzaktan gelen silah sesleri ve çığlıklar, çanlar ve sirenler, deniz ve orman, sayı istasyonu. Kapalıyken hepsi susar.\nVarsayılan: açık.'
- *Not: 'Master switch' → mevcut 'Ana şalter'.*

### 16. `Sandbox_ProjectALife.MetaSoundPhones` — Claude (yeni)
- **EN:** 'Phones and beeping'
- **TR:** 'Telefonlar ve bip sesleri'

### 17. `Sandbox_ProjectALife.MetaSoundPhones_tooltip` — Claude (yeni)
- **EN:** "House phones, the phones of the dead, and alarm beeps. A dead body's phone also stops drawing zombies when this is off.\nDefault on."
- **TR:** 'Ev telefonları, ölülerin telefonları ve alarm bipleri. Bu kapalıyken cesetlerdeki telefonlar zombi de çekmez.\nVarsayılan: açık.'

### 18. `Sandbox_ProjectALife.MetaSoundTvRadio` — Claude (yeni)
- **EN:** 'TV and radio noise'
- **TR:** 'Televizyon ve radyo cızırtısı'

### 19. `Sandbox_ProjectALife.MetaSoundTvRadio_tooltip` — Claude (yeni)
- **EN:** 'Emergency broadcast tones, radio backup calls and the radio cutting out.\nDefault on.'
- **TR:** 'Acil durum yayını sinyalleri, telsizden takviye çağrıları ve radyonun kesilmesi.\nVarsayılan: açık.'

### 20. `Sandbox_ProjectALife.MetaSoundPolice` — Claude (yeni)
- **EN:** 'Police radio chatter'
- **TR:** 'Polis telsizi konuşmaları'

### 21. `Sandbox_ProjectALife.MetaSoundPolice_tooltip` — Claude (yeni)
- **EN:** 'Dispatch chatter from police cars near you.\nDefault on.'
- **TR:** 'Yakınındaki polis arabalarından gelen merkez anonsları.\nVarsayılan: açık.'
- *Not: dispatch → merkez anonsu.*

### 22. `Sandbox_ProjectALife.MetaSoundGunfire` — Claude (yeni)
- **EN:** 'Distant gunfire and screams'
- **TR:** 'Uzaktan silah sesleri ve çığlıklar'
- *Not: Mevcut 'Uzaktan gelen silah sesleri' ile uyumlu.*

### 23. `Sandbox_ProjectALife.MetaSoundGunfire_tooltip` — Claude (yeni)
- **EN:** 'Far-off shootouts, artillery, explosions, screams and cries for help.\nDefault on.'
- **TR:** 'Uzaklardaki çatışmalar, top atışları, patlamalar, çığlıklar ve yardım çağrıları.\nVarsayılan: açık.'

### 24. `Sandbox_ProjectALife.MetaSoundBells` — Claude (yeni)
- **EN:** 'Bells and sirens'
- **TR:** 'Çanlar ve sirenler'

### 25. `Sandbox_ProjectALife.MetaSoundBells_tooltip` — Claude (yeni)
- **EN:** 'Church bells, police and service sirens, air raid sirens.\nDefault on.'
- **TR:** 'Kilise çanları, polis ve acil servis sirenleri, hava saldırısı sirenleri.\nVarsayılan: açık.'

### 26. `Sandbox_ProjectALife.MetaSoundNature` — Claude (yeni)
- **EN:** 'Nature ambience'
- **TR:** 'Doğa sesleri'

### 27. `Sandbox_ProjectALife.MetaSoundNature_tooltip` — Claude (yeni)
- **EN:** 'Ocean waves near open water and wind in the forest.\nDefault on.'
- **TR:** 'Açık suya yakınken dalga sesleri, ormanda rüzgâr.\nVarsayılan: açık.'

### 28. `Sandbox_ProjectALife.MetaSoundNumbers` — Claude (yeni)
- **EN:** 'Numbers station'
- **TR:** 'Sayı istasyonu'
- *Not: numbers station: şifreli sayı okuyan radyo yayını.*

### 29. `Sandbox_ProjectALife.MetaSoundNumbers_tooltip` — Claude (yeni)
- **EN:** 'The numbers station and its gong on radios and TVs.\nDefault on.'
- **TR:** 'Radyolarda ve televizyonlarda sayı istasyonu ve gong sesi.\nVarsayılan: açık.'

### 30. `Sandbox_ProjectALife.MetaSoundVolume` — Claude (yeni)
- **EN:** 'Meta sound volume (percent)'
- **TR:** 'Meta ses düzeyi (yüzde)'
- *Not: Mevcut '(yüzde)' kalıbı.*

### 31. `Sandbox_ProjectALife.MetaSoundVolume_tooltip` — Claude (yeni)
- **EN:** 'Scales every ambient meta sound above. 0 silences them.\nDefault 100.'
- **TR:** "Yukarıdaki bütün meta ortam seslerinin düzeyini ayarlar. 0'da hepsi susar.\nVarsayılan: 100."

### 32. `Sandbox_ProjectALife.CarsSpawnDistance` — Claude (yeni)
- **EN:** 'NPC car spawn distance (tiles)'
- **TR:** 'NPC arabalarının ortaya çıkma mesafesi (kare)'
- *Not: SÖZLÜK: dünyada kendiliğinden belirme → ortaya çıkma.*

### 33. `Sandbox_ProjectALife.CarsSpawnDistance_tooltip` — Claude (yeni)
- **EN:** 'Ambient NPC cars (travelers, start traffic, cars that become real when you near them) never appear closer than this to a player. Raid, pull-up, drive-by and police cars may come closer but never inside your view, and walls do not hide them.\nDefault 70.'
- **TR:** 'Çevredeki NPC arabaları (yoldan geçenler, oyun başı trafiği, sen yaklaşınca gerçeğe dönüşen arabalar) bir oyuncuya bundan daha yakında asla belirmez. Baskın, yanaşma, arabadan ateş ve polis arabaları daha yakında belirebilir ama asla görüş alanında belirmez; duvar arkası da görüş alanından sayılır.\nVarsayılan: 70.'
- *Not: 'walls do not hide them' = görüş kontrolünde duvar hesaba katılmaz.*

### 34. `Sandbox_ProjectALife.CarsBaseKeepOut` — Claude (yeni)
- **EN:** 'Car keep-out around bases (tiles)'
- **TR:** 'Arabalar üslerden uzak durur (kare)'
- *Not: Mevcut 'Karakollar oyuncu üslerinden uzak durur (kare)' kalıbı.*

### 35. `Sandbox_ProjectALife.CarsBaseKeepOut_tooltip` — Claude (yeni)
- **EN:** 'NPC cars never spawn or appear this close to a player base edge, and arriving crews stop and get out before it. 0 keeps them out of the base itself only.\nDefault 40.'
- **TR:** "NPC arabaları oyuncu üssünün sınırına bu mesafeden yakın asla ortaya çıkmaz ya da belirmez; gelen ekipler bu sınırdan önce durup arabadan iner. 0'da yalnızca üssün kendisine girmezler.\nVarsayılan: 40."
