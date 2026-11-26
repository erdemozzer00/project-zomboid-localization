# Oluşturucu ve Dünya Durumu · ekran görüntüsü takibi

Fable'dan gelen 57 satır [teknik kontrolden](../paketler/AL_SS_UI.md) geçti. Satır numaraları, yer tutucuların yazımı ve tekrar sayısı, sabit yüzdeler ve `/10` değerleri tam. [Anahtar haritası](../paketler/haritalar/AL_SS_UI_harita.json) tek `IG_UI_lua` paketine yöneliyor.

| Görsel | Uygulama |
|---|---|
| 1 · Ganimet | `buildCombatPage` içindeki silah düşürme ve iki kondisyon listesi Türkçe etiketli kopyayla oluşturuluyor. Sayısal değerler, seçenek kimlikleri ve sıra korunuyor. |
| 2 · İlişkiler | Açılır listedeki ve üst satırdaki tutum `relationLabel` üzerinden yerelleştiriliyor. `relationWhy` bilinen ittifak kodlarını sunumda çeviriyor. Bilinmeyen kodlar ve seçim değerleri korunuyor. |
| 3 · Klasör ipucu | Klasör kartının `addTooltip` çağrısı, Fable kalıbını sözlükteki klasör adıyla veya özgün adla dolduruyor. |
| 4 · Görünüm | **Far** ve **KIYAFET TAKIMLARI** ölçümden önce mevcut sözlükten alınıyor. Yeşil rozet, başlığın ölçülen sonu ile **ÇÖZÜM ÖNER** düğmesi arasına sığıyor. Dışarıdan çağrılan `Creator.fitText`, çok baytlı metni UTF-8 karakter sınırlarında kesiyor. Mevsim sekmeleri ve uygunluk rozeti kendi çeviri anahtarlarına bağlandı. |
| 5–6 · NPC üstü | Jeem `IGUI_ALJ_Intent_AttackingYou` ve `IGUI_ALJ_Moodle_Stressed` kendi paketinde kontrol edilecek. |
| 7 · Dünya Durumu | `ALifeStatusWindow.statusRows` dönüşünde ana gövde `self.status` alanlarıyla ve Fable kalıplarıyla dolduruluyor. Başlık ve satır sırası, isteğe bağlı nüfus ayarı ve ret gerekçesi, çok oyunculu veriler, sayaçlar ve renkler korunuyor. Fraksiyon sayımı bilinen adları yerelleştiriyor. Ayrıntılı tanılama ve bilinmeyen sunucu durumları mevcut gösterimden geliyor. |

**Onaylanan rötuşlar.** 21. satırdaki `Chinstrap` için **Çene şeridi**, 22. satırdaki **Hepsi** için **Tüm yıl** işlendi. Kısa sekme etiketi ve Dünya Durumu'nun tek sözcüklü durumları yalnız kendi ekranlarında aranan anahtarlara bağlandı.

Yerleşim ve istemci sunum bağlantıları yerel Workshop paketine aktarıldı. Ganimet seçenekleri ve ilişki değerleriyle Dünya Durumu satırları kurulu Lua modülleriyle sınandı. Dünya Durumu ana gövdesinin 22 satırı, Fable çıktısındaki gerçek Türkçeyle bellekte çalıştırıldı. Gerçek klasörde 57 çeviri ve 14 dosya doğrulandı. Dar ve geniş Oluşturucu düzeninin canlı oyun kontrolü bekliyor.
