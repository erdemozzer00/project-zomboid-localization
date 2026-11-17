"""NPC diyalog satırlarını (Talk/Data) çeviri kaynağına ekler.

Kullanım: python araclar/diyalog_cikar.py <grup>
Gruplar: d0 = konuşma penceresi açılış cevapları (NPC_OPEN), sivillere uyanlar
        d1 = sivil selamlaşma + evet/hayır cevapları · d2 = yoldan geçerken laf + kısa tepkiler
        d3 = salgının ilk günlerinde panik replikleri (PANIC, PANIC_DAY_*)
        d4 = küçük gruplar: enfekteyle temas, ev anısı, yalvarma, yere düşme, güvende an, arkadaşa vurulma
        d6a = sivillerin yoldan geçen başka bir NPC'yi selamlaması (PASSING_NPC_GREET)
        d6b = sivillerin tehlike sezmesi: duyulan sesler (HEARD_*), ordu/kalabalık zombi (HORDE_*), sürünen zombi
        d6c = sivillerin buldukları: ceset, kan, iz, mermi, silah, ilaç, yiyecek, su (FOUND_*, CORPSE_FOUND), boş/arama (LOOT_EMPTY, CONTAINER_SEARCH)
        d6d = sivillerin çatışma tepkileri: AFTER_FIGHT, CONTACT_HOSTILE, AIMED_AT, ALLY_DOWN, ALLY_HIT, COMBAT_END, COMBAT_ATTACK
        d6e = sivillerin hava, mevsim ve gün saati sözleri: COLD, HOT, WEATHER_*, SNOW_*, SHIVER, WET, SEASON_*, DAWN, NIGHTFALL
        d6f = sivillerin sohbet ve oyalanma sözleri: JOKE, CAMP_CHATTER, IDLE, LONG_WALK, STARE_PLAYER, LOCATION_COMMENT, CHECK_IN, HELPED_BY_PLAYER
        d6g = sivillerin yaralanma, hastalık, açlık/susuzluk ve erzak sözleri: INJURED_*, WOUNDED_HELP, HURT, SICK_*, COUGH, SNEEZE, SUPPLY_*, DAILY_NEEDS, HUNGRY...
        d6h = sivillerin çatışma çağrıları ve silah sorunları: GUN_FEAR, WEAPON_JAM, LOW_AMMO, REGROUP, RETREAT, COVER_ME, SURRENDER, MORALE_LOW, CONTACT/NEAR_MISS...
        d6i = sivillerin oyuncu ekibine katılma/ayrılma/görev sözleri: PARTY_* (JOIN_*, KICK, LEAVE_OK, LAG, LEFT_BEHIND, STORY_*, TASK_*, WARN_*)
        d6j = sivillerin oyuncu emirlerine (ORD_*), soygun (ROBBERY_*), karşılaşma (ENC_*) tepkileri ve meşgulken konuşma (TALK_BUSY_COMBAT)
        d6k = sivillerin grup sohbeti ve gündelik halleri: GOSSIP_VISITOR(S), LOCAL_MEMORY, FOOD_MEMORY, BANTER_*, TENSE_SILENCE, NPC_ASKS_*, STATUS_OK, PATROL_*, MEMBER_*, ANNOUNCE_ENTRY, MORALE_HIGH
        d6l = sivillerin kalan sözleri: ALLY_FOUND, AREA_CLEAR, BODY_LOOT_*, CAREFUL_*, DOOR_*, REST_*, WARMING, SEEK_WARMTH, SHOUT_HEARD_*, TALK_GREET_OPEN/FALLBACK_END/IGNORE_HOSTILE, WARNING_*, vb.
        d6m = yer tutuculu sivil barks (bkz. d6m işlevi; anahtar çıplak şablonun hash'i)
        d7a = kolluk (law + swat) selamlaşma ve geçiş sözleri: GREET_PLAYER, PASSING_PLAYER, PASSING_NPC_GREET
        d6n = rakamlı olay adı yüzünden atlanan sivil sözler: TALK_FALLBACK_1..3, ROBBERY_HANDS_UP_1..3
        d7b = kolluk (law + swat) panik sözleri: PANIC, PANIC_DAY_*
        d7c = kolluğun kalan barks'ı · d8a = asker barks · d9a = haydut+çete karışık · d9b = haydut · d9c = çete · d10a = geç savaş fraksiyonları (harici_paket.py ile)
        d11a = oyuncu EVET dedi (yes_*) · d11b = oyuncu HAYIR dedi (no_*) · d11c = replies, ASK_*, misc ve door dışı konular
        d11d = replies_misc (ziyaretçi sistemi VISIT_*/GUEST_* hariç) · d12 = replies_ask, en sık 40 konu (K39) (harici_paket.py ile; bütün roller)
        d14 = replies_ask, kalan 56 konu (K45): yer tutucusuz + yalnız cinsiyet yer tutuculu satırlar
Çıktı: kaynak/RadioData_lua.json (anahtar → EN; var olanlara eklenir),
       kaynak/RadioData_lua_baglam.json (anahtar → [dosya, olay, koşul])

Anahtar modun kendi anahtarı: "RD_ALifeLine_" + Text.hash(en) (ALifeText.lua, Text.lineKey).
Çeviriler TR RadioData.json'a gider (vanilla RD_ anahtarları da oradan okunur).
Mod bu anahtarlara kendisi bakmıyor; çeviri modundaki konuşma eki (ALifeTR_Konusma.lua) bakar (K28).
Yer tutuculu satırlar ({name}, {he}…) şimdilik alınmaz: metin doldurulduktan sonra hash tutmaz.
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
from lua_cikar import h  # noqa: E402

D = Path(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3803984183/mods/ProjectALifeNPCs/42.20/media/lua/shared/ProjectALife/Talk/Data")
STR = r'"((?:[^"\\]|\\.)*)"'
# Yalnızca ilk tablo (replikler); arkasından gelen etiket tablosu ({[1]="melee",...}) replik değil.
# Olay adında rakam olabilir (TALK_FALLBACK_1, ROBBERY_HANDS_UP_2): [A-Z_]+ bunları atlıyordu (2026-10-27).
SATIR = re.compile(r'\{"([A-Z0-9_]+)","([^"]*)",\{((?:\s*' + STR + r'\s*,?)*)\}', re.S)


def un(s):
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")


def oku(desen):
    for f in sorted(D.glob(desen)):
        for m in SATIR.finditer(f.read_text(encoding="utf-8")):
            yield f.name, m.group(1), m.group(2), [un(s) for s in re.findall(STR, m.group(3))]


def goster(s):
    """Speech.render ekrana basmadan önce ilk harfi büyütür; anahtar ekrandaki metnin hash'i olmalı."""
    m = re.search(r"[A-Za-z]", s)
    return s if m is None else s[:m.start()] + s[m.start()].upper() + s[m.start() + 1:]


