# SECRET_KEY security guide

This document explains secure practices for generating, storing, rotating, and deploying the Django `SECRET_KEY` for this project.

Why this matters
- `SECRET_KEY` is used by Django for cryptographic signing (cookies, CSRF tokens, password reset tokens, etc.). If leaked or predictable, it allows attackers to forge signed data.

Generate a strong key
- Use a secure random generator. Examples:
  - Python (one-off):
    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```
  - OpenSSL (one-off):
    ```bash
    openssl rand -base64 48
    ```
  - PowerShell (one-off):
    ```powershell
    Add-Type -AssemblyName System.Web
    [System.Web.Security.Membership]::GeneratePassword(50,10)
    ```

Local development (safe convenience)
- For local development you can put a `.env` file at the project root with:
  ```text
  SECRET_KEY="your-generated-secret"
  ```
- Ensure `.env` is in `.gitignore` (do not commit secrets).
- The project supports loading `.env` via `python-dotenv`.

Production (recommended)
- Never store `SECRET_KEY` in source control.
- Use your platform's secrets management service. Examples:
  - Heroku: `heroku config:set SECRET_KEY=...`
  - Linux systemd unit / environment variables
  - Docker secrets or Kubernetes Secrets
  - Cloud provider secrets:
    - AWS Secrets Manager / Parameter Store
    - Azure Key Vault
    - GCP Secret Manager

Examples — set SECRET_KEY in environment
- PowerShell (temporary for session):
  ```powershell
  $env:SECRET_KEY = 'your-secret-here'
  python manage.py runserver
  ```
- systemd service unit (production):
  ```ini
  [Service]
  Environment="SECRET_KEY=your-secret-here"
  ```
- Docker (docker-compose):
  ```yaml
  services:
    web:
      image: myapp:latest
      environment:
        - SECRET_KEY=${SECRET_KEY}
      secrets:
        - secret_key
  secrets:
    secret_key:
      file: ./secrets/secret_key.txt
  ```

CI / Deployment pipelines
- Use your CI/CD provider's secret storage rather than checking secrets into the repo.
- Example (GitHub Actions):
  ```yaml
  env:
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
  ```

Rotation and revocation
- Plan a rotation strategy: update secret in secret manager, deploy code using the new secret, and invalidate sessions if needed.
- If SECRET_KEY is leaked: rotate immediately and force session invalidation by changing the key (users will be logged out).

Testing and debugging
- For local experimentation you may use a `.env` file. Never use the same key in production and public repos.

Additional tips
- If you run multiple Django instances that must share signed cookies, ensure they share the same SECRET_KEY.
- Consider using a dedicated secret for cookies/tokens rather than sharing unrelated secrets.

Questions? Ask here and I can add platform-specific snippets for AWS/GCP/Azure, or create automation scripts to manage secrets for your deployment.