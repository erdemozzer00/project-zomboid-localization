"""Diyalog paketlerini Claude Code dışında (Gemini vb.) çevirtmek için girdi dosyası hazırlar ve dönen çeviriyi pakete çevirir.

Kullanım:
  python araclar/harici_paket.py hazirla D6n d6n [--parca 300]
      diyalog_cikar.py'deki <grup>'un henüz kaynakta ve başka bir bekleyen haritada olmayan satırlarını numaralar.
      Çıktı: gemini/girdi/<PAKET>_<i>.txt (çevirmene verilecek) ve rapor/<PAKET>_harita.json (numara → anahtar).
      Sahne notu: gemini/sahne/<PAKET>.json {"_baslik", "_genel", "OLAY": "açıklama"}; olay notu yoksa
      gemini/sahne/_olaylar.json'dan (önce tam ad, sonra "ÖNEK_*") alınır. Kaynağa dokunmaz.
  python araclar/harici_paket.py al D6n [gemini/cikti/D6n_1_TR.txt ...]
      Dosya verilmezse gemini/cikti/<PAKET>_*_TR.txt dosyalarının hepsini okur. "N | Türkçe [## not: ...]" satırları.
      Tamamlanmış parçalar pakete girer; parça numaraları eksik, sırasız, yinelenmiş, yanlış aralıkta ya da yabancıysa durur.
      Hiç satırı gelmemiş parçalar bekler; sonra tekrar çalıştırınca paket onlarla birlikte yeniden kurulur.
      Satırlarının yarısından azı noktalamayla biten dosya alınmaz (skill uygulanmamış: birebir çeviri); --zorla ile alınır.
      --ad KOD: paketler/<PAKET>.json yerine paketler/KOD.json yazar (işlenmiş paketi ezmeden tek dosyayı yeniden almak için).
      --claude: paket açıklamasına çeviriyi Claude'un yaptığını yazar (K43).
      Çıktı: paketler/<PAKET>.json; alınan anahtarları kaynak/RadioData_lua.json ve _baglam.json'a ekler.
      Sonra: paket_kontrol.py <PAKET>.
  python araclar/harici_paket.py hazirla-sahne SNA [--parca 300]
      Sahneleri (araclar/sahne_cikar.py) SAHNE_PAKETLERI'ndeki konulara göre ayırır. Her sahne bir blok: numaralı satırlar
      "N | K1 | metin", çevrilmeyecek ya da çevrilmiş satırlar "· K2 | metin" bağlam satırı. Sahne parçalar arasında bölünmez.
      Çıktı yine gemini/girdi/<PAKET>_<i>.txt ve rapor/<PAKET>_harita.json; `al` değişmeden çalışır.
  python araclar/harici_paket.py hazirla-liste G1 rapor/G1_anahtarlar.json [--dosya 100] [--mevcut]
      Zaten çevrilmiş satırları Gemini'ye yeniden çevirtmek için (K47; liste: araclar/gozden_sec.py). Tam --dosya parçaya böler,
      her olay başlığına "NEREDE:" (oyuncunun satırla karşılaşma biçimi, dosya türünden) ve olay notunu yazar
      (evet/hayır satırlarında D11a/D11b, sonra gemini/sahne/<PAKET>.json, sonra _olaylar.json). --mevcut: eski Türkçeyi de gösterir.
  python araclar/harici_paket.py hazirla-yeni Y1 [--satir 127] --yeni
      Mod güncellemesiyle gelen, kaynakta ve bekleyen haritalarda olmayan BÜTÜN grup satırlarını (diyalog_cikar.GRUPLAR)
      tek pakette toplar; grup, NEREDE ve olaya göre sıralar, dosya başına ≈--satir satır. Her başlıkta NEREDE + olay notu
      (önce grubun kendi gemini/sahne/<GRUP>.json'u, sonra _olaylar.json); grup değişince o grubun SAHNE notu.
  --yeni: girdi/çıktı klasörü gemini/yeni/girdi ve gemini/yeni/cikti olur (bütün komutlarda; mod güncellemesiyle gelen
      yeni satırlar için). Verilmezse gemini/girdi ve gemini/cikti (eski çevirilerin G turları).
      Sahnelerdeki yeni satırlar: hazirla-sahne <SAHNE_PAKETLERI'nde olmayan ad, ör. Y1S> --yeni (bütün konular).
  python araclar/harici_paket.py hazirla-itibar
  python araclar/harici_paket.py hazirla-creator
      Oluşturucu cümleleri baştan çeviri için (CR1; etiketler bağlayıcı terim, ortak anahtar ve fraksiyon verisi hariç).
      İtibar ekranının bütün metinleri baştan çeviri için (K57): IG_UI anahtarları IT1, IG_UI_lua anahtarları IT2.
  python araclar/harici_paket.py hazirla-radyo Y2 --yeni [--parca 150]
      1.5.0 radyo olayları (Radio/Data/ALifeRadioEvent_*) ve telsiz sohbetleri (ALifeRadioChatter): IG_UI.json'da olup
      çevirisi olmayan metinler (rapor/arayuz_1.5.0_IG_UI.json, tür "yeni"). Her olay bir blok: kişiler, yer, satırlar dosya
      sırasıyla ve etiketli (kim konuşuyor, oyuncu seçeneği, sonuç yazısı, söylenti). Kişi adları girdiye konmaz (aynen kalır).
      Harita "_dosya": "IG_UI" taşır: `al` paketi IG_UI'ye yazar, RadioData kaynağına eklemez (onaylamadan önce kaynak/en 1.5.0 olmalı).
  python araclar/harici_paket.py hazirla-agac Y4 diyalog --yeni [--satir 128]
  python araclar/harici_paket.py hazirla-agac Y5 arayuz --yeni
      1.5.0 konuşma ağaçları (araclar/agac_cikar.py, modun kendi Lua'sıyla). diyalog: NPC sözü, oyuncu sorusu/seçeneği, bark
      havuzları, TT_* ve esir cevapları (RadioData_lua); arayuz: sekme adları, TT_* düğme/not, esir sorusu (_dosya IG_UI_lua).
      Ağaç/havuz bölünmez; kaynakta, bekleyen haritada, tekrar ya da yer tutuculu satırlar "·" bağlam satırı olur.
      `al` haritadaki _noktalama_haric (satır yer[2] öneki) satırlarını noktalama oranına katmaz; _noktalama: false denetimi kapatır;
      _dosya "_lua" ile bitiyorsa anahtarlar kaynak/<dosya>.json'a eklenir.
  python araclar/harici_paket.py hazirla-arayuz-diyalog Y3 --yeni [--satir 128]
      1.5.0 IG_UI'de hâlâ çevirisiz olup diyalog niteliğinde olan metinler (araclar/arayuz_sinif.py'nin a sınıfı, rapor/arayuz_siniflar_1.5.0.json):
      oyuncunun söylediği satırlar (görev sorusu/raporu, konuşma seçenekleri, kapı cevapları), NPC'nin tek tek sözleri (hava/ruh hâli,
      söylenti, kayıp eşya, gözcü) ve yazılı notlar (anıt, el yazısı). Konuya göre bloklanır, blok parçalar arasında bölünmez.
      Harita "_dosya": "IG_UI" taşır (Y2 gibi); `al` paketi IG_UI'ye yazar, kaynağa dokunmaz. Önce `python -X utf8 araclar/arayuz_sinif.py`.
  python araclar/harici_paket.py hazirla-kacan Y6 --yeni [--satir 128]
      1.5.0 kaçan metinlerin diyalog grubu (araclar/kacan_cikar.py -> kaynak/IG_UI_kacan.json, tür "diyalog"): durum/esir/görev
      konuşma satırları ve alt notları (impact/risk/tip), bitiş telsiz çağrısı ve helikopter sorularının cevapları. Durum ve çağrı
      düğümü başına blok; NPC'nin o sahnedeki sözleri "·" bağlam. Anahtar IGUI_ALifeUI_ (Text.ui); harita "_dosya": "IG_UI_lua":
      `al` anahtarları kaynak/IG_UI_lua.json'a ekler (Y5 gibi). Önce `python -X utf8 araclar/kacan_cikar.py`.
  python araclar/harici_paket.py hazirla-liste-soz Y7 --yeni [--satir 128]
      Tablo içi listelerdeki NPC sözleri (araclar/liste_cikar.py, rapor/kacan_listeler_1.5.0.md): durumların giriş/cevap
      sözleri, esirlerin cevapları ve bitiş telsiz çağrısının cevap şeridi sorusu (düğüm sözleri ", " ile birleşik). Anahtar
      RD_ALifeLine_ + hash(oyunda gösterilen metin: Speech.render + caption; çağrıda Call.fill + birleştirme); harita _dosya
      "RadioData_lua". Kaynakta/bekleyen haritada olan ya da tekrar eden satır "·" bağlam. Yolu olmayan bitiş sözleri alınmaz.
  python araclar/harici_paket.py hazirla-bitis-soz Y9 --yeni
      Bitişin telsiz kartı (yayının ilk satırı) ve helikopter pilotunun sözleri; konuşma ekinin kurKart/kurPilot sarmasıyla
      görünür (rapor/kacan_listeler_1.5.0.md §4). Anahtar RD_ALifeLine_, harita _dosya "RadioData_lua".
Kurallar dosyası (Gemini skill): gemini/alife-ceviri/SKILL.md
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import diyalog_cikar  # noqa: E402
from lua_cikar import h  # noqa: E402

GIRDI, CIKTI, SAHNE = KOK / "gemini" / "girdi", KOK / "gemini" / "cikti", KOK / "gemini" / "sahne"
if "--yeni" in sys.argv:  # mod güncellemesiyle gelen yeni satırlar ayrı klasörde (2026-11-09, kullanıcı)
    GIRDI, CIKTI = KOK / "gemini" / "yeni" / "girdi", KOK / "gemini" / "yeni" / "cikti"
KAYNAK, BAGLAM = KOK / "kaynak" / "RadioData_lua.json", KOK / "kaynak" / "RadioData_lua_baglam.json"


def oku(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def yaz(p, veri, girinti=4):
    Path(p).write_text(json.dumps(veri, ensure_ascii=False, indent=girinti) + "\n", encoding="utf-8", newline="\n")


def bekleyen(haric):
    """Başka paketlerin haritalarındaki (henüz kaynağa alınmamış) anahtarlar: aynı satır iki pakete girmesin."""
    out = set()
    for f in (KOK / "rapor").glob("*_harita.json"):
        if f.name != f"{haric}_harita.json":
            out |= {v[0] for v in oku(f)["satirlar"].values()}
    return out


def olay_notu(sahne, genel, olay):
    """Önce paketin sahne notu, sonra genel not; her birinde önce tam ad, sonra en uzun "ÖNEK_*"."""
    for notlar in (sahne, genel):
        if notlar.get(olay):
            return notlar[olay]
        onekler = [k for k in notlar if k.endswith("_*") and olay.startswith(k[:-1])]
        if onekler:
            return notlar[max(onekler, key=len)]
    return ""


def hazirla(paket, grup, parca=300):
    kaynak, baska = oku(KAYNAK), bekleyen(paket)
    satirlar, gorulen = [], set()
    for en, yer in diyalog_cikar.GRUPLAR[grup]():
        k = "RD_ALifeLine_" + h(en)
        if k in kaynak or k in baska or k in gorulen:
            continue
        gorulen.add(k)
        satirlar.append((k, en, yer))
    if not satirlar:
        sys.exit(f"{grup}: kaynakta olmayan satır yok")
    satirlar.sort(key=lambda r: r[2][1])  # olay adına göre (sıra kararlı: dosya sırası korunur)
    sahne = oku(SAHNE / f"{paket}.json") if (SAHNE / f"{paket}.json").exists() else {}
    genel = oku(SAHNE / "_olaylar.json") if (SAHNE / "_olaylar.json").exists() else {}
    toplam, parcalar = len(satirlar), (len(satirlar) + parca - 1) // parca
    aralik = [[p * parca + 1, min((p + 1) * parca, toplam)] for p in range(parcalar)]
    harita = {"_paket": paket, "_grup": grup, "_baslik": sahne.get("_baslik", ""), "_parcalar": aralik,
              "satirlar": {str(i): [k, en, yer] for i, (k, en, yer) in enumerate(satirlar, 1)}}
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    for p, (bas, son) in enumerate(aralik, 1):
        cikti = [f"# PAKET {paket} · parça {p}/{parcalar} · satır {bas}-{son} ({son - bas + 1} satır)",
                 "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: her satır 'N | Türkçe', numaralar aynen, hiçbirini atlama."]
        if sahne.get("_genel"):
            cikti.append("# SAHNE: " + sahne["_genel"])
        cikti.append("# Girdi biçimi: N | koşul etiketleri | İngilizce")
        olay = None
        for i in range(bas, son + 1):
            k, en, yer = satirlar[i - 1]
            if yer[1] != olay:
                olay = yer[1]
                cikti += ["", f"##### {olay} #####"]
                notu = olay_notu(sahne, genel, olay)
                if notu:
                    cikti.append("# " + notu)
            cikti.append(f"{i} | {yer[2] or '-'} | {en}")
        (GIRDI / f"{paket}_{p}.txt").write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    yaz(KOK / "rapor" / f"{paket}_harita.json", harita, 1)
    print(f"{paket}: {toplam} satır, {parcalar} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{parcalar}.txt; harita rapor/{paket}_harita.json")


SAHNE_PAKETLERI = {  # paket -> konular; None = diğer bütün konular
    "SNA": ["any"], "SNB": ["plan"], "SNC": ["shelter"], "SND": ["panic_days"], "SNE": None,
}
SNE_HARIC = {k for v in SAHNE_PAKETLERI.values() if v for k in v}
SAHNE_ACIKLAMA = ("# SAHNE BLOKLARI: Her '##### SAHNE ... #####' başlığı bir, iki ya da daha çok NPC'nin kendi aralarındaki (tek kişiyse kendi kendine) TEK bir konuşmasıdır; "
                  "satırlar sırayla söylenir. K1, K2, K3 konuşmacı numaralarıdır, aynı sahnede hep aynı kişi. Başlıktaki koşullar: "
                  "reg/r1/r2/r3 = konuşanın rolü (r1 = K1), x1=f ya da x1=m = K1 kadın/erkek, mood = ruh hali, day/hour = salgının günü/saat, "
                  "world = mekân, faction = grup. '· ' ile başlayan satırlar BAĞLAMDIR (numarasızdır, çevirme, çıktıya yazma); numaralı satırların "
                  "tamamını çevir. Sahneyi baştan sona oku, konuşma bir bütündür: sözü devralma, 'o', 'bu', 'sen' göndermeleri ve ritim sahne boyunca tutarlı olsun.")


def hazirla_sahne(paket, parca=300):
    import sahne_cikar
    hepsi = paket not in SAHNE_PAKETLERI  # ör. Y1S: güncellemeyle gelen yeni sahne satırları, bütün konular
    konular = SAHNE_PAKETLERI.get(paket)
    kaynak, baska = oku(KAYNAK), bekleyen(paket)
    onayli = oku(KOK / "onayli" / "RadioData_lua.json") if (KOK / "onayli" / "RadioData_lua.json").exists() else {}
    secili = [x for x in sahne_cikar.sahneler()
              if hepsi or (x["konu"] in konular if konular else x["konu"] not in SNE_HARIC)]
    secili.sort(key=lambda x: (x["kosul"].split("|")[0], x["id"]))
    gorulen, bloklar, no = set(), [], 0
    satirlar = {}
    for x in secili:
        satir, yeni = [], 0
        for kisi, en in x["turlar"]:
            k = "RD_ALifeLine_" + h(diyalog_cikar.goster(en))
            etiket = f"K{kisi}"
            if "{" in en:
                satir.append(f"  · {etiket} | {en}   [yer tutuculu, çevrilmeyecek]")
            elif k in kaynak or k in baska:
                tr = onayli.get(k)
                satir.append(f"  · {etiket} | {en}" + (f"   → {tr}" if tr else ""))
            elif k in gorulen:
                satir.append(f"  · {etiket} | {en}   [aynı satır başka sahnede çevriliyor]")
            else:
                gorulen.add(k)
                no += 1
                yeni += 1
                satirlar[str(no)] = [k, en, [x["dosya"], x["id"], x["kosul"]]]
                satir.append(f"{no} | {etiket} | {en}")
        if yeni:
            bloklar.append((x, satir, yeni))
    if not bloklar:
        sys.exit(f"{paket}: çevrilecek sahne satırı yok")
    parcalar, mevcut, sayi = [], [], 0
    for blok in bloklar:
        if mevcut and sayi + blok[2] > parca + parca // 10:
            parcalar.append(mevcut)
            mevcut, sayi = [], 0
        mevcut.append(blok)
        sayi += blok[2]
    parcalar.append(mevcut)
    notlar = oku(SAHNE / f"{paket}.json") if (SAHNE / f"{paket}.json").exists() else {}
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    aralik, ilk = [], 1
    for p, blk in enumerate(parcalar, 1):
        son = ilk + sum(b[2] for b in blk) - 1
        aralik.append([ilk, son])
        cikti = [f"# PAKET {paket} · parça {p}/{len(parcalar)} · satır {ilk}-{son} ({son - ilk + 1} satır, {len(blk)} sahne)",
                 "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: yalnızca numaralı satırlar, her biri 'N | Türkçe' (K1/K2 etiketini yazma), "
                 "numaralar aynen, hiçbirini atlama.",
                 SAHNE_ACIKLAMA]
        if notlar.get("_genel"):
            cikti.append("# SAHNE: " + notlar["_genel"])
        for x, satir, _ in blk:
            cikti += ["", f"##### SAHNE {x['id']} · {x['konu']} · {x['kisi']} kişi · {x['kosul'] or '-'} #####"] + satir
        (GIRDI / f"{paket}_{p}.txt").write_text(chr(10).join(cikti) + chr(10), encoding="utf-8", newline=chr(10))
        ilk = son + 1
    yaz(KOK / "rapor" / f"{paket}_harita.json", {"_paket": paket, "_grup": "sahne", "_baslik": notlar.get("_baslik", ""),
        "_parcalar": aralik, "satirlar": satirlar}, 1)
    print(f"{paket}: {len(satirlar)} satır, {len(bloklar)} sahne, {len(parcalar)} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{len(parcalar)}.txt")


YENIDEN_ACIKLAMA = ("# YENİDEN ÇEVİRİ: Bu satırlar oyunda şu an skill'den önceki eski bir çeviriyle görünüyor; sıfırdan, İngilizceden kur. "
                    "Her başlığın altındaki 'NEREDE:' oyuncunun bu sözle nasıl karşılaştığını, '#' notu sahneyi anlatır. Önce bunları oku, "
                    "satırı o anda o yerde duyulacak sözle yaz.")
MEVCUT_ACIKLAMA = ("# MEVCUT: Her numaralı satırın altındaki 'MEVCUT:' oyundaki eski Türkçedir. Önce kendi satırını İngilizceden kur, sonra bak: "
                   "MEVCUT gerçekten doğal ve tamsa aynen yaz, değilse kendi satırını yaz. 'MEVCUT:' satırlarını çıktıya yazma.")
NEREDE = [  # (dosya öneki, oyuncunun karşılaşma biçimi); ilk eşleşen kazanır, özel önek genelden önce
    ("ALifeDialogue_replies_door_", "Oyuncunun sığınağının kapısında. Kapıyı çalan yabancı, kapının arkasındaki oyuncuya konuşuyor; "
                                    "bu, oyuncunun kapıdan söylediğine ya da yaptığına yabancının cevabı. Tek kişiye 'sen'; "
                                    "içeridekilerin hepsine seslenen satırlarda ('folks', 'everyone', 'all of you') çoğul."),
    ("ALifeDialogue_yes_", "Konuşma penceresinde. NPC oyuncuya bir şey sordu ya da teklif etti, oyuncu EVET düğmesine bastı; bu, NPC'nin "
                           "o cevaba yüz yüze tepkisi. Oyuncu okuyup konuşmaya devam eder."),
    ("ALifeDialogue_no_", "Konuşma penceresinde. NPC oyuncuya bir şey sordu ya da teklif etti, oyuncu HAYIR düğmesine bastı; bu, NPC'nin "
                          "o cevaba yüz yüze tepkisi. Oyuncu okuyup konuşmaya devam eder."),
    ("ALifeDialogue_replies_npc_", "Konuşma penceresinde. Oyuncu NPC'nin yanına gidip konuşmayı açtı; bu, pencere açılınca NPC'nin oyuncuya "
                                   "yüz yüze ilk sözü, 'sen'. Oyuncu okuyup bir konu seçecek."),
    ("ALifeDialogue_replies_", "Konuşma penceresinde. Oyuncu NPC'nin yanına gidip konuşmayı açtı ve listeden bu konuyu seçti; bu, NPC'nin "
                               "oyuncuya yüz yüze cevabı, 'sen'. Oyuncu satırı rahatça okur, sonra başka bir konu seçer."),
    ("ALifeDialogue_followb_barks_", "Dünyada, NPC'nin başının üstünde birkaç saniye görünen yazı. Konuşan, oyuncunun "
                                     "karşılaştığı bir grubun üyesi (etiketteki faction); söz oyuncuya ya da kendi arkadaşlarına, "
                                     "olay anında atılır. Kimse cevap vermez; bir bakışta okunacak, ağızdan çıktığı gibi olmalı."),
    ("ALifeTalk.lua", "Konuşma penceresinde. Oyuncu NPC'ye listeden bir soru sordu; bu, NPC'nin oyuncuya yüz yüze cevabı, 'sen'."),
    ("ALifeModuleBreach.lua", "Dünyada, NPC'nin başının üstünde birkaç saniye görünen yazı. NPC'ler kapalı bir kapıyı kırıp içeri "
                              "girmeye hazırlanıyor; ekip içi kısa komut."),
    ("ALifeModuleCareful.lua", "Dünyada, NPC'nin başının üstünde birkaç saniye görünen yazı. NPC, kendisine fazla yaklaşan ya da "
                               "silah doğrultan oyuncuyu uyarıyor; kısa, gergin, oyuncuya 'sen'."),
    ("ALifeDialogue_barks_", "Dünyada, NPC'nin başının üstünde birkaç saniye görünen yazı. Oyuncu yanından geçerken, yakınında dolaşırken "
                             "ya da olay anında görür; kimse cevap vermez, söylenip geçilen kısa söz. Bir bakışta okunacak, ağızdan çıktığı gibi olmalı."),
]


def nerede(dosya):
    return next((metin for onek, metin in NEREDE if dosya.startswith(onek)), "")


def hazirla_liste(paket, anahtar_dosya, dosya_sayisi=100, mevcut=False):
    """Zaten çevrilmiş satırları yeniden çevirtmek için (K47). Olay + karşılaşma yerine göre sıralar, tam dosya_sayisi parçaya böler."""
    kaynak, baglam = oku(KAYNAK), oku(BAGLAM)
    onayli = oku(KOK / "onayli" / "RadioData_lua.json")
    satirlar = [(k, kaynak[k], baglam[k]) for k in oku(anahtar_dosya)]
    satirlar.sort(key=lambda r: (nerede(r[2][0]), r[2][1]))  # aynı yerde görünenler ve aynı olay yan yana; sıra kararlı
    sahne = oku(SAHNE / f"{paket}.json") if (SAHNE / f"{paket}.json").exists() else {}
    genel = oku(SAHNE / "_olaylar.json")
    cevap = {"ALifeDialogue_yes_": oku(SAHNE / "D11a.json"), "ALifeDialogue_no_": oku(SAHNE / "D11b.json")}
    toplam = len(satirlar)
    aralik = [[p * toplam // dosya_sayisi + 1, (p + 1) * toplam // dosya_sayisi] for p in range(dosya_sayisi)]
    harita = {"_paket": paket, "_grup": "yeniden", "_baslik": sahne.get("_baslik", ""), "_parcalar": aralik,
              "satirlar": {str(i): [k, en, yer] for i, (k, en, yer) in enumerate(satirlar, 1)}}
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    notsuz, yersiz = set(), set()
    for p, (bas, son) in enumerate(aralik, 1):
        cikti = [f"# PAKET {paket} · parça {p}/{dosya_sayisi} · satır {bas}-{son} ({son - bas + 1} satır)",
                 "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: her satır 'N | Türkçe', numaralar aynen, hiçbirini atlama.",
                 YENIDEN_ACIKLAMA]
        if mevcut:
            cikti.append(MEVCUT_ACIKLAMA)
        if sahne.get("_genel"):
            cikti.append("# SAHNE: " + sahne["_genel"])
        cikti.append("# Girdi biçimi: N | koşul etiketleri | İngilizce")
        grup = None
        for i in range(bas, son + 1):
            k, en, yer = satirlar[i - 1]
            yer_metni = nerede(yer[0])
            if (yer_metni, yer[1]) != grup:
                grup = (yer_metni, yer[1])
                cikti += ["", f"##### {yer[1]} #####"]
                if yer_metni:
                    cikti.append("# NEREDE: " + yer_metni)
                else:
                    yersiz.add(yer[0])
                ozel = next((n for onek, n in cevap.items() if yer[0].startswith(onek)), None)
                notu = (olay_notu(ozel, {}, yer[1]) if ozel else "") or olay_notu(sahne, genel, yer[1])
                if notu:
                    cikti.append("# " + notu)
                else:
                    notsuz.add(yer[1])
            cikti.append(f"{i} | {yer[2] or '-'} | {en}")
            if mevcut:
                cikti.append(f"MEVCUT: {onayli[k]}")
        (GIRDI / f"{paket}_{p}.txt").write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    yaz(KOK / "rapor" / f"{paket}_harita.json", harita, 1)
    print(f"{paket}: {toplam} satır, {dosya_sayisi} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya_sayisi}.txt; "
          f"notsuz olay: {sorted(notsuz) or 'yok'}; yeri bilinmeyen dosya: {sorted(yersiz) or 'yok'}")


RADYO_ACIKLAMA = ("# RADYO OLAYLARI: Oyuncunun telsizinden (Field Band) gelen yardım çağrıları ve olaylar. Her '##### OLAY ... #####' başlığı tek "
                  "bir olaydır; KİŞİLER satırı konuşanları (ad, rol, huy) verir, satırlar olayın akış sırasıyla gelir. Etiketler: '<Ad> telsizde' = "
                  "o kişi telsizden konuşuyor (oyuncuyu görmüyor, sesi kısık/cızırtılı olabilir), '<Ad>' = olay yerinde ya da cevap olarak söylüyor, "
                  "'OYUNCU SEÇENEĞİ' = oyuncunun seçip söylediği cevap düğmesi (birinci tekil, kısa), 'SONUÇ' = olay bitince oyuncuya gösterilen "
                  "anlatım ('sen' = oyuncu, geçmiş zaman), 'GÖREV' = görev kartındaki başlık/özet/adım, 'SÖYLENTİ' = olaydan sonra başka NPC'lerin "
                  "anlattığı cümle; oyunda 'Evet, {what}' / 'Telsizde duydum, {what}' gibi bir cümlenin içine konur, küçük harfle başlar, noktasız "
                  "biter. Kişi adlarını aynen yaz. {dist} adım sayısı, {dir} yön (kuzeyinde, doğusunda…) olarak dolar: '{dist} adım {dir}' gibi kur.")
TELSIZ_ACIKLAMA = ("# TELSİZ SOHBETİ: Radyoda rastgele duyulan kısa telsiz konuşmaları (devriyeler, nöbetçiler, uzak gruplar). Her başlık bir "
                   "konuşma; etiket konuşanın telsiz çağrı adı. Çağrı adı satırları (ÇAĞRI ADI) kısa ve telsiz diline uygun çevrilir.")


def hazirla_radyo(paket, parca=150):
    """1.5.0 radyo olayları + telsiz sohbeti -> IG_UI anahtarlı Gemini girdisi (K52)."""
    gerek = {k for k, v in oku(KOK / "rapor" / "arayuz_1.5.0_IG_UI.json").items() if v["tur"] == "yeni"}
    baska = bekleyen(paket)
    kok = diyalog_cikar.LUA_KOK / "shared" / "ProjectALife" / "Radio"
    bloklar, gorulen = [], set()

    def ekle(satirlar, k, en, etiket, yer):
        if k in gerek and k not in baska and k not in gorulen:
            gorulen.add(k)
            satirlar.append((k, en, etiket, yer))

    for f in sorted((kok / "Data").glob("ALifeRadioEvent_*.lua")):
        metin = f.read_text(encoding="utf-8")
        adlar = dict(re.findall(r'key = "(\w+)", name = "([^"]+)"', metin))
        kisiler = []
        for govde in re.findall(r'\{ key = "\w+", name = .*?quirk = "[^"]*" \}', metin, re.S):
            a = dict(re.findall(r'(\w+) = "([^"]*)"', govde))
            kisiler.append(f"{a.get('name')} ({'kadın' if a.get('sex') == 'f' else 'erkek'}, {a.get('role', '')}; {a.get('quirk', '')})")
        olay = re.search(r'id = "(\w+)"', metin).group(1)
        baslik = re.search(r'title = "([^"]*)"', metin)
        yer_tur = re.search(r'kinds = \{([^}]*)\}', metin)
        satirlar, bolum, dugum = [], "", ""
        for satir in metin.splitlines():
            m = re.match(r"^    (\w+) = ", satir)
            if m:
                bolum = m.group(1)
            m = re.match(r"^        (\w+) = \{", satir)
            if m and bolum == "nodes":
                dugum = m.group(1)
            if bolum == "cast":
                continue  # kişi adları aynen kalır
            who = re.search(r'who = "(\w+)"', satir)
            for s_ in re.findall(diyalog_cikar.STR, satir):
                en = diyalog_cikar.un(s_)
                k = "IGUI_ALifeUI_" + h(en)
                if bolum in ("title", "task"):
                    etiket = "GÖREV"
                elif bolum == "rumor":
                    etiket = "SÖYLENTİ"
                elif who and en != who.group(1):
                    ad = adlar.get(who.group(1), who.group(1)).split()[0]
                    telsiz = bolum in ("callbacks", "memory", "reminder") or (bolum == "nodes" and dugum == "call")
                    etiket = ad + (" telsizde" if telsiz else "")
                elif re.search(r'\bid = "', satir) and bolum == "nodes":
                    etiket = "OYUNCU SEÇENEĞİ"
                elif bolum == "outcomes":
                    etiket = "SONUÇ"
                else:
                    etiket = bolum.upper() or "-"
                ekle(satirlar, k, en, etiket, [f.name, olay, etiket])
        if satirlar:
            ust = [f"##### OLAY {olay} · {baslik.group(1) if baslik else ''} #####",
                   "# KİŞİLER: " + "; ".join(kisiler)]
            if yer_tur:
                ust.append("# YER: " + yer_tur.group(1).replace('"', "").strip())
            bloklar.append((ust, satirlar))
    sohbet = (kok / "ALifeRadioChatter.lua").read_text(encoding="utf-8")
    for cid, govde in re.findall(r'Chatter\.add\(\{ id = "(\w+)".*?lines = \{(.*?)\} \}\)', sohbet, re.S):
        satirlar = []
        for ad, en in re.findall(r'name = "([^"]*)", text = "((?:[^"\\]|\\.)*)"', govde):
            ekle(satirlar, "IGUI_ALifeUI_" + h(ad), ad, "ÇAĞRI ADI", ["ALifeRadioChatter.lua", cid, "ÇAĞRI ADI"])
            en = diyalog_cikar.un(en)
            ekle(satirlar, "IGUI_ALifeUI_" + h(en), en, ad, ["ALifeRadioChatter.lua", cid, ad])
        if satirlar:
            bloklar.append(([f"##### TELSİZ {cid} #####"], satirlar))
    parcalar, mevcut, sayi = [], [], 0
    for blok in bloklar:
        if mevcut and sayi + len(blok[1]) > parca + parca // 10:
            parcalar.append(mevcut)
            mevcut, sayi = [], 0
        mevcut.append(blok)
        sayi += len(blok[1])
    parcalar.append(mevcut)
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    harita, aralik, no = {}, [], 0
    for p, blk in enumerate(parcalar, 1):
        ilk = no + 1
        govde = []
        for ust, satirlar in blk:
            govde += [""] + ust
            for k, en, etiket, yer in satirlar:
                no += 1
                harita[str(no)] = [k, en, yer]
                govde.append(f"{no} | {etiket} | {en}")
        aralik.append([ilk, no])
        cikti = [f"# PAKET {paket} · parça {p}/{len(parcalar)} · satır {ilk}-{no} ({no - ilk + 1} satır)",
                 "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama.",
                 YENI_ACIKLAMA, RADYO_ACIKLAMA, TELSIZ_ACIKLAMA, "# Girdi biçimi: N | etiket | İngilizce"] + govde
        (GIRDI / f"{paket}_{p}.txt").write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    yaz(KOK / "rapor" / f"{paket}_harita.json", {"_paket": paket, "_grup": "radyo", "_dosya": "IG_UI",
        "_baslik": "1.5.0 radyo olayları ve telsiz sohbeti", "_parcalar": aralik, "satirlar": harita}, 1)
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {len(parcalar)} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{len(parcalar)}.txt")


YENI_ACIKLAMA = ("# YENİ SATIRLAR: Modun son güncellemesiyle gelen, henüz hiç çevrilmemiş satırlar. Her başlığın altındaki 'NEREDE:' "
                 "oyuncunun bu sözle nasıl karşılaştığını, '#' notu sahneyi anlatır. Önce bunları oku, satırı o anda o yerde duyulacak sözle yaz.")
def kisa_kosul(kosul):
    """faction=<uzun liste> etiketini satır başına tekrar yazmamak için kısaltır: ilk birkaç grup adı + kalan sayısı.
    Grupları tarif etmez (mod bu kümelere ad vermiyor; K33: kaynakta olmayanı ekleme). Öteki etiketler aynen kalır."""
    parcalar = []
    for p in (kosul or "").split("|"):
        if p.startswith("faction=") and p.count(",") >= 5:
            ids = [i.removeprefix("alife_").replace("_", " ") for i in p[len("faction="):].split(",")]
            p = "faction=" + ", ".join(ids[:6]) + f" ve {len(ids) - 6} grup daha"
        parcalar.append(p)
    return "|".join(parcalar)


def grup_paketi(grup):
    return grup[0].upper() + grup[1:]  # d10a -> D10a, z1 -> Z1


def hazirla_yeni(paket, satir_basina=127):
    """Mod güncellemesiyle gelen yeni grup satırları (henüz hiç çevrilmemiş). hazirla_liste düzeni, YENİ başlığıyla."""
    kaynak, baska = oku(KAYNAK), bekleyen(paket)
    satirlar, gorulen, grup_sira = [], set(), {}
    for gi, (grup, fonk) in enumerate(diyalog_cikar.GRUPLAR.items()):
        grup_sira[grup] = gi
        for en, yer in fonk():
            k = "RD_ALifeLine_" + h(en)
            if k in kaynak or k in baska or k in gorulen:
                continue
            gorulen.add(k)
            satirlar.append((k, en, yer, grup))
    if not satirlar:
        sys.exit("kaynakta olmayan yeni satır yok")
    satirlar.sort(key=lambda r: (grup_sira[r[3]], nerede(r[2][0]), r[2][1]))
    genel = oku(SAHNE / "_olaylar.json")
    yedek = oku(SAHNE / "G1.json")
    cevap = {"ALifeDialogue_yes_": oku(SAHNE / "D11a.json"), "ALifeDialogue_no_": oku(SAHNE / "D11b.json")}
    sahneler = {}
    for *_, g in satirlar:
        f = SAHNE / f"{grup_paketi(g)}.json"
        sahneler[g] = oku(f) if f.exists() else yedek
    toplam = len(satirlar)
    dosya_sayisi = max(1, round(toplam / satir_basina))
    aralik = [[p * toplam // dosya_sayisi + 1, (p + 1) * toplam // dosya_sayisi] for p in range(dosya_sayisi)]
    harita = {"_paket": paket, "_grup": "yeni", "_baslik": "Mod güncellemesiyle gelen yeni diyaloglar", "_parcalar": aralik,
              "satirlar": {str(i): [k, en, yer] for i, (k, en, yer, _) in enumerate(satirlar, 1)}}
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    notsuz, yersiz = set(), set()
    for p, (bas, son) in enumerate(aralik, 1):
        cikti = [f"# PAKET {paket} · parça {p}/{dosya_sayisi} · satır {bas}-{son} ({son - bas + 1} satır)",
                 "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: her satır 'N | Türkçe', numaralar aynen, hiçbirini atlama.",
                 YENI_ACIKLAMA, "# Girdi biçimi: N | koşul etiketleri | İngilizce"]
        grup, baslik = None, None
        for i in range(bas, son + 1):
            k, en, yer, g = satirlar[i - 1]
            if g != grup:
                grup, baslik = g, None
                if sahneler[g].get("_genel"):
                    cikti += ["", "# SAHNE: " + sahneler[g]["_genel"]]
            yer_metni = nerede(yer[0])
            if (yer_metni, yer[1]) != baslik:
                baslik = (yer_metni, yer[1])
                cikti += ["", f"##### {yer[1]} #####"]
                if yer_metni:
                    cikti.append("# NEREDE: " + yer_metni)
                else:
                    yersiz.add(yer[0])
                ozel = next((n for onek, n in cevap.items() if yer[0].startswith(onek)), None)
                notu = (olay_notu(ozel, {}, yer[1]) if ozel else "") or olay_notu(sahneler[g], genel, yer[1])
                if notu:
                    cikti.append("# " + notu)
                else:
                    notsuz.add(yer[1])
            cikti.append(f"{i} | {kisa_kosul(yer[2]) or '-'} | {en}")
        (GIRDI / f"{paket}_{p}.txt").write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    yaz(KOK / "rapor" / f"{paket}_harita.json", harita, 1)
    print(f"{paket}: {toplam} satır, {dosya_sayisi} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya_sayisi}.txt; "
          f"notsuz olay: {sorted(notsuz) or 'yok'}; yeri bilinmeyen dosya: {sorted(yersiz) or 'yok'}")


AGAC_ACIKLAMA = ("# KONUŞMA AĞAÇLARI: Oyuncu konuşma penceresinde bir soru seçer, NPC cevap verir, oyuncu seçeneklerden birini seçer, "
                 "konuşma dallanır. Her '##### AĞAÇ ... #####' başlığı TEK bir konuşmadır; KİM satırı konuşan NPC'yi (blok: law polis, "
                 "military asker, crime suç/çete, survivor hayatta kalan, rescue kurtarıcı, social genel; rol: visitor kapıya gelen, "
                 "companion yol arkadaşı, trader tüccar, captive esir…), gün aralığını, tutumunu verir. Etiketler: 'OYUNCU SORUSU' = "
                 "konuşmayı açan, oyuncunun seçtiği düğme; 'OYUNCU SEÇENEĞİ → düğüm' = oyuncunun cevap düğmesi, ok nereye gittiğini "
                 "gösterir; 'NPC' = NPC'nin sözü (konuşma penceresinde ve başının üstünde görünür); 'NPC 1/2 (biri seçilir)' = aynı "
                 "anda yalnız biri söylenir, ikisi de tek başına anlamlı olmalı; ifade/ruh hâli NPC'nin o andaki tavrıdır. '# düğüm X ← "
                 "\"…\"' satırı oyuncunun hangi seçimiyle oraya gelindiğini söyler. Düğmeler (soru ve seçenek) oyuncunun kendi ağzından, "
                 "birinci tekil, KISA ve sonda nokta olmadan yazılır (soru işareti/ünlem kalabilir); NPC sözleri cümle noktalamasıyla. "
                 "'[Charm]' etiketli seçeneğin başına oyun '[Charm] ' ekler: sen yazma. '· etiket | metin' satırları bağlamdır "
                 "(başka yerde çevriliyor ya da oyunda dolan yer tutucusu olduğu için çevrilmez): numarası yok, çıktıya yazma.")
HAVUZ_ACIKLAMA = ("# HAVUZLAR: '##### HAVUZ blok · olay #####' başlığı, NPC'nin o olayda kendiliğinden söylediği kısa sözlerin "
                  "listesidir (başının üstünde görünür). Her satır ayrı ayrı rastgele seçilir; birbirinin devamı değildir. "
                  "'@d7' gibi ek o sözün yalnız oyunun 7.-14. günlerinde kullanıldığını söyler (d0: 0-7, d14: 14-30, d30: 30-60, d60: sonrası).")
ZINCIR_ACIKLAMA = ("# SORU ZİNCİRİ ve ESİR: Oyuncunun sorusu '#' satırında verilir (soru arayüz paketinde ayrıca çevrilir), altındaki "
                   "satırlar NPC'nin cevabıdır; parantezdeki grup cevabı kimin verdiğini söyler (aynı soruya grubuna göre biri). "
                   "ESİR bloklarında konuşan, oyuncunun esir aldığı NPC'dir (bağlı, korkmuş ya da inatçı).")
HAVUZ_OLAY = {
    "greet_stranger": "tanımadığı oyuncuyu karşılarken", "greet_known": "tanıdığı oyuncuyu karşılarken",
    "greet_friend": "dostu olan oyuncuyu karşılarken", "warn_lower_weapon": "oyuncuya silahını indirmesini söylerken",
    "warn_back_off": "oyuncuyu uzaklaşması için uyarırken", "refuse_talk": "konuşmayı reddederken", "bye": "vedalaşırken",
    "ask_supplies_yes": "oyuncunun erzak isteğini kabul ederken", "ask_supplies_no": "oyuncunun erzak isteğini reddederken",
    "give_thanks": "teşekkür ederken", "surrender_beg": "teslim olup yalvarırken", "surrender_comply": "teslim olup emre uyarken",
    "flee_panic": "panikle kaçarken", "hurt_pain": "yaralanıp acı çekerken", "help_me": "yardım isterken",
    "ally_down": "yanındaki biri düşünce", "taking_fire": "ateş altındayken", "reloading": "şarjör değiştirirken",
    "kill_confirm": "düşmanı vurduktan sonra", "threat_spotted": "tehlike görünce", "all_in_charge": "hep birlikte saldırıya geçerken",
    "fear_break": "korkudan dağılırken", "melee_taunt": "yakın dövüşte karşısındakine laf atarken",
    "idle_chatter": "boş anlarda kendi kendine ya da yanındakine", "visitor_arrive": "oyuncunun kapısına geldiğinde",
    "visitor_wait_gate": "oyuncunun kapısında beklerken", "visitor_leave": "oyuncunun kapısından ayrılırken",
    "companion_follow_ack": "yol arkadaşı olarak 'beni takip et' emrine cevap verirken",
    "companion_hold_ack": "yol arkadaşı olarak 'burada bekle' emrine cevap verirken",
    "companion_idle": "yol arkadaşı olarak boş anlarda oyuncuya", "radio_chatter": "telsizde konuşurken",
}
ARAYUZ_ACIKLAMA = ("# ARAYÜZ: Konuşma penceresindeki düğmeler ve altlarındaki kısa notlar. 'OYUNCU SORUSU' oyuncunun kendi ağzından "
                   "birinci tekil soru/söz (kısa, sonda nokta yok); 'NOT' düğmenin altında küçük yazıyla görünen, ne olacağını anlatan "
                   "kısa açıklama (sonda nokta yok); 'KOŞUL NOTU' düğmenin açılması için gereken (ör. güven, beceri). Sığması için kısa tut.")


def _bloklari_yaz(paket, bloklar, parca, aciklama, ek_harita, yeni=True, kurallar=None):
    """[(baslik_satirlari, [(k, en, etiket, yer) | ("#", not) | ("·", etiket, en)])] -> girdi dosyaları + harita.
    Blok parçalar arasında bölünmez (tek blok parçadan büyükse tek başına bir dosya).
    aciklama: satır listesi ya da o dosyadaki İngilizce satırların listesini alıp satır listesi döndüren işlev (arayüz girdileri: terim listesi).
    yeni=False: "YENİ SATIRLAR" diyalog açıklaması konmaz; kurallar: ikinci başlık satırını değiştirir."""
    parcalar, mevcut, sayi = [], [], 0
    for blok in bloklar:
        n = sum(1 for x in blok[1] if x[0] not in ("#", "·"))
        if mevcut and sayi + n > parca + parca // 10:
            parcalar.append(mevcut)
            mevcut, sayi = [], 0
        mevcut.append(blok)
        sayi += n
    if mevcut:
        parcalar.append(mevcut)
    GIRDI.mkdir(parents=True, exist_ok=True)
    for eski in GIRDI.glob(f"{paket}_*.txt"):
        eski.unlink()
    harita, aralik, no = {}, [], 0
    for p, blk in enumerate(parcalar, 1):
        ilk, govde, ens = no + 1, [], []
        for ust, satirlar in blk:
            govde += [""] + ust
            for x in satirlar:
                if x[0] == "#":
                    govde.append("# " + x[1])
                elif x[0] == "·":
                    govde.append(f"· {x[1]} | {x[2]}")
                else:
                    k, en, etiket, yer = x
                    no += 1
                    harita[str(no)] = [k, en, yer]
                    ens.append(en)
                    govde.append(f"{no} | {etiket} | {en.replace(chr(10), chr(92) + 'n')}")  # gerçek satır sonu girdide '\n' yazılır (Sandbox ipuçları)
        aralik.append([ilk, no])
        cikti = [f"# PAKET {paket} · parça {p}/{len(parcalar)} · satır {ilk}-{no} ({no - ilk + 1} satır)",
                 kurallar or "# Kurallar: A-Life çeviri kuralları (skill). Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama."]
        cikti += [YENI_ACIKLAMA] if yeni else []
        cikti += (aciklama(ens) if callable(aciklama) else aciklama) + ["# Girdi biçimi: N | etiket | İngilizce"] + govde
        (GIRDI / f"{paket}_{p}.txt").write_text("\n".join(cikti) + "\n", encoding="utf-8", newline="\n")
    yaz(KOK / "rapor" / f"{paket}_harita.json", {"_paket": paket, **ek_harita, "_parcalar": aralik, "satirlar": harita}, 1)
    return no, len(parcalar)


def hazirla_agac(paket, tur, parca=128):
    """1.5.0 konuşma ağaçları (araclar/agac_cikar.py). tur 'diyalog': RadioData_lua anahtarlı NPC sözü, oyuncu sorusu, seçenek,
    bark, TT_* NPC cevabı, esir cevabı. tur 'arayuz': IG_UI_lua anahtarlı sekme adı, TT_* düğme/not, esir sorusu/notu."""
    import agac_cikar
    baska = bekleyen(paket)
    gorulen = set()
    if tur == "diyalog":
        kaynak = oku(KAYNAK)
        ham, sayac = agac_cikar.agaclar()
        bloklar, cevrilen, atlanan = [], 0, 0
        for b in ham:
            satirlar = []
            for x in b["satirlar"]:
                if x[0] == "#":
                    satirlar.append(x)
                elif x[0] is None:
                    satirlar.append(("·", x[2], x[1] + "  (yer tutuculu, çevrilmez)"))
                elif x[0] in kaynak or x[0] in baska or x[0] in gorulen:
                    satirlar.append(("·", x[2], x[1]))
                    cevrilen += 1
                else:
                    gorulen.add(x[0])
                    satirlar.append(x)
            if not any(x[0] not in ("#", "·") for x in satirlar):
                atlanan += 1
                continue
            ust = list(b["baslik"])
            if b["tur"] == "havuz":
                ust.append("# NEREDE: NPC'nin " + HAVUZ_OLAY.get(b["olay"], b["olay"]) + " söylediği tek cümle (başının üstünde)"
                           + (f"; yalnız {b['faz']} döneminde" if b["faz"] else ""))
            bloklar.append((ust, satirlar))
        no, dosya = _bloklari_yaz(paket, bloklar, parca, [AGAC_ACIKLAMA, HAVUZ_ACIKLAMA, ZINCIR_ACIKLAMA],
                                  {"_grup": "agac", "_baslik": "1.5.0 konuşma ağaçları (diyalog)",
                                   "_noktalama_haric": ["soru", "secenek"]})
        print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt; "
              f"bağlam olarak gösterilen (kaynakta/bekleyen/tekrar) {cevrilen}; yer tutuculu (çevrilmez) {sayac['yer_tutuculu']}; "
              f"tamamı çevrili olduğu için atlanan blok {atlanan}")
    elif tur == "arayuz":
        dolu = set(oku(KOK / "kaynak" / "IG_UI_lua.json")) | set(oku(KOK / "kaynak" / "en" / "IG_UI.json"))
        bloklar, haric = [], 0
        for b in agac_cikar.arayuz():
            satirlar = []
            for x in b["satirlar"]:
                if x[0] in dolu or x[0] in baska or x[0] in gorulen:
                    haric += 1
                    continue
                gorulen.add(x[0])
                satirlar.append(x)
            if satirlar:
                bloklar.append((b["baslik"], satirlar))
        no, dosya = _bloklari_yaz(paket, bloklar, parca, [ARAYUZ_ACIKLAMA],
                                  {"_grup": "agac_arayuz", "_dosya": "IG_UI_lua", "_noktalama": False,
                                   "_baslik": "1.5.0 konuşma ağaçları (arayüz)"})
        print(f"{paket}: {no} satır, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt "
              f"(IG_UI_lua; zaten IG_UI/IG_UI_lua'da, bekleyen ya da tekrar: {haric})")
    else:
        sys.exit("tur: diyalog | arayuz")

# --- Y3: IG_UI'de kalan diyalog nitelikli metinler (rapor/arayuz_siniflar_1.5.0.json, araclar/arayuz_sinif.py) ---
Y3_ACIKLAMA = ("# ARAYÜZDEN GELEN DİYALOG: Bunlar menü yazısı değil, bir karakterin söylediği ya da yazdığı sözler; Y1/Y2 gibi sahnede kurulur. "
               "Etiket kim konuşuyor: OYUNCU (oyuncunun karakteri, birinci tekil, kısa), NPC (cevap/uyarı), NOT (yazılı not). "
               "{yer_tutucu} aynen kalır ({where} yer, {place} yer adı, {faction} grup, {name} kişi, {day} gün, {dist}/{dir} adım/yön). "
               "Aynı blokta alt alta duran satırlar aynı sözün başka söylenişleri ya da aynı notun satırlarıdır; hepsini ayrı ayrı çevir.")
Y3_ALAN = {"ask": "OYUNCU SORUSU", "report": "OYUNCU RAPORU", "text": "OYUNCU SEÇENEĞİ", "var": "OYUNCU SEÇENEĞİ (başka söylenişi)",
           "ui": "OYUNCU SEÇENEĞİ"}
Y3_DOSYA = {
    "ALifeTaskBoardData": ("GÖREV PANOSU", "oyuncu NPC'ye iş sorar (SORU) ve işi bitirince ona haber verir (RAPOR); görev başlığı/özeti çevrilmez"),
    "ALifeTaskBoardText": ("GÖREV PANOSU · ZORLUK/HATIRLATMA", "oyuncu görevi nasıl yapacağını seçer (temkinli ya da sert) ve verilmiş işi sorar"),
    "ALifeTaskTalk": ("GÖREV TEKLİFİ", "oyuncu NPC'ye iş ya da nöbet bulup bulmadığını sorar"),
    "ALifeFactionTalkData": ("GRUP KONUŞMASI", "oyuncu bir gruptan biriyle konuşurken menüden bu soruları seçer"),
    "ALifeTalk6": ("KONUŞMA · TAKİP SORULARI", "oyuncu bir NPC'ye, önceki cevabının ardından devam sorusu sorar"),
    "ALifeTalkGeneral": ("KONUŞMA · GENEL SORULAR", "oyuncu bir NPC'ye sohbet sorusu sorar; ayrı satırlar aynı sorunun başka söylenişleri"),
    "ALifeTalkIntents": ("KONUŞMA · KAPI VE KARŞILAŞMA CEVAPLARI", "kapıdaki ya da yolda karşılaştığı biri soru sorunca oyuncunun verdiği cevaplar"),
    "ALifeTalk3React": ("KONUŞMA · DURUMA GÖRE", "oyuncu kendi durumundan (yaralı, hekim, öldürdükleri) söz eder"),
    "ALifeCars2Talk": ("ARAÇ KONUŞMASI", "oyuncu bir NPC'den araç için yakıt, akü, tamir ister ya da kendi yakıtını verir"),
    "ALifeFactionTalk": ("KARŞILAŞMA CEVAPLARI", "silahlı bir grupla karşılaşmada oyuncunun cevapları (sabıkalı, polis, yardım)"),
    "ALifeRadioTalk": ("RADYO SORUSU", "oyuncu NPC'ye telsizde duyduklarını sorar"),
    "ALifeUI2TalkStyle": ("MESLEK SÖZLERİ", "oyuncunun mesleğine göre kendini tanıtması (hekim, aşçı, eski asker…)"),
    "ALifeAnswerChannel": ("KAPI CEVAPLARI", "oyuncu kapıdaki ya da yoldaki birine kısa cevap verir"),
    "ALifeEndingCallData": ("BİTİŞ · TELSİZ ÇAĞRISI", "oyuncu bitiş görevinin telsiz çağrısında karşı tarafa seslenir"),
    "ALifeEndingVerdict": ("BİTİŞ · HESAPLAŞMA", "oyuncunun son sorusu; cümle kalıbı aynı"),
    "ALifeNoveltyMoodData": ("HAVA VE RUH HÂLİ", "yakındaki NPC, hava ya da hâle göre (yağmur, soğuk, gün doğumu…) oyuncuya kendiliğinden tek cümle söyler"),
    "ALifeNoveltyRumorsData": ("SÖYLENTİ", "NPC bir grubun başına gelen olayı söylenti olarak anlatır; {where} yer, {faction} grup adı"),
    "ALifeNoveltyLostData": ("KAYIP EŞYA", "kayıp eşyasını arayan NPC oyuncudan bulmasını ister; bulunca teşekkür eder; {thing} eşya, {where} yer"),
    "ALifeWorldHunt": ("ARANIYORSUN HABERİ", "birinin oyuncuyu aradığı yolda duyulan söylenti olarak oyuncuya iletilir; {faction} grup adı"),
    "ALifeScout": ("GÖZCÜ HABERİ", "gözcü telsizden yakındaki bir yeri haber verir; {place} yer, {dist} adım, {dir} yön"),
    "ALifeNoveltyNotesData": ("EL YAZISI NOT", "oyuncunun bir yerde bulup okuduğu, ölen ya da giden birinin yazdığı not; aynı kutudaki satırlar tek bir not"),
    "ALifeNoveltyMemorialsData": ("ANIT YAZISI", "ölen birinin mezarına/işaretine kazınmış kısa yazı; {day} gün sayısı"),
}


def _ust_anahtar(rel, no):
    """Bir liste satırının ait olduğu tablo alanı (ör. rain = {): hava/ruh hâli gibi koşul adı."""
    yol = diyalog_cikar.LUA_KOK / rel
    try:
        satirlar = yol.read_text(encoding="utf-8", errors="ignore").split("\n")
    except OSError:
        return ""
    for i in range(no - 2, max(-1, no - 60), -1):
        m = re.match(r"^\s*(\w+)\s*=\s*\{\s*$", satirlar[i])
        if m:
            return m.group(1)
    return ""


def hazirla_arayuz_diyalog(paket, parca=128):
    """IG_UI'de kalan diyalog nitelikli (a sınıfı) metinler -> IG_UI anahtarlı Gemini girdisi (Y3)."""
    yol = KOK / "rapor" / "arayuz_siniflar_1.5.0.json"
    if not yol.exists():
        sys.exit("önce: python -X utf8 araclar/arayuz_sinif.py")
    siniflar = oku(yol)
    baska = bekleyen(paket)
    gerek = {k for k, v in oku(KOK / "rapor" / "arayuz_1.5.0_IG_UI.json").items() if v["tur"] == "yeni"}
    gruplar, gorulen = {}, set()
    for k, v in siniflar.items():
        if v["sinif"] != "a" or k not in gerek or k in baska or k in gorulen:
            continue
        gorulen.add(k)
        dosya = (v["satir"] or "?:0").split(":")[0]
        ad = dosya.rsplit("/", 1)[-1].replace(".lua", "") if v["satir"] else "?"
        if ad.startswith("ALifeTrees_") or ad.startswith("ALifeDialogue_"):
            ad = "ALifeTalkGeneral"  # ağaç/diyalog dosyalarından düşen tek tük sözler: genel konuşma
        no = int((v["satir"] or "?:0").split(":")[1])
        gruplar.setdefault(ad, []).append((no, k, v, dosya))
    bloklar = []
    for ad, liste in sorted(gruplar.items(), key=lambda x: list(Y3_DOSYA).index(x[0]) if x[0] in Y3_DOSYA else 99):
        baslik, nerede = Y3_DOSYA.get(ad, ("DİĞER", "oyunda bir karakterin söylediği söz"))
        liste.sort(key=lambda x: (x[0], {"text": 0, "ask": 0, "var": 1, "report": 2}.get(x[2]["alan"], 3), x[1]))
        alt_ad = liste[0][2]["alt"]
        alt_alt = {}
        for no, k, v, dosya in liste:
            if ad in ("ALifeNoveltyNotesData", "ALifeNoveltyMemorialsData"):
                anahtar = (dosya, no)  # aynı Lua satırı = aynı not
            else:
                anahtar = (_ust_anahtar(dosya, no) if v["alan"] == "liste" and v["satir"] else "", 0)
            alt_alt.setdefault(anahtar, []).append((no, k, v, dosya))
        notlar = ad in ("ALifeNoveltyNotesData", "ALifeNoveltyMemorialsData")
        for (kosul, _), satir_listesi in alt_alt.items():
            ust = [f"##### {baslik}" + (f" · {kosul}" if kosul and not isinstance(kosul, tuple) and not notlar else "") + " #####",
                   "# NEREDE: " + nerede]
            satirlar = []
            for no, k, v, dosya in satir_listesi:
                if v["alt"] == "yazili_not":
                    etiket = "NOT"
                elif v["alt"] == "npc_soz":
                    etiket = "NPC"
                else:
                    etiket = Y3_ALAN.get(v["alan"], "OYUNCU SEÇENEĞİ")
                satirlar.append((k, v["en"], etiket, [ad + ".lua", v["alan"] or "?", etiket]))
            bloklar.append((ust, satirlar))
    # küçük blokları aynı dosya adından arka arkaya koy (sıra korunur); büyüklük sınırı _bloklari_yaz'da
    no, dosya = _bloklari_yaz(paket, bloklar, parca, [Y3_ACIKLAMA],
                              {"_grup": "arayuz_diyalog", "_dosya": "IG_UI", "_baslik": "1.5.0 arayüzden gelen diyalog nitelikli metinler"})
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt (IG_UI)")


# --- Y6: kaçan metinlerin diyalog grubu (kaynak/IG_UI_kacan.json, araclar/kacan_cikar.py, rapor/kacan_ek_1.5.0.md) ---
Y6_ACIKLAMA = ("# KONUŞMA SATIRLARI VE ALT NOTLARI: Konuşma penceresinde oyuncunun seçtiği satırlar (OYUNCU SEÇENEĞİ: oyuncunun kendi ağzından, "
               "birinci tekil, kısa, sonda nokta yok) ve fare üstündeyken satırın altında çıkan kısa notlar (ALT NOT: seçimin sonucu, riski ya da "
               "ipucu; kısa açıklama, sonda nokta yok, oyuncuya 'sen' diye değil durumu anlatarak). NPC (soru) satırı karşıdakinin sorduğu "
               "soru, cümle noktalamasıyla. '·' ile başlayan satırlar bağlam (NPC'nin o sahnede söyledikleri): çıktıya yazılmaz.")
Y6_ETIKET = {"text": "OYUNCU SEÇENEĞİ", "label": "OYUNCU SEÇENEĞİ", "impact": "ALT NOT (sonuç)", "risk": "ALT NOT (risk)",
             "tip": "ALT NOT (ipucu)", "ask": "NPC (soru)"}
Y6_GRUP = {
    "durum_satiri": ("DURUM", "oyuncu kuşatılmış, yolu kesmiş ya da işi başından aşkın bir grupla karşılaşır ve konuşma penceresinden "
                     "bu satırları seçer; alt not seçimin sonucunu/riskini söyler"),
    "durum_sorusu": ("DURUMA GÖRE SORU", "oyuncu hava, gece, yara ya da karşısındakine göre NPC'ye soru sorar; alt not ne öğreneceğini söyler"),
    "esir_satiri": ("ESİR", "oyuncu elindeki esirle konuşur: yedirir, sorgular, bırakır, teslim eder ya da öldürür; alt not sonucu söyler"),
    "gorev_satiri": ("GÖREV · DELL'İN ÇANTALARI (Left Behind)", "Dell Tolliver adamlarının bıraktığı çantaları geri ister; sonra Wade'in "
                     "adamları oyuncunun yolunu keser. Satırlar oyuncunun Dell'e ve Wade'e söyledikleri; alt not satırın üstüne gelince çıkar"),
    "bitis_cagri": ("BİTİŞ · TELSİZ ÇAĞRISI", "bitiş görevinde ordu telsizden oyuncuya ulaşır; oyuncu karşılık seçer"),
    "bitis_soru": ("BİTİŞ · HELİKOPTERDE", "kurtarma helikopterinde pilot oyuncuya üç soru sorar; oyuncu dört cevaptan birini seçer"),
}


def hazirla_kacan(paket, parca=128):
    """Kaçan metinlerin diyalog grubu -> IG_UI_lua anahtarlı Gemini girdisi (Y6). Önce: python -X utf8 araclar/kacan_cikar.py."""
    import kacan_cikar
    from lupa.lua51 import LuaRuntime
    yol = KOK / "kaynak" / "IG_UI_kacan.json"
    if not yol.exists():
        sys.exit("önce: python -X utf8 araclar/kacan_cikar.py")
    kaynak, baglam = oku(yol), oku(KOK / "kaynak" / "IG_UI_kacan_baglam.json")
    baska = bekleyen(paket)
    alinacak = {k for k, v in baglam.items() if v[3] == "diyalog" and k not in baska}
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("require = function() end; ProjectALife = {}")
    for ad in ("shared/ProjectALife/Situations/ALifeSituationsData.lua", "shared/ProjectALife/Ending/ALifeEndingCallData.lua",
               "shared/ProjectALife/Ending/ALifeEndingData.lua"):
        lua.execute((kacan_cikar.MOD / ad).read_text(encoding="utf-8-sig"))
    P = lua.globals().ProjectALife

    def liste(t):
        return [] if t is None else [t[i] for i in range(1, len(t) + 1)]

    yazilan = set()

    def satir(en, alan):
        k = kacan_cikar.anahtar(en) if isinstance(en, str) else None
        if k not in alinacak or k in yazilan:
            return None
        yazilan.add(k)
        b = baglam[k]
        return (k, en, Y6_ETIKET[alan], [b[0].rsplit("/", 1)[-1], alan, Y6_ETIKET[alan]])

    def ust(grup, alt=""):
        baslik, nerede = Y6_GRUP[grup]
        return [f"##### {baslik}" + (f" · {alt}" if alt else "") + " #####", "# NEREDE: " + nerede]

    bloklar = []
    for sit in liste(P.SituationsData.situations):  # durum başına bir blok; NPC'nin girişte ve cevapta söyledikleri bağlam
        satirlar = [("·", "NPC (karşılaşınca)", s) for s in liste(sit.lines.enter)[:2]] if sit.lines else []
        for r in liste(sit.rows):
            for alan in ("text", "impact", "risk"):
                x = satir(r[alan], alan)
                if x:
                    satirlar.append(x)
            if sit.lines and sit.lines[r.key]:
                satirlar += [("·", "NPC (cevap)", s) for s in liste(sit.lines[r.key])[:1]]
        if any(x[0] != "·" for x in satirlar):
            bloklar.append((ust("durum_satiri", str(sit.label)), satirlar))
    for grup in ("durum_sorusu", "esir_satiri", "gorev_satiri"):
        satirlar = [x for x in (satir(kaynak[k], v[1]) for k, v in baglam.items() if v[2] == grup) if x]
        if satirlar:
            bloklar.append((ust(grup), satirlar))
    for ad, dugum in P.EndingCallData.nodes.items():  # telsiz çağrısı: düğüm başına, ordunun sözü bağlam
        satirlar = [("·", "TELSİZ (ordu)", s) for s in liste(dugum.lines)]
        for o in liste(dugum.opts):
            x = satir(o.label, "label")
            if x:
                satirlar.append(x)
        if any(x[0] != "·" for x in satirlar):
            bloklar.append((ust("bitis_cagri", str(ad)), satirlar))
    satirlar = []
    for b in liste(P.EndingData.talk.beats):
        x = satir(b.ask, "ask")
        satirlar += [x] if x else [("·", "NPC (soru)", b.ask)]
        for o in liste(b.options):
            x = satir(o.label, "label")
            if x:
                satirlar += [x, ("·", "NPC (cevap)", o.reply)]
    if any(x[0] != "·" for x in satirlar):
        bloklar.append((ust("bitis_soru"), satirlar))
    eksik = alinacak - yazilan
    if eksik:
        sys.exit(f"{paket}: {len(eksik)} satır bloklara girmedi: {sorted(kaynak[k] for k in eksik)[:5]}")
    no, dosya = _bloklari_yaz(paket, bloklar, parca, [Y6_ACIKLAMA],
                              {"_grup": "kacan_diyalog", "_dosya": "IG_UI_lua", "_noktalama_haric": ["OYUNCU", "ALT NOT"],
                               "_baslik": "1.5.0 kaçan metinler: konuşma satırları ve alt notları"})
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt "
          f"(IG_UI_lua; bekleyen başka haritada olduğu için alınmayan {len({k for k, v in baglam.items() if v[3] == 'diyalog'} - alinacak)})")