SIVIL = {"civilian", "family", "worker", "rescue"}


def sivil(kosul):
    """Koşulsuz satırlar ile sivil/aile/işçi/kurtarma kayıtlarına (ya da bu rollere) açık olanlar."""
    reg = re.search(r"reg=([^|]*)", kosul)
    if reg:
        return bool(SIVIL & set(reg.group(1).split(",")))
    rol = re.search(r"role=([^|]*)", kosul)
    if rol:
        return any(r.split("_")[0] in SIVIL for r in rol.group(1).split(","))
    return True


def d0():
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_replies_npc_*.lua"):
        if olay != "NPC_OPEN":
            continue
        reg = re.search(r"reg=([^|]*)", kosul)
        if reg and "civilian" not in reg.group(1).split(","):
            continue
        for s in satirlar:
            if "{" in s or s == olay:  # yer tutuculu ya da olay adının kendisi
                continue
            yield goster(s), [ad, olay, kosul]


def d1():
    """Sivillerin oyuncuyu selamlaması (GREET_PLAYER) + konuşmada evet/hayır cevapları (NPC_OPEN sorusu, genel)."""
    kaynaklar = (("ALifeDialogue_barks_greet_*.lua", ("GREET_PLAYER",)),
                 ("ALifeDialogue_yes_misc_*.lua", ("NPC_OPEN", "GENERIC")),
                 ("ALifeDialogue_no_misc_*.lua", ("NPC_OPEN", "GENERIC")))
    for desen, olaylar in kaynaklar:
        for ad, olay, kosul, satirlar in oku(desen):
            if olay not in olaylar or not sivil(kosul):
                continue
            for s in satirlar:
                if "{" not in s:
                    yield goster(s), [ad, olay, kosul]


def d2():
    """Sivillerin yoldan geçerken oyuncuya laf atması (PASSING_PLAYER) + kısa tepkiler:
    şarjör, mermi bitti, zombi yakında, oyuncu vurdu (ilk ve tekrar)."""
    kaynaklar = (("ALifeDialogue_barks_passing_*.lua", ("PASSING_PLAYER",)),
                 ("ALifeDialogue_barks_reload_*.lua", ("RELOAD",)),
                 ("ALifeDialogue_barks_misc_*.lua", ("OUT_OF_AMMO",)),
                 ("ALifeDialogue_barks_zombie_*.lua", ("ZOMBIE_CLOSE",)),
                 ("ALifeDialogue_barks_hit_*.lua", ("HIT_BY_PLAYER", "HIT_BY_PLAYER_AGAIN")))
    for desen, olaylar in kaynaklar:
        for ad, olay, kosul, satirlar in oku(desen):
            if olay not in olaylar or not sivil(kosul):
                continue
            for s in satirlar:
                if "{" not in s:
                    yield goster(s), [ad, olay, kosul]


def d3():
    """Sivillerin panik replikleri: genel panik (PANIC) + salgının ilk günlerinde
    zombi, saklanma, silah sesi ve grup halinde panik (PANIC_DAY_*)."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_panic_*.lua"):
        if not olay.startswith("PANIC") or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D4 = ("CONTACT_INFECTED", "HOME_MEMORY", "PLEAD", "INJURED_DOWN", "SAFE_MOMENT", "MATE_HIT_BY_PLAYER")


def d4():
    """Sivillerin küçük replik grupları: enfekte biriyle temas, ev/eski hayat anısı, yalvarma,
    yaralanıp yere düşme, güvende bir an, oyuncunun arkadaşına vurması."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D4 or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


def d6a():
    """Sivillerin yoldan geçen başka bir NPC'yi selamlaması (PASSING_NPC_GREET)."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_passing_*.lua"):
        if olay != "PASSING_NPC_GREET" or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6B = ("HORDE_SPOTTED", "HORDE_INCOMING", "CRAWLER_SPOTTED")


def d6b():
    """Sivillerin tehlike sezmesi: duyulan sesler (HEARD_*), zombi sürüsü, sürünen zombi."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not (olay.startswith("HEARD_") or olay in D6B) or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6C = ("CORPSE_FOUND", "LOOT_EMPTY", "CONTAINER_SEARCH")


