#!/usr/bin/env python3
import time
import uuid
import json
import sys
import argparse
import requests
import jwt            # PyJWT (only used for signing)
from jwcrypto import jwk

def load_private_key(jwk_path):
    with open(jwk_path, "r") as f:
        jwk_dict = json.load(f)
    jwk_obj = jwk.JWK(**jwk_dict)
    return jwk_dict, jwk_obj.export_to_pem(private_key=True, password=None)

def build_jwt_assertion(service_account_id, token_url, jwk_dict, private_key_pem):
    now = int(time.time())
    claims = {
        "iss": service_account_id,
        "sub": service_account_id,
        "aud": token_url,
        "iat": now,
        "exp": now + 300,
        "jti": str(uuid.uuid4()),
    }
    headers = {"alg": "RS256", "typ": "JWT"}
    kid = jwk_dict.get("kid")
    if kid is not None:
        headers["kid"] = str(kid)
    return jwt.encode(claims, private_key_pem, algorithm="RS256", headers=headers)

def fetch_token_response(token_url, assertion, scopes, client_id):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": assertion,
        "scope": scopes,
        "client_id": client_id,
    }
    resp = requests.post(token_url, data=data)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"ERROR {resp.status_code} fetching token:\n{resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json()

def main():
    p = argparse.ArgumentParser(
        description="Obtain a PingOne AIC access_token via JWT-bearer and show raw JSON"
    )
    p.add_argument("-u", "--tenant-url",       required=True,
                   help="e.g. https://acme-tenant.pingone.com")
    p.add_argument("-s", "--service-account-id", required=True,
                   help="Service-account ID from the AIC console")
    p.add_argument("-k", "--jwk-path",          required=True,
                   help="Path to your service-account JWK file")
    p.add_argument("-i", "--client-id",         default="service-account",
                   help="OAuth2 client_id (default: %(default)s)")
    p.add_argument("-c", "--scopes",            default="fr:idm:* fr:am:*",
                   help="Scopes to request (default: %(default)s)")
    args = p.parse_args()

    token_url = f"{args.tenant_url.rstrip('/')}/am/oauth2/access_token"
    jwk_dict, private_key_pem = load_private_key(args.jwk_path)
    assertion = build_jwt_assertion(
        args.service_account_id, token_url, jwk_dict, private_key_pem
    )

    # Fetch the raw JSON response
    token_response = fetch_token_response(
        token_url, assertion, args.scopes, args.client_id
    )

    # Print raw JSON payload
    print("\n=== Raw JSON Response ===\n")
    print(json.dumps(token_response, indent=2))

    # Print just the access_token
    access_token = token_response.get("access_token")
    print("\n=== Access Token ===\n")
    print(access_token)

if __name__ == "__main__":
    main()
