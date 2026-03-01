import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _headers(schema: str = "tienda_alquemia"):
    headers = {
        "Accept": "application/json",
        "Accept-Profile": schema,
        "Content-Profile": schema,
    }
    
    # Añadir API key solo si existe (necesario para Supabase Cloud)
    api_key = os.getenv("SUPABASE_KEY", "").strip()
    if api_key:
        headers["apikey"] = api_key
        headers["Authorization"] = f"Bearer {api_key}"
    
    return headers


def _request(method: str, table: str, params: dict | None = None, payload: dict | list | None = None, schema: str = "tienda_alquemia"):
    base = os.getenv("SUPABASE_URL", "").rstrip("/")
    if not base:
        print(f"[ERROR] SUPABASE_URL no configurado")
        return []

    query = urlencode(params or {}, doseq=True)
    
    # Detectar si es PostgREST puro o Supabase Cloud
    # Supabase Cloud usa /rest/v1/, PostgREST puro no
    is_postgrest = "postgrest" in base or "localhost" in base or "127.0.0.1" in base
    if is_postgrest:
        url = f"{base}/{table}"
    else:
        url = f"{base}/rest/v1/{table}"
    
    if query:
        url = f"{url}?{query}"

    print(f"[DEBUG] Llamando a: {url}")
    
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
            result = json.loads(body) if body else []
            print(f"[DEBUG] Respuesta: {len(result) if isinstance(result, list) else 'dict'} elementos")
            return result
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
