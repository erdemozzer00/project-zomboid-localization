"""Lua kaynağındaki dize sabitlerini (konum, metin) olarak verir; yorumları ve '...' dizelerini doğru atlar."""
import re


def dizeler(s):
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if s.startswith("--", i):
            m = re.match(r"--\[(=*)\[", s[i:])
            if m:
                j = s.find("]" + m.group(1) + "]", i)
                i = n if j < 0 else j + len(m.group(1)) + 2
            else:
                j = s.find("\n", i)
                i = n if j < 0 else j + 1
            continue
        m = re.match(r"\[(=*)\[", s[i:i + 20]) if c == "[" else None
        if m:
            j = s.find("]" + m.group(1) + "]", i)
            yield i, s[i + len(m.group(0)):j]
            i = n if j < 0 else j + len(m.group(1)) + 2
            continue
        if c in "\"'":
            j, buf = i + 1, []
            while j < n and s[j] != c and s[j] != "\n":
                if s[j] == "\\" and j + 1 < n:
                    e = s[j + 1]
                    buf.append({"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'"}.get(e, "\\" + e))
                    j += 2
                    continue
                buf.append(s[j])
                j += 1
            yield i, "".join(buf)
            i = j + 1
            continue
        i += 1
