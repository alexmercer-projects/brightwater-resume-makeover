#!/bin/bash
# Prints docs/resume.html to the PDF with headless Chrome, saves its plain text, then rebuilds the page.
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py >/dev/null
python3 -m http.server 8799 -d docs >/dev/null 2>&1 & srv=$!
sleep 1
google-chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=docs/Noa-Brightwater-resume-DEMO.pdf http://localhost:8799/resume.html 2>/dev/null
kill $srv
pdftotext -enc UTF-8 docs/Noa-Brightwater-resume-DEMO.pdf - | sed -e '/^\f*$/d' > docs/plain-text.txt
python3 tools/build_docx.py
python3 tools/build.py
pdfinfo docs/Noa-Brightwater-resume-DEMO.pdf | grep -E "Pages|File size"
