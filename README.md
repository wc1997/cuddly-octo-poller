# cuddly-octo-poller
Experimentation for IBKR API aggregation 

## IBKR Client Portal (REST API)

This repo now includes a Docker Compose setup for IBKR Gateway (TWS API).

### Files

- `docker-compose.tws.yml`
- `.env.example`

### Run

1. Create your env file and add IBKR credentials:

	```bash
	cp .env.example .env
	```

2. Start IB Gateway:

	```bash
	docker compose -f docker-compose.tws.yml up -d
	```

3. TWS socket is available on:

	```text
	127.0.0.1:4002
	```

4. Login to TWS via VNC

    ```text
    open vnc://localhost:5900
    ```
### Notes

- `config/config.default.yml` now defaults to TWS config keys:
	`twsHost`, `twsPort`, and `clientId`.
- Port `5900` is exposed for VNC troubleshooting/login workflows.
- Complete any IBKR 2FA/login prompts if required after container start.
- Keep real IBKR secrets/credentials out of git.

## Example: Query AAPL via TWS API

Use this minimal example script:

- `services/examples/aapl_tws_quote.py`

Install dependencies:

```bash
pip install -r services/examples/requirements.txt
```

Run with defaults (`127.0.0.1:4002`, `clientId=101`):

```bash
python services/examples/aapl_tws_quote.py
```

Or override connection settings:

```bash
IBKR_HOST=127.0.0.1 IBKR_PORT=4002 IBKR_CLIENT_ID=101 python services/examples/aapl_tws_quote.py
```

## Securing .env Secrets

Use this baseline for API keys and passwords:

1. Keep only placeholders in `.env.example`.
2. Store real secrets only in local `.env`.
3. Restrict file permissions so only your user can read it:

```bash
chmod 600 .env
```

4. Never echo secrets in logs or screenshots.
5. Rotate credentials immediately if they were exposed.

Optional but recommended:

- Add a pre-commit secret scanner such as gitleaks or detect-secrets.
- Use a secrets manager for non-local environments (1Password, Doppler, AWS Secrets Manager, Vault).
