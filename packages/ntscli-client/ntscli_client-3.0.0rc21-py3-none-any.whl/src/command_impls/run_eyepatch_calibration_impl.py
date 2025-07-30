import json

from src.clients.device_test_client import DeviceTestClient

indent = 4

def run_eyepatch_calibration_impl(esn: str, form_factor: str, smart_tv_topology: str, stb_topology: str, audio_source: str, audio_mode: str, eyepatch_serial: str, out_file, net_key: str, use_netflix_access: bool):
    device_test_client = DeviceTestClient(net_key, use_netflix_access)

    plan = device_test_client.get_eyepatch_calibration_plan(esn, form_factor, smart_tv_topology, stb_topology, audio_source, audio_mode, eyepatch_serial)
    run_resp = device_test_client.run_test_plan(plan)

    run_summary = device_test_client.get_run_plan_summary(run_resp["batchId"])

    json.dump(run_summary, out_file, indent=indent)
