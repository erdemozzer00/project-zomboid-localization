# Project A-Life — Türkçe diyalog yerelleştirme rehberi

Bu rehber Project A-Life diyaloglarını doğal, yaşayan Türkçeyle yazmak içindir. Türk oyuncunun duyacağı bir replik gibi yaz; İngilizce cümle düzenini Türkçeye taşımaya çalışma. Kaynağın anlamını ve sahnedeki bilgileri koru.

## Her satırdan önce zorunlu süreç (K36)

Diyalog çevirirken bu adımlar atlanmaz. Kullanıcı bunu defalarca söyledi: **birebir çeviri yapma; kendini o cümleyi bir sahnede söylüyormuş gibi düşün ve Türkçeyi yerelleştir. "Hiçbir Türk böyle konuşmaz" diyorsan o çeviriyi düzelt.**

1. **Kim, kime, neden söylüyor?** Bağlam başlığını, olay adını (ör. PASSING_NPC_GREET) ve koşulları oku. Dinleyen kim? Bazı olaylarda NPC başka bir NPC'ye ya da gruba konuşur, oyuncu yalnızca kenardan duyar; bazılarında doğrudan oyuncuya. Hitap (sen/siz, tekil/çoğul) buradan çıkar. Emin değilsen oyun kaynağındaki çağrı yerine bak.
2. **Sahneyi canlandır.** O karakter, o ruh halinde, o hava ve saatte, o niyetle bunu söylese bir Türk ne derdi? Önce o cümleyi kur, sonra kaynakla karşılaştır.
3. **Kalıbı değil işi çevir.** İngilizce deyim ve kalıbın yaptığı iş neyse (alay, rahatlatma, geri çekilme, şaka, uyarı) Türkçede o işi gören sözü bul: "forget it" → "boş ver / neyse", "take a load off" → "otur, dinlen", "I'd marry anyone with a percolator" → "demliği olanla evlenirim". Kelime sırasını ve "A, B, C" virgül zincirini İngilizce'den taşıma.
4. **Sesli oku, Türk testi.** Cümle konuşulur mu, kulağa çeviri gibi geliyor mu? "Düz yüzle", "tutunulacak komik bir şey", "unut gitsin", "hoş geldi" (yanlış kuruluş) gibi kalıplar bu testte kalır. Kontrol aracının geçmesi doğruluk kanıtı değildir.
5. **Araç Türkçeyi yönlendirmez.** Kontrol aracı bir uyarı verdi diye doğru çoğul hitabı tekile çevirme ya da cümleyi bozma. Gerçek çoğulsa çoğul yaz ve satıra `onayli_uslup_istisnalari` ile gerekçe ekle; araç yanlış uyarıyorsa aracı düzelt.
6. **Parça parça yaz.** Yaklaşık 100 satırlık bölümlerle ilerle, her bölümü yazdıktan sonra bu 4 adıma göre yeniden oku. Yüzlerce satırı tek seferde yazma.
7. **Kaynak bilgisi korunur.** İsim, yer, sayı, nesne, eylem aynı kalır; yeni olay, ilişki ya da ayrıntı eklenmez. Ölçü birimleri (feet, lb, °F) Türk oyuncuya göre çevrilir ve satır notunda belirtilir.

Birebir ve sahneli çeviri örnekleri (D6a, kullanıcının 20. satır itirazı sonrası):

| Kaynak | Birebir (yanlış) | Sahneli (doğru yön) |
|---|---|---|
| You hear that earlier? Never mind, nothing, forget it | Az önce duydun mu? Boş ver, bir şey değil, unut gitsin | Az önce bir ses duydun mu? Yok yok, boş ver... bir şey değildir. |
| Hot enough? Sorry, I always wanted to say that | Yeterince sıcak mı? Kusura bakma, hep bunu demek istemiştim | Sıcak bastırdı değil mi? Pardon, bunu söylemek için can atıyordum. |
| Rise and shine, ha, I never could say that with a straight face | Uyan da parla, ha, bunu hiç düz yüzle söyleyemedim | Hadi kalk, gün aydı! Hıh, bunu hiç gülmeden diyemedim. |
| Hell of a quitting time, huh? | Paydos saati de ne saatmiş, ha? | Paydos da ne paydosmuş, ha? |
| Same shift, different dead guy | Aynı vardiya, farklı ölü | Vardiya aynı, ölü başka. |

