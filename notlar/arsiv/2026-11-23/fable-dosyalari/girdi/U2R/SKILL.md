---
name: alife-ceviri-v2-u2r
description: Project A-Life 1.5.2 fraksiyon kataloğundaki 49 İngilizce etiketi Türkçeye yerelleştirir. Çeviri girdisi bu dosyanın içindedir.
---

# Project A-Life v2 · U2R fraksiyon adları

Project Zomboid Build 42, 1993 Kentucky’si. Bu 49 metin fraksiyon kataloğunda ekip, birlik, topluluk veya kapı ziyaretçisi türü adı olarak görünür. Her adı İngilizce girdiden yeniden kur. Türkçe etiketi listede bir bakışta okunacak kadar kısa, doğal ve ayırt edici yaz.

## Çeviri kuralları

- Grup türünü, birlik numaralarını, kısaltmaların anlamını ve adın çağrışımını koru. Yer, kişi ve kurum adlarının özel ad kısımlarını koru. Örneğin Riverside yer adı olarak kalır, yanındaki topluluk tanımı Türkçeleşir.
- Etiketleri ad öbeği olarak yaz. Aynı kuruma veya birliğe atıf yapan satırlarda aynı karşılığı kullan. Brigade / Bde → **Tugay**, Battalion / Bn → **Tabur**, Division → **Tümen**, Company → **Bölük**. 149. Zırhlı Tugay ve Kentucky Ordu Ulusal Muhafızları, kısaltılmış biçimleriyle geçtiklerinde de aynı birlik ve kurumu ifade eder.
- Crew genel kullanımda **Ekip**, haydut veya çete adlarında **Tayfa** da kullanılabilir. Group → **Grup**, Faction → **Fraksiyon**, Squad → **Tim**, Survivor → **Hayatta Kalan**, Visitor → **Ziyaretçi**. Gerçek yer ve grup adlarını, Türkçe tanımlayıcı sözcüklerle birleştirirken 1993 Kentucky bağlamını koru.
- Türkçe harfleri doğru yaz. Şapkalı harf kullanma. Grup ve birlik adlarında başlık biçimi kullan, bağlaçları küçük bırak ve sona nokta ekleme. Kaynaktaki anlamlı ayraçları, parantezleri ve sayıları koru. İngilizce sıra sayısı eklerini Türkçede noktayla göster.
- Numarasız bağlamı bir sonraki İngilizce etiketi anlamak için kullan. Bağlamdaki bilgiyi yalnız İngilizce etiketin anlamında zaten varsa Türkçe ada taşı.

## Çıktı

**U2R_1.txt** adında UTF-8 düz metin üret. Dosya 49 satır içersin. Biçim **N | Türkçe**. 1 ile 49 arasındaki her numarayı bir kez ve verilen sırada yaz. İngilizceyi, etiket sütununu, bağlamı, başlıkları ve açıklamaları çıkar. Düz metin dosyası verilemiyorsa aynı 49 satırı tek kod bloğunda ver.

## İngilizce girdi

### Askeri birlikler ve salgın sonrası gruplar

Bağlam — Kentucky Ordu Ulusal Muhafızlarının 149. Zırhlı Tugayına bağlı bir müfrezeden kalanlar.
1 | arayüz etiketi | Kentucky Guard - 149th Armored Bde

Bağlam — Fort Campbell çıkışlı 101. Hava İndirme Tümeninin Knox karantina kordonundaki müfrezesi.
2 | arayüz etiketi | 101st Airborne - Knox Cordon Detachment

Bağlam — Fort Knox’taki ABD Ordusu zırhlı birlikler okulunun eğitmenleri ve personeli. Cadre okulun çekirdek kadrosu.
3 | arayüz etiketi | US Army Armor School Cadre - Fort Knox

Bağlam — Fort Knox’a giriş yollarında görev yapan askeri polis bölüğü.
4 | arayüz etiketi | Fort Knox Military Police Company

Bağlam — 149. Zırhlı Tugayın köprü ve yol işleriyle görevli istihkamcıları.
5 | arayüz etiketi | 149th Armored Brigade - Engineers