def d6c():
    """Sivillerin etrafta bulduklarına tepkisi: FOUND_* (ceset, kan, iz, mermi, silah, ilaç, yiyecek, su),
    CORPSE_FOUND, boş çıkan yağma ve konteyner arama."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not (olay.startswith("FOUND_") or olay in D6C) or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6D = ("AFTER_FIGHT", "CONTACT_HOSTILE", "AIMED_AT", "ALLY_DOWN", "ALLY_HIT", "COMBAT_END", "COMBAT_ATTACK")


def d6d():
    """Sivillerin çatışma tepkileri: çatışma sonrası, düşmanla temas, silah doğrultulması,
    dostun düşmesi/vurulması, çatışmanın bitişi ve saldırı anı."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D6D or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6E = ("COLD", "HOT", "SHIVER", "WET", "SNOW_FALLING", "SNOW_GROUND", "DAWN", "NIGHTFALL")


def d6e():
    """Sivillerin hava, mevsim ve gün saati sözleri: soğuk, sıcak, titreme, ıslanma, yağmur/fırtına/sis (WEATHER_*),
    kar, mevsimler (SEASON_*), şafak ve akşam."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not (olay in D6E or olay.startswith(("WEATHER_", "SEASON_"))) or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6F = ("JOKE", "CAMP_CHATTER", "IDLE", "LONG_WALK", "STARE_PLAYER", "LOCATION_COMMENT", "CHECK_IN", "HELPED_BY_PLAYER")


def d6f():
    """Sivillerin sohbet ve oyalanma sözleri: şaka, kamp lafı, boş duruş, uzun yürüyüş, oyuncuya bakma,
    bulunulan yer hakkında yorum, hal hatır sorma ve oyuncunun yardımına teşekkür."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D6F or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6G = ("INJURED_BEG", "WOUNDED_HELP", "INJURED_RESCUED", "INJURED_UP", "INJURED_DEATH", "INJURED", "HURT", "MEDIC_HELP",
       "SICK_COMPLAINT", "SICK_RECOVERED", "COUGH", "SNEEZE", "DAILY_NEEDS", "HUNGRY", "THIRSTY", "TIRED", "EXHAUSTED", "NEED_MEDICINE")


def d6g():
    """Sivillerin yaralanma, hastalık ve ihtiyaç sözleri: yardım isteme, kurtarılma, yaralı ölümü, acı, öksürük/hapşırık,
    hastalık, açlık/susuzluk/yorgunluk ve erzak isteme/verme/yok deme (SUPPLY_*)."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not (olay in D6G or olay.startswith("SUPPLY_")) or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6H = ("GUN_FEAR", "WEAPON_JAM", "LOW_AMMO", "REGROUP", "RETREAT", "COVER_ME", "SURRENDER", "MORALE_LOW", "SUPPORT_CALL",
       "FLANK_START", "HOLD_POSITION", "MOVE_OUT", "LEADER_DOWN", "NEAR_MISS", "CLOSE_CONTACT", "DISTANT_CONTACT",
       "MULTIPLE_CONTACTS", "BITE_AVOIDED")


def d6h():
    """Sivillerin çatışma çağrıları ve silah sorunları: silahtan korkma, silah tutukluğu, mermi azlığı, toparlanma,
    geri çekilme, siper isteme, teslim olma, moral, destek çağrısı, kuşatma, mevzi, lider düşmesi, ramak kala, temas."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D6H or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


def d6i():
    """Sivillerin oyuncunun ekibine katılma, ayrılma, görev ve uyarı sözleri: PARTY_*."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not olay.startswith("PARTY_") or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


def d6j():
    """Sivillerin oyuncunun emirlerine (ORD_*), soygun ve yoklamaya (ROBBERY_*), yol karşılaşmalarına (ENC_*)
    tepkileri; çatışmadayken konuşulmaya cevap (TALK_BUSY_COMBAT)."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not (olay == "TALK_BUSY_COMBAT" or olay.startswith(("ORD_", "ROBBERY_", "ENC_"))) or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6K = ("GOSSIP_VISITOR", "GOSSIP_VISITORS", "LOCAL_MEMORY", "FOOD_MEMORY", "BANTER_INTRO", "BANTER_REACTION", "TENSE_SILENCE",
       "NPC_ASKS_COPING", "NPC_ASKS_DESTINATION", "NPC_ASKS_ROAD", "STATUS_OK", "PATROL_CHECKPOINT", "PATROL_START",
       "MEMBER_MISSING", "MEMBER_ACK", "ANNOUNCE_ENTRY", "MORALE_HIGH")


