"""Ziyaretçi/kapı sistemi (K46) dış çeviri girdileri için sahne notları: araclar/sahne/Z1.json ve Z2.json.

Kullanım: python -X utf8 araclar/ziyaretci_not.py
Her düğüm (vp_1006.VQ_HOUSE_BATH, vp_1006.react.gave_food…) için: konuşan ziyaretçi (cinsiyet, yaş, tip, tarif,
geldiği yer) ve oyuncunun ne sorduğu ya da ne yaptığı. Sonra: harici_paket.py hazirla Z1 z1 / Z2 z2.
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import diyalog_cikar as dc  # noqa: E402

OLAY = {
    "react.gave_food": "oyuncu ona yiyecek verdi", "react.gave_water": "oyuncu ona su verdi",
    "react.gave_book": "oyuncu ona kitap ödünç verdi", "react.gave_blanket": "oyuncu ona battaniye verdi",
    "react.gave_clothes": "oyuncu ona giysi verdi", "react.gave_smokes": "oyuncu ona sigara verdi",
    "react.gave_meds": "oyuncu ona ilaç verdi", "react.offered_bed": "oyuncu ona yatacak yer teklif etti",
    "react.thanks": "oyuncu ona teşekkür etti", "react.sorry": "oyuncu ondan özür diledi",
    "react.compliment": "oyuncu ona iltifat etti", "react.insult": "oyuncu ona hakaret etti",
    "react.threat": "oyuncu onu tehdit etti", "react.refused": "oyuncu isteğini geri çevirdi",
    "react.ignored": "oyuncu onu duymazdan geldi",
    "leave.angry": "kızgın ayrılırken söylüyor", "leave.plain": "evden ayrılırken söylüyor",
    "leave.grateful": "minnetle ayrılırken söylüyor", "leave.need_met": "ihtiyacı karşılandı, ayrılırken söylüyor",
    "return.arrive": "daha sonra yine kapına geldiğinde söylüyor",
    "return.gave_food": "tekrar geldi; geçen sefer ona yiyecek vermiştin",
    "return.refused_door": "tekrar geldi; geçen sefer kapıyı açmamıştın",
    "return.threatened": "tekrar geldi; geçen sefer onu tehdit etmiştin",
    "return.lied_to": "tekrar geldi; geçen sefer ona yalan söylemiştin",
}


def kisi_notu(k):
    cins = {"m": "erkek", "f": "kadın"}.get(k["cins"], "")
    parca = [f"KONUŞAN: {cins} {k['yas'] or ''} yaşında".strip()]
    if k["tip"]:
        parca.append(f"({k['tip']})")
    if k["tarif"]:
        parca.append(f"görünüş: {k['tarif']}")
    if k["nereden"]:
        parca.append(f"geldiği yer: {k['nereden']}")
    if k["is"]:
        parca.append(f"eski işi: {k['is'][:120]}")
    return "; ".join(parca)


def main():
    kisi = dc.kisiler()
    sorular = {k: next((v for a, v in al if a == "t.1"), "") for _, k, al in dc.alife_kayitlar("questions.alife")}
    z1 = {
        "_baslik": "Ziyaretçi/kapı sistemi: evinin kapısına gelen ya da misafirin olan yabancıların konuşmaları",
        "_genel": ("Oyuncunun bir evi (sığınağı) var. Yabancılar kapısını çalar; oyuncu kapıdan konuşur, isterse içeri alır, "
                   "misafir bir gece kalır, yiyecek/su/yatak alabilir, sohbet eder, sonra gider ya da tekrar gelir. Satırların hepsi "
                   "ZİYARETÇİNİN oyuncuya söylediği sözler; oyuncuya 'sen' de. Her başlıkta konuşanın kim olduğu yazıyor: sesini "
                   "yaşına, geçmişine ve karakterine göre kur (yaşlı köylü, genç anne, eski asker…); aynı kişinin bütün satırları aynı "
                   "ağızdan çıksın. 'güven=lo/mid/hi' ziyaretçinin oyuncuya güveni (düşük: çekingen, kısa; yüksek: açık, sıcak); "
                   "'any' her durumda. '..' kısa duraklama ya da yarım kalan düşünce: Türkçede '...' ya da cümleyi bölerek ver. Kasaba ve kişi adları "
                   "İngilizce kalır. Birimleri çevir (mil → km, Fahrenheit → Celsius). 'oyuncunun sorusu' satırı oyuncunun kapıda "
                   "sorduğu soru, numaralı satırlar ziyaretçinin cevabı."),
    }
    for _, k, al in dc.alife_kayitlar("nodes_*.alife"):
        kid, _, olay = k.partition(".")
        bilgi = kisi_notu(kisi[kid]) if kid in kisi else ""
        q = re.match(r"(VQ_\w+?)(\.d\d*)?$", olay)
        if q:
            durum = f"Oyuncunun sorusu: \"{sorular.get(q.group(1), q.group(1))}\""
            if q.group(2):
                durum += " — ziyaretçi cevap vermekten kaçınıyor (henüz yeterince güvenmiyor)"
        elif olay.startswith("VE_"):
            durum = "Ziyaretçinin kendiliğinden başlattığı bir olay; oyuncuya seçenek sunan soru/istek"
        else:
            durum = OLAY.get(olay, olay.replace("_", " "))
        z1[k] = f"{bilgi}. DURUM: {durum}"
    z2 = {
        "_baslik": "Ziyaretçi paneli: soru düğmeleri, olay seçenekleri, kişi tarifleri, öğrenilen bilgiler, kapı eylem satırları",
        "_genel": ("Konuşma penceresinde görünen kısa metinler. 'soru düğmesi': OYUNCUNUN ziyaretçiye sorduğu soru, düğmenin "
                   "üstünde yazar; oyuncunun ağzından, ziyaretçiye 'sen' diye, kısa ve doğal (en fazla ~60 karakter). 'olay seçeneği': "
                   "oyuncunun seçtiği tepki, kısa emir/eylem (Ayır onları, Yalan söyle). 'kişi tarifi': ziyaretçinin dış görünüşü, "
                   "pencerenin başlığında; isim öbeği olarak kur ('beyaz saçları kısa kesilmiş yaşlı bir adam'), en fazla ~150 karakter. "
                   "'oyuncunun öğrendiği bilgi': 'Bildiklerin' listesinde, ziyaretçi hakkında üçüncü tekil kısa not ('Elmer'a yardım "
                   "sözü verdi, geri dönmedi'). 'kapı eylem satırı': yıldızlar arasında kısa betimleme, yıldızları koru. "
                   "Bayt sınırı aşılırsa oyunda İngilizce görünür: kısa yaz."),
    }
    for k, kv in kisi.items():
        z2[k + ".desc"] = kisi_notu(kv)
        z2[k + ".facts"] = kisi_notu(kv)
    for ad, veri in (("Z1", z1), ("Z2", z2)):
        (KOK / "araclar" / "sahne" / f"{ad}.json").write_text(json.dumps(veri, ensure_ascii=False, indent=1) + "\n",
                                                            encoding="utf-8", newline="\n")
        print(ad, len(veri) - 2, "not")


if __name__ == "__main__":
    main()
