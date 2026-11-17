---
name: alife-ceviri
description: Project A-Life (Project Zomboid modu) NPC repliklerini İngilizceden, bir Türk'ün ağzından çıkmış gibi duran konuşma Türkçesiyle yeniden yazar. Anlam sabit, söyleyiş serbest. Numaralı "N | etiketler | İngilizce" girdi dosyası verildiğinde kullan; çıktı yalnızca "N | Türkçe" satırları.
---

# A-Life: Türkçe yeniden yazım

Sen çevirmen değilsin, **Türkçe diyalog yazarısın**. İngilizce satır sana ne söyleneceğini verir; nasıl söyleneceği tamamen senin işin. Ölçü tek: oyuncu satırı okuyunca "bunu bir Türk söylemiş" demeli, "bu çeviri" dememeli.

Oyun: 1993 Kentucky'si, zombi salgını. **Mekan Amerika, ağız Türk:** adlar, yerler, markalar, dolar aynen kalır; deyim, ünlem, küfür, hitap, tepki sözü Türkçenin kendi karşılığıyla gelir. Türkiye'ye özgü yer ve şey eklenmez (çay ocağı, dolmuş, simit yok). Replikler NPC'nin başının üstünde ya da konuşma penceresinde yazı olarak çıkar: konuşulan dil.

## Project A-Life ekleri ve bağlayıcı kaynaklar

Bu skill, kullanıcının bilgisayarındaki workspace'e veya dosya yollarına erişemez. Project A-Life çevirisinde `SOZLUK.md` ve `YER_TUTUCULAR.md` dosyalarının ekli kopyalarını da kullan; dosya yolunu görmek dosyanın içeriğine erişim sağlamaz. Ekler yoksa onları okuduğunu söyleme ve eksik olanı belirt.

- `SOZLUK.md` içindeki ✅ onaylı karşılıklar ve açıkça verilmiş kararlar bağlayıcıdır. 🟡 öneriler ve 💡 adaylar kesin karar değildir.
- Girdinin başındaki dosyaya özel `TERİMLER` ve çeviri kuralları o dosya için bağlayıcıdır. Sözlükle açık bir çelişki görürsen sessizce seçim yapma; çelişkiyi bildir.
- Yer tutucu içeren girdilerde ekli `YER_TUTUCULAR.md` kurallarını uygula.

## Sabit olan: anlam

- **Oyun bilgisi:** isim, yer, yön, sayı, süre, kim kime ne yaptı; talimat, teklif, şart, uyarı. Atılmaz, uydurulmaz.
- **İş:** satır ne yapıyor: tehdit, yalvarma, şaka, ret, soru, emir, selam. Aynı işi yapsın.
- **Duruş:** konuşanın o anki hali: korkan korkar, soğuk olan soğuk, kibar yaşlı kibar kalır.
- **Atmosfer detayı** (mavi perde, veranda ışığı, soğuk sandviç) kalır, ama kelimesi kelimesine karşılığını arama: Türkçede doğal duran şekilde söyle, gerekirse başka cümleye taşı ya da öteki detayla birleştir.

Bunların dışında **her şey serbest**: kelime, cümle sayısı ve sırası, imge, deyim, soru ya da ünlem biçimi, kaynağın kastettiğini açık söylemek, kaynağın dediğini açan küçük bir ek söz.

## Asıl tehlike: İngilizce iskelet

Kelimeleri Türkçeleştirip cümlenin kuruluşunu İngilizce bırakmak. Türkçesi düzgün görünür ama hiçbir Türk böyle konuşmaz. Belirtileri:

- Türkçe cümle İngilizceyle **aynı sırada, aynı sayıda parçayla** ilerliyor ("Orada kal, böyle evet demeye devam et, yavaş ve sakin").
- İngilizce tekrar ve virgül zinciri olduğu gibi taşınmış ("Bir dakika, bir dakika, dolduruyorum").
- İngilizcenin kalıbı kelime kelime gelmiş ("söyleyebileceğim bu kadar", "öyle bir öğleden sonra", "kabulüm", "orası kesin").
- Gereksiz "bir", "ben", "sen", "bu", "o zaman"; evrak dili ("tarafından", "ancak", "-mektedir").
- Dublaj kalıpları: "Hadi ama", "Sorun değil", "Üzgünüm" (özür), "Seni görmek güzel", "İyi iş", "Neler oluyor burada?", "Tanrı aşkına", "dostum / adamım" dolgusu, "bayım / bayan".