# --- Y7: tablo içi listelerdeki NPC sözleri (araclar/liste_cikar.py, rapor/kacan_listeler_1.5.0.md) ---
Y7_ACIKLAMA = ("# NPC SÖZLERİ: Etiketi NPC, ESİR, TELSİZ ya da PİLOT olan her satır bir karakterin ağzından konuşma, cümle noktalamasıyla. "
               "'·' ile başlayan satırlar bağlam (oyuncunun seçtiği satır ya da zaten çevrilmiş söz): çıktıya yazılmaz.")


def hazirla_liste_soz(paket, parca=128):
    """Durum/esir sözleri ve telsiz çağrısı soruları -> RadioData_lua anahtarlı Gemini girdisi (Y7)."""
    import liste_cikar
    bilinen = liste_cikar.bilinen() | bekleyen(paket)
    bloklar = liste_cikar.y7_bloklari(bilinen)
    no, dosya = _bloklari_yaz(paket, bloklar, parca, [Y7_ACIKLAMA],
                              {"_grup": "liste_soz", "_dosya": "RadioData_lua",
                               "_baslik": "1.5.0 tablo içi listelerdeki NPC sözleri (durum, esir, telsiz çağrısı)"})
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt "
          f"(RadioData_lua); harita rapor/{paket}_harita.json")



