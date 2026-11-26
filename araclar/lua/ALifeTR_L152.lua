-- Project A-Life 1.5.2: phone calls, mission text, tree notes and map tooltips.
if ALifeTurkce_L152 ~= nil then return end
local L = {}
ALifeTurkce_L152 = L

local function turkish()
    if ProjectALife == nil or ProjectALife.Text == nil then return false end
    if type(isServer) == "function" and isServer() then return false end
    local ok, lang = pcall(function() return tostring(Translator.getLanguage():name()) end)
    return ok and lang == "TR"
end

local function lookup(en, context, radio)
    local text = ProjectALife.Text
    local prefix = radio and "RD_ALifeLine_" or "IGUI_ALifeUI_"
    return text.lookup(text.key(prefix, en, context))
end

local function filled(en, vars, context, radio)
    local template = lookup(en, context, radio)
    if template ~= nil then return ProjectALife.Text.fill(template, vars) end
end

local function copy(source)
    local result = {}
    for key, value in pairs(source) do result[key] = value end
    return result
end

local function wrap(target, slot, make)
    if target == nil or type(target[slot]) ~= "function" then return end
    local marker = "ALifeTurkceL152_" .. slot
    if target[marker] then return end
    target[slot] = make(target[slot])
    target[marker] = true
end

local function atSentenceStart(template, position)
    local before = string.sub(template, 1, position - 1)
    return before == "" or string.find(before, "[%.%?!]%s*$") ~= nil
end

