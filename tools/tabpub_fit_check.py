# -*- coding: utf-8 -*-
# 2.4: tab-pub sig'ish-suite (fontTools): planshet (852-bazа) + telefon (387)
# Hamma o'lchov maket-px'da (koef bir xil bo'lgani uchun dpx'ga teng nisbat).
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

def load(path, wght):
    f = TTFont(path)
    if 'fvar' in f:
        instantiateVariableFont(f, {'wght': wght}, inplace=True)
    return f

FONTS = {}
def font(name, w):
    key = (name, w)
    if key not in FONTS:
        path = {'sora': 'fonts/sora-variable-latin.woff2',
                'rob_lat': 'fonts/roboto-latin.woff2',
                'rob_cyr': 'fonts/roboto-cyrillic.woff2'}[name]
        FONTS[key] = load(path, w)
    return FONTS[key]

def adv(f, ch):
    gid = f.getBestCmap().get(ord(ch))
    return None if gid is None else f['hmtx'][gid][0] / f['head'].unitsPerEm

def width(text, size, w=300):
    total = 0.0
    for ch in text:
        if 'Ѐ' <= ch <= 'ӿ' or ch in '«»“”№':
            a = adv(font('rob_cyr', w), ch) or adv(font('rob_lat', w), ch)
        else:
            a = adv(font('sora', w), ch)
            if a is None: a = adv(font('rob_lat', w), ch) or adv(font('rob_cyr', w), ch)
        if a is None: a = 0.6
        total += a * size
    return total

ok = True
def chk(name, w, lim):
    global ok
    good = w <= lim
    print(('PASS' if good else 'FAIL'), '%-58s %7.1f / %7.1f' % (name, w, lim))
    if not good: ok = False

js = open('js/script.js', encoding='utf-8').read()
rows = re.findall(r"\{ vac: '([^']*)',[^}]*url: '([^']*)',[^}]*source: '([^']*)' \}", js)
assert len(rows) == 27

# ============ PLANSHET (kontent eni 623 maket-852) ============
CW_T = 623
chk('T title L1 25/600', width('Все размещения объявлений на внешних ресурсах', 25, 600), CW_T)
chk('T title L2 25/600', width('специалистами газеты “Все Вакансии Нижнего”', 25, 600), CW_T)
chk('T sub 20/300', width('Подробная информация по счёту №Св000000000291', 20), CW_T)
# shapka: keyingi element boshlanishiga >=2 zazor (advance-model ink'dan
# ~3% keng — etalon-kalibr 133.2<->137.8 hisobga olingan)
chk('T hdr «Ссылка на источник.» 14/400', width('Ссылка на источник.', 14, 400), 141.3 - 2)
chk('T hdr «Скопировать»', 141.3 + width('Скопировать', 14, 400), 254.7 - 2)
chk('T hdr «Вакансия»', 254.7 + width('Вакансия', 14, 400), 514.3 - 2)
chk('T hdr «Начало.»', 514.3 + width('Начало.', 14, 400), 571.7 - 2)
chk('T hdr «Оконч.»', 571.7 + width('Оконч.', 14, 400), CW_T)
# qatorlar: sana ustuni — ROBOTO 20 (etalon: tabular advance, w~99.5)
def rwidth(text, size, w=300):
    total = 0.0
    for ch in text:
        a = adv(font('rob_lat', w), ch) or adv(font('rob_cyr', w), ch) or 0.6
        total += a * size
    return total
chk('T date Roboto 20/300', 514 + rwidth('03.09.2025', 20), CW_T)
chk('T «Скопировать» qatorda 21/300', width('Скопировать', 21), 238)

# havola-kesish va vakansiya-o'rash replikasi (JS algoritmi, +2 zaxira ceil)
def trunc(text, size, maxW):
    if width(text, size) + 2 <= maxW: return text
    t = text
    while len(t) > 1 and width(t + '...', size) + 2 > maxW:
        t = t[:-1]
    return t + '...'

def wrap2(text, size, maxW):
    words = text.split()
    l1 = ''; i = 0
    while i < len(words):
        cand = (l1 + ' ' + words[i]) if l1 else words[i]
        if l1 and width(cand, size) + 2 > maxW: break
        l1 = cand; i += 1
    if i >= len(words): return [l1]
    return [l1, trunc(' '.join(words[i:]), size, maxW)]

