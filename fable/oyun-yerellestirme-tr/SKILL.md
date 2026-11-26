---
name: oyun-yerellestirme-tr
description: Oyun metinlerini İngilizceden Türkçeye yerelleştirir. Karakter repliklerini bir Türk'ün ağzından çıkmış gibi yeniden yazar, ekran metinlerini kısa ve tutarlı çevirir. Numaralı "N | etiket | İngilizce" satırlarından oluşan girdi dosyası verildiğinde kullan. Projeye özel kurallar dosyanın başında gelir, çıktı yalnızca "N | Türkçe" satırlarıdır.
---

# Oyun yerelleştirme, İngilizceden Türkçeye

Bu skill zanaatı verir: iyi oyun Türkçesi nasıl yazılır. Projeye özel her şey (dünya, terimler, yer tutucular, etiketlerin anlamı, özel kurallar) girdi dosyasının başındaki notlarda gelir.

Replikte çevirmen değil, **Türkçe diyalog yazarısın**: İngilizce satır sahnede ne olduğunu söyler, ağızdan ne çıkacağına sen karar verirsin. Ekran metninde ise titiz bir çevirmensin: kısa, tutarlı, şaşırtmayan.

Ölçü tek: oyuncu satırı okuyunca aklına İngilizcesi gelmemeli.

## Dosyayı oku: öncelik sırası

1. **Dosya başındaki `#` notları** ve her başlığın (`##### ... #####`) altındaki notlar. Bu skill'den önce gelirler.
2. Bu skill'in kuralları ve varsayılanları.

Dosya başı şunları verebilir: DÜNYA (yer, yıl, ortam), TERİMLER, YER TUTUCULAR (hangisi nasıl dolar), ETİKETLER (satır etiketlerinin anlamı), biçim ve çıktı kuralları, metnin ekranda nerede göründüğü.

- Dosya başında olmayan proje kuralını uydurma. Anlamı açıklanmamış etiketten bilgi çıkarma; anlamını bilmediğin yer tutucuyu aynen bırak.
- Başlık tek bir durumdur: altındaki bütün satırları birlikte oku.
- Numarasız bağlam satırları (`·` ile başlayanlar, `MEVCUT:` gibi notlar) çevrilmez, çıktıya yazılmaz.
- Dosya başı ile bu skill çelişirse dosya başını uygula. Dosya başı kendi içinde ya da terim listesiyle çelişiyorsa sessizce seçim yapma: birini uygula, çıktının sonunda bildir.

## Her satırın türü

Tür dosyaya göre değil **satıra göre** belirlenir; aynı dosyada replik ile ekran metni karışık olabilir. Etiket ve başlık notu türü söyler. Emin değilsen: konuşan biri yoksa ekran metnidir.

| Tür | Nasıl tanınır | Nasıl yazılır |
|---|---|---|
| **Replik** | Bir karakter konuşuyor; etiket rolü, adı, sınıfı ya da ruh halini verir | Türkçe diyalog. Aşağıdaki replik bölümlerinin hepsi geçerli, serbestlik tam. |
| **Oyuncu sözü** | Oyuncunun seçtiği soru, cevap, seçenek düğmesi | Oyuncunun ağzından, birinci tekil, kısa ve yalın. Oyuncu herkes olabilir: ağız, küfür, dua, cinsiyetli söz, duygu eki yok. İskelet yine kırılır. |
| **Açıklama notu** | Düğme altı not, sonuç, ipucu, koşul, risk | Ne olacağını söyleyen kısa bilgi. Öznesiz, geniş ya da şimdiki zaman. Süs yok. |
| **Ekran metni** | Etiket, düğme, sekme, ayar, bildirim, başlık, kart, görev adımı | "Ekran metni" bölümü. Serbestlik yok. |
| **Anlatı** | Anlatıcı metni, günlük, bitiş yazısı, bulunan not | Yazı dili: akıcı, düzgün, kaynağın zamanı ve tonuyla. Konuşma sözleri (ya, be, valla) yok, ama iskelet yine kırılır, evrak dili yine yok. |
| **Telsiz, yayın, anons** | Telsizden konuşan kişi, radyo spikeri, hoparlör | Telsiz kısa ve kesik ("Tamam.", "Anlaşıldı.", "Dinlemedeyim."). Spiker düzgün ve ölçülü. Kişi telsizde de kendi sesiyle konuşur. |

| İngilizce | Tür | Türkçe |
|---|---|---|
| Can you spare some help? | oyuncu sözü | Bana yardım edebilir misin? |
| I'm short on food | oyuncu sözü | Yiyeceğim azaldı |
| They say what they can spare | açıklama notu | Neyi verebileceklerini söylerler |
| Get to the barn | görev adımı | Ahıra ulaş |
| Northeast | kart etiketi | Kuzeydoğu |
| Game saved | bildirim | Oyun kaydedildi |

Başlığı bütünüyle oku. Satırların ilişkisini sahne notundan öğren.

- **Sıralı konuşmada** her kişinin sesini ve söz sırasını koru. Bir sonraki konuşmacının cevabını veya esprisini erkene alma.
- **Alternatif havuzunda** oyun uygun sözlerden birini seçer. Her seçeneği tek başına oku. Anlaşılması, oyuncunun havuzdaki başka bir sözü duymasına bağlı kalmasın.
- **Dallanan konuşmada** oyuncunun seçimini ona bağlı NPC cevabıyla birlikte oku. Bir tepki aynı daldaki birkaç farklı oyuncu sözüne bağlanabiliyorsa her biriyle anlamlı olmalı. Dosya bağlantıyı açıklamıyorsa numara sırasından bir konuşma zinciri çıkarma.

## Dünya: mekân kaynağın, ağız Türk

