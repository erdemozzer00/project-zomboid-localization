"""Talk/Data'daki sahneleri (NPC'lerin kendi arasındaki çok turlu konuşmalar) okur.

Kayıt biçimi (ALifeDialogue_scenes_*.lua, ALifeDialogue_war_late_scenes_misc*.lua):
  {"fw_ld4_arguments_a_0001","any",2,"reg=civilian,family,worker,rescue|world=road",{1,"satır",2,"satır",...}}
  kimlik, konu, konuşmacı sayısı, koşul, sıralı (konuşmacı numarası, metin) çiftleri.

Oyunda sahne satırı Speech.render (ilk harf büyür) ve Speech.say -> AudioPolicy.caption yolundan geçer; anahtar
"RD_ALifeLine_" + Text.hash(diyalog_cikar.goster(metin)) (düz satırlar için). Süslü parantezli satırlar
(rastgele dolan {town}, {street} vb.) çevrilemez; sahnede bağlam olarak gösterilir.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diyalog_cikar as d  # noqa: E402

STRP = r'"((?:[^"\\]|\\.)*)"'
KAYIT = re.compile(r'\{"([A-Za-z0-9_]+)","(\w+)",(\d+),"([^"]*)",\{((?:\d+,' + STRP + r',?)+)\}')
TUR = re.compile(r'(\d+),' + STRP)


def sahneler():
    """Her sahne: dict(dosya, id, konu, kisi, kosul, turlar=[(konusmaci, metin)])."""
    for f in sorted(d.D.glob("ALifeDialogue_*scenes*.lua")):
        for m in KAYIT.finditer(f.read_text(encoding="utf-8")):
            turlar = [(int(a), d.un(b)) for a, b in TUR.findall(m.group(5))]
            yield {"dosya": f.name, "id": m.group(1), "konu": m.group(2), "kisi": int(m.group(3)),
                   "kosul": m.group(4), "turlar": turlar}