Bağlam — Kentucky Ulusal Muhafızları. Askeri kimlik, 123rd Armor birliğinin 2. Taburuna bağlı. Rifle Detail, taburdan ayrılmış piyade birliği.
6 | arayüz etiketi | 2nd Bn 123rd Armor - Rifle Detail

Bağlam — Emir almayı bırakıp sahra deposunu elinde tutan 149. Zırhlı Tugay mensupları.
7 | arayüz etiketi | Kentucky Guard Remnants - 149th Armored Bde

Bağlam — Atölye ve jeneratörü elinde tutan 149. Zırhlı Tugay istihkamcıları.
8 | arayüz etiketi | 149th Armored Bde - Engineer Holdouts

Bağlam — Eğitim sahasında bağlantısı kesilen 1. Zırhlı Eğitim Tugayı mensupları.
9 | arayüz etiketi | 1st Armor Training Brigade Remnants

Bağlam — Ulaştırma görevi için ayrılmış 149. Zırhlı Tugay personeli.
10 | arayüz etiketi | 149th Armored Bde - Transport Detail

Bağlam — Fort Knox’taki Ireland Army Community Hospital’dan gelen sahra sağlık personeli. Ireland hastane adının parçası.
11 | arayüz etiketi | Ireland Army Hospital - Medical Detail

Bağlam — Fort Campbell çıkışlı 5. Özel Kuvvetler Grubunun (Hava İndirme) bağlantısı kesilmiş müfrezesi.
12 | arayüz etiketi | 5th SFG (Airborne) - Isolated Detachment

### Sivil topluluklar ve yerel ekipler

Bağlam — Knox’ta birlikte çalışan şerif yardımcıları, itfaiyeciler ve paramedikler.
13 | arayüz etiketi | Knox First Responders

Bağlam — Rolling Fork’ta bir çitin arkasında bir araya gelen ailelerin ve diğer hayatta kalanların yerleşimi.
14 | arayüz etiketi | Rolling Fork Settlement

Bağlam — Salgının üzerinden bir ay geçmesine rağmen hala yolda olan insanlar.
15 | arayüz etiketi | Long Road Survivors

Bağlam — Louisville’de grev yapan toplu taşıma şoförleri ve atölye tamircileri.
16 | arayüz etiketi | Louisville Transit Strike Crew

Bağlam — Fort Knox’a gelen 100. Tümen yedekleri. IT, Institutional Training anlamındaki askeri eğitim kısaltması.
17 | arayüz etiketi | 100th Division (IT) Reservists - Fort Knox

Bağlam — Salt River’da küçük tekneyle insanları karşıya taşıyan ekip.
18 | arayüz etiketi | Salt River Ferrymen

Bağlam — Meade County’de kaçak içki imal eden ve takas yapan kooperatif.
19 | arayüz etiketi | Meade County Moonshine Co-op

Bağlam — Muldraugh yakınındaki kereste işleriyle uğraşan işçiler.
20 | arayüz etiketi | Sawmill Hands

### Birlikler, dayanışma grupları ve çeteler

Bağlam — Ortak bir kurul ve nöbet düzeni kuran Knox çevresindeki komşular, çiftçiler ve eski acil müdahale görevlileri.
21 | arayüz etiketi | Knox Commonwealth

Bağlam — Vadi yollarında dönüşümlü nöbet tutan çiftlik hanelerinin milis birliği. Ridge sırt veya tepe anlamında.
22 | arayüz etiketi | Ridge Militia League

Bağlam — Yerleşimler arasında malzeme taşıyan sürücüler, tüccarlar ve muhafızlar.
23 | arayüz etiketi | Valley Caravan League

Bağlam — Ekron çevresinde tohum, alet ve nöbet düzenini paylaşan çiftlikler.
24 | arayüz etiketi | Ekron Farm Co-op

Bağlam — Riverside iskelesini ayakta tutan iskele işçileri ve nehir kıyısındaki aileler. Riverside kasaba adı.
25 | arayüz etiketi | Riverside Ferry Union

Bağlam — Mount Hope’ta mutfak, derslik ve kapı nöbetini paylaşan aileler. Fellowship bir dayanışma topluluğunu anlatıyor.
26 | arayüz etiketi | Mount Hope Fellowship

