import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _headers(schema: str = "tienda_alquemia"):
    key = os.getenv("SUPABASE_SERVICE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "Accept-Profile": schema,
        "Content-Profile": schema,
    }


def _request(method: str, table: str, params: dict | None = None, payload: dict | list | None = None, schema: str = "tienda_alquemia"):
    base = os.getenv("SUPABASE_URL", "").rstrip("/")
    if not base:
        return []

    query = urlencode(params or {}, doseq=True)
    url = f"{base}/rest/v1/{table}"
    if query:
        url = f"{url}?{query}"

    headers = _headers(schema)
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        headers["Prefer"] = "return=representation"
        data = json.dumps(payload).encode("utf-8")

    req = Request(url=url, headers=headers, data=data, method=method)
    try:
        with urlopen(req, timeout=12) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else []
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8")
        except Exception:
            body = ""
        print(f"[Supabase REST] HTTP {e.code} en {table}: {body[:300]}")
        return []
    except (URLError, TimeoutError) as e:
        print(f"[Supabase REST] Error de red en {table}: {e}")
        return []


def _select_once(table: str, params: dict | None = None, schema: str = "tienda_alquemia"):
    return _request("GET", table, params=params, schema=schema)


def select(table: str, params: dict | None = None, schema: str = "tienda_alquemia"):
    data = _select_once(table, params, schema)
    if data:
        return data
    return []


def insert(table: str, payload: dict | list, schema: str = "tienda_alquemia"):
    data = _request("POST", table, payload=payload, schema=schema)
    if data:
        return data

    if schema != "tienda_alquemia":
        data_alt = _request("POST", table, payload=payload, schema="tienda_alquemia")
        if data_alt:
            return data_alt

    return []
