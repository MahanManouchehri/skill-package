# سازگاری پلتفرم‌ها

<div dir="rtl">

## انتخاب مسیر درست

| پلتفرم | فایل یا پوشهٔ موردنیاز | روش استفاده | محدودیت مهم |
| --- | --- | --- | --- |
| Codex | `SKILL.md` ریشه | نصب سراسری و استفادهٔ خودکار یا `$full-plan` | برای ظاهرشدن در فهرست، task جدید باز کنید |
| ChatGPT Web عمومی | `platforms/chatgpt-custom-gpt/INSTRUCTIONS.md` | متن را در Instructions یک Custom GPT paste کنید | ساخت Custom GPT به پلن و مجوز حساب وابسته است |
| Claude Code | `platforms/claude-code/commands/full-plan.md` | فایل را در `.claude/commands/full-plan.md` پروژه کپی کنید و سپس `/full-plan` را اجرا کنید | فرمان در همان پروژه فعال است |
| Claude Web | `platforms/claude-web/PROJECT-INSTRUCTIONS.md` | متن را در Project Instructions paste کنید | به همهٔ گفتگوهای همان Project اعمال می‌شود، نه کل حساب |

## دامنهٔ این بسته

این نسخه برای Codex ارزیابی می‌شود. پوشهٔ `platforms/chatgpt-skill/` در این snapshot موجود نیست و archive آماده یا سازگاری فعلی محصولات دیگر تأیید نشده است. adapterهای باقی‌مانده برای حفظ منابع قبلی نگه داشته شده‌اند؛ استفاده در سرویس دیگر به بررسی مستندات و امکانات همان محیط نیاز دارد.

## ChatGPT Custom GPT

یک Custom GPT بسازید، متن `platforms/chatgpt-custom-gpt/INSTRUCTIONS.md` را در بخش Instructions قرار دهید و در Preview یک درخواست APIمحور را آزمایش کنید. Instructions رفتار را کنترل می‌کنند؛ Knowledge فقط برای فایل‌های مرجع پروژه مناسب است.

## Claude Code

در ریشهٔ پروژهٔ Claude Code، پوشهٔ `.claude/commands` را ایجاد کنید و فایل adapter را با نام `full-plan.md` در آن قرار دهید. سپس در همان پروژه فرمان `/full-plan` را اجرا کنید. اگر نسخهٔ Claude Code شما فرمان سفارشی را نمایش نداد، محتوای همان فایل را مستقیماً در گفتگو وارد کنید یا مستندات نسخهٔ نصب‌شدهٔ Claude Code را بررسی کنید.

## Claude Web

در یک Project، بخش Project Instructions را باز کنید و متن adapter را کامل paste کنید. اگر برای طرح به قراردادها یا فایل‌های پروژه نیاز دارید، آن‌ها را جداگانه در Project Knowledge آپلود کنید. Instructions تعیین‌کنندهٔ رفتار هستند و Knowledge فقط منبع اطلاعات است.

## کنترل سازگاری

همهٔ adapterها باید این invariantها را حفظ کنند:

1. ابتدا شواهد مرتبط را بررسی کنند و قرارداد API را حدس نزنند.
2. هر endpoint را با ورودی، رفتار و خروجی دقیق توضیح دهند.
3. سناریوها را به‌ترتیب و بر اساس نقش بنویسند.
4. اختیار فعلی کاربر و دستورهای معتبر را حفظ کنند؛ فقط برای تصمیم مهم حل‌نشده یا اقدام محدودشده توقف کنند، نه برای تأیید دوبارهٔ تغییر معمول و مجاز.

</div>
