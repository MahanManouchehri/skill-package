# Full Plan

<div dir="rtl">

`full-plan` یک Skill سراسری برای Codex است که پیش از پیاده‌سازی فیچرهای APIمحور، قرارداد endpointها و سناریوهای واقعی استفاده از آن‌ها را به فارسی روشن و فنی آماده می‌کند.

هدف این است که پیش از تغییر کد، همهٔ افراد درگیر بدانند هر endpoint چه ورودی می‌گیرد، چه رفتاری دارد، چه پاسخی برمی‌گرداند و در کدام گام از جریان کار استفاده می‌شود.

## قابلیت‌ها

- اجرای خودکار برای طراحی یا پیاده‌سازی فیچرهای APIمحور
- اجرای صریح با عبارت `/full-plan`
- تفکیک endpointهای موجود، پیشنهادی و نیازمند تصمیم
- نمایش دقیق ورودی‌ها، اعتبارسنجی، مجوزها، رفتار، پاسخ موفق و خطاهای قابل انتظار
- تبدیل endpointها به سناریوهای مرتب و قابل اجرا برای هر نقش کاربری
- نگارش فارسی رسمی، طبیعی و مناسب مستندات فنی
- توقف پیش از پیاده‌سازی تا دریافت تأیید صریح کاربر

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

برای اینکه این جریان در یک پروژه اجباری شود، دستورالعمل نمونهٔ زیر را در `AGENTS.md` پروژه یا فایل سراسری Codex اضافه کنید:

```markdown
Before designing or implementing an API-backed feature, load and follow the
global `full-plan` skill. Treat `/full-plan` as an explicit request to
run the complete planning flow, and do not start implementation until the user
has confirmed the plan.
```

راهنمای کامل و نمونهٔ خروجی در [راهنمای استفاده](docs/USAGE.md) و [قالب خروجی](docs/OUTPUT-FORMAT.md) قرار دارد.

## ChatGPT و Claude

این مخزن adapterهای جداگانه برای ChatGPT Skills، ChatGPT Custom GPT، Claude Code و Claude Web دارد. روش درست نصب و محدودیت هر پلتفرم در [راهنمای سازگاری پلتفرم‌ها](docs/PLATFORM-COMPATIBILITY.md) توضیح داده شده است.

## دامنه

این Skill برای فیچرهایی مناسب است که endpoint، قرارداد request/response یا جریان API دارند. برای refactor داخلیِ کوچک یا تغییری که هیچ رفتار API ندارد، نباید به‌صورت بی‌دلیل اجرا شود.

## مشارکت

پیشنهاد، گزارش ایراد و pull request خوش‌آمد است. پیش از ارسال تغییر، [راهنمای مشارکت](CONTRIBUTING.md) را بخوانید.

## مجوز

این پروژه تحت [مجوز MIT](LICENSE) منتشر شده است.

</div>
