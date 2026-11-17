# lua_cikar / creator_cikar 1.5.0 farkı (2026-11-09)

Araçlar 1.5.0 Lua'sına karşı yeniden çalıştırıldı. **`kaynak/` dosyalarına yazılan sonuç geri alındı** (kullanıcı onayı yok); yeni anahtarlar `rapor/cikarici_yeni_1.5.0.json`, taşıma önerisi `rapor/lua_cikar_tasima_oneri_1.5.0.json`. Onaylı veri (`onayli/*`) değişmedi.

## Özet

| Kaynak | Eski | Yeni tarama | Yeni anahtar | Üretilmeyen (eski) | Not |
|---|---:|---:|---:|---:|---|
| `IG_UI_lua` | 375 | 399 | **+24** | 109 | `lua_cikar` ekleyerek çalışır (hiç silmez), "üretilmeyen" sıfırdan taramayla hesaplandı |
| `Creator_lua` | 1.729 | 1.842 | **+160** | **47** | `creator_cikar` baştan yazar, 47 anahtar kaynaktan düşer |

`lua_cikar.py` ilk denemede `ALifeNpcOpinion.lua` içindeki 3 DOLAYLI metin bulunamadığı için (`SystemExit`) **hiçbir şey yazmadan** duruyordu; `--devam` bayrağı eklendi (bulunamayanları listeler, kalanını işler). Bulunamayanlar: "I'm not telling you anything.", "I don't know you well enough for that.", "Not yet. Ask me when I trust you more." (metinler başka dosyalarda aynen duruyor, "Lua'da değişmeden duruyor" grubunda sayıldı; yalnız `ALifeNpcOpinion.lua` DOLAYLI listesi eskimiş, eylem gerekmiyor).

## IG_UI_lua: 109 üretilmeyen eski anahtar

| Durum | Sayı | Anlamı |
|---|---:|---|
| Aynı anahtar 1.5.0 `IG_UI.json`'da | 38 | Mod artık JSON'a koymuş; onaylı çeviri aynı anahtarla geçerli, B7'de IG_UI'ye kopyalanır |
| **Noktalama/harf farkıyla yeni anahtar** | **23** | "Hands up. Slow and easy." → "Hands up, slow and easy" gibi; çeviri taşınabilir (öneri dosyasında) |
| Metin Lua'da değişmeden duruyor | 46 | `ALifeVisitorReact`, `ALifeParty`, `ALifeStandoff` vb.; eski elle eklenmiş satırlar, tarama bunları üretmiyor ama anahtar geçerli. Eylem yok |
| Kodda yok | 2 | "I'm law enforcement. Talk to me." → yeniden yazılmış ("I'm a cop, you can talk to me", yeni anahtar, **çevrilmeli**); "Take your people and clear out of this area." → "Take your people and clear out" (taşıma önerisine elle eklendi, öneride toplam 24) |

Yeni 24 anahtar: konuşma menüsü emir/grup/kış satırları (`ALifeTalkOrderRows`, `ALifePartyRows`, `ALifeTalkWinterRows`). 23'ü yukarıdaki taşımalarla eşleşir (24 öneri satırı, iki eski anahtar aynı yeni metne gidiyor); **1'i gerçekten yeni** ("I'm a cop, you can talk to me").

## Creator_lua: 47 kaybolan anahtar

| Durum | Sayı |
|---|---:|
| Aynı anahtar 1.5.0 `IG_UI.json`'da | 28 |
| **Noktalama farkıyla yeni anahtar** ("Accuracy vs players (%)" → "Accuracy vs players"; 4 satır) | 4 |
| Lua'da duruyor ama `creator_cikar` artık üretmiyor ("VAR", "Primary", "NPC save failed") | 3 |
| Kodda yok: "spring grey shirts and peaked caps", "summer olive drab tees…" (4 giysi satırı), "DEFAULT PROGRAM", "NATURAL PARTIES", "INHERITED MODULES", "Project A-Life Creator", "PROJECT A-LIFE CREATOR", "capacity by weapon", "Example: Raiders, Story factions, Test groups...", "Move to a side angle…" | 12 |

Yeni 160 anahtar: Oluşturucu ekranı (ALifeCreatorUx/Core/UxStatus/UxTabs/LookSeasons/UxSafety/FactionSupport/Dense…) ve `faction_registry.alife` içindeki 25 etiket. 156'sı gerçekten yeni, 4'ü yukarıdaki taşımalarla eşleşir. Bunlar B12b olarak planlandı (`rapor/B_paket_plani_1.5.0.md`).

## Önerilen eylemler (uygulanmadı)

1. `rapor/lua_cikar_tasima_oneri_1.5.0.json`: 28 eski anahtar → yeni anahtar (24 IG_UI_lua, 4 Creator_lua); hepsinin onaylı çevirisi var. Uygulama: `araclar/anahtar_tasi.py` desenindeki gibi kullanıcı onayıyla.
2. Onay sonrası `kaynak/IG_UI_lua.json` ve `kaynak/Creator_lua.json` yeniden üretilir (`python -X utf8 araclar/lua_cikar.py --devam` ve `creator_cikar.py`); `creator_cikar` 47 anahtarı kaynaktan düşürür, `onayli/Creator_lua.json` değişmez (silme ayrı karar).
3. Kodda olmayan 14 anahtarın (IG_UI_lua 2 + Creator 12) onaylı çevirisi teslimde kalırsa zararsız.
