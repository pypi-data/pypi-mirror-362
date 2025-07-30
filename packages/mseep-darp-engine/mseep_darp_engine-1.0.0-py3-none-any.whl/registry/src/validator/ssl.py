import asyncio
import logging
import ssl
from typing import Self
from urllib.parse import urlparse

from cryptography import x509
from cryptography.hazmat._oid import ExtensionOID
from cryptography.hazmat.backends import default_backend

from .constants import EV_OIDS
from .constants import HTTP_PORT
from .constants import HTTPS_PORT
from .constants import SELF_SIGNED_CERTIFICATE_ERR_CODE
from .schemas import SSLAuthorityLevel


class SSLHelper:
    def __init__(self) -> None:
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def get_ssl_authority_level(self, url: str) -> SSLAuthorityLevel:
        try:
            cert = await self._load_certificate(url)
        except ssl.SSLCertVerificationError as exc:
            if exc.verify_code == SELF_SIGNED_CERTIFICATE_ERR_CODE:
                return SSLAuthorityLevel.SELF_SIGNED_CERTIFICATE
            return SSLAuthorityLevel.INVALID_CERTIFICATE
        except Exception as exc:
            self._logger.error("Failed to fetch ssl cert", exc_info=exc)
            return SSLAuthorityLevel.NO_CERTIFICATE

        if self._is_cert_respects_ev(cert):
            return SSLAuthorityLevel.EXTENDED_CERTIFICATE

        return SSLAuthorityLevel.CERTIFICATE_OK

    @classmethod
    def get_new_instance(cls) -> Self:
        return cls()

    @staticmethod
    def _extract_port(uri: str) -> int:
        parsed = urlparse(uri)

        if parsed.port:
            return parsed.port

        if parsed.scheme == "https":
            return HTTPS_PORT
        elif parsed.scheme == "http":
            return HTTP_PORT

        raise ValueError("Invalid URI", uri)

    @staticmethod
    def _extract_host(uri: str) -> str:
        parsed = urlparse(uri)

        if parsed.hostname is None:
            raise ValueError("Invalid URL: No hostname found")

        return parsed.hostname

    @classmethod
    async def _load_certificate(cls, url: str) -> x509.Certificate:
        hostname = cls._extract_host(url)
        port = cls._extract_port(url)

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        reader, writer = await asyncio.open_connection(
            hostname, port, ssl=ssl_context, server_hostname=hostname
        )

        ssl_object = writer.get_extra_info("ssl_object")
        der_cert = ssl_object.getpeercert(binary_form=True)
        writer.close()
        await writer.wait_closed()

        cert_obj = x509.load_der_x509_certificate(der_cert, default_backend())
        return cert_obj

    @staticmethod
    def _is_cert_respects_ev(cert: x509.Certificate) -> bool:
        try:
            policies = cert.extensions.get_extension_for_oid(
                ExtensionOID.CERTIFICATE_POLICIES
            ).value
        except x509.ExtensionNotFound:
            return False

        for policy in policies:
            if policy.policy_identifier.dotted_string in EV_OIDS:
                return True

        return False