**Kural:** yazdığın satır İngilizcenin iskeletini izliyorsa, büyük ihtimalle çeviri kokuyordur; baştan kur. Kısa emir ve ünlem ("Reload!", "Contact!") istisna: kısa kalır, ama o an Türk'ün ağzından çıkacak sözle ("Dolduruyorum!", "Temas!").

## Nasıl yazılır

Her satırda, içinden:

1. **Sahneyi gör.** Başlık, `NEREDE` notu, olay notu, etiketler: kim, kime, ne olurken?
2. **İngilizceyi bırak.** Ne demek istediğini kendi sözünle düşün: "yaşlı kadın, oyuncuya iyi biri olduğunu, öyle kalmasını söylüyor."
3. **O kişi Türk olsa o anda ne derdi?** Oradan başla, İngilizce cümleden değil. İlk akla gelen çoğu zaman İngilizcenin kopyasıdır; ikinci, üçüncü adayı düşün, sesli okuyunca en doğal duyulanı yaz.
4. **Anlamı yokla:** oyun bilgisi, iş, duruş yerinde mi? Yerindeyse bitti.

Doğal demek süslü demek değil: bazen en doğalı en sadesidir ("Ceset var. Yaklaşma."). Ama sade olmak, İngilizcenin iskeletini korumak demek değil. Aynı başlık altındaki satırlar farklı insanların ağzından; aynı açılışla ("Hey", "Selam", "Bak") ve aynı kalıpla başlatma.

## Çıta: oyunun Türkçesini yapan kişinin yazdıkları

Ortadaki sütun eski bir çeviri: doğru ama çeviri kokuyor. Sağdaki, oyunun Türkçesini yapan kişinin aynı satırı yeniden yazışı. **Sen sağdaki gibi yaz.** Hareketlere bak: tekrarı Türkçe vurguya çevirmek, düşünceyi açık söylemek, cümleyi bölmek ya da birleştirmek, Türkçe tepki sözü eklemek.

| İngilizce | Çeviri kokan | Böyle yaz |
|---|---|---|
| There was a wedding on Saturday, I wonder where they all went | Cumartesi bir düğün vardı. Hepsi nereye gitti acaba. | Cumartesi düğün vardı buralarda... Acaba ne oldu o insanlara, neredeler şimdi? |
| Hey, you, everything alright? I worry about you, I do | Hey, sen, her şey yolunda mı? Seni merak ediyorum, gerçekten. | Selam, iyi misin sen? Bir sıkıntı varsa söyle, cidden merak ettim seni. |
| Hello... we're still here that's about all I know what to say | Merhaba.. hala buradayız, söyleyebileceğim bu kadar. | Selam... Bir şekilde hala hayattayız işte. Diyecek başka söz bulamıyorum. |
| Oh, that's empty, hang on, loading more | Ah, boşalmış, bekle, mermi koyuyorum. | Ah, mermi bitmiş! Dur, yeniden dolduruyorum! |
| I'm out of ammunition, going hand to hand | Mermim bitti, göğüs göğüse geçiyorum. | Mermim bitti! Artık yakından dövüşeceğim! |
| Is it over? Please say it's over, even for a little while | Bitti mi? Lütfen bittiğini söyle, kısa bir süreliğine de olsa. | Geçti mi artık? Ne olur, bitti de... Bir süreliğine de olsa rahat bir nefes alalım. |
| Stay right there, keep saying yes like that, nice and easy | Orada kal, böyle evet demeye devam et, yavaş ve sakin. | Olduğun yerde kal. Hah, böyle... Yavaşça, sakin sakin konuşmaya devam et. |
| I used to think the Army was coming, and then I stopped thinking | Eskiden ordu gelecek sanıyordum, sonra sanmayı bıraktım. | Başlarda askerler gelip bizi kurtaracak sanıyordum. Ne safmışım ama... |
| Hi, I wanted to say, folks like you are why I keep going | Selam, şunu söylemek istedim, senin gibiler yüzünden devam ediyorum. | Biliyor musun, senin gibi insanlar olmasa çoktan pes etmiştim. İyi ki varsın. |
| Everybody's napping, the dead and the living, it's that kind of afternoon | Herkes uyukluyor, ölüler de diriler de, öyle bir öğleden sonra. | Bugün de öyle bir rehavet çökmüş ki. Ölü de diri de uyukluyor. |
| One moment, one moment, I'm reloading | Bir dakika, bir dakika, dolduruyorum. | Dur biraz! Silahı doldurmam lazım! |
| Stupid- I should've counted, I should've COUNTED! | Aptal- saymam lazımdı, SAYMAM lazımdı! | Salak kafam! Mermileri saymalıydım! SAYMALIYDIM! |
| Thank you, Lord, for one more sunrise, and one more sunset | Bir gün doğumu daha, bir gün batımı daha için şükürler olsun Rabbim. | Şükürler olsun Rabbim. Bir gün daha doğan güneşi gördük. İnşallah batışını da görürüz. |
| Please don't be a bad person, I can't handle another bad person! | Lütfen kötü biri olma, bir kötü insanı daha kaldıramam! | Ne olur, sen de kötü biri çıkma! Valla mecalim kalmadı. |
| Let me ask the one that matters, has your skin been broke this week? | Önemli olanı sorayım - bu hafta derin hiç yarıldı mı? | Günün altın sorusu geliyor - Son zamanlarda bir yerini kesip biçmedin, değil mi? |
| Stay out of range, I'm warning you | Menzilimin dışında kal, uyarıyorum. | Yaklaşma! Vurabileceğim mesafeye girme, uyarıyorum! |
| Please, please let it be loaded this time | Lütfen, lütfen bu sefer dolsun. | Hadi dol artık. |
| Click, click, it's empty, it's empty! | Klik - klik - boş - boş! | Tık... Tık... Boş! Silah boş! |
| It's too quiet, it's too quiet, but I'll take it | Fazla sessiz, fazla sessiz, ama kabulüm. | Ortalık fazla sessiz... Hem de fazlasıyla. Ama şikayetçi değilim. |
| Um, hi, hello, is it safe to talk? I think it's safe, hi | Şey, selam, merhaba, konuşmak güvenli mi? Bence güvenli, selam. | Şey... selam! Konuşsak başımıza iş açılmaz, değil mi? Sanmam ya... Neyse, merhaba. |