def d6k():
    """Sivillerin grup içi ve gündelik sözleri: ziyaretçiye gıybet/laf (GOSSIP_VISITOR*), yerel anı, yemek özlemi, laf atma,
    gergin sessizlik, oyuncuya hal/yol/gidiş sorma (NPC_ASKS_*), durum bildirme, devriye, ekip üyesi, ilk giriş duyurusu, moral."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D6K or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


D6L = ("SHOUT_HEARD_FRIENDLY", "TALK_GREET_OPEN", "TALK_FALLBACK_END", "REST_START",
       "RETURN_WITH_LOOT", "WARMING", "SHOUT_HEARD_NEUTRAL", "REST_END",
       "INVENTORY_FULL", "AREA_CLEAR", "SEARCH_COMPLETE", "SEEK_WARMTH",
       "BODY_LOOT_NOTHING", "CAREFUL_LAST_WARNING", "ALLY_FOUND", "CAREFUL_KEEP_BACK",
       "SHOUT_HEARD_CAREFUL", "FRIENDLY_FIRE", "LOST_TARGET", "ROOM_CLEAR",
       "SQUAD_REST_CALLED", "WARMED_UP", "BODY_LOOT_FOUND", "DRESS_WARM",
       "SQUAD_REST_READY", "BODY_LOOT_AMMO", "BODY_LOOT_FOOD", "BODY_LOOT_MEDS",
       "BODY_LOOT_WEAPON", "DOOR_LOCKED", "DOOR_OPENING", "ORDER_ACK",
       "DOOR_KNOCK", "WARN_BEFORE_ATTACK", "TALK_IGNORE_HOSTILE", "KILL_CONFIRMED",
       "LEADER_ORDER", "UNDER_FIRE", "WARNING_LOWER_WEAPON", "WARNING_STOP",
       "FLANK_COMPLETE", "RAID_START", "SPOT_STRANGER", "STEADY",
       "BUILDING_SECURED", "HIT_CONFIRMED", "GRABBED", "HOUSE_INFESTED",
       "INFECTED_DOWN", "KNOCKED_DOWN", "SCAVENGE_START", "SUPPRESSED",
       "SUPPRESS_FIRE", "TAKING_COVER", "CONTACT_PLAYER", "AREA_OVERRUN",
       "EAT_START", "ENTER_BUILDING", "FALL_BACK", "GETTING_UP",
       "MELEE_ENGAGE", "SEARCH_START", "VAULT_FAILED", "WEAPON_SWITCH",
       "WINDOW_BREAK", "ASK_AMMO", "ASK_MEDICAL", "DRINK_END",
       "DRINK_START", "EAT_END", "EXIT_BUILDING", "GATE_OPENING",
       "GATE_STUCK", "GIVE_AMMO", "LEAVING_COVER", "NEED_SMOKE",
       "SEARCH_SPLIT", "SMOKE_END", "SMOKE_START", "SPREAD_OUT",
       "VAULT_START", "WINDOW_ENTRY")


def d6l():
    """Sivillerin kalan yer tutucusuz sözleri: dost bulma, bölge/oda temizliği, ceset arama, kapı, uyarı, dinlenme, ısınma,
    bağırış duyma (SHOUT_HEARD_*), konuşma açılış/kapanışı (TALK_*), savaş içi kısa nidalar."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D6L or not sivil(kosul):
            continue
        for s in satirlar:
            if "{" not in s:
                yield goster(s), [ad, olay, kosul]


def d6m():
    """Sivillerin yer tutuculu barks'ı ({den}, {town}, {name}, {g:..|..}, {he}, {sir}…). Anahtar çıplak şablonun hash'i
    (Text.speech: line.k ya da Text.lineKey(şablon)); büyük harf yapılmaz, çünkü şablon Speech.render'dan önce aranır."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not sivil(kosul):
            continue
        for s in satirlar:
            if "{" in s and s != olay:
                yield s, [ad, olay, kosul]


KOLLUK = {"law", "swat"}
D7A = ("GREET_PLAYER", "PASSING_PLAYER", "PASSING_NPC_GREET")


def kolluk(kosul):
    """Yalnızca law/swat kayıtlarına (ya da bu rollere) açık koşullar."""
    reg = re.search(r"reg=([^|]*)", kosul)
    rol = re.search(r"role=([^|]*)", kosul)
    if reg:
        return set(reg.group(1).split(",")) <= KOLLUK
    if rol:
        return {r.split("_")[0] for r in rol.group(1).split(",")} <= KOLLUK
    return False


def d7a():
    """Kolluğun (law + swat) oyuncuyu selamlaması, yoldan geçerken laf atması ve başka bir NPC'yi selamlaması."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if olay not in D7A or sivil(kosul) or not kolluk(kosul):
            continue
        for s in satirlar:
            if "{" not in s and s != olay:
                yield goster(s), [ad, olay, kosul]


def d6n():
    """Rakamlı olay adları yüzünden atlanan sivil sözler: konuşmada anlamama (TALK_FALLBACK_1..3) ve
    acemi sivilin soygunda "eller yukarı" uyarıları (ROBBERY_HANDS_UP_1..3). Geç savaş fraksiyonları (faction=) hariç."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not re.search(r"_\d+$", olay) or not sivil(kosul) or "faction=" in kosul:
            continue
        for s in satirlar:
            if "{" not in s and s != olay:
                yield goster(s), [ad, olay, kosul]


def d7b():
    """Kolluğun (law + swat) salgının ilk günlerindeki panik sözleri: PANIC, PANIC_DAY_*."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_barks_*.lua"):
        if not olay.startswith("PANIC") or sivil(kosul) or not kolluk(kosul):
            continue
        for s in satirlar:
            if "{" not in s and s != olay:
                yield goster(s), [ad, olay, kosul]


BLOK_REG = {"law": "kolluk", "swat": "kolluk", "military": "asker", "elite": "asker", "raider": "haydut",
            "outlaw": "haydut", "prison": "haydut", "gang": "cete", "club": "cete", "crime": "cete"}
