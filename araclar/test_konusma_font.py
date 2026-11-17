"""Konuşma ekini gerçek A-Life Lua kaynakları ve sahte oyun çağrılarıyla denetler.

Çalıştırma: python -B -X utf8 araclar/test_konusma_font.py
Gereksinim: lupa (Lua 5.1). Bu denetim oyun içi çizimi doğrulamaz.
"""

import argparse
import hashlib
import json
import re
import runpy
import sys
import unittest
from pathlib import Path

from lupa.lua51 import LuaRuntime


KOK = Path(__file__).resolve().parent.parent
OYUN = Path(r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid")
MOD_LUA = Path(
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content\108600"
    r"\3803984183\mods\ProjectALifeNPCs\42.20\media\lua"
)
EK = KOK / "araclar/lua/ALifeTR_Konusma.lua"
MOD_DOSYALARI = (
    "shared/ProjectALife/Core/ALifeText.lua",
    "shared/ProjectALife/Audio/ALifeAudioPolicy.lua",
    "shared/ProjectALife/Talk/ALifeSpeech.lua",
    "shared/ProjectALife/World/ALifeTownRegions.lua",  # K46: ekin kasaba doğrulaması
)
EN = json.loads((KOK / "kaynak/RadioData_lua.json").read_text(encoding="utf-8"))
TR = json.loads((KOK / "teslim/RadioData.json").read_text(encoding="utf-8"))
ORNEK_ANAHTAR = "RD_ALifeLine_0cb665b165cd8785"
HARFLER = "ÇçĞğİıÖöŞşÜü"


def ek_metni():
    """Ekin yer tutucuları (__SABLONLAR__) doldurulmuş hâli; --ek verilmişse o dosya olduğu gibi."""
    if EK != KOK / "araclar/lua/ALifeTR_Konusma.lua":
        return EK.read_text(encoding="utf-8-sig")
    sys.path.insert(0, str(KOK / "araclar"))
    import workshop_kur
    return workshop_kur.ek_metni("ALifeTR_Konusma.lua")


class Oyun:
    def __init__(self, dil="TR", ek=True, geciken=None):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.g = self.lua.globals()
        self.g.DIL = dil
        self.g.CEVIRILER = self.lua.table_from(TR)
        self.lua.execute("""
            require = function() end
            ProjectALife = {}
            UIFont = { Small = "Small" }
            Translator = { getLanguage = function()
                return { name = function() return DIL end }
            end }
            getTextOrNull = function(key) return CEVIRILER[key] end
            BOOT, LOG, CIZIM, KUTU = {}, {}, {}, {}
            FONT_DENEME, MIRROR, SAY = 0, 0, 0
            BASLA = {}
            Events = { OnGameBoot = { Add = function(f) BOOT[#BOOT + 1] = f end },
                       OnGameStart = { Add = function(f) BASLA[#BASLA + 1] = f end } }
            print = function(s) LOG[#LOG + 1] = tostring(s) end
            SHELL = {
                addLineChatElement = function(self, ...)
                    local n = select("#", ...)
                    if n > 4 then
                        FONT_DENEME = FONT_DENEME + 1
                        if FONT_HATA then error("fontlu cagri reddedildi") end
                    end
                    CIZIM[#CIZIM + 1] = { n = n, ... }
                end,
                Say = function(self, text) SAY = SAY + 1; SON_SAY = text end
            }
            RENK = { 0.85, 0.6, 0.3 }
        """)
        for ad in MOD_DOSYALARI:
            self.lua.execute((MOD_LUA / ad).read_text(encoding="utf-8-sig"))
        self.lua.execute("""
            ProjectALife.NpcChat = { mirror = function() MIRROR = MIRROR + 1 end }
            ProjectALife.SpeechBubbles = { show = function(shell, text)
                KUTU[#KUTU + 1] = text
                return KUTU_ACIK == true
            end }
            ASIL_ENGINE_SAY = ProjectALife.Speech.engineSay
        """)
        self.geciken = geciken
        self.saklanan = None
        if geciken:
            self.saklanan = self.g.ProjectALife[geciken]
            self.g.ProjectALife[geciken] = None
        if ek:
            self.lua.execute(ek_metni())

    def baslat(self):
        if self.geciken:
            self.g.ProjectALife[self.geciken] = self.saklanan
        self.lua.execute("for _, f in ipairs(BOOT) do f() end")

    def goster(self, text):
        return self.g.ProjectALife.Speech.display(self.g.SHELL, text, self.g.RENK, "directed", "test-npc")

    def cevir(self, text):
        return self.g.ProjectALife.AudioPolicy.caption(text)

    def son(self):
        return self.g.CIZIM[len(self.g.CIZIM)]


class KonusmaFontTesti(unittest.TestCase):
    def test_gercek_replik_cevrilir_ve_harfleri_korunur(self):
        oyun = Oyun()
        text = oyun.cevir(EN[ORNEK_ANAHTAR])
        self.assertEqual(text, TR[ORNEK_ANAHTAR])
        self.assertTrue(oyun.goster(text))
        call = oyun.son()
        self.assertEqual(call[1], text)
        self.assertEqual([call[i] for i in (2, 3, 4)], [0.85, 0.6, 0.3])
        self.assertEqual([call[i] for i in (5, 6, 7)], ["Small", 30, "default"])
        self.assertEqual(oyun.g.MIRROR, 1)

    def test_turkce_harflerin_tamami_ve_uzun_metin_korunur(self):
        oyun = Oyun()
        text = (HARFLER + " — İğne, şişe, çığlık!\n") * 80
        oyun.goster(text)
        self.assertEqual(oyun.son()[1], text)

    def test_teslimdeki_tum_replikler_cizime_aynen_iletilir(self):
        oyun = Oyun()
        for text in TR.values():
            self.assertTrue(oyun.goster(text))
            self.assertEqual(oyun.son()[1], text)
            self.assertEqual(oyun.son()[5], "Small")
        self.assertEqual(len(oyun.g.CIZIM), len(TR))
        self.assertEqual(oyun.g.MIRROR, len(TR))

    def test_ingilizce_dilinde_orijinal_cagri_kullanilir(self):
        oyun = Oyun(dil="EN")
        original = EN[ORNEK_ANAHTAR]
        self.assertEqual(oyun.cevir(original), original)
        oyun.goster(original)
        self.assertEqual(oyun.son()["n"], 4)
        self.assertEqual(oyun.g.FONT_DENEME, 0)

    def test_cevirisi_olmayan_replik_aynen_kalir(self):
        oyun = Oyun()
        text = "An untranslated line for this check."
        self.assertEqual(oyun.cevir(text), text)
        oyun.goster(text)
        self.assertEqual(oyun.son()[1], text)

    def test_kutulu_konusma_standart_yaziya_gonderilmez(self):
        oyun = Oyun()
        oyun.g.KUTU_ACIK = True
        text = oyun.cevir(EN[ORNEK_ANAHTAR])
        self.assertTrue(oyun.goster(text))
        self.assertEqual(oyun.g.KUTU[1], text)
        self.assertEqual(len(oyun.g.CIZIM), 0)
        self.assertEqual(oyun.g.FONT_DENEME, 0)
        self.assertEqual(oyun.g.MIRROR, 1)

    def test_font_hatasinda_eski_yol_ve_ceviri_calismaya_devam_eder(self):
        oyun = Oyun()
        oyun.g.FONT_HATA = True
        for _ in range(3):
            text = oyun.cevir(EN[ORNEK_ANAHTAR])
            self.assertEqual(text, TR[ORNEK_ANAHTAR])
            self.assertTrue(oyun.goster(text))
            self.assertEqual(oyun.son()[1], text)
            self.assertEqual(oyun.son()["n"], 4)
        self.assertEqual(oyun.g.FONT_DENEME, 1)
        self.assertEqual(len(oyun.g.LOG), 1)
        self.assertFalse(oyun.g.ALifeTurkce_Konusma.kapali)

    def test_small_fontu_yoksa_eski_yola_donulur(self):
        oyun = Oyun()
        oyun.g.UIFont = None
        oyun.goster(HARFLER)
        self.assertEqual(oyun.son()[1], HARFLER)
        self.assertEqual(oyun.son()["n"], 4)
        self.assertFalse(oyun.g.ALifeTurkce_Konusma.kapali)

    def test_gec_yuklenen_konusma_baglanir_ve_ceviri_tekrarlanmaz(self):
        oyun = Oyun(geciken="Speech")
        self.assertEqual(len(oyun.g.BOOT), 1)
        oyun.baslat()
        oyun.baslat()
        oyun.cevir(EN[ORNEK_ANAHTAR])
        self.assertEqual(oyun.g.ProjectALife.Text.metrics.lookups, 1)
        oyun.goster(HARFLER)
        self.assertEqual(oyun.son()[5], "Small")
        self.assertEqual(len(oyun.g.CIZIM), 1)

    def test_gec_yuklenen_ceviri_yolu_baglanir(self):
        oyun = Oyun(geciken="AudioPolicy")
        oyun.baslat()
        self.assertEqual(oyun.cevir(EN[ORNEK_ANAHTAR]), TR[ORNEK_ANAHTAR])
        oyun.goster(HARFLER)
        self.assertEqual(oyun.g.FONT_DENEME, 1)

    def test_sayline_yolu_cevrilir(self):
        oyun = Oyun()
        metin = EN[ORNEK_ANAHTAR]
        oyun.g.ProjectALife.Speech.sayLine(oyun.g.SHELL, metin, "directed")
        self.assertEqual(oyun.g.SON_SAY, oyun.cevir(metin))
        self.assertNotEqual(oyun.g.SON_SAY, metin)

    def test_uzaktan_duyulan_uyari_cevrilir(self):
        oyun = Oyun()
        oyun.lua.execute("""
            ProjectALife.ModuleCareful = { relay = function(shell, player, text) SON_HALE = text return true end }
            CEVIRILER[ProjectALife.Text.key("IGUI_ALifeUI_", "Far shout")] = "Uzak bağırış"
            ProjectALife.Text.flush()
            for _, f in ipairs(BASLA) do f() end
            ProjectALife.ModuleCareful.relay(nil, nil, "Far shout")
        """)
        self.assertEqual(oyun.g.SON_HALE, "Uzak bağırış")

    def test_say_yolu_degistirilmez(self):
        oyun = Oyun()
        self.assertTrue(oyun.lua.eval("ProjectALife.Speech.engineSay == ASIL_ENGINE_SAY"))
        oyun.g.ProjectALife.Speech.engineSay(oyun.g.SHELL, HARFLER)
        self.assertEqual(oyun.g.SON_SAY, HARFLER)
        self.assertEqual(oyun.g.SAY, 1)

    def test_ek_yokken_font_parametresi_gonderilmez(self):
        oyun = Oyun(ek=False)
        oyun.goster(HARFLER)
        self.assertEqual(oyun.son()["n"], 4)
        self.assertNotEqual(oyun.son()[5], "Small")

    def test_tum_olceklerde_small_fontunun_turkce_glifleri_var(self):
        for scale in ("1x", "2x", "3x", "4x"):
            for name in ("zomboidSmall", "zomboidSmallDyslexic"):
                path = OYUN / "media/fonts/EN" / scale / (name + ".fnt")
                with self.subTest(font=str(path)):
                    text = path.read_text(encoding="utf-8-sig")
                    ids = set(map(int, re.findall(r"^char id=(\d+)", text, re.M)))
                    self.assertEqual([c for c in HARFLER if ord(c) not in ids], [])
                    pages = re.findall(r'^page id=\d+ file="([^"]+)"', text, re.M)
                    self.assertTrue(pages)
                    self.assertTrue(all((path.parent / page).is_file() for page in pages))

    def test_dialogue_fontunda_eksik_glifler_negatif_kontrol(self):
        text = (OYUN / "media/fonts/zomboidDialogue.fnt").read_text(encoding="utf-8-sig")
        ids = set(map(int, re.findall(r"^char id=(\d+)", text, re.M)))
        self.assertEqual({c for c in HARFLER if ord(c) not in ids}, set("ĞğİŞş"))

    def test_paketlenmis_ascii_ek_ayni_metni_cizer(self):
        config = runpy.run_path(str(KOK / "araclar/workshop_kur.py"))
        packed = config["ek_metni"]("ALifeTR_Konusma.lua")
        packed.encode("ascii")
        oyun = Oyun(ek=False)
        oyun.lua.execute(packed)
        text = oyun.cevir(EN[ORNEK_ANAHTAR])
        oyun.goster(text)
        self.assertEqual(oyun.son()[1], TR[ORNEK_ANAHTAR])
        self.assertEqual(oyun.son()[5], "Small")


def main():
    global EK, MOD_LUA, OYUN
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ek", type=Path, default=EK)
    parser.add_argument("--mod-lua", type=Path, default=MOD_LUA)
    parser.add_argument("--oyun", type=Path, default=OYUN)
    parser.add_argument("--rapor", type=Path)
    args = parser.parse_args()
    EK, MOD_LUA, OYUN = args.ek, args.mod_lua, args.oyun
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(KonusmaFontTesti)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.rapor:
        report = {
            "scope": "Lua 5.1; installed A-Life source; simulated drawing calls",
            "addon": str(EK),
            "addon_sha256": hashlib.sha256(EK.read_bytes()).hexdigest(),
            "upstream_sha256": {
                ad: hashlib.sha256((MOD_LUA / ad).read_bytes()).hexdigest() for ad in MOD_DOSYALARI
            },
            "tests_run": result.testsRun,
            "failures": [name.id() for name, _ in result.failures],
            "errors": [name.id() for name, _ in result.errors],
            "delivered_lines_checked": len(TR),
            "native_game_render_verified": False,
            "multiplayer_verified": False,
        }
        args.rapor.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
