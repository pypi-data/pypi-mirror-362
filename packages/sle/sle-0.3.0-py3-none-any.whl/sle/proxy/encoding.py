from pyasn1.codec.ber.encoder import encode as asn1_encode
from pyasn1.codec.der.decoder import decode as asn1_decode
import pyasn1.error

from sle import logger


class DataEncodingLayer:
    """
    The Data Encoding Layer is responsible for the encoding and decoding of all
    SLE protocol data units. It uses the ASN.1 types definitions.
    """

    def __init__(self, proxy, asn1_decoding_spec):
        self._proxy = proxy
        self._asn1_decoding_spec = asn1_decoding_spec

    def sle_pdu_request(self, pdu):
        encoded_pdu = asn1_encode(pdu)
        self._proxy.transport.sle_pdu_request(encoded_pdu)

    def sle_pdu_indication(self, encoded_pdu):
        decoding_result = True

        try:
            pdu = asn1_decode(encoded_pdu, asn1Spec=self._asn1_decoding_spec)[0]
        except (pyasn1.error.PyAsn1Error, TypeError) as e:
            logger.warning("Unable to decode PDU: %s", e)
            pdu = None
            decoding_result = False

        self._proxy.authentication.sle_pdu_indication(pdu, decoding_result)