BLOK_ROL = {"law": "kolluk", "swat": "kolluk", "soldier": "asker", "militia": "asker", "elite": "asker",
            "deserter": "asker", "mercenary": "asker", "raider": "haydut", "outlaw": "haydut", "prisoner": "haydut",
            "gang": "cete", "biker": "cete", "crime": "cete"}


def blok(kosul):
    """Sivil olmayan bir koşulun fraksiyon blokları: {"kolluk", "asker", "haydut", "cete"} alt kümesi, ya da {"gec_savas"}."""
    reg, rol = re.search(r"reg=([^|]*)", kosul), re.search(r"role=([^|]*)", kosul)
    if reg:
        return {BLOK_REG.get(x, "?") for x in reg.group(1).split(",")}
    if rol:
        return {BLOK_ROL.get(x.split("_")[0], "?") for x in rol.group(1).split(",")}
    return {"gec_savas"} if "faction=" in kosul else set()


def fraksiyon_barks(uygun):
    """Yer tutucusuz, sivil olmayan barks; blok kümesi uygun(...) olanlar."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_*barks_*.lua"):
        if (sivil(kosul) and "faction=" not in kosul) or not uygun(blok(kosul), olay):
            continue
        for s in satirlar:
            if "{" not in s and s != olay:
                yield goster(s), [ad, olay, kosul]


def d7c():
    """Kolluğun (law + swat) kalan barks'ı (panik hariç): çatışma, devriye, buluntu, sohbet, emir, soygun…"""
    return fraksiyon_barks(lambda b, olay: b == {"kolluk"} and not olay.startswith("PANIC"))


def d8a():
    """Askerlerin (military, elite, milis, asker kaçağı, paralı asker) barks'ı; asker + kolluk karışık kayıtlar dahil."""
    return fraksiyon_barks(lambda b, olay: "asker" in b and b <= {"asker", "kolluk"})


def d9a():
    """Haydut + çete karışık kayıtlar (yağmacı, kanun kaçağı, firari, sokak çetesi, motorcu, organize suç birlikte)
    ve dört bloğu birden kapsayan birkaç kayıt."""
    return fraksiyon_barks(lambda b, olay: ("haydut" in b and "cete" in b) or b == {"asker", "cete", "kolluk"})


def d9b():
    """Yalnız haydutların (yağmacı, kanun kaçağı, firari mahkum) barks'ı; asker + haydut karışık kayıtlar dahil."""
    return fraksiyon_barks(lambda b, olay: "haydut" in b and "cete" not in b)


def d9c():
    """Yalnız çetelerin (sokak çetesi, motosiklet çetesi, organize suç) barks'ı."""
    return fraksiyon_barks(lambda b, olay: b == {"cete"})


def d10a():
    """Geç savaş fraksiyonlarının (faction=alife_iron_orchard / argent_isolation / blackglass) barks'ı."""
    return fraksiyon_barks(lambda b, olay: b == {"gec_savas"})


def yersiz(*desenler):
    """Dosyalardaki bütün yer tutucusuz satırlar (bütün roller)."""
    for desen in desenler:
        for ad, olay, kosul, satirlar in oku(desen):
            for s in satirlar:
                if "{" not in s and s != olay:
                    yield goster(s), [ad, olay, kosul]


def d11a():
    """NPC bir şey sordu ya da teklif etti (katıl, yardım et, takas, birlikte yürü, kollarını göster…), oyuncu EVET dedi."""
    return yersiz("ALifeDialogue_yes_*.lua")


def d11b():
    """Aynı sorulara oyuncu HAYIR dedi."""
    return yersiz("ALifeDialogue_no_*.lua")


def d11c():
    """Replies: oyuncunun seçtiği konuya NPC cevabı; ASK_* soruları ve misc hariç (selam, veda, teşekkür, takip/bekle/gel/git, katılma, teklif…).
    replies_door (DOOR_*: ziyaretçi oyuncunun kapısında) hariç: K37, ziyaretçi sistemi."""
    return (r for r in yersiz("ALifeDialogue_replies_*.lua")
            if not re.match(r"ALifeDialogue_replies_(ask|misc|door)_", r[1][0]))


def d11d():
    """Replies_misc: silahı bırak, pazarlık, rüşvet, yalvarma, teslim ol, sakin ol, flört, evet/hayır/belki, hava/mevsim soruları…
    Ziyaretçi sistemi (VISIT_*, GUEST_*) hariç: K37, ek onları Türkçeleştirmiyor."""
    return (r for r in yersiz("ALifeDialogue_replies_misc_*.lua") if not r[1][1].startswith(("VISIT_", "GUEST_")))


# K39: ASK_* konularının yalnız en sık 40'ı (2026-10-28'de çevrilmemiş satır sayısına göre); kalan 56 konu İngilizce kalır.
D12_KONULAR = (
    "ASK_ADVICE", "ASK_JOB_BEFORE", "ASK_NEWS", "ASK_FAMILY", "ASK_DANGER", "ASK_WHAT_HAPPENED", "ASK_GROUP", "ASK_MISS",
    "ASK_LOOT_SPOT", "ASK_TRADE", "ASK_MILITARY", "ASK_PLANS", "ASK_DESTINATION", "ASK_SAFE_PLACE", "ASK_SCARED", "ASK_BASE",
    "ASK_NEED", "ASK_RADIO", "ASK_OTHER_SURVIVORS", "ASK_RAIDERS", "ASK_HELP", "ASK_ALONE_NIGHT", "ASK_HOPE",
    "ASK_HOW_SURVIVED", "ASK_LEADER", "ASK_CURE", "ASK_HOW_MANY", "ASK_AMMO", "ASK_GOVERNMENT", "ASK_WEAPON", "ASK_CAUSE",
    "ASK_NAME", "ASK_FORT_KNOX", "ASK_HORDE", "ASK_OKAY", "ASK_POLICE", "ASK_FOOD", "ASK_BITTEN", "ASK_SAFE_ZONE",
    "ASK_HOMETOWN")


