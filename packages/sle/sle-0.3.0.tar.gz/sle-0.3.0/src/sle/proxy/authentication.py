import datetime as dt
import random
import struct
import hashlib

from pyasn1.codec.ber.encoder import encode as asn1_encode
from pyasn1.codec.der.encoder import encode as asn1_der_encode
from pyasn1.codec.der.decoder import decode as asn1_decode

from sle import logger
from sle.datatypes.security import HashInput, Isp1Credentials


class AuthenticationLayer:
    """
    The Authentication Layer receives SLE protocol data units from the higher layers
    and adds credential parameters if required.
    """

    def __init__(
        self,
        proxy,
        hash_algorithm,
        local_identifier,
        peer_identifier,
        local_password,
        peer_password,
        authentication_delay,
    ):
        """
        Attributes:
        - local_identifier: Identifier of the local application
        - local_password: Password of the local application
        - peer_identifier: Identifier of the peer application
        - peer_password: Password of the peer application
        - authentication_delay: Maximum time between generation of credentials and its verification. Default: 180 seconds
        """
        self._proxy = proxy
        self._local_identifier = local_identifier
        self._local_password = local_password
        self._peer_identifier = peer_identifier
        self._peer_password = peer_password
        self._authentication_delay = authentication_delay
        self._hash_algorithm = hash_algorithm

    def sle_pdu_request(self, pdu, apply_authentication=False):
        if apply_authentication:
            if not self._local_password:
                logger.error(
                    "Local credentials not defined, but required for authentication"
                )
            local_credentials = self._make_credentials(
                self._local_identifier, self._local_password
            )
            pdu["invokerCredentials"]["used"] = local_credentials
        else:
            if "invokerCredentials" in pdu:
                pdu["invokerCredentials"]["unused"] = None
        self._proxy.encoding.sle_pdu_request(pdu)

    def sle_pdu_indication(self, pdu, decoding_result):
        if decoding_result is False:
            self._proxy.service_layer.sle_pdu_indication(
                pdu=None, authentication_result=False, decoding_result=False
            )

        key = pdu.getName()
        authentication_result = True

        if "responderIdentifier" in pdu[key]:
            responder_identifier = pdu[key]["responderIdentifier"]
            if self._peer_identifier not in responder_identifier.prettyPrint():
                logger.warning("Authentication failed. Wrong responder identifier.")
                authentication_result = False

        if "performerCredentials" in pdu[key]:
            performer_credentials = pdu[key]["performerCredentials"]["used"]
            if performer_credentials.isValue:
                if not self._check_return_credentials(
                    performer_credentials, self._peer_identifier, self._peer_password
                ):
                    logger.warning(
                        "Authentication failed. Credentials not valid or too old."
                    )
                    authentication_result = False

        self._proxy.service_layer.sle_pdu_indication(
            pdu, authentication_result, decoding_result
        )

    def _check_return_credentials(self, credentials, username, password):
        decoded_credentials = asn1_decode(
            credentials.asOctets(), asn1Spec=Isp1Credentials()
        )[0]
        days, ms, us = struct.unpack(
            "!HIH", bytearray(decoded_credentials["time"].asNumbers())
        )
        time_delta = dt.timedelta(days=days, milliseconds=ms, microseconds=us)
        cred_time = time_delta + dt.datetime(1958, 1, 1)
        random_number = int(decoded_credentials["randomNumber"])
        generated_credentials = self._generate_encoded_credentials(
            cred_time, random_number, username, password
        )
        return generated_credentials == credentials.asOctets()

    def _make_credentials(self, username, password):
        """Makes credentials for the initiator"""
        now = dt.datetime.utcnow()
        random_number = random.randint(0, 2147483647)
        return self._generate_encoded_credentials(
            now, random_number, username, password
        )

    def _generate_encoded_credentials(
        self, current_time, random_number, username, password
    ):
        """Generates encoded ISP1 credentials"""
        hash_input = HashInput()
        days = (current_time - dt.datetime(1958, 1, 1)).days
        millisecs = (
            1000
            * (
                current_time
                - current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            ).total_seconds()
        )
        microsecs = int(round(millisecs % 1 * 1000))
        millisecs = int(millisecs)
        credential_time = struct.pack("!HIH", days, millisecs, microsecs)

        hash_input["time"] = credential_time
        hash_input["randomNumber"] = random_number
        hash_input["userName"] = username
        hash_input["passWord"] = bytes.fromhex(password)
        der_encoded_hash_input = asn1_der_encode(hash_input)

        if self._hash_algorithm == "SHA-1":
            the_protected = bytearray.fromhex(
                hashlib.sha1(der_encoded_hash_input).hexdigest()
            )
        elif self._hash_algorithm == "SHA-256":
            the_protected = bytearray.fromhex(
                hashlib.sha256(der_encoded_hash_input).hexdigest()
            )
        else:
            raise ValueError(f"Not a valid hash algorithm: {self._hash_algorithm}")

        isp1_creds = Isp1Credentials()
        isp1_creds["time"] = credential_time
        isp1_creds["randomNumber"] = random_number
        isp1_creds["theProtected"] = the_protected

        return asn1_encode(isp1_creds)
