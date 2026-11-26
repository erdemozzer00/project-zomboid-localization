"""Ana mod güncellemesinde yalnızca noktalaması değişen diyalog satırlarının çevirisini yeni anahtara taşır.

Kullanım: python -X utf8 araclar/anahtar_tasi.py ETIKET [--uygula]
  ETIKET: sürüm adı (ör. 1.5.0); eşleme rapor/anahtar_tasima_<ETIKET>.json'a yazılır.
  --uygula olmadan yalnızca özet verir, hiçbir dosyaya yazmaz.

Anahtar = "RD_ALifeLine_" + hash(metin) olduğundan mod bir tireyi virgüle çevirince anahtar değişir ve çeviri
oyunda bulunamaz. Kurulu moddan bütün diyalog satırları (diyalog_cikar grupları + sahneler) yeniden çıkarılır;
kaynakta artık bulunmayan her eski satır, metni yalnızca noktalama/boşluk/büyük harf farkıyla aynı olan yeni
satır(lar)a eşlenir. Cümle içindeki soru ve ünlem işaretleri eşlemede korunur, sondaki yok sayılır.
Yazılanlar (--uygula): kaynak/RadioData_lua.json, kaynak/RadioData_lua_baglam.json, onayli/RadioData_lua.json
(eski anahtarın yerine yenisi, sıra korunur), paketler/haritalar/G1_harita.json ve rapor/G1_anahtarlar.json.
Eşleşmeyen eski satırlar (mod kaldırmış) yerinde kalır. Teslim/Workshop için sonra: son_kontrol → workshop_kur.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import diyalog_cikar  # noqa: E402
import sahne_cikar  # noqa: E402
from lua_cikar import h  # noqa: E402

KAYNAK, BAGLAM = KOK / "kaynak" / "RadioData_lua.json", KOK / "kaynak" / "RadioData_lua_baglam.json"
ONAYLI = KOK / "onayli" / "RadioData_lua.json"
KULLANICI_PAKETLERI = ("K1d", "K2b", "D6m")  # kullanıcının kendi metni çakışmada kazanır


def oku(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def yaz(p, veri, girinti=4):
    Path(p).write_text(json.dumps(veri, ensure_ascii=False, indent=girinti) + "\n", encoding="utf-8", newline="\n")


def imza(metin):
    """Harf/rakam + cümle içindeki soru/ünlem; geri kalan noktalama, boşluk, büyük harf ve sondaki ?/! yok sayılır
    (1.5.0'da 541 satırda yalnız sondaki işaret düşmüş ya da değişmişti: "Why do you ask?" -> "Why do you ask")."""
    return re.sub(r"[^a-z0-9?!]", "", metin.lower()).rstrip("?!")


def guncel_satirlar():
    """Kurulu moddan anahtar -> (EN, yer)."""
    out = {}
    for ad, fonk in diyalog_cikar.GRUPLAR.items():
        try:
            for en, yer in fonk():
                out.setdefault("RD_ALifeLine_" + h(en), (en, yer))
        except Exception as e:  # bir grup bozulursa ötekiler yine sayılsın
            print(f"UYARI: {ad} grubu okunamadı: {e}")
    for x in sahne_cikar.sahneler():
        for _, en in x["turlar"]:
            g = diyalog_cikar.goster(en)
            out.setdefault("RD_ALifeLine_" + h(g), (g, [x["dosya"], x["id"], x["kosul"]]))
    return out


def main(etiket, uygula):
    kaynak, baglam, onayli = oku(KAYNAK), oku(BAGLAM), oku(ONAYLI)
    guncel = guncel_satirlar()
    yeniler = defaultdict(list)
    for k, (en, _) in guncel.items():
        if k not in kaynak:
            yeniler[imza(en)].append(k)
    eski = [k for k in kaynak if k not in guncel]
    kullanici = set()
    for p in KULLANICI_PAKETLERI:
        kullanici |= set(oku(KOK / "paketler" / f"{p}.json")["satirlar"])

    esleme, hedef_sahibi, cakisma = {}, {}, 0
    for k in eski:
        if k not in onayli:
            continue
        for y in yeniler.get(imza(kaynak[k]), []):
            onceki = hedef_sahibi.get(y)
            if onceki is None:
                hedef_sahibi[y] = k
            elif onayli[onceki] != onayli[k]:
                cakisma += 1
                if k in kullanici and onceki not in kullanici:
                    hedef_sahibi[y] = k
    for y, k in hedef_sahibi.items():
        esleme.setdefault(k, []).append(y)

    birden_cok = sum(len(v) > 1 for v in esleme.values())
    kalkan = [k for k in eski if k not in esleme]
    yeni_sayi = sum(len(v) for v in yeniler.values())
    print(f"kaynakta {len(kaynak)} · modda artık olmayan {len(eski)} · modda yeni {yeni_sayi}")
    print(f"taşınacak eski satır {len(esleme)} -> yeni anahtar {len(hedef_sahibi)} "
          f"(birden çok yeni anahtara giden {birden_cok}, farklı çevirili çakışma {cakisma})")
    print(f"eşleşmeyen eski satır (mod kaldırmış) {len(kalkan)} · çevirisiz kalan yeni satır {yeni_sayi - len(hedef_sahibi)}")
    ornek = list(esleme.items())[:5]
    for k, ys in ornek:
        print(f"  {kaynak[k][:70]!r} -> {guncel[ys[0]][0][:70]!r}")
    if not uygula:
        print("--uygula verilmedi: hiçbir şey yazılmadı.")
        return

    def yeniden_kur(sozluk, deger):
        out = {}
        for k, v in sozluk.items():
            if k in esleme:
                for y in esleme[k]:
                    out[y] = deger(k, y, v)
            else:
                out[k] = v
        return out

    yaz(KAYNAK, yeniden_kur(kaynak, lambda k, y, v: guncel[y][0]))
    yaz(BAGLAM, yeniden_kur(baglam, lambda k, y, v: guncel[y][1]), 1)
    yaz(ONAYLI, yeniden_kur(onayli, lambda k, y, v: v))
    yaz(KOK / "rapor" / f"anahtar_tasima_{etiket}.json", esleme, 1)

    # G1 (sürmekte olan yeniden çeviri turu): harita ve anahtar listesi yeni anahtarlarla. Numara ve girdi dosyaları değişmez;
    # bir eski satır birden çok yeni anahtara gidiyorsa haritada ilki kalır, öteki onayla'da tasima eşlemesiyle eklenir.
    hy, ay = KOK / "paketler/haritalar" / "G1_harita.json", KOK / "rapor" / "G1_anahtarlar.json"
    if hy.exists():
        harita, anahtarlar = oku(hy), oku(ay)
        degisen = Counter()
        for n, (k, en, yer) in list(harita["satirlar"].items()):
            if k in esleme:
                y = esleme[k][0]
                harita["satirlar"][n] = [y, guncel[y][0], guncel[y][1]]
                degisen["taşındı"] += 1
            elif k not in guncel:
                degisen["modda yok"] += 1
        yaz(hy, harita, 1)
        yaz(ay, {(esleme[k][0] if k in esleme else k): v for k, v in anahtarlar.items()}, 0)
        print(f"G1 haritası: {dict(degisen)}")
    print(f"yazıldı: kaynak, bağlam, onaylı, rapor/anahtar_tasima_{etiket}.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--uygula" in sys.argv)
