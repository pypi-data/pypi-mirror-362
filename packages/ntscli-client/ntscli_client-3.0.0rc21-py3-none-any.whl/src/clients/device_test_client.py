from src import __version__
from requests import Session, exceptions
from requests_toolbelt.utils import dump
from src.clients.e2e_token_client import E2ETokenClient
from urllib3.util import Retry
from src.log import logger
from src.exceptions import MissingMetatronException

class DeviceTestClient:

    retries = Retry(total=0, backoff_factor=0.1, status_forcelist=[])

    target_app_name = "wall_e"

    def __init__(self, net_key=None, use_netflix_access=False):
        self.url = "https://third-party-gateway.dta.netflix.net"
        self.port = 443
        self.session = Session()
        if net_key is not None:
            self.auth_header = "Authorization"
            self.auth_value = f"Bearer {net_key}"
        elif use_netflix_access:
            # leverage Metatron
            self.url = "https://third-party-gateway-mtls.dta.netflix.net"
            try:
                from metatron.http import MetatronAdapter
                self.auth_header = "X-Forwarded-Authentication"
                self.auth_value = E2ETokenClient().get_e2e_token(DeviceTestClient.target_app_name)['token']
                self.session.mount(self.__get_url_with_port(), MetatronAdapter(DeviceTestClient.target_app_name, max_retries=DeviceTestClient.retries))
            except ImportError:
                raise MissingMetatronException()
        else:
            raise Exception("User is not authenticated")

    def get_test_plan(self, esn: str):
        resp = self.session.get(f"{self.__get_url_with_port()}/test-plan/esn/{esn}?format=marathonlite", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            claim_device_message = "Device must be claimed to get a testplan."
            if e.response.text is not None and claim_device_message in e.response.text:
                raise Exception(claim_device_message)
            logger.error(f"Failed to get test plan: {e}")
            raise Exception("Failed to get test plan")
        return resp.json()

    def get_playlist_test_plan(self, playlist_id: str, esn: str):
        resp = self.session.get(f"{self.__get_url_with_port()}/playlist/id/{playlist_id}/esn/{esn}?format=marathonlite", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to get playlist test plan: {e}")
            raise Exception("Failed to get playlist test plan")
        return resp.json()

    def get_dynamic_filter_test_plan(self, dynamic_filter_id: str, esn: str, sdk_or_apk: str):
        sdk_or_apk_query_param = f"&singleNamespaceFilter={sdk_or_apk}" if sdk_or_apk else ""
        resp = self.session.get(f"{self.__get_url_with_port()}/dynamic-filter/id/{dynamic_filter_id}/esn/{esn}?format=marathonlite{sdk_or_apk_query_param}", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to get dynamic filter test plan: {e}")
            raise Exception("Failed to get dynamic filter test plan")
        return resp.json()

    def get_status(self, rae: str, esn: str):
        query_params = f"rae={rae}" if rae is not None else f"esn={esn}"
        resp = self.session.get(f"{self.__get_url_with_port()}/device-status?{query_params}", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to get status: {e}")
            raise Exception("Failed to get status")
        return resp.json()

    def get_eleven_calibration_plan(self, esn: str):
        resp = self.session.get(f"{self.__get_url_with_port()}/eleven/calibration/esn/{esn}?format=marathonlite", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to get eleven calibration plan: {e}")
            raise Exception("Failed to get eleven calibration plan")
        return resp.json()

    def get_eyepatch_calibration_plan(self, esn: str, form_factor: str, smart_tv_topology: str, stb_topology: str, audio_source: str, audio_mode: str, eyepatch_serial: str):
        resp = self.session.get(f"{self.__get_url_with_port()}/eyepatch/calibration/esn/{esn}?format=marathonlite", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to get eyepatch calibration plan: {e}")
            raise Exception("Failed to get eyepatch calibration plan")
        plan = resp.json()
        plan["test_overrides"] = self.__get_eyepatch_calibration_plan_overrides(form_factor, smart_tv_topology, stb_topology, audio_source, audio_mode, eyepatch_serial)
        return plan

    def run_test_plan(self, plan):
        overrides = { "test_log_level": "warning" }
        plan_overrides = plan.get("test_overrides", {})

        overrides.update(plan_overrides)
        #TODO: determine whether we should make these user configurable parameters
        plan["target_profiles"] = [ { "esn": plan["esn"] } ]
        plan["test_overrides"] = overrides
        plan["stress_count"] = 0
        plan["retry_count"] = 0

        resp = self.session.post(f"{self.__get_url_with_port()}/testruns/launch/nts/batch", json=plan, headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            device_already_reserved_message = "Device has already been reserved"
            if e.response.text is not None and device_already_reserved_message in e.response.text:
                raise Exception(device_already_reserved_message)
            logger.error(f"Failed to run test plan: {e}")
            raise Exception("Failed to run test plan")
        return {
            "batchId": resp.json()["batch_id"]
        }

    def cancel_test_plan_run(self, batch_id: str, esn: str):
        json = { "esn" : esn }
        resp = self.session.post(f"{self.__get_url_with_port()}/testruns/cancel/batch/{batch_id}", json=json, headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            logger.error(f"Failed to cancel test plan run: {e}")
            raise Exception("Failed to cancel test plan run")
        return {
            "batchId": resp.json()["batch_id"],
            "details": resp.json()["details"]
        }

    def get_run_plan_summary(self, batch_id: str):
        resp = self.session.get(f"{self.__get_url_with_port()}/batch/results/batchId/{batch_id}", headers=self.__get_headers())
        self.__log_resp(resp)
        try:
            resp.raise_for_status()
        except exceptions.HTTPError as e:
            if resp.status_code == 404:
                logger.debug(f"Test plan run summary is not yet available for batchId {batch_id}")
                return { "batchId": batch_id }
            else:
                logger.error(f"Failed to get test plan run summary: {e}")
                raise Exception("Failed to get test plan run summary")
        return self.__extract_cli_summary(resp.json())

    def __get_eyepatch_calibration_plan_overrides(self, form_factor, smart_tv_topology, stb_topology, audio_source, audio_mode, eyepatch_serial):
        overrides = {
            "promptChoice_formFactor": "positive",
            "promptInput_formFactor": form_factor.lower(),
            "promptChoice_audioSource": "positive",
            "promptInput_audioSource": audio_source.lower(),
            "promptChoice_audioMode": "positive",
            "promptInput_audioMode": audio_mode.lower(),
            "skipPrompt": "true"
        }

        # Optional overrides
        if eyepatch_serial is not None:
            overrides["promptChoice_epchoice"] = "positive"
            overrides["promptInput_epchoice"] = eyepatch_serial
        if stb_topology is not None:
            overrides["promptChoice_stbTopology"] = "positive"
            overrides["promptInput_stbTopology"] = stb_topology.lower()
        if smart_tv_topology is not None:
            overrides["promptChoice_smartTvTopology"] = "positive"
            overrides["promptInput_smartTvTopology"] = smart_tv_topology.lower()

        return overrides

    def __get_url_with_port(self):
        return f"{self.url}:{self.port}"

    def __get_headers(self):
        return {
            self.auth_header: self.auth_value,
            "Content-Type": "application/json",
            # Wall-E overrides client.appId but not the user agent.
            "x-netflix.client.appid": "nts-cli",
            "User-Agent": f"nts-cli/{__version__.__version__}"
        }

    def __log_resp(self, resp):
        data = dump.dump_all(resp)
        logger.debug(data.decode('utf-8'))

    def __extract_cli_summary(self, results):
        summary = results["summary"]
        return {
            "batchId": summary.get("batchId"),
            "passed": summary.get("passed"),
            "failed": summary.get("failed"),
            "timedout": summary.get("timedout"),
            "canceled": summary.get("canceled"),
            "invalid": summary.get("invalid"),
            "running": summary.get("running"),
            "pending": summary.get("pending"),
            "total": summary.get("total")
        }