## Sahneyi kur, sonra yaz

Her repliği önce bir sahne olarak düşün. Kaynağın ne söylediğini ve ne istediğini belirle. Bağlam dosyasındaki rolü, ruh halini, oyuncuyla ilişkisini, zamanı ve çevre koşullarını oku. Karakteri bu sahnede hayal et. Sonra onun ağzından Türkçe yaz ve repliği sesli okunuyormuş gibi yeniden kontrol et.

**Kaynak anlamı → karakter ve ruh hali → bağlamla sınırlı sahne → doğal Türkçe → son kontrol.**

Sahneyi hayal etmek, kaynağa yeni olay, geçmiş, ilişki veya ayrıntı eklemek değildir. Adları, yerleri, tarihleri, nesneleri ve eylemleri koru. Bir deyim tonu taşıyabilir; kaynak bilgisini değiştiremez.

## Replikte ses ve ritim

- Her NPC aynı kişi gibi konuşmaz. Yaş, deneyim, meslek, aile ilişkisi, korku ve öfke tonu değiştirir. Acemi asker telaşla sorabilir; deneyimli biri kısa ve kuru konuşabilir; ebeveyn çocuğunu koruyabilir; sağlık görevlisi duruma göre sakin ya da sert olabilir.
- Kısa ve gerçekçi yaz. Kaynakta anlamı olan bir ayrıntıyı sırf replik kısalsın diye atma.
- Gereksiz “ben”, “işte”, “gerçekten” ve benzeri sözcükleri ekleme. Konuşanın vurgusu, karşıtlığı veya ritmi için gerekiyorsa kullan.
- Tekrar, duraksama, kekeleme ve büyük harf her zaman hata değildir. Panik, yaralanma, tereddüt veya vurgu anlatıyorsa koru; Türkçede doğal duracak biçimde düzenle.
- Türkçe deyim, gündelik söz ve küçük şaka sahneye uyduğunda işe yarar. Her satıra argo, espri veya ağır drama ekleme.
- NPC oyuncuya sesleniyorsa “sen” kullan. Replik açıkça bir gruba sesleniyorsa çoğul hitabı koru ve paket notunda gerekçelendir.
- Yeni Türkçe çeviri metinlerinde şapkalı harf kullanma.
- Dua, kilise ve inanç sözlerini karakterin kimliğine ve oyunun dünyasına göre çevir. Bilinen dua metinlerini sırf üslup için yeniden yazma. Yer adlarını ve özel adları sözlüğe göre koru.

## Kültürel bağlam, inanç ve küfür (K35)

Karakterler 1993 Kentucky'sinde yaşayan Hristiyan Amerikalılardır, ama oyuncu Türkçe duyar. Kullanıcı kararı: Türkçede doğal duyulan, dine özgü kalıplar **serbesttir ve tercih edilir**. “Allah'ım”, “Aman Allah'ım”, “Yarabbi”, “inşallah”, “vallahi”, “Allah'a emanet ol”, “Allah razı olsun”, “Allah korusun” gibi sözleri kaynak ve sahne istediğinde kullan. “Tanrım” de olur; zorunlu değil, yasak da değil. Din adamı (papaz) konuşuyorsa “Rabbim / Rab” ve kilise dili (Göklerdeki Babamız, Selam sana Meryem, Mezmur) korunur. Her “God” sözcüğü otomatik aynı karşılığa çevrilmez; ünlemse ünlem, duaysa dua, deyimse Türkçede aynı işi gören söz seçilir.

Küfrün ve argonun gücünü kaynağa göre ayarla; karakteri kaynaktan daha kaba yapma. Kullanıcının kendi düzeltmelerindeki seçimler (ör. “Tanrım”, “Kahretsin”, “uğursuzluk getirirsin”) aynen kalır.