def d12():
    """Replies_ask: oyuncunun ASK_* sorularına NPC cevabı; yalnız D12_KONULAR (K39)."""
    return (r for r in yersiz("ALifeDialogue_replies_ask_*.lua") if r[1][1] in D12_KONULAR)


CINS_YT = re.compile(r"\{(he|him|his|hers|himself|sir|mister|g:[^{}|]*\|[^{}|]*)\}", re.I)


def d13():
    """Yalnız cinsiyet yer tutuculu ({he}, {sir}, {g:a|b}) kalan satırlar: barks, replies (ASK_* için D12_KONULAR), yes/no.
    Rastgele dolan yer tutuculular ({name}, {town}…) hariç; ziyaretçi sistemi ve kapı cevapları hariç (K37, K39).
    Anahtar çıplak şablonun hash'i (d6m gibi); oyunda iki cinsiyet varyantı sablon_varyant.py ile türetilir."""
    for desen in ("ALifeDialogue_barks_*.lua", "ALifeDialogue_replies_*.lua", "ALifeDialogue_yes_*.lua", "ALifeDialogue_no_*.lua"):
        for ad, olay, kosul, satirlar in oku(desen):
            if ad.startswith("ALifeDialogue_replies_door") or olay.startswith(("VISIT_", "GUEST_")):
                continue
            if ad.startswith("ALifeDialogue_replies_ask") and olay not in D12_KONULAR:
                continue
            for s in satirlar:
                if "{" in s and s != olay and "{" not in CINS_YT.sub("", s):
                    yield s, [ad, olay, kosul]


def d14():
    """Replies_ask: D12_KONULAR dışında kalan 56 konu (K45). Yer tutucusuz satırlar ve d13'teki gibi yalnız cinsiyet
    yer tutuculu şablonlar; rastgele dolan yer tutuculular ({name}, {town}…) hariç."""
    for r in yersiz("ALifeDialogue_replies_ask_*.lua"):
        if r[1][1] not in D12_KONULAR:
            yield r
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_replies_ask_*.lua"):
        if olay not in D12_KONULAR:
            for s in satirlar:
                if "{" in s and s != olay and "{" not in CINS_YT.sub("", s):
                    yield s, [ad, olay, kosul]


def d15():
    """Rastgele dolan yer tutuculu ({town}, {den}, {name}, {time}…) bütün kalan satırlar (K46): konuşma eki oyunda
    dolu metni şablona uydurup Türkçesini doldurur (ALifeTR_Konusma.lua SABLONLAR). Anahtar çıplak şablonun hash'i.
    Yan yana iki yer tutucu (arada yazı yok) eşlenemediği için hariç."""
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_*.lua"):
        for s in satirlar:
            if s != olay and "{" in CINS_YT.sub("", s) and not re.search(r"\}\{", s):
                yield s, [ad, olay, kosul]


DOLINES = re.compile(r'\{"([a-z_]+)","([^"]*)",\{((?:\s*' + STR + r'\s*,?)*)\}', re.S)


def d16():
    """Kapı/ziyaretçi eylem satırları (DoLines, "*{v:He} glances at your hands*", K46): konuşma penceresinde
    görünür, ek VisitorDoLines.pick/lines'ı sarar. Anahtar ham satırın hash'i; m/f hâlleri sablon_varyant türetir."""
    for f in sorted(D.glob("ALifeDoLines_lines_*.lua")):
        for m in DOLINES.finditer(f.read_text(encoding="utf-8")):
            for s in re.findall(STR, m.group(3)):
                yield un(s), [f.name, m.group(1), m.group(2)]


ZIYARETCI = Path(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3803984183/mods/ProjectALifeNPCs/common/alife_runtime/visitors")
LUA_KOK = D.parent.parent.parent.parent  # media/lua


def alife_kayitlar(desen):
    """.alife kayıtları: "tür kimlik" satırı, altında "  anahtar değer" satırları, "end" ile biter. → (tür, kimlik, [(anahtar, değer)])"""
    for f in sorted(ZIYARETCI.glob(desen)):
        tur = kimlik = None
        alanlar = []
        for satir in f.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"(\w+) (\S+)$", satir)
            if m and tur is None and not satir.startswith(" "):
                tur, kimlik, alanlar = m.group(1), m.group(2), []
            elif satir.strip() == "end" and tur is not None:
                yield tur, kimlik, alanlar
                tur = None
            elif tur is not None:
                a = re.match(r"\s+(\S+) (.*)$", satir)
                if a:
                    alanlar.append((a.group(1), a.group(2)))


