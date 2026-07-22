# Clarity — Product Vision

**Clarity** is a real fintech product for Uzbekistan — not a demo, not a tutorial app.

PayMe, Click, and PayNet won by making payments easy. Clarity wins by making **spending understandable**: where money goes, how habits change month to month, and what to do next — inside an app people already trust with their cards.

---

## One-liner

> See your money clearly. Pay when you need to — understand it every day.

## The gap we fill

| Incumbents (PayMe, Click, PayNet) | Clarity |
|-----------------------------------|---------|
| Payment-first home screen | Insights-first home screen |
| Transaction list as archive | Categorized spending with trends |
| Super-app marketplace growth | Focused personal finance clarity |
| “Send money” as the hero action | “Understand spending” as the hero action |

We are not replacing wallets. We are the layer that makes every card and every payment **legible**.

## Target user (V1)

- Urban Uzbekistan, 22–35, already uses PayMe or Click for payments
- Has 1–3 cards (Humo/Uzcard), pays utilities and shops online
- Wants to know where salary goes without opening a spreadsheet

## Core pillars

1. **Clarity** — monthly breakdowns, category trends, plain-language summaries
2. **Trust** — bank-grade security, no dark patterns, transparent fees
3. **Speed** — sub-second insights, offline-friendly cached views
4. **Local** — UZS/tiyin, uz/ru locale, Humo/Uzcard/Visa support

## V1 — Launch scope

| Ship | Defer |
|------|-------|
| Phone OTP auth + PIN | Biometric login |
| Link cards (Humo/Uzcard/Visa) | Direct bank API (phase 2) |
| Auto-categorized transaction feed | Manual merchant rules engine |
| Monthly insights dashboard | Budgets & alerts |
| User custom categories | Shared family accounts |

## V2 — Growth

- Budget targets per category with push alerts
- Recurring payment detection (“you pay Beeline every month”)
- Export for tax / business expenses
- Merchant enrichment (logos, cleaner names)

## V3 — Scale

- Open banking / aggregator partnerships
- B2B white-label for banks
- Credit insights (with licensed partners)
- Regional expansion (KZ, KG)

## Success metrics (12 months post-launch)

| Metric | Target |
|--------|--------|
| MAU | 100k |
| D7 retention | > 40% |
| Cards linked per user | ≥ 1.5 |
| Weekly insights opens | > 3× / active user |
| NPS | > 50 |

## What we are building right now

```
mobile (Flutter)  →  API (FastAPI)  →  PostgreSQL
     │                    │
     └── insights home    └── categories + monthly aggregates
```

Current milestone: **wire Insights home to live API data** and ship a credible first-run experience after login.

## Principles (non-negotiable)

1. Amounts stored as **integers in tiyin** — never floats
2. No raw PAN — last four digits only
3. Every query scoped to authenticated `user_id`
4. Document every major product and architecture decision in `docs/`
