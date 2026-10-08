# راهنمای توسعه مستقل — {{FEATURE_NAME}}

> **Snapshot:** Repository: `{{REPO}}` | Branch: `{{BRANCH}}` | HEAD: `{{COMMIT}}` | Working tree: `{{DIRTY_STATUS}}` | Analyzed at: `{{DATE_TIMEZONE}}`
>
> **Scope:** {{IN_SCOPE}} | **Exclusions:** {{OUT_OF_SCOPE}} | **Overall coverage:** {{VERIFIED_OR_PARTIAL}}

<!-- Content above/below is generated unless inside a MANUAL block. On refresh, preserve manually authored prose as well. -->

## ۱. شروع سریع و ترتیب مطالعه

- مسئولیت واقعی فیچر و هدف کاربر، در ۲–۴ جمله.
- اول چه فایلی باز شود و چرا: `path:Lx-Ly`.
- ترتیب خواندن چند فایل مرکزی با دلیل.
- مسیر اصلی اجرا در یک Call Chain کوتاه.

## ۲. محدوده و نقشه معماری

- نقاط ورود واقعی و مرز بین `CORE`، `RELATED` و `BOUNDARY`.
- Component graph فقط با رابطه‌های تأییدشده؛ اگر Mermaid مفید است از آن استفاده کن.
- Registrationها و wiringهای خارجی به‌طور روشن برچسب‌گذاری شوند.

## ۳. File & Symbol Atlas

| فایل + خط | Symbol / Signature | نقش | Called by / Registration | Calls / Dependency | اثر و نقطه تغییر |
|---|---|---|---|---|---|
| `path:Lx-Ly` | `ExactSymbol()` | ... | `caller path:Lx` | `callee path:Ly` | ... |

برای Symbolهای بحرانی توضیح بده ورودی/خروجی، شاخه‌های اصلی، مرزهای مجوز و تأثیر تغییر آن چیست. تعریف + محل فراخوانی هر Edge مهم باید مستند باشد.

## ۴. Execution Walkthrough

برای هر سناریوی اصلی و خطاهای مهم:
1. Trigger و Registration + Evidence.
2. Controller/Handler + Validation/Authorization.
3. Calls، شرط‌ها، DI و State changes.
4. Persistence/Transaction/Cache/Event/Job/External side effect، به ترتیب واقعی.
5. Response یا Outcome؛ failure branches/exception handling.

## ۵. Technical Contracts

- API input/output/status codes (only observed facts).
- مدل/جدول/رابطه/Query و قواعد تغییر State.
- Authorization، Validation و قواعد ممنوعیت.
- Sync/Async order، idempotency/concurrency و خطاها (اگر مرتبط).
- قواعد معماری: `SOURCE_VERIFIED` از `DOCUMENTED` و `INFERRED` جدا باشد.

## ۶. Architecture Decisions & Invariants

| قاعده/تصمیم | شواهد | الزام یا تفسیر | اثر شکستن |
|---|---|---|---|

## ۷. Independent Development Playbook

برای هر تغییر واقعی یا محتمل (هدف: سه سناریوی مستقل در صورت کاربرد):
1. Goal و رفتار فعلی.
2. `Primary Edit` (فایل + متد + علت).
3. `Dependent Edit` و `Verify Only` همراه با دلیل.
4. مراحل فنی، Invariantها و اثر تغییر API/DB/Events.
5. تست‌ها/ابزار دیباگ، معیار پذیرش و راه بازگشت ایمن.

## ۸. Debugging Playbook

| نشانه | اولین نقطه | Breakpoint/Log/State | فرضیه با برچسب شواهد | روش ابطال یا تأیید |
|---|---|---|---|---|

## ۹. Testing & Manual Verification

- `Existing Tests`: مسیر و Assertionهای واقعی.
- `Missing Tests`: شکاف‌های مشخص، بدون ادعای وجودشان در repo.
- `Verification`: دستورهای مناسب و پیش‌نیاز/اثر جانبی، وضعیت `NOT RUN` یا دقیقاً اجراشده.
- جست‌وجوهای مفید IDE / `rg` برای یافتن caller، symbol و binding.

## ۱۰. Coverage, Unknowns, Freshness

| بُعد | Verified / Partial / Unknown / N/A | مدرک / شکاف / مرحله بعد |
|---|---|---|
| Entry Points | ... | ... |
| Main & Error Flows | ... | ... |
| Dependencies | ... | ... |
| State & Persistence | ... | ... |
| Validation & Authorization | ... | ... |
| Async & External | ... | ... |
| Change Impact | ... | ... |
| Tests & Debugging | ... | ... |

- موارد unresolved با اثر واقعی و مسیر پیگیری.
- تغییرات مؤثر از snapshot؛ چه زمانی باید `REFRESH` انجام شود.

## ۱۱. Independent Development Readiness

- [ ] فایل شروع هر سناریوی اصلی مشخص است.
- [ ] تعریف و Call Site متدهای کلیدی قابل یافتن هستند.
- [ ] اولین نقطه تغییر، مصرف‌کنندگان و Invariantها مشخص‌اند.
- [ ] مسیر دیباگ و تستِ متناسب با رفتار وجود دارد.
- [ ] ابهامات جدی به‌صراحت گزارش شده‌اند.

## یادداشت‌های توسعه‌دهنده (حفظ در REFRESH)

<!-- HAND-OFF:MANUAL:BEGIN -->
<!-- Add your own comments here. This section must survive refresh unchanged. -->
<!-- HAND-OFF:MANUAL:END -->