# --- E: oyunda İngilizce kalan NPC sözleri (araclar/ceviri_bosluk_1.py + _2.py, rapor/ceviri_bosluk_tara2.json) ---
E_ACIKLAMA = ("# EKSİK SÖZLER: Bunlar oyunda şimdiye dek hiç çevrilmemiş, İngilizce kalan NPC sözleridir. Her numaralı satır bir karakterin ağzından "
              "çıkan söz ya da uzun bir sözün devam parçasıdır (küçük harfle başlayan satır, önceki sözün devamıdır). '· ' satırları bağlamdır: "
              "çıktıya yazılmaz. Her satırı o anda o yerde söylenecek konuşma Türkçesi olarak yaz.")


def hazirla_bosluk(paket, parca=128):
    """Oyunda İngilizce kalan, Lua'da satır listesi/ek cümle olarak gömülü NPC sözlerini RadioData_lua anahtarlı Gemini girdisine çevirir."""
    import re as _re
    from lua_cikar import MOD
    from lua_dize import dizeler
    tara = KOK / "rapor" / "ceviri_bosluk_tara2.json"
    if not tara.exists():
        sys.exit("önce: python -X utf8 araclar/ceviri_bosluk_1.py ; python -X utf8 araclar/ceviri_bosluk_2.py")
    bilinen = set(oku(KAYNAK)) | bekleyen(paket)

    def gorunur(rel):
        n = rel.rsplit("/", 1)[-1]
        if any(x in n for x in ("Registry", "Validat", "Debug", "Test", "Lint")):  # geliştirici doğrulama iletileri, ekranda görünmez
            return False
        if "Talk/Data/ALifeDialogue_" in rel:
            return not any(x in n for x in ("_radio_", "_intents_"))
        if rel.startswith("shared/ProjectALife/Talk/Trees/") or "Trees" in n:
            return True
        if rel.startswith("shared/ProjectALife/Talk/") and "/" not in rel[len("shared/ProjectALife/Talk/"):]:
            return not any(x in n for x in ("Intents", "Server", "Checks", "Guard", "Roles", "Contacts", "Drift", "Hook", "Gesture.lua"))
        return n in ("ALifeFollowBLines.lua",)

    satirlar_dosya = {}
    for rel, no, t in oku(tara):
        if gorunur(rel) and t == t.strip():  # baş/son boşluklu parçalar birleştirilen iç iletilerdir
            satirlar_dosya.setdefault(rel, []).append((no, t))
    gorulen, bloklar, atlanan = set(), [], 0
    for rel in sorted(satirlar_dosya):
        kaynak_metin = (MOD / rel).read_text(encoding="utf-8", errors="replace").split(chr(10))
        ad = rel.rsplit("/", 1)[-1]
        veri = "Talk/Data/" in rel
        # satır numarasına göre grupla: Data'da satır = bir kayıt; diğerlerinde en yakın üst tablo adları
        gruplar = {}
        for no, t in satirlar_dosya[rel]:
            if veri:
                kayit = kaynak_metin[no - 1]
                strs = [x for _, x in dizeler(kayit)]
                olay = strs[0] if strs else ""
                kosul = strs[1] if len(strs) > 1 else ""
                anahtar = (no, f"{olay} · {kosul}" if kosul else olay)
            else:
                yol, girinti = [], len(kaynak_metin[no - 1]) - len(kaynak_metin[no - 1].lstrip())
                for j in range(no - 2, -1, -1):
                    m = _re.match(r'^(\s*)\[?"?([A-Za-z_][\w ]*)"?\]?\s*=\s*\{', kaynak_metin[j])
                    if m and len(m.group(1)) < girinti:
                        yol.insert(0, m.group(2))
                        girinti = len(m.group(1))
                        if girinti == 0 or len(yol) >= 3:
                            break
                anahtar = (0, " > ".join(yol) or ad)
            gruplar.setdefault(anahtar, []).append((no, t))
        for (kno, baslik), liste in sorted(gruplar.items()):
            satir = []
            if veri:
                ilk = [x for _, x in dizeler(kaynak_metin[kno - 1])]
                ana = next((x for x in ilk[2:] if len(x) > 3 and "|" not in x and "=" not in x and ("RD_ALifeLine_" + h(diyalog_cikar.goster(x))) in bilinen), None)
                if ana:
                    satir.append(("·", "NPC (ana söz, çevrili)", ana))
            for no, t in liste:
                k = "RD_ALifeLine_" + h(diyalog_cikar.goster(t))
                if k in bilinen or k in gorulen:
                    atlanan += 1
                    continue
                gorulen.add(k)
                satir.append((k, t, "NPC", [ad, baslik, "NPC"]))
            if any(x[0] not in ("#", "·") for x in satir):
                nerede_m = nerede(ad) if veri else "Dünyada ya da konuşma kutusunda NPC'nin ağzından çıkan söz; oyuncu kısa bir an görür."
                bloklar.append(([f"##### {ad} · {baslik} #####"] + (["# NEREDE: " + nerede_m] if nerede_m else []), satir))
    no, dosya = _bloklari_yaz(paket, bloklar, parca, [E_ACIKLAMA],
                              {"_grup": "bosluk_soz", "_dosya": "RadioData_lua",
                               "_baslik": "Oyunda İngilizce kalan NPC sözleri (liste ve ek cümleler)"}, yeni=False)
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt "
          f"(RadioData_lua); atlanan (zaten var/tekrar) {atlanan}")



