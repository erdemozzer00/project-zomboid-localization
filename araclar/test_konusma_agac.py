"""Konuşma ağaçları (1.5.0) için ek: modun gerçek ağaç motoru, sunucu söyleme yolu ve istemci paneliyle uçtan uca.

Çalıştırma: python -B -X utf8 araclar/test_konusma_agac.py
Gereksinim: lupa. Çeviriler sahtedir ("TR<...>"); anahtarlar agac_cikar.py'nin Y4/Y5 için ürettiğiyle aynı yoldan gelir.
Denetlenen: oyuncu sorusu (promptRows) ve seçenek (runRows) düğmeleri Türkçe, "[Charm] " öneki İngilizce kalır, oyuncunun
yankısı öneki söker; NPC sözü TreeServer.say ile aynı render + caption yolundan Türkçe; NPC sözü olarak noktalı çevrilmiş
aynı İngilizce düğmede noktasız; panel modülü yokken ek sessiz, sonradan yüklenince OnGameStart'ta bağlanır; dil Türkçe
değilse hiçbir şey değişmez. Oyun içi çizimi doğrulamaz.
"""
import sys
import unittest
from pathlib import Path

from lupa.lua51 import LuaRuntime

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
import agac_cikar  # noqa: E402
import workshop_kur  # noqa: E402

PANEL = "client/ProjectALife/UI2/ALifeUI2TalkTrees.lua"
EK = workshop_kur.ek_metni("ALifeTR_Konusma.lua")


class Oyun:
    def __init__(self, dil="TR", panel_once=True):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        g = self.g = self.lua.globals()
        g.DIL = dil
        dosyalar = {f.stem[len("ALifeTrees_"):]: f for f in agac_cikar.VERI.glob("ALifeTrees_*.lua")}

        def yukle(yol):
            yol, onek = str(yol), "ProjectALife/Talk/Trees/Data/ALifeTrees_"
            if yol.startswith(onek) and yol[len(onek):] in dosyalar:
                return self.lua.execute(dosyalar[yol[len(onek):]].read_text(encoding="utf-8-sig"))
            return None

        g.A_yukle = yukle
        self.lua.execute("""
            require = function(p) return A_yukle(p) end
            ProjectALife = {}
            ProjectALife.Experiments = { enabled = function() return true end }
            CEVIRILER, LOG, BASLA, BOOT, YANKI = {}, {}, {}, {}, {}
            UIFont = { Small = "Small" }
            Translator = { getLanguage = function() return { name = function() return DIL end } end }
            getTextOrNull = function(key) return CEVIRILER[key] end
            print = function(s) LOG[#LOG + 1] = tostring(s) end
            Events = { OnGameBoot = { Add = function(f) BOOT[#BOOT + 1] = f end },
                       OnGameStart = { Add = function(f) BASLA[#BASLA + 1] = f end } }
        """)
        for ad in agac_cikar.MOD_DOSYALARI[:5]:  # Text, AudioPolicy, Speech, TreeRegistry, TreeEngine
            self.lua.execute((agac_cikar.MOD_LUA / ad).read_text(encoding="utf-8-sig"))
        self.lua.execute(agac_cikar.YARDIMCI)
        g.ProjectALife.TreeRegistry.load()
        if panel_once:
            self.panel_yukle()
        self.lua.execute(EK)

    def panel_yukle(self):
        self.lua.execute((agac_cikar.MOD_LUA / PANEL).read_text(encoding="utf-8-sig"))

    def oyun_basla(self):
        self.lua.execute("for _, f in ipairs(BASLA) do f() end")

    def cevir(self, en, tr):
        self.g.CEVIRILER[self.g.ProjectALife.Text.lineKey(en)] = tr

    def ilk_agac(self, kosul):
        R = self.g.ProjectALife.TreeRegistry
        for i in range(1, len(R.trees) + 1):
            t = R.trees[i]
            if kosul(t):
                return t
        raise AssertionError("uygun ağaç yok")

    def gorunum(self, tree, dugum="start"):
        ctx = self.lua.eval("{ charm = 100, repLevel = 4, opinion = 100, day = 1, flags = {}, tasks = {} }")
        return self.g.ProjectALife.TreeEngine.nodeView(tree, dugum, ctx, self.lua.table(), 1)

    def charmli_dugum(self):
        """[Charm] etiketli seçeneği olan ilk düğüm."""
        E, R = self.g.ProjectALife.TreeEngine, self.g.ProjectALife.TreeRegistry
        for i in range(1, len(R.trees) + 1):
            t = R.trees[i]
            for nid, node in t.nodes.items():
                ch = node._choices
                for j in range(1, len(ch) + 1):
                    if E.charmTagged(ch[j]) and "{" not in ch[j].text:
                        return t, nid
        raise AssertionError("charm seçeneği yok")


