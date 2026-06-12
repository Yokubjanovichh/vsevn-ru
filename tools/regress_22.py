# -*- coding: utf-8 -*-
# 2.2: desktop regress-suite (17 nuqta) + P1/P2/P3/P5/P6 tekshiruvlari
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

css = open('css/style.css', encoding='utf-8').read()
js = open('js/script.js', encoding='utf-8').read()
html = open('index.html', encoding='utf-8').read()

desktop = css.split('@media (max-width: 799.98px)')[0]
tablet = css.split('@media (max-width: 799.98px)')[1].split('@media (max-width: 489.98px)')[0]
phone = css.split('@media (max-width: 489.98px)')[1]

ok = True
def chk(name, cond):
    global ok
    print(('PASS' if cond else 'FAIL'), name)
    if not cond: ok = False

# === desktop regress-suite (17) ===
X = ['32.3', '290.7', '511', '874', '1150.7', '1344', '1601.5']
for i, x in enumerate(X, 1):
    chk(f'{i}) .rcol-{i} left calc({x}', f'.rcol-{i} {{ left: calc({x}' in desktop)
chk('8) RESUME_COLS x', all(s in js for s in ['x: 49,', 'x: 322.8,', 'x: 540.2,', 'x: 896.2,', 'x: 1181,', 'x: 1373.5,', 'x: 1621,']))
chk('9) .resume-col absolute top 13.8', re.search(r'\.resume-col\s*\{[^}]*position:\s*absolute[^}]*top:\s*calc\(13\.8', desktop) is not None)
chk('10) .resume-cell clip-path inset(-8', re.search(r'\.resume-cell\s*\{[^}]*position:\s*absolute', desktop) is not None and 'clip-path: inset(calc(-8' in desktop)
chk('11) .resume-row h calc(89', re.search(r'\.resume-row\s*\{[^}]*height:\s*calc\(89', desktop) is not None)
chk('12) .resume-cols band 1743.5x48.8', re.search(r'\.resume-cols\s*\{[^}]*width:\s*calc\(1743\.5[^}]*height:\s*calc\(48\.8', desktop) is not None)
chk('13) .resume-filter-btn left 1724.1 top 32.3', re.search(r'\.resume-filter-btn\s*\{[^}]*left:\s*calc\(1724\.1[^}]*top:\s*calc\(32\.3', desktop) is not None)
chk('14) .resume-search 1442/31.15 271.04x49.85', re.search(r'\.resume-search\s*\{[^}]*left:\s*calc\(1442[^}]*top:\s*calc\(31\.15[^}]*width:\s*calc\(271\.04[^}]*height:\s*calc\(49\.85', desktop) is not None)
chk('15) .tab-view display:none media tashqarisida', '.tab-view { display: none; }' in desktop)
chk('16) tnav/tstats/trow faqat media ichida', all(('.tnav' not in desktop, '.tstats' not in desktop, '.trow' not in desktop)) and '.tnav' in tablet and '.tstats' in tablet)
chk('17) planshet grid calc(418 saqlangan', 'grid-template-columns: calc(418' in tablet)
chk('+) telefon qoidalari faqat 489.98 ichida', '.tnav { flex-direction: column' not in tablet and 'flex-direction: column' in phone)
# 2.1 saqlanish
chk('+) pub defolt yashirin / pub-mode qoidalari', '.pub-panel { display: none; }' in desktop and 'body.pub-mode .pub-panel { display: block; }' in desktop and 'body.pub-mode .pub-panel { display: none; }' in tablet)

# === P1: juftlik hover ===
chk('H1) .vcard-foot pointer-events none', re.search(r'\.vcard-foot \{ pointer-events: none; \}', desktop) is not None)
chk('H2) view/arrow pointer auto + cursor pointer', re.search(r'\.vcard-view,\s*\.vcard-arrow \{\s*pointer-events: auto;\s*cursor: pointer;', desktop) is not None)
chk('H3) punktir ::after 1.26/2.53 top 13.5 #161715', all(s in desktop for s in ['.vcard-view::after', 'top: calc(13.5', 'height: calc(1.26', '#161715 0 calc(1.26', 'calc(2.53']))
chk('H4) hover -> punktir opacity 1', '.vcard-foot:hover .vcard-view::after { opacity: 1; }' in desktop)
chk('H5) hover -> doira #2F3027, strelka oq', '.vcard-foot:hover .vcard-arrow svg circle { fill: #2F3027; }' in desktop and '.vcard-foot:hover .vcard-arrow svg path { stroke: #FFFFFF; }' in desktop)

# === P2: mapping va klik ===
words = re.findall(r'data-pub-word="([^"]+)"', html)
chk('M1) 5 karta data-pub-word', words == ['Сайты', 'Телеграм', 'ВКонтакте', 'Одноклассники', 'Макс'])
chk('M2) initViewCards oqimda + foot click + to\'liq almashtirish (value=word)', 'initViewCards();' in js and "foot.addEventListener('click'" in js and 'input.value = word;' in js)
chk('M3) TODO-STAGE3 marker + hash fallback', 'TODO-STAGE3' in js and "if (location.hash !== '#pub') location.hash = '#pub';" in js)

# === P3/P5: filtr birlik-testlari (data + qoida replikasi) ===
rows = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',\s*account: '([^']*)',\s*accDate: '([^']*)',\s*url: '([^']*)',\s*removed: '([^']*)',\s*source: '([^']*)' \}", js)
names = dict(re.findall(r"(ok|vk|site|tg|max): '([^']+)'", js.split('PUB_SOURCE_NAMES = {')[1].split('};')[0]))
chk('F0) PUB_SOURCE_NAMES 5 nom', names == {'ok': 'Одноклассники', 'vk': 'ВКонтакте', 'site': 'Сайты', 'tg': 'Телеграм', 'max': 'Макс'})
def flt(q):
    q = q.strip().lower()
    return sum(1 for r in rows if not q or names[r[6]].lower().startswith(q))
cases = [('', 27), ('о', 6), ('О', 6), ('в', 6), ('С', 5), ('Теле', 5), ('М', 5), ('м', 5), ('xyz', 0), ('контакте', 0), ('Одноклассники', 6), ('  т  ', 5)]
for q, exp in cases:
    got = flt(q)
    chk(f'F) «{q}» -> {exp} qator', got == exp)

# === karta-bosish almashtirish ssenariysi (mantiq replikasi) ===
val = ''
val = 'Телеграм'; n1 = flt(val)
val = 'Макс'; n2 = flt(val)       # yangi so'z eskisini TO'LIQ almashtiradi
chk('S1) Телеграм(5) -> Макс(5), almashtirish', n1 == 5 and n2 == 5 and val == 'Макс')
# ✕ tozalash: bo'sh -> 27
chk('S2) ✕ -> bo\'sh -> 27 qator + applyPubSearch chaqiriladi', flt('') == 27 and js.count('applyPubSearch();') >= 3)
chk('S3) resume mantig\'iga teginilmagan (applyResumeSearch ichida pub yo\'q)',
    'PUB' not in js.split('function applyResumeSearch()')[1].split('function ')[0])

chk('V) versiyalar 435/347', 'style.css?v=435' in html and 'script.js?v=347' in html)
print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
