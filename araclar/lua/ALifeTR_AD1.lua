-- Project A-Life admin tools: localize presentation fields on the client.
if ALifeTurkce_AD1 then return end
ALifeTurkce_AD1 = true

local keys = __AD1_METINLERI__

-- Keep the base UI call outside this boundary. A failing presentation hook
-- must never suppress or repeat an admin action.
local function display(callback, ...)
    local ok, value = pcall(callback, ...)
    if ok then return value end
end

local function turkish()
    if type(getTextOrNull) ~= "function" then return false end
    return display(function()
        if type(isServer) == "function" and isServer() then return false end
        return tostring(Translator.getLanguage():name()) == "TR"
    end) == true
end

local function afterPresentation(update, ...)
    if turkish() then display(update) end
    return ...
end

local function translated(group, value)
    if type(value) ~= "string" then return value end
    local key = keys[group][value]
    if key == nil then return value end
    local text = display(getTextOrNull, key)
    if type(text) == "string" and text ~= "" and text ~= key then return text end
    return value
end

local function translatedPrefix(group, value, prefix)
    if type(value) ~= "string" or string.sub(value, 1, #prefix) ~= prefix then return value end
    return translated(group, prefix) .. string.sub(value, #prefix + 1)
end

local function templateOr(fallback, key, vars)
    local text = ProjectALife.Text
    if type(text) ~= "table" or type(text.ui) ~= "function" then return fallback end
    local value = text.ui(key, vars)
    if type(value) == "string" and value ~= "" and value ~= text.fill(key, vars) then return value end
    return fallback
end

local function tuningDescription(raw)
    if type(raw) ~= "string" then return raw end
    local vehicle, status, detail = string.match(raw, "^<TEXT> Car (.-) | (.-) <LINE> (.*)$")
    if vehicle == nil then return raw end
    local label = vehicle == "not selected" and templateOr(vehicle, vehicle) or vehicle
    local header = templateOr("Car " .. vehicle, "Car {vehicle}", { vehicle = label })
    local note = translated("drivingTuning", detail)
    if detail == "Per-car settings last for this game session. Motion applies live; planner changes rebuild the path." then
        note = templateOr(detail, detail)
    end
    return "<TEXT> " .. header .. " | " .. templateOr(status, status) .. " <LINE> " .. note
end

local function buttonText(button, group)
    if type(button) ~= "table" then return end
    local title = translated(group, button.title)
    if title ~= button.title and type(button.setTitle) == "function" then button:setTitle(title) end
    button.tooltip = translated(group, button.tooltip)
end

local installed = setmetatable({}, { __mode = "k" })
local function wrap(target, name, create)
    if type(target) ~= "table" or type(target[name]) ~= "function" then return end
    local slots = installed[target]
    if slots == nil then
        slots = {}
        installed[target] = slots
    end
    if slots[name] == target[name] then return end
    local replacement = create(target[name])
    slots[name], target[name] = replacement, replacement
end

local drivingButtons = {
    "inButton", "driveButton", "outButton", "stopButton", "detachButton",
    "cancelModeButton", "rideButton", "attachButton", "repairHealthButton",
}

local routeButtons = {
    "editButton", "modeButton", "centerMeButton", "centerCarButton", "presetsButton",
    "addPositionButton", "waypointButton", "dismountButton", "xyButton", "deleteButton", "clearButton",
}

local function routeButton(button, group, titleText)
    if type(button) ~= "table" or type(button.setTitle) ~= "function" then return end
    wrap(button, "setTitle", function(original)
        return function(self, title, ...)
            if turkish() then
                title = display(function()
                    local text = titleText and titleText(title) or translated(group, title)
                    if text == title or type(self.width) ~= "number" then return text end
                    local font = type(self.getFont) == "function" and self:getFont() or self.font or UIFont.Small
                    if getTextManager():MeasureStringX(font, text) + 12 <= self.width then return text end
                    return title
                end) or title
            end
            return original(self, title, ...)
        end
    end)
    button:setTitle(button.title)
    button.tooltip = translated(group, button.tooltip)
end

local function installDriving(panel)
    wrap(panel, "show", function(original)
        return function(...)
            return afterPresentation(function()
                for _, name in ipairs(routeButtons) do display(routeButton, panel[name], "drivingRoute") end
                if type(panel.mapTab) == "table" and panel.mapTab.title == "Map" then
                    panel.mapTab:setTitle(templateOr("Map", "Map"))
                end
                local logs = panel.logsUI
                if type(logs) == "table" then
                    for _, name in ipairs({ "filter", "pause", "overhead" }) do
                        display(routeButton, logs[name], "drivingRoute")
                    end
                end
            end, original(...))
        end
    end)
    wrap(panel, "openCrew", function(original)
        return function(...)
            local previous = panel.modal
            return afterPresentation(function()
                local modal = panel.modal
                if modal == previous or type(modal) ~= "table" or type(modal.dialog) ~= "table" then return end
                local prefix = "Edit NPC attachments | Car "
                local expected = prefix .. tostring(modal.vehicleId)
                for _, child in pairs(modal.dialog.children or {}) do
                    if type(child) == "table" and child.name == expected and type(child.setName) == "function" then
                        child:setName(translatedPrefix("crewTitle", expected, prefix))
                    end
                end
            end, original(...))
        end
    end)
    wrap(panel, "openPresets", function(original)
        return function(...)
            return afterPresentation(function()
                local dialog = panel.modal
                if type(dialog) ~= "table" or dialog.kind ~= "presets" then return end
                for _, name in ipairs({ "save", "replace", "delete", "load", "copy" }) do
                    display(routeButton, dialog[name], "routePresets")
                end
                local window = dialog.dialog
                if type(window) == "table" then
                    wrap(window, "update", function(update)
                        return function(...)
                            return afterPresentation(function()
                                if type(dialog.copy) == "table" then
                                    dialog.copy.tooltip = translated("routePresets", dialog.copy.tooltip)
                                end
                            end, update(...))
                        end
                    end)
                end
            end, original(...))
        end
    end)
    wrap(panel, "buildPerformance", function(original)
        return function(...)
            return afterPresentation(function()
                local controls = panel.performanceUI
                if type(controls) == "table" then buttonText(controls.start, "drivingPerformance") end
            end, original(...))
        end
    end)
    wrap(panel, "buildTuning", function(original)
        return function(...)
            return afterPresentation(function()
                local tuning = panel.tuningUI
                if tuning and type(tuning.apply) == "table" and tuning.apply.title == "Apply to car" then
                    tuning.apply:setTitle(templateOr("Apply to car", "Apply to car"))
                end
                if tuning and tuning.root and type(tuning.root.children) == "table" then
                    for _, child in pairs(tuning.root.children) do
                        if type(child) == "table" and type(child.setTitle) == "function" then
                            display(buttonText, child, "drivingTuning")
                        end
                    end
                end
            end, original(...))
        end
    end)
    wrap(panel, "updateTuning", function(original)
        return function(...)
            return afterPresentation(function()
                local tuning = panel.tuningUI
                local info = tuning and tuning.info
                if type(info) ~= "table" then return end
                local raw = info.text
                local shown = tuningDescription(raw)
                if shown ~= raw then
                    info.text = shown
                    info:paginate()
                end
            end, original(...))
        end
    end)
    wrap(panel, "updateButtons", function(original)
        return function(...)
            return afterPresentation(function()
                for _, name in ipairs(drivingButtons) do display(buttonText, panel[name], "driving") end
                for _, button in pairs(panel.carModeButtons or {}) do
                    display(buttonText, button, "driving")
                end
            end, original(...))
        end
    end)
    wrap(panel, "pickerRows", function(original)
        return function(...)
            return afterPresentation(function()
                if type(panel.modal) == "table" then buttonText(panel.modal.detachOne, "driving") end
            end, original(...))
        end
    end)
end

local function installTabs(console, window)
    wrap(console, "search", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(function()
                for _, row in ipairs(rows) do
                    if row.kind == "control" and row.tab == "spawn" then
                        row.label = translated("spawnDetails", translated("search", row.label))
                        row.tip = translated("spawnDetails", translated("search", row.tip))
                    elseif row.kind == "control" and row.id == "overview.cards" then
                        row.tip = translated("adminWorld", row.tip)
                    elseif row.kind == "settings" or row.kind == "factions" then
                        row.tip = translated("search", row.tip)
                    end
                end
            end) end
            return rows
        end
    end)
    wrap(window, "buildTabButtons", function(original)
        return function(self, ...)
            return afterPresentation(function()
                for id, button in pairs(self.tabButtons) do
                    local tab = console.tab(id)
                    if tab and tab.builtin then buttonText(button, "tabs") end
                end
            end, original(self, ...))
        end
    end)
    wrap(window, "buildLauncherTab", function(original)
        return function(panel, owner, tab, ...)
            if turkish() and type(tab) == "table" and tab.builtin then
                tab = display(function()
                    local localized = {}
                    for key, value in pairs(tab) do localized[key] = value end
                    localized.description = translated("tabs", tab.description)
                    if tab.id == "cleanup" then
                        localized.description = translated("cleanupDetails", localized.description)
                    end
                    localized.tip = translated("tabs", tab.tip)
                    return localized
                end) or tab
            end
            return original(panel, owner, tab, ...)
        end
    end)
end

local function installAdminControls(console, window, ui)
    local function builtin(panel)
        if type(panel) ~= "table" or panel.tabId == nil then return false end
        local tab = console.tab(panel.tabId)
        return tab ~= nil and tab.builtin == true
    end
    wrap(ui, "addLabel", function(original)
        return function(panel, label, ...)
            if turkish() then
                label = display(function()
                    if not builtin(panel) then return label end
                    return translatedPrefix("adminWindow", translated("adminLabels", label),
                        "This tab failed to build: ")
                end) or label
            end
            return original(panel, label, ...)
        end
    end)
    wrap(ui, "button", function(original)
        return function(panel, x, y, width, height, label, ...)
            if turkish() then
                label = display(function()
                    return builtin(panel) and translated("adminButtons", label) or label
                end) or label
            end
            return original(panel, x, y, width, height, label, ...)
        end
    end)
    wrap(ui, "drawLabels", function(original)
        return function(panel, ...)
            if turkish() then display(function()
                if builtin(panel) and panel.tabId == "diagnostics" and type(panel.status) == "table" then
                    local raw = panel.status.text
                    local count = type(raw) == "string" and string.match(raw, "^Module table: (%d+) modules$")
                    local prefix = translated("adminWorld", "Module table: ")
                    if count and prefix ~= "Module table: " then panel.status.text = prefix .. count end
                end
            end) end
            return original(panel, ...)
        end
    end)
    wrap(ui, "actionButton", function(original)
        return function(window, panel, ...)
            local entry = original(window, panel, ...)
            if turkish() then display(function()
                local button = type(entry) == "table" and entry.pin
                if not builtin(panel) or type(button) ~= "table" or type(button.tooltip) ~= "string" then return end
                local limit = string.match(button.tooltip, "^Pin to the toolbar %(up to (%d+)%)%. Click again to unpin%.$")
                if limit then
                    button.tooltip = templateOr(button.tooltip, "Pin to the toolbar (up to {limit}). Click again to unpin.",
                        { limit = limit })
                end
            end) end
            return entry
        end
    end)
    wrap(window, "buildTab", function(original)
        return function(view, tab, ...)
            local panel = original(view, tab, ...)
            if turkish() then display(function()
                if not builtin(panel) then return end
                if panel.tabId == "reputation" then
                    buttonText(panel.hostile, "adminButtons")
                    buttonText(panel.baseline, "adminButtons")
                elseif panel.tabId == "overview" and type(panel.cards) == "table" then
                    wrap(panel.cards.world, "prerender", function(draw)
                        return function(card, ...)
                            if turkish() then display(function()
                                for _, line in ipairs(card.lines or {}) do
                                    line.text = translatedPrefix("adminWorld", translated("adminWorld", line.text), "RAID wave ")
                                end
                            end) end
                            return draw(card, ...)
                        end
                    end)
                end
            end) end
            return panel
        end
    end)
    wrap(window, "new", function(original)
        return function(self, ...)
            local view = original(self, ...)
            if turkish() then display(function()
                local version = ProjectALife.Version
                if view.title == version.title("A-Life Admin") then
                    view:setTitle(version.title(translated("adminWindow", "A-Life Admin")))
                end
            end) end
            return view
        end
    end)
    wrap(window, "createChildren", function(original)
        return function(self, ...)
            return afterPresentation(function()
                local entry = self.searchEntry
                if type(entry) == "table" and type(entry.setTooltip) == "function" then
                    entry:setTooltip(translated("adminWindow", entry.tooltip))
                end
            end, original(self, ...))
        end
    end)
    wrap(window, "setStatus", function(original)
        return function(view, text, ...)
            if turkish() then text = display(translated, "adminWindow", text) or text end
            return original(view, text, ...)
        end
    end)
    wrap(window, "accessBadge", function(original)
        return function(view, ui, ...)
            local access, width = original(view, ui, ...)
            if turkish() and type(access) == "table" then
                local badge = display(function()
                    local text = translated("adminWindow", access.text)
                    if text == access.text then return nil end
                    local result = {}
                    for key, value in pairs(access) do result[key] = value end
                    result.text = text
                    return { access = result, width = ui.measure(text) + 14 }
                end)
                if badge then return badge.access, badge.width end
            end
            return access, width
        end
    end)
end

local function updateTickLabel(ticks, index, label)
    ticks.options[index] = label
    if type(ticks.optionsIndex) == "table" then ticks.optionsIndex[index] = label end
end

local function localizeChoices(rows)
    for _, row in ipairs(rows) do
        row[1] = translated("choices", row[1])
        row[3] = translated("choices", row[3])
    end
end

local function headingRows(rows)
    local localized = {}
    for index, row in ipairs(rows) do
        localized[index] = { translated("choices", row[1]), row[2], row[3] }
    end
    return localized
end

local function localizeAdvanced(panel, plan, ui)
    local advanced = panel.advanced
    local body = advanced and advanced.body
    if not body or type(body.labelRefs) ~= "table" then return end
    local index = 1
    for _, row in ipairs(plan.ADVANCED) do
        local widget = panel.adv[row.key]
        if row.kind == "bool" then
            if widget and widget.options and widget.options[1] then
                updateTickLabel(widget, 1, translated("advanced", row.label))
            end
        else
            local label = body.labelRefs[index]
            if widget and label and label.text == ui.fit(row.label, widget.width) then
                label.text = ui.fit(translated("advanced", row.label), widget.width)
            end
            index = index + 1
        end
        if widget then widget.tooltip = translated("advanced", widget.tooltip) end
    end
end

local function installSpawner(panel, plan, ui, browser)
    wrap(panel, "planRows", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(localizeChoices, rows) end
            return rows
        end
    end)
    wrap(panel, "refresh", function(original)
        return function(view, ...)
            return afterPresentation(function()
                if type(view.w) == "table" then buttonText(view.w.kind, "spawn") end
            end, original(view, ...))
        end
    end)
    wrap(panel, "refreshSwitch", function(original)
        return function(view, ...)
            return afterPresentation(function()
                if type(view.w) == "table" then buttonText(view.w.factionSwitch, "spawn") end
            end, original(view, ...))
        end
    end)
    wrap(panel, "refreshRoster", function(original)
        return function(view, ...)
            return afterPresentation(function()
                local label = view.L.roster
                label.text = translatedPrefix("spawnDetails", label.text, "Selected roster: ")
            end, original(view, ...))
        end
    end)
    wrap(panel, "refreshSummary", function(original)
        return function(view, ...)
            return afterPresentation(function()
                local label = view.L.summary
                label.text = translatedPrefix("spawnDetails", label.text, "Not ready: ")
            end, original(view, ...))
        end
    end)
    wrap(browser, "factionRows", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(function()
                for _, row in ipairs(rows) do
                    if row.kind == "automatic" or row.kind == "folder" then
                        row.tip = translated("spawnDetails", row.tip)
                    end
                end
            end) end
            return rows
        end
    end)
    wrap(browser, "presetRows", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(function()
                for _, row in ipairs(rows) do
                    if row.kind == "preset" then row.label = translated("outpostNames", row.label) end
                end
            end) end
            return rows
        end
    end)
    wrap(browser, "visitRows", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(function()
                for _, row in ipairs(rows) do
                    if row.kind == "visit" and type(row.id) == "string"
                            and row.tip == "Forces the safehouse event " .. row.id .. " for your test base." then
                        row.tip = templateOr(row.tip, "Forces the safehouse event {event} for your test base.",
                            { event = row.id })
                    end
                end
            end) end
            return rows
        end
    end)
    if plan == nil or ui == nil then return end
    wrap(panel, "combo", function(original)
        return function(view, name, field, rows, ...)
            if field == "heading" and turkish() then
                rows = display(headingRows, rows) or rows
            end
            return original(view, name, field, rows, ...)
        end
    end)
    wrap(browser, "poolRows", function(original)
        return function(...)
            local rows = original(...)
            if turkish() then display(function()
                for _, row in ipairs(rows) do
                    local pool = plan.pool(row.id)
                    if pool and row.label == pool.label then
                        row.label = translated("choices", row.label)
                        local suffix = " A new one is picked every time you spawn. " .. plan.POOL_HINT
                        if row.tip == pool.tip .. suffix then
                            row.tip = translated("choices", pool.tip) .. suffix
                        end
                    end
                end
            end) end
            return rows
        end
    end)
    wrap(panel, "layoutAdvanced", function(original)
        return function(view, ...)
            return afterPresentation(function()
                if type(view.advanced) ~= "table" then return end
                display(buttonText, view.advanced.back, "spawn")
                display(buttonText, view.advanced.reset, "spawn")
                localizeAdvanced(view, plan, ui)
            end, original(view, ...))
        end
    end)
end

local function installCleanup(window, client)
    wrap(window, "new", function(original)
        return function(self, ...)
            local view = original(self, ...)
            if turkish() then display(function()
                local version = ProjectALife.Version
                if version and type(version.title) == "function"
                        and view.title == version.title("CLEANUP A-LIFE") then
                    view:setTitle(version.title(translated("cleanup", "CLEANUP A-LIFE")))
                end
                wrap(view, "drawText", function(draw)
                    return function(self, text, ...)
                        if turkish() then
                            text = display(function()
                                return translatedPrefix("cleanupDetails", translated("cleanupDetails", text),
                                    "Spawns refused while locked: ")
                            end) or text
                        end
                        return draw(self, text, ...)
                    end
                end)
            end) end
            return view
        end
    end)
    wrap(window, "wrap", function(original)
        return function(font, text, ...)
            if turkish() then
                text = display(function()
                    return translatedPrefix("cleanupDetails", translated("cleanupDetails", text), "Map markers removed here: ")
                end) or text
            end
            return original(font, text, ...)
        end
    end)
    wrap(window, "addButton", function(original)
        return function(self, label, ...)
            return original(self, turkish() and translated("cleanup", label) or label, ...)
        end
    end)
    if client == nil then return end
    wrap(window, "refresh", function(original)
        return function(self, ...)
            return afterPresentation(function()
                local ticks = self.ticks
                if not ticks or type(ticks.options) ~= "table" then return end
                local available = ticks.width - ticks.boxSize - ticks.textGap - (ticks.leftMargin or 0) - 4
                local counts = client.counts()
                for index, row in ipairs(client.rows) do
                    local text = translated("cleanup", row.label)
                    local suffix = counts[row.count] ~= nil and ("  (" .. tostring(counts[row.count]) .. ")") or ""
                    if text ~= row.label and ticks.options[index] == row.label .. suffix
                            and getTextManager():MeasureStringX(UIFont.Small, text .. suffix) <= available then
                        updateTickLabel(ticks, index, text .. suffix)
                    end
                end
            end, original(self, ...))
        end
    end)
    wrap(window, "statusLines", function(original)
        return function(...)
            local function present(rows, ...)
                if turkish() and type(rows) == "table" then
                    display(function() rows[1] = translated("cleanup", rows[1]) end)
                end
                return rows, ...
            end
            return present(original(...))
        end
    end)
end

local function stampCounts(raw)
    local lead, place, same, skip, tail = string.match(raw, "^(.-)Will place (%d+), already there (%d+), skipped (%d+)%.(.*)$")
    if place == nil or (lead ~= "" and lead ~= "Ready. " and lead ~= "Nothing to place here. ") then return raw end
    local removed = tail ~= "" and string.match(tail, "^ Removes (%d+) old objects%.$")
    if tail ~= "" and not removed then return raw end
    local head = lead
    if lead ~= "" then
        local sentence = string.sub(lead, 1, #lead - 1)
        head = templateOr(sentence, sentence) .. " "
    end
    local key = "Will place {place}, already there {same}, skipped {skip}."
    local original = "Will place " .. place .. ", already there " .. same .. ", skipped " .. skip .. "."
    local shown = templateOr(original, key, { place = place, same = same, skip = skip })
    if removed then tail = " " .. templateOr(string.sub(tail, 2), "Removes {removed} old objects.", { removed = removed }) end
    return head .. shown .. tail
end

local function buildMessage(raw)
    if type(raw) ~= "string" then return raw end
    local reason = string.match(raw, "^Save failed: (.+) You can still use Copy to clipboard%.$")
    if reason then
        return templateOr(raw, "Save failed: {reason} You can still use Copy to clipboard.",
            { reason = templateOr(reason, reason) })
    end
    local folderReason, path = string.match(raw, "^Could not open the folder: (.-) It is (.+)$")
    if folderReason then
        return templateOr(raw, "Could not open the folder: {reason} It is {path}",
            { reason = templateOr(folderReason, folderReason), path = path })
    end
    reason = string.match(raw, "^Could not open the folder: (.+)$")
    if reason then
        return templateOr(raw, "Could not open the folder: {reason}", { reason = templateOr(reason, reason) })
    end
    return stampCounts(translated("builderDetails", raw))
end

local function stampPlaceTip(raw)
    if type(raw) ~= "string" then return raw end
    local hint = "Build it for real. Click twice to confirm."
    if raw == hint then return templateOr(hint, hint) end
    local reason = string.match(raw, "^Build it for real%. Click twice to confirm%. Not now: (.+)$")
    if reason == nil then return raw end
    local status = templateOr("Not now: " .. reason, "Not now: {reason}", { reason = buildMessage(reason) })
    return templateOr(hint, hint) .. " " .. status
end

local function installBuilder(builder, stamp)
    wrap(builder, "button", function(original)
        return function(parent, title, callback, tip, ...)
            if turkish() then
                title = display(translated, "build", title) or title
                tip = display(translated, "build", tip) or tip
            end
            return original(parent, title, callback, tip, ...)
        end
    end)
    wrap(builder, "row", function(original)
        return function(view, y, height, items, ...)
            if turkish() then
                items = display(function()
                    local rows = {}
                    for i, item in ipairs(items) do
                        local row = {}
                        for key, value in pairs(item) do row[key] = value end
                        row.label = translated("build", row.label)
                        rows[i] = row
                    end
                    return rows
                end) or items
            end
            return original(view, y, height, items, ...)
        end
    end)
    wrap(builder, "createChildren", function(original)
        return function(self, ...)
            return afterPresentation(function()
                local list = self.c.list
                list.tooltip = translated("build", list.tooltip)
            end, original(self, ...))
        end
    end)
    wrap(builder, "sync", function(original)
        return function(view, ...)
            return afterPresentation(function()
                view.c.clear.tooltip = translatedPrefix("build", translated("build", view.c.clear.tooltip),
                    "Remove every marker. Not now: ")
                view.c.capture.tooltip = translated("build", view.c.capture.tooltip)
            end, original(view, ...))
        end
    end)
    wrap(builder, "syncKind", function(original)
        return function(view, ...)
            return afterPresentation(function()
                local combo = view.c.kind
                combo.tooltip = translated("builderDetails", combo.tooltip)
            end, original(view, ...))
        end
    end)
    wrap(builder, "wrap", function(original)
        return function(font, text, ...)
            if turkish() then text = display(buildMessage, text) or text end
            return original(font, text, ...)
        end
    end)
    wrap(stamp, "resultText", function(original)
        return function(...)
            local raw = original(...)
            if not turkish() or type(raw) ~= "string" then return raw end
            return display(function() return (string.gsub(raw, "[^\n]+", stampCounts)) end) or raw
        end
    end)
    wrap(stamp, "sync", function(original)
        return function(view, ...)
            return afterPresentation(function()
                local place = view.c.place
                place.tooltip = stampPlaceTip(place.tooltip)
                buttonText(place, "build")
                buttonText(view.c.pick, "build")
            end, original(view, ...))
        end
    end)
    for _, class in pairs({ builder = builder, stamp = stamp }) do
        wrap(class, "new", function(original)
            return function(self, ...)
                local view = original(self, ...)
                if turkish() then display(function()
                    local title = translated("build", view.title)
                    if title ~= view.title then view:setTitle(title) end
                end) end
                return view
            end
        end)
    end
end

local function installStatus(window)
    wrap(window, "costRows", function(original)
        return function(self, rows, ...)
            local start = type(rows) == "table" and #rows + 1 or 1
            return afterPresentation(function()
                for i = start, #rows do
                    local text = translated("status", rows[i].text)
                    text = translatedPrefix("status", text, "Heaviest per tick (ms): ")
                    rows[i].text = translatedPrefix("status", text, "Server profiler: ")
                end
            end, original(self, rows, ...))
        end
    end)
end

local function installClassicSpawner(window)
    wrap(window, "createChildren", function(original)
        return function(self, ...)
            return afterPresentation(function()
                local combo = self.combos and self.combos.count
                local text = ProjectALife.Text
                if combo and text and combo.tooltip ==
                    "How many NPCs one SPAWN makes. The server keeps it inside its group cap and the hostile ceiling. Remembered for next time." then
                    combo.tooltip = text.ui(combo.tooltip)
                end
                wrap(self, "drawTextCentre", function(draw)
                    return function(view, label, ...)
                        if turkish() then label = display(translated, "classicDetails", label) or label end
                        return draw(view, label, ...)
                    end
                end)
            end, original(self, ...))
        end
    end)
    wrap(window, "populate", function(original)
        return function(self, ...)
            return afterPresentation(function()
                local combo = self.combos and self.combos.encounter
                local prefix = "Staffed outpost: "
                for _, option in ipairs(combo and combo.options or {}) do
                    local name = type(option.text) == "string" and string.match(option.text, "^Staffed outpost: (.+)$")
                    if name and type(option.data) == "string" and window.outpostPresetOf(option.data) ~= nil then
                        option.text = translated("classicDetails", prefix) .. translated("outpostNames", name)
                    end
                end
            end, original(self, ...))
        end
    end)
    wrap(window, "shortGroupText", function(original)
        return function(...)
            local text = original(...)
            if not turkish() or type(text) ~= "string" then return text end
            return display(function()
                local active, requested, suffix = string.match(text, "^A%-Life: spawned (%d+) of (%d+)(.*)$")
                if active == nil then return text end
                local prefix = string.sub(text, 1, #text - #suffix)
                return templateOr(prefix, "A-Life: spawned {active} of {requested}", { active = active, requested = requested })
                    .. suffix
            end) or text
        end
    end)
end

local function encounterLabel(label)
    if label == "ADVANCED OPTIONS  v" then
        local closed = translated("classicEncounter", "ADVANCED OPTIONS  >")
        return (string.gsub(closed, ">$", "v"))
    end
    return translated("classicEncounter", label)
end

local function installClassicEncounter(console)
    wrap(console, "createChildren", function(original)
        return function(self, ...)
            return afterPresentation(function()
                for _, name in ipairs({ "primaryButton", "advancedToggle", "hereButton",
                    "ruleButton", "squadButton", "persistToggle", "mapButton" }) do
                    display(routeButton, self[name], "classicEncounter", encounterLabel)
                end
                wrap(self, "drawText", function(draw)
                    return function(view, label, ...)
                        if turkish() then label = display(function()
                            local text = translated("classicEncounter", label)
                            text = translatedPrefix("classicEncounter", text, "FACTIONS REFUSED: ")
                            return translatedPrefix("classicEncounter", text, "REFRESH REFUSED: ")
                        end) or label end
                        return draw(view, label, ...)
                    end
                end)
            end, original(self, ...))
        end
    end)
end

local function install()
    local mod = ProjectALife
    if type(mod) ~= "table" then return end
    local console, window = mod.AdminConsole, mod.AdminWindow
    if console then
        installTabs(console, window and window.class)
        installAdminControls(console, window and window.class, mod.AdminUI)
    end
    installSpawner(mod.SpawnerPanel, mod.SpawnPlan, mod.AdminUI, mod.SpawnerBrowser)
    installCleanup(ALifeCleanupWindow, mod.CleanupClient)
    installDriving(mod.DrivingPanel)
    installBuilder(mod.BuilderWindow, ALifeStampWindow)
    installStatus(ALifeStatusWindow)
    installClassicSpawner(ALifeDebugSpawnerWindow)
    installClassicEncounter(mod.EncounterConsole)
end

local function installSafely()
    display(install)
end

installSafely()
if type(Events) == "table" then
    if Events.OnGameBoot then display(Events.OnGameBoot.Add, installSafely) end
    if Events.OnGameStart then display(Events.OnGameStart.Add, installSafely) end
end
