"""Modun Lua kodunda Text.ui'den geçen ama EN JSON'da anahtarı olmayan metinleri çıkarır.

Kullanım: python araclar/lua_cikar.py
Çıktı: kaynak/IG_UI_lua.json (EN, anahtar → metin), kaynak/IG_UI_lua_baglam.json (anahtar → dosya:satır)

Anahtar = "IGUI_ALifeUI_" + Text.hash(en) (ALifeText.lua). Oyun çeviriyi TR dosyasında bulur;
EN dosyasında olmaması sorun değil (getTextOrNull).
Doğrudan çağrılar (Text.ui("...")) kendiliğinden bulunur. Tablodan gelen metinler (Text.ui(row.label))
DOLAYLI listesiyle eklenir: her biri koda bakılarak Text.ui'ye gittiği doğrulanmış metinlerdir.
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
MOD = Path(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3803984183/mods/ProjectALifeNPCs/42.20/media/lua")
STR = r'"((?:[^"\\\n]|\\.)*)"'

# Dosya → Text.ui'ye tablo üzerinden giden metinler (kod okunarak seçildi)
DOLAYLI = {
    "ALifeFieldRadioWindow.lua": [  # tabs / blocs / stanceWords / reasons / head-note-empty yardımcıları
        "Standing", "Contacts", "Heard", "Notes",
        "Law and police", "Civilians and workers", "Families", "Gangs and criminals", "Raiders", "Careful",
        "Open the world map once, then try again.", "That marker is not on your map any more.",
        "This build cannot edit map markers.", "Select a contact first.", "That did not work.",
        "Nothing yet. Press Refresh to ask the server.", "How the blocs see you",
        "Last known standing, as the server told you. It can be out of date until you press Refresh.",
        "Your group", "People who told you where they live", "Nothing yet. Ask someone friendly: Where do you live?",
        "Heard on the air", "Nothing yet. Tune a radio to hear Knox County Radio.",
        "Letters, signs and news from your base", "Nothing yet. Notes appear when something happens at your base.",
        "Letters themselves are items in your inventory. This list only tells you that something was left.",
    ],
    "ALifeFieldRadioData.lua": [  # metaLabels
        "A helicopter passed over", "Military aircraft overhead", "A car crash in the distance",
        "A siren, a scream or a radio in the distance", "A siren over the county",
    ],
    "ALifeSafehouseClient.lua": [  # events → FieldRadio.noteTitle
        "Thank-you letter", "Warning letter", "Threat letter", "Demand letter", "Trade offer", "Honest map",
        "Apology", "Missing person notice", "Territory notice", "Last letter", "Gift",
        "Visitor: beggar", "Visitor: trader", "Visitor: law, stay inside (window)", "Visitor: law, census",
        "Visitor: asks to sleep one night", "Visitor: being chased", "Visitor: wounded at the window",
        "Visitor: protection racket", "Visitor: neighbour", "Visitor: returning your things",
        "Visitor: drunk (window)", "Visitor: preacher", "Visitor: fake police", "Visitor: medic on rounds",
        "Visitor: messenger with a job (window)", "Visitor: neighbour borrows a tool",
        "Visitor: police collecting weapons", "Visitor: asks you to come help (window)",
        "Visitor: a family in need (party)", "Visitor: a returning guest", "Visitor: asks to lodge a few nights",
        "Visitor: panicked knock, the dead behind", "Visitor: shelter from the weather",
        "Visitor: needs medical help", "Ladder 2: paint X by the door", "Ladder 3: sabotage while away",
        "Ladder 4: night raid", "Ladder 4: horde lure raid", "Ladder 4: power cut raid", "Ladder 4: siege",
        "Sign: fuel siphoned from a car", "Sign: garden picked", "Night: flashlight at the window",
        "Sign: camp traces", "Sign: front door left open", "Mark: chalk symbol", "Mark: tally marks",
        "Mark: faction colours", "Night: knock, nobody there", "Radio: your house mentioned",
        "Night: distant gunshots", "Night: a dog barking", "Night: glass breaks nearby", "Mark: blood by the door",
    ],
    "ALifeTalkCinema.lua": [  # pushChip / orderTips / markedChips
        "Police", "Medic", "Veteran", "Craft", "Order", "Toll", "Duty", "Shelter", "Trade", "Weather", "Reply",
        "Asked", "Suggested", "Risky", "New", "Later",
        "Make them raise their hands.", "Make them drop their weapon.",
        "Make them drop the weapon and raise their hands.", "Demand everything they are carrying.",
        "Tell them to get out of here.", "Tell them and their group to clear out of the area.",
        "Make them fall in behind you.", "Take the weapons from someone who has surrendered.",
        "Search the pockets of someone who has surrendered.", "Let them lower their hands.",
    ],
    "ALifeWounds.lua": [  # Wounds.label / Wounds.partLabel
        "scratch", "laceration", "deep wound", "bite", "bullet wound", "bruise", "fracture", "burn",
        "head", "torso", "left arm", "right arm", "left leg", "right leg",
        "bleeding", "bandaged", "splinted",  # Wounds.label("bleeding") vb.: tabloda yok, doğrudan geçer
    ],
    "ALifeTalkSocial.lua": [  # Social.reasons → fikir kaydı nedeni (Cinema: Text.ui(reason))
        "You were friendly.", "You left on good terms.", "You were easy to talk to.", "You showed you cared.",
        "You offered to help.", "You asked about their life and they opened up.", "You got too personal, too soon.",
        "You pushed for details about their people.", "You asked for a handout.", "You came at them with words.",
        "You asked at a bad moment.", "You kept asking the same thing.", "You wore out their patience.",
        "They were glad you came back.",
    ],
    "ALifeTalkQuestions.lua": ["You answered their question"],
    "ALifeNpcOpinion.lua": [  # labels → Text.ui(opinion.label); why/reason
        "Hates you", "Resents you", "Distrusts you", "Unsure of you", "Likes you", "Trusts you", "Would stand by you",
        "You shared food or water with them.", "You patched someone up.", "You fought beside them.",
        "You saved a life.", "You dealt fairly.", "You kept your word.", "You treated them well at the door.",
        "You walked the road together.", "You threatened them and it did not work.", "You were rude to them.",
        "You took things from them.", "You hit one of theirs.", "You killed one of their own.", "You broke a deal.",
        "You came through for the group.", "You let the group down on a job.", "You left them when it mattered.",
        "A stranger so far, judged by what they have heard.",
        "I'm not telling you anything.", "I don't know you well enough for that.",
        "Not yet. Ask me when I trust you more.",
    ],
}
# Ziyaretçi/kapı sistemi (K46). Sonda eklenir, önceki anahtarların sırası bozulmasın.
DOLAYLI_ZIYARETCI = {
    "ALifeVisitorTalk.lua": [  # tabLabels → Menu.groupLabel: Text.ui(group.label)
        "Talk", "Past", "Now", "House", "World", "Offer", "Closer",
    ],
    "ALifeSafehouseEvents.lua": [  # row.notice → Director.tell → SafehouseClient.notice (ek, IGUI anahtarı)
        "Planks pried off the windows and glass on the ground. Someone worked on the house while you were out.",
        "The fuel tank is lower than you left it. Someone has been at it.",
        "Your garden has been picked over. Someone took the ripe crops.",
        "A flashlight beam sweeps your windows from outside, then goes out.",
        "Empty cans and litter by the house. Someone watched this place for a night.",
        "The front door stands open. You left it shut.",
        "Three knocks at the door. When you look, nobody is there.",
        "On the radio someone talks about a house with a running generator. It sounds like yours.",
        "Shots, far off. A few of them, then nothing.",
        "A dog barks somewhere out in the dark. It goes on for a while.",
        "Glass breaks somewhere close. Then it is quiet again.",
    ],
    "ALifeSafehouseDirector.lua": [  # markTexts ({faction}'lı flag hariç) ve Director.tell/notice sabitleri
        "A chalk symbol by the door. Travellers' code: kind people live here.",
        "A chalk symbol by the door. Travellers' code: this house has food.",
        "A chalk symbol by the door. Travellers' code: armed, keep away.",
        "Fresh paint by the front door: a big X at eye level. Someone marked this house.",
        "Tally marks scratched by the door. Someone is counting how many live here.",
        "Blood smeared on the wall by the front door. It is fresh.",
        "A mark by the door.",
        "You scrub the mark off the wall.",
        "You delivered the message. They will remember it.",
        "Your help was needed, and it was real. They shared what they had.",
        "The days to deliver the note have run out.",
        "Whatever was happening out there is over now.",
    ],
}
# Oyuncu bildirimleri (K46). KAMP'tan sonra eklenir, önceki anahtarların sırası bozulmasın.
DOLAYLI_BILDIRIM = {
    "ALifeTalk.lua": [  # Talk.typedNotices → Party.notice → SafehouseClient.notice (ek, IGUI anahtarı)
        "Step closer to the door to talk to them",
        "Pick one of the door options to talk to them",
        "They can't answer right now",
        "They are thinking it over, try again in a moment",
        "Not now! Wait until the fighting or danger has passed, then try Talk again",
        "They're in too much pain to talk. Help them recover, then try again",
        "No trade is available here. Open Talk with a trader to see an offer",
        "They can't offer a trade right now. Try Talk again later",
        "Their last trade is still being settled. Try Talk again later",
        "Open the door before trying to trade",
    ],
    "ALifeOutpostExpeditions.lua": [  # Standoff.notify → Input.showNotice: Text.ui(text)
        "Heard a big armed group is coming down the road, get somewhere safe",
        "Three groups just left together, keep your eyes on the road",
    ],
    "ALifeModuleCareful.lua": [  # Careful.heardWords → Careful.relay (ek, IGUI anahtarı) → setHaloNote
        "You hear people up ahead shouting at you to turn back",
        "You hear fighting ahead, and somebody in it yelling at you to keep away",
        "They're shouting again, sounds like the last warning",
        "They're shouting at you to back off, get away from there",
    ],
}
# camp_traces bildirimi (Director.scatterTraces): nights 1-3, "a night" → "N nights"; ateş yalnız 2+ gecede eklenir.
# Anahtar dolu metnin hash'i olduğu için her biçim ayrı satırdır.
KAMP = "Empty cans and litter by the house. Someone watched this place for {}."
KAMP_ATES = " Someone kept a small fire going."
KAMP_BICIMLER = [KAMP.format(g) + ates for g in ("2 nights", "3 nights") for ates in ("", KAMP_ATES)]
# Konuşma menüsü satır tabloları (Rows.add / addGroup): text, tip, hint, label, title, variants alanları
# Text.ui(Intents.choiceLabel(...)), Text.ui(choice.tip), Text.ui(group.label) ile ekrana gider.
SATIR_ALANLARI = re.compile(r'\b(text|tip|hint|label|title|variants)\s*=\s*(\{[^{}]*\}|' + STR + ')')
SATIR_TABLOSU = re.compile(r'\b[A-Za-z]+\.(?:add|addGroup|addChoice)\(\{')
# ALifeRepLevels.lua: text.ui(row.en) ve text.ui(row.hint) → tablo satırlarının hepsi
REP_DOSYA = "ALifeRepLevels.lua"


def h(t):
    a, b = 5381, 52711
    for c in t.encode("utf-8"):
        a = (a * 33 + c) % 2147483647
        b = (b * 131 + c) % 2147483629
    return "%08x%08x" % (a, b)


YOK = []  # --devam: kodda bulunamayan DOLAYLI metinler (varsayılan: ilkinde durur)


def bulunamadi(ad, en):
    if "--devam" not in sys.argv:
        raise SystemExit(f"{ad}: bulunamadı (mod değişmiş olabilir): {en!r}  (hepsini listelemek için --devam)")
    YOK.append((ad, en))


def un(s):
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")


def main():
    en_json = json.loads((MOD / "shared/Translate/EN/IG_UI.json").read_text(encoding="utf-8"))
    dosyalar = {f.name: f for f in MOD.rglob("*.lua")}
    # L3 satırları kaynak dosyaya elle eklendi, buradaki taramada yok: var olan anahtarlar korunur, sıra bozulmaz
    hedef = KOK / "kaynak"
    cikti = json.loads((hedef / "IG_UI_lua.json").read_text(encoding="utf-8"))
    baglam = json.loads((hedef / "IG_UI_lua_baglam.json").read_text(encoding="utf-8"))

    def ekle(en, yer, ctx=None):
        key = "IGUI_ALifeUI_" + h((ctx + "|" + en) if ctx is not None else en)
        if key in en_json or not en.strip():
            return
        cikti.setdefault(key, en)
        baglam.setdefault(key, [])
        if yer not in baglam[key]:
            baglam[key].append(yer)

    dogrudan = re.compile(r'(?:\b[Tt]ext\.|FieldRadio\.)(?:ui|msg|forPlayer)\(\s*' + STR +
                          r'(\s*,\s*(?:nil|\{[^{}]*\}|[A-Za-z_][\w.]*)\s*,\s*' + STR + r')?')
    kelime = re.compile(r'Cinema\.word\(\s*' + STR + r'\s*,\s*' + STR)
    for ad, f in sorted(dosyalar.items()):
        s = f.read_text(encoding="utf-8", errors="ignore")
        for m in dogrudan.finditer(s):
            ctx = un(m.group(3)) if m.group(3) is not None else None
            ekle(un(m.group(1)), f"{ad}:{s.count(chr(10), 0, m.start()) + 1}", ctx)
        for m in kelime.finditer(s):
            ekle(un(m.group(2)), f"{ad}:{s.count(chr(10), 0, m.start()) + 1}")

    for ad, liste in DOLAYLI.items():
        s = dosyalar[ad].read_text(encoding="utf-8", errors="ignore")
        for en in liste:
            i = s.find('"' + en.replace('"', '\\"') + '"')
            if i < 0:
                bulunamadi(ad, en)
                continue
            ekle(en, f"{ad}:{s.count(chr(10), 0, i) + 1}")

    for ad, f in sorted(dosyalar.items()):
        if not re.search(r'Rows|Intents', ad):
            continue
        s = f.read_text(encoding="utf-8", errors="ignore")
        for m in SATIR_TABLOSU.finditer(s):
            i, d = m.end(), 1
            while d and i < len(s):
                d += (s[i] == "{") - (s[i] == "}")
                i += 1
            govde = s[m.end():i - 1]
            for fm in SATIR_ALANLARI.finditer(govde):
                for sm in re.finditer(STR, fm.group(2)):
                    ekle(un(sm.group(1)), f"{ad}:{s.count(chr(10), 0, m.start()) + 1}")

    s = dosyalar[REP_DOSYA].read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'\b(?:en|blurb|hint)\s*=\s*' + STR, s):
        ekle(un(m.group(1)), f"{REP_DOSYA}:{s.count(chr(10), 0, m.start()) + 1}")

    for ad, liste in DOLAYLI_ZIYARETCI.items():
        s = dosyalar[ad].read_text(encoding="utf-8", errors="ignore")
        for en in liste:
            i = s.find('"' + en + '"')
            if i < 0:
                bulunamadi(ad, en)
                continue
            ekle(en, f"{ad}:{s.count(chr(10), 0, i) + 1}")
    s = dosyalar["ALifeSafehouseDirector.lua"].read_text(encoding="utf-8", errors="ignore")
    i = s.find(KAMP_ATES)
    if i < 0 or '"a night", nights .. " nights"' not in s:
        raise SystemExit("ALifeSafehouseDirector.lua: kamp bildirimi değişmiş")
    for en in KAMP_BICIMLER:
        ekle(en, f"ALifeSafehouseDirector.lua:{s.count(chr(10), 0, i) + 1}")
    for ad, liste in DOLAYLI_BILDIRIM.items():
        s = dosyalar[ad].read_text(encoding="utf-8", errors="ignore")
        for en in liste:
            i = s.find('"' + en + '"')
            if i < 0:
                bulunamadi(ad, en)
                continue
            ekle(en, f"{ad}:{s.count(chr(10), 0, i) + 1}")

    (hedef / "IG_UI_lua.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")
    (hedef / "IG_UI_lua_baglam.json").write_text(json.dumps(baglam, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(cikti)} metin -> kaynak/IG_UI_lua.json")
    for ad, en in YOK:
        print(f"BULUNAMADI {ad}: {en!r}")


if __name__ == "__main__":
    main()
