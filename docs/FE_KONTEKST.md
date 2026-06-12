# FE KONTEKST — vsevn.ru «Событие 2» (frontend ishchi-konteksti)

> Bu fayl yangi sessiya ishni xatosiz davom ettirishi uchun. Loyiha: kwork,
> «Отправленные резюме» kabineti sahifasi. Menejer TЗ beradi → bitta qadam
> bajariladi → DOKLAD (kodsiz) → TO'XTASH. Brauzerда tekshirilmaydi (vizualni
> foydalanuvchi tekshiradi); o'z-nazorat — PIL/fontTools bilan etalon o'lchash
> va dasturiy testlar. Til: o'zbekcha doklad, ruscha kod-kommentlar.

## 0. Qat'iy qoidalar
- Faqat toza HTML/CSS/JS. jQuery/framework/build TAQIQ. Rastr TAQIQ — hammasi inline-SVG.
- Barcha UI matn statik-dizayn dvigateli orqali (SVG `<text>`); istisno — qidiruv `<input>` (placeholder native).
- Pixel-perfect: o'lchamlar `calc(N * var(--dpx, 0.0520833vw))` (dizayn-px @1920).
- Data-driven: jadval/popап/chartlar JS massivlardan.
- Har o'zgarishda `node --check js/script.js`; versiya bump (`?v=` ikkalasi index.html'da).
- DOKLADGA KOD TASHLANMAYDI. Har adaptiv-dokладда desktop regress-suite (5-bo'lim).

## 1. Tuzilma va kalibrlar
```
index.html            — butun markup (sidebar, hero, mid-row, jadval, popап, tab-view)
css/style.css         — v=444 (keyingi bump: 445; 4-fix-4: passiv .snav-btn fon transparent, inset-kontur/aktiv qora saqlangan). GLOW'lar (4-fix-3): filter:blur YO'Q (Firefox ~100px cheklovi) — 3 glow radial-gradient, Gauss-stoplar (I(t·R)/I(0), R=yarim-o'q+2.2σ): GLOW-1/karta-zaif σ=587.5 peak .259 (markazlar (1231,518)/(1768,1121.5), box 3133×3860); GLOW-2 σ=400 peak .399, markaz (101,1072), vertikal radius 672 ga SIQILGAN (ko'rinadigan tepa y=400 — snav ~350 dan pastda; 4-fix-2 shu yerda).
js/script.js          — v=353 (keyingi bump: 354)
assets/figma/*.svg    — rasmiy ikonkalar (cowboy, nav-*, stat-*, search-lupa, dots-menu, terminal-logo...)
fonts/                — sora-variable-latin (100-800), figtree-variable (300-900), roboto-* (VARIABLE 100-900!)
docs/design/          — etalonlar: Homies Lab_ru2.jpg (4×1920 to'liq maket), panel-*@4x, vcard@4x,
                        search-states@1x, states-sheet@1x (1072×641), cowboy-tooltip@1x,
                        tablet-resume@4x (4×852), tablet-links@4x (2-bosqich), mobile-resume@4x (4×387),
                        mobile-links@4x (2-bosqich)
docs/ТЗ_реестр_требований.md — qabul cheklisti (R/G/POP/SEL kodlari)
```
- **dpx tizimi**: 1 dpx = dizayn-px @1920 = `0.0520833vw` (CSS fallback); JS runtime'da `--dpx`ni px qiymat sifatida har resize'da yangilab turadi (`updateZoomAwareLines`). Hech qachon --dpx'ni qo'lda o'rnatmaslik.
- **Mobil kalibrlar**: planshet maketi 852px → `TAB_T = 1920/852 = 2.2535`; telefon maketi 387px → `PHONE_T = 1920/387 = 4.962`. Mobil o'lchamlar CSS'da tayyor ko'paytirilgan dpx, JS'da maket-px × koef.
- **Breakpointlar**: `@media (max-width: 799.98px)` planshet (desktop bloklar yashirinadi, `.tab-view` ochiladi), `@media (max-width: 489.98px)` telefon (planshet ustiga override). Ikkala chegara kesilishida `matchMedia.change → renderStaticText()` (to'liq qayta-render).
- Layout: `.dash-page > .dash-card(overflow:hidden, glow ::before/::after) > .dash-top(flex: sidebar+main) + .resume-panel + .tab-view + #pageSpacer(dinamik)`.

## 2. Dvigatel va kengaytmalar (js/script.js)
Yadro: `renderElementText(el, {text, lines, size, width, height, x, y, anchor, weight, color, family, lineHeight, letterSpacing, useBitmapText:false})` → SVG `<text>`; `measureTextWidth(text,size,weight,family)` (canvas, natija = ceil+2); render-key (`getSvgTextRenderKey`) takror chizishni kesadi. Birinchi baseline = `round(0.82·size)`; cap: kirill→Roboto 0.711·size, lotin/raqam→Sora 0.753·size. Fontlar: `DASH_NAV_TEXT_FAMILY` = Sora-stack (kirill Roboto'ga tushadi — ataylab), `REPORT_TEXT_FAMILY` = Figtree-stack.

`renderStaticText()` (DOMContentLoaded + fonts.ready + breakpoint-change'larda) oqimiga ulanganlar:
- `renderDashboardStaticText` — sidebar nav/bell/exit matnlari.
- `renderHeroStaticText` + `initGauge` — hero matnlari va parametrik gauge (`.hero-gauge[data-value/max]`).
- `renderMidStaticText` (midTextSpecs) — o'rta qator panellari A/B/C + vcard matnlari.
- `initLineCharts` — `.line-chart[data-values...]` chiziq-chartlar; `initReachBars` — `.reach-bar[data-pct]` ustunlar (h=143.1+1.447·pct).
- `initResumeTable` — desktop jadval DOM (RESUME_ROWS→qatorlar) + matnlar; `renderResumeCellText`/`renderHighlightedCellText` (oranj #FD6429 highlight rect+tspan).
- `initResumeSearch` — prefix-qidiruv (`wordPrefixRanges` — faqat so'z boshi, case-insensitive), filtr, fokus holatlari (.is-focused/.has-value), ✕ tozalash; `applyResumeSearch` = qidiruv ∧ hisob-filtri + popап ochiq bo'lsa SEL1 qayta hisob.
- `initAccountsPopup` (2.3 dan: FABRIKA) — `createAccPopupController(cfg)` → 2 instansiya: `resumeAccPopup` (head '.resume-panel:not(.pub-panel) .resume-head', ID'lar accPopup/accList/accThumb, apply=applyResumeSearch) va `pubAccPopup` (head '.pub-head', pubAccPopup/pubAccList/pubAccThumb, apply=applyPubSearch). ACCOUNTS YAGONA manba, har kontroller O'Z filterSet/scrollIndex/bound/listBuilt; `accountFilterSet` = resumeAccPopup.filterSet (shim — applyResumeSearch tegilmagan). open() boshqalarini yopadi (bir vaqtda 1 popап); POP7 o'z popап/dots'idan tashqari click → yopish; filtr-✕ faqat O'Z ro'yxatini tozalaydi; mexanika 1.6 aynan (layoutAccPopup --acc-w/--acc-date-x, scrollbar, POP8 filter-active CSS pub-head'ga avtomatik, SEL1 ensureAccPopupVisible ikkala apply'da). addAccountEntry ikkala ro'yxatni markListStale qiladi.
- `initTabView` + `renderTabText(el, makSize, weight, color, makLh, koef)` — mobil ko'rinish: nav/statlar/kompaniya/jadval matnlari (koef=TAB_T yoki PHONE_T; PHONE_T'da `data-text-phone` varianti tanlanadi), `formatPhoneIntl` (+7 XXX XXX-XX-XX).
- `initTabPub` (2.4) — adaptiv pub-jadval `.tab-pub` (PUB_ROWS yagona manba): sarlavha 25/600 lh30.3 (tel 20/600 lh24.1), sub 20/300 (tel 18, 2 qator statik), shapka 14/400 (tel «Вакансия» yashirin, «Начало/End»), qator h65m (tel stacked h138m), ajratkich OQISH rgba(255,255,255,.66) 2m; havola PROTOKOLSIZ `truncToWidth` bilan «...» (planshet 238m, tel 305m), vakansiya `wrapTwoLines` 2 qatorgacha; **sanalar Roboto** (`renderTabDate`, 20: etalon cap 14.4/w 99.5 = Roboto tabular, Sora sig'masdi), `pubDateDots` («25 Янв 2025»/«25 Апреля 2025»→«25.01.2025», 3-harf prefiks lug'ati); `copyToClipboard` (clipboard API→execCommand fallback, feedback YO'Q — TODO-CLIENT); `applyPubSearch` adaptiv qatorlarni ham filtrlaydi (`pubRowMatches` umumiy predikat — desktop bilan bitta holat). Ko'rinish: media ichida body.pub-mode → .ttable yashirin, .tab-pub block; adaptivda qidiruv kapsulasi YO'Q (1.8 resume'da ham yo'q — naqsh saqlangan).
- `initPubTable` (2.1) — «Дополнительные публикации» jadvali (PUB_ROWS→#pubRows, resume CSS-klasslari umumiy; per-ustun baseline: vac 50.5 / raqamli 49.6); `initPubSearch` — pub-kapsula fokus/✕ + real-time filtr; `initPubToggle` — DEV: hash `#pub` → body.pub-mode + snav aktiv almashinuvi (3-bosqichgacha vaqtinchalik).
- `applyPubSearch` (2.2) — PUB_SOURCE_NAMES {ok:Одноклассники, vk:ВКонтакте, site:Сайты, tg:Телеграм, max:Макс} display-nomi BOSHIDAN prefix (case-insens.), highlight YO'Q; bo'sh→27, mos yo'q→0. `initViewCards` (P1/P2) — vcard «Посмотреть»+strelka juftlik-hover (CSS: .vcard-foot pointer-events:none, bolalari auto → bo'sh oraliq hover bermaydi; aktiv: punktir 1.26/2.53 top13.5 #161715, doira #2F3027, strelka oq — pressed ham shu, states-sheet'da alohida rang yo'q); klik → data-pub-word so'zi pub-qidiruvga (to'liq almashtirish) + hash #pub fallback (// TODO-STAGE3).
- `renderUiTips` — generik tooltip matnlari (`.ui-tip`; `.ui-tip--dark` = ixcham to'q #64635C/oq 14.2 — kovboy+exit; oddiy = #BDBBB7/qora 22); pozitsiyalar: default below-center, `data-tip-pos="below-right"` (+15.7, gap 21.8), `"above-center"` (gap 7); ko'rsatish sof CSS `.has-ui-tip:hover`.
- `initUiTipClamp` — mouseover'da tooltip gorizontal clamp (karta/viewport chetidan chiqsa marginLeft bilan suriladi).
- `initScrollTop` — «вверх»: chegara desktop 400 / mobil(<800) 100; visualViewport.resize'da `innerHeight − vv.height > 150` → klaviatura ochiq deb tugma yashiriladi (faqat mobilda; vv yo'q brauzerda fallback — oddiy xatti-harakat); breakpoint change → sync.

## 3. Data massivlari (hammasi js/script.js ichida)
- `RESUME_ROWS` — 20 yozuv {name, phone(89XXXXXXXXX), vacancy, email, replyDate, account, accountDate}. Familiyalar А..Х 20 turli harf, vakansiyalar 20 turli harf; R4: №3 Васильев va №12 Морозов umumiy hisob `Св000000001829`.
- `RESUME_COLS` — 7 ustun {key, x(panel-rel), size, maxW(himoya)}: x=[49,322.8,540.2,896.2,1181,1373.5,1621], size=[23,23,20,20,20,18.82,20], weight 300, rang #2E2F27; baseline qator ichida 50.5, qator h 89.
- `ACCOUNTS` — 20 yozuv {num, date DD.MM.YYYY} SANA BO'YICHA KAMAYISH; 19 tasi jadval hisoblari + `Св000000001944` (resume-jadvalda yo'q); `accountInsertIndex/addAccountEntry` tartibni saqlab qo'shadi.
- `PUB_COLS`/`PUB_ROWS` (2.1) — pub-jadval: 6 ustun {key,x,size,base,maxW}: x=[46.8,589.4,789.1,1034.3,1234.4,1581.1], size=[23,20,18.82,20,20,20], base=[50.5,49.6…]; header `.pcol-1..6` band-rel x=[18.8,559.2,759.6,1005.8,1203.4,1543.5]. 27 yozuv {vac,placed,account,accDate,url,removed,source}; source ok6/vk6/site5/tg5/max5; 7 hisob 2 tadan (1829/1846/1874/1902/1917/1930/1944), barcha 20 ACCOUNT ishlatilgan, accDate ↔ ACCOUNTS sanasi mos; placed «11 Нояб 2024» (qisqa oy) KAMAYISH tartibida, accDate/removed to'liq oy; etalon qatori t.me/Rabota_vod/273 + Св…1829 saqlangan.
- `heroTextSpecs`/`midTextSpecs` — selektor-spec jadvallar (size/weight/color/lineHeight/family:'figtree') — renderHero/MidStaticText ularni renderElementText'ga uzatadi.
- Mobil kegllar initTabView ichida shartli: tablet/phone juftliklar (nav 19/16, stat-num 47/45, label 16.5/16, kompaniya 34/21+25/19, title 25/20.5 (600), sub 22/19, headerlar 18.5/14, yozuvlar 21/18; telefon vakansiya QIZIL #820407, tel #1F76A3).

## 4. Asosiy ranglar/tokenlar
#2E2F27 (asosiy to'q matn), #7C7971/#7B786F (kulrang), #FD6429 (highlight), #1F76A3 (tel ko'k), #820407 (mobil vakansiya qizili), #FE1D19 (filtr qizili), #0087FC oilasi (popап ko'klari: kontur/checked; #7BBEF9 noaktiv, #026FCE hover, #86C7FF thumb), #B1AFAA/#7C7971 (✕ normal/hover), #BDBBB7 (oddiy tooltip), #64635C (dark tooltip), #2F3027/#40422E (olive karta normal/hover), #EEE5CE (mobil tugma hover), #DD5326 (exit).

## 5. Desktop regress-suite (har adaptiv-dokладда majburiy)
Python bilan tekshirish — `css.split('@media (max-width: 799.98px)')[0]` (desktop qismi) ichida:
1–7) `.rcol-1..7 { left: calc(X` X=[32.3,290.7,511,874,1150.7,1344,1601.5];
8) JS `RESUME_COLS` x = [49,322.8,540.2,896.2,1181,1373.5,1621];
9) `.resume-col` absolute top 13.8; 10) `.resume-cell` absolute + `clip-path: inset(calc(-8`;
11) `.resume-row` h calc(89; 12) `.resume-cols` band w 1743.5 h 48.8;
13) `.resume-filter-btn` absolute left 1724.1 top 32.3; 14) `.resume-search` left 1442 top 31.15, 271.04×49.85;
15) `.tab-view { display: none; }` media TAShQARISIDA; 16) tnav/tstats/trow qoidalari FAQAT media ichida;
17) planshet blokida `grid-template-columns: calc(418` saqlangan.
Qo'shimcha: telefon qoidalari faqat 489.98 ichida; `node --check`.

