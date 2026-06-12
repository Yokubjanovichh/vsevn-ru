# -*- coding: utf-8 -*-
# 2.4-FIX: desktop regress (17) + tstat/tth tuzatish nazoratlari + fit-matematika
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
chk('16) tnav/tstats/trow faqat media ichida', all(('.tnav' not in desktop, '.tstats' not in desktop, '.trow-' not in desktop)) and '.tnav' in tablet and '.tstats' in tablet)
chk('17) planshet grid calc(418 saqlangan', 'grid-template-columns: calc(418' in tablet)
chk('+) telefon qoidalari faqat 489.98 ichida', '.tnav { flex-direction: column' not in tablet and 'flex-direction: column' in phone)

# === FIX-1: tstat tuzilma himoyasi va etalon qiymatlar ===
chk('F1) .tstat nowrap + font-size:0 (planshet bloki)', re.search(r'\.tstat \{[^}]*white-space: nowrap;[^}]*font-size: 0;', tablet) is not None)
chk('F2) planshet chip margin 19.8', 'margin-right: calc(19.8' in tablet)
chk('F3) telefon chip margin 74', 'margin-right: calc(74 ' in phone)
chk('F4) raqamlar renderTabRoboto 46/45', "renderTabRoboto(el, ph ? 46 : 45, '#2F3028', K)" in js)
chk('F5) renderTabRoboto Roboto-family', 'TAB_ROBOTO_FAMILY = "\'Roboto\', Arial, sans-serif"' in js and 'family: TAB_ROBOTO_FAMILY' in js)
chk('F6) tab-pub sanalari ham renderTabRoboto', js.count('renderTabRoboto(tr.querySelector') == 2 and 'renderTabDate' not in js)

# === FIX-2: tth-vac liniya ===
chk('F7) telefon .tth-vac vertical-align: top', re.search(r'\.tth-vac \{ position: static; display: inline-block; vertical-align: top;', phone) is not None)
chk('F8) planshet .tth-name/.tth-phone vertical-align saqlangan', '.tth-name, .tth-phone { display: inline-block; vertical-align: top; }' in tablet)

# === fit-matematika (Roboto 300 advance: raqam 0.5547em, % 0.7393em) ===
DIG = 0.5547; PCT = 0.7393
def box(text, size_dpx):
    import math
    adv = sum(PCT if c == '%' else DIG for c in text) * size_dpx
    return math.ceil(adv) + 2 + 4   # measureTextWidth ceil+2, svg +4
# planshet: size 45*2.2535=101.41; col4 = 1400-(418+354+372)=256
t_need = 59 + 19.8 + box('246', 45 * 2.2535)
chk('M1) planshet col4: %.0f <= 256' % t_need, t_need <= 256)
# telefon: size 46*4.962=228.25; col2 = 1612-918=694; scrollbar eng yomoni -105
p_need = 99 + 74 + box('246', 46 * 4.962)
chk('M2) telefon col2 (scrollbar bilan): %.0f <= 589' % p_need, p_need <= 589)
chk('M3) telefon col1 88%%: %.0f <= 813' % (99 + 74 + box('88%', 46 * 4.962)), 99 + 74 + box('88%', 46 * 4.962) <= 918 - 105)
# 1.8/2.4 kalit nuqtalari saqlangan
chk('K1) .ttable margin 41 saqlangan', re.search(r'\.ttable\s*\{\s*margin-top:\s*calc\(41', tablet) is not None)
chk('K2) .trow grid 588 saqlangan', 'grid-template-columns: calc(588' in tablet)
chk('K3) tab-pub qoidalari saqlangan', '.tab-pub { display: none; }' in desktop and 'body.pub-mode .tab-pub { display: block; }' in tablet)
chk('K4) tstats grid 918 saqlangan (telefon)', 'grid-template-columns: calc(918' in phone)
chk('V) versiyalar 437/350', 'style.css?v=437' in html and 'script.js?v=350' in html)
print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
