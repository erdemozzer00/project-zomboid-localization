# A-Life Lokalizasyon

## İçindekiler
- `site/`: yayınlanacak statik site (`index.html`, `stil.css`, `uygulama.js`, `config.js`, `veri/`).
- `arac/katalog_uret.py`: kataloğu repodan üretir.
- `supabase.sql`: ortak havuz ve profil tabloları.

## Katalog ve GitHub Pages yayını
Onaylı Türkçe, İngilizce kaynak, sahne bağlamı, paket haritası veya site dosyaları main dalına gönderilince GitHub Actions kataloğu yeniden üretir ve yayınlar. Yerel çeviriler yayına girmek için onayli/ dosyalarıyla birlikte commit edilip gönderilir.

[Actions](https://github.com/erdemozzer00/project-zomboid-localization/actions/workflows/publish-pages.yml) üzerinden son dağıtımı kontrol et veya iş akışını elle çalıştır. [Canlı sitedeki](https://erdemozzer00.github.io/project-zomboid-localization/) katalog sürümünün ilk bölümü kaynak commit'i gösterir.

Yerel önizleme için depo kökünden çalıştır:

    python ceviri-masasi/arac/katalog_uret.py --repo . --cikti ceviri-masasi/site/veri

Araç belirtilen katalog dizinini yeniden oluşturur. Üretilen site/veri/ dizini Git'e eklenmez.

## Girişli ortak havuz (Supabase)
Google Auth Platform üzerinde Web application türünde bir OAuth istemcisi oluştur. Yetkili yönlendirme URI’si olarak `https://vxieysispctubjhiwiej.supabase.co/auth/v1/callback` kullan. Supabase Authentication ayarlarında Google sağlayıcısını etkinleştir ve istemci kimliği ile gizli anahtarı oraya kaydet. Yeni kullanıcıların kayıt olmasına izin ver. URL Configuration içinde Site URL olarak yayın adresini ayarla. Yerel deneme için kullanılan tam adresi de Redirect URLs listesine ekle.

Çevirmen ilk girişte görünen adını yazar. Öneriler giriş yapan hesabın kimliğiyle kaydedilir.
Giriş yapmayan kimse havuzu okuyamaz ya da yazamaz; kimse öneri silemez ya da değiştiremez.

## Yerel mod
`config.js` boşken site giriş istemez ve önerileri yalnızca o tarayıcıda saklar. Denemek için:
    cd site && python -m http.server 8000

## İndirilen JSON
`bicim: ceviri-masasi/oneriler@2`. Her öneride `hedef`, `anahtar`, `katalog_surumu`, `en`, `gorulen_tr`,
`onerilen_tr`, `gerekce`, `yazar {id, ad}`, `olusturma`, `ayni_satira_oneri_sayisi` ve `baglam` bulunur.
