# Clarity — Security

Production-grade security from day one. We handle financial identity data — treat every environment like it could go live tomorrow.

## V1 requirements

- [ ] JWT access tokens with short expiry
- [ ] PIN hashed with bcrypt
- [ ] Secrets in `.env` / secret manager, never committed
- [ ] HTTPS in production
- [ ] Rate limit auth endpoints
- [ ] No raw card numbers stored (last_four only)
- [ ] OTP via certified SMS provider in production

## Threat model (draft)

| Threat | Mitigation |
|--------|------------|
| Brute-force OTP | Rate limiting, lockout, SMS provider throttling |
| Token theft | Secure storage on mobile, short TTL, refresh rotation |
| SQL injection | SQLAlchemy ORM, parameterized queries |
| IDOR | Always scope queries by authenticated user_id |

## Documents to add

- `threat-model.md`
- `security-requirements.md`
