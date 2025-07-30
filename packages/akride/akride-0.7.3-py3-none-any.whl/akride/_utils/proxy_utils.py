"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Dict, Optional, Tuple
from urllib.request import getproxies, proxy_bypass

import attr
from yarl import URL


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ProxyInfo:
    proxy: URL
    proxy_auth: Optional[str]


def proxies_from_env() -> Dict[str, ProxyInfo]:
    proxy_urls = {
        k: URL(v) for k, v in getproxies().items() if k in ("http", "https")
    }
    stripped = {k: strip_auth_from_url(v) for k, v in proxy_urls.items()}
    ret = {}
    for proto, val in stripped.items():
        proxy, auth = val
        ret[proto] = ProxyInfo(proxy, auth)
    return ret


def strip_auth_from_url(url: URL) -> Tuple[URL, Optional[str]]:
    if url.user:
        return url.with_user(None), f"{url.user}:{url.password}"
    return url.with_user(None), None


def get_env_proxy_for_url(url: URL):
    """Get a permitted proxy for the given URL from the env."""
    if url.host is not None and proxy_bypass(url.host):
        raise LookupError(f"Proxying is disallowed for `{url.host!r}`")

    proxies_in_env = proxies_from_env()
    try:
        proxy_info = proxies_in_env[url.scheme]
    except KeyError as kErr:
        raise LookupError(
            f"No proxies found for `{url!s}` in the env"
        ) from kErr
    else:
        return proxy_info.proxy, proxy_info.proxy_auth