class AgacEkiTesti(unittest.TestCase):
    def test_soru_dugmesi_cevrilir(self):
        o = Oyun()
        E, C = o.g.ProjectALife.TreeEngine, o.g.ProjectALife.UI2TalkTrees
        t = o.ilk_agac(lambda t: "{" not in t.prompt)
        en = E.clean(E.fill(t.prompt, o.lua.table()))
        o.cevir(en, "TR<soru>")
        satir = o.lua.table_from({"id": t.id, "text": en})
        win = o.lua.table_from({"treeOffer": o.lua.table_from({"World": o.lua.table_from([satir])})})
        win.topic = "World"
        rows = C.promptRows(win, "World")
        self.assertEqual(rows[1].text, "TR<soru>")
        self.assertEqual(rows[1].treePrompt, t.id)
        # classicRows (eski pencere) aynı C.promptRows'u çağırır
        win.topic = "Personal"
        win.treeOffer.Personal = o.lua.table_from([o.lua.table_from({"id": t.id, "text": en})])
        self.assertEqual(C.classicRows(win)[1].text, "TR<soru>")

    def test_secenek_ve_charm_oneki(self):
        o = Oyun()
        E, C = o.g.ProjectALife.TreeEngine, o.g.ProjectALife.UI2TalkTrees
        t, nid = o.charmli_dugum()
        v = o.gorunum(t, nid)
        beklenen = []
        for i in range(1, len(v.choices) + 1):
            metin = str(v.choices[i].text)
            govde = metin[len("[Charm] "):] if metin.startswith("[Charm] ") else metin
            o.cevir(govde, f"TR<{i}>")
            beklenen.append(("[Charm] " if metin.startswith("[Charm] ") else "") + f"TR<{i}>")
        self.assertTrue(any(b.startswith("[Charm] ") for b in beklenen))
        win = o.lua.table_from({"treeRun": o.lua.table_from({"topic": "World", "choices": v.choices})})
        rows = C.runRows(win)
        self.assertEqual([str(rows[i].text) for i in range(1, len(rows) + 1)], beklenen)
        # seçilen düğmenin yankısı: mod "[Charm] " önekini söküp Türkçe gövdeyi yazar, caption onu bozmaz
        o.lua.execute("""
            YANKI_WIN = { append = function(self, text, who) YANKI[#YANKI + 1] = ProjectALife.AudioPolicy.caption(text) end,
                          refreshChoices = function() end, playerNum = 0 }
            getSpecificPlayer = function() return nil end
        """)
        secilen = next(i for i in range(1, len(rows) + 1) if str(rows[i].text).startswith("[Charm] ") and not rows[i].locked)
        o.g.YANKI_WIN.treeRun = o.lua.table_from({"tree": t.id, "topic": "World"})
        C.choose(o.g.YANKI_WIN, rows[secilen])
        self.assertEqual(o.g.YANKI[1], beklenen[secilen - 1][len("[Charm] "):])

    def test_npc_sozu_sunucu_yolundan_cevrilir(self):
        o = Oyun()
        Sp, P = o.g.ProjectALife.Speech, o.g.ProjectALife.AudioPolicy
        t = o.ilk_agac(lambda t: True)
        v = o.gorunum(t)
        gosterilen = Sp.render(v.text, o.lua.table(), None, None)  # TreeServer.say
        o.cevir(gosterilen, "TR<npc>")
        self.assertEqual(P.caption(gosterilen), "TR<npc>")  # panel:append ve baş üstü yazı bu yoldan

    def test_npc_sozu_noktasi_dugmede_duser(self):
        o = Oyun()
        E, C = o.g.ProjectALife.TreeEngine, o.g.ProjectALife.UI2TalkTrees
        t = o.ilk_agac(lambda t: "{" not in t.prompt)
        en = E.clean(E.fill(t.prompt, o.lua.table()))
        o.cevir(en, "Tamam.")
        win = o.lua.table_from({"treeOffer": o.lua.table_from({"World": o.lua.table_from([o.lua.table_from({"id": t.id, "text": en})])})})
        self.assertEqual(C.promptRows(win, "World")[1].text, "Tamam")
        o.cevir("Wait up", "Bekle...")  # "..." korunur (Text.lookup önbelleği yüzünden ayrı metin)
        win.treeOffer.World[1].text = "Wait up"
        self.assertEqual(C.promptRows(win, "World")[1].text, "Bekle...")

    def test_cevirisi_olmayan_ingilizce_kalir(self):
        o = Oyun()
        C = o.g.ProjectALife.UI2TalkTrees
        win = o.lua.table_from({"treeOffer": o.lua.table_from({"World": o.lua.table_from([o.lua.table_from({"id": "x", "text": "Zzz unknown"})])})})
        self.assertEqual(C.promptRows(win, "World")[1].text, "Zzz unknown")

    def test_panel_sonradan_yuklenir(self):
        o = Oyun(panel_once=False)
        self.assertFalse(any("kapatildi" in str(s) for s in o.g.LOG.values()))
        o.panel_yukle()
        o.oyun_basla()
        o.cevir("Who are you", "TR<kim>")
        C = o.g.ProjectALife.UI2TalkTrees
        self.assertTrue(C.ALifeTurkceKurulu)
        win = o.lua.table_from({"treeOffer": o.lua.table_from({"World": o.lua.table_from([o.lua.table_from({"id": "x", "text": "Who are you"})])})})
        self.assertEqual(C.promptRows(win, "World")[1].text, "TR<kim>")

    def test_panel_hic_yoksa_sessiz(self):
        o = Oyun(panel_once=False)
        o.oyun_basla()
        self.assertIsNone(o.g.ProjectALife.UI2TalkTrees)
        self.assertFalse(o.g.ALifeTurkce_Konusma.kapali)

    def test_dil_turkce_degilse_dokunmaz(self):
        o = Oyun(dil="EN")
        C = o.g.ProjectALife.UI2TalkTrees
        o.cevir("Who are you", "TR<kim>")
        win = o.lua.table_from({"treeOffer": o.lua.table_from({"World": o.lua.table_from([o.lua.table_from({"id": "x", "text": "Who are you"})])})})
        self.assertEqual(C.promptRows(win, "World")[1].text, "Who are you")

    def test_y4_haritasi_ile_ayni_anahtar(self):
        """Gemini girdisindeki anahtar, ekin düğmede baktığı anahtarla aynı (soru ve seçenek)."""
        o = Oyun()
        E = o.g.ProjectALife.TreeEngine
        harita = KOK / "rapor" / "Y4_harita.json"
        if not harita.exists():
            self.skipTest("Y4 haritası yok")
        import json
        satirlar = json.loads(harita.read_text(encoding="utf-8"))["satirlar"]
        dugmeler = [v for v in satirlar.values() if v[2][2].startswith(("soru", "secenek"))][:200]
        self.assertTrue(dugmeler)
        for k, en, _ in dugmeler:
            self.assertEqual(o.g.ProjectALife.Text.lineKey(E.clean(en)), k)


if __name__ == "__main__":
    unittest.main(verbosity=1)
