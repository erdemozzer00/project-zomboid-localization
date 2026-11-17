# KS1 — kısa sözcük denetimi: harita ipucu / yoldaş sayfası sözcükleri (IG_UI)

Dağılım: Claude (yeni): 7 · Toplam: 7

**Otomatik kontrol: temiz** ✅

### 1. `IGUI_ALifeUI_14834b90263b8507` — Claude (yeni)
- **EN:** 'people'
- **Eski TR:** 'insanlar'
- **TR:** 'kişi'
- *Not: 'people': harita ipucu başlığı 'Ad - {n} person/people, durum' (ALifeSquadMapTooltip.lua:206); 'insanlar' '5 insanlar' çıkıyordu, Türkçede sayıdan sonra tekil: '5 kişi'. CompanionRules'taki 'people' yalnız mantık anahtarı, ekranda görünmez.*

### 2. `IGUI_ALifeUI_0059783c35eae848` — Claude (yeni)
- **EN:** 'in'
- **Eski TR:** 'içinde'
- **TR:** 'kalan süre'
- *Not: 'in': 'Sıradaki tim' satırı, 'in ~2 h (game time)' (SquadMapTooltip.lua:238); 'içinde ~2 sa' sıra olarak bozuktu, 'arrives in' = 'varışına kalan' ile aynı kalıpta: 'kalan süre ~2 sa (oyun saati)'.*

### 3. `IGUI_ALifeUI_005978fa35eaeb52` — Claude (yeni)
- **EN:** 'of'
- **Eski TR:** 'ait'
- **TR:** '/'
- *Not: 'of': 'Görevdeki timler' satırı, '{çıkan} of {sınır}' (SquadMapTooltip.lua:241); 'ait' '2 ait 4' çıkıyordu → '2 / 4'.*

### 4. `IGUI_ALifeUI_3440dcbf1f6fb3ff` — Claude (yeni)
- **EN:** 'Cooking'
- **Eski TR:** 'yemek pişirme'
- **TR:** 'Yemek pişirme'
- *Not: 'Cooking': yoldaş sayfasında beceri etiketi ve konuşma düğmesi etiketi; kardeşleri (Marangozluk, Yakın dövüş, Müzik) büyük harfle başlıyor, 'yemek pişirme' küçük harfliydi.*

### 5. `IGUI_ALifeUI_76ea3b03763ed0be` — Claude (yeni)
- **EN:** 'Mechanics'
- **Eski TR:** 'mekanik'
- **TR:** 'Mekanik'
- *Not: 'Mechanics': yoldaş sayfasında beceri etiketi; büyük harfle başlamalı (Marangozluk, Müzik gibi).*

### 6. `IGUI_ALifeUI_0fa5ea463808917d` — Claude (yeni)
- **EN:** 'foraging'
- **Eski TR:** 'yiyecek arama'
- **TR:** 'yiyecek arıyor'
- *Not: 'foraging' (küçük harf): harita ipucunda faaliyet fiili ('Yapılan: …'), kardeşleri fiil çekimli (kaçıyor, avlanıyor); 'yiyecek arama' isimdi. Beceri etiketi 'Foraging' ayrı anahtar (Toplayıcılık).*

### 7. `IGUI_ALifeUI_0fd1544c2d532e03` — Claude (yeni)
- **EN:** 'nearby'
- **TR:** 'yakında'
- *Not: 'nearby': harita ipucu başlığında 'Ad - 3 kişi, nearby' durumu (SquadMapTooltip.lua:207); çevirisi hiç yoktu (ILERLEME'de 'görünmez' sayılmıştı, görünür). 'far away' = 'çok uzakta' karşılığı.*