worstL = ''
for vac, url, src in rows:
    t = trunc(url.replace('https://', ''), 21, 238)
    w = width(t, 21)
    if w > width(worstL, 21): worstL = t
chk('T eng keng kesilgan havola 21/300 (%s)' % worstL, width(worstL, 21), 238)
worstV = max((wrap2(v, 21, 240) for v, _, _ in rows), key=lambda ls: max(width(l, 21) for l in ls))
chk('T eng keng vakansiya-qator (2 qatorgacha)', max(width(l, 21) for l in worstV), 240)
print('   (planshet: barcha vakansiyalar <=2 qator: %s)' %
      all(len(wrap2(v, 21, 240)) <= 2 for v, _, _ in rows))

# ============ TELEFON (kontent eni 307 maket-387) ============
CW_P = 307
chk('P title L1 20/600', width('Все размещения объявлений', 20, 600), CW_P)
chk('P title L2 20/600', width('на внешних ресурсах специа-', 20, 600), CW_P)
chk('P title L3 20/600', width('листами газеты “Все В. Н.”', 20, 600), CW_P)
chk('P sub L1 18/300', width('Подробная информация по счёту', 18), CW_P)
chk('P sub L2 18/300', width('Св00000003222 от 03.09.2025', 18), CW_P)
chk('P hdr «Ссылка на источник.»', width('Ссылка на источник.', 14, 400), 140.8 - 2)
chk('P hdr «Скопировать»', 140.8 + width('Скопировать', 14, 400), 235.2 - 2)
# etalon «Начало End» deyarli tegib turadi (guruh 235.2..307.8 zich);
# advance-model rsb/lsb ~2.5 ni o'z ichiga oladi -> ink-gap ~3 ta'minlanadi
chk('P hdr «Начало»', 235.2 + width('Начало', 14, 400), 283.5 + 1.5)
chk('P hdr «End»', 283.5 + width('End', 14, 400), CW_P + 4)
# sanalar yonma-yon — ROBOTO 20 (etalon: d1 w99.5 + gap 11.7 = d2 left 111.2)
chk('P d1 Roboto 20 d2-gacha', rwidth('03.09.2025', 20), 111.2 - 4)
chk('P d2 o\'ng chetgacha', 111.2 + rwidth('03.09.2025', 20), CW_P)
# eng keng sana (54 ta konvertlangan qiymat orasida, Roboto 20)
RU = {'янв':'01','фев':'02','мар':'03','апр':'04','мая':'05','май':'05','июн':'06',
      'июл':'07','авг':'08','сен':'09','окт':'10','ноя':'11','дек':'12'}
def dots(s):
    p = s.strip().split()
    return ('0' + p[0] if len(p[0]) < 2 else p[0]) + '.' + RU[p[1].lower()[:3]] + '.' + p[2]
rows_full = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',[^}]*removed: '([^']*)',", js)
alldates = [dots(r[1]) for r in rows_full] + [dots(r[2]) for r in rows_full]
worstD = max(alldates, key=lambda t: rwidth(t, 20))
chk('P/T eng keng sana (%s)' % worstD, rwidth(worstD, 20), 109)
worstLp = ''
for vac, url, src in rows:
    t = trunc(url.replace('https://', ''), 20, 305)
    if width(t, 20) > width(worstLp, 20): worstLp = t
chk('P eng keng kesilgan havola 20/300 (%s)' % worstLp, width(worstLp, 20), 305)
worstVp = max((wrap2(v, 20, 305) for v, _, _ in rows), key=lambda ls: max(width(l, 20) for l in ls))
chk('P eng keng vakansiya-qator', max(width(l, 20) for l in worstVp), 305)
print('   (telefon: barcha vakansiyalar <=2 qator: %s)' %
      all(len(wrap2(v, 20, 305)) <= 2 for v, _, _ in rows))
# nechta havola umuman kesiladi?
nt = sum(1 for _, u, _ in rows if trunc(u.replace('https://', ''), 21, 238) != u.replace('https://', ''))
np_ = sum(1 for _, u, _ in rows if trunc(u.replace('https://', ''), 20, 305) != u.replace('https://', ''))
print('   (kesilgan havolalar: planshet %d/27, telefon %d/27)' % (nt, np_))

print('TOTAL:', 'ALL FIT' if ok else 'OVERFLOW PRESENT')
