"""Check AD1 presentation hooks against the installed A-Life Lua modules."""
import json
from pathlib import Path
import unittest

from lupa.lua51 import LuaRuntime

from lua_cikar import MOD
from workshop_kur import ek_metni


ROOT = Path(__file__).resolve().parent.parent


class AD1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MOD.is_dir():
            raise unittest.SkipTest("Project A-Life Lua source is unavailable")
        rows = json.loads((ROOT / "paketler/haritalar/AD1_harita.json").read_text(encoding="utf-8"))["satirlar"]
        cls.keys = {text: key for key, text, _ in rows.values()}
        cls.translations = json.loads((ROOT / "teslim/IG_UI.json").read_text(encoding="utf-8"))
        cls.patch = ek_metni("ALifeTR_AD1.lua")
        cls.sources = {}
        for name in (
            "ALifeAdminActions", "ALifeSpawnPlan", "ALifeAdminConsole", "ALifeAdminWindow",
            "ALifeSpawnerPanel", "ALifeSpawnerBrowser", "ALifeCleanupWindow", "ALifeDrivingCrewPicker",
            "ALifeEncounterConsole",
        ):
            cls.sources[name] = next(MOD.rglob(f"{name}.lua")).read_text(encoding="utf-8-sig")

    def setUp(self):
        self.lua = LuaRuntime()
        self.globals = self.lua.globals()
        self.globals.getTextOrNull = self.lua.eval("function(lookup) return function(key) return lookup(key) end end")(
            self.translations.get
        )
        self.lua.execute("""
            lang = "TR"
            Translator = { getLanguage = function() return { name = function() return lang end } end }
            function isServer() return server == true end
            function require() return {} end
            function getTextManager() return { MeasureStringX = function(_, _, text) return #text * 4 end } end
            UIFont = { Small = 1 }
            ISCollapsableWindow = { derive = function() return {} end }
            function event()
                local callbacks = {}
                return { Add = function(fn) callbacks[#callbacks + 1] = fn end,
                         fire = function() for _, fn in ipairs(callbacks) do fn() end end }
            end
            Events = { OnGameBoot = event(), OnGameStart = event() }
            function button()
                return { setEnable = function(self, value) self.enabled = value end,
                         setTitle = function(self, title) self.title = title end,
                         setEnabled = function(self, value) self.enabled = value end }
            end
            ProjectALife = { TalkUi = { onTextScale = function() end } }
        """)
        self.lua.execute(self.patch)
        for name, source in self.sources.items():
            if name != "ALifeEncounterConsole":
                self.lua.execute(source)
        self.lua.execute("""
            ProjectALife.AdminUI = {
                fit = function(text) return text end,
                metrics = function() return { buttonH = 24, fontH = 14, rowH = 20 } end,
                measure = function(text) return #text end,
                wrap = function(text) return { text } end,
                addLabel = function(panel, text) panel.label = text end,
                colors = { text = {} },
                button = function(_, _, _, _, _, title, _, callback)
                    local result = button()
                    result.title = title
                    result.callback = callback
                    return result
                end,
                setBounds = function(widget, _, _, width) if width then widget.width = width end end,
            }
            Events.OnGameBoot.fire()
            Events.OnGameStart.fire()
        """)
        self.project = self.globals.ProjectALife

    def test_admin_presentation_is_scoped_and_preserves_action(self):
        self.globals.adjust = self.tr("ADJUST")
        self.globals.make_hostile = self.tr("Make hostile")
        self.globals.forum_tip = self.tr("Make this faction hostile to you. Reversible")
        self.globals.host_badge = self.tr("HOST")
        self.lua.execute("""
            local console, ui, window = ProjectALife.AdminConsole, ProjectALife.AdminUI, ProjectALife.AdminWindow.class
            console.addTab({ id = "reputation", title = "Reputation", builtin = true })
            console.addTab({ id = "extension", title = "Extension" })
            local builtin, extension = { tabId = "reputation" }, { tabId = "extension" }
            ui.addLabel(builtin, "ADJUST")
            ui.addLabel(extension, "ADJUST")
            assert(builtin.label == adjust and extension.label == "ADJUST")
            local action = function() return "original" end
            builtin.hostile = ui.button(builtin, 0, 0, 120, 24, "Make hostile", nil, action)
            assert(builtin.hostile.title == make_hostile and builtin.hostile.callback == action)
            assert(ui.button(extension, 0, 0, 120, 24, "Make hostile").title == "Make hostile")
            builtin.hostile.tooltip = "Make this faction hostile to you. Reversible"
            window.buildTab = function() return builtin end
            local source = { role = "HOST", text = "HOST", ok = true }
            window.accessBadge = function() return source, 18 end
            Events.OnGameStart.fire()
            assert(window.buildTab({}) == builtin and builtin.hostile.tooltip == forum_tip)
            local badge, width = window.accessBadge({}, ui)
            assert(badge.text == host_badge and badge.role == "HOST" and width == #host_badge + 14)
            assert(source.text == "HOST")
            lang = "EN"
            ui.addLabel(builtin, "ADJUST")
            assert(builtin.label == "ADJUST")
        """)

    def test_builder_labels_are_measured_before_layout_and_routes_fit(self):
        self.globals.floors_from = self.tr("Floors from")
        self.globals.edit_route = self.tr("Edit route")
        self.globals.done_editing = self.tr("Done editing")
        self.lua.execute("""
            local builder = { row = function(_, _, _, items) return items end }
            local driving = { show = function() return "opened", nil, 9 end }
            ProjectALife.BuilderWindow, ProjectALife.DrivingPanel = builder, driving
            driving.editButton, driving.modeButton = button(), button()
            driving.editButton.title, driving.editButton.width = "Edit route", 350
            driving.modeButton.title, driving.modeButton.width = "Mode: destination", 16
            Events.OnGameStart.fire()
            local items = { { label = "Floors from", fixed = 40 }, { slot = "count" } }
            local layout = builder.row({}, 1, 2, items)
            assert(layout[1].label == floors_from and layout[1].fixed == 40)
            assert(items[1].label == "Floors from" and layout[2].slot == "count")
            local opened, unused, result = driving.show()
            assert(opened == "opened" and unused == nil and result == 9)
            assert(driving.editButton.title == edit_route and driving.modeButton.title == "Mode: destination")
            driving.editButton:setTitle("Done editing")
            assert(driving.editButton.title == done_editing)
            server = true
            driving.editButton:setTitle("Edit route")
            assert(driving.editButton.title == "Edit route")
        """)

    def test_compound_labels_keep_runtime_values_and_original_states(self):
        package = json.loads((ROOT / "paketler/AD153.json").read_text(encoding="utf-8"))
        translations = self.translations | {key: row["tr"] for key, row in package["satirlar"].items()}
        self.globals.getTextOrNull = self.lua.eval("function(lookup) return function(key) return lookup(key) end end")(
            translations.get
        )
        self.lua.execute((MOD / "shared/ProjectALife/Core/ALifeText.lua").read_text(encoding="utf-8-sig"))
        self.globals.outpost = self.tr("Toll chain")
        self.globals.staffed = self.tr("Staffed outpost: ")
        self.lua.execute(r"""
            local mod, ui, console = ProjectALife, ProjectALife.AdminUI, ProjectALife.AdminConsole
            local text = mod.Text
            local tip = "Pin to the toolbar (up to 6). Click again to unpin."
            ui.actionButton = function(_, _, spec)
                return { spec = spec, pin = { tooltip = tip, actionId = spec.id } }
            end
            mod.SpawnerBrowser.visitRows = function()
                return { { kind = "visit", id = "friendly_visitor", label = "A visitor",
                    tip = "Forces the safehouse event friendly_visitor for your test base." } }
            end
            mod.BuilderWindow = { wrap = function(_, value, width) return { value }, width end }
            ALifeStampWindow = {
                resultText = function(view) return view.raw end,
                sync = function(view)
                    view.c.place.tooltip = "Build it for real. Click twice to confirm. Not now: Preview this exact target first (step 3)."
                end,
            }
            ALifeDebugSpawnerWindow = {
                outpostPresetOf = function(id) if id == "outpost:toll" then return "toll" end end,
                populate = function(view)
                    view.combos = { encounter = { options = {
                        { text = "Staffed outpost: Toll chain", data = "outpost:toll" },
                        { text = "Staffed outpost: Toll chain", data = "custom" },
                    } } }
                    return 9
                end,
                shortGroupText = function() return "A-Life: spawned 3 of 5 (reason % preserved)" end,
            }
            local driving = { updateTuning = function() return 17 end }
            local count = 0
            local info = {
                text = "<TEXT> Car 123 | Showing applied settings. <LINE> Entire custom % reason.",
                paginate = function() count = count + 1 end,
            }
            driving.vehicleId, driving.tuningUI = 123, { info = info }
            local title = { name = "Edit NPC attachments | Car 123", setName = function(self, name) self.name = name end }
            driving.openCrew = function()
                driving.modal = { vehicleId = 123, dialog = { children = { title } } }
                return "opened"
            end
            mod.DrivingPanel = driving
            Events.OnGameStart.fire()
            console.addTab({ id = "tools", title = "Tools", builtin = true })
            local spec = { id = "tools.test" }
            local action = ui.actionButton({}, { tabId = "tools" }, spec)
            assert(action.spec == spec and action.pin.actionId == "tools.test")
            assert(action.pin.tooltip == text.ui("Pin to the toolbar (up to {limit}). Click again to unpin.", { limit = 6 }))
            local visit = mod.SpawnerBrowser.visitRows()[1]
            assert(visit.id == "friendly_visitor" and visit.label == "A visitor")
            assert(visit.tip == text.ui("Forces the safehouse event {event} for your test base.", { event = visit.id }))
            local builderMessage = "Could not open the folder: The folder could not be opened. It is C:/Save%/Lua"
            local wrapped, width = mod.BuilderWindow.wrap(1, builderMessage, 200)
            assert(width == 200)
            assert(wrapped[1] == text.ui("Could not open the folder: {reason} It is {path}",
                { reason = text.ui("The folder could not be opened."), path = "C:/Save%/Lua" }))
            local view = { raw = "Will place 3, already there 1, skipped 2. Removes 4 old objects.\nother reason" }
            local stamp = ALifeStampWindow.resultText(view)
            assert(view.raw ~= stamp and string.find(stamp, "\nother reason", 1, true))
            assert(string.find(stamp, text.ui("Removes {removed} old objects.", { removed = 4 }), 1, true))
            view.c = { place = button(), pick = button() }
            ALifeStampWindow.sync(view)
            assert(view.c.place.tooltip == text.ui("Build it for real. Click twice to confirm.") ..
                " " .. text.ui("Not now: {reason}", { reason = text.ui("Preview this exact target first (step 3).") }))
            local popup = {}
            assert(ALifeDebugSpawnerWindow.populate(popup) == 9)
            local options = popup.combos.encounter.options
            assert(options[1].text == staffed .. outpost and options[1].data == "outpost:toll")
            assert(options[2].text == "Staffed outpost: Toll chain")
            assert(ALifeDebugSpawnerWindow.shortGroupText() ==
                text.ui("A-Life: spawned {active} of {requested}", { active = 3, requested = 5 }) .. " (reason % preserved)")
            assert(driving.updateTuning() == 17 and count == 1)
            assert(info.text == "<TEXT> " .. text.ui("Car {vehicle}", { vehicle = 123 }) ..
                " | " .. text.ui("Showing applied settings.") .. " <LINE> Entire custom % reason.")
            assert(driving.updateTuning() == 17 and count == 1)
            assert(driving.openCrew() == "opened" and title.name ~= "Edit NPC attachments | Car 123")
            assert(string.sub(title.name, -3) == "123")
            lang = "EN"
            local untouched = mod.BuilderWindow.wrap(1, builderMessage, 100)
            assert(untouched[1] == builderMessage)
        """)

    def tr(self, text):
        return self.translations[self.keys[text]]

    def test_classic_encounter_preserves_commands_and_localizes_presentation(self):
        self.lua.execute("""
            local function noop() end
            ISPanel = { derive = function() return {} end, new = function(class)
                return setmetatable({ initialise = noop }, { __index = class })
            end }
            ISCollapsableWindow.createChildren = noop
            ISButton = { new = function(_, x, y, width, height, title, owner, callback)
                local control = button()
                control.width, control.title, control.callback = width, title, callback
                control.initialise, control.instantiate = noop, noop
                control.setVisible = function(self, visible) self.visible = visible end
                return control
            end }
            local color = { r = 1, g = 1, b = 1 }
            ProjectALife.UI2Theme = { skin = function() return setmetatable({}, {
                __index = function() return color end,
            }) end }
            ProjectALife.UI2Chrome = setmetatable({}, { __index = function() return noop end })
            function getSpecificPlayer(index) return index end
            function sendClientCommand(index, module, command, args)
                request = { index, module, command, args }
            end
        """)
        self.lua.execute(self.sources["ALifeEncounterConsole"])
        self.globals.primary_title = self.tr("SPAWN ENCOUNTER + SQUAD")
        self.globals.advanced_title = self.tr("ADVANCED OPTIONS  >")
        self.globals.refusal = self.tr("FACTIONS REFUSED: ")
        self.lua.execute("""
            Events.OnGameStart.fire()
            local class = ProjectALife.EncounterConsole
            local rendered = {}
            local view = setmetatable({ width = 720, height = 520, count = 3, playerNum = 1,
                targetPosition = { x = 10, y = 20, z = 0 }, persistent = true,
                addChild = function() end, drawRect = function() end,
                drawText = function(_, label) rendered[label] = true end,
            }, { __index = class })
            view:createChildren()
            assert(view.primaryButton.title == primary_title)
            assert(view.advancedToggle.title == advanced_title)
            assert(view.primaryButton.callback == class.onSpawnEncounter)
            view:onToggleAdvanced()
            assert(view.advancedToggle.title == advanced_title:gsub(">$", "v"))
            assert(view.hereButton.visible)
            view.factionList:setRows({ { id = "faction-id", label = "Faction" } })
            view.encounterList:setRows({ { id = "encounter-id", label = "Encounter" } })
            view.count, view.persistent = 3, true
            view.primaryButton.callback(view)
            local args = request[4]
            assert(request[1] == 1 and request[2] == "ProjectALife" and request[3] == "debugSpawnCatalog")
            assert(args.factionId == "faction-id" and args.encounterId == "encounter-id")
            assert(args.x == 10 and args.y == 20 and args.z == 0 and args.count == 3 and args.persistent)
            view:applyCatalogRefusal("server_reason")
            view:render()
            assert(rendered[refusal .. "server_reason"] and view.message == "FACTIONS REFUSED: server_reason")
            getTextOrNull = function() error("dictionary unavailable") end
            view:render()
            assert(rendered[view.message])
            lang = "EN"
            view:onToggleAdvanced()
            assert(view.advancedToggle.title == "ADVANCED OPTIONS  >")
        """)

    def test_plan_options_preserve_ids_shared_rows_and_english(self):
        plan, panel = self.project.SpawnPlan, self.project.SpawnerPanel
        option = plan.KINDS[1]
        label, tip = option.label, option.tip
        row = panel.planRows(plan.KINDS)[1]
        self.assertEqual((row[1], row[2], row[3]), (self.tr(label), option.id, self.tr(tip)))
        self.assertEqual((option.label, option.tip), (label, tip))
        self.globals.lang = "EN"
        row = panel.planRows(plan.KINDS)[1]
        self.assertEqual((row[1], row[2], row[3]), (label, option.id, tip))

    def test_missing_or_failed_translation_uses_the_original_strings(self):
        plan, panel = self.project.SpawnPlan, self.project.SpawnerPanel
        option = plan.KINDS[1]
        for lookup in (
            "function() return nil end",
            "function(key) return key end",
            'function() error("translation table unavailable") end',
        ):
            self.globals.getTextOrNull = self.lua.eval(lookup)
            row = panel.planRows(plan.KINDS)[1]
            self.assertEqual((row[1], row[2], row[3]), (option.label, option.id, option.tip))

    def test_presentation_error_preserves_original_calls_and_return_values(self):
        self.lua.execute("""
            local panel = ProjectALife.SpawnerPanel
            local calls = 0
            panel.refreshSwitch = function(_, fail)
                calls = calls + 1
                if fail then error("original panel error") end
                return nil, "original result", false
            end
            Events.OnGameStart.fire()
            local button = setmetatable({}, { __index = function() error("unexpected widget layout") end })
            local view = { w = { factionSwitch = button } }
            local first, result, last = panel.refreshSwitch(view)
            assert(first == nil and result == "original result" and last == false and calls == 1)
            local ok, reason = pcall(panel.refreshSwitch, view, true)
            assert(not ok and string.find(reason, "original panel error", 1, true) and calls == 2)
        """)

    def test_advanced_layout_translates_without_changing_the_spec(self):
        self.lua.execute("""
            advanced = {
                width = 750, height = 500,
                back = button(), reset = button(),
                body = { vscroll = {}, width = 750, height = 500, setScrollHeight = function() end,
                         setYScroll = function() end, getYScroll = function() return 0 end },
            }
            advanced.back.title = "Back to Spawn"
            advanced.reset.title = "Reset to defaults"
            view = { advanced = advanced, adv = {} }
            for _, row in ipairs(ProjectALife.SpawnPlan.ADVANCED) do
                view.adv[row.key] = { options = { row.label }, advRow = row }
            end
            ProjectALife.SpawnerPanel.layoutAdvanced(view)
        """)
        view = self.globals.view
        self.assertEqual(view.advanced.back.title, self.tr("Back to Spawn"))
        for _, row in self.project.SpawnPlan.ADVANCED.items():
            widget = view.adv[row.key]
            if row.tip in self.keys:
                self.assertEqual(widget.tooltip, self.tr(row.tip))
            if row.kind == "bool" and row.label in self.keys:
                self.assertEqual(widget.options[1], self.tr(row.label))
            self.assertEqual(widget.advRow.label, row.label)
        labels = {entry.text for _, entry in view.advanced.body.labelRefs.items()}
        self.assertIn(self.tr("Behaviour doctrine"), labels)

        self.lua.execute("""
            local labels = {}
            for _, row in ipairs(ProjectALife.SpawnPlan.ADVANCED) do labels[row.label] = true end
            ProjectALife.AdminUI.fit = function(text)
                if not labels[text] then error("unsupported localized font measurement") end
                return text
            end
            ProjectALife.SpawnerPanel.layoutAdvanced(view)
        """)
        labels = {entry.text for _, entry in view.advanced.body.labelRefs.items()}
        self.assertIn("Behaviour doctrine", labels)

    def test_admin_search_keeps_callbacks_and_translates_results(self):
        console = self.project.AdminConsole
        result = next(row for _, row in console.search("spawn type").items() if row.id == "spawn.kind")
        self.assertEqual(result.label, self.tr("Spawn type"))
        tab = console.tab("spawn")
        self.assertEqual(tab.controls[1].label, "Spawn type")
        self.assertTrue(self.lua.eval("rawequal")(result.run, tab.controls[1].run))

    def test_builtin_launcher_keeps_registry_and_action(self):
        self.lua.execute("""
            tab = {
                id = "companions", title = "COMPANIONS", builtin = true,
                tip = "Open the companion sheet: stats, tasks, journal and gear",
                description = "The companion sheet lists the survivors travelling with you: health, needs, skills, orders, journal and gear.",
                launcher = function() end,
            }
            panel = { width = 400 }
            ProjectALife.AdminWindow.class.buildLauncherTab(panel, {}, tab)
        """)
        self.assertEqual(self.globals.panel.label, self.tr(self.globals.tab.description))
        button = self.globals.panel.launchButton
        self.assertEqual(button.tooltip, self.tr(self.globals.tab.tip))
        self.assertEqual(button.tabId, "companions")
        self.assertTrue(button.enabled)

    def test_cleanup_refresh_keeps_scope_data_and_counts(self):
        self.lua.execute("""
            cleanup = ProjectALife.CleanupClient
            cleanup.state = { mode = "running", job = { counts = {} } }
            local row = cleanup.rows[1]
            cleanup.state.job.counts[row.count] = 42
            cleanupView = {
                ticks = { options = {}, optionsIndex = {}, optionData = {}, width = 500, boxSize = 8, textGap = 6 },
                list = { clear = function() end },
                leftNeed = 320, tabButtons = {}, setOn = function() end, layout = function() end,
            }
            for index, spec in ipairs(cleanup.rows) do
                cleanupView.ticks.options[index] = spec.label
                cleanupView.ticks.optionData[index] = spec.key
            end
            ALifeCleanupWindow.refresh(cleanupView)
            ALifeCleanupWindow.refresh(cleanupView)
        """)
        row = self.project.CleanupClient.rows[1]
        ticks = self.globals.cleanupView.ticks
        self.assertEqual(ticks.options[1], self.tr(row.label) + "  (42)")
        self.assertEqual(ticks.optionData[1], row.key)
        status = self.globals.ALifeCleanupWindow.statusLines(self.globals.cleanupView)
        self.assertEqual(status[1], self.tr("World: CLEANUP RUNNING, A-Life spawning is locked"))
        self.lua.execute("""
            cleanupView.ticks.width = 60
            ALifeCleanupWindow.refresh(cleanupView)
        """)
        self.assertEqual(ticks.options[1], row.label + "  (42)")
        self.assertEqual(ticks.optionData[1], row.key)

    def test_driving_updates_each_refresh_and_ignores_non_turkish_clients(self):
        self.lua.execute("""
            local mod = ProjectALife
            mod.DrivingPanel = {
                vehicleId = 7, route = { {} }, clearUnloadedSelection = function() end,
                active = function() return nil end,
            }
            mod.DrivingDemoClient = { bindings = {}, pending = {} }
            mod.DrivingDemo = {}
            mod.DrivingFleet = { departure = function() return nil, true end }
            mod.DrivingCarMode = {
                player = function() return false end,
                get = function() return "npc" end,
            }
            mod.CarAttack = { available = function() return true end }
            mod.CarHullHealth = { read = function() return nil end }
            mod.DrivingRiders = { seat = function() return nil end }
            function getVehicleById() return {} end
            function getSpecificPlayer() return {} end
            local panel = mod.DrivingPanel
            for _, name in ipairs({ "attachButton", "inButton", "driveButton", "outButton", "stopButton",
                    "detachButton", "cancelModeButton", "rideButton", "modeButton", "editButton", "xyButton",
                    "waypointButton", "dismountButton", "deleteButton", "addPositionButton", "clearButton",
                    "centerMeButton", "centerCarButton", "xField", "yField" }) do
                panel[name] = button()
            end
            panel.carModeButtons = { attack = button() }
            panel.carModeButtons.attack.title = "Attack mode"
            panel.repairHealthButton = button()
            panel.repairHealthButton.title = "Repair car HP"
            mod.installDrivingCrewPicker()
            Events.OnGameStart.fire()
        """)
        package = json.loads((ROOT / "paketler/DR154.json").read_text(encoding="utf-8"))
        mapping = json.loads((ROOT / "paketler/haritalar/DR154_harita.json").read_text(encoding="utf-8"))
        pending = {key: value["tr"] for key, value in package["satirlar"].items()}
        self.globals.getTextOrNull = self.lua.eval(
            "function(lookup) return function(key) return lookup(key) end end"
        )((self.translations | pending).get)
        driving = {text: pending[key] for key, text, _ in mapping["satirlar"].values()}
        attack_hint = mapping["satirlar"]["13"][1]
        self.project.CarAttack.tooltip = attack_hint
        panel = self.project.DrivingPanel
        panel.updateButtons()
        self.assertEqual(panel.carModeButtons.attack.title, driving["Attack mode"])
        self.assertEqual(panel.carModeButtons.attack.tooltip, driving[attack_hint])
        self.assertEqual(self.project.CarAttack.tooltip, attack_hint)
        self.assertEqual(panel.repairHealthButton.title, driving["Repair car HP"])
        self.project.DrivingCarMode.get = self.lua.eval('function() return "attack" end')
        panel.updateButtons()
        self.assertEqual(panel.stopButton.tooltip, driving["Cancel Attack mode and stop the car. Crew stays seated."])
        self.assertEqual(panel.driveButton.title, self.tr("Get in & drive"))
        self.assertTrue(panel.driveButton.enabled)
        self.assertFalse(panel.detachButton.enabled)
        self.assertEqual(panel.detachButton.title, self.tr("Detach crew"))
        self.globals.server = True
        panel.updateButtons()
        self.assertEqual(panel.detachButton.title, "Detach crew")
        self.globals.server = False
        self.globals.lang = "EN"
        panel.updateButtons()
        self.assertEqual(panel.driveButton.title, "Get in & drive")


if __name__ == "__main__":
    unittest.main()