def hazirla_bitis_soz(paket, parca=128):
    """Telsiz kartı + pilot sözleri -> RadioData_lua anahtarlı Gemini girdisi (Y9)."""
    import liste_cikar
    bilinen = liste_cikar.bilinen() | bekleyen(paket)
    bloklar = liste_cikar.y9_bloklari(bilinen)
    no, dosya = _bloklari_yaz(paket, bloklar, parca, [Y7_ACIKLAMA],
                              {"_grup": "bitis_soz", "_dosya": "RadioData_lua",
                               "_baslik": "1.5.0 bitiş: telsiz kartı ve helikopter pilotunun sözleri"})
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt "
          f"(RadioData_lua); harita rapor/{paket}_harita.json")

# --- Y8 ve Y10-Y15: arayüz ve baskın/bitiş girdileri (K53: B10-B14 Gemini'de; rapor/B_paket_plani_1.5.0.md) ---
ARAYUZ_PLAN = {  # plan adı -> (hedef dosya, başlık)
    "B10": ("IG_UI", "1.5.0 yoldaş sayfası ve harita ipuçları"),
    "B11": ("IG_UI", "1.5.0 ilan panosu, radyo ve dünya olayı bildirimleri"),
    "B12a": ("IG_UI", "1.5.0 Oluşturucu ekranı ve ayar ipuçları (IG_UI)"),
    "B12b": ("Creator_lua", "1.5.0 Oluşturucu sabit yazıları (Creator_lua)"),
    "B13": ("IG_UI", "1.5.0 itibar, başlangıç, günlük, sürüş, bitiş ekranı ve jenerik"),
    "B14": ("IG_UI_lua", "1.5.0 kaçan metinlerin arayüz grubu (ayarlar, görev aşamaları, emir çarkı)"),
    "B16": ("IG_UI_lua", "1.5.1 yönetici ve geliştirici arayüzü (anahtarsız çizilen metinler; çeviri için ek kodu gerekir)"),
}
GOZCU_DOSYALARI = ("ALifeRaidText", "ALifeEndingStory", "ALifeEndingVerdict", "ALifeEndingPolish")
GOZCU_EK = ("The army took you into custody", "Your file stayed on a desk")  # veri kaynaklı iki bitiş anlatısı satırı (dosyası belirsiz)
B14_NEREDE = {
    "ayar": ("GÜNLÜK · AYARLAR", "Günlük > Ayarlar ekranı: konuşma penceresi, altyazı, görev izleyici, ok, jenerik hızı ve yayıncı modu satırları; satırın adı, değerlerinin adı (Old cinematic, Bottom right…) ve fareyle çıkan ipucu"),
    "ayar_grubu": ("GÜNLÜK · AYAR GRUPLARI", "Aynı ekranın grup başlıkları (Text and motion, Subtitles, Tasks and popups, Intro)"),
    "gorev_asamasi": ("GÜNLÜK · GÖREV AŞAMALARI (Left Behind)", "Dell'in çanta görevinin günlükteki aşama başlığı ve alt açıklaması"),
    "gorev_cipi": ("KONUŞMA · GÖREV ETİKETİ", "Aynı görevin konuşma satırlarındaki küçük etiket (Reward, Comply, Fight)"),
    "arkadas_carki": ("EMİR ÇARKI · ALT MENÜLER", "Grup emir çarkının alt menüleri"),
}
ARAYUZ_KURALLARI = [
    "# ARAYÜZ DOSYASI: Bu satırlar konuşma değil, EKRAN METNİ: düğme, ayar, ipucu, bildirim, etiket. Sahne ya da karakter canlandırma yok; kısa, net ve tutarlı yaz.",
    "# BİÇİM: Etiketlerde emir ya da isim biçimi kullan ('Kaydet', 'Teçhizat'). 'siz' hitabı yok, '-dır' yok; ipucu ve açıklamada gerekirse 'sen'. Sonda nokta İngilizcedeki gibi: İngilizcede yoksa yazma, varsa koru.",
    "# KORUNACAKLAR: {yer_tutucu}, %%, %1, \\n ve <...> etiketleri ile renk kodları aynen kalır. Kısaltmalar (HP, NPC, GM, MHz…) ve özel adlar (kişi, grup, yer, silah adı) çevrilmez. Sayıları ve birimleri koru.",
    "# UZUNLUK: Türkçe İngilizceden belirgin uzun olmasın; düğmelerde ve sekme adlarında en fazla yaklaşık 1,3 katı. Sığmıyorsa kısalt, anlamı koru.",
    "# BÜYÜK HARF: İngilizcede BÜYÜK HARFLİ yazılmış etiket Türkçede de büyük harfli olur (İ/ı kurallarıyla).",
    "# EKRAN: Her ##### başlığının altındaki 'EKRAN:' notu metnin hangi ekranda ya da panelde göründüğünü söyler; önce onu oku. Etiket sütunu kodda alanın adıdır (ui, tip, label…), çıktıya yazma.",
]
Y8_ACIKLAMA = ("# BASKIN KARTI VE BİTİŞ ANLATISI: GÖZCÜ satırları baskın kartında çıkan kısa gözcü cümleleridir: bir gözcü, uzaktan ya da yakından baskını "
               "haber veriyor (ses: baskıncı çete, asker, kolluk, silahlı yerel halk; taşıt: yaya, araç, helikopter). Her başlık TEK bir aşamanın "
               "birbirinin alternatifi sözleridir, oyunda biri rastgele seçilir; her satırı tek başına, kartta bir bakışta okunacak kısa uyarı olarak kur "
               "ve ses grubuna uydur. KART satırları kartın büyük harfli başlık/şerit etiketleri ve yön, uzaklık, grup büyüklüğü, süre ifadeleridir. "
               "ANLATI satırları oyun sonunda ekranda sırayla akan bitiş anlatısıdır (ANLATI BAŞLIĞI büyük harfli bölüm başlığı); aynı başlık altındaki "
               "satırlar ardışık okunan tek bir hikâyedir, 'sen' = oyuncu, geçmiş zaman, edebî ama sade. Sonda noktayı İngilizcedeki gibi bırak "
               "(gözcü cümlelerinde nokta yok). {yer_tutucu} ve sayılar aynen kalır.")