def kisiler():
    """vp_1006 → {"cins", "yas", "tarif", "nereden", "is", "tip", "olgular": {id: etiket}}"""
    tipler = {k: dict(a).get("a.label", "") for _, k, a in alife_kayitlar("archetypes.alife")}
    out = {}
    for tur, k, alanlar in alife_kayitlar("people_*.alife"):
        a = dict(alanlar)
        olgular = {a[f"facts.{n}.id"]: v for f, v in alanlar for n in [f.split(".")[1]] if re.fullmatch(r"facts\.\d+\.label", f)}
        out[k] = {"cins": a.get("card.sex"), "yas": a.get("card.age"), "tarif": a.get("card.desc", ""),
                  "nereden": a.get("origin.from", ""), "is": a.get("origin.work", ""),
                  "tip": tipler.get(a.get("card.arch"), ""), "olgular": olgular}
    return out


def z1():
    """Ziyaretçi/kapı sistemi KONUŞMALARI (K46): Speech.say → caption, anahtar goster(metin)'in hash'i.
    nodes_* (t.<güven>.<n>, cb, beat), lines_* havuzları (DoLines hariç), Talk/Data replies_door + VISIT_/GUEST_
    (yer tutucusuz), ALifeDoorEncounters cevapları (soru etiketi koşul), ALifeSafehouseVisit cümleleri."""
    for tur, k, alanlar in alife_kayitlar("nodes_*.alife"):
        kapi = dict(alanlar).get("gate.rule", "")
        for alan, deger in alanlar:
            m = re.match(r"t\.(\w+)\.\d+$", alan)
            if m:
                yield goster(deger), ["nodes", k, "güven=" + m.group(1) + (" | " + kapi if kapi else "")]
            elif re.match(r"cb\.\d+$", alan):
                yield goster(deger), ["nodes", k, "geri dönüş"]
            elif re.match(r"beat\.\w+\.\d+$", alan):
                yield goster(deger.split("|", 1)[1]), ["nodes", k, "devam cümlesi"]
    for tur, k, alanlar in alife_kayitlar("lines_*.alife"):
        if tur != "pool" or dict(alanlar).get("p.kind") == "dolines":
            continue
        for alan, deger in alanlar:
            if re.match(r"t\.(\d+|\w+\.\w+\.\d+)$", alan):
                yield goster(deger), ["lines", k, ""]
    for ad, olay, kosul, satirlar in oku("ALifeDialogue_*.lua"):
        if ad.startswith("ALifeDialogue_replies_door") or olay.startswith(("VISIT_", "GUEST_")):
            for s in satirlar:
                if s != olay and "{" not in s:
                    yield goster(s), [ad, olay, kosul]
    kapi = (LUA_KOK / "shared/ProjectALife/World/ALifeDoorEncounters.lua").read_text(encoding="utf-8")
    for olay, blok in re.findall(r"\n    (\w+) = \{\n(.*?)\n    \},", kapi, re.S):
        for slot, govde in re.findall(r"(\w+) = \{ (.*?) \},?\n", blok):
            etiket = re.search(r'label = "([^"]*)"', govde)
            for s in re.findall(STR, re.sub(r'label = "[^"]*",?', "", govde)):
                yield goster(un(s)), ["ALifeDoorEncounters.lua", f"DOOR_{olay}_{slot}", "oyuncunun sorusu: " + (etiket.group(1) if etiket else "")]
    ziyaret = (LUA_KOK / "server/ProjectALife/World/ALifeSafehouseVisit.lua").read_text(encoding="utf-8")
    for s in re.findall(STR, ziyaret):
        s = un(s)
        if re.match(r"[A-Z][a-z']+[ ,.!?]", s) and len(s.split()) >= 3 and not re.search(r"[_/%\[\]{}]|\.lua", s):
            yield goster(s), ["ALifeSafehouseVisit.lua", "SAFEHOUSE_VISIT", ""]


def z2():
    """Ziyaretçi PANELİ ve kapı eylem satırları (K46): ek Panel.clean / Panel.notes / VisitorDoLines'ı sarar,
    anahtar metnin kendisinin hash'i (büyütme yok). Soru düğmeleri (questions t.N), olay seçenekleri (events ch.N.label),
    "bildiklerin" notları (people facts.N.label), kişi tarifi (card.desc), DoLines havuzu (lines p.kind dolines)."""
    for tur, k, alanlar in alife_kayitlar("questions.alife"):
        sekme = dict(alanlar).get("q.tab", "")
        for alan, deger in alanlar:
            if re.match(r"t\.\d+$", alan):
                yield deger, ["questions", k, "soru düğmesi, sekme=" + sekme]
    for tur, k, alanlar in alife_kayitlar("events.alife"):
        for alan, deger in alanlar:
            if re.match(r"ch\.\d+\.label$", alan):
                yield deger, ["events", k, "olay seçeneği"]
    for k, kisi in kisiler().items():
        if kisi["tarif"]:
            yield kisi["tarif"], ["people", k + ".desc", "kişi tarifi"]
        for olgu, etiket in kisi["olgular"].items():
            yield etiket, ["people", k + ".facts", "oyuncunun öğrendiği bilgi"]
    for tur, k, alanlar in alife_kayitlar("lines_*.alife"):
        if tur == "pool" and dict(alanlar).get("p.kind") == "dolines":
            for alan, deger in alanlar:
                if re.match(r"t\.(\d+|\w+\.\w+\.\d+)$", alan):
                    yield deger, ["lines", k, "kapı eylem satırı"]


