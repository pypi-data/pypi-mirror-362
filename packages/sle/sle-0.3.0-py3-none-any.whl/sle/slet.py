""" SLET - SLE Test Tool

A command line tool that acts as SLE user to test connections to an SLE provider.

"""

import os
import sys
import logging
import time
from pprint import pprint
import yaml
import sle

logging.basicConfig(level=logging.DEBUG)


def run():
    # read the config file (first argument)
    if len(sys.argv) < 2:
        raise ValueError("Missing sle config file as argument")

    if not os.path.isfile(sys.argv[1]):
        raise ValueError(f"File {sys.argv[1]} does not exist")

    if sys.argv[1].split(".")[-1].lower() not in ["yaml", "yml"]:
        raise ValueError("Config file shall be in YAML format")

    with open(sys.argv[1], "r") as file:
        config = yaml.safe_load(file)

    # check if log file is supplied
    dump_file = None
    if len(sys.argv) >= 3:
        dump_file = open(sys.argv[2], "a")

    # Select provider, if multiple found in config file
    providers = [x for x in config["Providers"]]
    if len(providers) > 1:
        print("Select provider:")
        for n, p in enumerate(providers):
            print(f"[{n + 1}] {p}")
        provider = providers[int(input()) - 1]
        provider_config = config["Providers"][provider]
    else:
        provider_config = config["Providers"][providers[0]]

    # Select service instance, if multiple available
    services = [x for x in provider_config["Services"]]
    if len(services) > 1:
        print("Select service:")
        for n, p in enumerate(services):
            sii = provider_config["Services"][p].get("service_instance_identifier")
            print(f"[{n + 1}] {p}, {sii}")
        service = services[int(input()) - 1]
        service_config = provider_config["Services"][service]
    else:
        service_config = provider_config["Services"][services[0]]

    config = {**provider_config, **service_config}
    d = dict(config)
    del d["Services"]
    print()
    print("Configuration:")
    pprint(d)
    print()

    config_kwargs = {
        "service_instance_identifier": config.get("service_instance_identifier"),
        "responder_host": config.get("responder_host"),
        "responder_port": config.get("responder_port"),
        "auth_level": config.get("auth_level"),
        "local_identifier": config.get("local_identifier"),
        "peer_identifier": config.get("peer_identifier"),
        "responder_port_identifier": config.get("responder_port_identifier"),
        "local_password": config.get("local_password"),
        "peer_password": config.get("peer_password"),
        "heartbeat_interval": config.get("heartbeat_interval"),
        "heartbeat_deadfactor": config.get("heartbeat_deadfactor"),
        "version_number": config.get("version_number"),
        "hash_algorithm": config.get("hash_algorithm"),
    }

    if service_config["type"].lower() == "cltu":
        from sle.datatypes.cltu_structure import CltuParameterName

        parameters = str([n for n in CltuParameterName().namedValues])
        sle_service = sle.CltuServiceUser(**config_kwargs)

    elif config["type"].lower() == "raf":
        from sle.datatypes.raf_structure import RafParameterName

        parameters = str([n for n in RafParameterName().namedValues])
        sle_service = sle.RafServiceUser(**config_kwargs)

    elif config["type"].lower() == "rcf":
        from sle.datatypes.rcf_structure import RcfParameterName

        parameters = str([n for n in RcfParameterName().namedValues])
        sle_service = sle.RcfServiceUser(**config_kwargs)

    if dump_file:

        def frame_received(frame):
            if dump_file:
                dump_file.write(str(frame))

        sle_service.frame_indication = frame_received

    WAIT_DELAY = 5  # seconds to wait for SLE state change

    HELP_TEXT = """
    ==================
    SLE User Test Tool

    b = bind
    s = start
    r = schedule immediately status report
    g = get parameter
    p = stop
    u = unbind
    a = peer abort
    d = transfer data (only forward service)
    t = throw event
    h = show this help text
    q = quit
    ==================
    """
    print(HELP_TEXT)

    try:
        while True:
            time.sleep(0.5)
            cmd = input("Enter choice: ").lower()
            print()

            if cmd == "q":
                break
            if cmd == "h":
                print(HELP_TEXT)

            if cmd == "b":
                sle_service.bind()
                if not sle_service.wait_for_state(sle.SleState.READY, WAIT_DELAY):
                    print("Error during bind")

            elif cmd == "r":
                sle_service.schedule_status_report()

            elif cmd == "g":
                print(parameters)
                parameter = input("Select parameter: ")
                sle_service.get_parameter(parameter)

            elif cmd == "s":
                if isinstance(sle_service, sle.RcfServiceUser):
                    gvcid = [int(x) for x in config["gvcid"].split(",")]
                    sle_service.start(gvcid)
                else:
                    sle_service.start()
                if not sle_service.wait_for_state(sle.SleState.ACTIVE, WAIT_DELAY):
                    print("Error during start")

            elif cmd == "p":
                sle_service.stop()
                if not sle_service.wait_for_state(sle.SleState.READY, WAIT_DELAY):
                    print("Error during stop")

            elif cmd == "d" and isinstance(sle_service, sle.CltuServiceUser):
                data = input("Enter hex pattern of data: ")
                sle_service.transfer_data(bytearray.fromhex(data), notify=True)

            elif cmd == "t" and isinstance(sle_service, sle.CltuServiceUser):
                event_id, event_qualifier = input("Enter: ").split(",")
                sle_service.throw_event(event_id, event_qualifier)

            elif cmd == "u":
                sle_service.unbind()
                if not sle_service.wait_for_state(sle.SleState.UNBOUND, WAIT_DELAY):
                    print("Error during unbind")

            elif cmd == "a":
                sle_service.peer_abort()

    except KeyboardInterrupt:
        pass
    finally:
        if dump_file:
            dump_file.close()
