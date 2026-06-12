# -*- coding: utf-8 -*-
# 2.3: desktop regress-suite (17) + resume-popап daxlsizligi (1.6) + pub-popап
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

# === resume popап daxlsizligi (1.6 nazorat nuqtalari) ===
chk('R1) .acc-popup left/top 88.9 / --acc-w qoidalari', re.search(r'\.acc-popup\s*\{[^}]*left:\s*calc\(\(1771\.7 - var\(--acc-w[^}]*top:\s*calc\(88\.9', desktop) is not None)
chk('R2) POP8 CSS: filter-active kapsula 1401.5 / dots 1680.6', '.resume-head.filter-active .resume-search { left: calc(1401.5' in desktop and re.search(r'\.resume-head\.filter-active \.resume-filter-btn\s*\{[^}]*left:\s*calc\(1680\.6', desktop) is not None)
chk('R3) resume popап markup (accPopup/accList/accThumb)', all(s in html for s in ['id="accPopup"', 'id="accList"', 'id="accThumb"']))
chk('R4) ACCOUNTS 20 ta, sana-kamayish', True)  # quyida data bilan
accounts = re.findall(r"\{ num: '(Св\d+)', date: '(\d\d\.\d\d\.\d{4})' \}", js)
def dkey(d): p = d.split('.'); return int(p[2])*10000+int(p[1])*100+int(p[0])
ks = [dkey(d) for _, d in accounts]
chk('R4) ACCOUNTS 20 ta, sana-kamayish', len(accounts) == 20 and ks == sorted(ks, reverse=True))
chk('R5) applyResumeSearch mantig\'i o\'zgarmagan (searchOk && accOk + accountFilterSet)',
    'const accOk = !accountFilterSet.size || accountFilterSet.has(row.account);' in js and
    "tr.style.display = (searchOk && accOk) ? '' : 'none';" in js)
chk('R6) accountFilterSet = resumeAccPopup.filterSet (shim)', 'const accountFilterSet = resumeAccPopup.filterSet;' in js)
chk('R7) resume SEL1 tail saqlangan', "document.getElementById('accPopup');\n        if (popup && !popup.hidden) ensureAccPopupVisible(popup);" in js)
chk('R8) eski singleton globallar olib tashlangan', not re.search(r'accScrollIndex|accPopupEls|accListBuilt|accPopupBound|openAccPopup|closeAccPopup|toggleAccount\b', js))
chk('R9) resume kontroller selektorlari', "headSel: '.resume-panel:not(.pub-panel) .resume-head'" in js and "popupId: 'accPopup'" in js)

# === pub popап (2.3) ===
chk('P1) pub markup: pubAccPopup/pubAccList/pubAccThumb + filter-x pub-head ichida', all(s in html for s in ['id="pubAccPopup"', 'id="pubAccList"', 'id="pubAccThumb"']))
pub_head = html.split('class="resume-head pub-head"')[1].split('<div class="resume-cols"')[0]
chk('P2) pub-head ichida filter-x + tooltip + popап', 'resume-filter-x' in pub_head and 'Деактивировать фильтрацию по выбранным счетам' in pub_head and 'pubAccPopup' in pub_head)
chk('P3) pub kontroller cfg', "headSel: '.pub-head'" in js and "popupId: 'pubAccPopup'" in js and 'apply: function () { applyPubSearch(); }' in js)
chk('P4) applyPubSearch: sourceOk && accOk (pub set)', 'const accOk = !pubAccPopup.filterSet.size || pubAccPopup.filterSet.has(row.account);' in js and "tr.style.display = (sourceOk && accOk) ? '' : 'none';" in js)
chk('P5) pub SEL1 tail', "document.getElementById('pubAccPopup');\n        if (popup && !popup.hidden) ensureAccPopupVisible(popup);" in js)
chk('P6) mutual-exclusion open()da', 'accPopupControllers.forEach(function (c) { if (c !== ctl) c.close(); });' in js)
chk('P7) filter-X faqat O\'Z ro\'yxatini tozalaydi', "cur.list.querySelectorAll('.acc-row.is-checked')" in js)
chk('P8) buildAccList parametrlangan (filterSet)', 'function buildAccList(list, filterSet)' in js and 'buildAccList(e.list, ctl.filterSet);' in js)
chk('P9) addAccountEntry ikkala ro\'yxatni eskirtadi', 'accPopupControllers.forEach(function (c) { c.markListStale(); });' in js)

# === filtr birlik-testlari (data + qoida replikasi) ===
rows = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',\s*account: '([^']*)',\s*accDate: '([^']*)',\s*url: '([^']*)',\s*removed: '([^']*)',\s*source: '([^']*)' \}", js)
names = dict(re.findall(r"(ok|vk|site|tg|max): '([^']+)'", js.split('PUB_SOURCE_NAMES = {')[1].split('};')[0]))
def pub_visible(q, accset):
    q = q.strip().lower()
    n = 0
    for r in rows:
        sourceOk = not q or names[r[6]].lower().startswith(q)
        accOk = not accset or r[2] in accset
        if sourceOk and accOk: n += 1
    return n
chk('T1) {Св…1829} -> 2 qator', pub_visible('', {'Св000000001829'}) == 2)
chk('T2) {Св…1944} -> 2 qator', pub_visible('', {'Св000000001944'}) == 2)
chk('T3) bitta-qatorli {Св…1811} -> 1', pub_visible('', {'Св000000001811'}) == 1)
chk('T4) «О» + {Св…1829} -> 1 (faqat ok-qator)', pub_visible('О', {'Св000000001829'}) == 1)
chk('T5) OR: {1829,1846} -> 4', pub_visible('', {'Св000000001829', 'Св000000001846'}) == 4)
chk('T6) filtr-✕ reset: «О» + bo\'sh set -> 6', pub_visible('О', set()) == 6)
chk('T7) hech mos kelmas kombinatsiya -> 0', pub_visible('Макс', {'Св000000001923'}) == 0)
# mustaqillik: resume to'plami pub natijasiga ta'sir qilmaydi (replika)
res_rows = re.findall(r"\{ name: '[^']*',\s*phone: '[^']*',\s*vacancy: '[^']*',\s*email: '[^']*',\s+replyDate: '[^']*',\s*account: '([^']*)',\s*accountDate: '[^']*' \}", js)
def resume_visible(accset):
    return sum(1 for a in res_rows if not accset or a in accset)
rset = {'Св000000001829'}; pset = {'Св000000001944'}
chk('T8) mustaqillik: resume{1829}=2 & pub{1944}=2, kesishmaydi',
    resume_visible(rset) == 2 and pub_visible('', pset) == 2 and len(res_rows) == 20)
# computePopupReveal ssenariylari (1.6 dagi 3 holat)
m = re.search(r'function computePopupReveal\(popupBottomDoc, cardBottomDoc, viewportH, scrollY\) \{[\s\S]*?\n    \}', js)
chk('T9) computePopupReveal imzosi saqlangan', m is not None)
def reveal(pb, cb, vh, sy):
    margin = 12; need = pb + margin
    return (max(0, need - cb), max(0, (need - vh) - sy))
chk('T10) reveal: sig\'adi -> 0/0', reveal(900, 1500, 1080, 0) == (0, 0))
chk('T11) reveal: karta past, dorisovka', reveal(1600, 1450, 1080, 0) == (162, 532))
chk('T12) reveal: skroll yetarli bo\'lsa faqat spacer', reveal(1600, 1450, 1080, 600) == (162, 0))

chk('V) versiyalar 435/348', 'style.css?v=435' in html and 'script.js?v=348' in html)
print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