Bağlam — Malzeme toplama sahasını işleten tamirciler ve metal işçileri.
27 | arayüz etiketi | Foundry Works Collective

Bağlam — Dar vadide yaşayan, av sahasını ve erzağı paylaşan ailelerin anlaşması. Hollow betimleyici, Valley Caravan League ayrı bir grup.
28 | arayüz etiketi | Hollow Compact

Bağlam — Küçük klinikleri yürüten bakıcılar ve gönüllüler.
29 | arayüz etiketi | Clinic Circle

Bağlam — Çalıntı yakıtla geçinen yol çetesi. Redline motor devir göstergesinin kırmızı sınırına gönderme yapıyor.
30 | arayüz etiketi | Redline Reavers

Bağlam — Zorla pay toplayan grup. Tithe, geleneksel onda bir payı çağrıştırıyor.
31 | arayüz etiketi | The Tithe

Bağlam — Gece hareket eden yağmacıların ironik adı. Ayrı bir grup olan Warehouse Night Shift, oyunda Depo Gece Vardiyası diye geçiyor.
32 | arayüz etiketi | Night Shift

Bağlam — Erzak biriktiren ve nöbet düzeni olan silahlı topluluğun adı. Choir adın imgesi.
33 | arayüz etiketi | Iron Choir

### Kapı ziyaretçisi türleri

Bağlam — Yakın sokaklardan kapıya gelen komşular.
34 | arayüz etiketi | Neighbours

Bağlam — Gideceği belirli bir yer olmayan otostopçular ve yayalar.
35 | arayüz etiketi | Drifters

Bağlam — Yakındaki çiftlik ve evlerden gelen, hane halkını soran aile üyeleri.
36 | arayüz etiketi | Family Folk

Bağlam — Salgın öncesinde işlerini kaybetmiş fabrika işçileri ve şoförler.
37 | arayüz etiketi | Laid-off Workers

Bağlam — Papaz, diyakoz, koro ve cemaat üyeleri.
38 | arayüz etiketi | Churchfolk

Bağlam — Hemşireler, sağlık yardımcıları ve ara sıra bir taşra doktoru.
39 | arayüz etiketi | Medical Folk

Bağlam — Marangozlar, hat işçileri, boyacılar ve berber gibi zanaat sahipleri.
40 | arayüz etiketi | Tradespeople

Bağlam — Yaşı ilerlemiş çiftler, eşini kaybetmiş kişiler ve emekli öğretmenler.
41 | arayüz etiketi | Elders

Bağlam — Üniversite öğrencileri, tezgahtarlar ve yirmili yaşlarında müzisyenler.
42 | arayüz etiketi | Young Adults

Bağlam — Üniformayı bırakmış eski askerler ve bir şerif yardımcısı. Etiket, eski hizmet mensuplarını kapsıyor.
43 | arayüz etiketi | Ex-Service

Bağlam — Sert görünüşlü, zararsız motorcular ve gezginler.
44 | arayüz etiketi | Rough but Harmless

Bağlam — Kasaba dışından gelen aileler, tarım işçileri ve turistler.
45 | arayüz etiketi | Outsiders

### Geç dönemde karşılaşılan çeteler

Bağlam — Ohio kıyısında malzeme toplayan grup. Slackwater, akıntısı durgun suyu anlatıyor.
46 | arayüz etiketi | Slackwater Rats

Bağlam — Kömür havzasının işsiz madencileri. Black lung, madencilerde görülen akciğer hastalığına gönderme yapıyor.
47 | arayüz etiketi | Black Lung Crew

Bağlam — Telsizle haberleşen kamyoncuların konvoyu. Breaker Nine çağrı biçimindeki ayırt edici ad.
48 | arayüz etiketi | Breaker Nine Convoy

Bağlam — Hipodromun seyisleri, yarış tahmincileri ve antrenman binicilerinden oluşan grup. Longshot at yarışı jargonunda düşük olasılıklı bahsi çağrıştırıyor.
49 | arayüz etiketi | Longshot Crew
