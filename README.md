# AIC Service Account Access Token Script

This repository provides a simple Python script (`aic-sa-access-token.py`) to automate the OAuth 2.0 JWT‑Bearer flow for obtaining an access token from a PingOne Advanced Identity Cloud (AIC) service account. Instead of manually crafting JWT assertions and cURL commands, this script handles all steps programmatically.

## 🎯 Value Proposition

* **Automation & Efficiency**: Eliminates repetitive manual steps and reduces human error when fetching tokens.
* **Reproducibility**: Guarantees consistent JWT creation and token retrieval across environments.
* **Integration‑Ready**: Scriptable in CI/CD pipelines, build processes, or other automation frameworks.
* **Extensibility**: Easy to adapt for additional parameters, logging, or integration with other tooling.

## 🛠️ Prerequisites

1. **Python 3.7+** installed. Verify with:

   ```bash
   python3 --version
   ```
2. **pip** package manager available. Verify with:

   ```bash
   pip3 --version
   ```
3. Install required Python packages:

   ```bash
   pip3 install requests pyjwt jwcrypto
   ```

## 🔧 Preparing Your AIC Tenant

1. **Log in** to the PingOne Admin Console for your target environment.
2. Navigate to **Service Accounts** and **Create a new service account**. Note:

   * Give it a descriptive name.
   * Enable **JWT Bearer** for OAuth 2.0.
3. Once created:

   * Copy the **Service Account ID** (the GUID under “ID”).
   * **Download** the private key in JWK JSON format. Save it locally (e.g., `service_account_key.jwk`).

## 📁 Repository Layout

```
├── aic-sa-access-token.py   # Main Python script
└── service_account_key.jwk  # Your downloaded JWK file (Gitignored)
```

> **Security Note**: Never commit your JWK file or private keys to source control.

## 🚀 Usage

1. Ensure your JWK file is present and your Python dependencies are installed.

2. Run the script with the required parameters:

   ```bash
   python3 aic-sa-access-token.py \
     --tenant-url https://<your-tenant>.pingone.com \
     --service-account-id <SERVICE_ACCOUNT_ID> \
     --jwk-path ./service_account_key.jwk \
     --client-id service-account \
     --scopes "fr:am:* fr:idm:*"
   ```

3. **Output**:

   * Displays the **raw JSON** response from AIC (including `access_token`, `token_type`, `expires_in`).
   * Prints the extracted **ACCESS TOKEN** on its own.

### Example

```bash
$ python3 aic-sa-access-token.py \
    -u https://acme-tenant.pingone.com \
    -s 449d7e27-7889-47af-a736-83b6bbf97ec5 \
    -k ./service_account_key.jwk \
    -i service-account \
    -c "fr:am:* fr:idm:*"

=== Raw JSON Response ===
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5...,",
  "token_type": "Bearer",
  "expires_in": 3600
}

=== Access Token ===
eyJhbGciOiJSUzI1NiIsInR5...
```

## 📚 Further Reading

* [PingOne AIC Developer Docs: JWT‑Bearer Flow](https://docs.pingidentity.com/pingoneaic/latest/developer-docs/postman-collection.html)
* [RFC 7523: JWT Profile for OAuth 2.0](https://tools.ietf.org/html/rfc7523)

---

*This project is provided under the MIT License. See `LICENSE` for details.*

