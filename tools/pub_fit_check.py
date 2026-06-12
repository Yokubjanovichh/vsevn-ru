# -*- coding: utf-8 -*-
# 2.1: pub-jadval sig'ish-tekshiruvi (fontTools, haqiqiy advance @300)
# kirill -> Roboto variable wght300, lotin/raqam/punkt -> Sora variable wght300
import sys
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

def load(path, wght):
    f = TTFont(path)
    if 'fvar' in f:
        instantiateVariableFont(f, {'wght': wght}, inplace=True)
    return f

def adv(f, ch):
    cmap = f.getBestCmap()
    gid = cmap.get(ord(ch))
    if gid is None: return None
    return f['hmtx'][gid][0] / f['head'].unitsPerEm

sora = load('fonts/sora-variable-latin.woff2', 300)
rob_lat = load('fonts/roboto-latin.woff2', 300)
rob_cyr = load('fonts/roboto-cyrillic.woff2', 300)

def width(text, size):
    w = 0.0
    for ch in text:
        if 'Ѐ' <= ch <= 'ӿ':
            a = adv(rob_cyr, ch) or adv(rob_lat, ch)
        else:
            a = adv(sora, ch)
            if a is None: a = adv(rob_lat, ch) or adv(rob_cyr, ch)
        if a is None:
            print('  !! glyph yo`q:', repr(ch)); a = 0.6
        w += a * size
    return w

# ustun limitlari (maxW, dizayn-px)
LIM = {'vac': 526.6, 'placed': 183.7, 'account': 229.2,
       'accDate': 184.1, 'url': 330.7, 'removed': 191.9}
SIZE = {'vac': 23, 'placed': 20, 'account': 18.82,
        'accDate': 20, 'url': 20, 'removed': 20}

# yakuniy data — bevosita js/script.js'dagi PUB_ROWS'dan
import re
js = open('js/script.js', encoding='utf-8').read()
rows = re.findall(r"\{ vac: '([^']*)',\s*placed: '([^']*)',\s*account: '([^']*)',"
                  r"\s*accDate: '([^']*)',\s*url: '([^']*)',\s*removed: '([^']*)',"
                  r"\s*source: '([^']*)' \}", js)
assert len(rows) == 27, len(rows)
candidates = {
 'vac': sorted(set(r[0] for r in rows)),
 'placed': [r[1] for r in rows],
 'account': sorted(set(r[2] for r in rows)),
 'accDate': [r[3] for r in rows],
 'url': [r[4] for r in rows],
 'removed': [r[5] for r in rows],
}
# shapka matnlari ham (22/300, ustun oralig'iga sig'ishi)
HEAD = [('ВАКАНСИЯ', 540.6), ('ДАТА РАЗМЕЩ.', 200.4), ('СЧЁТ', 246.2),
        ('ДАТА СЧЁТА', 197.6), ('ССЫЛКА НА ОБЪЯВЛЕНИЕ', 340.1),
        ('ДАТА УДАЛЕНИЯ', 200)]

allok = True
for key, vals in candidates.items():
    lim, size = LIM[key], SIZE[key]
    worst = max(vals, key=lambda t: width(t, size))
    for t in vals:
        w = width(t, size)
        flag = 'OK ' if w <= lim else 'FAIL'
        if w > lim: allok = False
        if w > lim or t == worst:
            print('%s %-8s %6.1f / %6.1f  %s' % (flag, key, w, lim, t))
for t, lim in HEAD:
    w = width(t, 22)
    flag = 'OK ' if w <= lim else 'FAIL'
    if w > lim: allok = False
    print('%s %-8s %6.1f / %6.1f  %s' % (flag, 'head', w, lim, t))
print('TOTAL:', 'ALL FIT' if allok else 'TRIM NEEDED')

# etalon kalibr: t.me/Rabota_vod/273 etalonda 280.6 px
print('kalibr t.me/Rabota_vod/273: hisob=%.1f etalon=280.6' %
      width('https://t.me/Rabota_vod/273', 20))
