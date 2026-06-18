# Clarity — Design Documentation

## Structure

```
design/
├── design-system.md    # colors, typography, spacing
├── user-flows.md       # onboarding, login, insights
└── figma/              # links or exports
```

## Flutter mirror

Each backend module has a matching feature folder under `mobile/lib/features/`:

| Module | Screens |
|--------|---------|
| auth | login, OTP, PIN |
| users | profile |
| cards | list, link card |
| transactions | list, detail |
| categories | list |
| insights | monthly dashboard (home) |
