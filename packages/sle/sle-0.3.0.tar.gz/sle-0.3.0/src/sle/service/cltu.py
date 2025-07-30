import time
import struct

from sle import logger
from sle.constants import SleState, UnbindReason
from sle.datatypes.cltu_pdu import CltuUserToProviderPdu, CltuProviderToUserPdu
from sle.datatypes.cltu_structure import CltuParameterName
from .base import SleUser, CCSDS_EPOCH


class CltuServiceUser(SleUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, asn1_decoding_spec=CltuProviderToUserPdu(), **kwargs)
        self._service_type = "fwdCltu"
        self._handlers = {
            "CltuBindReturn": self._bind_return_handler,
            "CltuUnbindReturn": self._unbind_return_handler,
            "CltuStartReturn": self._start_return_handler,
            "CltuStopReturn": self._stop_return_handler,
            "CltuGetParameterReturn": self._get_parameter_return_handler,
            "CltuScheduleStatusReportReturn": self._schedule_status_report_return_handler,
            "CltuStatusReportInvocation": self._status_report_invocation_handler,
            "CltuTransferDataReturn": self._transfer_data_return_handler,
            "CltuThrowEventReturn": self._throw_event_return_handler,
            "CltuAsyncNotifyInvocation": self._async_notify_invocation_handler,
        }

        self._cltu_id = 0
        self._event_invocation_id = 0

    def _get_new_cltu_id(self):
        self._cltu_id += 1
        return self._cltu_id

    def bind(self):
        pdu = CltuUserToProviderPdu()["cltuBindInvocation"]
        super().bind(pdu)

    def unbind(self, reason=UnbindReason.OTHER):
        pdu = CltuUserToProviderPdu()["cltuUnbindInvocation"]
        pdu["unbindReason"] = reason
        super().unbind(pdu)

    def start(self):
        pdu = CltuUserToProviderPdu()["cltuStartInvocation"]
        pdu["firstCltuIdentification"] = self._cltu_id
        super().start(pdu)

    def stop(self):
        pdu = CltuUserToProviderPdu()["cltuStopInvocation"]
        super().stop(pdu)

    def schedule_status_report(self, report_type="immediately", cycle=None):
        pdu = CltuUserToProviderPdu()["cltuScheduleStatusReportInvocation"]
        super().schedule_status_report(pdu, report_type, cycle)

    def get_parameter(self, parameter):
        if parameter not in [n for n in CltuParameterName().namedValues]:
            logger.error("Parameter name does not exist %s", parameter)
            return
        pdu = CltuUserToProviderPdu()["cltuGetParameterInvocation"]
        pdu["cltuParameter"] = CltuParameterName().namedValues[parameter]
        super().get_parameter(pdu)

    def peer_abort(self, reason="otherReason"):
        pdu = CltuUserToProviderPdu()
        pdu["cltuPeerAbortInvocation"] = reason
        super().peer_abort(pdu)

    def transfer_data(
        self, data, earliest_time=None, latest_time=None, delay=0, notify=False
    ):
        logger.debug("%s request (transfer data)", self.__class__.__name__)

        if self.state != SleState.ACTIVE:
            logger.error(
                "Request (transfer data) not valid for current state: %s", self.state
            )
            return

        pdu = CltuUserToProviderPdu()["cltuTransferDataInvocation"]
        pdu["invokeId"] = self._get_new_invoke_id()
        pdu["cltuIdentification"] = self._cltu_id

        if earliest_time:
            t = struct.pack("!HIH", (earliest_time - CCSDS_EPOCH).days, 0, 0)
            pdu["earliestTransmissionTime"]["known"]["ccsdsFormat"] = t
        else:
            pdu["earliestTransmissionTime"]["undefined"] = None

        if latest_time:
            t = struct.pack("!HIH", (latest_time - CCSDS_EPOCH).days, 0, 0)
            pdu["latestTransmissionTime"]["known"]["ccsdsFormat"] = t
        else:
            pdu["latestTransmissionTime"]["undefined"] = None

        pdu["delayTime"] = delay
        pdu["cltuData"] = data

        if notify:
            pdu["slduRadiationNotification"] = 0
        else:
            pdu["slduRadiationNotification"] = 1

        logger.debug("Sending CLTU id: %s", self._cltu_id)
        logger.debug(pdu.prettyPrint())

        if self._auth_level == "all":
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)

        self._get_new_cltu_id()  # increase CLTU counter

    def _transfer_data_return_handler(self, pdu):
        logger.debug("%s return handler (transfer data)", self.__class__.__name__)

        if self.state != SleState.ACTIVE:
            logger.warning(
                "Return (transfer data) not expected for current state: %s", self.state
            )

        key = pdu.getName()
        result = pdu[key]["result"].getName()
        cltu_id = pdu[key]["cltuIdentification"]
        buffer_available = pdu[key]["cltuBufferAvailable"]

        if result == "positiveResult":
            logger.debug(
                "CLTU %s transfer passed. Buffer available: %s",
                cltu_id,
                buffer_available,
            )
        else:
            result = pdu[key]["result"]["negativeResult"]
            if result.getName() == "common":
                opts = ["Duplicate Invoke Id", "Other Reason"]
                diag = opts[result["common"]]
            else:
                opts = [
                    "Unable to Process",
                    "Unable to Store",
                    "Out of Sequence",
                    "Inconsistent Time Range",
                    "Invalid Time",
                    "Late Sldu",
                    "Invalid Delay Time",
                    "CLTU Error",
                ]
                diag = opts[result["specific"]]
            logger.debug(
                "CLTU %s transfer failed. Diagnose: %s. Buffer available: %s",
                cltu_id,
                diag,
                buffer_available,
            )

    def throw_event(self, event_id, event_qualifier):
        logger.debug("%s request (throw event)", self.__class__.__name__)

        if self.state == SleState.UNBOUND:
            logger.error(
                "Request (throw event) not valid for current state: %s", self.state
            )
            return

        pdu = CltuUserToProviderPdu()["cltuThrowEventInvocation"]
        pdu["invokeId"] = self._get_new_invoke_id()
        pdu["eventInvocationIdentification"] = self._event_invocation_id
        pdu["eventIdentifier"] = event_id
        pdu["eventQualifier"] = event_qualifier
        logger.debug("Sending throw event invocation...")
        if self._auth_level == "all":
            self._proxy.authentication.sle_pdu_request(pdu, True)
        else:
            self._proxy.authentication.sle_pdu_request(pdu, False)

    def _throw_event_return_handler(self, pdu):
        logger.debug("%s return handler (throw event)", self.__class__.__name__)

        if self.state == SleState.UNBOUND:
            logger.warning(
                "Return (throw event) not expected for current state: %s", self.state
            )

        key = pdu.getName()
        result = pdu[key]["result"].getName()
        eid = pdu[key]["eventInvocationIdentification"]
        if result == "positiveResult":
            msg = "Throw event invocation successful"
            self._event_invocation_id = eid
        else:
            diag = pdu[key]["result"].getComponent()
            diag = diag[diag.getName()]
            msg = "Throw event invocation #{} Failed. Reason: {}".format(eid, diag)
        logger.debug(msg)

    def _async_notify_invocation_handler(self, pdu):
        logger.debug("%s invocation (async notify)", self.__class__.__name__)

        if self.state == SleState.UNBOUND:
            logger.error(
                "Invocation (async notify) not expted for current state: %s", self.state
            )

        pdu = pdu["cltuAsyncNotifyInvocation"]

        report = "\n"
        if "cltuNotification" in pdu:
            report += "CLTU Notification: {}\n".format(
                pdu["cltuNotification"].getName()
            )

        if "cltuLastProcessed" in pdu:
            if pdu["cltuLastProcessed"].getName() == "noCltuProcessed":
                report += " Last Processed: None\n"
            else:
                last_processed = pdu["cltuLastProcessed"].getComponent()
                time = "unknown"
                if "known" in last_processed["radiationStartTime"]:
                    time = (
                        last_processed["radiationStartTime"]
                        .getComponent()
                        .getComponent()
                        .asOctets()
                        .hex()
                    )
                    # TODO: convert hex to datetime
                report += " Last Processed: id: {} | ".format(
                    last_processed["cltuIdentification"]
                )
                report += "rad start: {} | status: {}\n".format(
                    time, last_processed["cltuStatus"]
                )

        if "cltuLastOk" in pdu:
            if pdu["cltuLastOk"].getName() == "noCltuOk":
                report += " Last Ok: No CLTU Ok\n"
            else:
                last_ok = pdu["cltuLastOk"].getComponent()
                time = "unknown"
                if "known" in last_ok["radiationStopTime"]:
                    time = (
                        last_ok["radiationStopTime"]
                        .getComponent()
                        .getComponent()
                        .asOctets()
                        .hex()
                    )
                report += " Last Ok: id: {} | end: {}\n".format(
                    last_ok["cltuIdentification"], time
                )

        if "productionStatus" in pdu:
            report += " Production Status: {}\n".format(pdu["productionStatus"])

        if "uplinkStatus" in pdu:
            report += " Uplink Status: {}\n".format(pdu["uplinkStatus"])

        logger.debug(report)
