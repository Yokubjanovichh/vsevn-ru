#!/usr/bin/env python
# coding: utf-8
# 8-C: mobile/planshet `.tsearch` qidiruv-kapsulasi geometriyasini etalondan
# (PIL bilan) o'lchaydi. Yondashuv: kulrang kontur #7C7971 (border) atrofida
# pikselli yig'indi-hisob bilan kapsula bbox'ini topish.
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import numpy as np

SCALE = 4  # @4x export
BORDER_TARGET = np.array([0x7C, 0x79, 0x71], dtype=int)
TOLERANCE = 22

ETALONLAR = [
    ('mobile-resume', 'docs/design/mobile-resume@4x.jpg', 387),
    ('tablet-resume', 'docs/design/tablet-resume@4x.jpg', 852),
    ('mobile-links',  'docs/design/mobile-links@4x.jpg',  387),
    ('tablet-links',  'docs/design/tablet-links@4x.jpg',  852),
]

def find_border_mask(arr, tol=TOLERANCE):
    diff = np.abs(arr.astype(int) - BORDER_TARGET.reshape(1, 1, 3))
    return (diff < tol).all(axis=2)

def measure_capsule(path, maket_w):
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    h_full, w_full = arr.shape[:2]

    # Kapsula taxminan etalon top 1/4 atrofida (sarlavha+sub+kapsula bloki)
    y_search_max = h_full // 4
    region = arr[:y_search_max]
    mask = find_border_mask(region)

    # Har qator uchun border-pikseller sonini hisoblash; kapsula yuqori va
    # pastki chetlari eng katta gorizontal segmentlar (yumaloq emas, balki
    # to'g'ri uzun chiziqlar — kapsula chapdan o'ngga kichik ovalish)
    row_counts = mask.sum(axis=1)
    if row_counts.max() == 0:
        return None

    # Eng katta gorizontal kontur segmentlari kapsula yuqori/pastki chetlari
    threshold = max(50, w_full // 6)  # kapsula border-len ~ eni/2 dan ko'p
    rows_with_border = np.where(row_counts >= threshold)[0]
    if len(rows_with_border) == 0:
        # Threshold past — kapsula ko'rilmaydi yoki kontur uzilgan
        threshold = max(20, w_full // 20)
        rows_with_border = np.where(row_counts >= threshold)[0]
        if len(rows_with_border) == 0:
            return None

    # Yaxshilangan klasterizatsiya: kapsula = ikkita yaqin gorizontal chiziq
    # (yuqori va pastki kontur), ular orasida gap = kapsula ichi. Klasterlarni
    # gap=10+ piksel orqali ajratamiz va eng katta gap orqali bog'langan ikki
    # klasterni kapsula deb topamiz.
    diffs = np.diff(rows_with_border)
    gap_idx = np.where(diffs > 10)[0]
    if len(gap_idx) == 0:
        y_top = int(rows_with_border[0])
        y_bot = int(rows_with_border[-1])
    else:
        starts = np.concatenate([[rows_with_border[0]], rows_with_border[gap_idx + 1]])
        ends = np.concatenate([rows_with_border[gap_idx], [rows_with_border[-1]]])
        gaps_between = starts[1:] - ends[:-1]
        # Kapsula ichidagi gap ~ kapsula balandligi - 2*border qalinligi (~30-200 px)
        # Eng katta GAP orqali ajratilgan ikki klaster = kapsula yuqori+pastki
        max_gap_i = int(gaps_between.argmax())
        y_top = int(starts[max_gap_i])
        y_bot = int(ends[max_gap_i + 1])

    # Kapsula chap/o'ng chegaralari
    cap_mask = mask[y_top:y_bot + 1]
    col_counts = cap_mask.sum(axis=0)
    cols_with_border = np.where(col_counts > 3)[0]
    if len(cols_with_border) == 0:
        return None
    x_left = int(cols_with_border[0])
    x_right = int(cols_with_border[-1])

    w_px = x_right - x_left
    h_px = y_bot - y_top
    img_w = arr.shape[1]
    img_scale = img_w / maket_w  # ~ SCALE=4

    return {
        'image_size': (img_w, h_full),
        'bbox_4x': (x_left, y_top, x_right, y_bot),
        'capsule_w_px@4x': w_px,
        'capsule_h_px@4x': h_px,
        'capsule_w_maket': round(w_px / img_scale, 2),
        'capsule_h_maket': round(h_px / img_scale, 2),
        'capsule_y_top_maket': round(y_top / img_scale, 2),
        'border_radius_h/2_maket': round(h_px / img_scale / 2, 2),
        'img_scale_to_maket': round(img_scale, 4),
    }

for name, path, maket_w in ETALONLAR:
    print(f'=== {name} ({path}, maket-w {maket_w}px) ===')
    try:
        r = measure_capsule(path, maket_w)
        if r:
            for k, v in r.items():
                print(f'  {k}: {v}')
        else:
            print('  DETEKTSIYA YO\'Q (kapsula konturi topilmadi)')
    except Exception as e:
        print(f'  XATO: {e}')
    print()