local function wrapPhoneLine(original, phone)
    return function(raw, call)
        call = call or phone.call
        if call == nil or type(raw) ~= "string" or not string.find(raw, "{", 1, true) or not turkish() then
            return original(raw, call)
        end
        local template = lookup(raw)
        if template == nil then return original(raw, call) end
        local function replacement(position, token)
            if token == "lost" then
                local name = type(call.state) == "table" and call.state.lost or nil
                if type(name) == "string" and name ~= "" then return name end
                return atSentenceStart(template, position) and "O" or "o"
            elseif token == "you" then
                local name = call.you
                if name == "friend" then
                    local ok, playerName = pcall(function() return phone.player():getDescriptor():getForename() end)
                    if not ok or playerName ~= name then name = nil end
                end
                if name ~= nil and name ~= "" then return name end
                return lookup("Friend") or "friend"
            elseif token == "he" then return "o"
            elseif token == "He" then return "O"
            elseif token == "his" then return "onun"
            elseif token == "him" then
                if raw == "We'll ring the bell for {him} on Sunday" then return "onun" end
                return atSentenceStart(template, position) and "Onu" or "onu"
            end
            return "{" .. token .. "}"
        end

        -- Kahlua passes only the first capture to a gsub replacement function.
        local parts, cursor = {}, 1
        while true do
            local first, last, token = string.find(template, "{(%a+)}", cursor)
            if first == nil then
                parts[#parts + 1] = string.sub(template, cursor)
                return table.concat(parts)
            end
            parts[#parts + 1] = string.sub(template, cursor, first - 1)
            parts[#parts + 1] = replacement(first, token)
            cursor = last + 1
        end
    end
end

local function wrapPhoneAsk(original)
    return function(...)
        local ask = original(...)
        if ask ~= nil and type(ask.name) == "string" and turkish() then
            ask.name = lookup(ask.name, "alifetr.phone.caller") or ask.name
            local tags = { ["REP 1"] = true, ["FIRST AID 2"] = true, ["FIRST AID 3"] = true,
                ["MECHANICS 2"] = true, ["MECHANICS 3"] = true }
            for _, option in ipairs(ask.options or {}) do
                if type(option.label) == "string" then
                    option.label = string.gsub(option.label, "^%[([^%]]+)%]", function(tag)
                        return "[" .. (tags[tag] and lookup(tag) or tag) .. "]"
                    end, 1)
                end
            end
        end
        return ask
    end
end

local places = {
    warehouse = "IGUI_warehouseKey", factory = "IGUI_FactoryKey", store = "IGUI_generalstoreKey",
    ["police station"] = "IGUI_PoliceKey", ["fire station"] = "IGUI_FireDeptKey",
    clinic = "IGUI_DoctorKey", ["gun store"] = "IGUI_gunstoreKey",
    ["storage building"] = "IGUI_warehouseKey", building = "IGUI_Photo_aBuilding",
}
local directions = {
    east = true, ["south-east"] = true, south = true, ["south-west"] = true,
    west = true, ["north-west"] = true, north = true, ["north-east"] = true,
}

local function placeName(place)
    local value = ProjectALife.Text.lookup(places[place])
    if place == "store" and value ~= nil then return string.match(value, "%S+$") or value end
    return value and string.match(value, "^(.-) / ") or value or place
end

local function directionName(direction)
    return lookup(direction) or direction
end

local function speechTail(tail)
    local kind, town = string.match(tail, "^It's (in) (.+)$")
    if kind == nil then kind, town = string.match(tail, "^It's (near) (.+)$") end
    if kind == nil then return tail end
    local phrase = filled(kind .. " {town}", { town = town })
    return phrase and filled("It's {phrase}", { phrase = phrase }) or tail
end

local missionLines = {
    "It's a {place}, about {dist} meters {dir} of here. Brown duffel, Earl's name on the strap. Watch the loading bay",
    "Good, keep that out, you'll need it.. {place}, about {dist} meters {dir}. Brown duffel. Earl's name on the strap",
    "Patch yourself up first, I mean it.. {place}, about {dist} meters {dir}. Brown duffel, Earl's name on the strap",
    "{place}. About {dist} meters {dir}. You'll smell it before you see it",
}
local function escape(value)
    return (string.gsub(value, "%p", "%%%0"))
end

local boardText = __GOREV_METINLERI__
local function compile(text)
    local fields = {}
    local pattern = string.gsub(escape(text), "%%{(%a+)%%}", function(field)
        fields[#fields + 1] = field
        if field == "dist" then return "([%d?]+)" end
        if field == "n" or field == "count" then return "(%d+)" end
        if field == "min" or field == "max" then return "(%-?%d+%.?%d*)" end
        return "([^\r\n]+)"
    end)
    return { text = text, pattern = "^" .. pattern .. "$", fields = fields }
end

local function translate(raw, rule, convert, radio)
    if #rule.fields == 0 then
        return raw == rule.text and lookup(raw, nil, radio) or nil
    end
    local captures = { string.match(raw, rule.pattern) }
    if captures[1] == nil then return nil end
    local vars = {}
    for index, field in ipairs(rule.fields) do
        local value = captures[index]
        if convert ~= nil then value = convert(field, value) end
        if value == nil then return nil end
        vars[field] = value
    end
    return filled(rule.text, vars, nil, radio)
end

for _, group in pairs(boardText) do
    for index, en in ipairs(group) do group[index] = compile(en) end
end
local function findTranslation(raw, rules, convert, radio)
    for _, rule in ipairs(rules) do
        local tr = translate(raw, rule, convert, radio)
        if tr ~= nil then return tr end
    end
end

local boardPlaces = {
    house = "ev", warehouse = "depo", store = true,
    ["clothing store"] = "IGUI_clothingstoreKey", ["electronics store"] = "IGUI_electronicsstoreKey",
    farm = "IGUI_FarmKey", pharmacy = "IGUI_PharmacyKey", marker = "Marker",
    garage = "garage", ["far marker"] = "far marker", ["next spot"] = "next spot", spot = "spot", post = "post",
}
local function boardPlace(raw)
    if raw == "house" or raw == "warehouse" then return boardPlaces[raw] end
    if raw == "store" then
        local name = ProjectALife.Text.lookup("IGUI_generalstoreKey")
        return name and string.match(name, "%S+$") or raw
    end
    local key = boardPlaces[raw]
    if key == nil then return nil end
    return (string.sub(key, 1, 5) == "IGUI_" and ProjectALife.Text.lookup(key) or lookup(key)) or raw
end

local function boardWhere(raw)
    if raw == "out there" then return lookup(raw) end
    local spot, dist, dir = string.match(raw, "^the (.+), about (%d+) meters ([a-z%-]+)$")
    if spot == nil or not directions[dir] then return nil end
    local place = boardPlace(spot)
    if place ~= nil then
        return filled("the {place}, about {dist} meters {dir}", { place = place, dist = dist, dir = directionName(dir) })
    end
    for name in pairs(boardPlaces) do
        local prefix = name .. " "
        if string.sub(spot, 1, #prefix) == prefix then
            local rest = string.sub(spot, #prefix + 1)
            local kind, town = string.match(rest, "^(in) (.+)$")
            if kind == nil then kind, town = string.match(rest, "^(near) (.+)$") end
            local phrase = kind and filled(kind .. " {town}", { town = town }) or rest
            return filled("the {place} {townphrase}, about {dist} meters {dir}",
                { place = boardPlace(name), townphrase = phrase, dist = dist, dir = directionName(dir) })
        end
    end
end

local function boardValue(field, raw)
    if field == "where" then return boardWhere(raw) end
    if field == "place" then return boardPlace(raw) end
    if field == "dir" then return directions[raw] and directionName(raw) or nil end
    if field == "unlock" then
        local data = ProjectALife.TaskBoardData
        for _, label in pairs(data and data.unlockLabels or {}) do
            if string.lower(label) == raw then return lookup(label) or label end
        end
        return nil
    end
    return raw
end

local function boardSpeech(raw)
    for _, question in ipairs(boardText.how) do
        local suffix = "... " .. question.text
        if string.sub(raw, -#suffix) == suffix then
            local pitch = findTranslation(string.sub(raw, 1, #raw - #suffix), boardText.pitch, boardValue, true)
            local how = lookup(question.text, nil, true)
            if pitch ~= nil and how ~= nil then return string.gsub(pitch, "%.$", "") .. "... " .. how end
        end
    end
    return findTranslation(raw, boardText.speech, boardValue, true)
end

local missionLinePatterns = {}
for index, template in ipairs(missionLines) do
    local pattern = escape(template)
    pattern = string.gsub(pattern, "%%{place%%}", function() return "([a-z ]+)" end)
    pattern = string.gsub(pattern, "%%{dist%%}", function() return "(%d+)" end)
    pattern = string.gsub(pattern, "%%{dir%%}", function() return "([a-z%-]+)" end)
    missionLinePatterns[index] = "^" .. pattern .. "(.*)$"
end

-- Invoked by the existing caption hook after its exact RadioData lookup.
function L.missionSpeech(raw)
    if not turkish() then return nil end
    for index, template in ipairs(missionLines) do
        local place, dist, direction, tail = string.match(raw, missionLinePatterns[index])
        if place ~= nil and places[place] ~= nil and directions[direction]
                and (tail == "" or string.sub(tail, 1, 3) == ".. ") then
            if not turkish() then return nil end
            local tr = filled(template, { place = placeName(place), dist = dist, dir = directionName(direction) }, nil, true)
            if tr ~= nil and tail ~= "" then
                return string.gsub(tr, "%.$", "") .. ".. " .. speechTail(string.sub(tail, 4))
            end
            return tr
        end
    end
    return boardSpeech(raw)
end

local doorAliases = {
    ["You lost or something?!"] = "RD_ALifeLine_3c2e09d82d934946",
    ["Hey, how are you holding up?"] = "RD_ALifeLine_2dbd31291427ebd5",
    ["What now?"] = "RD_ALifeLine_767c0c125327caaf",
    ["Yeah, what?"] = "RD_ALifeLine_57540c18193384fe",
    ["What do you want now"] = "RD_ALifeLine_77059aa8357c632e",
}

function L.doorSpeech(raw)
    if not turkish() then return nil end
    local alias = doorAliases[raw]
    if alias ~= nil then return ProjectALife.Text.lookup(alias) end
    local count = string.match(raw, "^There's (%d+) of us here, we're together$")
    if count ~= nil and tonumber(count) >= 2 then
        return filled("There's {count} of us here, we're together", { count = count }, nil, true)
    end
    count = string.match(raw, "^Noted%. (%d+) residents home, and your report about bites%. Stay inside%. We're moving on%.$")
    if count ~= nil then
        return filled("Noted. {count} residents home, and your report about bites. Stay inside. We're moving on.",
            { count = count }, nil, true)
    end
end

local missionContext = "alifetr.mission.log"
local dellSummary = "Dell Tolliver's crew dropped their bags in a {place} when a horde came through. He wants Earl's bag back."
local dellStages = {}
for _, template in ipairs({ "Get to the {place}", "Clear the {place}", dellSummary }) do
    local pattern = string.gsub(escape(template), "%%{place%%}", function() return "([a-z ]+)" end)
    dellStages[#dellStages + 1] = { template = template, pattern = "^" .. pattern .. "$" }
end
local function dellText(raw)
    for _, stage in ipairs(dellStages) do
        local place = string.match(raw, stage.pattern)
        if place ~= nil and places[place] ~= nil then
            return filled(stage.template, { place = placeName(place) })
        end
    end
    local dist, direction = string.match(raw, "^Dell said it's about (%d+) meters ([a-z%-]+)$")
    if dist ~= nil and directions[direction] then
        return filled("Dell said it's about {dist} meters {dir}", { dist = dist, dir = directionName(direction) }, missionContext)
    end
end

local function taskGiverText(raw, missions)
    local who = string.match(raw, "^For (.+)$")
    local template = "For {who}"
    if who == nil then
        who = string.match(raw, "^Talk to (.+)$")
        template = "Talk to {who}"
    end
    if who == nil then return nil end
    for _, mission in pairs(missions or {}) do
        if mission.tree == true then
            local report = mission.stages and mission.stages[2]
            if (template == "For {who}" and mission.summary == raw)
                    or (template == "Talk to {who}" and report ~= nil and report.detail == raw) then
                return filled(template, { who = who }, missionContext)
            end
        end
    end
end

local treeTitles = {
    ["Bring supplies"] = true, ["Bring medicine"] = true, ["Clear a house"] = true, ["Find someone"] = true,
    ["Deliver a note"] = true, ["Scout an outpost"] = true, ["Walk them somewhere"] = true,
    ["Thin out the dead"] = true,
}
local function treeTitle(raw)
    local title, suffix = string.match(raw, "^(.-)( %([%d/]+%))$")
    title = title or raw
    if not treeTitles[title] then return raw end
    local tr = lookup(title) or lookup(title, nil, true)
    return tr and (string.gsub(tr, "%.$", "") .. (suffix or "")) or raw
end

local function missionText(raw, missions)
    local tr = dellText(raw)
    if tr ~= nil then return tr end
    local count = string.match(raw, "^Expires in about (%d+) hours$")
    if count ~= nil then return filled("Expires in about {n} hours", { n = count }, missionContext) end
    local have, need = string.match(raw, "^Handed in (%d+%.%d) of (%d+%.%d) L of water$")
    if have ~= nil then return filled("Handed in {have} of {need} L of water", { have = have, need = need }, missionContext) end
    have, need = string.match(raw, "^Handed in (%d+) of (%d+)$")
    if have ~= nil then return filled("Handed in {have} of {need}", { have = have, need = need }, missionContext) end
    tr = taskGiverText(raw, missions)
    if tr ~= nil then return tr end
    local distance, detail = string.match(raw, "^(About [%d?]+ meters [a-z%-]+)%. (.+)$")
    if distance == nil then distance, detail = string.match(raw, "^(About %? meters out there)%. (.+)$") end
    if distance ~= nil then
        local a = distance == "About ? meters out there" and lookup("out there")
            or findTranslation(distance, boardText.stage, boardValue)
        local b = lookup(detail) or findTranslation(detail, boardText.stage, boardValue)
        if a ~= nil then return a .. ". " .. (b or detail) end
    end
    if raw == "About ? meters out there" then return lookup("out there") end
    tr = findTranslation(raw, boardText.stage, boardValue)
    if tr ~= nil then return tr end
    if raw == "Look around" then return lookup(raw, nil, true) end
    local title = treeTitle(raw)
    if title ~= raw then return title end
end

local function wrapMissionText(original, board)
    return function(raw, vars, ...)
        if type(raw) == "string" and vars == nil and turkish() then
            -- Keep the official/static IG lookup ahead of the reconstructed templates.
            if lookup(raw) == nil then
                local tr = missionText(raw, (board.state or {}).missions)
                if tr ~= nil then return tr end
            end
        end
        return original(raw, vars, ...)
    end
end

local treeContext = "alifetr.tree.note"
local function treeNote(raw)
    if type(raw) ~= "string" then return raw end
    local tr = lookup(raw, treeContext)
    if tr ~= nil then return tr end
    tr = findTranslation(raw, boardText.tree, function(field, value)
        return field == "task" and treeTitle(value) or value
    end)
    if tr ~= nil then return tr end
    if raw == "No tasks right now" then return lookup(raw) or raw end
    local count, item = string.match(raw, "^Received (%d+)x (.+)$")
    if count ~= nil then return filled("Received {count}x {item}", { count = count, item = item }, treeContext) or raw end
    item = string.match(raw, "^Found: (.+)$")
    if item ~= nil then return filled("Found: {item}", { item = item }, treeContext) or raw end
    local task = string.match(raw, "^Task failed: (.+)$")
    if task ~= nil then return filled("Task failed: {task}", { task = treeTitle(task) }, treeContext) or raw end
    local who = string.match(raw, "^Task done: go back to (.+)$")
    if who ~= nil then return filled("Task done: go back to {who}", { who = who }, treeContext) or raw end
    return raw
end

local function wrapTreeNote(original)
    return function(args, ...)
        if type(args) == "table" and turkish() then
            local translated = treeNote(args.text)
            if translated ~= args.text then
                args = copy(args)
                args.text = translated
            end
        end
        return original(args, ...)
    end
end

local function wrapTreeResult(original)
    return function(panel, args, ...)
        if type(args) == "table" and args.ok == true and type(args.notes) == "table" and turkish() then
            local notes
            for index, raw in ipairs(args.notes) do
                local translated = treeNote(raw)
                if translated ~= raw then
                    notes = notes or copy(args.notes)
                    notes[index] = translated
                end
            end
            if notes ~= nil then
                args = copy(args)
                args.notes = notes
            end
        end
        return original(panel, args, ...)
    end
end

local mapContext = "alifetr.map.tip"
local mapTitles = {
    task = "A task is here", base = "Outpost", extraction = "Extraction zone",
    radio = "Radio mark", generic = "Marked place",
}
local function mapText(raw)
    local who = string.match(raw, "^Task: Report to (.+)$")
    if who == "them" then
        local label = lookup("Talk to the one who asked")
        return label and filled("Task: {title}", { title = label }) or raw
    end
    if who ~= nil then return filled("Task: Report to {who}", { who = who }) or raw end
    local title = string.match(raw, "^Task: (.+)$")
    if title ~= nil and treeTitles[title] then return filled("Task: {title}", { title = treeTitle(title) }) or raw end
    if raw == "Last seen here" then return lookup(raw) or raw end
    return treeTitle(raw)
end

local function wrapMapTip(original)
    return function(row, ...)
        local lines = original(row, ...)
        if type(lines) ~= "table" or not turkish() then return lines end
        local title = mapTitles[row.kind]
        if row.kind == "extraction" and lines[1] ~= nil and lines[1].text == title then
            lines[1].text = lookup(title, mapContext) or title
        end
        if lines[2] ~= nil and title ~= nil and lines[2].text == title
                and (row.kind ~= "generic" or #row.lines == 0) then
            local context = row.kind ~= "base" and mapContext or nil
            lines[2].text = lookup(title, context) or title
        end
        for _, line in ipairs(lines) do
            if type(line.text) == "string" then line.text = mapText(line.text) end
        end
        return lines
    end
end

local function wrapCreatorModal(original)
    return function(class, x, y, w, h, text, yesno, subject, ...)
        local creator = ProjectALife.CreatorScreen
        if creator ~= nil and creator.window ~= nil and type(subject) == "table"
                and subject.window == creator.window and type(text) == "string" and turkish() then
            text = findTranslation(text, boardText.modal) or text
        end
        return original(class, x, y, w, h, text, yesno, subject, ...)
    end
end

local function wrapShare(original)
    return function(...)
        local text = original(...)
        if not turkish() or type(text) ~= "string" then return text end
        return (string.gsub(text, "[^\n]+", function(line)
            -- Specific variants carry the Workshop ID or additional item count.
            for _, index in ipairs({4, 7, 1, 2, 3, 5, 6, 8}) do
                local tr = translate(line, boardText.share[index])
                if tr ~= nil then return tr end
            end
        end))
    end
end

local function wrapSaveStatus(original)
    return function(label, text, tone, ...)
        if tone == "error" and type(text) == "string" and turkish() then
            local reason = string.match(text, "^SAVE FAILED: (.+)$")
            if reason ~= nil then
                text = filled("SAVE FAILED: {reason}", { reason = lookup(reason) or reason }) or text
                return original(label, text, tone, ...)
            end
            local field, problem = string.match(text, "^([^:]+): (.+)$")
            local translated = problem and findTranslation(problem, boardText.number)
            if translated ~= nil then text = (lookup(field) or field) .. ": " .. translated end
        end
        return original(label, text, tone, ...)
    end
end

local function wrapSaveNotice(original)
    return function(text, ...)
        if type(text) == "string" and turkish() then
            local reason = string.match(text, "^NPC save failed: (.+)$")
            local title = reason and lookup("NPC save failed")
            if title ~= nil then text = title .. ": " .. (lookup(reason) or reason) end
        end
        return original(text, ...)
    end
end

local function withMethod(target, slot, make, callback, ...)
    local previous = rawget(target, slot)
    target[slot] = make(target[slot])
    local ok, result = pcall(callback, ...)
    target[slot] = previous
    if not ok then error(result, 0) end
    return result
end

local clothingRoles = { civilian = "Civilian", law = "Police", military = "Military",
    fire = "Firefighter", medical = "Medical" }

local function wrapClothingSummary(original, view)
    return function(self, shown, hidden, ...)
        local raw = original(self, shown, hidden, ...)
        if view.showAll or not turkish() then return raw end
        local season = ProjectALife.ClothingHealth.SEASON_WORD[self.season] or "Any season"
        local kind = self.role and self.role.kind or "civilian"
        local role = clothingRoles[kind] or kind
        return filled("{season} set, {role}: {shown} shown, {hidden} hidden. SHOW ALL lists every item.",
            { season = lookup(season) or season, role = lookup(role) or role, shown = shown, hidden = hidden }) or raw
    end
end

local function clothingCollision(item, found)
    local first = found[1]
    local name = item.label
    if name == nil or name == "" then name = ProjectALife.ClothingAdvisor.nameOf(item.id) end
    local text = filled("{item} collides with {other} ({slot} slot).",
        { item = name, other = first.name, slot = lookup(first.slot) or first.slot })
    if text == nil then return nil end
    local wasSame = "Both use the same body location."
    if first.same then
        text = text .. " " .. (lookup(wasSame) or wasSame)
    elseif first.reason ~= nil and first.reason ~= "" then
        text = text .. " " .. (lookup(first.reason) or first.reason) .. "."
    end
    if #found > 1 then
        local others = {}
        for index = 2, #found do others[#others + 1] = found[index].name end
        local items = table.concat(others, ", ")
        text = text .. " " .. (filled("It also collides with {items}.", { items = items })
            or ("It also collides with " .. items .. "."))
    end
    if first.alternative ~= nil then
        local alternative = first.alternative.name
        text = text .. " " .. (filled("Compatible alternative: {item}.", { item = alternative })
            or ("Compatible alternative: " .. alternative .. "."))
    end
    local question = "Pick it anyway?"
    return text .. "\n" .. (lookup(question) or question)
end

local function wrapClothingGuard(original)
    return function(self, item, selected, proceed, ...)
        if not turkish() or item == nil or ISModalDialog == nil or type(ISModalDialog.new) ~= "function"
                or lookup("{item} collides with {other} ({slot} slot).") == nil then
            return original(self, item, selected, proceed, ...)
        end
        return withMethod(ISModalDialog, "new", function(new)
            return function(class, x, y, w, h, text, yesno, subject, ...)
                if type(subject) == "table" and subject.view == self and subject.id == item.id then
                    local found = self:collision(item)
                    if found ~= nil and found[1] ~= nil then text = clothingCollision(item, found) or text end
                end
                return new(class, x, y, w, h, text, yesno, subject, ...)
            end
        end, original, self, item, selected, proceed, ...)
    end
end

local loanNotices = {
    compile("Your {item} is back by the door."),
    compile("There is no sign of your {item}. The neighbour never brought it back."),
}

local function translateLoan(text)
    if type(text) ~= "string" or #text > 400 or not turkish() then return nil end
    local tr = findTranslation(text, loanNotices)
    if tr ~= nil and #tr <= 400 then return tr end
end

local function wrapLoanNotice(original)
    return function(arguments, ...)
        local tr = type(arguments) == "table" and translateLoan(arguments.text)
        if tr then
            arguments = copy(arguments)
            arguments.text = tr
        end
        return original(arguments, ...)
    end
end

local function wrapLocalLoanTell(original)
    return function(player, text, ...)
        return original(player, translateLoan(text) or text, ...)
    end
end

local function wrapImport(original)
    local status = compile("MISSING ITEMS - {count} - FULL LIST IN CONSOLE.TXT")
    return function(window, ...)
        local label = window and window.statusLabel
        if type(label) ~= "table" or type(label.setName) ~= "function" or not turkish() then
            return original(window, ...)
        end
        return withMethod(label, "setName", function(setName)
            return function(self, text, ...)
                return setName(self, type(text) == "string" and translate(text, status) or text, ...)
            end
        end, original, window, ...)
    end
end

local function wrapPosPaint(original)
    return function(panel, ...)
        local label = turkish() and lookup("(not showing now)")
        if not label or type(panel) ~= "table" or type(panel.drawText) ~= "function" then
            return original(panel, ...)
        end
        return withMethod(panel, "drawText", function(drawText)
            return function(self, text, ...)
                if type(text) == "string" then
                    text = string.gsub(text, " %(not showing now%)$", function() return " " .. label end)
                end
                return drawText(self, text, ...)
            end
        end, original, panel, ...)
    end
end

local function wrapRadioOption(original)
    return function(self, frequency, name, ...)
        if name == "Knox County Radio" and turkish() then name = lookup(name) or name end
        return original(self, frequency, name, ...)
    end
end

local function wrapGiverDraw(original, map)
    return function(target, ...)
        if not turkish() or type(target) ~= "table" or type(target.drawText) ~= "function" then
            return original(target, ...)
        end
        local labels = {}
        for _, row in ipairs(map.rows or {}) do
            local title = treeTitle(row.title)
            local label = row.name .. ": " .. (lookup(title) or title)
            if row.stale then
                local seen = lookup("Last seen here")
                if seen ~= nil then labels[row.label .. " (last seen)"] = label .. " (" .. seen .. ")" end
            else
                labels[row.label] = label
            end
        end
        return withMethod(target, "drawText", function(drawText)
            return function(self, text, ...) return drawText(self, labels[text] or text, ...) end
        end, original, target, ...)
    end
end

local extractionName = "Extraction zone"
local extractionId = "ending_zone"

local function extractionKey()
    return ProjectALife.Text.key("IGUI_ALifeUI_", extractionName, mapContext)
end

local function clearExtractionIcon(labels, x, y)
    if labels == nil or type(labels.clear) ~= "function" then return false end
    if not labels.clear(extractionName, x, y) then return false end
    if type(labels.save) == "function" then labels.save() end
    return true
end

local function nearNumber(a, b)
    return type(a) == "number" and type(b) == "number" and math.abs(a - b) < 0.01
end

local function oldExtractionStyle(symbol)
    return type(symbol.getRed) == "function" and type(symbol.getGreen) == "function"
        and type(symbol.getBlue) == "function" and type(symbol.getScale) == "function"
        and nearNumber(symbol:getRed(), 1) and nearNumber(symbol:getGreen(), 0.7)
        and nearNumber(symbol:getBlue(), 0.1) and nearNumber(symbol:getScale(), 1.5)
end

local function dropOldExtraction(x, y)
    local api = ProjectALife.RadioClient.symbols()
    if api == nil or type(api.removeSymbolByIndex) ~= "function" then return end
    for index = api:getSymbolCount() - 1, 0, -1 do
        local symbol = api:getSymbolByIndex(index)
        if symbol ~= nil and type(symbol.getUntranslatedText) == "function"
                and symbol:getUntranslatedText() == extractionName
                and nearNumber(symbol:getWorldX(), x) and nearNumber(symbol:getWorldY(), y)
                and oldExtractionStyle(symbol) then
            api:removeSymbolByIndex(index)
        end
    end
end

local function wrapExtractionMark(original)
    return function(args, ...)
        local haven = ProjectALife.SafehouseClient
        local labels, defs = ProjectALife.MapLabels, ProjectALife.MissionDefs
        if type(args) ~= "table" or args.id ~= extractionId or args.name ~= extractionName
                or tonumber(args.x) == nil or tonumber(args.y) == nil or haven == nil
                or (defs ~= nil and type(defs.fallbackOn) == "function" and defs.fallbackOn()) then
            return original(args, ...)
        end
        local icons = labels ~= nil and labels.on()
        local key = extractionKey()
        local legacy = not icons and ProjectALife.Text.lookup(key) ~= nil
        if legacy then
            args = copy(args)
            args.name = key
        end
        local marked = original(args, ...)
        if marked and (legacy or icons) then
            local x, y = tonumber(args.x), tonumber(args.y)
            if legacy then
                clearExtractionIcon(labels, x, y)
                dropOldExtraction(x, y)
            elseif type(haven.dropSymbols) == "function" then
                haven.dropSymbols(key, x, y)
            end
        end
        return marked
    end
end

local function wrapExtractionUnmark(original, radio)
    return function(id, ...)
        local row = id == extractionId and radio.marks[id] or nil
        local removed = original(id, ...)
        local haven = ProjectALife.SafehouseClient
        if row ~= nil and haven ~= nil and type(haven.dropSymbols) == "function" then
            local key = extractionKey()
            if row.text == key then
                removed = clearExtractionIcon(ProjectALife.MapLabels, row.x, row.y) or removed
            else
                removed = haven.dropSymbols(key, row.x, row.y) > 0 or removed
            end
        end
        return removed
    end
end

local function restoreExtraction()
    local radio, data = ProjectALife.RadioClient, ProjectALife.EndingData
    if radio == nil or data == nil or radio.marks[extractionId] ~= nil then return end
    local api = radio.symbols()
    local key = extractionKey()
    if api == nil or ProjectALife.Text.lookup(key) == nil then return end
    for index = 0, api:getSymbolCount() - 1 do
        local symbol = api:getSymbolByIndex(index)
        if symbol ~= nil and type(symbol.getUntranslatedText) == "function" then
            local text = symbol:getUntranslatedText()
            if text == key or text == extractionName then
                local x, y = symbol:getWorldX(), symbol:getWorldY()
                for _, pad in pairs({ data.pad, data.padOld }) do
                    if nearNumber(x, pad.x) and nearNumber(y, pad.y) then
                        -- A player note needs more than the same title and position to match.
                        if text == extractionName and type(symbol.setUntranslatedText) == "function"
                                and oldExtractionStyle(symbol) then
                            symbol:setUntranslatedText(key)
                            text = key
                        end
                        if text == key then
                            radio.marks[extractionId] = { text = key, x = x, y = y }
                            return
                        end
                    end
                end
            end
        end
    end
end

local function wrapWorldMapShow(original)
    return function(...)
        local shown = original(...)
        local ok, err = pcall(restoreExtraction)
        if not ok then print("[ProjectALife TR] Extraction map symbol: " .. tostring(err)) end
        return shown
    end
end

local function wrapStatusNew(original)
    return function(self, ...)
        local window = original(self, ...)
        if turkish() then
            local title = lookup("Project A-Life Status")
            if title ~= nil then window:setTitle(ProjectALife.Version.title(title)) end
        end
        return window
    end
end

local function wrapDropChoices(original, field)
    return function(panel, x, y, width, options, ...)
        local policy = ProjectALife.DropPolicy
        if turkish() and policy ~= nil and options == policy[field] then
            local labels = {}
            for index, option in ipairs(options) do
                labels[index] = copy(option)
                labels[index][1] = lookup(option[1]) or option[1]
            end
            options = labels
        end
        return original(panel, x, y, width, options, ...)
    end
end

local function wrapRelationLabel(original)
    return function(...)
        local label = original(...)
        return turkish() and (lookup(label) or label) or label
    end
end

local blocLabels = { military = "Military", civilian = "Civilian", law = "Law" }

local function wrapRelationWhy(original)
    return function(layer, bloc, ...)
        local label = blocLabels[bloc]
        if label ~= nil and turkish() and (layer == "bloc" or layer == "profession_default") then
            bloc = lookup(label) or bloc
        end
        return original(layer, bloc, ...)
    end
end

local function wrapRelationStatus(original, creator)
    return function(window, ...)
        if not turkish() or window == nil or type(creator.mirroredPlayerRelation) ~= "function" then
            return original(window, ...)
        end
        local word, source
        local result = withMethod(creator, "mirroredPlayerRelation", function(mirrored)
            return function(...)
                word, source = mirrored(...)
                return word, source
            end
        end, original, window, ...)
        if word ~= nil and source ~= nil and window.effectiveRelationStatus ~= nil then
            local title = filled("PLAYER  {value}  /  {source}", { value = creator.relationLabel(word), source = source })
            if title ~= nil then window.effectiveRelationStatus:setName(title) end
        end
        return result
    end
end

local function wrapFolderTooltip(original)
    return function(control, text, ...)
        if type(text) == "string" and turkish() then
            local folder = string.match(text, "^(.+)%.  Click to fold or unfold%.$")
            if folder ~= nil then text = filled("{folder}. Click to fold or unfold.", { folder = lookup(folder) or folder }) or text end
        end
        return original(control, text, ...)
    end
end

local function wrapSeasonTitle(original, creator)
    return function(profile, id, status, ...)
        local raw = original(profile, id, status, ...)
        if not turkish() then return raw end
        local season = profile.outfitSeason and profile.outfitSeason[id]
        local suffix = status == " +" and " +" or status == "  OFF" and " -" or ""
        for _, spec in ipairs(creator.seasonSpecs or {}) do
            if spec.season == season then return id .. " " .. (lookup(spec.label) or spec.label) .. suffix end
        end
        local any = lookup("Any", "alifetr.creator.season")
        return any and (id .. " " .. any .. suffix) or raw
    end
end

local function wrapOutfitSummary(original, health)
    return function(result, season, ...)
        local raw = original(result, season, ...)
        if not turkish() then return raw end
        if result == nil then return lookup("No clothing data for this set.") or raw end
        if result.empty then return lookup("EMPTY SET") or raw end
        local name = season ~= nil and health.SEASON_WORD[season] or "Any season"
        local vars = { season = lookup(name) or name, count = #result.issues }
        local template = result.ok and "VALID FOR {season}"
            or (vars.count == 1 and "{count} ISSUE FOR {season}" or "{count} ISSUES FOR {season}")
        return filled(template, vars) or raw
    end
end

local function statusValue(value)
    value = tostring(value or "none")
    local common = { on = "On", off = "Off", none = "None" }
    return lookup(value, "alifetr.status.value") or (common[value] and lookup(common[value])) or value
end

local function censusNames(value)
    if value == nil then return statusValue("none") end
    local raw, parts, cursor = tostring(value), {}, 1
    while true do
        local first, last, label, counts = string.find(raw, "(.-) (%d+/%d+/%d+)", cursor)
        if first == nil then
            parts[#parts + 1] = string.sub(raw, cursor)
            return table.concat(parts)
        end
        local separator, name = string.match(label, "^(,?%s*)(.+)$")
        if name ~= nil then label = separator .. (lookup(name) or name) end
        parts[#parts + 1] = label .. " " .. counts
        cursor = last + 1
    end
end

local function statusDisplayRows(s)
    local runtime = "running"
    if s.runtimeEnabled == false then runtime = "disabled"
    elseif s.runtimeStarted ~= true then
        runtime = "starting"
        local retry = ProjectALife.RuntimeRetry
        if s.startState ~= nil and retry ~= nil then runtime = retry.line(s.startState, s.startRetry, s.startReason) end
    elseif (tonumber(s.tickCount) or 0) == 0 then runtime = "waiting for first tick" end

    local function count(key) return { count = s[key] or 0 } end
    local census = "World census: {alive} in the world, {living} living of {total}, killed {killed}, arrivals {arrivals}"
    if s.censusSetting ~= nil and s.censusSetting ~= s.censusTotal then
        census = "World census: {alive} in the world, {living} living of {total} (this world's pool was fixed at {total} when it began; the setting now says {setting} and applies to new worlds), killed {killed}, arrivals {arrivals}"
    end
    local offline = "Offline founded / refused: {founded} / {refused}"
    if s.offlineRefusedWhy ~= nil then offline = offline .. " ({reason})" end
    return {
        { "Actors: ", "Actors: {count}", count("total") },
        { "Active / spawning: ", "Active / spawning: {active} / {spawning}", { active = s.active or 0, spawning = s.spawning or 0 } },
        { "Dormant / dead: ", "Dormant / dead: {dormant} / {dead}", { dormant = s.dormant or 0, dead = s.dead or 0 } },
        { "Physical shells: ", "Physical shells: {count}", count("shells") },
        { "Running actions: ", "Running actions: {count}", count("runningActions") },
        { "Pending spawns: ", "Pending spawns: {count}", count("pendingSpawns") },
        { "Watchdog recoveries: ", "Watchdog recoveries: {count}", count("recoveries") },
        { "Offline squads on the map: ", "Offline squads on the map: {count}", count("offlineSquads") },
        { "Offline founded / refused: ", offline, { founded = s.offlineFounded or 0, refused = s.offlineRefused or 0, reason = statusValue(s.offlineRefusedWhy) } },
        { "Far cleaner: ", "Far cleaner: {profile} map, {state}, stowed {groups} groups / {people} NPCs",
            { profile = statusValue(s.farCleanerProfile), state = statusValue(s.farCleanerOn == true and "on" or "off"), groups = s.farCleanerGroups or 0, people = s.farCleanerActors or 0 } },
        { "Encounter rolls / spawned: ", "Encounter rolls / spawned: {rolls} / {spawned}", { rolls = s.encounterRolls or 0, spawned = s.encounterPlaced or 0 } },
        { "Runtime: ", "Runtime: {state}", { state = statusValue(runtime) } },
        { "Pacing: ", "Pacing: {crews} new crews, {refusals} refusals", { crews = s.worldPressureCommitted or 0, refusals = s.worldPressureRefused or 0 } },
        { "Last pacing refusal: ", "Last pacing refusal: {reason} (last delay {hours}h)", { reason = statusValue(s.worldPressureReason), hours = s.worldPressureRetryHours or 0 } },
        { "Proof car: ", "Proof car: {state}", { state = statusValue(s.roadProof or "off") } },
        { "World census: ", census, { alive = s.censusAlive or 0, living = s.censusLiving or 0,
            total = s.censusTotal or 0, setting = s.censusSetting, killed = s.censusKilled or 0, arrivals = s.censusArrivals or 0 } },
        { "Census by faction (alive/killed/arrived): ", "Census by faction (alive/killed/arrived): {factions}", { factions = censusNames(s.censusFactions) } },
        { "Health: ", s.healthOk == true and "Health: OK" or "Health: {errors} error(s)", { errors = s.healthErrors or 0 } },
        { "Runtime faults / overruns: ", "Runtime faults / overruns: {faults} / {overruns}", { faults = s.runtimeFaults or 0, overruns = s.tickOverruns or 0 } },
        { "Protected areas: ", "Protected areas: {count}", count("noSpawnZones") },
        { "Tick ms (last / max): ", "Tick ms (last / max): {last} / {max}", { last = s.lastTickMs or 0, max = s.maximumTickMs or 0 } },
        { "Tick count / budget: ", "Tick count / budget: {count} / {budget}", { count = s.tickCount or 0, budget = s.tickBudget or 0 } },
    }
end

local function wrapStatusRows(original)
    return function(self, ...)
        local rows = original(self, ...)
        local waiting = "Waiting for server status..."
        if not turkish() or rows[1] == nil then return rows end
        if self.status == nil and rows[1].text == waiting then
            rows[1].text = lookup(waiting) or waiting
        elseif type(self.status) == "table" then
            local rules, index = statusDisplayRows(self.status), 1
            for _, row in ipairs(rows) do
                if not row.heading then
                    local rule = rules[index]
                    if rule == nil or type(row.text) ~= "string" or string.sub(row.text, 1, #rule[1]) ~= rule[1] then break end
                    row.text = filled(rule[2], rule[3]) or row.text
                    index = index + 1
                end
            end
        end
        return rows
    end
end

local function install()
    if ProjectALife == nil then return end
    local phone, board = ProjectALife.PhonesClient, ProjectALife.UI2Missions
    wrap(phone, "line", function(original) return wrapPhoneLine(original, phone) end)
    wrap(phone, "buildAsk", wrapPhoneAsk)
    wrap(board, "text", function(original) return wrapMissionText(original, board) end)
    wrap(ProjectALife.UI2TalkTrees, "note", wrapTreeNote)
    wrap(ProjectALife.UI2TalkTrees, "result", wrapTreeResult)
    wrap(ProjectALife.MapLabels, "tipLines", wrapMapTip)
    local giverMap = ProjectALife.UI2GiverMap
    wrap(giverMap, "draw", function(original) return wrapGiverDraw(original, giverMap) end)
    wrap(ISModalDialog, "new", wrapCreatorModal)
    wrap(ProjectALife.FactionShare, "describeMissing", wrapShare)
    wrap(ProjectALife.CreatorScreen, "paintSaveStatus", wrapSaveStatus)
    wrap(ProjectALife.CreatorSaveQueue, "say", wrapSaveNotice)
    local clothingView = ProjectALife.CreatorScreen and ProjectALife.CreatorScreen.clothingView
    wrap(clothingView, "summaryText", function(original) return wrapClothingSummary(original, clothingView) end)
    wrap(clothingView, "guard", wrapClothingGuard)
    wrap(ProjectALife.CreatorScreen, "importFactionPack", wrapImport)
    wrap(ProjectALife.SafehouseClient, "notice", wrapLoanNotice)
    wrap(ProjectALife.SafehouseDirector, "tell", wrapLocalLoanTell)
    wrap(ProjectALife.UIPos, "editorPaint", wrapPosPaint)
    wrap(RWMChannel, "addComboOption", wrapRadioOption)
    local radio = ProjectALife.RadioClient
    wrap(radio, "mark", wrapExtractionMark)
    wrap(radio, "unmark", function(original) return wrapExtractionUnmark(original, radio) end)
    wrap(ISWorldMap, "ShowWorldMap", wrapWorldMapShow)
    wrap(ALifeStatusWindow, "new", wrapStatusNew)
    wrap(ALifeStatusWindow, "statusRows", wrapStatusRows)
    local creator, health = ProjectALife.CreatorScreen, ProjectALife.ClothingHealth
    wrap(creator, "addCombo", function(original) return wrapDropChoices(original, "presets") end)
    wrap(creator, "addNumberChoices", function(original) return wrapDropChoices(original, "conditions") end)
    wrap(creator, "relationLabel", wrapRelationLabel)
    wrap(creator, "relationWhy", wrapRelationWhy)
    wrap(creator, "refreshEffectiveRelation", function(original) return wrapRelationStatus(original, creator) end)
    wrap(creator, "addTooltip", wrapFolderTooltip)
    wrap(creator, "memberSeasonTitle", function(original) return wrapSeasonTitle(original, creator) end)
    wrap(health, "summary", function(original) return wrapOutfitSummary(original, health) end)
end

install()
if type(Events) == "table" then
    if Events.OnGameBoot then Events.OnGameBoot.Add(install) end
    if Events.OnGameStart then Events.OnGameStart.Add(install) end
end