## 6. Saboqlar (takrorlamaslik!)
- **slice-to-EOF TAQIQ**: `s[s.index('@media...'):]` bilan almashtirish media'dan keyingi desktop qoidalarni yutgan (1.8-REGRESS). Har doim aniq anchor-to-anchor.
- CSS tartibi tarixiy aralash: 1.4 jadval qoidalari 1.5–1.8 bloklaridan KEYIN ham bor — qidirishda butun faylga grep.
- Roboto VARIABLE (100-900) — 600 haqiqiy bold, advance kengayadi; sig'ish hisoblarini fontTools instancer bilan kerakli weight'da qilish.
- Etalon JPEG ranglari aldashi mumkin (eski image5 sariq karta — yolg'on edi); yuqori sifatli @4x etalon ustun.
- measureTextWidth natijasi = ceil(w)+2 (zaxira ichida).
- fill SVG-atributi CSS qoidasidan yutqazadi — hover/checked rang almashinuvi qayta-rendersiz (`.acc-row:hover .svg-label text {fill}`).
- `.dash-card overflow:hidden` — popап/elementlar kartadan chiqsa kesiladi; sahifani uzaytirish kerak bo'lsa spacer KARTA ICHIGA.
- Sheet-kolajlar (states-sheet) masshtabi nomuvofiq (1.6–2.0) — ichki kalibr (matn cap ↔ ma'lum kegl) yoki ma'lum element orqali.
- Bash heredoc uzun bo'lsa "unexpected EOF" — python skriptни faylga yozib ishga tushirish; print'da cp1252 → `sys.stdout.reconfigure(encoding='utf-8')`.

## 7. TODO-CLIENT markerlari (mijoz qiymatlari kelganda almashtirish)
- index.html: kovboy tooltip matni («Газета «Все Вакансии Нижнего»» vaqtincha) — 2 komment.
- css/style.css: `.snav-logo:hover svg { filter: brightness(0.93) saturate(1.15) }` vaqtincha hover — 2 komment.
- Ochiq savollar: panel B punktir (Figma kutilmoqda), GLOW-2/karta-glow aniq spec, panel A/C/vcards/jadval fill'lari (hozir rgba(255,253,244,.62)), jadval band qoplamasi rgba(150,140,110,.12), mobil 432 yorlig'i «Всего дополнительных размещений» (semantika savoli), «Терминал» faqat planshetda ko'rinadi (telefon bandda logosiz — etalon).

## 8. JORIY HOLAT (keyingi qadam)
- 1.8/2.1/2.2/2.3 QABUL QILINGAN. **2.4 BAJARILDI** (css v=436, js v=349): adaptiv pub-jadval .tab-pub (planshet+telefon, etalonlar tablet-links@4x/mobile-links@4x); suite'lar `tools/regress_24.py` (17+30 PASS) va `tools/tabpub_fit_check.py` (ALL FIT). DOKLAD berilgan, qabul kutilmoqda.
- 2.4 saboq: tab-pub SANALARI etalon bo'yicha Roboto-raqam (tabular) — Sora-raqamlar nopproporsional/keng (03.09.2025: Sora 110.8 vs Roboto 101.7 vs etalon 99.5); mobil «Начало End» etalon'da deyarli tegib turadi (End o'ng cheti kontentdan ~2m chiqadi — dizayn shunday).
- **2.4-FIX BAJARILDI** (css v=437, js v=350): tstat raqamlari ham ROBOTO (45 planshet / 46 telefon — etalon cap 31.8/32.8 va ink-enlar isbotladi; Sora 47/45 ~14% keng bo'lib planshet col4 da DOIMIY (290>256), telefonda scrollbar-sharoitda «246» ni ag'darardi — vw scrollbar'ni o'z ichiga oladi, konteyner real eni esa yo'q, −84..105dpx); `renderTabDate`→`renderTabRoboto` (sanalar+raqamlar); chip margin etalon: 19.8dpx planshet / 74dpx telefon (ink-gap − raqam lsb); `.tstat{white-space:nowrap; font-size:0}` (struktura himoyasi + probel-tugunlarning real-px hissasi o'chirildi); telefon `.tth-vac{vertical-align:top}` (baseline-siljish: 856 vs 852 → 854=854=854). Suite `tools/regress_24fix.py` 17+17 PASS; headless DOM sonli-o'lchov bilan tasdiq (700/390/320 + 17px scrollbar-sim + #pub).
- MUHIM o'lchov-saboq: Homies Lab_ru.jpg (7752×6000, ×4.0375) O'NG chetida ~21.6px **scrollbar запечён** (karta 41.6..1856.8, 1898.4 ichida markazlangan) — o'ng-anker elementlar (kapsula/«...») chapga surilgan ko'rinadi; ular uchun resume Figma-spec qayta ishlatildi, chap-anker (title/ustunlar) etalondan.
- **3-BOSQICH BAJARILDI** (css v=438, js v=351): S1 — `setPubMode(on)` (klasslar+hash replaceState+initTabView tnav-rang uchun; filtr/qidiruv holatlariga TEGMAYDI), sidebar `.snav-btn` va mobil `.tnav-btn` ads/resume kliklari bog'langan (journal/email harakatsiz); B1 — `.promo-arrow` klik → pub + `scrollPubTitleTop()` (desktop .pub-title / adaptiv .tpub-title ekran tepasiga, smooth; hover TODO-CLIENT); «Посмотреть» endi setPubMode(true)+so'z; TODO-STAGE3 yopildi, hash dev-yo'l sifatida ishlaydi (hashchange listener). YANGI QOIDALAR: brauzer-MCP TAQIQ, tekshiruv minimal (node --check + nishonli), doklад 6-8 qator.
- **3-FIX** (css v=439): (1) planshet ttable/tpub title-sub svg'lariga `max-width:100%` himoya (etalon'da title ink 1386/1410 — chetga 5.6m, render-zaxira/kasr-piksel chiqaradi; viewBox meet → yomon holatda proporsional siqiladi); (2) promo-arrow hover = «Посмотреть» uslubi (doira #2F3027/oq strelka) + transition .18s — TODO-CLIENT yopildi; (3) telefon `.tpubh-end` 1406.8→1418 (etalon ink-oraliq «Начало|End» = 5m).
- **4-BOSQICH BAJARILDI** (v=440/352): TD1 — kovboy SVG dedupe (defs + 7×`<path id="cb0..6">` + `<g id="cbAll">`, masklar/filter/stroke'lar `<use>` orqali; 179.5KB→24.2KB, index 261.9→106.5KB, path-data baytma-bayt saqlangan); G2-audit toza (y=round(0.82s) yagona formula; resume raqam-ustunlari ru2-etalon bo'yicha umumiy baseline 50.5 — hujjatlangan istisno; pub/tab-pub raqam-qoida qo'llangan); PIXEL-PASS 12 nuqta ✓; favicon data:, (konsol-404 o'chdi). Deploy-to'plam: index.html + css/ + js/ + fonts/ (20 fayl) + icons/clear/ (2 svg); tools/, docs/, assets/figma (faqat kommentlarda), image*.png — deploy'ga KIRMAYDI.
- **4-FIX** (v=441/353): tnav hover etalon (fon #EEE5CE, kontur fonga singiydi — border-color ham #EEE5CE, transition .18s, `:not(.is-active)`); krossbrauzer: `<use>` xlink:href dublikatlar (28) + xmlns:xlink, `bindMqChange` (addListener fallback), `smoothScrollTo` (scrollBehavior detect), `inset:0` → longhand (9 joy), `-webkit-clip-path` dublikat; flex-gap Safari ≥14.1 talab (zamonaviy maqsadga mos, o'zgarmadi); iOS fokus-zoom viewport maximum-scale=1 bilan allaqachon o'chiq.
- TODO-CLIENT: «Скопировать» feedback; tab-pub sub semantikasi.
- Xotira fayli: `C:/Users/admin/.claude/projects/C--Users-admin-Desktop-header-only/memory/vsevn-dashboard-arch.md` — to'liq arxitektura tarixi (o'qish tavsiya etiladi).
