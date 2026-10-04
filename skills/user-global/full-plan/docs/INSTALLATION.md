# نصب و به‌روزرسانی

<div dir="rtl">

## پیش‌نیاز

- نصب بودن Git
- دسترسی نوشتن به پوشهٔ سراسری Codex

## نصب سراسری در Windows

مسیر پیش‌فرض Skillهای شخصی Codex در Windows این است:

```text
C:\Users\<your-user>\.codex\skills
```

برای نصب، این دستور را با نام کاربری Windows خود اجرا کنید:

```powershell
git clone https://github.com/MahanManouchehri/full-plan.git "C:\Users\<your-user>\.codex\skills\full-plan"
```

اگر پوشهٔ مقصد از قبل وجود دارد، آن را overwrite نکنید. ابتدا محتوای آن را بررسی کنید؛ ممکن است نسخه‌ای محلی با تغییرات شخصی داشته باشید.

پس از نصب، task جدیدی در Codex باز کنید تا metadata اسکیل دوباره خوانده شود.

## به‌روزرسانی

اگر Skill از همین مخزن نصب شده و تغییر محلی مهمی ندارید:

```powershell
git -C "C:\Users\<your-user>\.codex\skills\full-plan" pull --ff-only
```

گزینهٔ `--ff-only` از ایجاد merge commit ناخواسته جلوگیری می‌کند. اگر فرمان متوقف شد، ابتدا تغییرات محلی را بررسی و سپس دربارهٔ حفظ یا کنارگذاشتن آن‌ها تصمیم بگیرید.

## نصب در پروژه‌ای که AGENTS.md دارد

فقط نصب Skill، الزام استفاده از آن را در یک پروژه ایجاد نمی‌کند. برای فعال‌سازی خودکار در پروژه، در `AGENTS.md` بنویسید که پیش از طراحی یا پیاده‌سازی فیچر APIمحور، `full-plan` اجرا شود و تا تأیید کاربر، کدنویسی آغاز نشود.

اگر Skill در مسیر سراسری نبود، می‌توانید در همان دستورالعمل، مخزن رسمی این پروژه را به‌عنوان منبع بازیابی معرفی کنید:

```text
https://github.com/MahanManouchehri/full-plan
```

</div>
