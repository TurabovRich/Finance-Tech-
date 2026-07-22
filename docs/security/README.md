# Clarity — Security

Production-grade security from day one. We handle financial identity data — treat every environment like it could go live tomorrow.

## V1 requirements

- [x] JWT access tokens with short expiry
- [x] Refresh tokens: opaque, hashed at rest (SHA-256), revocable, expire after `REFRESH_TOKEN_EXPIRE_DAYS`
- [x] Every protected endpoint scoped by authenticated `user_id` (JWT-derived, never client-supplied)
- [ ] PIN hashed with bcrypt (hashing implemented; persistence to `users.pin_hash` still open)
- [ ] Secrets in `.env` / secret manager, never committed
- [ ] HTTPS in production
- [ ] Rate limit auth endpoints
- [ ] No raw card numbers stored (last_four only)
- [ ] OTP via certified SMS provider in production

## Threat model (draft)

| Threat | Mitigation |
|--------|------------|
| Brute-force OTP | Not yet mitigated — rate limiting/lockout still open (tracked in backlog) |
| Token theft (access token) | Secure storage on mobile (planned), short TTL (30 min default) |
| Token theft (refresh token) | Stored server-side only as a SHA-256 hash; revocable via `/auth/logout` or `/auth/sessions/{id}/revoke`; **not rotated on use** — see tradeoff below |
| SQL injection | SQLAlchemy ORM, parameterized queries |
| IDOR | Every cards/categories/insights/transactions endpoint derives `user_id` from the JWT via `get_current_user_id`, never from client input |
| Compromised device | `GET /auth/sessions` + `POST /auth/sessions/{id}/revoke` let a user list and kill any session by device/IP without knowing its refresh token |

### Recorded tradeoff: no refresh-token rotation yet
OAuth2-style rotation (issue a new refresh token on every use, invalidate the old
one, and treat reuse of a burned token as a signal of theft) gives stronger
compromise detection than what's implemented. It also requires tracking token
"families" and handling concurrent-refresh races correctly. V1 ships a simpler
model — one long-lived, revocable, hashed refresh token per session — which closes
the "no way to log out or revoke at all" gap without that added complexity.
Revisit once there's real usage to justify it.

## Documents to add

- `threat-model.md`
- `security-requirements.md`