D17_ARALIK = {  # olay -> (dosya, [(ilk satır, son satır)]); mod 1.5.0 satır numaraları (1.4.6'dan kaydırıldı, 2026-11-09),
    # rapor/atlanan_metinler.md B grubu. Mod güncellenince yeniden bul: aralık dışına kayan satır sessizce düşer.
    "GOSSIP": ("shared/ProjectALife/Audio/ALifeGossip.lua", [(1589, 1604), (1639, 1729)]),
    "PLAN": ("shared/ProjectALife/World/ALifePlanData.lua", [(480, 544)]),
    "YARALI": ("shared/ProjectALife/Behaviours/ALifeInjuryRules.lua", [(11, 11), (34, 63)]),
    "PANIK": ("server/ProjectALife/Fear/ALifeModulePanic.lua", [(34, 48)]),
    "SOZ_KONUSMA": ("server/ProjectALife/Talk/ALifeTalk.lua", [(158, 162), (254, 254), (267, 267), (605, 605), (744, 757), (1568, 1583)]),
    "SOZ_BIKKIN": ("server/ProjectALife/Talk/ALifeTalkSocial.lua", [(57, 70)]),
    "SOZ_ERZAK": ("server/ProjectALife/Talk/ALifeTalkSupplies.lua", [(75, 103)]),
    "SOZ_AD": ("shared/ProjectALife/Records/ALifeNames.lua", [(144, 148)]),
    "SOZ_EV": ("server/ProjectALife/Activities/ALifeHavens.lua", [(469, 469), (535, 547)]),
    "SOZ_ITIBAR": ("server/ProjectALife/Decisions/ALifeReputationPersonal.lua", [(1198, 1205), (1330, 1335), (1422, 1425)]),
    "SOYGUN": ("server/ProjectALife/Behaviours/ALifeModuleRobbery.lua", [(92, 104), (1644, 1653)]),
    "UYARI": ("server/ProjectALife/Behaviours/ALifeModuleCareful.lua", [(200, 203), (474, 478)]),
    "UYARI_NOKTA": ("server/ProjectALife/Behaviours/ALifeModuleStances.lua", [(596, 601)]),
    "UYARI_NAMLU": ("server/ProjectALife/Fear/ALifeThreatWatch.lua", [(188, 191)]),
    "UYARI_KARAKOL": ("server/ProjectALife/Outposts/ALifeOutpostTheft.lua", [(150, 150)]),
    "CATISMA_TELSIZ": ("server/ProjectALife/Outposts/ALifeOutpostRadio.lua", [(306, 306)]),
    "CATISMA_KAPI": ("server/ProjectALife/Behaviours/ALifeModuleBreach.lua", [(1011, 1014), (1311, 1311), (1358, 1358)]),
    "CATISMA_KESKIN": ("server/ProjectALife/Combat/ALifeSniperAwareness.lua", [(491, 491)]),
    "YEDEK": ("shared/ProjectALife/Audio/ALifeVoiceTextFallback.lua", [(7, 62)]),
}


def d17():
    """Atlanan NPC konuşmaları (K46): Talk/Data dışındaki Lua dizgeleri. {yer tutuculu} ve %s'li satırlar, oyuncu
    bildirimleri (Talk.typedNotices, Careful.heardWords, Expeditions) ve birleştirilen parçalar hariç."""
    for olay, (dosya, araliklar) in D17_ARALIK.items():
        yol = LUA_KOK / dosya
        satirlar = yol.read_text(encoding="utf-8").splitlines()
        for bas, son in araliklar:
            for satir in satirlar[bas - 1:son]:
                if satir.strip().startswith("--"):
                    continue
                for s in re.findall(STR, satir):
                    s = un(s)
                    if re.search(r"[A-Za-z]{2}", s) and " " in s.strip() or s.endswith(("!", "?", ".")):
                        if not re.search(r"[{}%_/]|^[A-Z_]+$", s):
                            yield goster(s), [yol.name, olay, ""]


GRUPLAR = {"d17": d17, "z1": z1, "z2": z2, "d16": d16, "d15": d15, "d14": d14, "d13": d13, "d0": d0, "d1": d1, "d2": d2, "d3": d3, "d4": d4, "d6a": d6a, "d6b": d6b, "d6c": d6c, "d6d": d6d, "d6e": d6e, "d6f": d6f, "d6g": d6g, "d6h": d6h, "d6i": d6i, "d6j": d6j, "d6k": d6k, "d6l": d6l, "d6m": d6m, "d7a": d7a, "d6n": d6n, "d7b": d7b, "d7c": d7c, "d8a": d8a, "d9a": d9a, "d9b": d9b, "d9c": d9c, "d10a": d10a, "d11a": d11a, "d11b": d11b, "d11c": d11c, "d11d": d11d, "d12": d12}


def main(grup):
    yol, byol = KOK / "kaynak" / "RadioData_lua.json", KOK / "kaynak" / "RadioData_lua_baglam.json"
    cikti = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
    baglam = json.loads(byol.read_text(encoding="utf-8")) if byol.exists() else {}
    yeni = 0
    for en, yer in GRUPLAR[grup]():
        k = "RD_ALifeLine_" + h(en)
        if k not in cikti:
            cikti[k] = en
            baglam[k] = yer
            yeni += 1
    yol.write_text(json.dumps(cikti, ensure_ascii=False, indent=4) + "\n", encoding="utf-8", newline="\n")
    byol.write_text(json.dumps(baglam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{grup}: {yeni} yeni satır; toplam {len(cikti)} -> kaynak/RadioData_lua.json")


if __name__ == "__main__":
    main(sys.argv[1])