| Kaynak | Uygun Türkçe örneği | Neden |
|---|---|---|
| “Oh my God” | “Aman Allah'ım!” (ya da “Tanrım!”) | Ünlem; sahnenin tonuna göre seçilir. |
| “Thank God” | “Çok şükür.” / “Allah'a şükür.” | Doğal Türkçe kalıp. |
| “Go with God” | “Allah'a emanet ol.” | Veda kalıbı. |
| “Honest to God” | “Allah şahidim olsun.” / “Yemin ederim.” | Vurgu işlevi korunur. |
| “Shit!” | “Kahretsin!” / daha ağır kaynakta daha güçlü | Kaynağın gücü korunur. |

## Kullanıcının düzeltmelerinden örnekler

Bu örnekler birer kalıp değildir. Bir repliğin amacı, sahnesi ve karakteri Türkçe seçimini belirler.

| Kaynak | Kullanıcının Türkçesi | Gösterdiği tercih |
|---|---|---|
| “Oh, it’s you! I’m so glad, come, sit, tell me everything.” | “Aa, sensin! Seni gördüğüme sevindim. Gel, otur da dökül bakalım, neler var neler yok?” | “Tell me everything” için Türkçede söylenen sıcak ifade seçiliyor. |
| “I go to school in Rosewood — went, I guess I went.” | “Ben Rosewood’da okuyorum. Yani... okuyordum. Artık öyle demek lazım galiba.” | Salgın sonrası değişen zamanı duraksamayla hissettiriyor. |
| “It’s mostly water.” | “Çorba demeye bin şahit ister zaten.” | Hafif mizah, aynı yemek bilgisi ve yakınma içinde kalıyor. |
| “My shift’s over, but nobody told the dead.” | “Benim mesai bitti de şu ölülere söyleyen olmamış galiba.” | Meslek ve zombi tehdidi kısa bir kara mizaha bağlanıyor. |
| “My favorite survivor.” | “Ooo, kimleri görüyorum! Bizim buraların gözdesi gelmiş!” | Yapay “favori hayatta kalanım” yerine oyuncuya hitap eden karşılama geliyor. |
| “Haven’t talked to anyone in four days, so, if I ramble, sorry.” | “Dört gündür kimseyle iki laf etmedim. Çenem düşerse kusura bakma.” | Uzun süredir yalnız kalmış karakterin sesi ve Türkçe gündelik ifade korunuyor. |
| “Keep your eyes up. I’m reloading.” | “Gözünü dört aç! Ben silahı dolduruyorum!” | “Dikkat et” yerine sahnedeki tehdide uygun uyarı seçiliyor. |
| “Changing mags, cover.” | “Şarjör değiştiriyorum, arkamı kolla!” | Savaş sırasında duyulacak kısa ve işlevli emir kuruluyor. |

## Kullanıcının sahne örneği

“I’m not okay, but I don’t want to talk about it.” cümlesi her durumda “İyi değilim ama bunun hakkında konuşmak istemiyorum.” diye kalmak zorunda değil. Yorgun bir karakter merdivene çökmüşse “İyi değilim... Ama boş ver, konuşacak halim yok.” denebilir. Bu seçim yorgunluğu Türkçe ritimle verir; yeni bir olay eklemez.

“You look terrible.” için de karaktere ve ana göre “Üzerinden tır geçmiş gibisin.” denebilir. Deyim, yüzün kötü göründüğü bilgisini korur ve Türkçede doğal duyulur.

## Kapsam ve kayıt

Kullanıcının yaptığı 603 diyalog düzeltmesi kendi seçtiği metin olarak kalır. K2a paketi bunlara dokunmadan, daha önce çevrilmiş 400 başka diyalog satırını Codex imzasıyla kaydeder. Paket bu 400 değişikliği ve gerekçelerini gösterir; kullanıcı ayrıca en iyi 20 örneği inceler. Bu örnekler kalan satırlar için otomatik onay sayılmaz.
