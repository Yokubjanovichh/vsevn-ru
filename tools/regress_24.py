# -*- coding: utf-8 -*-
# 2.4: desktop regress (17) + 1.8 planshet daxlsizligi + tab-pub + sana-konversiya
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
chk('16) tnav/tstats/trow faqat media ichida', all(('.tnav' not in desktop, '.tstats' not in desktop, '.trow ' not in desktop and '.trow{' not in desktop and '.trow-' not in desktop)) and '.tnav' in tablet and '.tstats' in tablet)
chk('17) planshet grid calc(418 saqlangan', 'grid-template-columns: calc(418' in tablet)
chk('+) telefon qoidalari faqat 489.98 ichida', '.tnav { flex-direction: column' not in tablet and 'flex-direction: column' in phone)

# === 1.8 planshet daxlsizligi ===
chk('18a) .ttable margin/padding saqlangan', re.search(r'\.ttable\s*\{\s*margin-top:\s*calc\(41', tablet) is not None)
chk('18b) .trow grid 588 saqlangan', 'grid-template-columns: calc(588' in tablet)
chk('18c) scroll-top real-px saqlangan', 'width: 64px' in tablet and 'height: 42px' in tablet)
chk('18d) telefon .trow block saqlangan', '.trow { display: block' in phone)

# === 2.4 tuzilma ===
chk('A1) .tab-pub display:none desktop qismida', '.tab-pub { display: none; }' in desktop)
chk('A2) pub-mode almashinuvi media ichida', 'body.pub-mode .ttable { display: none; }' in tablet and 'body.pub-mode .tab-pub { display: block; }' in tablet and 'body.pub-mode .pub-panel { display: none; }' in tablet)
chk('A3) desktopda .tab-pub korsatish qoidasi YOQ', 'body.pub-mode .tab-pub' not in desktop)
chk('A4) markup: tab-pub + 5 shapka + tabPubRows', all(s in html for s in ['class="tab-pub"', 'tpubh-link', 'tpubh-copy', 'tpubh-vac', 'tpubh-start', 'tpubh-end', 'id="tabPubRows"']))
chk('A5) title/sub data-text-phone variantlari', 'специа-|листами газеты “Все В. Н.”' in html and 'Подробная информация по счёту|Св00000003222 от 03.09.2025' in html)
chk('A6) telefon shapkasida Вакансия yashirin, End/Начало variantlari', '.tpubh-vac { display: none; }' in phone and 'data-text-phone="Начало"' in html and 'data-text-phone="End"' in html)
chk('A7) planshet pozitsiyalari (574/1159/1288.3; row 146.5; sep 4.5)', all(s in tablet for s in ['calc(574 ', 'calc(1159 ', 'calc(1288.3 ', 'calc(146.5 ', 'calc(4.5 ']))
chk('A8) telefon pozitsiyalari (698.7/1167/1406.8; row 684.8; d2 551.8)', all(s in phone for s in ['calc(698.7 ', 'calc(1167 ', 'calc(1406.8 ', 'calc(684.8 ', 'calc(551.8 ']))
chk('A9) initTabPub oqimda + PUB_ROWS yagona manba', 'initTabPub();' in js and 'PUB_ROWS.forEach' in js.split('function initTabPub')[1].split('function initScrollTop')[0] and 'TAB_PUB_ROWS' not in js)
chk('A10) clipboard + TODO-CLIENT + fallback', 'navigator.clipboard.writeText(text).catch(legacy)' in js and "document.execCommand('copy')" in js and 'TODO-CLIENT' in js.split('function copyToClipboard')[1].split('function ')[0] + js.split('// «Скопировать»')[1].split('function copyToClipboard')[0])
chk('A11) applyPubSearch adaptiv qatorlarni ham filtrlaydi', "document.getElementById('tabPubRows')" in js.split('function applyPubSearch()')[1].split('\n    }')[0] + js.split('function applyPubSearch()')[1] and 'pubRowMatches' in js)
chk('A12) protokol kesiladi (etalon: yandex.ru/...)', "row.url.replace(/^https?:\\/\\//, '')" in js)

# === sana-konversiya birlik-testi (27 yozuv, replika) ===
RU = {'янв':'01','фев':'02','мар':'03','апр':'04','мая':'05','май':'05','июн':'06',
      'июл':'07','авг':'08','сен':'09','окт':'10','ноя':'11','дек':'12'}
def dots(s):
    p = s.strip().split()
    mm = RU.get(p[1].lower()[:3])
    if not mm: return None
    return ('0' + p[0] if len(p[0]) < 2 else p[0]) + '.' + mm + '.' + p[2]
rows = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',\s*account: '([^']*)',\s*accDate: '([^']*)',\s*url: '([^']*)',\s*removed: '([^']*)',\s*source: '([^']*)' \}", js)
chk('D0) 27 yozuv', len(rows) == 27)
bad = [(r[1], r[5]) for r in rows if not dots(r[1]) or not dots(r[5])]
chk('D1) 27/27 placed+removed konvertatsiya xatosiz', not bad)
cases = [('25 Янв 2025', '25.01.2025'), ('8 Авг 2024', '08.08.2024'),
         ('11 Нояб 2024', '11.11.2024'), ('22 Ноября 2024', '22.11.2024'),
         ('5 Марта 2025', '05.03.2025'), ('21 Мая 2025', '21.05.2025'),
         ('16 Февраля 2025', '16.02.2025'), ('30 Декабря 2024', '30.12.2024')]
for src, exp in cases:
    chk(f'D) «{src}» -> {exp}', dots(src) == exp)
chk('D2) formatlar DD.MM.YYYY (27x2)', all(re.match(r'^\d\d\.\d\d\.\d{4}$', dots(r[1])) and re.match(r'^\d\d\.\d\d\.\d{4}$', dots(r[5])) for r in rows))

chk('V) versiyalar 436/349', 'style.css?v=436' in html and 'script.js?v=349' in html)
print('TOTAL:', 'ALL PASS' if ok else 'FAILURES PRESENT')
