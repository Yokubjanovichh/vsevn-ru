# -*- coding: utf-8 -*-
# 2.1: desktop regress-suite (17 nuqta) + pub-jadval tekshiruvlari
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

# === 2.1 pub-panel tekshiruvlari ===
chk('P1) .pub-panel display:none defolt (desktop qism)', '.pub-panel { display: none; }' in desktop)
chk('P2) pub-mode almashinuv qoidalari', 'body.pub-mode .resume-panel:not(.pub-panel) { display: none; }' in desktop and 'body.pub-mode .pub-panel { display: block; }' in desktop)
chk('P3) planshetda pub-panel pub-mode bilan ham yashirin', 'body.pub-mode .pub-panel { display: none; }' in tablet)
PX = ['18.8', '559.2', '759.6', '1005.8', '1203.4', '1543.5']
for i, x in enumerate(PX, 1):
    chk(f'P4.{i}) .pcol-{i} left calc({x}', f'.pcol-{i} {{ left: calc({x}' in desktop)
chk('P5) .pub-title left 27.2', '.pub-title { left: calc(27.2' in desktop)
chk('P6) PUB_COLS x/size/base', all(s in js for s in [
    "x: 46.8,   size: 23,    base: 50.5", "x: 589.4,  size: 20,    base: 49.6",
    "x: 789.1,  size: 18.82, base: 49.6", "x: 1034.3, size: 20,    base: 49.6",
    "x: 1234.4, size: 20,    base: 49.6", "x: 1581.1, size: 20,    base: 49.6"]))
chk('P7) markup: pub-panel resume-panel klassi bilan', 'class="resume-panel pub-panel"' in html)
chk('P8) markup: pubRows + 6 ustun-header', 'id="pubRows"' in html and all(f'pcol-{i}' in html for i in range(1, 7)))
chk('P9) header matnlari', all(t in html for t in ['ВАКАНСИЯ', 'ДАТА РАЗМЕЩ.', 'СЧЁТ', 'ДАТА СЧЁТА', 'ССЫЛКА НА ОБЪЯВЛЕНИЕ', 'ДАТА УДАЛЕНИЯ']))
chk('P10) renderStaticText oqimida initPub*', all(s in js for s in ['initPubTable();', 'initPubSearch();', 'initPubToggle();']))
chk('P11) dev-toggle hash #pub', "location.hash === '#pub'" in js)
chk('P12) versiyalar 434/346', 'style.css?v=434' in html and 'script.js?v=346' in html)

# === PUB_ROWS data-tekshiruvlari (JS massivni parslash) ===
rows = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',\s*account: '([^']*)',\s*accDate: '([^']*)',\s*url: '([^']*)',\s*removed: '([^']*)',\s*source: '([^']*)' \}", js)
chk('D1) 27 qator', len(rows) == 27)
from collections import Counter
src = Counter(r[6] for r in rows)
chk('D2) source taqsimoti ok6/vk6/site5/tg5/max5', src == Counter({'ok': 6, 'vk': 6, 'site': 5, 'tg': 5, 'max': 5}))
acc = Counter(r[2] for r in rows)
pairs = [a for a, c in acc.items() if c == 2]
chk('D3) 7 hisob 2 tadan, qolgani 1 tadan (jami 20 hisob)', len(pairs) == 7 and all(c <= 2 for c in acc.values()) and len(acc) == 20)
# hisoblar ACCOUNTS ro'yxatidan va accDate o'sha hisob sanasiga mos (DD.MM.YYYY <-> to'liq oy)
accounts_js = dict(re.findall(r"\{ num: '(Св\d+)', date: '([^']+)' \}", js))
MON = {1:'Января',2:'Февраля',3:'Марта',4:'Апреля',5:'Мая',6:'Июня',7:'Июля',8:'Августа',9:'Сентября',10:'Октября',11:'Ноября',12:'Декабря'}
def full(d):
    dd, mm, yy = d.split('.')
    return f'{int(dd)} {MON[int(mm)]} {yy}'
bad = [r[2] for r in rows if r[2] not in accounts_js or full(accounts_js[r[2]]) != r[3]]
chk('D4) account ∈ ACCOUNTS va accDate mos', not bad)
chk('D5) URL barchasi unikal', len(set(r[4] for r in rows)) == 27)
chk('D6) vakansiyalar ~10 xil', len(set(r[0] for r in rows)) == 10)
# placed kamayish tartibi
SHORT = {'Янв':1,'Фев':2,'Мар':3,'Апр':4,'Мая':5,'Июн':6,'Июл':7,'Авг':8,'Сен':9,'Окт':10,'Нояб':11,'Дек':12}
def key(d):
    p = d.split()
    return (int(p[2]), SHORT[p[1]], int(p[0]))
ks = [key(r[1]) for r in rows]
chk('D7) ДАТА РАЗМЕЩ. kamayish tartibida', ks == sorted(ks, reverse=True))
chk('D8) etalon qatori (t.me/Rabota_vod/273, Св...1829, 11 Нояб 2024)',
    any(r[1] == '11 Нояб 2024' and r[2] == 'Св000000001829' and r[4] == 'https://t.me/Rabota_vod/273' for r in rows))
# URL manba-mosligi
dom = {'ok': 'ok.ru', 'vk': 'vk.com', 'tg': 't.me', 'max': 'max.ru'}
mis = [r[4] for r in rows if r[6] in dom and dom[r[6]] not in r[4]]
mis += [r[4] for r in rows if r[6] == 'site' and any(d in r[4] for d in dom.values())]
chk('D9) URL manbaga mos', not mis)

print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
