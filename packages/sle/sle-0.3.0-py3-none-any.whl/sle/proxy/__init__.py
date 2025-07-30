from .authentication import AuthenticationLayer
from .encoding import DataEncodingLayer
from .transport import TransportMappingLayer, Role


class UserProxy:

    def __init__(
        self,
        service_layer,
        local_identifier,
        peer_identifier,
        local_password,
        peer_password,
        asn1_decoding_spec,
        heartbeat_interval,
        heartbeat_deadfactor,
        buffer_size,
        hash_algorithm,
    ):
        self.connected = False

        self.service_layer = service_layer
        self.authentication = AuthenticationLayer(
            proxy=self,
            local_identifier=local_identifier,
            peer_identifier=peer_identifier,
            local_password=local_password,
            peer_password=peer_password,
            hash_algorithm=hash_algorithm,
            authentication_delay=180,
        )

        self.encoding = DataEncodingLayer(self, asn1_decoding_spec)

        self.transport = TransportMappingLayer(
            self, heartbeat_interval, heartbeat_deadfactor, buffer_size, Role.INITIATOR
        )

        self.transport.tml_protocol_abort_indication = (
            service_layer.tml_protocol_abort_indication
        )
