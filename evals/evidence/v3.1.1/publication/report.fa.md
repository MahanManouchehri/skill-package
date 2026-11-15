# گزارش نهایی Skill Package 3.1.1

این گزارش، شواهد snapshot منتشرشده در tag `v3.1.1` و کامیت `80ca761864da9134141df432224015390afe8ea6` را ثبت می‌کند. تغییرات بعدی مستندات روی `main`، tag یا نتایج تاریخی این گزارش را تغییر نمی‌دهند.

وضعیت: **DONE_WITH_LIMITATIONS**. اصلاحات، تست‌های محلی و ویندوز، Commit، Push و annotated tag انجام و تأیید شدند. نصب فعلی هر ۲۶ اسکیل با نسخهٔ منتشرشده تطبیق دارد؛ وضعیت نصب **NO_REINSTALL_NEEDED** است. پوشش native کاملِ ۶۰ سناریو به‌دلیل توقف ثبت‌شدهٔ مصرف تکمیل نشده است.

| شناسه | مقدار تأییدشده |
|---|---|
| مخزن و نسخه | [MahanManouchehri/skill-package — v3.1.1](https://github.com/MahanManouchehri/skill-package/tree/v3.1.1) |
| مسیر محلی | `/Users/mahan/Desktop/Web/skill-package` |
| مبنا | `11d61b3e05afaf2749d7314d1a72d0c1d9ed3523` — v3.1.0 |
| کامیت نهایی و مقصد tag | `80ca761864da9134141df432224015390afe8ea6` |
| شیء annotated tag | `cd2a33f7c977e752d3afec6a1ac1e31c36f170cf` |
| hash کل distribution | `dfa901f3c1bbb9fe54c4ee69ca043fbd217c21435236c32a453c747d2d58eb7b` |
| hash فایل manifest | `68a965cdeaa8c93abf363e0e017d840ec65e3229ba467036408d13e00df9c64b` |

ریموت main و مقصد نهایی tag از GitHub خوانده و با کامیت محلی مقایسه شدند. push معمولی بود؛ force، جابه‌جایی tag قبلی یا تغییر branch protection انجام نشد. working tree تمیز است. tag شیء مستقل از نوع `tag` دارد و به کامیت بالا resolve می‌شود. GitHub Release object ساخته نشد؛ انتشار نسخه با annotated tag انجام شد.

| موضوع | پیش از اصلاح | پس از اصلاح |
|---|---|---|
| CLI و مدل | Homebrew 0.142.5، کاتالوگ قدیمی و خطای model_not_found؛ هشدار سازگاری cache | باینری رسمی همراه برنامه 0.167.0-alpha.3.2، مدل صریح gpt-6.1-sol و ورود ChatGPT؛ پاسخ واقعی مدل و خواندن واقعی فایل ثبت شد |
| تست UI | ۱۳۰ تست واقعی موفق و دو placeholder ناشی از خطای import؛ discovery برابر ۱۳۲ | ۱۵۳ تست اصلی واقعاً اجرا و پاس شدند؛ صفر failure، error و skip؛ ۵ تست launcher و دروازهٔ relevance با ۹۰ کیس نیز پاس شدند |
| ویندوز | شواهد تازهٔ runtime وجود نداشت؛ probe قدیمی PID برای ویندوز ناامن بود | probe فقط‌خواندنی Win32، محافظ مسیر و بازیابی اصلاح شدند؛ CI کامل Windows Server 2025 و هر دو PowerShell موفق شدند |
| ۱۲ مورد routing تاریخی | ۱۲ مجموعهٔ خواندن ناقص در بررسی delegated | A=0، B=7، C=5، D=0؛ تغییر سیاست اسکیل لازم تشخیص داده نشد؛ نتایج تاریخی بازنویسی نشدند |

## تست‌های واقعی و محدودهٔ آن‌ها

[CI موفق روی کامیت نهایی](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) و [اجرای موفقِ خود tag](https://github.com/MahanManouchehri/skill-package/actions/runs/43765443386) روی Windows Server 2025، نسخهٔ 10.0.26100، با Python 3.12.10 اجرا شد:

| مجموعه | اجرا / موفق | خطا / skip |
|---|---:|---:|
| Package tools و transaction/recovery | ۵۷ / ۵۷ | ۰ / ۰ |
| Runner helpers | ۲۷ / ۲۷ | ۰ / ۰ |
| کل تست‌های اصلی UI | ۱۵۳ / ۱۵۳ | ۰ / ۰ |
| Launcherهای authoring | ۵ / ۵ | ۰ / ۰ |
| فایل‌سیستم واقعی ویندوز: junction، فایل قفل‌شده و مسیر بلند | ۴ / ۴ | ۰ / ۰ |
| PowerShell 5.1.26100.33648 | parser هر شش اسکریپت و کل fixture موفق | بدون خطای اجرا |
| PowerShell 7.6.9 | parser هر شش اسکریپت و کل fixture موفق | بدون خطای اجرا |

همین مجموعه‌های مستقل Python، به‌جز چهار تست مخصوص ویندوز، روی macOS 26.2 با Python 3.14.2 و PyYAML 6.0.3 نیز پاس شدند. validator فعلی رسمی، هر ۲۶ اسکیل را تأیید کرد. تست catalog آفلاین ۱۱/۱۱ و smoke جست‌وجو، مسیر و cwd برابر ۱۳/۱۳ موفق بود. دروازهٔ frozen relevance با همان threshold و fingerprintهای قدیمی، ۹۰ کیس را ارزیابی و پاس کرد؛ این نتیجه تأیید هدف کیفیت جدید یا پاسخ بی‌نقص تک‌تک جست‌وجوها نیست.

سناریوهای PowerShell فقط در پروفایل‌های یکتای موقت runner اجرا شدند: نصب، تأیید ۲۶ اسکیل، تکرار نصب بدون تغییر فایل یا بکاپ، بکاپ با hash، rollback خطای تزریق‌شده، inventory، مسیر فارسی و کاراکترهای ویژه، CODEX_HOME، USERPROFILE، dry-run مسیر .agents و رد واقعی SUBST. هیچ پروفایل واقعی کاربر روی ویندوز هدف نبود.

چهار CI ناموفق اولیه حفظ شده‌اند: خطای context در workflow پیش از شروع runner؛ تشخیص نادرست `..` در لینک معتبر؛ پاک‌سازی Git object فقط‌خواندنی در fixture؛ و اشکالات نمایش مسیر/CWD و فرض نادرست fixture دربارهٔ گزارش نصب اولیه. همه اصلاح و دوباره اجرا شدند. هیچ تست یا assertion حذف، skip یا ضعیف نشد. تست تکرار نصب، ساختار کامل پوشه‌ها و فایل‌ها و hash همهٔ بکاپ‌ها را قبل و بعد مقایسه می‌کند.

وضعیت‌های ویندوز: **STATIC_REVIEWED، CROSS_PLATFORM_TESTED، POWERSHELL_PARSED و WINDOWS_CI_PASS**. این شواهد به محیط ثبت‌شده محدود است؛ Windows PC کاربر، SMB/UNC واقعی، ACLهای دلخواه، انواع antivirus، قطع برق و همهٔ فایل‌سیستم‌ها آزمایش نشده‌اند. نصب PowerShell مستقل برای درایو ثابت محلی است و alias، SUBST و UNC را رد می‌کند؛ ابزار Python محدودیت‌های جداگانهٔ مستند دارد.

## شواهد native و موارد تأییدنشده

مسیر دقیق CLI:
`/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex`

مدل درخواست‌شده `gpt-6.1-sol` و effort سناریوهای بانک `medium` بود. فرمان پیش‌فرض Homebrew ارتقا یا جایگزین نشد. `login status` رسمی، ورود ChatGPT را تأیید کرد؛ harness فایل احراز هویت را باز یا کپی نکرد. فهرست مدلِ محلی با turn واقعی موفق تأیید شد؛ دسترسی مدل صرفاً از روی کاتالوگ نتیجه‌گیری نشده است. تغییر اسکیل، مجوز مدل ایجاد نکرده است.

از ۶۰ سناریوی اصلی، **۱۲ مورد تلاش شد: ۱۰ turn کامل، دو توقف بر اثر سقف مصرف و ۴۸ مورد اجرا‌نشده**. بررسی مستقلِ تمام ۶۸ فرمان ثبت‌شده، هشت برنامه را در محدودهٔ READ_ONLY_ROUTING_PLAN قابل‌قبول دانست. S07 و S12 فایل compatible-response را از مسیر نصب کاربر خواندند؛ محتوای ثبت‌شده با fixture یکسان است، اما این دو مورد **FAIL جداسازی مسیر** باقی مانده‌اند. S04 و S21 به‌دلیل پیام usage limit، **BLOCKED/UNVERIFIED** هستند.

چهار تلاش اولیه با محافظ اضافی macOS، به‌علت ممنوعیت sandbox تو‌در‌تو امکان خواندن فایل نداشتند و جداگانه نگهداری شدند. پنج probe کمکی smoke/tool جزو ۶۰ سناریو شمرده نشده‌اند. مدل جایگزین برای عبور از سقف مصرف استفاده نشد و retry خودکار انجام نشد. [جدول هر ۱۲ سناریو و اسکیل‌های واقعاً خوانده‌شده](native-cases.csv).

پس از بررسی، fixture به نسخهٔ محلی اسکیل‌ها ارجاع می‌دهد؛ خواندن شناخته‌شده از مسیر بیرونی و تغییر فایل fixture باعث FAIL می‌شود. این اصلاحات تست helper دارند، اما پس از سقف مصرف، native دوباره اجرا نشده است. فهرست فعال اسکیل‌ها با محدودیت filesystem برای خواندن یکسان نیست؛ فرمان‌های پیچیده همچنان به بررسی raw trace نیاز دارند. تمام ۶۰ نتیجهٔ پذیرش کامل برنامه، مرورگر، provider یا production **UNVERIFIED** است؛ این‌ها برنامه‌ریزی فقط‌خواندنی‌اند.

## ابزارهای UI، مجوز و فایل‌های تغییرکرده

پیاده‌سازی واقعی ابزارها از [upstream در commit 6ae86f6](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/6ae86f61f520d6ca229d2f40e070410638c908c5) بازیابی و با Git blob و SHA256 تطبیق داده شد؛ متن MIT حفظ شده است. ابزارهای authoring در scripts ریشه‌اند و جزو payload نصب اسکیل نیستند. launcher نسخهٔ دست‌نخوردهٔ grader را در checkout موقت canonical با کپی دقیق بایت‌ها اجرا می‌کند. fixture، threshold، fingerprint و assertionهای قدیمی تغییر نکرده‌اند؛ هر ۷۰ فایل UI با مبنا یکسان است. Django stack اختصاصی ندارد؛ رد صریح و fallback عمومی UX تست شدند.

| فایل یا گروه | علت تغییر |
|---|---|
| `evals/run.py` و `evals/test_runner.py` | preflight صریح، discovery قابل‌حمل، فهرست دقیق ۲۶ اسکیل، تشخیص خواندن بیرونی و تغییر fixture؛ ۱۴ تست قبلی حفظ شدند |
| `scripts/package_tools.py` و تست‌های آن | liveness امن ویندوز، مسیرها، UTF-8، بازیابی و پاک‌سازی scratch مجاز؛ ۱۳ تست جدید |
| `scripts/common.ps1`، `install.ps1` و driverهای Windows | هویت درایو، منع alias/overlap و تست واقعی نصب/بکاپ/rollback در temp |
| ابزارهای ریشهٔ UI، vendor، license و provenance | بازگرداندن authoring واقعی و اجرای oracle اصلی بدون تغییر payload |
| `.github/workflows/windows-validation.yml` | actionهای رسمی pin‌شده، temp اجباری و همهٔ دروازه‌های واقعی Windows |
| `evals/evidence/v3.1.1/` | traceهای خام، خطاهای حفظ‌شده، adjudication و شواهد جدید؛ داده‌های قدیمی دست‌نخورده‌اند |
| VERSION، manifest، integrity و مستندات | patch 3.1.1، hashهای کامل و شرح دقیق تست‌ها و محدودیت‌ها |

[فهرست کامل ۲۳۵ فایل تغییرکرده، علت هرکدام و hash](changed-files.json). Commitهای میانی خطاها را پنهان نمی‌کنند؛ نسخهٔ نهایی با CI موفق همان SHA منتشر شده است.

## نصب و حفظ داده‌ها

payload هر ۲۶ اسکیل با مبنا یکسان است. درخت نصب هر ۲۶ مورد با manifest کامیت منتشرشده تطبیق داده شد: ۲۳ مورد در `/Users/mahan/.codex/skills` و سه مورد در `/Users/mahan/.agents/skills`. discovery واقعی نیز ۲۶ نام یکتا و فعال نشان داد. وضعیت نصب **NO_REINSTALL_NEEDED** است؛ نصب مجدد، جابه‌جایی پوشه یا بکاپ تازه انجام نشد. installer رسمی جایگزین یا دور زده نشد؛ طبق شرط صریح دستورکار، برای payload یکسان اجرا نشد.

هر ۱۶ رکورد managed، پنج system exclusion، schema 1، بانک اصلی ۶۰ سناریو و همهٔ شواهد قبلی حفظ شده‌اند. ۶۲۵ فایل محافظت‌شده تغییر نکرده‌اند. hash بانک `701e40e161d8f76848b04618857d46ea8f52b6f456eb7be82fa87944c7ee1706` و digest payload برابر `485af03ae334b09f1d8646fff62c4af47b1373541a4c14459d09b9c550c82a97` است. تمام ۸۶۹ فایل distribution با integrity تطبیق دارند؛ خود integrity و .git در aggregate نیستند. `git diff --check` پاس است و اسکن قواعد موجود secrets هیچ موردی گزارش نکرد.

فایل auth/config و مسیرهای اسکیل یا plugin به‌صورت دستی تغییر نکردند. hash کش مدل در جریان استفادهٔ runtime تغییر کرد؛ کش حذف، بازنویسی یا به نسخهٔ قبلی برگردانده نشد. بکاپ‌های قبلی و اسکیل‌های نامرتبط حفظ شدند. هیچ managed/system/plugin snapshot جدیدی نصب یا از مسیر زنده کپی نشد.

[رسید انتشار و نصب](receipt.json) · [discovery نصب](installed-discovery.json) · [ممیزی نهایی](final-check.md)
