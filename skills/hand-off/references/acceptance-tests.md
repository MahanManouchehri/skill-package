# Skill Acceptance Tests (eval design; not evidence of running)

## Routing tests

| User request | Expected mode |
|---|---|
| `$hand-off Ticketing` | HANDOFF, two documents |
| `کل Authentication این پروژه رو توضیح بده` | HANDOFF, two documents |
| `چه متدی این ServiceProvider رو صدا می‌زنه؟` | EXPLAIN, chat only |
| `ارتباط Controller و Event رو در Support توضیح بده` | EXPLORE, chat only |
| `Hand-off قبلی Support رو با سورس جدید تطبیق بده` | REFRESH, merge-safe docs |
| `ServiceProvider در Laravel چیست؟` | no hand-off: generic theory |
| `یک endpoint ایجاد کن` | no hand-off: implementation only |
| `با سورس ناموجود، این ماژول رو کامل توضیح بده` | limited answer, no invented source |

## Content tests on real Laravel and Django projects

- Central method has exact definition location, verifiable call site and binding/registration if indirect.
- Trace reaches persisted state/response; optional/dynamic paths labeled honestly.
- Auth/validation/error/transactions/event/queue treatment accurate for the real implementation.
- Three feasible independent development recipes, or fewer with explicit feature-specific rationale.
- LLM context allows another model to identify correct **documented** files without falsely claiming live repo access.
- Source tree unchanged; exported docs contain no credentials.
- Re-running installer does not duplicate global marker or change `compatible-response`.
- Refresh with dirty Git and manual sections preserves non-generated text.

Failures should be recorded with prompt, repository revision, expected behavior, observed behavior, and concrete correction; do not label acceptance passed until actually tested.
