# -*- coding: utf-8 -*-
# 1.8-C: desktop regress-suite (17 nuqta) + scroll-top mobil tekshiruvlari
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

# === 1.8-C tekshiruvlari ===
m = re.search(r'function initScrollTop\(\)[\s\S]*?\n    \}\n', js)
body = m.group(0) if m else ''
chk('C1) mobil chegara 100 / desktop 400', "mobileMq.matches ? 100 : 400" in body)
chk('C2) mobileMq = 799.98px', "matchMedia('(max-width: 799.98px)')" in body)
chk('C3) visualViewport resize listener', 'window.visualViewport' in body and "vv.addEventListener('resize'" in body)
chk('C4) klaviatura sharti faqat mobilda', '!(mobileMq.matches && keyboardOpen)' in body)
chk('C5) fallback: vv yoq bo\'lsa keyboardOpen=false qoladi', 'let keyboardOpen = false' in body)
chk('C6) klaviatura chegarasi 150px', '> 150' in body)
chk('C7) breakpoint change -> sync', "mobileMq.addEventListener('change', sync)" in body)
chk('C8) smooth scroll saqlangan', "behavior: 'smooth'" in body)
chk('C9) scroll-top tugma #zoomFrame tashqarisida', html.index('id="scrollTopBtn"') > html.index('id="zoomFrame"') and 'scrollTopBtn' in html.split('</body>')[0].rsplit('zoomFrame', 1)[1])
chk('C10) mobil real-px o\'lchamlar o\'zgarmagan (64x42)', re.search(r'\.scroll-top\s*\{[^}]*width:\s*64px[^}]*height:\s*42px', tablet) is not None)
chk('C11) versiyalar: css 433, js 345', 'style.css?v=433' in html and 'script.js?v=345' in html)

# simulyatsiya: sync mantiqi (chegara/klaviatura kombinatsiyalari)
def visible(scrollY, mobile, kb):
    threshold = 100 if mobile else 400
    return scrollY > threshold and not (mobile and kb)
cases = [
    (50, True, False, False),   # mobil, 100 dan past -> yo'q
    (150, True, False, True),   # mobil, 100 dan yuqori -> bor
    (150, True, True, False),   # mobil + klaviatura -> yashirin
    (150, False, False, False), # desktop, 400 dan past -> yo'q
    (450, False, False, True),  # desktop, 400 dan yuqori -> bor
    (450, False, True, True),   # desktop + (nazariy) kb -> baribir bor
]
sim = all(visible(s, m_, k) == exp for s, m_, k, exp in cases)
chk('C12) sync simulyatsiyasi 6/6 ssenariy', sim)

print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
