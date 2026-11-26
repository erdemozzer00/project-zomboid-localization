# Project A-Life — Türkçe diyalog yerelleştirme rehberi

Bu yerel rehber, İngilizce girdi için hangi sahne bilgisinin gerekli olduğunu ve Erdem'in istediği rötuşlarda korunacak Türkçe üslubu tarif eder. Çeviri ayrı ortamda Fable'da yapılır. Bir repliğin bağlamı gerekirken o bilgiyi doğrudan TXT'ye yaz.

## Girdide sahne bağlamı

Kaynakta konuşanın kim olduğunu, kime seslendiğini ve repliğin nerede duyulduğunu doğrula. Oyuncu bir NPC konuşmasını kenardan duyuyorsa bunu TXT'de belirt. Konuşma ağacında seçeneği ve ona bağlı cevabı birlikte göster. Rolü, ruh halini, ilişkileri ve koşulları yalnızca kaynak desteklediği ölçüde ekle.

## Rötuşta anlam ve doğallık

- Repliğin yaptığı işi koru. Örneğin konuşan konuyu kapatıyorsa “forget it” yerine sahnesine göre “boş ver” veya “neyse” doğal duyulur. Cümleyi karakterin ağzından sesli okunuyormuş gibi dinle.
- İsim, yer, sayı, nesne, eylem ve oyundaki ilişki kaynağa sadık kalır. Ölçü birimi yerelleştirilecekse dosya içindeki kuralı açık yaz.
- Gerçek grup hitabını koru. Denetim aracı doğru çoğulu işaretlerse `onayli_uslup_istisnalari` kaydına gerekçeyi ekle.

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

Küfrün ve argonun gücünü kaynağa göre ayarla. A-Life repliklerinde karakterin sesine uyuyorsa Fable panik anında küfrü bir kademe ağırlaştırabilir. Kullanıcının kendi düzeltmelerindeki seçimler (ör. “Tanrım”, “Kahretsin”, “uğursuzluk getirirsin”) aynen kalır.

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

Erdem'in daha önce onayladığı Türkçe kendi seçtiği biçimde korunur. Rötuşları Erdem'in belirttiği satırlara ve kapsama uygula.