- Yer, çağ ve ortam dosya başında yazar. Yazmıyorsa metinden çıkar; çıkmıyorsa zamansız ve yersiz yaz.
- Adlar, yerler, markalar, para birimi, kurumlar, rütbeler ve inanç dünyası (kilise, şerif, dolar) kaynaktaki gibi kalır. Türkiye'ye özgü yer ve şey eklenmez (çay ocağı, dolmuş, simit, muhtar).
- Deyim, ünlem, küfür, hitap, dua, tepki sözü Türkçenin kendi karşılığıyla gelir.
- **İstanbul Türkçesi.** Dosya başı bir karaktere özel ağız istemiyorsa yöresel ağız yok (geliyom, gidek, gardaş, heç).
- **Çağa uy.** Oyunun yılından sonra çıkan söz yok. Çağ belli değilse de internet ve sokak jargonu yok: kanka, bro, tek başına "aynen", "sıkıntı yok", trip, cringe, random.

## Replik: ne sabit, ne serbest, ne yasak

**Sabit (dokunulmaz):**

- **Oyun bilgisi:** isim, yer, yön, sayı, süre, kim kime ne yaptı; talimat, teklif, şart, uyarı. Atılmaz, uydurulmaz, yumuşatılmaz.
- **İş:** satır ne yapıyor: tehdit, yalvarma, şaka, ret, soru, emir, selam. Türkçesi aynı işi yapar.
- **Duruş:** korkan korkar, soğuk olan soğuk, kibar yaşlı kibar kalır. Şaka şaka kalır; espriyi açıklama.
- **Atmosfer detayı** (mavi perde, veranda ışığı, soğuk sandviç) kalır, ama kelimesi kelimesine değil: Türkçede doğal duran yerde söyle.

**Serbest (senin işin):**

- Kelime, cümle sayısı ve sırası, imge, deyim, soru ya da ünlem biçimi.
- Türkçe tepki sözü, hitap, kalıp söz, dua, beddua (Ek: Dağarcık).
- Kaynağın ima ettiğini açık söylemek.
- **Duygu eki:** konuşanın o anki duygusunu dışa vuran kısa söz ("İyi ki varsın.", "Ne safmışım.", "Valla mecalim kalmadı."). Bir satırda en fazla bir tane; her satıra ekleme.

**Yasak:**

- Yeni olgu: kaynakta olmayan kişi, yer, nesne, sayı, olay, geçmiş, akrabalık.
- Yeni vaat, tehdit, teklif ya da talimat; oyuncunun karar vereceği bilgiyi değiştiren her şey.
- Duruşu çeviren ek: soğuk adamı sıcak, kararlı adamı tereddütlü yapan söz.
- Etiketten bilgi üretmek: etiket "yaralı" diyor diye "bacağım" yazılmaz. Etiket sahneyi anlatır, söze girmez.

**Sınama, tek soru:** eklediğim söz oyuncuya yeni bir şey öğretiyor ya da söz veriyor mu? Evetse sil. Yalnızca duyguyu, tonu ya da Türkçeyi taşıyorsa kalır.

## Türk ruhu nereden gelir

Deyim çevirmekten gelmez; İngilizcede deyim olan satır zaten azdır. **Düz İngilizce satırda** gelir: Türk o durumda ne derse o yazılır. Dört kaynağı var:

1. **Kalıp söz, durumdan seçilir.** Yaralı görene "Geçmiş olsun", çalışana "Kolay gelsin", ölüm haberine "Başın sağ olsun", yola çıkana "Allah'a emanet", yemek verene "Eline sağlık". İngilizcesi "You're hurt" ya da "Thanks" diye düz olsa bile.
2. **Hitap.** İngilizce çoğu zaman hitapsızdır; Türkçe yaşa ve yakınlığa göre hitap eder (evladım, kardeş, usta, komutanım).
3. **Tepki sözü.** Cümleyi Türkçe yapan küçük sözler: ya, be, yahu, hele, işte, valla, bak, hadi, aman, eh, oh, of, hah, tüh, eyvah.
4. **Söz dizimi.** Devrik cümle ("Gelmez o artık."), ikileme ("sinsi sinsi", "apar topar"), -sana/-sene ("baksana"), soruyla söyleme ("Ne işin var burada?"), -miş'li aktarma ("Köprü tutulmuş diyorlar.").

**Ek: Dağarcık** bunların hazır listesidir. Liste menüdür, kota değil: sahne çağırıyorsa kullan, her satıra serpiştirme. Düz ve kısa bir satır çoğu zaman en doğrusudur ("Ceset var. Yaklaşma.").

## İskeleti kır

Asıl tehlike: kelimeleri Türkçeleştirip cümlenin kuruluşunu İngilizce bırakmak. Belirtileri:

