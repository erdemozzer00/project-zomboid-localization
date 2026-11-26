"""L152 presentation regressions against the installed 1.5.2 Lua modules."""
import json
from pathlib import Path
import unittest

from lupa import LuaRuntime
from lupa.lua51 import LuaRuntime as Lua51Runtime

from lua_cikar import MOD
from workshop_kur import ek_metni


ROOT = Path(__file__).resolve().parent.parent


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


class L152Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MOD.is_dir():
            raise unittest.SkipTest("Project A-Life Lua source is unavailable")
        cls.ig = read_json(ROOT / "teslim/IG_UI.json")
        cls.rd = read_json(ROOT / "teslim/RadioData.json")
        cls.patch = ek_metni("ALifeTR_L152.lua")
        cls.speech_patch = ek_metni("ALifeTR_Konusma.lua")
        cls.sources = {}
        for name in (
            "ALifeText", "ALifeAudioPolicy", "ALifeSpeech", "ALifePhonesData", "ALifePhones",
            "ALifePhonesClient", "ALifeUI2Answer", "ALifeUI2TalkAsk", "ALifeMapLabels",
            "ALifeMissionDefs", "ALifeMissionRules", "ALifeUI2Missions", "ALifeUI2TalkTrees",
        ):
            path = next(MOD.rglob(f"{name}.lua"))
            cls.sources[name] = path.read_text(encoding="utf-8-sig")
        steamapps = next(parent for parent in MOD.parents if parent.name == "steamapps")
        vanilla_path = steamapps / "common/ProjectZomboid/media/lua/shared/Translate/TR/IG_UI.json"
        cls.vanilla = read_json(vanilla_path) if vanilla_path.exists() else {
            "IGUI_warehouseKey": "Depo / Antrepo", "IGUI_FactoryKey": "Fabrika",
        }

    def setUp(self):
        self.start()

    def start(self, patch_before_game=False, runtime=LuaRuntime):
        self.lua = runtime()
        g = self.lua.globals()
        g.lookup = self.lookup
        self.hidden = set()
        self.lua.execute("""
            function require() end
            function isClient() return client == true end
            function isServer() return server == true end
            function getTextOrNull(key) if lang == "TR" then return lookup(key) end end
            function event()
                local callbacks = {}
                return { callbacks = callbacks, Add = function(fn) callbacks[#callbacks+1] = fn end,
                         fire = function(...) for _, fn in ipairs(callbacks) do fn(...) end end }
            end
            lang, client = "TR", true
            Events = { OnGameBoot = event(), OnServerCommand = event() }
            Translator = { getLanguage = function() return { name = function() return lang end } end }
            ISCollapsableWindow = { derive = function() return {} end }
            local player = { getDescriptor = function() return { getForename = function() return "Ada%2" end } end }
            function getSpecificPlayer() return player end
            ProjectALife = {
                UI2Hud = { register = function() end }, UI2Keys = { register = function() end },
                UI2TalkTone = { kinds = {}, of = function() return "plain" end },
                UI2Talk = { Window = {}, text = function(s) return ProjectALife.Text.ui(s) end },
                TalkMenu = { Window = {} },
            }
        """)
        if patch_before_game:
            self.lua.execute(self.patch)
        for code in self.sources.values():
            self.lua.execute(code)
        self.lua.execute(self.speech_patch)
        if not patch_before_game:
            self.lua.execute(self.patch)
        self.project = g.ProjectALife

    def lookup(self, key):
        if key not in self.hidden:
            return self.ig.get(key, self.rd.get(key, self.vanilla.get(key)))

    def test_board_speech_and_joined_offers_keep_runtime_values(self):
        manifest = read_json(ROOT / "paketler/haritalar/TB_GENEL_harita.json")
        check = self.lua.eval("""function(en, question)
            local P = ProjectALife
            local raw = P.Speech.render(en, {
                where = "the house near Rosewood, about 120 meters east", name = "Ada%2",
            })
            if question ~= nil then raw = raw .. "... " .. question end
            local tr = P.AudioPolicy.caption(raw)
            assert(tr ~= raw and not string.find(tr, "{", 1, true), raw)
            if string.find(en, "{where}", 1, true) then
                assert(string.find(tr, "Rosewood", 1, true) and string.find(tr, "120", 1, true), tr)
            end
            if string.find(en, "{name}", 1, true) then
                assert(string.find(tr, "Ada%2", 1, true), tr)
            end
        end""")
        rows, technical = manifest["satirlar"], manifest["_teknik"]
        for no in technical["kalip_satirlari"]:
            check(rows[str(no)][1], None)
        for no in technical["birlesen_teklif_satirlari"]:
            for question in technical["yaklasim_sorusu_satirlari"]:
                check(rows[str(no)][1], rows[str(question)][1])

    def test_board_stage_templates_and_tree_notifications(self):
        data = next(MOD.rglob("ALifeTaskBoardData.lua")).read_text(encoding="utf-8-sig")
        self.lua.execute(data)
        self.lua.execute("""
            local P = ProjectALife
            local M = P.UI2Missions
            assert(M.text("Treat the wounded at the marker") ~= "Treat the wounded at the marker")
            assert(M.text("Get to the house") ~= "Get to the house")
            local detail = M.text("About 120 meters east. About 15 minutes left on site")
            assert(detail:find("120") and detail:find("15") and not detail:find("About"), detail)
            for _, unlock in pairs(P.TaskBoardData.unlockLabels) do
                local raw = "Task complete, " .. unlock:lower() .. " unlocked"
                assert(M.text(raw) ~= raw, raw)
            end
            assert(M.text("Bring supplies (3)") ~= "Bring supplies (3)")
            local panel = { refreshChoices = function() end, append = function(self, text) self.text = text end }
            local args = { ok = true, notes = { "New task: Bring supplies (3)" } }
            P.UI2TalkTrees.result(panel, args)
            assert(panel.text:find("(3)", 1, true) and not panel.text:find("Bring supplies", 1, true))
            assert(args.notes[1] == "New task: Bring supplies (3)")
        """)

    def test_creator_and_display_hooks_keep_original_data(self):
        share = next(MOD.rglob("ALifeFactionShare.lua")).read_text(encoding="utf-8-sig")
        start = share.index("function Share.describeMissing(")
        end = share.index("\nfunction ", start + 1)
        self.lua.execute("local Share = {}; ProjectALife.FactionShare = Share\n" + share[start:end])
        self.lua.execute("""
            local window = { statusLabel = { setName = function(self, name) self.name = name end } }
            ProjectALife.CreatorScreen = {
                window = window,
                paintSaveStatus = function(_, text) return text end,
                importFactionPack = function(w)
                    w.statusLabel:setName("MISSING ITEMS - 7 - FULL LIST IN CONSOLE.TXT")
                    return true
                end,
            }
            ISModalDialog = { new = function(_, x, y, w, h, text) return text end }
            ProjectALife.UIPos = { editorPaint = function(panel) panel:drawText("X (not showing now)") end }
            RWMChannel = { addComboOption = function(_, freq, name) return freq .. " " .. name end }
            Events.OnGameBoot.fire()
            local P, C = ProjectALife, ProjectALife.CreatorScreen
            local raw = "Delete this NPC?"
            assert(ISModalDialog:new(0, 0, 1, 1, raw, true, {window = window}) ~= raw)
            assert(ISModalDialog:new(0, 0, 1, 1, raw, true, {window = {}}) == raw)
            assert(C.paintSaveStatus({}, "Game day: use whole numbers from 0.", "error"):find("0"))
            assert(not C.paintSaveStatus({}, "Game day: use whole numbers from 0.", "error"):find("Game day", 1, true))
            assert(C.importFactionPack(window) and window.statusLabel.name:find("7"))
            assert(not window.statusLabel.name:find("MISSING ITEMS", 1, true))
            local report = { mods = {{ name = "My Mod", workshop = "123", items = {"Base.Box"} }},
                items = {"Base.One", "Base.Two", "Base.Three", "Base.Four"} }
            local description = P.FactionShare.describeMissing(report)
            assert(description:find("My Mod", 1, true) and description:find("123", 1, true))
            assert(description:find("Base.Three", 1, true) and not description:find("Unknown items", 1, true))
            local panel = { drawText = function(self, text) self.text = text end }
            P.UIPos.editorPaint(panel)
            assert(panel.text ~= "X (not showing now)")
            panel:drawText("X (not showing now)")
            assert(panel.text == "X (not showing now)")
            assert(RWMChannel:addComboOption(99600, "Knox County Radio") ~= "99600 Knox County Radio")
        """)

    def test_phone_badges_preserve_option_ids(self):
        self.lua.execute("""
            local P = ProjectALife.PhonesClient
            local tree = ProjectALife.Phones.tree(1)
            P.call = {tree = tree, node = tree.start, asked = {}, state = {}, you = "Ada"}
            local tags = {"REP 1", "FIRST AID 2", "FIRST AID 3", "MECHANICS 2", "MECHANICS 3"}
            function ProjectALife.Phones.visible()
                local options = {}
                for _, tag in ipairs(tags) do options[#options + 1] = {id = tag, label = "Example", tag = tag} end
                return options
            end
            local ask = P.buildAsk()
            for index, tag in ipairs(tags) do
                local row = ask.options[index]
                assert(row.id == tag and row.label ~= "[" .. tag .. "] Example")
                assert(row.label:find("Example", 1, true))
            end
        """)

    def test_extraction_marker_legacy_icon_replay_and_cleanup(self):
        self.lua.execute("ProjectALife.AdminConsole = { onReply = function() end }")
        for name in ("ALifeSafehouseClient", "ALifeRadioClient"):
            self.lua.execute(next(MOD.rglob(name + ".lua")).read_text(encoding="utf-8-sig"))
        self.lua.execute("""
            local P = ProjectALife
            local api = { rows = {} }
            function api:getSymbolCount() return #self.rows end
            function api:getSymbolByIndex(index) return self.rows[index + 1] end
            function api:removeSymbolByIndex(index) table.remove(self.rows, index + 1) end
            function api:getDefaultTextLayerID() return "default" end
            function api:addUntranslatedText(text, layer, x, y)
                local row = {
                    getUntranslatedText = function() return text end,
                    setUntranslatedText = function(_, value) text = value end,
                    setRGBA = function(self, r, g, b) self.r, self.g, self.b = r, g, b end,
                    getRed = function(self) return self.r or 0 end,
                    getGreen = function(self) return self.g or 0 end,
                    getBlue = function(self) return self.b or 0 end,
                    setScale = function(self, scale) self.scale = scale end,
                    getScale = function(self) return self.scale or 0 end,
                    getWorldX = function() return x end, getWorldY = function() return y end,
                }
                self.rows[#self.rows + 1] = row
                return row
            end
            ISWorldMap_instance = { mapAPI = { getSymbolsAPI = function() return api end } }
            ISWorldMap = { ShowWorldMap = function() return "open" end }
            P.EndingData = { pad = {x = 10, y = 20}, padOld = {x = 40, y = 50} }
            P.MissionDefs.fallbackOn = function() return false end
            local icons = false
            P.MapLabels.on = function() return icons end
            P.MapLabels.save, P.MapLabels.attach = function() end, function() end
            Events.OnGameBoot.fire()

            local raw = "Extraction zone"
            local key = P.Text.key("IGUI_ALifeUI_", raw, "alifetr.map.tip")
            local args = {id = "ending_zone", kind = "mark", name = raw, x = 10, y = 20}
            api:addUntranslatedText(raw, "default", 60, 20)
            local old = api:addUntranslatedText(raw, "default", 10, 20)
            old:setRGBA(1, 0.7, 0.1, 1)
            old:setScale(1.5)
            local radio = P.RadioClient
            assert(radio.card(args) and args.name == raw)
            assert(#api.rows == 2 and api.rows[2]:getUntranslatedText() == key)
            assert(radio.card(args) and #api.rows == 2)
            assert(radio.card({id = "ending_zone", kind = "drop"}) and #api.rows == 1)
            assert(api.rows[1]:getWorldX() == 60)

            assert(radio.card(args))
            icons = true
            assert(radio.card(args) and #api.rows == 1)
            local row = P.MapLabels.rows[P.MapLabels.keyOf(raw, 10, 20)]
            assert(row and row.kind == "extraction" and P.MapLabels.tipLines(row)[1].text == P.Text.lookup(key))
            icons = false
            assert(radio.card(args) and #api.rows == 2)
            assert(not P.MapLabels.rows[P.MapLabels.keyOf(raw, 10, 20)])
            assert(radio.card({id = "ending_zone", kind = "drop"})
                and #api.rows == 1 and not P.MapLabels.rows[P.MapLabels.keyOf(raw, 10, 20)])

            local other = {id = "radio_other", kind = "mark", name = raw, x = 25, y = 20}
            assert(radio.card(other) and api.rows[2]:getUntranslatedText() == raw)
            local trLookup = getTextOrNull
            function getTextOrNull(k)
                if k == key and lang == "EN" then return raw end
                return trLookup(k)
            end
            lang = "EN"
            P.Text.flush()
            assert(radio.card(args) and api.rows[3]:getUntranslatedText() == key)
            assert(P.Text.lookup(key) == raw)
            assert(radio.card({id = "ending_zone", kind = "drop"}))
            local saved = api:addUntranslatedText(raw, "default", 40, 50)
            saved:setRGBA(1, 0.7, 0.1, 1)
            saved:setScale(1.5)
            local note = api:addUntranslatedText(raw, "default", 40, 50)
            assert(ISWorldMap.ShowWorldMap() == "open")
            assert(saved:getUntranslatedText() == key and note:getUntranslatedText() == raw)
            assert(radio.card({id = "ending_zone", kind = "drop"}))
            assert(api.rows[#api.rows] == note)
        """)

    def test_creator_main_menu_title_is_measured_and_drawn_in_turkish(self):
        self.lua.execute("""
            UIFont = {Medium = 1, Large = 2, Small = 3}
            function getTextManager()
                return {getFontHeight = function() return 12 end, MeasureStringX = function() return 160 end}
            end
            ProjectALife.CreatorScreen = {open = function() end, menuSubtitle = function() return "Subtitle" end,
                shortItemName = function(id) return id:match("%.(.+)$") or id end,
                fitText = function(s) return s end, openItemPicker = function(window, kind, slot, combo, title)
                    local label = {name = string.upper(title), setNameWithoutMoving = function(self, s) self.name = s end}
                    window.itemPicker = {children = {label}}
                end}
            function getItemNameFromFullType(id)
                if id == "Base.Crowbar" then return "Levye" end
                if id == "Example.CustomBat" then return "Custom bat display name" end
                return id
            end
            ProjectALife.Version = {calmFont = function(font) return font end, clean = function() return true end}
            local function draw(self, text) self.shown = text end
            ProjectALife.UI2Chrome = {
                track = function() return 1 end,
                boldWidth = function(_, s, track) measured = s; spacing = track; return utf8.len(s) * 8 end,
                capsFit = function() error("Original fitting must not split the translated title") end,
                softText = draw, boldText = draw,
            }
        """)
        source = next(MOD.rglob("ALifeCreatorMenuTile.lua")).read_text(encoding="utf-8-sig")
        self.lua.execute(source)
        self.lua.execute(ek_metni("ALifeTR_Creator.lua"))
        self.lua.execute("""
            local tile = ProjectALife.CreatorScreen.menuTile
            local color = {r = 0, g = 0, b = 0}
            tile.tones = function()
                return {panel = color, optSelect = color, line = color,
                    optLight = color, text = color, faint = color, dim = color}
            end
            tile.sprite = function() end
            tile.version = function() return "" end
            local approved = ProjectALife.Text.ui("A-LIFE CREATOR")
            assert(approved ~= "A-LIFE CREATOR")
            local panel = {width = 440, height = 75, drawRect = function() end, drawText = function() end}
            tile.draw(panel)
            assert(panel.shown == approved and measured == approved and spacing == 0)
            panel.width = 200
            tile.draw(panel)
            assert(panel.shown:match("^A%-LIFE ") and panel.shown:sub(-2) == ".." and utf8.len(panel.shown))
            local creator, window = ProjectALife.CreatorScreen, {}
            creator.openItemPicker(window, "clothing", "Back", {}, "Back choices")
            local text = ProjectALife.Text
            local back = text.ui("BACK")
            assert(back ~= "BACK")
            assert(window.itemPicker.children[1].name == text.fill(text.ui("{x} choices"), {x = back}))
            creator.openItemPicker(window, "weapon", "Back", {}, "Back choices")
            assert(window.itemPicker.children[1].name == "BACK CHOICES")
            assert(creator.shortItemName("Base.Crowbar") == "Levye")
            assert(creator.shortItemName("Example.CustomBat") == "Custom bat display name")
            assert(creator.shortItemName("Example.Missing") == "Missing")
            assert(creator.shortItemName("none") == "none")
        """)

    def test_creator_outfit_badge_leaves_room_after_the_translated_title(self):
        self.lua.execute("""
            unpack = table.unpack
            UIFont = {Small = 1}
            function getTextManager()
                return {MeasureStringX = function(_, _, name) return utf8.len(name) * 8 end}
            end
            local function control(x, name)
                local noop = function() end
                return {x = x, name = name, font = 1, initialise = noop, instantiate = noop,
                    setX = function(self, x) self.x = x end,
                    setWidth = function(self, width) self.width = width end,
                    setName = function(self, name) self.name = name end}
            end
            ISButton = {new = function(_, x, y, w) local b = control(x); b.width = w; return b end}
            local Creator = {px = function(n) return n end, outfitIds = {}, addTooltip = function() end,
                addButton = function(_, x) return control(x) end,
                fitText = function(s) return s end,
                addLabel = function(page, x, _, name, _, _, room)
                    if room and #name * 8 > room then name = 'Eyeshado...' end
                    local label = control(x, name)
                    page:addChild(label)
                    return label
                end}
            ProjectALife.CreatorScreen = Creator
            Creator.open = function(width)
                local window = {page = {children = {}, addChild = function(self, c) table.insert(self.children, c) end}}
                Creator.window = window
                window.title = Creator.addLabel(window.page, 12, 0, 'OUTFIT SETS')
                window.eye = Creator.addLabel(window.page, 12, 30, 'Eyeshadow', nil, nil, 58)
                Creator.outfitHealth.install(window, window.page, width, 0)
                return window
            end
        """)
        source = next(MOD.rglob("ALifeCreatorOutfitHealth.lua"))
        self.lua.execute(source.read_text(encoding="utf-8-sig"))
        self.lua.execute(ek_metni("ALifeTR_Creator.lua"))
        self.lua.execute("""
            local C = ProjectALife.CreatorScreen
            local title = ProjectALife.Text.ui('OUTFIT SETS')
            assert(title ~= 'OUTFIT SETS')
            for _, width in ipairs({310, 520}) do
                local w = C.open(width)
                assert(w.eye.name == 'Far')
                if width == 520 then assert(w.title.name == title) end
                assert(w.healthBadge.x >= w.title.x + utf8.len(w.title.name) * 8 + 8)
                assert(w.healthBadge.x + w.healthBadge.width == w.healthFixButton.x - 8)
            end
            assert(C.fitText('ABCDŞDEFG', 1, 56) == 'ABCD...')
        """)

    def test_creator_rule_tooltips_in_both_scopes_and_after_option_changes(self):
        self.start(runtime=Lua51Runtime)
        rows = read_json(ROOT / "paketler/haritalar/AL_OLUSTURUCU_KURAL_harita.json")["satirlar"]
        self.ig = dict(self.ig)
        for key, _, _ in rows.values():
            self.ig.pop(key, None)
        core = next(MOD.rglob("ALifeCreatorCore.lua")).read_text(encoding="utf-8-sig")
        tables = core[core.index("local MEMBER_MODULES ="):core.index("local MODULE_STATES =")]
        builder = core[core.index("local function buildModuleOverrideCards("):core.index("local function addRatingSlider(")]
        self.lua.execute("""
            UIFont = {Small = 1}
            local function size(n) return n end
            Creator = {px = size, rowHeight = size, fontHeight = size,
                moduleControlLabel = function(spec) return spec[1] end}
            ProjectALife.CreatorScreen = Creator
            function addSectionCard(panel) return panel end
            function addButton() end
            function addLabel(panel, x, y, title)
                local label = {}
                table.insert(panel.children, label)
                panel.labels[title] = label
                return label
            end
            function addCombo(panel, x, y, w, states)
                local combo = {state = states[1][2], map = true}
                combo.getOptionData = function(self) return self.state end
                table.insert(panel.children, combo)
                return combo
            end
            function addTooltip(widget, text)
                widget.tooltip = widget.map and {defaultTooltip = text} or text
            end
            function addInfoBadge(panel, x, y, tip)
                local badge = {tooltip = tip}
                table.insert(panel.children, badge)
                table.insert(panel.badges, badge)
            end
            function Creator.open(scope)
                local w = {children = {}, labels = {}, badges = {}, combos = {}, prerender = function() end}
                Creator.window = w
                Creator.buildModuleOverrideCards(w, 0, 0, 600, w.combos, scope)
                return w
            end
        """)
        self.lua.execute(tables + "\nCreator.memberModules = MEMBER_MODULES\n" + builder)
        for module in ("ALifeModuleRules", "ALifeCreatorModuleRules"):
            self.lua.execute(next(MOD.rglob(module + ".lua")).read_text(encoding="utf-8-sig"))
        extra_note = "Additional rule from another mod."
        self.lua.execute("table.insert(ProjectALife.ModuleRules.entries, {module='fear', note=...})", extra_note)
        self.lua.execute(ek_metni("ALifeTR_Creator.lua"))
        self.lua.execute("Events.OnGameBoot.fire()")
        creator = self.project.CreatorScreen
        for language, available in (("TR", 0), ("TR", 2), ("TR", 20), ("EN", 20)):
            self.lua.globals().lang = language
            for index, (key, _, _) in rows.items():
                if int(index) <= available:
                    self.ig[key] = f"Ç%1-test-{index}."
            self.project.Text.flush()
            # A real language/dictionary change starts a new game process.
            state = self.lua.globals().ALifeTurkce_Creator
            state.turkce, state.onbellek = None, self.lua.table()
            for scope in ("faction", "member"):
                window = creator.open(scope)
                labels = [v.tooltip for v in window.labels.values()]
                combos = [v.tooltip.defaultTooltip for v in window.combos.values()]
                badges = [v.tooltip for v in window.badges.values()]
                self.assertIn(extra_note, window.combos.fear.tooltip.defaultTooltip)
                if language == "TR":
                    base = window.combos.fear.ruleTip.split(" RULES: ", 1)[0]
                    self.assertNotEqual(self.project.Text.ui(base), base)
                    self.assertIn(self.project.Text.ui(base), window.combos.fear.tooltip.defaultTooltip)
                    self.assertNotIn("World switches and valid task conditions", window.combos.fear.tooltip.defaultTooltip)
                for key, en, _ in rows.values():
                    expected = self.ig.get(key, en) if language == "TR" else en
                    for visible in (labels, combos, badges):
                        self.assertTrue(any(expected in tip for tip in visible), (scope, en))
                for module, dependency, row in (("meleeCaution", "withdraw", "10"),
                                                ("meleeIntimidate", "warning", "11"),
                                                ("weaponSwitchMelee", "zombieAvoid", "9")):
                    combo = window.combos[module]
                    raw = combo.ruleTip
                    for choice in ("on", "off"):
                        combo.state, window.combos[dependency].state = choice, "off"
                        creator.refreshModuleRuleHints(window.combos)
                        warning = combo.tooltip.defaultTooltip
                        key, en, _ = rows[row]
                        expected = self.ig.get(key, en) if language == "TR" else en
                        self.assertEqual(warning.count(expected), 2 if choice == "on" else 1)
                        self.assertEqual(combo.ruleTip, raw)
                        self.assertEqual(combo.getOptionData(combo), choice)
                        for _ in range(15):
                            window.prerender(window)
                        self.assertEqual(combo.tooltip.defaultTooltip, warning)
                        if language == "EN" and choice == "off":
                            self.assertEqual(warning, raw)

    def test_boot_and_repeat_load_preserve_the_same_wrappers(self):
        self.start(patch_before_game=True)
        self.lua.execute("""
            local P = ProjectALife.PhonesClient
            previous = P.line
            Events.OnGameBoot.fire()
            assert(P.line ~= previous)
            installed = P.line
        """)
        self.lua.execute(self.patch)
        self.lua.execute("""
            local P = ProjectALife.PhonesClient
            Events.OnGameBoot.fire()
            assert(P.line == installed)
            assert(P.line("I have to go", {state = {}}) ~= "I have to go")
        """)

    def test_status_window_and_door_captions_use_the_exact_translation_paths(self):
        values = {
            "IGUI_ALifeUI_0c999e3722da3d6a": "Waiting TR",
            "RD_ALifeLine_5359b13d505dae1c": "Company {count}",
            "RD_ALifeLine_4697c88d71172cab": "Census {count}",
        }
        self.lua.globals().lookup = lambda key: values.get(key) or self.lookup(key)
        self.lua.execute("""
            local P = ProjectALife
            P.Version = {title = function(text) return text .. " v1.5.2" end}
            ALifeStatusWindow = {
                new = function() return {
                    title = P.Version.title("Project A-Life Status"),
                    setTitle = function(self, title) self.title = title end,
                } end,
                statusRows = function() return {{text = "Waiting for server status..."}, {text = "Other"}} end,
            }
            Events.OnGameBoot.fire()
            local approved = P.Text.ui("Project A-Life Status")
            assert(approved ~= "Project A-Life Status")
            assert(ALifeStatusWindow:new().title == approved .. " v1.5.2")
            local rows = ALifeStatusWindow.statusRows({})
            assert(rows[1].text == "Waiting TR" and rows[2].text == "Other")
            assert(ALifeStatusWindow.statusRows({status = {}})[1].text == "Waiting for server status...")
            local caption = P.AudioPolicy.caption
            assert(caption("What now?") == P.Text.lookup("RD_ALifeLine_767c0c125327caaf"))
            local group = "There's 3 of us here, we're together"
            assert(caption(group) == "Company 3")
            assert(caption("There's 1 of us here, we're together") == "There's 1 of us here, we're together")
            local invalid = "Noted. many residents home, and your report about bites. Stay inside. We're moving on."
            assert(caption(invalid) == invalid)
            assert(caption("Noted. 4 residents home, and your report about bites. Stay inside. We're moving on.") == "Census 4")
            lang = "EN"
            assert(ALifeStatusWindow:new().title == "Project A-Life Status v1.5.2")
            assert(caption(group) == group)
        """)

    def test_new_menu_text_uses_clothing_save_and_loan_presentation_hooks(self):
        self.start(runtime=Lua51Runtime)
        samples = {
            "2": "Save {reason}", "3": "Catalog {season} {role} {shown}/{hidden}",
            "4": "Collision {item}, {other}, {slot}.", "5": "Same.", "6": "Also {items}.",
            "7": "Alternative {item}.", "8": "Continue?", "9": "Returned {item}", "10": "Lost {item}",
            "11": "Use the Talk menu TR",
        }
        rows = read_json(ROOT / "paketler/haritalar/AL_MENU_UI_harita.json")["satirlar"]
        values = {rows[n][0]: value for n, value in samples.items()}
        self.lua.globals().lookup = lambda key: values.get(key) or self.lookup(key)
        self.lua.execute("""
            local P = ProjectALife
            P.CreatorScreen = {
                px = function(n) return n end,
                paintSaveStatus = function(label, text, tone) label.text, label.tone = text, tone end,
            }
            P.SafehouseClient = {notice = function(args) shownNotice = args; return true end}
            P.SafehouseDirector = {tell = function(player, text, mark) haloText, haloMark = text, mark end}
            P.ClothingAdvisor = {nameOf = function(id) return id end}
            ISModalDialog = {new = function(_, x, y, w, h, text, yesno, owner, act)
                modalText, modalSubject, modalAct = text, owner, act
                local noop = function() end
                return {initialise = noop, addToUIManager = noop, setAlwaysOnTop = noop, bringToTop = noop}
            end}
        """)
        for module in ("ALifeClothingHealth", "ALifeCreatorClothingView", "ALifeCreatorSaveQueue"):
            self.lua.execute(next(MOD.rglob(module + ".lua")).read_text(encoding="utf-8-sig"))
        self.lua.execute("""
            local P = ProjectALife
            Events.OnGameBoot.fire()
            local View = P.CreatorScreen.clothingView
            local coat = {id = 'coat', label = 'Coat%2'}
            local view = setmetatable({season = 1, role = {kind = 'law'}, confirmed = {},
                collision = function() return {{name = 'Other', slot = 'ShoulderSlot', same = true,
                    alternative = {name = 'Alt'}}, {name = 'Third'}} end}, View)
            assert(view:summaryText(5, 3) == 'Catalog ' .. P.Text.ui('Spring') .. ' ' .. P.Text.ui('Police') .. ' 5/3')
            View.showAll = true
            assert(view:summaryText(5, 3):match('^Everything is listed'))
            assert(view:guard(coat, false, function() confirmed = true end))
            assert(modalText == 'Collision Coat%2, Other, ShoulderSlot. Same. Also Third. Alternative Alt.\\nContinue?')
            modalAct(modalSubject, {internal = 'NO'})
            assert(not confirmed)
            modalAct(modalSubject, {internal = 'YES'})
            assert(confirmed and view:guard(coat, false, function() end) == false)
            local label, reason = {}, 'the save could not start'
            P.CreatorScreen.paintSaveStatus(label, 'SAVE FAILED: ' .. reason, 'error')
            assert(label.text == 'Save ' .. P.Text.ui(reason) and label.tone == 'error')
            P.CreatorSaveQueue.say('NPC save failed: ' .. reason)
            assert(P.CreatorSaveQueue.noticeText == P.Text.ui('NPC save failed') .. ': ' .. P.Text.ui(reason))
            local payload = {text = 'Your Axe%5 is back by the door.', mark = 'base', flag = 7}
            assert(P.SafehouseClient.notice(payload))
            assert(shownNotice.text == 'Returned Axe%5' and shownNotice.mark == 'base' and shownNotice.flag == 7)
            assert(payload.text == 'Your Axe%5 is back by the door.')
            local lost = 'There is no sign of your Axe%5. The neighbour never brought it back.'
            P.SafehouseDirector.tell({}, lost, 'base')
            assert(haloText == 'Lost Axe%5' and haloMark == 'base')
            P.SafehouseClient.notice({text = 'They have nothing to say to that right now, try the Talk menu'})
            assert(shownNotice.text == 'Use the Talk menu TR')
            server = true
            P.SafehouseDirector.tell({}, lost, 'base')
            assert(haloText == lost)
        """)

    def test_screenshot_status_and_creator_display_hooks_use_scoped_labels(self):
        from lua_cikar import h

        def key(source, context=None):
            return 'IGUI_ALifeUI_' + h(source if context is None else context + '|' + source)

        labels = {
            key('Actors: {count}'): 'NPC: {count}',
            key('Health: {errors} error(s)'): 'Sağlık {errors}',
            key('Runtime: {state}'): 'Durum: {state}',
            key('waiting for first tick', 'alifetr.status.value'): 'ilk döngüyü bekliyor',
            key('Census by faction (alive/killed/arrived): {factions}'): 'Nüfus: {factions}',
            key('Always (100%)'): 'Her zaman (100%)',
            key('Used, half gone (5/10)'): 'Yarı ömür (5/10)',
            key('{folder}. Click to fold or unfold.'): 'Aç/kapat: {folder}',
            key('Any', 'alifetr.creator.season'): 'Tüm yıl',
        }
        self.lua.globals().lookup = lambda key: labels.get(key) or self.lookup(key)
        self.lua.execute("""
            local P = ProjectALife
            P.StatusStore = {subscribe = function() end}
            P.SafehouseClient = {statusText = function() return 'Other addon text' end}
            local choices = function(_, _, _, _, options) return options end
            P.CreatorScreen = {addCombo = choices, addNumberChoices = choices,
                relationChoices = {{'Neutral', 'neutral'}}, selectedData = function() return 'neutral' end,
                addTooltip = function(_, text) return text end}
            P.RelationLayers = {professionOf = function() end}
        """)
        for module in ("ALifeDropPolicy", "ALifeStatusWindow", "ALifeCreatorFactionRelations", "ALifeCreatorWardrobe"):
            self.lua.execute(next(MOD.rglob(module + '.lua')).read_text(encoding='utf-8-sig'))
        self.lua.execute("""
            Events.OnGameBoot.fire()
            local P = ProjectALife
            local window = setmetatable({status = {total = 99, runtimeStarted = true, tickCount = 0, healthErrors = 2,
                censusFactions = 'Law Remnants 11/13/1, Rogue, Law Remnants 4/5/6'}}, {__index = ALifeStatusWindow})
            local rows, texts = window:statusRows(), {}
            for _, row in ipairs(rows) do texts[row.text] = true end
            assert(rows[1].heading and rows[2].text == 'NPC: 99')
            local law = P.Text.ui('Law Remnants')
            assert(law ~= 'Law Remnants')
            assert(texts['Durum: ilk döngüyü bekliyor'] and texts['Sağlık 2'] and texts['Other addon text'])
            assert(texts['Nüfus: ' .. law .. ' 11/13/1, Rogue, Law Remnants 4/5/6'])
            local creator, presets, conditions = P.CreatorScreen, P.DropPolicy.presets, P.DropPolicy.conditions
            local localPresets = creator.addCombo({}, 0, 0, 100, presets)
            assert(presets[8][1] == 'Always (100%)' and localPresets[8][1] == 'Her zaman (100%)')
            assert(localPresets[8][2] == presets[8][2] and localPresets[8][4] == presets[8][4])
            local localConditions = creator.addNumberChoices({}, 0, 0, 100, conditions)
            assert(localConditions[6][1] == 'Yarı ömür (5/10)' and localConditions[6][2] == 5)
            assert(conditions[6][1] == 'Used, half gone (5/10)')
            local relation = {effectiveRelationStatus = {setName = function(self, s) self.label = s end}}
            creator.refreshEffectiveRelation(relation)
            assert(relation.effectiveRelationStatus.label:find('Tarafsız', 1, true))
            assert(creator.relationWhy('bloc', 'military'):find(P.Text.ui('Military'), 1, true))
            assert(creator.addTooltip({}, 'ALife Government.  Click to fold or unfold.') == 'Aç/kapat: ' .. P.Text.ui('ALife Government'))
            assert(creator.memberSeasonTitle({outfitSeason = {}}, 'E', ' +') == 'E Tüm yıl +')
            lang = 'EN'
            assert(window:statusRows()[2].text == 'Actors: 99')
            assert(creator.addCombo({}, 0, 0, 100, presets) == presets)
        """)

    def test_phone_name_strip_embedding_pronouns_and_english_fallback(self):
        self.lua.execute("""
            local P, A = ProjectALife.PhonesClient, ProjectALife.UI2Answer
            local tree = ProjectALife.Phones.tree(1)
            P.call = { tree = tree, node = tree.start, asked = {}, state = {lost = "Can%1"}, you = "Ada%2" }
            local first = P.buildAsk()
            assert(first.name == "Anne Baba (Florida)" and first.text:find("Can%1", 1, true))
            assert(first.id == "PHONE#1" and #first.options > 0 and first.options[1].id == tree.nodes[tree.start].opts[1].id)
            local cleaned = A.clean(first)
            assert(A.tagText(cleaned) == "ANNE" and cleaned.name == first.name)
            local win = {choiceSlots = 2, append = function(self, text, name) self.name, self.text = name, text end,
                         refreshChoices = function() end}
            local Ask = ProjectALife.UI2TalkAsk
            assert(Ask.attach(win, cleaned) and win.name == first.name and win.text == first.text and win.askSlots == 2)
            assert(Ask.detach(win, "timeout") and win.choiceSlots == 2 and win.askEmbed == nil)
            for _, female in ipairs({false, true}) do
                P.call.state.female = female
                assert(P.line("I took it off {him}. {He} was one of those things"):match("^Onu"))
                assert(P.line("We'll ring the bell for {him} on Sunday"):find("onun ", 1, true))
            end
            assert(P.line("{lost}, are you okay?", {state = {}}):match("^O,"))
            assert(P.line("{He} {him} {his}", {state = {female = true}}) == "She her her")
            P.call.office, P.call.final = true, {"I have to go"}
            local last = P.buildAsk()
            assert(last.name == first.name and last.options[1].id == "hang" and last.text ~= P.call.final[1])
            assert(P.onChoice(last.id, "hang") and P.call == nil)
            lang = "EN"
            ProjectALife.Text.flush()
            P.call = {tree = tree, node = tree.start, asked = {}, state = {lost = "Can", female = true}}
            assert(P.buildAsk().name == tree.caller)
            assert(P.line("I took it off {him}. {He} was one of those things") == "I took it off her. She was one of those things")
        """)

    def test_mission_payload_presentation_and_network_speech(self):
        self.lua.execute("""
            local M, T = ProjectALife.UI2Missions, ProjectALife.Text
            local shown
            ProjectALife.UI2Notify = { ready = function() return true end, push = function(event) shown = event end }
            local raw = "Dell said it's about 220 meters south-east"
            local hand = "Handed in 0.5 of 2.0 L of water"
            local first = {missions = {}, events = {{text = hand, seq = 1}}}
            Events.OnServerCommand.fire("ProjectALife", "ui2MissionState", first)
            assert(M.state == first and shown == nil)
            local payload = {missions = {dt_one = {tree = true, summary = "For Ada %2", stages = {{}, {detail = "Talk to Ada %2"}}}},
                             events = {{title = "Left Behind", text = hand, kind = "updated", seq = 2}}}
            Events.OnServerCommand.fire("ProjectALife", "ui2MissionState", payload)
            assert(M.state == payload and payload.events[1].text == hand)
            assert(shown.title == "Geride Kalanlar" and shown.text == "Teslim edilen su: 0.5/2.0 litre")
            assert(M.text(raw) == "Dell'in dediğine göre güneydoğu yönünde yaklaşık 220 metre")
            assert(M.text("Get to the warehouse") == "Depoya git")
            assert(M.text("Get to the factory") == "Şuraya ulaş: Fabrika")
            assert(M.text("For Ada %2") == "Ada %2 için" and M.text("Talk to Ada %2") == "Ada %2 ile konuş")
            assert(M.text("For someone you met") == "Tanıştığın biri için")
            assert(M.text("Talk to the one who asked") == "İşi verenle konuş")
            assert(M.text("Talk to Dell and hand it over") == T.ui("Talk to Dell and hand it over"))
            assert(M.text("Expires in about 12 hours") == "Süresi yaklaşık 12 saat sonra doluyor")
            assert(M.text("Handed in 2 of 6") == "Teslim edilen: 2/6")
            local rules, defs, speech = ProjectALife.MissionRules, ProjectALife.MissionDefs, ProjectALife.Speech
            local shell, output = {}, nil
            speech.findShell = function(uid) if uid == "dell-1" then return shell end end
            speech.refusedDead = function() return false end
            speech.adapters.draw = function(_, text) output = text return true end
            for _, key in ipairs({"dell_accept", "dell_accept_armed", "dell_accept_hurt", "dell_where"}) do
                local line = rules.fill(defs.lines[key][1], {place="warehouse", dist=220, dir="south-east"})
                local packet = {uid = "dell-1", text = line .. ".. It's near Rosewood"}
                Events.OnServerCommand.fire("ProjectALife", "speech", packet)
                assert(output:find("Depo", 1, true) and output:find("güneydoğu", 1, true) and output:find("220", 1, true))
                assert(output:find("Konum: Rosewood yakınında", 1, true))
                assert(packet.text ~= output)
            end
            local invalid = "the warehouse. About far meters left. You'll smell it before you see it"
            assert(ProjectALife.AudioPolicy.caption(invalid) == invalid)
            local static = defs.lines.dell_recap_active[1]
            assert(ProjectALife.AudioPolicy.caption(static) == getTextOrNull(T.lineKey(static)))
            assert(T.ui(defs.row("UI2_DELL_WHAT").text) == "Bir şey kaybetmiş gibi bir halin var")
        """)

    def test_tree_note_and_panel_result_keep_the_original_packet(self):
        self.lua.execute("""
            local P = ProjectALife
            local note, panelOutput
            P.Notice = {line = function(_, s) note = s return true end}
            P.Speech.playerKey = function() return "test-player" end
            local panel = { uid = "npc", playerNum = 0, sessionId = 1, treeRun = {},
                            append = function(_, text) panelOutput[#panelOutput+1] = P.AudioPolicy.caption(text) end,
                            refreshChoices = function() end }
            P.TalkMenu.instance = panel
            local result = { uid = "npc", playerKey = "test-player", sessionId = 1, ok = true,
                             choices = {{id = "keep"}}, notes = {"Received 3x Ada's 50% Bag", "[Charm] Success"} }
            panelOutput = {}
            Events.OnServerCommand.fire("ProjectALife", "treeResult", result)
            assert(panelOutput[1] == "Alındı: 3x Ada's 50% Bag" and panelOutput[2] == "[Charm] Başarılı")
            assert(result.notes[1] == "Received 3x Ada's 50% Bag" and panel.treeRun.choices == result.choices)
            for source, expected in pairs({["Delivered"] = "Teslim edildi", ["Found: 50% map"] = "Bulundu: 50% map",
                      ["Task failed: Ada's task"] = "Görev başarısız oldu: Ada's task",
                      ["Task done: go back to Ada %2"] = "Görev tamamlandı: Ada %2 ile tekrar görüş"}) do
                local packet = {text = source}
                Events.OnServerCommand.fire("ProjectALife", "treeNote", packet)
                assert(note == expected and packet.text == source)
            end
            note = nil
            Events.OnServerCommand.fire("OtherMod", "treeNote", {text = "Delivered"})
            assert(note == nil)
        """)

    def test_missing_terms_and_map_display_keep_raw_inputs(self):
        text = self.project.Text
        self.hidden.add(text.key("IGUI_ALifeUI_", "Parents (Florida)", "alifetr.phone.caller"))
        self.hidden.add(text.key("IGUI_ALifeUI_", "Extraction zone", "alifetr.map.tip"))
        self.hidden.add(text.lineKey(self.project.MissionDefs.lines.dell_where[1]))
        self.lua.execute("""
            local P, map = ProjectALife.PhonesClient, ProjectALife.MapLabels
            local tree = ProjectALife.Phones.tree(1)
            P.call = {tree = tree, node = tree.start, asked = {}, state = {lost = "Can"}}
            assert(P.buildAsk().name == tree.caller)
            local key = map.set("Extraction zone", 11, 22)
            assert(map.rows[key].kind == "extraction" and map.tipLines(map.rows[key])[1].text == "Extraction zone")
            map.clear("Extraction zone", 11, 22)
            assert(map.rows[key] == nil)
            for kind, expected in pairs({task = "Burada görev var", radio = "Telsiz işareti",
                                         generic = "İşaretli konum", base = "Karakol"}) do
                local k = map.set("Ada", 11, 22, {icon = kind})
                local row = map.rows[k]
                local visible = map.tipLines(row)
                assert(visible[1].text == "Ada" and visible[2].text == expected and row.text == "Ada")
            end
            local line = "warehouse. About 120 meters east. You'll smell it before you see it"
            assert(ProjectALife.AudioPolicy.caption(line) == line)
            local unrelated = "At the warehouse. About 120 meters east. You'll smell it before you see it"
            assert(ProjectALife.AudioPolicy.caption(unrelated) == unrelated)
        """)


if __name__ == "__main__":
    unittest.main()
