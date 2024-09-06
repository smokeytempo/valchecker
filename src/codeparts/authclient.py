# https://github.com/floxay/python-riot-auth

import contextlib
import ctypes
import ssl
import sys
import warnings
from secrets import token_urlsafe
from typing import Optional

import aiohttp

class RiotAuth:
    RIOT_CLIENT_USER_AGENT = token_urlsafe(111).replace("_", "W").replace("-", "w")
    CIPHERS13 = ":".join(  # https://docs.python.org/3/library/ssl.html#tls-1-3
        (
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
        )
    )
    CIPHERS = ":".join(
        (
            "ECDHE-ECDSA-CHACHA20-POLY1305",
            "ECDHE-RSA-CHACHA20-POLY1305",
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "ECDHE-ECDSA-AES128-SHA",
            "ECDHE-RSA-AES128-SHA",
            "ECDHE-ECDSA-AES256-SHA",
            "ECDHE-RSA-AES256-SHA",
            "AES128-GCM-SHA256",
            "AES256-GCM-SHA384",
            "AES128-SHA",
            "AES256-SHA",
            "DES-CBC3-SHA",  # most likely not available
        )
    )
    SIGALGS = ":".join(
        (
            "ecdsa_secp256r1_sha256",
            "rsa_pss_rsae_sha256",
            "rsa_pkcs1_sha256",
            "ecdsa_secp384r1_sha384",
            "rsa_pss_rsae_sha384",
            "rsa_pkcs1_sha384",
            "rsa_pss_rsae_sha512",
            "rsa_pkcs1_sha512",
            "rsa_pkcs1_sha1",  # will get ignored and won't be negotiated
        )
    )

    def __init__(self) -> None:
        self._auth_ssl_ctx = RiotAuth.create_riot_auth_ssl_ctx()
        self._cookie_jar = aiohttp.CookieJar()
        self.access_token: Optional[str] = None
        self.scope: Optional[str] = None
        self.id_token: Optional[str] = None
        self.token_type: Optional[str] = None
        self.expires_at: int = 0
        self.user_id: Optional[str] = None
        self.entitlements_token: Optional[str] = None

    @staticmethod
    def create_riot_auth_ssl_ctx() -> ssl.SSLContext:
        ssl_ctx = ssl.create_default_context()

        # https://github.com/python/cpython/issues/88068
        addr = id(ssl_ctx) + sys.getsizeof(object())
        ssl_ctx_addr = ctypes.cast(addr, ctypes.POINTER(ctypes.c_void_p)).contents

        libssl: Optional[ctypes.CDLL] = None
        if sys.platform.startswith("win32"):
            for dll_name in (
                "libssl-3.dll",
                "libssl-3-x64.dll",
                "libssl-1_1.dll",
                "libssl-1_1-x64.dll",
            ):
                with contextlib.suppress(FileNotFoundError, OSError):
                    libssl = ctypes.CDLL(dll_name)
                    break
        elif sys.platform.startswith(("linux", "darwin")):
            libssl = ctypes.CDLL(ssl._ssl.__file__)  # type: ignore

        if libssl is None:
            raise NotImplementedError(
                "Failed to load libssl. Your platform or distribution might be unsupported, please open an issue."
            )

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1  # deprecated since 3.10
        ssl_ctx.set_alpn_protocols(["http/1.1"])
        ssl_ctx.options |= 1 << 19  # SSL_OP_NO_ENCRYPT_THEN_MAC
        libssl.SSL_CTX_set_ciphersuites(ssl_ctx_addr, RiotAuth.CIPHERS13.encode())
        libssl.SSL_CTX_set_cipher_list(ssl_ctx_addr, RiotAuth.CIPHERS.encode())
        # setting SSL_CTRL_SET_SIGALGS_LIST
        libssl.SSL_CTX_ctrl(ssl_ctx_addr, 98, 0, RiotAuth.SIGALGS.encode())
        # setting SSL_CTRL_SET_GROUPS_LIST
        libssl.SSL_CTX_ctrl(ssl_ctx_addr, 92, 0, ":".join(
            (
                "x25519",
                "secp256r1",
                "secp384r1",
            )
        ).encode())

        # print([cipher["name"] for cipher in ssl_ctx.get_ciphers()])
        return ssl_ctx