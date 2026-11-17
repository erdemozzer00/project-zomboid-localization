"""Şablon varyantlarını (teslim/RadioData.json'daki cinsiyet çözülmüş ek satırlar) oyunun kendi Lua koduyla denetler.

Çalıştırma: python -B -X utf8 araclar/test_sablon_varyant.py
Gereksinim: lupa (Lua 5.1). Her uygun şablon için gerçek Speech.render(şablon, nil, nil, "m"/"f") çıktısının
Python'un ürettiğiyle aynı olduğunu, Text.lineKey'inin teslimde bulunduğunu ve konuşma ekinin caption'da süslü
parantezsiz Türkçe döndürdüğünü doğrular. Oyun içi çizimi doğrulamaz.
"""
import json
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import test_konusma_font as t  # noqa: E402
import sablon_varyant as sv  # noqa: E402

EN = json.loads((KOK / "kaynak/RadioData_lua.json").read_text(encoding="utf-8"))
ONAYLI = json.loads((KOK / "onayli/RadioData_lua.json").read_text(encoding="utf-8"))
TESLIM = json.loads((KOK / "teslim/RadioData.json").read_text(encoding="utf-8"))
# DoLines ({v:He}) konuşma yolundan geçmez; onları test_sablon_eslesme.DoLinesTesti dener
SABLONLAR = {k: v for k, v in ONAYLI.items() if "{" in EN[k] and not sv.V.search(EN[k]) and sv.varyantlar(EN[k], v) is not None}


class SablonVaryantTesti(unittest.TestCase):
    def test_sablon_sayisi(self):
        self.assertGreaterEqual(len(SABLONLAR), 1)

    def test_gercek_lua_ile_ayni_metin_ve_anahtar_ve_ceviri(self):
        oyun = t.Oyun()
        lua = oyun.g.ProjectALife
        sayac = 0
        for k, tr in SABLONLAR.items():
            for cinsiyet, (en_py, tr_py) in zip(("m", "f"), sv.varyantlar(EN[k], tr)):
                with self.subTest(anahtar=k, cinsiyet=cinsiyet):
                    render = lua.Speech.render(EN[k], None, None, cinsiyet)
                    self.assertEqual(render, en_py)
                    anahtar = lua.Text.lineKey(render)
                    self.assertEqual(anahtar, sv.anahtar(en_py))
                    self.assertEqual(TESLIM[anahtar], tr_py)
                    cevrilen = oyun.cevir(render)
                    self.assertEqual(cevrilen, tr_py)
                    self.assertNotIn("{", cevrilen)
                    self.assertNotIn("}", cevrilen)
                    sayac += 1
        self.assertEqual(sayac, 2 * len(SABLONLAR))

    def test_eski_satirlar_degismez(self):
        for k, v in EN.items():
            if "{" in v:
                continue
            if k in ONAYLI:
                self.assertEqual(TESLIM[k], ONAYLI[k])


if __name__ == "__main__":
    t.EN, t.TR = EN, TESLIM
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
