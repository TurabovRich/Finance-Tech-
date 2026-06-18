# Clarity — Security

Educational simulation — still practice production habits.

## V1 requirements

- [ ] JWT access tokens with short expiry
- [ ] PIN hashed with bcrypt
- [ ] Secrets in `.env`, never committed
- [ ] HTTPS in production
- [ ] Rate limit auth endpoints
- [ ] No raw card numbers stored (last_four only)

## Threat model (draft)

| Threat | Mitigation |
|--------|------------|
| Brute-force OTP | Rate limiting, lockout |
| Token theft | Secure storage on mobile, short TTL |
| SQL injection | SQLAlchemy ORM, parameterized queries |
| IDOR | Always scope queries by authenticated user_id |

## Documents to add

- `threat-model.md`
- `security-requirements.md`