RAID_FAZ = {"warning": "uyarı: baskın yola çıktı, saatler var", "near": "yaklaşıyor", "arrived": "geldi", "assault": "saldırı sürüyor",
            "breach": "kapıyı kırmaya çalışıyorlar", "holding": "mevzide bekliyorlar", "retreat": "geri çekiliyorlar", "aftermath": "baskın bitti"}
RAID_SES = {"raider": "baskıncı çete", "military": "asker birliği", "law": "kolluk (polis, SWAT)", "other": "silahlı yerel halk"}
RAID_TASIT = {"foot": "yaya", "car": "araçla", "heli": "helikopterle"}
RAID_ALAN_GRUP = {"close": "distance", "mid": "distance", "far": "distance", "handful": "sizes", "crew": "sizes", "warband": "sizes",
                  "unknown": "unknown"}
RAID_KART = {
    "diger": "Baskın kartındaki öteki kısa ifadeler ({dir} yön, {dist} uzaklık yer tutucuları ve dalga sayacı)",
    "tags": "Baskın kartının büyük harfli üst etiketi (aşamayı söyler)", "strip": "Kartın alt şeridindeki büyük harfli aşama etiketi",
    "plain": "Baskın kartının sade, tek cümlelik uyarısı (gözcü sesi olmadan)", "compass": "Kartta baskının geldiği yön",
    "distance": "Kartta baskının uzaklığını söyleyen kısa ifade", "sizes": "Kartta baskıncı grubunun büyüklüğünü söyleyen kısa ifade",
    "etas": "Kartta baskının ne zaman geleceğini söyleyen kısa ifade", "unknown": "Baskıncının adı bilinmiyorsa adın yerine kullanılan ifade",
}
BITIS_NOT = {
    "ALifeEndingStory": ("BİTİŞ ANLATISI", "Oyun sonunda ekranda sırayla akan bitiş hikâyesi; BAŞLIK büyük harfli bölüm adı, altındaki satırlar hikâyenin ardışık cümleleri"),
    "ALifeEndingPolish": ("BİTİŞ ANLATISI · KISA SÜRÜM", "Bitiş hikâyesinin kısa anlatımı: aynı bitişin ardışık cümleleri"),
    "?": ("BİTİŞ ANLATISI · ORDU GÖZALTI", "Bitiş anlatısında ordunun oyuncuyu gözaltına aldığı sonun iki ardışık cümlesi (veri dosyasından, kaynağı belirsiz)"),
    "ALifeEndingVerdict": ("BİTİŞ · HESAPLAŞMA SATIRLARI", "Bitişte oyuncuya yaşananları alt alta sayan kısa anlatı satırları; {zombies}, {humans}, {rep} yer tutucuları sayı ya da ifadeyle dolar"),
}