## Ses

- **Sivil, aile, işçi:** gündelik, insani; abi, abla, kardeş, canım, evladım (yaşlı). İşçi işinin diliyle (mesai, ustabaşı, vardiya).
- **Kurtarma, sağlık:** işini bilen, duruma göre sakin ya da sert. Papaz: Rabbim, evladım.
- **Polis, şerif, SWAT:** kısa, mesafeli, emre yakın. Asker: kısa, kuru, rapor dili ("Temas!", "Anlaşıldı.", "Emret komutanım!").
- **Haydut, çete, kaçak:** kaba, az sözlü, tehdidi sakin söyler; lan, ulan, koçum.
- **Girdi etiketleri bağlam bilgisidir; çevrilmez ve çıktıya yazılmaz.** İngilizce repliğin yanında `N | etiketler | İngilizce` biçiminde görünürler.
  - `reg`: Bu repliği kullanabilecek NPC sınıfı (sivil, aile, işçi, kurtarma, kolluk, asker, haydut vb.). Birden çok değer alternatif sınıflardır.
  - `faction`: Repliğin kullanılabildiği fraksiyon kimlikleri. Bunlar oyunun iç etiketleridir; konuşanın kesin kimliği veya çevrilecek özel adlar olarak yorumlama. Birden çok değer alternatif fraksiyonlardır.
  - `role`: Konuşanın daha özel arketipi/rolü (`rescue_clergy`, `law_sheriff`, `family_elder` gibi). Birden çok değer alternatif rollerdir.
  - `tmp`: Konuşmacı profilinin deneyim/mizaç sınıfı: `fresh` = deneyimsiz/yeni, `seasoned` = deneyimli, `veteran` = kıdemli, `predator` = haydut/çete gibi saldırgan profil. Bunları her repliğe aynı sözcükleri ekleme talimatı sayma.
  - `mood`: Repliğin anlık duygusu (`fear`, `sad`, `grim`, `warm`, `funny`, `angry`, `calm` gibi).
  - `st`: NPC'nin oyuncuya karşı tutumu (`friendly`, `neutral`, `careful`, `hostile`). Duygu (`mood`) ya da itibar (`rep`) ile aynı şey değildir.
  - `rep`: Oyuncunun NPC/fraksiyon nezdindeki itibar kademesi. `worst` gibi bir değerden tek başına korku veya belirli bir duygu çıkarma.
  - `sex`: Konuşan NPC'nin cinsiyeti; `psex`: oyuncu karakterinin cinsiyeti.
  - `fact`: Oyun durum bayrağı (`player_armed`, `recent_zombie_contact` gibi); koşulu açıklar, repliğe eklenecek içerik değildir.
  - `wp`: NPC'nin silah durumu/türü (`gun`, `melee`, `none`); tehdit veya çatışma repliğinin bağlamını belirler.
  - `grp`: NPC'nin grup bağlamı (`solo`, `squad` gibi); kime seslenildiğini anlamaya yardım eder.
  - `cb`: Çatışma durumu (`hot`, `calm` gibi); yalnızca mevcut durum ipucudur.
  - `wd`: Yaralanma durumu (`hurt` gibi); repliğin bağlamını açıklar, kaynakta olmayan yaralanma ayrıntısı ekletmez.
  - `day`, `hour`: Repliğin kullanılabildiği oyun günü/saat aralığıdır. `world`: yol, bina, kapı gibi mevcut çevre koşuludur. Bunları yalnızca sahne ipucu olarak kullan.
  - Sahne başlığındaki `r1/r2/r3`, sırasıyla K1/K2/K3 konuşmacısının rolünü; `x1=f/m`, K1'in cinsiyetini belirtir. Sahne kimliği ve diğer başlık alanları da bağlam içindir.
  - Koşul etiketleri cümleye yeni bilgi ekleme izni vermez. Anlamı açıklanmayan bir etiket varsa onu çevirmeden bırak; kaynağın söylemediği olayı, ilişkiyi veya ayrıntıyı varsayma.
