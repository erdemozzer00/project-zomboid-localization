"""Bir paketi (paketler/<kod>.json) otomatik kontrol eder ve okunur .md üretir.

Kullanim: python araclar/paket_kontrol.py S1
Kontroller: anahtar yeni EN'de var mı · yer tutucu / %% / \\n uyumu · şapkalı harf · ayraç · baş-son boşluk ·
"siz" hitabı (K7) · "-dır/-mektedir" (K5) · sözlükte yasaklı karşılıklar.
RadioData diyaloglarında satır sonu noktalaması, satır başlangıcı tekrarı ve seçili kalıp taraması uyarı olarak raporlanır.
K düzeltme paketlerinde gerekçeli kullanıcı onayı, hitap ve "-dır" uyarısını kaldırabilir.
Anahtar, yer tutucu ve boşluk kontrolleri bu onaydan etkilenmez.
"""
import json, re, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
YT = re.compile(r'\{[A-Za-z]+\}|%%|\n|<[A-Za-z]+[^>]*>')
CINS = re.compile(r'\{(he|him|his|hers|himself|sir|mister|v:[A-Za-z]+)\}', re.I)  # v: DoLines zamirleri (K46), Türkçede kalkar
G = re.compile(r'\{g:([^{}]*)\}')
SIZ = re.compile(r"\b(siz|sizi|size|sizin|sizce)\b|[a-zçğıöşü]{2,}(ınız|iniz|unuz|ünüz|yınız|yiniz|yunuz|yünüz|sınız|siniz|sunuz|sünüz)\b", re.I)
DIR = re.compile(r"([aeıioöuü']d[ıiuü]r|[pçtkshşf]t[ıiuü]r)[.!]?$|mektedir|maktadır")
# Ettirgen emir kipleri "-dır" eki değil (ör. "oluştur", "çalıştır", "paylaştır", "birleştir"); "prosedür" kök
EMIR = re.compile(r"(oluştur|sustur|çalıştır|değiştir|ulaştır|yaklaştır|karıştır|yetiştir|alıştır|yapıştır|iyileştir|yerleştir|geliştir|eriştir|attır|bıraktır|ettir|bastır|siktir|l[ae]şt[ıi]r|prosedür)[.!]?$", re.I)
# Sözlük kararlarına aykırı karşılıklar (SOZLUK.md B)
YASAK = {
    r'\bdoğur(?!ur\b|mak\b|du\b|duk|acak|ttu|tuk|tum)': 'spawn → oluştur / ortaya çıkma / doğma noktası',
    r'(?<!\w\s)(Düzenleyici|DÜZENLEYİCİ)': 'Creator → Oluşturucu',
    r'\btayfası\b(?!.*\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ Tayfası)': 'crew → ekip (çete adı değilse)',
    r'güvenli evin? (?=.*shelter)': 'shelter → sığınak',
}
SAPKALI = re.compile(r'[âîûÂÎÛ]')
SATIR_SONU = re.compile(r"[.!?…][\"'”’»)\]}]*$")
ILK_KELIME = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ]+(?:['’][A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ]+)?")
DUBLAJ_KALIPLARI = {
    'Hadi ama': re.compile(r'\bhadi\s+ama\b', re.I),
    'Sorun değil': re.compile(r'\bsorun\s+değil\b', re.I),
    'dostum': re.compile(r'\bdostum\b', re.I),
}


def load(p):
    s = p.read_text(encoding='utf-8').strip()
    if not s.startswith('{'):
        s = '{' + s.rstrip().rstrip(',') + '\n}'
    return json.loads(s)


def main(kod):
    paket = json.loads((KOK / 'paketler' / f'{kod}.json').read_text(encoding='utf-8'))
    dosya = paket['_dosya']
    if paket.get('_duzeltme'):  # K paketleri (araclar/duzeltme_al.py): "eski" = şu anki onaylı çeviri
        yeni = load(KOK / ('kaynak' if dosya.endswith('_lua') else 'kaynak/en') / f'{dosya}.json')
        eskiTR = load(KOK / 'onayli' / f'{dosya}.json')
        if dosya.endswith('_lua'):
            yerler = json.loads((KOK / 'kaynak' / f'{dosya}_baglam.json').read_text(encoding='utf-8'))
            baglam = {k: {'secenek': {'kod': ', '.join(v[:2])}} for k, v in yerler.items()}
        else:
            baglam = json.loads((KOK / 'rapor' / 'baglam.json').read_text(encoding='utf-8')).get(dosya, {})
        return kontrol(kod, paket, yeni, dict(yeni), eskiTR, {}, baglam)
    if dosya.endswith('_lua'):  # Lua'dan çıkarılan metinler (araclar/lua_cikar.py): eski çeviri / çevirmen yok
        yeni = load(KOK / 'kaynak' / f'{dosya}.json')
        eskiEN, eskiTR = {}, {}
        # Çevirmen diyalogları (araclar/diyalog_cevirmen.py al): çevirmenin ilk hali pakette saklı
        cev = {k: (r['cevirmen'], r['cevirmen_tr']) for k, r in paket['satirlar'].items() if r.get('cevirmen')}
        yerler = json.loads((KOK / 'kaynak' / f'{dosya}_baglam.json').read_text(encoding='utf-8'))
        baglam = {k: {'secenek': {'kod': ', '.join(v[:2])}} for k, v in yerler.items()}
        return kontrol(kod, paket, yeni, eskiEN, eskiTR, cev, baglam)
    yeni = load(KOK / 'kaynak' / 'en' / f'{dosya}.json')
    if not (KOK / f'{dosya}-updated.json').exists():  # ItemName (K46): modun eski çevirisi/çevirmeni yok
        return kontrol(kod, paket, yeni, {}, {}, {}, {})
    eskiEN = load(KOK / f'{dosya}-updated.json')
    eskiTR = load(KOK / f'{dosya}-updated-translated.json')
    cev = {}
    for d in ((KOK / 'çevirmenler').iterdir() if (KOK / 'çevirmenler').exists() else ()):  # çevirmen dönemi bitti (2026-11-13)
        for f in d.iterdir():
            if f.name == "NOTLAR.txt": continue
            for k, v in load(f).items():
                cev[k] = (d.name, v)
    baglam = json.loads((KOK / 'rapor' / 'baglam.json').read_text(encoding='utf-8'))[dosya]
    if paket.get('_surum_farki'):  # B paketleri: "eski" = yapımcının önceki JSON'u + bizim onaylı çevirimiz
        eskiEN = load(KOK / 'yeni jsonlar' / f'{dosya}.json')
        eskiTR = load(KOK / 'onayli' / f'{dosya}.json')
        cev = {}
    return kontrol(kod, paket, yeni, eskiEN, eskiTR, cev, baglam)


def kontrol(kod, paket, yeni, eskiEN, eskiTR, cev, baglam):

    hatalar, stil_uyarilari, md = [], [], [f"# {paket['_paket']}\n"]
    sayac = Counter()
    harita_yolu = KOK / 'rapor' / f'{kod}_harita.json'
    harita = json.loads(harita_yolu.read_text(encoding='utf-8')) if harita_yolu.exists() else {}
    diyalog_paketi = paket.get('_dosya') == 'RadioData_lua'
    noktalama_eksik = []
    ilk_kelimeler = Counter()
    kalip_eslesmeleri = {kalip: [] for kalip in DUBLAJ_KALIPLARI}
    for i, (k, r) in enumerate(paket['satirlar'].items(), 1):
        if k not in yeni:
            hatalar.append(f'{k}: yeni EN\'de yok'); continue
        en, tr = yeni[k], r['tr']
        if SAPKALI.search(tr):
            hatalar.append(f'{k}: şapkalı harf kullanılmış')
        istisna = r.get('onayli_uslup_istisnalari', {})  # K36: D paketlerinde de, gerekçeli
        if not isinstance(istisna, dict):
            istisna = {}
        istisna = {a: b for a, b in istisna.items()
                   if a in ('hitap', 'dir', 'sozluk') and isinstance(b, str) and b.strip()}
        if k in cev:
            tur = f'Çevirmen ({cev[k][0]})'
        elif k in eskiEN and eskiEN[k] == en:
            tur = 'Eski çevirin'
        elif k in eskiEN:
            tur = 'Claude (EN değişmiş)'
        elif 'çeviri: harici AI' in paket.get('_paket', ''):
            tur = 'Fable (harici çeviri)'
        else:
            tur = 'Claude (yeni)'
        if r.get('kim'):  # K paketleri: düzeltmeyi kim yaptı
            tur = r['kim']
        degisti = (k in cev and cev[k][1] != tr) or (tur == 'Eski çevirin' and eskiTR[k] != tr)
        sayac[tur] += 1
        # Cinsiyetli zamir/hitap yer tutucuları ({he}, {him}, {sir}…) Türkçede yok olabilir ya da {g:a|b}'ye dönebilir
        # (Speech.gendered oyunda şablonu doldurur); onlar dışındakiler EN'dekiyle aynı olmalı.
        yt_en, yt_tr = [x for x in YT.findall(en) if not CINS.fullmatch(x)], [x for x in YT.findall(tr) if not CINS.fullmatch(x)]
        if Counter(x.lower() for x in yt_en) != Counter(x.lower() for x in yt_tr):  # {At}/{at}: cümle başı büyük harfli kalıp Türkçede ortada küçük olur
            hatalar.append(f'{k}: yer tutucu/biçim farkı EN={sorted(yt_en)} TR={sorted(yt_tr)}')
        for g in G.findall(tr):
            if g.count('|') != 1 or g.startswith('|') or g.endswith('|'):
                hatalar.append(f'{k}: bozuk {{g:{g}}}')
        boru_en, boru_tr = G.sub('', en).count('|'), G.sub('', tr).count('|')
        if boru_tr != boru_en or re.match(r'K\d+\b', tr):  # cinsiyet seçeneklerindeki | yukarıda çıkarıldı
            hatalar.append(f'{k}: "|" sayısı kaynakla uyuşmuyor ya da K1/K2 etiketi kalmış → {tr[:50]}')
        artik = G.sub('', tr)
        artik = re.sub(r'\{[a-zA-Z]+\}', '', artik)
        if '{' in artik or '}' in artik:
            hatalar.append(f'{k}: bozuk süslü parantez → {artik.strip()[:60]}')
        if re.search(r'[Ͱ-῿　-﫿]', tr):  # Gemini zaman zaman Kiril/Tay harfi sızdırıyor
            hatalar.append(f'{k}: Latin dışı harf')
        # Baş/son boşluk EN'dekiyle aynı olmalı (Lua ön ekleri "PAGE " gibi bilerek boşlukla biter)
        if re.match(r'\s*', tr).group() != re.match(r'\s*', en).group() or tr[len(tr.rstrip()):] != en[len(en.rstrip()):]:
            hatalar.append(f'{k}: baş/son boşluk')
        # Oyunda İngilizce kalan büyük harfli etiketler (ör. "PARTY SIZE") "siz" sayılmaz
        tr_siz = re.sub(r"\b[A-Z][A-Z0-9]+\b", "", tr)
        tr_siz = re.sub(r"\b([Üü]zgünüz|[Yy]orgunuz)\b", "", tr_siz)  # "biz üzgünüz/yorgunuz", "-ünüz" eki değil
        if SIZ.search(tr_siz) and 'hitap' not in istisna:
            hatalar.append(f'{k}: "siz" hitabı? → {SIZ.search(tr_siz).group(0)}')
        for satir in tr.split('\n'):
            if DIR.search(satir.strip()) and not EMIR.search(satir.strip()) and satir.strip() not in ('Nadir', 'Çok nadir') and 'dir' not in istisna:
                hatalar.append(f'{k}: "-dır/-mektedir" → {satir.strip()[-30:]}')
        for pat, neden in YASAK.items():
            if re.search(pat, tr) and 'sozluk' not in istisna:
                hatalar.append(f'{k}: sözlük ({neden})')
        if diyalog_paketi:
            for satir in tr.split('\n'):
                satir = satir.strip()
                if not satir:
                    continue
                if not SATIR_SONU.search(satir):
                    noktalama_eksik.append((k, satir))
                sade = re.sub(r'\{[^{}]*\}', '', satir)
                ilk = ILK_KELIME.search(sade)
                if ilk:
                    ilk_kelimeler[ilk.group(0).casefold()] += 1
            for kalip, ifade in DUBLAJ_KALIPLARI.items():
                if ifade.search(tr):
                    kalip_eslesmeleri[kalip].append(k)
        sec = (baglam.get(k) or {}).get('secenek') or {}
        bag = ', '.join(f'{a}={b}' for a, b in sec.items() if a != 'page')
        isaret = ' 🟡 ÖNERİ' if r.get('oneri') or degisti else ''
        md.append(f"### {i}. `{k}` — {tur}{isaret}")
        if bag and not re.search(r'_(tooltip|option\d+)$', k):
            md.append(f'*Bağlam: {bag}*')
        if r.get('baglam'):
            md.append(f"*Bağlam: {r['baglam']}*")
        md.append(f'- **EN:** {en!r}')
        if k in eskiEN and eskiEN[k] != en:
            md.append(f'- **Eski EN:** {eskiEN[k][:300]!r}{"…" if len(eskiEN[k]) > 300 else ""}')
        if k in eskiTR:
            md.append(f'- **Eski TR:** {eskiTR[k][:300]!r}{"…" if len(eskiTR[k]) > 300 else ""}')
        if k in cev:
            md.append(f'- **{cev[k][0]}:** {cev[k][1]!r}')
        if r.get('kullanici_tr') is not None and r['kullanici_tr'] != tr:
            md.append(f'- **Gönderdiğin TR:** {r["kullanici_tr"]!r}')
        md.append(f'- **TR:** {tr!r}')
        for tur, gerekce in istisna.items():
            if paket.get('_duzeltme'):
                etiket = 'Kullanıcı onaylı üslup'
            elif 'çeviri: harici AI' in paket.get('_paket', ''):
                etiket = 'Kullanıcı onaylı Fable istisnası'
            else:
                etiket = 'Gerekçeli üslup istisnası (Claude)'
            md.append(f'- *{etiket} ({tur}): {gerekce}*')
        if r.get('not'):
            md.append(f"- *Not: {r['not']}*")
        md.append('')
    # Terim uyarısı (hata değil): girdideki İngilizce terim var, beklenen Türkçesi yok.
    terim_uyarilari = []
    if harita.get('_terimler'):
        import arayuz_terimler
        terim_uyarilari = arayuz_terimler.uyarilar(
            [(k, yeni[k], r['tr']) for k, r in paket['satirlar'].items() if k in yeni], harita['_terimler'])

    if diyalog_paketi:
        if noktalama_eksik:
            ornekler = '; '.join(f'{k}: {satir[:80]!r}' for k, satir in noktalama_eksik[:15])
            stil_uyarilari.append(f'Satır sonu noktalaması eksik: {len(noktalama_eksik)} satır. Örnekler: {ornekler}')
        if ilk_kelimeler:
            toplam_baslangic = sum(ilk_kelimeler.values())
            en_sik = ilk_kelimeler.most_common(5)
            acilis_ozeti = ', '.join(f'{kelime}: {adet} (%{100 * adet / toplam_baslangic:.1f})' for kelime, adet in en_sik)
            stil_uyarilari.append(f'En sık satır başlangıçları ({toplam_baslangic} satır): {acilis_ozeti}')
            esik = max(5, (toplam_baslangic + 19) // 20)  # %5 veya en az 5 kullanım; yalnızca inceleme sinyali
            for kelime, adet in en_sik:
                if adet >= esik:
                    stil_uyarilari.append(
                        f'Satır başlangıcında tekrar sinyali: “{kelime}” {adet}/{toplam_baslangic} satırda '
                        f'(%{100 * adet / toplam_baslangic:.1f}); bağlama göre gözden geçir.')
        for kalip, anahtarlar in kalip_eslesmeleri.items():
            if anahtarlar:
                stil_uyarilari.append(
                    f'Üslup kalıbı “{kalip}” {len(anahtarlar)} satırda bulundu; örnek anahtarlar: {anahtarlar[:10]}')

    ozet = [
        'Dağılım: ' + ', '.join(f'{a}: {b}' for a, b in sayac.items()) + f' · Toplam: {sum(sayac.values())}\n',
        ('**Otomatik kontrol: SORUN VAR**\n' + '\n'.join(f'- {h}' for h in hatalar) + '\n') if hatalar else '**Otomatik kontrol: temiz** ✅\n',
    ]
    if terim_uyarilari:
        ozet.append(f'**Terim uyarısı (hata değil, {len(terim_uyarilari)}):** girdideki terim listesinde olan İngilizce terim satırda var ama beklenen Türkçe karşılık geçmiyor.\n'
                    + '\n'.join(f'- {u}' for u in terim_uyarilari) + '\n')
    if stil_uyarilari:
        ozet.append('**Diyalog/üslup taraması (uyarı; otomatik hata değil)**\n'
                    + '\n'.join(f'- {u}' for u in stil_uyarilari) + '\n')
    md = [md[0], *ozet, *md[1:]]
    (KOK / 'paketler' / f'{kod}.md').write_text('\n'.join(md).rstrip() + '\n', encoding='utf-8', newline='\n')
    print(dict(sayac), 'toplam', sum(sayac.values()))
    print('HATALAR:' if hatalar else 'temiz', *hatalar, sep='\n  ')
    if terim_uyarilari:
        print(f'TERİM UYARILARI ({len(terim_uyarilari)}, hata değil):', *terim_uyarilari, sep='\n  ')
    if stil_uyarilari:
        print('DİYALOG/ÜSLUP TARAMASI (uyarı; otomatik hata değil):', *stil_uyarilari, sep='\n  ')


if __name__ == '__main__':
    main(sys.argv[1])
