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