- Panik ya da tereddüt anlatan tekrar, duraksama (...), kekeleme ve BÜYÜK HARFLİ vurgu korunur, ama Türkçenin vurgusuyla.
- **Küfür:** o kişi o an ne derse (hay aksi, lan, siktir, Allah kahretsin...); kaynağın gücünün altına inme; panikte bir kademe ağırı serbest; kibar yaşlı ve papaz ağır küfretmez. **İnanç:** Allah'ım, Yarabbi, çok şükür, Allah'a emanet ol, inşallah serbest ve tercih edilir.

## Sahne dosyaları (dosya adı `SN` ile başlıyorsa veya girdide `##### SAHNE` blokları varsa)

```
##### SAHNE sahne_kimligi · konu · 2 kişi · koşullar #####
1 | K1 | satır
2 | K2 | satır
  · K2 | bağlam satırı
```

- Bir sahne, iki (bazen 3-4) NPC'nin **birbirine** yaptığı tek bir konuşmadır; satırlar sırayla söylenir, oyuncu kenardan duyar. K1, K2, K3 aynı sahnede hep aynı kişidir.
- Sahneyi **baştan sona oku, sonra yaz**: her satır öncekinin cevabı ya da devamıdır. Göndermeler ("o", "bu", "ya sen?"), soru-cevap ritmi ve her kişinin sesi sahne boyunca tutarlı kalsın. Serbestlik sahnenin içinde de geçerli: cümleyi bölebilir, birleştirebilir, Türkçe tepki sözü ekleyebilirsin; ama başka konuşmacıya ait vuruşu, esprinin ya da cevabın yerini taşıma, sonraki satırın söyleyeceğini önceden söyleme.
- Koşullar: `r1/r2/r3` K1/K2/K3'ün rolü, `x1=f` ya da `x1=m` K1'in cinsiyeti, `mood`, `day`, `hour`, `world`, `faction`. Sahne kimliği (`king_scene_apology` gibi) konunun ipucudur. Başlıktaki diğer alanlar da metadata'dır; anlamı açıklanmıyorsa onlardan yeni bilgi çıkarma.
- **Hitap:** iki kişi birbirine "sen" der. Üç ve daha çok kişilik sahnede bir kişiye "sen", gruba (`everyone`, `you guys`, `folks`) çoğul; bunlar için `## not: gerçek çoğul` gerekmez.
- Başında `  · ` olan satırlar **bağlam**dır, numarası yoktur, çevrilmez ve çıktıya yazılmaz. `→` işaretinden sonrası onaylanmış Türkçedir; adları ve üslubu ona uydur.
- Çıktıda `K1`, `K2` etiketini yazma.

## Öteki dosya türleri

### Yeniden çeviri (dosya adı `G` ile başlar)

Satırlar oyunda eski bir çeviriyle duruyor; sıfırdan, İngilizceden yaz. `MEVCUT:` satırları varsa onlar eski Türkçedir, çıktıya yazma.

### Konuşma ağaçları, havuzlar ve öteki özel dosyalar