def _lua_yolu(rel, no):
    """Bir dizgenin içinde durduğu iç içe tabloların anahtarları (dıştan içe): ['lines', 'near', 'raider', 'foot']."""
    try:
        sat = (diyalog_cikar.LUA_KOK / rel).read_text(encoding="utf-8", errors="ignore").split("\n")
    except OSError:
        return []
    if not 0 < no <= len(sat):
        return []
    girinti = lambda s: len(s) - len(s.lstrip())
    yol, cur = [], girinti(sat[no - 1])
    m = re.search(r'([\w.]+)\s*=\s*\{\s*"', sat[no - 1])
    if m:
        yol.append(m.group(1).split(".")[-1])
    for j in range(no - 2, max(-1, no - 90), -1):
        satir = sat[j]
        if not satir.strip() or girinti(satir) >= cur:
            continue
        m = re.match(r'\s*(?:local\s+)?([\w.]+)\s*=\s*\{[^}]*$', satir)
        if m:
            yol.append(m.group(1).split(".")[-1])
            cur = girinti(satir)
            if cur == 0:
                break
    return yol[::-1]


def _plan_girdileri():
    """Plan listeleri + sınıf bilgisi: (plan, siniflar, {anahtar: giriş}) ; giriş = {k, en, rel, dosya, alan, no, konu}."""
    plan = oku(KOK / "rapor" / "B_paket_plani_1.5.0.json")
    sin = oku(KOK / "rapor" / "arayuz_siniflar_1.5.0.json")
    girdiler = {}
    for k, v in sin.items():
        rel = v["dosya"] or "?"
        girdiler[k] = {"k": k, "en": v["en"], "rel": rel, "dosya": rel.rsplit("/", 1)[-1].replace(".lua", ""), "alan": v["alan"],
                       "no": int(v["satir"].split(":")[1]) if v["satir"] else 0, "konu": v["konu"]}
    return plan, sin, girdiler


def _gozcu_anahtarlari(plan, girdiler):
    out = []
    for b in ("B11", "B12", "B13"):
        for k in plan[b]["anahtar"]:
            g = girdiler[k]
            if g["dosya"] in GOZCU_DOSYALARI or g["en"].startswith(GOZCU_EK):
                out.append(k)
    return out


ITIBAR_EKRAN = [  # (Lua dosyası, başlık, EKRAN notu) — K57: itibar ekranının baştan çevirisi
    ("ALifeRepLevels", "İTİBAR SEVİYELERİ", "Kişisel itibar seviyelerinin adları (The Villain … The Legend; oyuncunun lakabı gibi okunur: 'Artık X olarak tanınıyorsun') ve her seviyenin altında çıkan bir iki cümlelik açıklama (insanlar sana nasıl davranıyor)"),
    ("ALifeRepScreen", "İTİBAR EKRANI · ÖZET", "Karakter ekranındaki itibar özeti: seviye adı, 'Reputation:' / 'Humans Killed:' etiketleri, takip kapalı ya da sunucu bekleniyor durumu"),
    ("ALifeUI2RepBar", "İTİBAR ÇUBUĞU", "İtibar sekmesinin üstündeki çubuk: başlık etiketleri (BÜYÜK HARF), puan, seviye ve ne anlama geldiği"),
    ("ALifeUI2RepBar2", "İTİBAR ÇUBUĞU · SON DEĞİŞİKLİK", "Çubuğun ikinci sürümü: İTİBARIN başlığı, son değişiklik satırı"),
    ("ALifeUI2RepProgress", "İTİBAR İLERLEMESİ", "Seviye ilerleme şeridi ({day} gün, {level} seviye, {amount} puan; 'You {reason}' satırında {reason} eylem kaydının küçük harfli geçmiş zaman hâlidir)"),
    ("ALifeUI2RepTab", "İTİBAR SEKMESİ", "Günlüğün İtibar sekmesi: fraksiyon listesi, seviye listesi, 'itibar nasıl işler' açılır bölümü"),
    ("ALifeUI2RepTabModel", "İTİBAR SEKMESİ · EYLEM KAYITLARI VE KURALLAR", "İtibarını değiştiren eylemlerin kısa kayıtları (geçmiş zaman, 'sen' öznesi gizli: 'Killed a friend' → '… öldürdün'), fraksiyonun sana dönme nedenleri ve 'itibar nasıl işler' maddeleri"),
    ("ALifeRepTab", "İTİBAR SEKMESİ (ESKİ GÖRÜNÜM) · SON DEĞİŞİKLİKLER", "Eski görünümdeki itibar sekmesi: son değişiklikler listesi, seviye ipuçları, puan gizliyse yazısı"),
    ("ALifeRepView", "İTİBAR GÖRÜNÜMÜ · FRAKSİYONLARIN SANA BAKIŞI", "Fraksiyonların sana tavrını söyleyen satırlar ({who} grup adı, çoğul), seviye atlama ve düşme satırları, seviyenin sana getirdikleri"),
    ("ALifeRepNotify", "İTİBAR BİLDİRİMİ", "İtibar değişince ekranın köşesinde çıkan kısa bildirim ({amount} '+5' gibi işaretli sayı, {name} seviye adı)"),
    ("ALifeRepIcons", "İTİBAR · SİMGE İPUCU", "Eylem simgesinin üstüne gelince çıkan kısa açıklama (küçük harfle başlar, geçmiş zaman; 'You {reason}' kalıbının içine de girer)"),
    ("ALifeStanding", "FRAKSİYON DURUMU", "Bir fraksiyonla aranın durum adları"),
]


def hazirla_itibar(paket_ui="IT1", paket_lua="IT2"):
    """İtibar ekranının bütün metinleri (çevrilmiş olsalar da) baştan çeviri için: IG_UI anahtarları -> IT1, IG_UI_lua -> IT2 (K57)."""
    import arayuz_terimler
    from lua_cikar import h as lua_hash, MOD, STR, un
    ui, lua = oku(KOK / "onayli" / "IG_UI.json"), oku(KOK / "onayli" / "IG_UI_lua.json")
    en_ui, en_lua = oku(KOK / "kaynak" / "en" / "IG_UI.json"), oku(KOK / "kaynak" / "IG_UI_lua.json")
    dosyalar = {f.stem: f for f in MOD.rglob("*.lua")}
    gorulen, bloklar = set(), {paket_ui: [], paket_lua: []}
    for ad, bas, nerede in ITIBAR_EKRAN:
        metin = dosyalar[ad].read_text(encoding="utf-8")
        satirlar = {paket_ui: [], paket_lua: []}
        for m in re.finditer(STR, metin):
            k = "IGUI_ALifeUI_" + lua_hash(un(m.group(1)))
            ham = un(m.group(1))
            kod = re.fullmatch(r"[a-z_]+", ham) and not re.search(r"\b(?:ui|msg)\(\s*$", metin[max(0, m.start() - 12):m.start()])
            if k in gorulen or kod or re.search(r"\b(stance|id|cat|kind|ladderFrom)\s*=\s*$", metin[max(0, m.start() - 20):m.start()]):
                continue
            no = metin.count(chr(10), 0, m.start()) + 1
            if k in ui and k in en_ui:
                hedef, en = paket_ui, en_ui[k]
            elif k in lua and k in en_lua:
                hedef, en = paket_lua, en_lua[k]
            else:
                continue
            gorulen.add(k)
            satirlar[hedef].append((k, en, f"{ad}:{no}", [f"{dosyalar[ad].relative_to(MOD).as_posix()}:{no}"]))
        for hedef, liste in satirlar.items():
            if liste:
                bloklar[hedef].append(([f"##### {bas} #####", "# EKRAN: " + nerede], liste))
    maden = {}  # yalnız sözlük: madenden gelen kısa sözcükler (hold → Basılı tut gibi) bu ekranda yanıltıyor
    for paket, dosya in ((paket_ui, "IG_UI"), (paket_lua, "IG_UI_lua")):
        def aciklama(ens):
            liste = arayuz_terimler.dosya_terimleri(ens, maden)
            return ARAYUZ_KURALLARI + [
                "# BAŞTAN ÇEVİRİ: Bu metinler oyunda şu an eski bir çeviriyle duruyor; sen sıfırdan İngilizceden kur. Ekran metni ama oyuncuya "
                "konuşan bir ekran: kuru tutanak dili değil, bir Türk oyun yazarının yazacağı gibi doğal ve kısa yaz. Seviye adları ve açıklamaları "
                "oyuncunun lakabı ve ünü gibi okunsun.",
                "# TERİMLER (bağlayıcı; yalnız bu dosyada geçenler): " + "; ".join(f"{e} → {t}" for e, t in liste)]
        no, parca = _bloklari_yaz(paket, bloklar[paket], 400, aciklama,
                                  {"_grup": "arayuz_itibar", "_dosya": dosya, "_noktalama": False, "_bosluk_koru": True,
                                   "_baslik": "İtibar ekranı, baştan çeviri (K57)"}, yeni=False,
                                  kurallar="# Kurallar: alife-ceviri skill'i, ARAYÜZ bölümü. Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama.")
        print(f"{paket}: {no} satır, {len(bloklar[paket])} blok, {parca} parça ({dosya})")


def hazirla_creator(paket="CR1"):
    """Oluşturucu (Creator) cümleleri baştan çeviri için (ipucu, yardım, açıklama, uyarı; K57). Etiketler değişmez:
    cümlelerde geçen etiketler mevcut Türkçesiyle bağlayıcı TERİMLER olur. Başka ekranlarla ortak anahtar ve fraksiyon verisi alınmaz."""
    import arayuz_nerede
    en = oku(KOK / "kaynak" / "Creator_lua.json")
    tr = oku(KOK / "onayli" / "Creator_lua.json")
    baglam = oku(KOK / "kaynak" / "Creator_lua_baglam.json")
    ortak = set(oku(KOK / "onayli" / "IG_UI.json")) | set(oku(KOK / "onayli" / "IG_UI_lua.json"))
    dosyalar, etiketler = {}, []
    for k, v in en.items():
        yer = str((baglam.get(k) or ["?"])[0])
        if "faction_registry" in yer or k not in tr:
            continue
        if len(v.split()) <= 3 and len(v) >= 3 and not v.endswith(("...", ".", "!", "?")):
            etiketler.append((v, tr[k]))
        if not (len(v.split()) >= 6 or re.search(r"[.!?]$", v)) or k in ortak:
            continue
        ad, _, no = yer.partition(":")
        ad = ad.split("/")[-1].replace(".lua", "")
        dosyalar.setdefault(ad, []).append((int(no) if no.isdigit() else 0, k, v, yer))
    N = arayuz_nerede.NEREDE
    bloklar = []
    for ad in sorted(dosyalar, key=lambda a: (-len(dosyalar[a]), a)):
        bas, nerede, *_ = N.get(ad, ("OLUŞTURUCU · " + ad.replace("ALifeCreator", "").upper(), "Oluşturucu ekranı (" + ad + ")"))
        liste = sorted(dosyalar[ad])
        for i in range(0, len(liste), 40):
            parca_liste = liste[i:i + 40]
            alt = f" ({i // 40 + 1}/{-(-len(liste) // 40)})" if len(liste) > 40 else ""
            bloklar.append(([f"##### {bas}{alt} #####", "# EKRAN: " + nerede],
                            [(k, v, ad.replace("ALifeCreator", "") or "-", [yer]) for _, k, v, yer in parca_liste]))

    def aciklama(ens):
        metin = "\n".join(ens).lower()
        sec = sorted({(e, t) for e, t in etiketler if re.search(r"(?<![a-z])" + re.escape(e.lower()) + r"(?![a-z])", metin)},
                     key=lambda x: (-len(x[0]), x[0]))[:120]
        return ARAYUZ_KURALLARI + [
            "# BAŞTAN ÇEVİRİ: Bunlar A-Life Oluşturucu ekranının cümleleri (ipucu, yardım, açıklama, uyarı). Oyunda eski bir çeviriyle "
            "duruyorlar; sen sıfırdan İngilizceden kur. Düğme ve sekme adları DEĞİŞMİYOR: cümle bir düğmeyi, sekmeyi ya da ayarı adıyla "
            "anıyorsa aşağıdaki TERİMLER'deki Türkçe adı aynen kullan (oyuncu ekranda o adı görüyor). Bir Türk oyun yazarının yazacağı gibi "
            "doğal, kısa ve açık yaz; teknik tutanak dili değil.",
            "# TERİMLER (bağlayıcı; ekrandaki mevcut düğme/ayar adları): " + "; ".join(f"{e} → {t}" for e, t in sec)]

    no, parca = _bloklari_yaz(paket, bloklar, 150, aciklama,
                              {"_grup": "arayuz_creator", "_dosya": "Creator_lua", "_noktalama": False, "_bosluk_koru": True,
                               "_baslik": "Oluşturucu cümleleri, baştan çeviri (K57)"}, yeni=False,
                              kurallar="# Kurallar: alife-ceviri skill'i, ARAYÜZ bölümü. Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama.")
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {parca} parça (Creator_lua)")


