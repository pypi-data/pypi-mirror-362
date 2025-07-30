import datetime
import time

from .. import logger
from ..constants import SleState, AuthLevel
from ..datatypes.service_instance import (
    OperationIdentifier_v1,
    OperationIdentifier,
    ServiceInstanceIdentifier,
    ServiceInstanceAttributeElement,
    ServiceInstanceAttribute,
)
from ..proxy import UserProxy


CCSDS_EPOCH = datetime.datetime(1958, 1, 1)


class SleUser:

    def __init__(
        self,
        service_instance_identifier,
        responder_host,
        responder_port,
        auth_level,
        local_identifier,
        peer_identifier,
        responder_port_identifier=None,
        local_password=None,
        peer_password=None,
        heartbeat_interval=25,
        heartbeat_deadfactor=5,
        buffer_size=256000,
        version_number=5,
        hash_algorithm="SHA-256",
        asn1_decoding_spec=None,  # to be provided by child class
    ):

        self._service_instance_identifier = service_instance_identifier
        self._responder_host = responder_host
        self._responder_port = responder_port
        self._responder_port_identifier = responder_port_identifier
        self._auth_level = auth_level.lower()
        self._initiator_identifier = local_identifier
        self._version_number = version_number

        self.state = SleState.UNBOUND
        self._handlers = {}
        self._invoke_id = 0

        self._proxy = UserProxy(
            service_layer=self,
            local_identifier=local_identifier,
            peer_identifier=peer_identifier,
            local_password=local_password,
            peer_password=peer_password,
            asn1_decoding_spec=asn1_decoding_spec,
            heartbeat_interval=heartbeat_interval,
            heartbeat_deadfactor=heartbeat_deadfactor,
            buffer_size=buffer_size,
            hash_algorithm=hash_algorithm,
        )

        self._service_type = None  # to be set in derived class

    def _get_new_invoke_id(self):
        self._invoke_id += 1
        return self._invoke_id

    def wait_for_state(self, state, timeout=0, interval=0.1):
        start = time.time()
        if not isinstance(state, list):
            state = [state]
        while self.state not in state:
            if timeout and time.time() - start > timeout:
                return False
            time.sleep(interval)
        return True

    def bind(self, pdu):
        logger.debug("%s request (bind)", self.__class__.__name__)

        if self.state != SleState.UNBOUND:
            logger.error("Request (bind) not valid for current state: %s", self.state)
            return

        self._proxy.transport.tml_connect_request(
            self._responder_host, self._responder_port
        )

        self._proxy.connected = False
        self._proxy.connection_error = False
        while True:
            if self._proxy.connected:
                break
            if self._proxy.connection_error:
                logger.warning("TML connection failure")
                return
            time.sleep(0.1)

        pdu["initiatorIdentifier"] = self._initiator_identifier
        pdu["responderPortIdentifier"] = self._responder_port_identifier
        pdu["serviceType"] = self._service_type
        pdu["versionNumber"] = self._version_number

        inst_ids = [
            st.split("=") for st in self._service_instance_identifier.split(".")
        ]

        if self._version_number == 1:
            OID = OperationIdentifier_v1
        else:
            OID = OperationIdentifier

        sii = ServiceInstanceIdentifier()
        for i, iden in enumerate(inst_ids):
            identifier = OID[iden[0].replace("-", "_")]
            siae = ServiceInstanceAttributeElement()
            siae["identifier"] = identifier
            siae["siAttributeValue"] = iden[1]
            sia = ServiceInstanceAttribute()
            sia[0] = siae
            sii[i] = sia
        pdu["serviceInstanceIdentifier"] = sii

        if self._auth_level in [AuthLevel.BIND, AuthLevel.ALL]:
            self._proxy.authentication.sle_pdu_request(pdu, apply_authentication=True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, apply_authentication=False)

        self.state = SleState.BINDING

    def _bind_return_handler(self, pdu):
        logger.debug("%s return handler (bind)", self.__class__.__name__)

        if self.state != SleState.BINDING:
            logger.warning(
                "Return (bind) not expected for current state: %s", self.state
            )

        key = pdu.getName()
        result = pdu[key]["result"].getName()

        if result == "positive":
            logger.debug("Bind successful")
            self.state = SleState.READY
        else:
            logger.warning(
                "Bind unsuccessful. Reason: %s",
                pdu[key]["result"][result].prettyPrint(),
            )
            self._proxy.transport.tml_disconnect_request()
            self.state = SleState.UNBOUND

    def unbind(self, pdu):
        logger.debug("%s request (unbind)", self.__class__.__name__)

        if self.state != SleState.READY:
            logger.error("Request (unbind) not valid for current state: %s", self.state)
            return

        if self._auth_level == AuthLevel.ALL:
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)
        self.state = SleState.UNBINDING

    def _unbind_return_handler(self, pdu):
        logger.debug("%s return handler (unbind)", self.__class__.__name__)

        if not self.state == SleState.UNBINDING:
            logger.warning(
                "Return (unbind) not expected for current state: %s", self.state
            )

        self._proxy.transport.tml_disconnect_request()
        logger.debug("Unbind successful")
        self.state = SleState.UNBOUND

    def start(self, pdu):
        logger.debug("%s request (start)", self.__class__.__name__)

        if self.state != SleState.READY:
            logger.error("Request (start) not valid for current state: %s", self.state)
            return

        pdu["invokeId"] = self._get_new_invoke_id()
        if self._auth_level == AuthLevel.ALL:
            self._proxy.authentication.sle_pdu_request(pdu, apply_authentication=True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, apply_authentication=False)
        self.state = SleState.STARTING

    def _start_return_handler(self, pdu):
        logger.debug("%s return handler (start)", self.__class__.__name__)

        if not self.state == SleState.STARTING:
            logger.warning(
                "return (start) not expected for current state: %s", self.state
            )

        key = pdu.getName()
        result = pdu[key]["result"].getName()
        if result == "positiveResult":
            logger.info("Start successful")
            self.state = SleState.ACTIVE
        else:
            logger.info(
                "Start unsuccessful: %s", pdu[key]["result"][result].prettyPrint()
            )
            self.state = SleState.READY

    def stop(self, pdu):
        logger.debug("%s request (stop)", self.__class__.__name__)

        if self.state != SleState.ACTIVE:
            logger.error("Request (stop) not valid for current state: %s", self.state)
            return

        pdu["invokeId"] = self._get_new_invoke_id()
        if self._auth_level == AuthLevel.ALL:
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)
        self.state = SleState.STOPPING

    def _stop_return_handler(self, pdu):
        logger.debug("%s return handler (stop)", self.__class__.__name__)

        if not self.state == SleState.STOPPING:
            logger.error("Return (stop) not expected for current state: %s", self.state)

        key = pdu.getName()
        result = pdu[key]["result"].getName()
        if result == "positiveResult":
            logger.info("Stop successful")
            self.state = SleState.READY
        else:
            logger.info("Stop unsuccessful")
            self.state = SleState.ACTIVE

    def schedule_status_report(self, pdu, report_type, cycle):
        logger.debug("%s request (schedule status report)", self.__class__.__name__)

        if self.state not in [SleState.READY, SleState.ACTIVE]:
            logger.error(
                "Request (schedule status report) not valid for current state: %s",
                self.state,
            )
            return

        pdu["invokeId"] = self._get_new_invoke_id()

        if report_type == "immediately":
            pdu["reportRequestType"]["immediately"] = None
        elif report_type == "periodically":
            pdu["reportRequestType"]["periodically"] = cycle
        elif report_type == "stop":
            pdu["reportRequestType"]["stop"] = None
        else:
            raise ValueError("Unknown report type: {}".format(report_type))

        if self._auth_level == AuthLevel.ALL:
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)

    def _schedule_status_report_return_handler(self, pdu):
        logger.debug(
            "%s return handler (schedule status report)", self.__class__.__name__
        )

        if self.state not in [SleState.READY, SleState.ACTIVE]:
            logger.warning(
                "Return (schedule status report) not expected for current state: %s",
                self.state,
            )

        logger.info("Received schedule status report return")
        key = pdu.getName()
        result = pdu[key]["result"].getName()
        if result == "positiveResult":
            logger.info("Schedule status report successful")
        else:
            diag = pdu[key]["result"].getComponent()
            if diag.getName() == "common":
                diag_options = ["duplicateInvokeId", "otherReason"]
            else:
                diag_options = [
                    "notSupportedInThisDeliveryMode",
                    "alreadyStopped",
                    "invalidReportingCycle",
                ]
            reason = diag_options[int(diag.getComponent())]
            logger.warning(
                "Status report scheduling failed. " "Reason: {}".format(reason)
            )

    def _status_report_invocation_handler(self, pdu):
        logger.debug("%s invocation (status report)", self.__class__.__name__)
        key = pdu.getName()

        if self.state not in [SleState.READY, SleState.ACTIVE]:
            logger.warning(
                "Invocation (status report) not expected for current state: %s",
                self.state,
            )

        self.status_report_indication(pdu[key])

    def get_parameter(self, pdu):
        logger.debug("%s request (get parameter)", self.__class__.__name__)

        if self.state not in [SleState.READY, SleState.ACTIVE]:
            logger.error("Request (get parameter) not valid for current state")
            return

        pdu["invokeId"] = self._get_new_invoke_id()
        if self._auth_level == AuthLevel.ALL:
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)

    def _get_parameter_return_handler(self, pdu):
        logger.debug("%s return handler (get parameter)", self.__class__.__name__)

        if self.state == SleState.UNBOUND:
            logger.error(
                "Request (get parameter) not valid for current state: %s", self.state
            )
            return

        key = pdu.getName()
        result = pdu[key]["result"].getName()
        if result == "negativeResult":
            logger.warning("Get parameter invocation failed")
            return
        pdu = pdu[key]["result"].getComponent()
        self.parameter_indication(pdu)

    def peer_abort(self, pdu):
        logger.debug("%s request (peer abort)", self.__class__.__name__)

        if self.state == SleState.UNBOUND:
            logger.error(
                "Request (peer abort) not valid for current state: %s", self.state
            )
            return

        self._proxy.authentication.sle_pdu_request(pdu, False)
        self.state = SleState.UNBOUND
        self._proxy.transport.tml_disconnect_request()

    def sle_pdu_indication(self, pdu, authentication_result, decoding_result):
        logger.debug("%s indication (sle pdu)", self.__class__.__name__)

        if decoding_result is False:
            logger.debug("%s decoding failed, discarding PDU", self.__class__.__name__)
            return

        if authentication_result is False:
            logger.debug(
                "%s authentication failed, discarding PDU", self.__class__.__name__
            )
            return

        key = pdu.getName()
        key = key[:1].upper() + key[1:]

        if key in self._handlers:
            pdu_handler = self._handlers[key]
            pdu_handler(pdu)
        else:
            logger.error("PDU of type %s has no associated handler", key)

    def _transfer_buffer_handler(self, pdu):
        logger.debug("%s transfer buffer handler", self.__class__.__name__)

        if self.state != SleState.ACTIVE:
            logger.warning(
                "Return (transfer buffer) not expected for current state: %s",
                self.state,
            )

        key = pdu.getName()
        for frame_or_notify in pdu[key]:
            self.sle_pdu_indication(
                frame_or_notify, authentication_result=True, decoding_result=True
            )

    def _annotated_frame_handler(self, pdu):
        logger.debug("%s annotated frame handler", self.__class__.__name__)

        if self.state != SleState.ACTIVE:
            logger.warning(
                "Return (annotated frame) not expected for current state: %s",
                self.state,
            )

        frame = pdu.getComponent()
        if not frame.isValue:
            logger.error("TransferBuffer received but data cannot be located")
            return
        self.frame_indication(frame)

    def parameter_indication(self, pdu):
        logger.debug(
            "%s parameter indication: \n %s", self.__class__.__name__, pdu
        )  # to be implemented by application

    def status_report_indication(self, pdu):
        logger.debug(
            "%s status report indication: \n %s", self.__class__.__name__, pdu
        )  # to be implemented by application

    def frame_indication(self, pdu):
        logger.debug(
            "%s frame indication: \n %s", self.__class__.__name__, pdu
        )  # to be implemented by application

    def tml_protocol_abort_indication(self, diagnostic=None):
        logger.warning(
            "TML protocol abort indication. Diagnostic code: %s",
            None if diagnostic is None else int.from_bytes(diagnostic, byteorder="big"),
        )
        self.state = SleState.UNBOUND
