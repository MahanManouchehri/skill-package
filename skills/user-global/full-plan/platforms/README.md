# پلتفرم‌ها و منبع حقیقت

<div dir="rtl">

رفتار اصلی Full Plan در `SKILL.md` ریشه تعریف شده است. فایل‌های این پوشه adapter هستند: هرکدام همان قرارداد رفتاری را در قالب قابل استفادهٔ پلتفرم هدف ارائه می‌کند.

هنگام تغییر رفتار اصلی، `SKILL.md` ریشه و adapter مربوطه را با هم بررسی کنید. adapter نباید قانون تازه‌ای بسازد یا اجازهٔ شروع پیاده‌سازی بدون تأیید صریح کاربر بدهد.

| مسیر | کاربرد |
| --- | --- |
| `chatgpt-skill/` | بستهٔ قابل upload برای قابلیت Skills در ChatGPT |
| `chatgpt-custom-gpt/` | Instructions قابل paste در Custom GPT |
| `claude-code/` | فرمان پروژه‌ای `/full-plan` برای Claude Code |
| `claude-web/` | Project Instructions برای Claude Web |

راهنمای انتخاب، نصب و محدودیت هر مسیر در [سازگاری پلتفرم‌ها](../docs/PLATFORM-COMPATIBILITY.md) قرار دارد.

</div>
