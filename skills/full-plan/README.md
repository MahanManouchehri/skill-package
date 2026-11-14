# Full Plan

<div dir="rtl">

`full-plan` یک Skill برای Codex است که پیش از پیاده‌سازی رفتار معنادار، بازیگرها، قواعد، حالت‌های خطا، معیار پذیرش و سناریوهای واقعی را به فارسی روشن و فنی آماده می‌کند؛ اگر API لازم باشد، قرارداد دقیق endpointها را هم می‌نویسد.

هدف این است که پیش از تغییر کد، همهٔ افراد درگیر بدانند هر endpoint چه ورودی می‌گیرد، چه رفتاری دارد، چه پاسخی برمی‌گرداند و در کدام گام از جریان کار استفاده می‌شود.

## قابلیت‌ها

- انتخاب متناسب با نیاز برای طراحی رفتار، جریان کار و فیچرهای APIمحور
- اجرای صریح با عبارت `/full-plan`
- تفکیک endpointهای موجود، پیشنهادی و نیازمند تصمیم
- نمایش دقیق ورودی‌ها، اعتبارسنجی، مجوزها، رفتار، پاسخ موفق و خطاهای قابل انتظار
- تبدیل endpointها به سناریوهای مرتب و قابل اجرا برای هر نقش کاربری
- نگارش فارسی رسمی، طبیعی و مناسب مستندات فنی
- توقف فقط برای تصمیم مهم حل‌نشده یا عملیات نیازمند تأیید طبق قواعد پروژه؛ ادامهٔ تغییر معمول و مجاز بدون تأیید تکراری

## ساختار مخزن

```text
.
├── SKILL.md                 # دستورالعمل اصلی Skill با نام full-plan
├── agents/openai.yaml       # نام و توضیح نمایشی Skill
├── docs/
│   ├── INSTALLATION.md       # نصب و به‌روزرسانی سراسری
│   ├── PLATFORM-COMPATIBILITY.md # سازگاری و نصب پلتفرم‌ها
│   ├── USAGE.md              # روش استفاده و الگوی خروجی
│   └── OUTPUT-FORMAT.md      # قالب جزئی قرارداد endpoint و سناریو
├── platforms/                 # adapterهای ChatGPT و Claude
├── CHANGELOG.md              # تغییرات نسخه‌ها
├── CONTRIBUTING.md           # راهنمای مشارکت
└── LICENSE                   # مجوز MIT
```

## نصب سریع

برای نصب سراسری در Windows، در PowerShell اجرا کنید:

```powershell
git clone https://github.com/MahanManouchehri/full-plan.git "C:\Users\<your-user>\.codex\skills\full-plan"
```

پس از نصب، یک task جدید باز کنید تا Codex فهرست Skillها را دوباره بارگذاری کند. جزئیات نصب، به‌روزرسانی و رفع تداخل در [راهنمای نصب](docs/INSTALLATION.md) آمده است.

## شروع استفاده

برای اجرای صریح، در درخواست خود بنویسید:

```text
/full-plan
```

یا به‌صورت مستقیم از نام Skill استفاده کنید:

```text
$full-plan
```

انتخاب خودکار اسکیل با مدل انجام می‌شود و نصب به‌تنهایی تضمین اجرای همیشگی نیست. در صورت نیاز و با تصمیم خودتان، این قطعهٔ اختیاری را با حفظ دستورهای قبلی در `AGENTS.md` ادغام کنید؛ نصب‌کننده آن فایل را تغییر نمی‌دهد:

```markdown
For meaningful feature/workflow contracts, use `full-plan` proportionately
under `steps`. Respect current user authorization and project governance.
Wait only for unresolved major decisions or separately restricted actions;
do not request ceremonial reapproval of a routine authorized change.
```

راهنمای کامل و نمونهٔ خروجی در [راهنمای استفاده](docs/USAGE.md) و [قالب خروجی](docs/OUTPUT-FORMAT.md) قرار دارد.

## ChatGPT و Claude

adapterهای قدیمی Custom GPT، Claude Code و Claude Web برای حفظ منابع قبلی باقی مانده‌اند. هدف این نسخه و مسیر نصب این پکیج Codex است؛ این فایل‌ها مدرک دسترسی یا سازگاری فعلی سرویس‌های دیگر نیستند. جزئیات منابع موجود در [راهنمای سازگاری](docs/PLATFORM-COMPATIBILITY.md) آمده است.

## دامنه

این Skill برای قرارداد رفتار و جریان‌های معنادار مناسب است، چه API داشته باشند و چه از UI یا job شروع شوند. برای refactor داخلی کوچک، اصلاح تایپی یا تغییر ظاهری محدود، طرح کامل بی‌دلیل نسازید.

## مشارکت

پیشنهاد، گزارش ایراد و pull request خوش‌آمد است. پیش از ارسال تغییر، [راهنمای مشارکت](CONTRIBUTING.md) را بخوانید.

## مجوز

این پروژه تحت [مجوز MIT](LICENSE) منتشر شده است.

</div>