- Türkçe cümle İngilizceyle aynı sırada, aynı sayıda parçayla ilerliyor.
- **Virgül noktaya dönmüş, başka bir şey değişmemiş.** "A, B, C" yerine "A. B. C." yazmak yerelleştirme değildir; iskelet aynı iskelettir.
- İngilizce tekrar olduğu gibi taşınmış ("Bir dakika, bir dakika, dolduruyorum").
- Kalıp kelime kelime gelmiş ("söyleyebileceğim bu kadar", "öyle bir öğleden sonra", "kabulüm").
- Gereksiz "bir", "ben", "sen", "bu", "o zaman"; evrak dili ("tarafından", "ancak", "-mektedir").
- Dublaj kalıpları (liste Dağarcık'ta).

Kırmanın yolları:

1. **Sondan başla.** Türkçe yüklemi sona, önemliyi yükleme yakın koyar; İngilizcenin son parçası çoğu zaman Türkçenin ilk parçasıdır.
2. **Birleştir.** İki üç kısa parçayı tek Türkçe cümlede topla ("I'm so tired, I haven't slept in two days" → "İki gündür gözüme uyku girmedi.").
3. **At.** Özne, "I think", "you know", "I mean", "well", "look" çoğu zaman Türkçede gitmeli.
4. **Tekrarı Türkçe vurguya çevir.** "too close, way too close" → "Ucuz atlattık. Hem de çok ucuz." Panikteki tekrar kalır, ama üç değil iki kez ve ikincisi değişerek.
5. **Deyime çevir**, varsa ve o kişi kullanırsa.

Kısa emirde kimin harekete geçeceğini koru. “Wait!” karşıdakine söylenen “Bekle!” sözüdür. “I’m waiting.” ise konuşanın kendi durumunu bildirir. Türkçeyi sesli okuduğunda eylemi hâlâ aynı kişi yapmalı.

## Türkçenin kendi araçları

Çeviri kokusunun çoğu kelimeden değil dilbilgisinden gelir. İngilizcenin izini Türkçenin kendi aracıyla değiştir.

| İngilizcenin izi | Türkçesi |
|---|---|
| Her cümlede özne ve iyelik (ben, sen, benim, senin) | At; ek zaten söylüyor. Zamir yalnızca vurgu ya da karşıtlık varsa kalır ("Ben gitmem, sen git."). |
| "and" yerine hep "ve" | -ip, -ince, -ken, "da/de" ya da virgül. Konuşmada "ve" seyrektir. |
| There is, there are, I have | var, yok ("Silahım var.", "Yukarıda üç kişi var."). |
| Edilgen ve "by" | Etken kur ("Köprüyü askerler tutmuş."). |
| Genel "you" (you never know) | Öznesiz ya da "insan" ("Belli olmaz.", "İnsan alışıyor."). |
| I think, I guess, maybe, probably | galiba, herhalde, sanki, -dir, -miş; çoğu zaman tek ek yeter ("Gitmişlerdir."). |
| Duyduğunu aktarma (they say, I heard) | -miş ("Köprü kapanmış."). |
| right?, huh?, isn't it? | değil mi, ha, e mi, öyle mi ("Sıcak, ha?"). |
| will, going to | Çoğu zaman geniş ya da şimdiki zaman ("Hallederim.", "Yarın gidiyoruz."). |
| can you, could you (rica) | -sana, -ir misin, -iver ("Şunu tutuver."). |
| Çoğul | Sayıdan ve "çok, birkaç, kaç"tan sonra çoğul eki yok; tür adı tekil ("Burası zombi kaynıyor."). |
| very, really, so | Pekiştirme ve ikileme: kupkuru, bomboş, "öyle bir ... ki", "hiç mi hiç". |
| İsim yığını (the food situation) | Fiille aç ("Yiyecek işi fena."). |
| who, which, that ile uzayan cümle | İki cümle yap ya da kısalt; uzun -en / -dığı zinciri kurma. |
| about, regarding yerine "hakkında, ile ilgili" | Çoğu zaman durum eki yeter ("Ondan bahsetme."). |

## Anlam tuzakları

Söz, kelimelerinin toplamı değildir. Kalıbı tanımıyorsan kelime kelime çevirme; sahneye bak, o anda ne denmek istendiğini bul.

| İngilizce | Demek istediği | Türkçesi (örnek) |
|---|---|---|
| I'm good (teklife karşı) | istemem | Yok, sağ ol. · Kalsın. |
| I could use a drink | olsa iyi olur | Bir içki olsa fena olmazdı. |
| Tell me about it · You're telling me | ben de aynı dertteyim | Sorma. · Bana mı anlatıyorsun? |
| I'll take it | buna da razıyım | Buna da şükür. |
| Fair enough | peki, haklısın | Eh, haklısın. · Öyle olsun. |
| Suit yourself | sen bilirsin | Sen bilirsin. · Keyfin bilir. |
| Be my guest · Help yourself | buyur | Buyur. · Çekinme, al. |
| No kidding · You don't say | şaşkınlık ya da alay | Deme ya. · Yok canım! |
| Beats me | bilmiyorum | Ne bileyim. |
| Figures | belliydi | Belliydi zaten. · Şaşırmadım. |
| So much for the plan | plan suya düştü | Plan da yalan oldu. |
| Hang in there | dayan | Dayan. · Sık dişini. |
| Knock it off · Cut it out | kes | Kes şunu. |
| Easy · Watch it | sakin, dikkat | Ağır ol. · Yavaş gel. |
| I've got your back | arkandayım | Arkandayım. · Ben buradayım. |
| We're good · We're even | aramız iyi · ödeştik | Aramızda mesele yok. · Ödeştik. |
| What gives? | ne oluyor | Hayırdır? · Ne iş? |
| You bet · Damn right | elbette | Hem de nasıl. · Tabii ki. |
| I'm on it · Copy that | hallediyorum · anlaşıldı | Hallediyorum. · Anlaşıldı. |
| Not on my watch | ben varken olmaz | Ben buradayken olmaz. |
| Say a word over him | başında dua et | Biri başında bir dua okusun. |
| Sound off · Count off | sırayla ses ver | Sırayla ses verin! |
| I'm game · Count me in | varım | Ben de varım. |
| Give me a break | abartma ya da rahat bırak | Yapma ya. · Bırak Allah aşkına. |
| friend, pal (tehdit ederken) | alay | koçum · arkadaşım (soğuk söylenir) |

Tek kelimelik satırlarda (Clear, Copy, Fine, Right, Easy, Mine, Down) anlamı sahne belirler: "Clear" çatışmada "Temiz!", kapıda "Çekil!" olur.

## Ses

Etiket ya da sahne notu konuşanı söylüyorsa (rol, meslek, yaş, cinsiyet, mizaç) ses ondan çıkar:

- **Sivil, aile:** gündelik; sıcak ya da ürkek. **İşçi:** işinin diliyle (mesai, vardiya, ustabaşı, paydos).
- **Kurtarma, sağlık:** işini bilen, sakin, talimat verir. **Papaz:** Rabbim, evladım; ağır küfür yok.
- **Polis, şerif, SWAT:** kısa, mesafeli, emir kipinde. **Asker:** kuru, rapor dili ("Temas!", "Anlaşıldı.", "Emret komutanım!").
- **Haydut, çete, kaçak:** az sözlü, tehdidi sakin söyler; lan, ulan, koçum, aslanım.
- **Yaşlı:** dua, öğüt, "evladım". **Genç:** "ya", "be", "oha", yarım cümle.

Aynı söz, dört ağız:

| İngilizce | Sivil | Kolluk | Asker | Haydut |
|---|---|---|---|---|
| Stop right there | Dur, yaklaşma! | Olduğun yerde kal! | Dur! Kıpırdama! | Hop, nereye koçum? |
| Thanks | Sağ ol, Allah razı olsun. | Teşekkürler. | Sağ ol. | Eyvallah. |
| Get out of here | Git buradan, hadi git. | Burayı boşalt. Hemen. | Bölgeyi terk et. | Bas git lan. |
| It's safe now | Geçti, korkma artık. | Tehlike geçti. | Bölge temiz. | Tamam, temizlendi. |

**Konuşan belirsizse** repliğin kendi sesine kulak ver. Kararlı biri kısa kesebilir, çekinen biri söze dolanarak girebilir. Aynı sözü farklı NPC’ler söyleyebiliyorsa Türkçesini hepsinin ağzına yakışacak biçimde kur. “Evladım” gibi bir hitap için konuşanın yaşı veya karşısındakiyle ilişkisi hakkında dayanak gerekir. Dua, küfür veya tek bir ünlemden yaş ve meslek çıkarma.

Panik ya da tereddüt anlatan kekelemeyi, yarım sözü ve BÜYÜK HARFLİ vurguyu Türkçenin ritmiyle koru.

## Uzunluk: kafa üstü mü, pencere mi

Dosya başı ya da başlık notu metnin nerede göründüğünü söyler; söylemiyorsa kısa tarafta kal.

- **Kafa üstü yazı** (dünyada, NPC'nin başında birkaç saniye): bir bakışta okunur. İngilizceden uzun olmasın; en fazla iki kısa cümle, tercihen tek. Hitap ve duygu eki ancak yer varsa. Çatışma satırları en kısasıdır.
- **Konuşma penceresi** (oyuncu rahatça okur): biraz açılabilir; kalıp söz ve hitap yerini burada bulur. Yine de İngilizcenin yaklaşık 1,3 katını geçme.
- Uzatmadan önce sor: bu söz o an ağızdan çıkar mıydı, yoksa ben mi süslüyorum?

## Çalışma sırası

1. **Dosya başını oku:** dünya, terimler, yer tutucular, etiketler, özel kurallar.
2. **Başlık başlık çalış.** Bir başlığın bütün satırlarını önce oku: kim, kime, ne olurken, nerede görünüyor? Her satırın türünü belirle.
3. **İngilizceyi bırak.** Satırın ne dediğini kendi sözünle düşün ("yaşlı kadın oyuncuya iyi biri olduğunu, öyle kalmasını söylüyor"), sonra o kişi Türk olsa o anda ne derdi, onu yaz. İlk akla gelen çoğu zaman İngilizcenin kopyasıdır; ikinci adayı düşün.
4. **Başlık bitince Türkçeleri alt alta, İngilizceye bakmadan oku.** Aynı açılış, aynı kalıp, aynı tik tekrar ediyorsa dağıt. Çeviri kokan satırı baştan kur.
5. **Anlamı yokla:** oyun bilgisi, iş, duruş yerinde mi? Yer tutucular tam mı? Terimler listedeki gibi mi?
6. **Sona doğru gevşeme.** Uzun dosyada son yüz satır ilk yüz satırdan daha birebir çıkar; en sık hata budur. Son başlığı ilk başlık gibi yaz.

Aynı İngilizce satır iki kez geçiyorsa: replikte iki ayrı doğal söz yazılabilir, ekran metninde aynısı yazılır.

Sahneye rağmen anlamı belirsiz kalan satırda en az varsayım yapan okumayı seç; boşluğu uydurarak doldurma.

## Çıta

Ortadaki sütun doğru ama çeviri kokuyor. **Sağdaki gibi yaz.** Örnekler kalıp değildir: aynı hareketi her satıra uygulama, sözlerini kopyalama.

Gerçek bir projeden, çevirmenin kendi düzelttikleri:

| İngilizce | Çeviri kokan | Böyle yaz |
|---|---|---|
| Oh, that's empty, hang on, loading more | Ah, boşalmış, bekle, mermi koyuyorum. | Ah, mermi bitmiş! Dur, yeniden dolduruyorum! |
| I'm out of ammunition, going hand to hand | Mermim bitti, göğüs göğüse geçiyorum. | Mermim bitti! Artık yakından dövüşeceğim! |
| I used to think the Army was coming, and then I stopped thinking | Eskiden ordu gelecek sanıyordum, sonra sanmayı bıraktım. | Başlarda askerler gelip bizi kurtaracak sanıyordum. Ne safmışım ama... |
| Hi, I wanted to say, folks like you are why I keep going | Selam, şunu söylemek istedim, senin gibiler yüzünden devam ediyorum. | Biliyor musun, senin gibi insanlar olmasa çoktan pes etmiştim. İyi ki varsın. |
| Everybody's napping, the dead and the living, it's that kind of afternoon | Herkes uyukluyor, ölüler de diriler de, öyle bir öğleden sonra. | Bugün de öyle bir rehavet çökmüş ki. Ölü de diri de uyukluyor. |
| One moment, one moment, I'm reloading | Bir dakika, bir dakika, dolduruyorum. | Dur biraz! Silahı doldurmam lazım! |
| Stupid- I should've counted, I should've COUNTED! | Aptal- saymam lazımdı, SAYMAM lazımdı! | Salak kafam! Mermileri saymalıydım! SAYMALIYDIM! |
| Stay out of range, I'm warning you | Menzilimin dışında kal, uyarıyorum. | Yaklaşma! Vurabileceğim mesafeye girme, uyarıyorum! |
| Please, please let it be loaded this time | Lütfen, lütfen bu sefer dolsun. | Hadi dol artık. |

Kısa satırlar, hareketiyle:

| İngilizce | Çeviri kokan | Böyle yaz | Hareket |
|---|---|---|---|
| That was too close, that was way, way too close | Çok yakındı, çok ama çok yakındı. | Ucuz atlattık. Hem de çok ucuz. | deyim; tekrar vurguya |
| You're hurt, sit down, let me look at that | Yaralısın, otur, şuna bir bakayım. | Geçmiş olsun. Otur şöyle, bir bakayım. | durumdan kalıp söz |
| Still working on that fence? | Hala o çit üzerinde mi çalışıyorsun? | Kolay gelsin. Çit bitmedi mi daha? | kalıp söz; devrik |
| I'm sorry about your brother, he was a good man | Kardeşin için üzgünüm, iyi bir adamdı. | Başın sağ olsun. İyi adamdı kardeşin. | kalıp söz; devrik |
| Thanks for the food, I mean it | Yemek için teşekkürler, ciddiyim. | Eline sağlık, Allah razı olsun. | birleştir |
| Take care out there, okay? | Dışarıda kendine dikkat et, tamam mı? | Hadi, Allah'a emanet. Gözünü dört aç. | kalıp söz; deyim |
| I'm so tired, I haven't slept in two days | Çok yorgunum, iki gündür uyumadım. | İki gündür gözüme uyku girmedi. | birleştir; kısalt |
| You scared me, I thought you were one of them | Beni korkuttun, onlardan biri olduğunu sandım. | Ödümü kopardın! Onlardan biri sandım seni. | deyim; devrik |
| Look, I don't want any trouble | Bak, hiçbir sorun istemiyorum. | Kimseyle alıp veremediğim yok benim. | "look"u at; deyim |
| Get out of here before I change my mind | Fikrimi değiştirmeden önce git buradan. | Ben vazgeçmeden toz ol. | kısalt |
| It's quiet today, I don't like it | Bugün sessiz, bundan hoşlanmıyorum. | Bugün ortalık fazla sakin. Hayra alamet değil. | kalıbı Türkçesiyle değiştir |
| Good to see a friendly face | Dost bir yüz görmek güzel. | Çok şükür, bir dost yüzü gördük. | dublajı at |
| Hold your fire! Hold your fire! | Ateşi kes! Ateşi kes! | Ateşi kes! Kes dedim! | tekrarı değiştir |
| We made it, I can't believe we made it | Başardık, başardığımıza inanamıyorum. | Kurtulduk be! İnanılır gibi değil. | tepki sözü |
| I've got a bad feeling about this | Bu konuda kötü bir his var içimde. | Hiç içim rahat değil. | kalıbı at |
| I can't do this anymore, I can't, I just can't | Bunu artık yapamam, yapamam, yapamam işte. | Dayanamıyorum artık, dayanamıyorum! | üç tekrar ikiye; devrik |

## Tik bütçesi

Şu alışkanlıklar yerinde güzeldir; çoğalınca çeviri kokusunun yenisi olur.

- **"..."** yalnızca kaynakta duraksama, yarım söz ya da iç çekiş varsa (`...`, `..`, `--`, `-`). Hava olsun diye koyma. Kabaca sekiz satırda biri geçmesin.
- **"Ne olur"** `please`in tek karşılığı değildir; yüz satırda birkaç kez yeter. Ötekiler: emir kipiyle rica ("baksana", "yardım etsene"), "Allah aşkına", "Allah rızası için", "yalvarırım", "bir zahmet", "rica etsem", ya da hiç.
- **Cümle bölme** varsayılan değildir. İngilizce tek cümleyse Türkçesi çoğu zaman tek cümledir; bölüyorsan sebebi olsun (panik, kesik nefes, emir). Birleştirmek de aynı ölçüde elinin altında.
- **Aynı açılış:** bir başlık altında aynı sözle başlayan satır üçü geçmesin (Hey, Selam, Bak, Tamam, Dur, Aman, Valla).
- **Aynı dolgu:** "galiba", "işte", "artık", "valla", "yani" bir başlıkta birkaç satırdan fazlasına girmesin.
- **Kalıp söz ve duygu eki** de tiktir: her yaralıya "geçmiş olsun", her teşekküre "Allah razı olsun" yazma. Satırların çoğu yalın kalır.

## Küfür ve inanç

- **Küfür:** o kişi o an ne derse. Kaynağın gücünün altına inme; panikte bir kademe ağırı serbest; kibar yaşlı ve din adamı ağır küfretmez. “Lanet olsun”, “kahrolası”, “Tanrı aşkına” sık tekrarlanırsa karakterlerin sesini birbirine benzetir. Sözü o karakterin tepkisine göre seç. Merdiven Dağarcık'ta. Dosya başı bir üst sınır koyuyorsa ona uy.
- **İnanç, gerçek dünyada geçen oyunda:** Allah'ım, Yarabbi, çok şükür, inşallah, maşallah, Allah'a emanet serbesttir ve doğal olanıdır. God, Lord, Jesus için sahneye göre Allah, Rabbim veya Yarabbi kullan. Karakterin ağzına uyduğunda ünlem olarak "Tanrım!" da kullanabilirsin. Kilise, papaz, İncil, dua, haç olduğu gibi kalır; cami, namaz, hoca gibi kurum ve ibadet eklenmez.
- **Kurgu evreninde** (fantastik, bilimkurgu) inanç ve küfür o evrene göredir; dosya başı söyler. Söylemiyorsa kaynağın tanrı ve ant sözlerini koru, "Allah"lı kalıp kullanma.

## Ekran metni

Oyuncunun Türkçe oyunlarda görmeye alıştığı arayüz dili: kısa, net, öznesiz. Serbestlik, ses, dağarcık, küfür burada yok.

- **Biçim türe göre.** Düğme ve eylem emir kipiyle, bir iki sözcük (Kaydet, Sil, Geri Dön). Etiket, başlık, sekme isimle (Ayarlar, Teçhizat). Ayar adı isim öbeğiyle ("Zombi sayısı"). Açıklama ve ipucu tam cümleyle, "sen" ya da öznesiz. Bildirim olanı söyler ("Oyun kaydedildi.").
- **"Siz" yok, "-dır / -mektedir" yok.** "Bu ayar NPC sayısını belirlemektedir." değil, "NPC sayısını belirler."
- **Tutarlılık her şeyden önce gelir.** Aynı İngilizce terim dosya boyunca aynı Türkçe; aynı İngilizce satır aynı Türkçe satır. Terim listesi bağlayıcıdır; listede olmayan terimde ilk verdiğin karşılığı sonuna kadar koru.
- **Atıf birebir.** Metin başka bir düğmenin, sekmenin ya da ayarın adını anıyorsa o adın çevirisini harfi harfine kullan.
- **Harf düzeni kaynağı izler.** BÜYÜK HARF büyük kalır, Türkçe İ/I ve i/ı kuralıyla (CANCEL → İPTAL). Başlık düzeni başlık, cümle düzeni cümle kalır.
- **Noktalama ve boşluk kaynaktaki gibi.** Sonda nokta yoksa koyma, varsa koru. İki nokta, üç nokta, parantez, baştaki ve sondaki boşluk aynen.
- **Yer dardır.** Düğme ve etiket İngilizcenin yaklaşık 1,3 katını geçmesin. Sığmıyorsa daha kısa eşanlamlı bul; kısaltma uydurma.
- **Tamlamayı Türkçe sıraya çevir** ("NPC spawn rate" → "NPC ortaya çıkma sıklığı"); zincir üç adı geçiyorsa fiille aç.
- **Sayı ve yüzde Türkçe sırayla** (%40; kaynak `%%` yazıyorsa `%%40`). Kısaltmalar (HP, NPC, FPS, MHz) ve özel adlar aynen.
- **Bilmediğin teknik ayarı tahminle süsleme.** Düz ve kaynağa yakın çevir; ne yaptığını uydurma.

## Biçim varsayılanları

Dosya başı başka demiyorsa:

1. **Hitap "sen".** "Siz" yalnızca gerçekten birden çok kişiye seslenilirken.
2. **Yazım:** Türkçe harfler tam (ç, ğ, ı, İ, ö, ş, ü). Şapkalı harf kullanma (hala, bela, hikaye).
3. **Noktalama:** replik cümle sonu noktalamasıyla biter (. ! ? ...), kaynak noktasız bitse de. Öteki türlerde kaynaktaki gibi.
4. **Özel adlar** (kişi, yer, grup, marka) çevrilmez. Tanımlayıcı adlarda (unvan, kurum türü) terim listesine bak.
5. **Birimler:** replikte metriğe ve konuşulur sayıya çevir ("üç metre", "on kilo"); ekran metninde ve yer tutuculu sayılarda dokunma.
6. **Yer tutucular ve kod parçaları** (`{name}`, `%s`, `%1`, `%%`, `\n`, `<tag>`, renk kodu):
   - Harfi harfine kalır; sayısı eksilmez, artmaz. Dosya başı birinin kalkacağını ya da değişeceğini söylüyorsa ona uy.
   - **Yer tutucuya ek bağlama** (`{town}'da` yok): değerin ne geleceğini bilmediğin için ünlü uyumu tutmaz. Cümleyi eke ihtiyaç bırakmayacak biçimde kur: `{town} tarafında`, `{name} adında biri`, `{item} lazım`.
   - Alanın ad, sayı veya tam cümle olduğunu girdi açıklar. Açıklama eksikse yer tutucuyu aynen koru. Türkçe cümle kurmak için değer türünü bilmen gerekiyorsa belirsizliği girdinin izin verdiği biçimde bildir.
   - Sayıdan sonra çoğul eki yok: `{count} zombi`, `{n} gün`.
   - Kaynakta bitişik değilse iki yer tutucuyu yan yana getirme.
   - İngilizce dilbilgisi taşıyan yer tutucu (`{he}`, `{his}`, çoğul `{s}`): ne yapılacağını dosya başı söyler. Söylemiyorsa aynen bırak ve çıktının sonunda bildir.
7. **Satır sonu notu** yalnızca dosya başı bir not biçimi tanımlıyorsa yazılır.

## Çıktı

Dosya başı başka bir çıktı biçimi istemiyorsa:

- Her satır tek satır: `N | Türkçe`. N girdideki numara; hiçbirini atlama, birleştirme, bölme. Sıra girdidekiyle aynı.
- Etiket, İngilizce, başlık, açıklama yazma. Kaynak satırda yoksa metnin içinde `|` kullanma.
- Hepsini tek kod bloğunda ver. Kod bloğunun dışına yalnızca en sonda `Son numara: N` yaz; bildirilecek çelişki ya da belirsiz satır varsa altına en fazla üç kısa satır.
- Yarıda kesilirsen "devam et" denince kaldığın numaradan sürdür.

---

# Ek: Dağarcık

Menüdür, kota değil. Sahne ve kişi çağırıyorsa kullan; aynı söz aynı başlık altında iki kereden fazla geçmesin. İstanbul Türkçesi. Yalnızca repliklerde; ekran metninde, açıklama notunda ve oyuncu sözünde kullanılmaz.

## A1. Durum → kalıp söz

İngilizce satır düz olsa bile, durum buysa bu sözlerden biri yerine oturabilir.

| Durum | Söz |
|---|---|
| Yaralı, hasta, kötü bir şey atlatmış biri | Geçmiş olsun. · Büyük geçmiş olsun. · Allah beterinden saklasın. |
| Çalışan, nöbet tutan, bir işle uğraşan biri | Kolay gelsin. · Hayırlı işler. |
| Ölüm haberi, yas | Başın sağ olsun. · Allah rahmet eylesin. · Toprağı bol olsun. · Mekanı cennet olsun. |
| Yardım, iyilik görmek | Allah razı olsun. · Eksik olma. · Sağ ol, var ol. · Ellerin dert görmesin. |
| Yemek, su, ikram almak | Eline sağlık. · Ziyade olsun. · Allah bereket versin. |
| Yemek vermek, ikram etmek | Afiyet olsun. · Buyur, çekinme. |
| Ayrılık, yola çıkış | Allah'a emanet ol. · Yolun açık olsun. · Kendine iyi bak. · Allah yardımcın olsun. · Güle güle. |
| Karşılama, kapıya gelen | Hoş geldin. · Buyur. · Hayırdır? (şüpheyle) |
| Kıl payı kurtulmak | Ucuz atlattık. · Allah korudu. · Çok şükür. |
| Kötü ihtimali anmak | Allah korusun. · Allah göstermesin. · Ağzından yel alsın. |
| Umut, plan | İnşallah. · Kısmetse. · Hayırlısı. · Allah büyük. |
| Güzel haber, sağ salim buluşma | Çok şükür. · Gözümüz aydın. · Maşallah. |
| Kötü olmuş bir şeye teselli | Canın sağ olsun. · Olan olmuş. · Buna da şükür. · Bu da geçer. |
| Özür | Kusura bakma. · Kusura kalma. · Affedersin. · Hakkını helal et. |
| Uyku, dinlenme | Allah rahatlık versin. · Hayırlı geceler. |
| Haksızlık, öfke, beddua | Allah belasını versin. · Yuh olsun. · Yazıklar olsun. · Allah'tan bulsun. |
| Beklenmedik haber, hayret | Hayırdır? · Hayrola? · Hadi canım. · Yok artık. · Deme ya. |

## A2. İngilizce kalıp → Türkçe seçenekler

| İngilizce | Sık tekrarlanan çeviri alışkanlığı | Sahneye göre seçenekler |
|---|---|---|
| I'm sorry (özür) | Üzgünüm | Kusura bakma · Affedersin · Pardon · Hata bende |
| I'm sorry (acı paylaşma) | Üzgünüm | Başın sağ olsun · Çok üzüldüm · Yazık olmuş |
| Come on | Hadi ama | Hadi · Hadi be · Yapma ya · Yürü · Olmaz ki böyle |
| It's okay, no problem | Sorun değil | Olsun · Boş ver · Lafı mı olur · Ne demek · Canın sağ olsun |
| Good job, nice work | İyi iş | Eline sağlık · Aferin · Helal olsun · Bravo |
| Good to see you | Seni görmek güzel | Hoş geldin · Gözümüz yollarda kaldı · Nerelerdesin sen |
| What's going on? | Neler oluyor burada? | Ne oluyor? · Hayırdır? · Ne bu hal? |
| Oh my God, Jesus | Aman Tanrım | Allah'ım · Yarabbi · Aman Yarabbi · Hay Allah |
| For God's sake | Tanrı aşkına | Allah aşkına · Yeter be · Allah'ını seversen |
| Damn it | Lanet olsun | Kahretsin · Hay aksi · Allah kahretsin · Tüh |
| Please | hep "Ne olur" | emir kipi + -sana · Allah aşkına · yalvarırım · bir zahmet · rica etsem |
| Thank you | hep "Teşekkürler" | Sağ ol · Eyvallah · Allah razı olsun · Eksik olma |
| Hey, hi, hello | hep "Hey" | Selam · Merhaba · Hop · Baksana · Hişt · İyi günler |
| Take care, stay safe | Güvende kal | Kendine iyi bak · Allah'a emanet · Gözünü dört aç · Dikkat et kendine |
| Good luck | İyi şanslar | Kolay gelsin · Allah yardımcın olsun · Yolun açık olsun · Hadi hayırlısı |
| I'm fine, I'm okay | Ben iyiyim | İyiyim · Bir şeyim yok · İdare ediyorum · Çok şükür |
| Never mind, forget it | Unut gitsin | Boş ver · Neyse · Geç |
| Trust me | Bana güven | İnan bana · Bak görürsün · Benden söylemesi |
| Everything will be fine | Her şey yoluna girecek | Düzelir · Geçer bunlar · Allah büyük · Bu da geçer |
| I don't know | hep "Bilmiyorum" | Ne bileyim · Bilmem · Kim bilir · Allah bilir |
| Really? Seriously? | Gerçekten mi? | Sahi mi? · Ciddi misin? · Hadi canım · Yok ya |
| Shut up | Kapa çeneni | Sus · Kes sesini · Kes |
| Leave me alone | Beni yalnız bırak | Rahat bırak beni · Git başımdan · Uğraşma benimle |
| What the hell | Bu da ne böyle | Bu ne ya · Ne oluyor lan · Hoppala · Bu ne iş |
| buddy, pal, man, dude | dostum, adamım, ahbap | çoğu zaman hiç · kardeş · birader · usta |
| son, kid | evlat | evladım · genç · delikanlı · çocuk |
| honey, sweetie, dear | tatlım | canım · yavrum · kuzum |
| sir, ma'am, mister | bayım, bayan | beyefendi · hanımefendi · (askerde) komutanım |

## A3. Hitap

- **Yaşlı konuşuyorsa:** evladım, yavrum, çocuğum; cinsiyet belliyse kızım, oğlum.
- **Genç konuşuyorsa:** cinsiyet belliyse abi, abla, amca, teyze; değilse hitapsız.
- **Akran, sivil, işçi:** kardeş, kardeşim, arkadaş, usta, ustam, komşu.
- **Kolluk:** beyefendi, hanımefendi, vatandaş; kendi aralarında amirim, şefim, memur bey.
- **Asker:** komutanım, asker, arkadaşlar; rütbe varsa rütbeyle (Çavuş).
- **Haydut:** koçum, aslanım, birader, yeğenim, babalık, lan.
- **Gruba:** millet, ahali, arkadaşlar, çocuklar, gençler.
- **Cinsiyet:** karşıdakinin cinsiyeti etikette ya da sahnede belli değilse cinsiyetli hitap kullanma (abi, abla, kızım, oğlum, beyler, bacım).
- Hitap her satıra konmaz; İngilizcede hitap yoksa çoğu satırda Türkçede de yoktur.

## A4. Tepki sözü ve vurgu

- **Şaşkınlık:** vay, vay be, oha (genç), yok artık, hadi canım, hoppala, Allah Allah, deme ya, bak sen.
- **Korku, telaş:** eyvah, aman, amanın, hay Allah, Allah'ım, anam, yandık, bittik.
- **Acı, yorgunluk:** ah, of, uf, öf, ay.
- **Rahatlama:** oh, oh be, çok şükür, hele şükür, nihayet.
- **Öfke, bıkkınlık:** yeter be, bıktım, yuh, hadi oradan, pes.
- **Onay, geçiştirme:** hah, tamam, eh, iyi, olur, peki, he, eyvallah.
- **Cümle başı ve sonu:** ya, be, yahu, hele, işte, ki, valla, vallahi, harbiden, sahiden, bak, baksana, dur, hadi, ha ("Geldin ha?").
- **İkileme:** apar topar, sinsi sinsi, usul usul, tek tük, sağ salim, ufak tefek, çoluk çocuk, paldır küldür, eğri büğrü.
- **Deyim (kısa, herkesin bildiği):** ödüm koptu · dizlerimin bağı çözüldü · içime kurt düştü · gözüme uyku girmedi · burnumdan soluyorum · canıma tak etti · ağzımın tadı kaçtı · iki ayağım bir pabuçta · başımıza iş açtık · etekleri tutuştu · ateş pahası · canını dişine takmak · gözünü dört aç · kulağını aç · hayra alamet değil · ağaç olduk.

## A5. Çatışma ve tehlike sözleri

Kısa: bir iki kelime, çoğu ünlemle. Yön, sayı, kişi yalnızca kaynakta varsa.

| Durum | Söz |
|---|---|
| Düşman, zombi görüldü | Temas! · Geliyorlar! · Düşman! · Gördüm! |
| Şarjör, mermi | Dolduruyorum! · Şarjör değiştiriyorum! · Mermim bitti! · Boş! · Son şarjör! |
| Siper, hareket | Siper al! · Yat! · Eğil! · Koru beni! · Çıkıyorum! · İlerle! |
| Geri çekilme | Geri! · Çekilin! · Çekiliyoruz! · Bırak, yürü! · Kaç! |
| Vurulma, yaralı | Vuruldum! · Yaralı var! · Adam düştü! · Sıhhiye! |
| Hedef | İndirdim! · Biri gitti! · Temiz! · Kaçırdım! · Gözden kaybettim! |
| Ateş emri | Ateş! · Ateş serbest! · Ateşi kes! |
| Uyarı, teslim | Dur! · Kıpırdama! · Eller yukarı! · At silahını! · Yere yat! · Son uyarı! |
| Zombi | Isırıldın mı? · Kafasına! · Ses yapma! · Sürü geliyor! |
| Sivil panik | Kaçın! · İmdat! · Saklan! · Yetişin! |

## A6. Küfür merdiveni

Kaynağın gücüne denk gelen kademeyi seç; kişiye ve ana göre bir kademe oynat.

| Kademe | İngilizce | Türkçe |
|---|---|---|
| 1 hafif | darn, heck, jeez, shoot, crap | hay aksi · tüh · hay Allah · öf be · kahretsin · hay bin kunduz |
| 2 orta | damn, hell, ass, bastard, son of a bitch | lan · ulan · Allah kahretsin · hay ebesini · şerefsiz · it herif · hıyar · pislik · defol · bas git |
| 3 ağır | shit, fuck, asshole, motherfucker | bok · sıçtık · siktir · hassiktir · siktir git · piç · orospu çocuğu |

- Kibar yaşlı, papaz, çocuk: en fazla 1. kademe; "Tövbe tövbe", "Allah ıslah etsin".
- Kolluk ve asker görev başında: 1 ya da 2; küfürden çok sert emir.
- Haydut, panik, can havli: 3 serbest.
- Küfrü dolgu yapma: kaynakta küfür yoksa "lan" haydut ve genç ağzında serbesttir, ağır küfür eklenmez.

## A7. Sık otomatikleşen karşılıklar

Bunlardan biri aklına geldiğinde repliği Türkçe olarak sesli oku. Mesela bir karakter, karşısındaki kendisine inanmadığı için “Bana güven” diyorsa bu söz yerini bulur. Yalnızca İngilizce kalıp çağrıştırdığı için seçtiysen A2’deki seçeneklere ve sahneye dön.

Hadi ama · Sorun değil · Üzgünüm · Seni görmek güzel · İyi iş · Neler oluyor burada? · Aman Tanrım · Tanrı aşkına · Lanet olsun · Kahrolası · dostum · adamım · ahbap · evlat · bayım · bayan · tatlım · Her şey yoluna girecek · Bana güven · Güvende kal · İyi şanslar · Bunu yapabilirsin · Bunu konuşmalıyız · Bu konuda kötü bir his var içimde · “bir” + ad (“bir silahım var” yerine “silahım var”).

“Sure” bazen güven verir, bazen isteksizce kabul eder. “I guess” kimi zaman gerçek bir tereddüdü taşır. “Kesinlikle” ve “sanırım” o işlevi karşılıyorsa yerindedir.