def hazirla_baskin(paket, parca=150):
    """Baskın kartı (RaidText) gözcü cümleleri + bitiş anlatısı -> IG_UI anahtarlı Gemini girdisi (Y8, K38'in devamı)."""
    plan, _, girdiler = _plan_girdileri()
    baska, onayli = bekleyen(paket), oku(KOK / "onayli" / "IG_UI.json")
    gruplar = {}
    for k in _gozcu_anahtarlari(plan, girdiler):
        g = girdiler[k]
        if k in onayli or k in baska:
            continue
        yol = tuple(_lua_yolu(g["rel"], g["no"])) if g["no"] else ()
        if g["dosya"] == "ALifeRaidText" and not yol:  # tek satırlık tablolar (distance, sizes…): alan adından
            yol = (RAID_ALAN_GRUP.get(g["alan"], "diger"),)
        if g["dosya"] != "ALifeRaidText" and yol:  # bitiş: başlık ('stories' ya da 'endings' tablosu) ile cümleleri ('lines') aynı bloğa
            yol = (yol[-2] if yol[-1] == "lines" and len(yol) > 1 else yol[-1],)
        gruplar.setdefault((g["dosya"], yol), []).append(g)
    sira = {"ALifeRaidText": 0, "ALifeEndingStory": 1, "ALifeEndingPolish": 2, "ALifeEndingVerdict": 3}
    faz_sira = list(RAID_FAZ)

    def sirala(x):
        dosya, yol = x[0]
        satirli = len(yol) > 1 and yol[0] == "lines"
        return (sira.get(dosya, 9), satirli, faz_sira.index(yol[1]) if satirli and yol[1] in faz_sira else 99,
                list(RAID_SES).index(yol[2]) if satirli and len(yol) > 2 and yol[2] in RAID_SES else 9, yol)

    bloklar = []
    for (dosya, yol), liste in sorted(gruplar.items(), key=sirala):
        liste.sort(key=lambda g: (g["no"], g["k"]))
        if dosya == "ALifeRaidText":
            if yol and yol[0] == "lines" and len(yol) > 1:
                faz = RAID_FAZ.get(yol[1], yol[1])
                ses = RAID_SES.get(yol[2], yol[2]) if len(yol) > 2 else ""
                tasit = RAID_TASIT.get(yol[3], yol[3]) if len(yol) > 3 else ""
                baslik = "BASKIN KARTI · GÖZCÜ · " + faz + (f" · {ses}" if ses else "") + (f" · {tasit}" if tasit else "")
                nerede = ("Baskın kartında gözcünün kısa uyarı cümlesi" + (f"; konuşan: {ses}" if ses else "")
                          + (f"; baskın {tasit} geliyor" if tasit else "") + ". Bu bloktaki satırlar birbirinin alternatifi, oyunda biri rastgele seçilir")
                etiket = "GÖZCÜ"
            else:
                ad = yol[0] if yol else "?"
                baslik = f"BASKIN KARTI · KART ETİKETLERİ ({ad})"
                nerede = RAID_KART.get(ad, "Baskın kartındaki kısa etiket")
                etiket = "KART"
        else:
            b, nerede = BITIS_NOT[dosya]
            baslik = b + (f" · {yol[0]}" if yol else "")
            etiket = "ANLATI"
        satirlar = []
        for g in liste:
            e = "ANLATI BAŞLIĞI" if (dosya != "ALifeRaidText" and g["alan"] == "title") else etiket
            satirlar.append((g["k"], g["en"], e, [g["dosya"] + ".lua", g["alan"] or "?", e]))
        bloklar.append(([f"##### {baslik} #####", "# NEREDE: " + nerede], satirlar))
    if not bloklar:
        sys.exit(f"{paket}: baskın/bitiş anlatısı satırı yok")
    toplam = sum(len(b[1]) for b in bloklar)
    dosya_sayisi = max(1, -(-toplam // parca))
    no, dosya = _bloklari_yaz(paket, bloklar, -(-toplam // dosya_sayisi), [Y8_ACIKLAMA],
                              {"_grup": "baskin_bitis", "_dosya": "IG_UI", "_noktalama": False, "_bosluk_koru": True,
                               "_baslik": "1.5.0 baskın kartı gözcü cümleleri ve bitiş anlatısı"})
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt (IG_UI)")


def _arayuz_secimi(plan_adi):
    """Plan adına göre giriş listesi (süzülmemiş: dolu/bekleyen sonra) ; giriş: {k, en, dosya, alan, no, rel, konu[, yer, veri_sira]}."""
    plan, _, girdiler = _plan_girdileri()
    gozcu = set(_gozcu_anahtarlari(plan, girdiler))
    if plan_adi in ("B10", "B11", "B13"):
        return [girdiler[k] for k in plan[plan_adi]["anahtar"] if k not in gozcu]
    if plan_adi == "B12a":
        out, veri = [], 0
        for k in plan["B12"]["anahtar"]:
            g = girdiler[k]
            if g["rel"] == "?":
                veri += 1
                g = dict(g, veri_sira=veri)
            if k in gozcu:
                continue
            out.append(g)
        return out
    if plan_adi == "B12b":
        yeni = oku(KOK / "rapor" / "cikarici_yeni_1.5.0.json")["Creator_lua"]
        sec = set(plan["B12b"]["anahtar"])
        out = []
        for k, v in yeni.items():
            if k in sec:
                dosya, _, no = v["yer"][0].partition(":")
                ad = dosya.replace(".lua", "")
                if dosya.startswith("faction_registry"):  # .alife verisi: yer metninden tür (kart satırı, takım adı, dolap açıklaması)
                    ad = "faction_registry_" + ("about" if "about" in v["yer"][0] else "ad" if "fraksiyon kısmı" in v["yer"][0] else "aciklama")
                    no = "0"
                out.append({"k": k, "en": v["en"], "rel": dosya, "dosya": ad, "alan": None,
                            "no": int(no) if no.isdigit() else 0, "konu": "Oluşturucu", "yer": [v["yer"][0]]})
        return out
    if plan_adi == "B16":  # rapor/kacan_1.5.0.json (araclar/kacan_tara.py): yonetici_arayuzu, görünür; anahtar = IGUI_ALifeUI_ + hash
        out, gorulen = [], set()
        for a in oku(KOK / "rapor" / "kacan_1.5.0.json"):
            if a["kategori"] != "yonetici_arayuzu" or not a["gorunur"]:
                continue
            k = "IGUI_ALifeUI_" + h(a["en"])
            if k in gorulen:
                continue
            gorulen.add(k)
            rel, _, no = a["yer"][0].rpartition(":")
            ad = rel.rsplit("/", 1)[-1].replace(".lua", "")
            out.append({"k": k, "en": a["en"], "rel": rel, "dosya": ad, "alan": None, "no": int(no) if no.isdigit() else 0,
                        "konu": "yönetici/geliştirici paneli (oyuncu ekranı değil; kısa düğme, etiket, ipucu, durum yazısı)", "yer": [a["yer"][0]]})
        return out
    if plan_adi == "B14":
        kaynak, baglam = oku(KOK / "kaynak" / "IG_UI_kacan.json"), oku(KOK / "kaynak" / "IG_UI_kacan_baglam.json")
        out = []
        for k, v in baglam.items():
            if v[3] == "arayuz":
                dosya, _, no = v[0].rpartition(":")
                out.append({"k": k, "en": kaynak[k], "rel": dosya, "dosya": v[2], "alan": v[1], "no": int(no) if no.isdigit() else 0,
                            "konu": v[2], "yer": list(v)})
        return out
    sys.exit(f"plan: {', '.join(ARAYUZ_PLAN)}")


def _bolumle(liste, bolum, en_cok=30):
    """Aynı dosyanın satırlarını alt bloklara böler: dosyaya özel Lua satır aralıkları varsa onlarla, yoksa ≤en_cok satırlık dilimlerle."""
    if bolum:
        parca = {}
        for g in liste:
            i = next((i for i, (a, b, _) in enumerate(bolum) if a <= g["no"] <= b), len(bolum) - 1)
            parca.setdefault(i, []).append(g)
        return [(bolum[i][2], l) for i, l in sorted(parca.items())]
    if len(liste) <= en_cok:
        return [("", liste)]
    n = -(-len(liste) // en_cok)
    boy = -(-len(liste) // n)
    return [(f"{i + 1}/{n}", liste[i * boy:(i + 1) * boy]) for i in range(n)]


def hazirla_arayuz(paket, plan_adi, parca=150):
    """Plan paketinin (B10-B14) ekran metinlerini Gemini girdisine çevirir: arayüz kuralları + dosyaya özel terim listesi + ekran notu."""
    import arayuz_nerede
    import arayuz_terimler
    hedef, baslik = ARAYUZ_PLAN[plan_adi]
    baska = bekleyen(paket)
    if hedef == "IG_UI":
        dolu = set(oku(KOK / "onayli" / "IG_UI.json"))
    elif hedef == "Creator_lua":
        dolu = set(oku(KOK / "kaynak" / "Creator_lua.json"))
    else:
        dolu = set(oku(KOK / "kaynak" / f"{hedef}.json")) | set(oku(KOK / "kaynak" / "en" / "IG_UI.json"))
    tum = _arayuz_secimi(plan_adi)
    secim = [g for g in tum if g["k"] not in dolu and g["k"] not in baska]
    if not secim:
        sys.exit(f"{paket}: {plan_adi} için çevrilecek satır yok")
    N = arayuz_nerede.NEREDE
    sira = {ad: i for i, ad in enumerate(N)}
    bloklar, kod_sozcuk, eksik = [], [], set()

    def yol_etiketi(g):
        etiket = g["alan"] or "-"
        if g["alan"] == "liste" and g["no"] and g["rel"] != "?":
            yol = _lua_yolu(g["rel"], g["no"])
            if yol:
                etiket += " " + ".".join(yol[-2:])
        return etiket

    def satir(g, etiket=None):
        e = etiket or yol_etiketi(g)
        return (g["k"], g["en"], e, g.get("yer") or [g["dosya"] + ".lua", g["alan"] or "?", e])

    if plan_adi == "B14":
        gruplar = {}
        for g in secim:
            gruplar.setdefault(g["dosya"], []).append(g)
        for ad, (bas, nerede) in B14_NEREDE.items():
            liste = sorted(gruplar.pop(ad, []), key=lambda g: (g["rel"], g["no"], g["k"]))
            for alt, parca_liste in _bolumle(liste, None, 24):
                if parca_liste:
                    bloklar.append(([f"##### {bas}" + (f" ({alt})" if alt else "") + " #####", "# EKRAN: " + nerede]
                                    + (["# NOT: 'Right', 'Left', 'Auto', 'Strong' gibi kısa sözcükler oyunda başka yerlerde de aynı çeviriyle çıkar; hepsine uyan, tek başına anlaşılır karşılık seç"]
                                       if ad == "ayar" and alt in ("", "1/3") else []),
                                    [satir(g, g["alan"]) for g in parca_liste]))
        if gruplar:
            sys.exit(f"{paket}: tanımsız B14 grupları: {sorted(gruplar)}")
    else:
        dosyalar, veri = {}, []
        for g in secim:
            if g["rel"] == "?":
                veri.append(g)
            else:
                dosyalar.setdefault(g["dosya"], []).append(g)
        for ad in sorted(dosyalar, key=lambda a: sira.get(a, 999)):
            liste = sorted(dosyalar[ad], key=lambda g: (g["no"], g["k"]))
            if ad in arayuz_nerede.KOD_SOZCUK:
                kod_sozcuk += liste
                continue
            if ad not in N:
                eksik.add(ad)
            bas, nerede, *bolum = N.get(ad, (ad, f"{liste[0]['konu']} (ekran notu yok)"))
            for alt, parca_liste in _bolumle(liste, bolum[0] if bolum else None):
                bloklar.append(([f"##### {bas}" + (f" ({alt})" if alt and not bolum else "") + " #####",
                                 "# EKRAN: " + nerede + (f" · {alt}" if alt and bolum else "")], [satir(g) for g in parca_liste]))
        if kod_sozcuk:
            bloklar.append((["##### KISA SÖZCÜKLER (kod içinde geçen; ekranda görünüp görünmediği belirsiz) #####",
                             "# EKRAN: Oyunun kodunda tek başına geçen kısa sözcükler (durum, yön, eşleştirme sözcüğü). Bağlam yok: sözcüğü en yaygın, "
                             "yalın anlamıyla küçük harfle çevir; kişi adı ve kod gibi duruyorsa aynen bırak"],
                            [satir(g, "SÖZCÜK · " + g["dosya"].replace("ALife", "")) for g in sorted(kod_sozcuk, key=lambda g: (g["dosya"], g["no"]))]))
        if veri:
            for bas_sira, son_sira, ilk, bas, nerede in arayuz_nerede.CREATOR_VERI:
                if not any(g["en"].startswith(ilk) for g in tum if g.get("veri_sira") == bas_sira):
                    sys.exit(f"{paket}: B12 veri satır sırası değişmiş ({bas_sira}. satır '{ilk}' ile başlamıyor)")
                kume = [g for g in veri if bas_sira <= g["veri_sira"] <= son_sira]
                if kume:
                    bloklar.append(([f"##### {bas} #####", "# EKRAN: " + nerede], [satir(g, "veri") for g in kume]))
            if any(not any(a <= g["veri_sira"] <= b for a, b, *_ in arayuz_nerede.CREATOR_VERI) for g in veri):
                sys.exit(f"{paket}: CREATOR_VERI aralıkları dışında B12 veri satırı var")
    if eksik:
        print(f"{paket}: UYARI ekran notu olmayan dosyalar (arayuz_nerede.py'ye ekle): {sorted(eksik)}")
    toplam = sum(len(b[1]) for b in bloklar)
    dosya_sayisi = max(1, -(-toplam // parca))
    maden = arayuz_terimler.madenle()
    terimler = {}

    def aciklama(ens):
        liste = arayuz_terimler.dosya_terimleri(ens, maden, plan_adi)
        for e, t in liste:
            terimler.setdefault(e, t)
        return ARAYUZ_KURALLARI + ["# TERİMLER (bağlayıcı; yalnız bu dosyada geçenler; sözcük aynı anlamda geçiyorsa bu karşılığı kullan): " + "; ".join(f"{e} → {t}" for e, t in liste)]

    ek = {"_grup": "arayuz_" + plan_adi.lower(), "_dosya": hedef, "_plan": plan_adi, "_noktalama": False, "_bosluk_koru": True,
          "_baslik": baslik}
    no, dosya = _bloklari_yaz(paket, bloklar, -(-toplam // dosya_sayisi), aciklama, ek, yeni=False,
                              kurallar="# Kurallar: aşağıdaki ARAYÜZ kuralları (sahne/karakter canlandırma yok). Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama.")
    yol = KOK / "rapor" / f"{paket}_harita.json"
    h = oku(yol)
    h["_terimler"] = [[e, t] for e, t in terimler.items()]
    yaz(yol, h, 1)
    print(f"{paket}: {no} satır, {len(bloklar)} blok, {dosya} parça -> {GIRDI.relative_to(KOK).as_posix()}/{paket}_1..{dosya}.txt ({hedef}; "
          f"plan {plan_adi}; terim {len(terimler)})")


SATIR = re.compile(r"^\s*(?:[-*]\s*)?\**(\d+)\**\s*\|\s*(.*?)\s*$")
NOKTALAMA = re.compile(r"[.!?…]['\"”’)\]]*$|\*$")  # *...*: DoLines eylem satırı (K46)


SANDBOX_KURALLARI = [
    "# AYAR EKRANI: Bu satırlar oyunun Sandbox (ayarlar) ekranındaki Project A-Life seçenekleridir. Her ##### bloğu TEK bir ayardır: "
    "'ayar adı' listede görünen kısa başlık, 'ipucu' fareyle üstüne gelince çıkan açıklama, 'seçenek N' açılır listedeki seçeneklerdir. "
    "'·' ile başlayan satır çevrilmez: sabit çeviridir (değişmez), bağlam olarak gösterilir; blokta bir ayar adı ya da seçenek '·' ise onun "
    "Türkçesini aynen kullan.",
    "# AYAR ADI ve SEÇENEK: Ayar adı kısa, net, Türkçe oyun menüsü dilinde; ekranda sığmalı (en fazla ≈1,3 kat). Aynı sayfadaki kardeş ayarlarla "
    "biçim tutsun. '[Expert]' / '[Uzman]' gibi köşeli ön ekler İngilizcedeki gibi varsa kalır, aynı sözcükle çevrilir. Seçenekler (Off/Low/Normal/High…) "
    "kısa ve bir ölçek gibi sıralı okunmalı.",
    "# İPUCU: 1-3 cümle, 'sen' hitabı gerekirse, sade ve açık. Sayılar, birimler ve 'x2', '%' gibi işaretler aynen. İpucu başka bir ayarın adını "
    "anıyorsa o ayarın adını kullan; aynı dosyada o ayar varsa onun çevirisiyle birebir aynı yaz, başka dosyadaysa en doğal karşılığı ver (sonradan eşitlenir).",
    "# SATIR SONU: İngilizcedeki '\\n' ipucunda satır sonudur. Türkçede de aynen '\\n' olarak (iki karakter: ters bölü ve n) kalsın, çıktı tek satır olsun. "
    "Son satır çoğunlukla 'Default X (n).' biçimindedir: 'Varsayılan: X (n).' olarak yaz; X bir seçenek adıysa aynı bloktaki seçeneğin Türkçesiyle "
    "birebir aynı olmalı, sayılar aynen kalmalı.",
    "# SABİT KARŞILIKLAR (bütün dosyalarda aynı): Default on. → Varsayılan: açık. · Default off. → Varsayılan: kapalı. · [Expert] → [Uzman] · EXPERT - → UZMAN - · "
    "Off → Kapalı · Low → Düşük · Normal → Normal · High → Yüksek · Very high → Çok yüksek · Raiders → Yağmacılar · raid → baskın.",
]


def hazirla_sandbox(paket="SB1", parca=150):
    """Ayar ekranı (Sandbox) metinleri baştan çeviri için (K57). Sıra ve sayfa mod dosyası sandbox-options.txt'den; her ayar bir blok
    (ad + ipucu + seçenekler). Kullanıcının kendi eski çevirisi (Sandbox-updated-translated) bağlam '·' olur, çevrilmez."""
    import arayuz_terimler
    from lua_cikar import MOD
    en = oku(KOK / "kaynak" / "en" / "Sandbox.json")
    tr = oku(KOK / "onayli" / "Sandbox.json")
    temel_tr = oku(KOK / "Sandbox-updated-translated.json")
    temel_en = oku(KOK / "Sandbox-updated.json")
    kendi = {k for k in en if k in temel_tr and temel_tr[k] == tr.get(k) and temel_en.get(k) == en[k]}
    sandbox = (MOD.parent / "sandbox-options.txt").read_text(encoding="utf-8", errors="ignore")
    sayfalar = {}  # sayfa -> [(ayar kodu, [anahtar...])]
    gorulen = set()

    def al_anahtar(k):
        if k in en and k not in gorulen:
            gorulen.add(k)
            return k
        return None

    for m in re.finditer(r"option\s+([\w.]+)\s*=\s*\{(.*?)\n\}", sandbox, re.S):
        ad, govde = m.group(1), m.group(2)
        sayfa = re.search(r"page\s*=\s*([\w]+)", govde)
        ceviri = re.search(r"translation\s*=\s*([\w.]+)", govde)
        ipucu = re.search(r"_tooltip\s*=\s*([\w.]+)", govde)
        deger = re.search(r"valueTranslation\s*=\s*([\w.]+)", govde)
        if not (sayfa and ceviri):
            continue
        anahtarlar = []
        for k in (f"Sandbox_{ceviri.group(1)}", f"Sandbox_{ipucu.group(1)}" if ipucu else None):
            if k and al_anahtar(k):
                anahtarlar.append(k)
        for vt in {x for x in (deger.group(1) if deger else None, ceviri.group(1)) if x}:
            for k in sorted((x for x in en if x.startswith(f"Sandbox_{vt}_option")), key=lambda x: int(re.search(r"(\d+)$", x).group(1))):
                if al_anahtar(k):
                    anahtarlar.append(k)
        if anahtarlar:
            sayfalar.setdefault(sayfa.group(1), []).append((ad, anahtarlar))
    sayfa_basliklari = [k for k in en if re.fullmatch(r"Sandbox_ProjectALife_\w+", k)]
    for k in sayfa_basliklari:
        gorulen.add(k)
    kalan = [k for k in en if k not in gorulen]

    def etiket(k):
        if k.endswith("_tooltip"):
            return "ipucu"
        mm = re.search(r"_option(\d+)$", k)
        return f"seçenek {mm.group(1)}" if mm else "ayar adı"

    etiketler = {v: k for k, v in en.items() if not re.search(r"_(tooltip|option\d+)$", k) and len(v) > 14}

    def satir(k, atif=True):
        if k in kendi:
            return ("·", f"{etiket(k)} · SABİT ÇEVİRİ (değiştirme, aynen kullan): {tr[k]}", en[k])
        return (k, en[k], etiket(k), [k])

    bloklar = []
    if sayfa_basliklari:
        bloklar.append((["##### SEKME ADLARI #####", "# EKRAN: Sandbox ekranının üstündeki Project A-Life sekmelerinin adları (sayfa başlıkları, kısa); sayfaların sırası ve içeriği aşağıdaki bloklardan anlaşılır"],
                        [satir(k) for k in sayfa_basliklari]))
    for sayfa, ayarlar in sayfalar.items():
        baslik = next((en[k] for k in sayfa_basliklari if k.endswith("_" + sayfa.split("ProjectALife_")[-1])), sayfa)
        for ad, ks in ayarlar:
            ust = [f"##### {baslik.upper()} · {ad} #####", f"# EKRAN: Sandbox ekranı, '{baslik}' sekmesi, ayar kodu {ad}"]
            satirlar = [satir(k) for k in ks]
            for k in ks:
                if k.endswith("_tooltip") and k not in kendi:
                    for v, lk in etiketler.items():
                        if v.lower() in en[k].lower() and not k.startswith(lk) and lk not in ks:
                            satirlar.append(("#", f"ATIF: ipucundaki '{v}' başka bir ayarın adıdır; oradaki Türkçe adla aynı yaz"))
                            break
            bloklar.append((ust, satirlar))
    if kalan:
        gruplar = {}
        for k in kalan:
            gruplar.setdefault(re.sub(r"(_tooltip|_option\d+)$", "", k), []).append(k)
        for taban, ks in gruplar.items():
            bloklar.append(([f"##### DİĞER · {taban} #####", "# EKRAN: Sandbox ekranı, ayar sayfalarının dışında kalan ayar (ör. sürüş)"], [satir(k) for k in ks]))
    maden = {}

    def aciklama(ens):
        liste = arayuz_terimler.dosya_terimleri(ens, maden)
        return ARAYUZ_KURALLARI + SANDBOX_KURALLARI + [
            "# BAŞTAN ÇEVİRİ: Bu ayarlar oyunda şu an eski bir çeviriyle duruyor; sen sıfırdan İngilizceden kur. Ayar ekranı: kuru tutanak "
            "değil, bir Türk oyun yazarının yazacağı gibi doğal, kısa ve açık yaz. Aynı kavrama her yerde aynı sözcük.",
            "# TERİMLER (bağlayıcı; yalnız bu dosyada geçenler): " + "; ".join(f"{e} → {t}" for e, t in liste)]

    toplam, dosya = _bloklari_yaz(paket, bloklar, parca, aciklama,
                                  {"_grup": "arayuz_sandbox", "_dosya": "Sandbox", "_noktalama": False, "_bosluk_koru": True,
                                   "_satir_sonu": True, "_baslik": "Ayar ekranı (Sandbox), baştan çeviri (K57)"}, yeni=False,
                                  kurallar="# Kurallar: alife-ceviri skill'i, ARAYÜZ bölümü. Çıktı: her satır 'N | Türkçe' (etiketi yazma), numaralar aynen, hiçbirini atlama.")
    print(f"{paket}: {toplam} satır, {len(bloklar)} blok, {dosya} parça (Sandbox); kendi çevirin (bağlam, çevrilmez): {len(kendi)}; "
          f"kalan/diğer: {len(kalan)}; sayfa: {len(sayfalar)}; toplam anahtar {len(en)}")


def noktalama_orani(metinler):
    """Sonu noktalamalı satırların oranı. Kaynak satırların çoğu noktasız biter; skill'in uygulandığı Gemini çıktılarında
    oran ~%100, uygulanmadığı çıktılarda (birebir, birim çevrilmemiş: SNE_5-19, SNC_1/3/4, SNB_7) %8-25 (2026-11-03)."""
    metinler = [m.partition("##")[0].strip() for m in metinler]
    return sum(1 for m in metinler if NOKTALAMA.search(m)) / max(1, len(metinler))


def al(paket, dosyalar, zorla=False, ad=None, claude=False):
    harita = oku(KOK / "rapor" / f"{paket}_harita.json")
    beklenen = harita["satirlar"]
    aralik = harita.get("_parcalar") or [[1, len(beklenen)]]
    if not dosyalar:
        # Kullanıcı bazen "_TR" eklemeden kaydeder (D13_1.txt): ikisini de kabul et; aynı parça iki adla varsa _TR esas.
        adlar = {}
        for f in CIKTI.glob(f"{paket}_*.txt"):
            m = re.fullmatch(re.escape(paket) + r"_(\d+)(_TR)?\.txt", f.name)
            if m and (m.group(1) not in adlar or m.group(2)):
                adlar[m.group(1)] = f
        dosyalar = [adlar[k] for k in sorted(adlar, key=int)]
    if not dosyalar:
        sys.exit(f"{paket}: {CIKTI.relative_to(KOK).as_posix()}/ içinde {paket}_*.txt yok")
    gelen, tekrar, yabanci, supheli, sira_hatasi = {}, [], [], [], []
    for d in dosyalar:
        okunan = []
        for satir in Path(d).read_text(encoding="utf-8-sig").splitlines():
            m = SATIR.match(satir)
            if m:
                okunan.append((m.group(1), re.sub(r"^K\d+\s*\|\s*", "", m.group(2))))  # sahne etiketi geri yazılmışsa at
        numaralar = [int(n) for n, _ in okunan]
        if numaralar != sorted(numaralar):
            sira_hatasi.append(f"{Path(d).name}: satır numaraları sırasız ({numaralar[:8]})")
        parca = re.fullmatch(re.escape(paket) + r"_(\d+)(_TR)?\.txt", Path(d).name)
        if parca:
            parca_no = int(parca.group(1))
            if not 1 <= parca_no <= len(aralik):
                sira_hatasi.append(f"{Path(d).name}: beklenmeyen parça numarası")
            else:
                bas, son = aralik[parca_no - 1]
                beklenen_numaralar = list(range(bas, son + 1))
                if numaralar != beklenen_numaralar:
                    sira_hatasi.append(
                        f"{Path(d).name}: parça {parca_no} için {bas}-{son} sıralı numaralar bekleniyor; "
                        f"gelen {len(numaralar)} satır, başlangıç {numaralar[:5]}, bitiş {numaralar[-5:]}"
                    )
        # Oran yalnız cümle satırlarında (K42): düğmeler/notlar noktasız biter, seçenek ağırlıklı dosyayı yanlışlıkla reddetmesin.
        haric = tuple(harita.get("_noktalama_haric", ()))
        cumle = [metin for n, metin in okunan if not (haric and n in beklenen and str(beklenen[n][2][2]).startswith(haric))]
        oran = noktalama_orani(cumle)
        if harita.get("_noktalama", True) and len(cumle) >= 20 and oran < 0.5 and not zorla:
            supheli.append(f"{Path(d).name} (%{oran * 100:.0f})")
            continue
        for n, metin in okunan:
            if n not in beklenen:
                yabanci.append(n)
                continue
            if n in gelen:
                tekrar.append(n)
            gelen[n] = metin
    if supheli:
        print(f"{paket}: ALINMADI, skill uygulanmamış görünüyor (satır sonu noktalaması düşük; iyi çıktılarda ~%100): "
              f"{', '.join(supheli)}. Yeni sohbet açıp güncel alife-ceviri yönergesiyle yeniden çevirt; yine de almak için --zorla.")
    tamam, bekliyor, yarim = [], [], []
    for p, (bas, son) in enumerate(aralik, 1):
        nums = [str(i) for i in range(bas, son + 1)]
        var = [n for n in nums if n in gelen]
        if len(var) == len(nums):
            tamam.append(p)
        elif not var:
            bekliyor.append(p)
        else:
            yarim.append((p, [n for n in nums if n not in gelen]))
    if yarim or tekrar or yabanci or sira_hatasi:
        sys.exit(f"{paket}: yarım parça {[(p, len(e), e[:20]) for p, e in yarim]} · tekrar {tekrar[:30]} · "
                 f"beklenmeyen numara {yabanci[:30]} · sıra/parça hatası {sira_hatasi[:20]}")
    if not tamam:
        sys.exit(f"{paket}: tamamlanmış parça yok")
    satirlar = {}
    for p in tamam:
        bas, son = aralik[p - 1]
        for i in range(bas, son + 1):
            k, en, yer = beklenen[str(i)]
            tr, _, not_ = gelen[str(i)].partition("##")
            tr = tr.strip().strip('"“”').strip()
            if harita.get("_satir_sonu"):  # girdide '\n' yazılan satır sonu geri çevrilir
                tr = tr.replace("\\n", "\n")
            not_ = re.sub(r"^\s*not\s*:\s*", "", not_, flags=re.I).strip()
            if not tr:
                sys.exit(f"{paket}: {i}. satır boş")
            if harita.get("_bosluk_koru"):  # çıktı satırı sonda boşluğu yutar; baş/son boşluk İngilizcedeki gibi geri konur (paket_kontrol)
                tr = en[:len(en) - len(en.lstrip())] + tr.strip() + en[len(en.rstrip()):]
            satirlar[k] = {"tr": tr, **({"not": not_} if not_ else {})}
    baslik = harita.get("_baslik") or harita["_grup"]
    kapsam = "" if not bekliyor else f"; parça {tamam} / {len(aralik)}, bekleyen {bekliyor}"
    cevirmen = "Claude, K43 yeniden çeviri" if claude else "harici AI; kalite incelemesi yapılmadı"
    hedef = harita.get("_dosya", "RadioData_lua")
    yaz(KOK / "paketler" / f"{ad or paket}.json", {
        "_paket": f"{ad or paket} — {baslik}, {len(satirlar)}{kapsam} (çeviri: {cevirmen})",
        "_dosya": hedef, "satirlar": satirlar}, 2)
    if hedef != "RadioData_lua" and not hedef.endswith("_lua"):  # IG_UI anahtarları kaynak/en/<dosya>.json'dan gelir (K26)
        print(f"{paket}: {len(satirlar)} satır (parça {tamam}/{len(aralik)}; bekleyen {bekliyor or 'yok'}) -> paketler/{ad or paket}.json "
              f"({hedef}). Sıradaki: python -X utf8 araclar/paket_kontrol.py {ad or paket}")
        return
    # RadioData_lua ya da başka bir _lua kaynağı (ör. IG_UI_lua, Y5): onayla anahtarları kaynak/<hedef>.json'dan sıralar
    k_yol, b_yol = KOK / "kaynak" / f"{hedef}.json", KOK / "kaynak" / f"{hedef}_baglam.json"
    kaynak, baglam = oku(k_yol), (oku(b_yol) if b_yol.exists() else {})
    yeni = 0
    for p in tamam:
        bas, son = aralik[p - 1]
        for i in range(bas, son + 1):
            k, en, yer = beklenen[str(i)]
            if k not in kaynak:
                kaynak[k], baglam[k] = en, yer
                yeni += 1
    yaz(k_yol, kaynak)
    yaz(b_yol, baglam, 1)
    print(f"{paket}: {len(satirlar)} satır (parça {tamam}/{len(aralik)}; bekleyen {bekliyor or 'yok'}) -> paketler/{ad or paket}.json; "
          f"kaynak/{hedef}.json'a {yeni} yeni satır (toplam {len(kaynak)}). Sıradaki: python -X utf8 araclar/paket_kontrol.py {ad or paket}")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "hazirla":
        p = sys.argv.index("--parca") if "--parca" in sys.argv else None
        hazirla(sys.argv[2], sys.argv[3], int(sys.argv[p + 1]) if p else 300)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-sahne":
        p = sys.argv.index("--parca") if "--parca" in sys.argv else None
        hazirla_sahne(sys.argv[2], int(sys.argv[p + 1]) if p else 300)
    elif len(sys.argv) >= 4 and sys.argv[1] == "hazirla-liste":
        p = sys.argv.index("--dosya") if "--dosya" in sys.argv else None
        hazirla_liste(sys.argv[2], sys.argv[3], int(sys.argv[p + 1]) if p else 100, "--mevcut" in sys.argv)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-yeni":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_yeni(sys.argv[2], int(sys.argv[p + 1]) if p else 127)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-radyo":
        p = sys.argv.index("--parca") if "--parca" in sys.argv else None
        hazirla_radyo(sys.argv[2], int(sys.argv[p + 1]) if p else 150)
    elif len(sys.argv) >= 4 and sys.argv[1] == "hazirla-agac":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_agac(sys.argv[2], sys.argv[3], int(sys.argv[p + 1]) if p else 128)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-arayuz-diyalog":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_arayuz_diyalog(sys.argv[2], int(sys.argv[p + 1]) if p else 128)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-kacan":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_kacan(sys.argv[2], int(sys.argv[p + 1]) if p else 128)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-bosluk":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_bosluk(sys.argv[2], int(sys.argv[p + 1]) if p else 128)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-liste-soz":
        p = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_liste_soz(sys.argv[2], int(sys.argv[p + 1]) if p else 128)
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-arayuz":
        p = sys.argv.index("--plan") if "--plan" in sys.argv else None
        if not p or sys.argv[p + 1] not in ARAYUZ_PLAN:
            sys.exit(f"--plan {'|'.join(ARAYUZ_PLAN)} gerekli")
        q = sys.argv.index("--satir") if "--satir" in sys.argv else None
        hazirla_arayuz(sys.argv[2], sys.argv[p + 1], int(sys.argv[q + 1]) if q else 150)
    elif len(sys.argv) >= 2 and sys.argv[1] == "hazirla-creator":
        hazirla_creator()
    elif len(sys.argv) >= 2 and sys.argv[1] == "hazirla-sandbox":
        hazirla_sandbox(*(sys.argv[2:3] or ["SB1"]))
    elif len(sys.argv) >= 2 and sys.argv[1] == "hazirla-itibar":
        hazirla_itibar()
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-baskin":
        hazirla_baskin(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "hazirla-bitis-soz":
        hazirla_bitis_soz(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "al":
        a = sys.argv.index("--ad") if "--ad" in sys.argv else None
        ad = sys.argv[a + 1] if a else None
        dosyalar = [x for i, x in enumerate(sys.argv[3:], 3) if x not in ("--zorla", "--claude", "--ad", "--yeni") and (a is None or i != a + 1)]
        al(sys.argv[2], dosyalar, "--zorla" in sys.argv, ad, "--claude" in sys.argv)
    else:
        sys.exit(__doc__)
