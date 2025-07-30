import json

from src.clients.device_test_client import DeviceTestClient

indent = 4

def run_eleven_calibration_impl(esn: str, out_file, net_key: str, use_netflix_access: bool):
    device_test_client = DeviceTestClient(net_key, use_netflix_access)

    plan = device_test_client.get_eleven_calibration_plan(esn)
    run_resp = device_test_client.run_test_plan(plan)

    run_summary = device_test_client.get_run_plan_summary(run_resp["batchId"])

    json.dump(run_summary, out_file, indent=indent)
