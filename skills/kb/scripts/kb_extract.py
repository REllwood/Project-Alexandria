#!/usr/bin/env python3
"""kb_extract.py - extract plain text from Office/text files using only the
standard library (+ macOS `textutil` for .docx). For PDFs, use the Read tool.

Usage: kb_extract.py <file> [--max-chars N]
Prints extracted text to stdout.
"""
import argparse, os, re, shutil, subprocess, sys, zipfile
from xml.sax.saxutils import unescape


def _unescape(s):
    return unescape(s, {"&#10;": "\n", "&#13;": "\n"})


def docx(path):
    # Prefer a real converter when available (textutil on macOS, pandoc anywhere);
    # fall back to a cross-platform stdlib paragraph extractor so it works everywhere.
    for cmd in (["textutil", "-convert", "txt", "-stdout", path],
                ["pandoc", path, "-t", "plain", "--wrap=none"]):
        if shutil.which(cmd[0]):
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if out.returncode == 0 and out.stdout.strip():
                    return out.stdout
            except (OSError, subprocess.SubprocessError):
                pass
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
    except Exception:
        return ""
    paras = []
    for p in re.split(r"</w:p>", xml):           # one paragraph per <w:p>
        runs = re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", p, re.S)  # only the w:t text element
        line = _unescape("".join(runs)).strip()
        if line:
            paras.append(line)
    return "\n\n".join(paras)


def pptx(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        slides = sorted([n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                        key=lambda n: int(re.search(r"(\d+)", n).group(1)))
        notes = {int(re.search(r"(\d+)", n).group(1)): n for n in names
                 if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)}
        for i, s in enumerate(slides, 1):
            xml = z.read(s).decode("utf-8", "ignore")
            runs = [_unescape(t) for t in re.findall(r"<a:t>(.*?)</a:t>", xml, re.S)]
            txt = "\n".join(r for r in runs if r.strip())
            out.append(f"## Slide {i}\n{txt}")
            if i in notes:
                nxml = z.read(notes[i]).decode("utf-8", "ignore")
                nruns = [_unescape(t) for t in re.findall(r"<a:t>(.*?)</a:t>", nxml, re.S)]
                ntxt = "\n".join(r for r in nruns if r.strip())
                if ntxt.strip():
                    out.append(f"_Speaker notes:_ {ntxt}")
    return "\n\n".join(out)


def xlsx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            ss = z.read("xl/sharedStrings.xml").decode("utf-8", "ignore")
            # each <si> may have multiple <t> runs; join per <si>
            for si in re.findall(r"<si>(.*?)</si>", ss, re.S):
                shared.append(_unescape("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S))))
        sheets = sorted([n for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n)],
                        key=lambda n: int(re.search(r"(\d+)", n).group(1)))
        out = []
        for sn in sheets:
            xml = z.read(sn).decode("utf-8", "ignore")
            rows_txt = []
            for row in re.findall(r"<row[^>]*>(.*?)</row>", xml, re.S):
                cells = []
                for c in re.findall(r"<c\b([^>]*)>(.*?)</c>", row, re.S):
                    attrs, body = c
                    v = re.search(r"<v>(.*?)</v>", body, re.S)
                    if not v:
                        # inline string?
                        istr = re.search(r"<is>.*?<t[^>]*>(.*?)</t>", body, re.S)
                        cells.append(_unescape(istr.group(1)) if istr else "")
                        continue
                    val = v.group(1)
                    if 't="s"' in attrs:  # shared string index
                        try: cells.append(shared[int(val)])
                        except (ValueError, IndexError): cells.append("")
                    else:
                        cells.append(_unescape(val))
                if any(x.strip() for x in cells):
                    rows_txt.append(" | ".join(cells))
            if rows_txt:
                out.append(f"### {os.path.basename(sn)}\n" + "\n".join(rows_txt))
        return "\n\n".join(out)


def eml(path):
    import email
    from email import policy
    with open(path, "rb") as fh:
        msg = email.message_from_binary_file(fh, policy=policy.default)
    hdr = (f"From: {msg.get('from','')}\nTo: {msg.get('to','')}\n"
           f"Cc: {msg.get('cc','')}\nDate: {msg.get('date','')}\n"
           f"Subject: {msg.get('subject','')}\n\n")
    content = ""
    try:
        body = msg.get_body(preferencelist=("plain", "html"))
        if body is not None:
            content = body.get_content()
            if body.get_content_type() == "text/html":
                content = _unescape(re.sub(r"<[^>]+>", " ", content))
    except Exception:
        content = ""
    return hdr + content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--max-chars", type=int, default=120000)
    a = ap.parse_args()
    ext = os.path.splitext(a.file)[1].lower()
    if ext == ".docx":
        text = docx(a.file)
    elif ext == ".pptx":
        text = pptx(a.file)
    elif ext == ".xlsx":
        text = xlsx(a.file)
    elif ext == ".eml":
        text = eml(a.file)
    elif ext in (".txt", ".md", ".csv", ".tsv", ".rtf"):
        text = open(a.file, encoding="utf-8", errors="ignore").read()
    elif ext == ".pdf":
        text = f"[PDF: {a.file} — read it with the Read tool, which extracts PDF text directly.]"
    else:
        text = f"[Unsupported type {ext}: {a.file}]"
    text = text or "[no text extracted]"
    sys.stdout.write(text[:a.max_chars])


if __name__ == "__main__":
    main()