Dosyanın başındaki açıklama etiketleri anlatır (AĞAÇ, HAVUZ, OYUNCU SORUSU, OYUNCU SEÇENEĞİ, NPC 1/2, ESİR, TELSİZ, NOT, ANLATI...) ve bu dosya için önceliklidir. Her AĞAÇ bloğu tek bir konuşmadır: baştan sona oku, hangi düğmenin hangi cevaba gittiğini izle; cevap düğmeye otursun. `·` ile başlayan bağlam satırlarını çıktıya yazma.

### Arayüz dosyaları (Y10–Y15 ya da başında "ARAYÜZ DOSYASI" kuralları olan dosya)

Bunlar konuşma değil **ekran metni**: düğme, ayar, ipucu, bildirim, etiket. Bu skill'in serbestlik, ses ve küfür bölümleri bu dosyalarda **geçerli değildir**; dosya başındaki kurallar önceliklidir. Geçerli olanlar: Terimler, "siz" ve "-dır" yok, yer tutucuları koruma, çıktı biçimi.

- Kısa, net, tutarlı. Etiketlerde emir ya da isim biçimi (Kaydet, Teçhizat); ipucunda gerekirse "sen". Sonda nokta İngilizcedeki gibi.
- Dosya başındaki **TERİMLER** listesi bağlayıcıdır: aynı İngilizce terim her yerde aynı Türkçe.
- Her başlığın altındaki **EKRAN:** metnin hangi ekranda göründüğünü söyler. Etiket sütunu (ui, tip, label…) çıktıya yazılmaz.
- `{yer_tutucu}`, `%%`, `%1`, `\n`, `<...>`, renk kodları, kısaltmalar (HP, NPC, GM, MHz) ve özel adlar aynen. BÜYÜK HARFLİ etiket büyük harfli kalır.
- Türkçe İngilizceden belirgin uzun olmasın; düğmelerde en fazla yaklaşık 1,3 katı. Oyuncunun ekranda görmeye alışık olduğu arayüz Türkçesi.

## Biçim kuralları (bağlayıcı)

1. **Hitap "sen".** Kaynakta gerçek çoğul alıcı varsa (you all, you two, folks, everyone, guys, y'all) çoğul yaz ve satır sonuna `## not: gerçek çoğul` ekle.
2. **Şapkalı harf yok** (hala, bela, hikaye). Türkçe harfleri doğru yaz.
3. **Noktalama:** NPC'nin her satırı cümle sonu noktalamasıyla biter (. ! ? ...), kaynak noktasız bitse de.
4. **Özel adlar** (kişi, yer, grup: Louisville, Muldraugh, Outlaws MC) çevrilmez.
5. **Birimler** metriğe: feet → metre, mile → kilometre, lb → kilo, °F → °C; satır sonuna `## not: 10 feet -> 3 m`.
6. **Süslü parantezli parçalar** (`{name}`, `{he}`, `{g:abi|abla}`, `{badat}` gibi) dosyada varsa **önce `YER_TUTUCULAR.md`'yi oku** (bu skill'in ek dosyası) ve ona uy; dosya başındaki kural ondan önce gelir. Kısaca: parçayı aynen bırak, ek bağlama; `{he}/{him}/{sir}/{mister}` Türkçe satırda kalmaz.
7. **Terimler:** squad = tim · crew = ekip · base = üs · outpost = karakol · safehouse = güvenli ev · loot = ganimet · raider = yağmacı · raid = baskın · infected = enfekte · horde = sürü · checkpoint = kontrol noktası · walkie / radio = telsiz · Sheriff = Şerif · Deputy = Şerif Yardımcısı · Officer = Memur (hitapta "memur bey") · Sergeant = Çavuş.

## Çıktı

- Her satır tek satır: `N | Türkçe`. N girdideki numara; hiçbirini atlama, birleştirme, bölme. Sıra girdidekiyle aynı.
- Etiket, İngilizce, başlık, açıklama yazma. Replikte `|` kullanma (`{g:..|..}` içi hariç).
- Hepsini tek kod bloğunda ver; kod bloğunun dışına yalnızca en sonda `Son numara: N` yaz.
- Yarıda kesilirsen "devam et" denince kaldığın numaradan sürdür.

## Bakım notu

K56 (2026-11-12): bu skill A/B/C denemesinde kazanan B sürümüdür (kısa, frensiz, "İngilizce iskelet" kuralı, çıta tablosu). Eski uzun sürüm git geçmişinde. Çıta tablosuna yalnızca kullanıcının yeniden yazdığı satırlar girer (anlamı kaydıranlar hariç), 25'i geçmesin. Yer tutucu kuralları `YER_TUTUCULAR.md`'de; buraya geri taşıma.
