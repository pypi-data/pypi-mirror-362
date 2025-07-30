import os
import uuid
import pandas as pd
import json
from typing import List, Optional, Any, Dict, Callable
from dataclasses import field
from datetime import datetime
import hashlib
import base64
import requests
from packaging.version import Version
from tqdm.auto import tqdm
import asyncio
import time
from wakepy import keep
from contextlib import nullcontext

from vijil.api import (
    make_api_request,
    get_api_proxy_dict,
    BASE_URL,
    SUPPORTED_HUBS,
    DEFAULT_DETECTOR_PARAMS,
    DETECTOR_LIST,
)
from vijil.types import VijilClient
from vijil.utils import calculate_md5_base64
from vijil.agents._server import start_ngrok_server, LocalServer
from vijil.agents.executor import LocalAgentExecutor
from vijil.agents.constants import TERMINAL_STATUSES, API_URL_TO_USER_URL_MAP

ERROR_SKIP_KEYS = ["ERROR", "SKIP"]
HUB_CONFIG_FIELDS = {
    "vertex": ["region", "project_id", "client_id", "client_secret", "refresh_token"],
    "digitalocean": ["agent_id", "agent_key"],
}
HUBS_NEEDING_URL = ["custom", "bedrock_custom", "azure", "digitalocean"]
HUBS_NOT_NEEDING_MODEL_NAME = ["digitalocean"]
FORMAT_OPTIONS = ["dataframe", "list"]
TYPE_OPTIONS = [None, "benchmark", "audit", "dimension", "custom"]
DIMENSION_LIST = [
    "security",
    "privacy",
    "hallucination",
    "robustness",
    "toxicity",
    "stereotype",
    "fairness",
    "ethics",
    "Performance",
]
AGENT_DIMENSION_LIST = [
    "security",
    "privacy",
    "hallucination",
    "robustness",
    "toxicity",
    "stereotype",
    "fairness",
    "ethics",
]

STANDALONE_HARNESSES = ["trust_score", "llm_trust_score"]
CUSTOM_HARNESS_TYPES = [
    "AGENT_POLICY",
    "KNOWLEDGE_BASE",
    "FUNCTION_ROUTE",
    "PERSONA",
]

def modify_hub(model_hub: str):
    if model_hub == "bedrock":
        return "bedrock_custom"
    return model_hub


class APIKeys:
    """
    Class for managing model hub API keys, which are required to query models.

    :param client: The Vijil client instance.
    :type client: VijilClient
    """

    def __init__(self, client: VijilClient) -> None:
        """Constructor class

        :param client: The Vijil client instance.
        :type client: VijilClient
        """
        self.endpoint = "api-keys"
        self.client = client
        pass

    def list(self):
        """List all stored model hub API keys.

        :return: List of dictionaries. Each dictionary contains information about an API key.
        :rtype: List(dict)
        """
        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            token=self.client.api_key,
        )
        return response

    def get_id_by_name(self, name: str):
        """Get the id of a key by its name. Used by other functions to get the id of a key to modify.

        :param name: The name of the key.
        :type name: str
        :return: The id of the key.
        :rtype: str
        """

        if not self.name_exists(name):
            raise ValueError(
                f"Key '{name}' does not exist. Please specify an existing name."
            )

        # get id of key to modify
        response = self.list()
        return [item["id"] for item in response if item["name"] == name][0]

    def check_model_hub(self, model_hub: str):
        """Used by other functions to check that the model hub is valid and the key name is unique

        :param model_hub: The name of the model hub.
        :type model_hub: str
        :raises ValueError: If the model hub is not supported.
        """

        model_hub = modify_hub(model_hub)

        # check if model_hub is valid
        if (model_hub is not None) and (model_hub not in SUPPORTED_HUBS.keys()):
            raise ValueError(f"Model hub {model_hub} is not supported.")

    def name_exists(self, name: str):
        """Check whether the API key name already exists. Some functions need it to be exist, others need it to not exist.

        :param name: The name of the key.
        :type name: str
        :return: True if the name exists among the stored API keys, False otherwise.
        :rtype: bool
        """

        response = self.list()
        if response is not None and name in [item["name"] for item in response]:
            return True
        else:
            return False

    def create(
        self,
        name: str,
        model_hub: str,
        rate_limit_per_interval: int = 60,
        rate_limit_interval: int = 10,
        api_key: Optional[str] = None,
        hub_config: Optional[dict[Any, Any]] = None,
        url: Optional[str] = None,
    ):
        """Create a new model hub API key.

        :param name: Name for the API key. This must be unique.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        :raises ValueError: If you try to create a key with a name that belongs to an existing key.
        :return: Response to the API request.
        :rtype: dict
        :param api_key: The API key.
        :type api_key: str, optional
        :param hub_config: A dictionary containing additional configuration for the model hub. Defaults to None.
        :type hub_config: dict, optional
        """
        # conditional checks for fields
        model_hub = modify_hub(model_hub)

        # hub name
        self.check_model_hub(model_hub=model_hub)

        # api key name
        if self.name_exists(name):
            raise ValueError(
                f"Key name '{name}' already exists. Please specify a different name."
            )

        # hub config and api key for vertex
        if model_hub in HUB_CONFIG_FIELDS.keys():
            api_key = ""
            if hub_config is None or not all(
                [field in hub_config for field in HUB_CONFIG_FIELDS[model_hub]]
            ):
                raise ValueError(
                    f"Please provide the following fields in the hub_config for {SUPPORTED_HUBS[model_hub]}: {HUB_CONFIG_FIELDS[model_hub]}"
                )
        else:
            if hub_config is not None:
                raise ValueError(
                    f"Hub config is only needed for {SUPPORTED_HUBS[model_hub]}. Please remove it for other model hubs."
                )
            if api_key is None:
                raise ValueError("Please provide an API key.")

        # construct the payload
        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
            "url": url,
        }
        if hub_config:
            payload["hub_config"] = hub_config

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key,
        )

    def rename(self, name: str, new_name: str):
        """Rename a stored API key

        :param name: The current name of the key.
        :type name: str
        :param new_name: The new name of the key.
        :type new_name: str
        """

        key_id = self.get_id_by_name(name=name)

        payload = {"name": new_name}

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key,
        )

    def modify(
        self,
        name: str,
        model_hub: str,
        api_key: Optional[str] = None,
        rate_limit_per_interval=None,
        rate_limit_interval=None,
    ):
        """Modify model hub, key, or rate limits of a stored API key. Cannot be used to rename key.

        :param name: The name of the key you want to modify.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str, optional
        :param api_key: The API key.
        :type api_key: str, optional
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        """

        # check that model hub is supported and key name refers to existing name
        self.check_model_hub(model_hub=model_hub)

        key_id = self.get_id_by_name(name=name)

        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
        }

        # remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key,
        )

    def delete(self, name: str):
        """Delete API key with specified name

        :param name: The name of the key you want to delete
        :type name: str
        :return: Response to the API request.
        :rtype: dict
        """

        key_id = self.get_id_by_name(name=name)

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="delete",
            token=self.client.api_key,
        )


class Harnesses:
    """Class for handling harnesses API requests.

    :param client: The VijilClient instance.
    :type client: VijilClient
    """

    def __init__(self, client: VijilClient) -> None:
        """Initialize the Harnesses class.

        :param VijilClient client: The VijilClient instance.
        :type client: VijilClient
        """
        self.endpoint = "harness-configs"
        self.client = client
        pass

    def calculate_md5_base64(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            md5_hash = hashlib.md5(file.read()).digest()
            return base64.b64encode(md5_hash).decode()

    def calculate_file_size(self, file_path):
        return os.path.getsize(file_path)

    def list(self, type: Optional[str] = None, format: str = "dataframe"):
        """List all harnesses.

        :return: List of dicts where each dict contains the metadata for a harness.
        :rtype: List(dict)
        """
        # input validation
        if format not in FORMAT_OPTIONS:
            raise ValueError("Invalid format. Must be 'dataframe' or 'list'.")
        if type not in TYPE_OPTIONS:
            raise ValueError(f"Invalid type. Must be one of {TYPE_OPTIONS}.")

        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            token=self.client.api_key,
            params={"limit": 10000},
        )
        harness_list = pd.DataFrame.from_records(
            [h["harness_config"] for h in response["results"]]
        )

        # filter by type if specified
        if type is not None:
            harness_list = harness_list[
                harness_list["harness_type"].str.contains(type.upper(), na=False)
            ]
            if (
                type == "dimension"
            ):  # further filter to small only if type is 'dimension'
                harness_list = harness_list[
                    harness_list["id"].str.contains("_Small", na=False)
                ]

        # # filter for latest versions
        unique_harnesses = list(set(harness_list["id"].tolist()))
        unique_harness_list = []
        for h in unique_harnesses:
            id_harness = harness_list[harness_list["id"] == h]
            versions = []
            for v in id_harness["version"]:
                try:
                    versions.append(Version(v))
                except Exception as e:  # noqa: F841
                    continue

            # control for None being the only version
            if len(versions) > 0:
                max_version_row = id_harness[
                    id_harness["version"] == str(max(versions))
                ].iloc[0]
            else:
                max_version_row = id_harness.iloc[0]
            unique_harness_list.append(max_version_row)

        unique_harness_df = pd.concat(unique_harness_list, axis=1).T.reset_index(
            drop=True
        )
        unique_harness_df["id"] = unique_harness_df["id"].apply(
            lambda x: ".".join(x.split(".")[2:])
        )  # drop prefix 'vijil.harnesses.'
        unique_harness_df = unique_harness_df[["id", "name", "description"]]
        if format == "list":
            return unique_harness_df.to_dict(orient="records")
        return unique_harness_df

    def create(
        self,
        name: str,
        system_prompt: str,
        category: List[str],
        description: Optional[str] = "",
        policy_file_path: Optional[str] = None,
        kb_bucket: Optional[str] = None,
        input_schema: Optional[Dict[str, Any]] = {},
        output_schema: Optional[Dict[str, Any]] = {},
        function_route: Optional[str] = "",
        persona_ids: Optional[List[str]] = [],
    ):
        """
        Create a custom harness from a system prompt and file.

        :param name: The name of the harness.
        :param system_prompt: The system prompt for the model you're testing.
        :param category: The category of the harness. Options are "AGENT_POLICY", "KNOWLEDGE_BASE", "FUNCTION_ROUTE", "PERSONA"
        :param policy_file_path: The path to the policy document (pdf or txt). Applicable to an agent policy harness. Defaults to "".
        :param kb_bucket: The bucket name for the knowledge base. Must be specified if you want to include a knowledge base harness. Defaults to "".
        :param input_schema: The input schema to be used for harness creation. Applicable to a tool-calling agent. Defaults to {}.
        :param output_schema: The output schema to be used for harness creation. Applicable to a tool-calling agent. Defaults to {}.
        :param function_route: The function route to be used for harness creation. Applicable to a tool-calling agent. Defaults to "".
        :param persona_ids: The persona IDs to be used for harness creation. Applicable to a persona harness. Defaults to [].
        """
        # initial validation
        if (
            "AGENT_POLICY" in category
            and (not policy_file_path)
            and not (system_prompt)
        ):
            raise ValueError(
                "For AGENT_POLICY category, policy_file_path or system_prompt must be specified."
            )
        elif "FUNCTION_ROUTE" in category and (
            not function_route or not input_schema or not output_schema
        ):
            raise ValueError(
                "For FUNCTION_ROUTE category, function_route must be specified and input_schema and output_schema must be empty."
            )
        elif "KNOWLEDGE_BASE" in category:
            if not kb_bucket:
                raise ValueError(
                    "For KNOWLEDGE_BASE category, kb_bucket must be specified."
                )
        elif "PERSONA" in category and not persona_ids:
            raise ValueError(
                "For PERSONA category, persona_ids must be specified as a list of persona IDs."
            )
        # check if none of the allowed types are present in category
        elif not any(cat in CUSTOM_HARNESS_TYPES for cat in category):
            raise ValueError(
                f"Invalid category. Category must be one of {CUSTOM_HARNESS_TYPES}."
            )

        # step 1: staging api call
        harness_config_id = str(uuid.uuid4())
        staging_payload = {
            "harness_config_version": "1.0.X",
            "harness_name": name,
            "agent_system_prompt": system_prompt,
        }
        try:
            staging_response = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"{self.endpoint}/{harness_config_id}/stages",
                method="post",
                data=staging_payload,
                token=self.client.api_key,
            )
            staging_id = staging_response.get("id")
        except Exception as e:
            raise ValueError(f"Failed to initialize harness staging: {e}")

        # step 2 and step 2.5: only if policy files are there
        if "AGENT_POLICY" in category and policy_file_path:
            # step 2: get a signed URL with file info
            file_size = os.path.getsize(policy_file_path)  # type: ignore
            checksum = calculate_md5_base64(policy_file_path)  # type: ignore
            # file must be .pdf or  .txt
            if policy_file_path.endswith(".pdf"):
                file_type = "application/pdf"
            elif policy_file_path.endswith(".txt"):
                file_type = "text/plain"
            else:
                raise ValueError("Policy file must be a .pdf or .txt file.")

            signed_url_payload = {
                "category": "AGENT_POLICY",
                "file_name": policy_file_path,  # just take raw filename
                "file_size": file_size,
                "file_type": file_type,
                "checksum": checksum,
            }
            try:
                signed_url_response = make_api_request(
                    base_url=self.client.base_url,
                    endpoint=f"{self.endpoint}/{harness_config_id}/stages/{staging_id}/files",
                    method="post",
                    data=signed_url_payload,
                    token=self.client.api_key,
                )
            except Exception as e:
                raise ValueError(f"Failed to create signed URL for policy upload: {e}")

            # step 3: upload file using signed URL
            with open(policy_file_path, "rb") as f:  # type: ignore
                policy_content = f.read()
            try:
                file_upload_response = requests.put(
                    signed_url_response["upload_url"],
                    data=policy_content,
                    headers={"Content-Type": file_type, "Content-MD5": checksum},
                )
            except Exception as e:
                raise ValueError(f"Failed to upload policy file: {e}")
            if file_upload_response.status_code != 200:
                raise ValueError(
                    f"Failed to upload policy file: {file_upload_response.text}"
                )

            # step 3: verify file upload
            try:
                make_api_request(
                    base_url=self.client.base_url,
                    endpoint=f"{self.endpoint}/{harness_config_id}/stages/{staging_id}/files",
                    method="get",
                    params={"staging_id": staging_id},
                    token=self.client.api_key,
                )
            except Exception as e:
                raise ValueError(f"Policy file not uploaded: {e}")

        # step 4: staging complete api call
        function_route_params = (
            {
                "input_schema": str(input_schema),
                "output_schema": str(output_schema),
                "function_route": function_route,
            }
            if "FUNCTION_ROUTE" in category
            else None
        )
        rag_params = (
            {"bucket_name": kb_bucket} if "KNOWLEDGE_BASE" in category else None
        )
        persona_params = (
            {"persona_ids": persona_ids} if "PERSONA" in category else None
        )
        
        try:
            staging_complete_response = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"{self.endpoint}/{harness_config_id}/stages/{staging_id}",
                method="put",
                data={
                    "harness_types": category,
                    "function_route_params": function_route_params,
                    "rag_params": rag_params,
                    "persona_params": persona_params
                },
                token=self.client.api_key,
            )
        except Exception as e:
            raise ValueError(f"Failed to create harness: {e}")
        
        if staging_complete_response.get("status") != "CREATED":
            raise ValueError(f"Failed to create staging: {staging_complete_response.get('error')}")

        # stage 5: send harness creation request
        eval_config_input = {
            "harness_description": description if description else "",
            # since system prompt is always there, we always include these two
            "include_correctness": True,
            "include_exfil": True
        }
        if "AGENT_POLICY" in category:
            eval_config_input["include_adherence"] = True
        if "FUNCTION_ROUTE" in category:
            eval_config_input["include_tool"] = True
        if "PERSONA" in category:
            eval_config_input["include_persona"] = True
        try:
            _ = make_api_request(
                base_url=self.client.base_url,
                endpoint="harness-creation-agent",
                method="post",
                data={
                    "harness_staging_id": staging_id,
                    "eval_config_input": eval_config_input,
                },
                token=self.client.api_key,
            )
        except Exception as e:
            raise ValueError(f"Failed to create harness: {e}")

        return {
            "harness_name": name,
            "harness_config_id": harness_config_id,
            "status": staging_complete_response.get("status"),
        }

    def get_status(self, harness_id: str):
        """
        Get the status of a harness.

        :param harness_id: The ID of the harness.
        :return: The status of the harness.
        :rtype: str
        """
        all_status = make_api_request(
            base_url=self.client.base_url,
            endpoint="harness-config-stages",
            token=self.client.api_key,
        ).get("results")
        for status in all_status:
            if status.get("harness_config_id") == harness_id:
                return status

        return f"Harness {harness_id} not found. Please check the ID and try again."

    def delete(self, harness_id: str):
        """
        Not implemented yet.
        """
        raise NotImplementedError("Delete harnesses is not implemented yet.")

        # if request is succeessful, return the harness id, name, and a "submitted" message
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=f"harness-configs/{harness_id}",
            method="delete",
            token=self.client.api_key,
        )


class AnalysisReports:
    def __init__(
        self, client: VijilClient, evaluation_id: str, evaluation_metadata: dict
    ) -> None:
        self.client = client
        # By specifying the evaluation metadata as a requirement, we avoid a circular dependency
        # Otherwise AnalysisReports needs evaluations to be defined, and evaluations needs AnalysisReports for the reports function signature
        self.evaluation_metadata = evaluation_metadata
        self.evaluation_id = evaluation_id

    def _list_reports(self, status: Optional[str] = "CREATED"):
        """
        List all the reports for an evaluation
        """
        try:
            response = make_api_request(
                base_url=f"{self.client.base_url}/evaluations/{self.evaluation_id}",
                endpoint="list-reports",
                token=self.client.api_key,
                params={"status": status},
            )
            return response["report_ids"]
        except Exception as e:
            raise ValueError(
                f"Error listing reports for evaluation {self.evaluation_id} : {e}"
            )

    def _get_analysis_report_by_id(self, report_id: str):
        """
        Get the report given eval ID and report ID
        """
        try:
            response = make_api_request(
                base_url=f"{self.client.base_url}/evaluations/{self.evaluation_id}/reports",
                endpoint=report_id,
                token=self.client.api_key,
            )
            return response
        except Exception as e:
            raise ValueError(
                f"Error fetching report {report_id} for evaluation {self.evaluation_id} : {e}"
            )

    def _request_analysis_report(self):
        try:
            # First check the tag
            evaluation_tag = self.evaluation_metadata.get("tags")
            if evaluation_tag is None:
                # Old evaluations may not have tags
                raise ValueError(
                    "Reports can only be generated for evaluations with Tags. Your evaluation was likely generated with an older version of Vijil Evaluate. Please create a new evaluation."
                )
            disallowed_tags = ["benchmarks"]
            for disallowed_tag in disallowed_tags:
                if disallowed_tag in evaluation_tag:
                    raise ValueError(
                        f"The evaluation {self.evaluation_id} is tagged {disallowed_tag}. Reports cannot be generated for evaluations with this tag."
                    )

            response = make_api_request(
                base_url=f"{self.client.base_url}/evaluations/{self.evaluation_id}",
                endpoint="reports",
                method="POST",
                token=self.client.api_key,
                data={"version": self.client.get_latest_objects_version()},
            )
            return response
        except Exception as e:
            raise ValueError(
                f"Error requesting report for evaluation {self.evaluation_id} : {e}"
            )

    def _save_report(self, report_content: str, save_file: str, format: str) -> None:
        """
        Save the report content to a file in the specified format.

        :param report_content: The content of the report.
        :param save_file: The file path to save the report.
        :param format: The format of the report ('html' or 'pdf').
        """
        if format == "html":
            with open(save_file, "w", encoding="utf-8") as f:
                f.write(report_content)
        elif format == "pdf":
            # Import only if you need to
            from weasyprint import HTML
            from bs4 import BeautifulSoup

            # Parse the HTML content
            soup = BeautifulSoup(report_content, "html.parser")

            # Delete all collapsible buttons
            for button in soup.find_all("button", class_="collapsible"):
                button.decompose()

            # Delete all plotly divs
            for div in soup.find_all("div", class_="graph-container"):
                div.decompose()

            # Replace all collapsible content divs with regular divs
            for div in soup.find_all("div", class_="collapsible-content"):
                div.name = "div"
                del div["class"]

            # Add CSS to make all text left-justified and ensure it's applied globally
            body_content = str(soup.prettify())
            report_content = f"""  # type: ignore[str-bytes-safe]
            <style>
                body {{
                    font-size: 12px;
                }}
            </style>
            {body_content}
            """

            # Render the updated HTML to PDF
            HTML(string=report_content).write_pdf(save_file)

    def generate(
        self,
        save_file: Optional[str] = None,
        wait_till_completion: bool = True,
        poll_frequency: int = 5,
        format="html",
    ) -> None | str:
        """
        Generates an analysis report for the evaluation.
        First checks to see if a report already exists, if so, it fetches the most recent report.
        Otherwise, a request is sent to create a report. If wait_till_completion is true, we wait till the report generation process is completed.
        """

        # This is the max report generation time on backend as well, so in theory we should not need to do this wait
        # That said, it can't hurt to be safe :)

        if not save_file:
            save_file = f"{self.evaluation_id}-report.{format}"
        else:
            ext = save_file.split(".")[-1]
            if ext not in ["html", "pdf"]:
                raise ValueError(
                    "The analysis report is generated as an HTML file. Please use a .html or .pdf file extension"
                )

        MAX_REPORT_TIME = 3 * 60
        available_reports = self._list_reports()
        if available_reports:
            # Use the most recent report ID
            latest_report = self._get_analysis_report_by_id(available_reports[0])
            report_content = latest_report.get("report_content", None)
            if not report_content:
                raise ValueError(
                    f"Report {available_reports[0]} for evaluation {self.evaluation_id} is not available."
                )

            self._save_report(report_content, save_file, format)
            print(
                f"Report {available_reports[0]} for evaluation {self.evaluation_id} was saved to {save_file}"
            )
            return None

        # No created reports - check if one is currently being generated
        # Reports are in descending order of creation time already
        ongoing_reports = self._list_reports(status=None)
        report_id = None
        report_status_message = None
        if ongoing_reports:
            for ongoing_report_id in ongoing_reports:
                report = self._get_analysis_report_by_id(ongoing_report_id)
                if report.get("report_status") != "FAILED":
                    report_id = report.get("report_id")
                    report_status_message = report.get("report_status_message")
                    break

        if not report_id:
            # No reports available. Create one
            report_request = self._request_analysis_report()
            report_id = report_request["report_id"]
            report_status_message = (
                "Creating your evaluation report - check back in after a minute."
            )

        if not wait_till_completion:
            print(f"Report ID {report_id} in progress. Status: {report_status_message}")
            return report_id

        start_time = time.time()
        current_status_message = None
        while time.time() - start_time < MAX_REPORT_TIME:
            try:
                current_report = self._get_analysis_report_by_id(report_id)
                status = current_report.get("report_status")
                status_message = current_report.get("report_status_message")
                if status_message != current_status_message:
                    current_status_message = status_message
                    print(status_message + ".....")
                if status in ("CREATED", "FAILED"):
                    report_content = current_report.get("report_content", None)
                    self._save_report(report_content, save_file, format)
                    print(
                        f"Report {report_id} for evaluation {self.evaluation_id} was saved to {save_file}"
                    )
                    return None
            except Exception as e:
                raise ValueError(
                    f"An error occurred while checking the report status: {e}"
                )
            time.sleep(poll_frequency)

        raise TimeoutError(
            f"Timed out waiting for report {report_id} to complete after {MAX_REPORT_TIME} seconds."
        )


class Evaluations:
    """Class for handling evaluations API requests.

    :param client: The VijilClient instance.
    :type client: VijilClient
    """

    def __init__(self, client: VijilClient) -> None:
        self.endpoint = "evaluations"
        self.client = client
        self.api_proxy_dict: dict = field(default_factory=dict)
        self.detectors = Detectors(client)

    def list(self, limit=10):
        """List all valuations. Will return only 10 evaluations unless specified.

        :param limit: The number of evaluations to return, defaults to 10.
        :type limit: int, optional
        """

        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "?limit=" + str(limit),
            token=self.client.api_key,
        )
        return response["results"]

    def list_harnesses_for_type(self, harness_types: List[str], latest_version: bool = True):
        try:
            response = make_api_request(
                base_url=self.client.base_url,
                endpoint="harness-configs",
                token=self.client.api_key,
                params={
                    "harness_type": harness_types,
                    "limit": 1000,
                    "offset": 0,
                    "version": self.client.get_latest_objects_version() if latest_version else None,
                },
            )
            results = response.get("results", [])
            harness_ids = []
            for result in results:
                harness_config = result.get("harness_config", {})
                harness_ids.append(harness_config.get("id", None))
            return harness_ids
        except Exception as e:
            raise ValueError(
                f"An error occured while listing the available harnesses for types {harness_types} : {e}"
            )

    def get_harness_tags(self, harness_names=List[str]):
        """
        Given the list of harnesses, ensure they belong to the same tag group and get the tag group.
        This is to ensure they are all on the correct UI page
        """
        try:
            # Check for standalone harnesses first
            for harness in harness_names:
                if harness in STANDALONE_HARNESSES and len(harness_names) > 1:
                    raise ValueError(
                        f"The harness {harness} is a standalone harness, and cannot be tested with other harnesses in the same evaluation"
                    )
            if len(harness_names) == 1 and harness_names[0] in STANDALONE_HARNESSES:
                return "DIMENSION"

            full_harness_names = [f"vijil.harnesses.{h}" for h in harness_names]
            vijil_dimension_harnesses = self.list_harnesses_for_type(["DIMENSION"])
            vijil_benchmark_harnesses = self.list_harnesses_for_type(
                ["BENCHMARK_SECURITY", "BENCHMARK_SAFETY", "BENCHMARK_RELIABILITY"]
            )
            vijil_custom_harnesses = self.list_harnesses_for_type(["CUSTOM"], latest_version=False)
            vijil_scenario_harnesses = self.list_harnesses_for_type(["SCENARIO"])
            vijil_audit_harnesses = self.list_harnesses_for_type(["AUDIT"])

            # Since the UI doesn't treat audits differently, they're merged with dimensions

            type_to_harnesses = {
                "DIMENSION": vijil_dimension_harnesses + vijil_audit_harnesses,
                "BENCHMARK": vijil_benchmark_harnesses,
                "CUSTOM": vijil_custom_harnesses + vijil_audit_harnesses,
                "SCENARIO": vijil_scenario_harnesses,
            }

            matched_types = []

            for harness_type, harness_set in type_to_harnesses.items():
                if all(h in harness_set for h in full_harness_names):
                    matched_types.append(harness_type)

            if len(matched_types) == 1:
                return matched_types[0]
            elif not matched_types:
            # elif not matched_types and harness_type != "CUSTOM":
                raise ValueError(
                    f"None of the harnesses were found in a single tag group: {harness_names}"
                )
            else:
                raise ValueError(
                    f"Harnesses belong to multiple tag groups: {matched_types} for {harness_names}"
                )

        except Exception as e:
            raise ValueError(
                f"An error occured while obtaining the tags for harnesses {harness_names} : {e}"
            )

    def create(
        self,
        model_hub: str,
        harness_version: Optional[str] = None,
        model_name: Optional[str] = None,
        name: Optional[str] = None,
        api_key_name: Optional[str] = None,
        model_url: Optional[str] = None,
        model_params={},
        harness_params={},
        harnesses=[],
        tags: Optional[List[str]] = None,
    ):
        """Create a new evaluation.

        :param model_hub: The model hub you want to use. Supported options are "openai", "together", "digitalocean", "custom".
        :type model_hub: str
        :param harness_version: The version of the harness you want to use.
        :type harness_version: str
        :param model_name: The name of the model you want to use. Check the model hub's API documentation to find valid names.
        :type model_name: str, optional
        :param name: The name of the evaluation. If not specified, model hub will be concatenated with model name.
        :type name: str, optional
        :param api_key_name: The name of the model hub API key you want to use. If not specified, will use the first key we find for the specified model_hub.
        :type api_key_name: str, optional
        :param model_url: The URL of the model you want to use. Only required for custom model hub. Defaults to None
        :type model_url: str, optional
        :param model_params: A dictionary specifying inference parameters like temperature and top_p. If none are specified, model hub defaults will be used. Defaults to {}
        :type model_params: dict, optional
        :param harness_params: Set optional parameters like is_lite, defaults to {}
        :type harness_params: dict, optional
        :param harnesses: A list of harnesses you want to include in the evaluation, defaults to []
        :type harnesses: List[str], optional
        :params tags: A list of tags to use when creating the evaluation. These control how the evaluation gets displayed in the Vijil UI. Defaults to None, which sets the page automatically
        :type tags: List[str], optional
        :raises TypeError: If you have no API keys stored.
        :raises ValueError: If you have no API keys stored for the specified model hub.
        :raises ValueError: If you supply an api_key_name that does not exist.
        :raises ValueError: If you specify lite mode for any harness other than ethics.
        :return: API response containing evaluation ID of the newly created evaluation.
        :rtype: dict
        """

        model_hub = modify_hub(model_hub)

        if not harness_version:
            harness_version = self.client.get_latest_objects_version()

        # store all api keys in a dictionary if not there
        if self.api_proxy_dict.__class__.__name__ == "Field":
            try:
                self.api_proxy_dict = get_api_proxy_dict(
                    base_url=self.client.base_url, token=self.client.api_key
                )
            except TypeError:
                raise TypeError("No API keys found. Please upload an API key first.")

        # get api key proxy for the model hub
        try:
            hub_api_proxy_dict = self.api_proxy_dict[model_hub]
        except KeyError:
            raise ValueError(f"No API key stored for model hub {model_hub}")

        # get api key proxy for the model hub
        if api_key_name is not None:
            # find api key id for the api key name
            if api_key_name not in hub_api_proxy_dict.keys():
                raise ValueError(f"No API key found for name {api_key_name}")
            else:
                api_key_proxy = hub_api_proxy_dict[api_key_name]
        else:  # if no key specified, use first value in hub dictionary
            api_key_proxy = next(iter(hub_api_proxy_dict.values()))

        # create the payload
        payload = {
            # "name": name if name else f"{SUPPORTED_HUBS[model_hub]}-{model_name}",
            "name": name
            if name
            else f"{SUPPORTED_HUBS[model_hub]}-{model_name}-{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}",
            "id": str(uuid.uuid4()),
            "hub": model_hub,
            "api_key_proxy": api_key_proxy,
            "scenario_config_filters": [],
            "agent_params": {"temperature": 0, "top_p": 1, "max_tokens": 125},
            "is_lite": False,
            "version": harness_version,
        }
        if model_hub in HUBS_NOT_NEEDING_MODEL_NAME:
            payload["model"] = "n/a"
        else:
            try:
                payload["model"] = model_name
            except KeyError:
                raise ValueError(
                    f"No model name specified for {model_hub}. Please specify a model name."
                )

        if model_hub in HUBS_NEEDING_URL:
            if model_url is None:
                raise ValueError("For this model hub, you must specify a model URL.")
            if model_hub == "custom" and api_key_name is None:
                raise ValueError(
                    "For custom model hubs, you must specify an API key name. Use `api_keys.list()` to see available keys."
                )
            payload["url"] = model_url

        if model_params:
            for key, value in model_params.items():
                payload["agent_params"][key] = value
            if model_params.get("num_generations"):
                payload["num_generations"] = model_params["num_generations"]
        for option in ["sample_size", "is_lite"]:
            if harness_params.get(option):
                payload[option] = harness_params[option]

        if "trust_score" in harnesses:
            if len(harnesses) == 1:
                harnesses_modified = [f"{dim}_Small" for dim in AGENT_DIMENSION_LIST]
            else:
                raise ValueError(
                    "The `trust_score` harness is available only as a standalone harness."
                )
        elif "llm_trust_score" in harnesses:
            if len(harnesses) == 1:
                harnesses_modified = [f"{dim}_Small" for dim in DIMENSION_LIST]
            else:
                raise ValueError(
                    "The `llm_trust_score` harness is available only as a standalone harness."
                )
        else:
            harnesses_modified = harnesses

        payload["harness_config_ids"] = [
                f"vijil.harnesses.{h}" for h in harnesses_modified
            ]

        # Fetch the tags for the harnesses
        if tags is None:
            eval_tag = self.get_harness_tags(harnesses_modified)
            tag_map = {
                "BENCHMARK": "benchmarks",
                "CUSTOM": "custom",
                "DIMENSION": "vijil_harness",
                "SCENARIO": "vijil_scenario",
                "AUDIT": "audit",
            }
            payload["tags"] = [tag_map[eval_tag]]
        else:
            payload["tags"] = tags

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key,
        )

    def get_status(self, evaluation_id: str):
        """Retrieve the status of an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dict with the id, status, and other metadata of the evaluation
        :rtype: dict
        """

        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"evaluations/{evaluation_id}",
            token=self.client.api_key,
        )
        return response

    def get_metadata(self, evaluation_id: str):
        """
        Get the metadata for an evaluation ID, including tag information
        """
        try:
            response = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"evaluations/metadata/{evaluation_id}",
                token=self.client.api_key,
            )
            return response
        except Exception as e:
            raise ValueError(
                f"An error occurred while getting the metadata for evaluation {evaluation_id} : {e}"
            )

    def get_tree(self, evaluation_id: str):
        """
        Retrieve the tree of an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: For each probe, information about which harness and scenario it came from
        :rtype: dict
        """

        # harness level
        try:
            harness_info = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"harness?evaluation_id={evaluation_id}",
                token=self.client.api_key,
            )
        except Exception as e:
            raise ValueError(f"Error getting harness info: {e}")

        # scenario level
        try:
            scenario_info = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"scenarios?evaluation_id={evaluation_id}",
                token=self.client.api_key,
            )
        except Exception as e:
            raise ValueError(f"Error getting scenario info: {e}")

        # probe level
        try:
            probe_info = make_api_request(
                base_url=self.client.base_url,
                endpoint=f"probes?evaluation_id={evaluation_id}",
                token=self.client.api_key,
            )
        except Exception as e:
            raise ValueError(f"Error getting probe info: {e}")

        # build tree
        tree = {}
        for harness in harness_info["results"]:
            tree[harness["config_id"]] = {
                "name": harness["name"],
                "type": "harness",
                "children": harness["scenario_config_ids"],
            }
        for scenario in scenario_info["results"]:
            tree[scenario["config_id"]] = {
                "name": scenario["name"],
                "type": "scenario",
                "children": scenario["probe_config_ids"],
            }
        for probe in probe_info["results"]:
            tree[probe["config_id"]] = {
                "name": probe["name"],
                "type": "probe",
                "children": probe["prompt_ids"],
            }
        return tree

    def get_ancestry(self, tree: dict, node_id: str):
        """
        Retrieve the ancestry of a node in the tree

        :param tree: The tree of the evaluation
        :type tree: dict
        :param node_id: The unique ID of the node
        :type node_id: str
        :return: a dict with each ancestor as a value and ancestor types as the keys
        :rtype: dict
        """

        ancestors = {}
        node_value = tree.get(node_id)  # value of node
        if node_value is None:
            raise ValueError(f"Node {node_id} not found in tree.")
        current_node = node_value
        current_node_id = node_id
        while current_node["type"] != "harness":
            for parent_id, parent in tree.items():
                if current_node_id in parent["children"]:
                    ancestors[parent["type"]] = {
                        "id": parent_id,
                        "name": parent["name"],
                    }
                    current_node = parent
                    current_node_id = parent_id
                    break
        return ancestors

    def summarize(self, evaluation_id: str):
        """
        Return summary dataframe of the evaluation results, aggregated at every level
        (overall eval, dimension, scenario, probe)

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dataframe with the level, level_name, and score of the evaluation
        :rtype: pandas.DataFrame
        """

        # initalize list of dicts where keys are level, level_name, score
        summary_rows = []

        # get status of evaluation
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:  # for when evaluation doesn't exist
            raise e

        # evaluation level
        if status_dict["status"] == "COMPLETED":
            row = dict()
            row["level"] = "overall"
            row["level_name"] = "evaluation"
            row["score"] = round(status_dict["score"] * 100, 2)
            summary_rows.append(row)
        else:
            raise ValueError("Evaluation is not completed yet, check back later.")

        # harness level
        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"harness?evaluation_id={evaluation_id}",
            token=self.client.api_key,
        )
        for harness in response["results"]:
            if harness["harness_type"] == "DIMENSION" and harness["score"] is not None:
                row = dict()
                row["level"] = "harness"
                row["level_name"] = harness["name"]
                row["score"] = round(harness["score"] * 100, 2)
                summary_rows.append(row)

        # scenario level
        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"scenarios?evaluation_id={evaluation_id}",
            token=self.client.api_key,
        )
        for scenario in response["results"]:
            if scenario["score"] is not None:
                row = dict()
                row["level"] = "scenario"
                row["level_name"] = scenario["name"]
                row["score"] = round(scenario["score"] * 100, 2)
                summary_rows.append(row)

        # probe level
        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"probes?evaluation_id={evaluation_id}",
            token=self.client.api_key,
        )
        for probe in response["results"]:
            if probe["score"] is not None:
                row = dict()
                row["level"] = "probe"
                row["level_name"] = probe["name"]
                row["score"] = round(probe["score"] * 100, 2)
                summary_rows.append(row)

        return pd.DataFrame(summary_rows)

    def describe(
        self,
        evaluation_id: str,
        limit: int = 1000,
        format: str = "dataframe",
        prettify: bool = True,
        hits_only: bool = False,
    ):
        """
        Return either list or dataframe of prompt-level metadata and evaluation results,
        with metadata and evaluation scores for each prompt/response in the given evaluation id.

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in description. Defaults to 1000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "dataframe". Options are "dataframe" and "list"
        :type format: str, optional
        :raises ValueError: If specified format is not 'dataframe' or 'list'
        :param prettify: If True, will remove the "vijil.probes." prefix from the probe names to make it more readable. Defaults to True.
        :type prettify: bool, optional
        :type hits_only: bool, optional
        :param hits_only: If True, will only return prompts that had undesirable responses (according to our detectors). Defaults to False.
        """
        if limit is None:
            limit = 1000000

        response = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"responses?evaluation_id={evaluation_id}&limit={limit}&is_visible=true",
            token=self.client.api_key,
        )

        # change detector ids to list if it is a string
        results = response["results"]
        if len(results) == 0:
            raise ValueError(
                f"No results found for evaluation id {evaluation_id}. Please check that you have the correct id."
            )
        for idx, res in enumerate(results):
            if isinstance(
                res["detector_ids"], str
            ):  # modify this to accomodate >1 detector_id
                # split by comma and remove whitespace
                results[idx]["detector_ids"] = [
                    d.strip() for d in res["detector_ids"].split(",")
                ]

        prompt_list = [
            {
                "probe": res["probe_config_id"],
                "input_prompt_id": res["input_prompt_id"],
                "prompt": res["input_prompt"],
                "prompt_list": res["prompt"],
                "prompt_group": res["prompt_group"],
                "response": res["response"],
                "detectors": res["detector_ids"],
                "detector_scores": res["detector_scores"],
                "score": res.get("score", {}).get("score")
                if res.get("score") is not None
                else None,
                "triggers": res.get("triggers", []),
                "generation": res["generation"],
                "status": res["status"],
                "error_message": res["error_message"],
            }
            for res in results
        ]

        # convert to df for easier data processing
        prompt_list_df = pd.DataFrame(prompt_list)

        # get probe metadata
        probes = self.get_probes_info(evaluation_id=evaluation_id)
        # above returns a list of dicts with keys: probe, name, description, scoring_function
        # populate probe column in prompt_list_df with name from probes dict
        prompt_list_df["probe_name"] = prompt_list_df["probe"].apply(
            lambda x: [p["name"] for p in probes if p["probe"] == x][0]
        )
        prompt_list_df["probe_description"] = prompt_list_df["probe"].apply(
            lambda x: [p["description"] for p in probes if p["probe"] == x][0]
        )
        prompt_list_df["probe_scoring_function"] = prompt_list_df["probe"].apply(
            lambda x: [p["scoring_function"] for p in probes if p["probe"] == x][0]
        )

        # get detector metadata
        detectors = prompt_list_df["detectors"].values
        flattened_detectors = [item for sublist in detectors for item in sublist]
        unique_detectors = set(flattened_detectors)
        detector_metadata = {
            det: self.detectors.get_detector_info(detector_id=det)
            for det in unique_detectors
        }
        prompt_list_df["detector_names"] = prompt_list_df["detectors"].apply(
            lambda dets: [detector_metadata[det]["name"] for det in dets]
        )
        prompt_list_df["detector_descriptions"] = prompt_list_df["detectors"].apply(
            lambda dets: [detector_metadata[det]["description"] for det in dets]
        )

        # get harness and scenario each response belongs to
        tree = self.get_tree(evaluation_id=evaluation_id)
        # column function on 'probe' column. Get ancestors of each probe. Assign to new columns harness, harness_name, scenario, scenario_name
        prompt_list_df["harness"] = prompt_list_df["probe"].apply(
            lambda x: self.get_ancestry(tree, x)["harness"]["id"]
        )
        prompt_list_df["harness_name"] = prompt_list_df["probe"].apply(
            lambda x: self.get_ancestry(tree, x)["harness"]["name"]
        )
        prompt_list_df["scenario"] = prompt_list_df["probe"].apply(
            lambda x: self.get_ancestry(tree, x)["scenario"]["id"]
        )
        prompt_list_df["scenario_name"] = prompt_list_df["probe"].apply(
            lambda x: self.get_ancestry(tree, x)["scenario"]["name"]
        )

        # get scenario metadata and set description
        scenarios = self.get_scenario_info(evaluation_id=evaluation_id)
        prompt_list_df["scenario_description"] = prompt_list_df["scenario"].apply(
            lambda x: [s["description"] for s in scenarios if s["scenario"] == x][0]
        )

        # get harness metadata and set description
        harnesses = self.get_harness_info()
        prompt_list_df["harness_description"] = prompt_list_df["harness"].apply(
            lambda x: [h["description"] for h in harnesses if h["harness"] == x][0]
        )

        # joins for displaying second prompt in pairwise prompts
        prompt_list_df["prompt_group_len"] = prompt_list_df["prompt_group"].apply(
            lambda x: len(x)
        )
        pairwise = prompt_list_df[prompt_list_df["prompt_group_len"] == 2]
        nonpairwise = prompt_list_df[prompt_list_df["prompt_group_len"] != 2]
        pairwise["input_prompt_id2"] = pairwise["prompt_group"].apply(lambda x: x[1])
        pairwise_with_prompt2_text = pairwise.merge(
            pairwise[["input_prompt_id", "prompt", "response"]].rename(
                columns={
                    "input_prompt_id": "input_prompt_id2",
                    "prompt": "prompt2",
                    "response": "response2",
                }
            ),
            on="input_prompt_id2",
            how="inner",
        )
        # filter out rows with skipped responses---these do not add any information since their reversed counterparts will be included
        pairwise_with_prompt2_text = pairwise_with_prompt2_text[
            pairwise_with_prompt2_text["detector_scores"].apply(
                lambda x: not any(["SKIP" in item for item in x])
            )
        ]
        # add empty columns to nonpairwise rows
        nonpairwise["input_prompt_id2"] = None
        nonpairwise["prompt2"] = None
        nonpairwise["response2"] = None
        # concatenate pairwise and nonpairwise dfs row-wise
        output_df = pd.concat([pairwise_with_prompt2_text, nonpairwise], axis=0)
        # drop prompt_group_len column which we needed only for processing
        output_df.drop(columns=["prompt_group_len"], inplace=True)

        if hits_only:
            output_df = output_df[output_df["score"] == 0]

        # prettify probe names
        if prettify:
            output_df["probe"] = output_df["probe"].apply(
                lambda x: x.replace("vijil.probes.", "")
            )

        # sort by probes for easier viewing
        output_df.sort_values("probe", inplace=True)

        if format == "list":
            return output_df.to_dict(orient="records")
        elif format == "dataframe":
            return output_df
        else:
            raise ValueError("format must be 'list' or 'dataframe'")

    def export(
        self,
        evaluation_id: str,
        limit: int = 1000000,
        format: str = "csv",
        output_dir: str = "./",
        prettify: bool = True,
        hits_only: bool = False,
    ):
        """
        Exports output logs from describe() into csv, jsonl, json, or parquet

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in the report. Defaults to 1000000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "csv". Options are "csv", "parquet", "json" and "jsonl"
        :type format: str, optional
        :raises ValueError: If specified format is not 'csv', 'parquet', 'json' or 'jsonl'
        :param output_dir: The directory to save the report. Defaults to the current directory.
        :type output_dir: str, optional
        :param prettify: If True, will remove the "vijil.probes." prefix from the probe names to make it more readable. Defaults to True.
        :type prettify: bool, optional
        :type hits_only: bool, optional
        :param hits_only: If True, will only return prompts that had undesirable responses (according to our detectors). Defaults to False.
        """

        if format == "csv":
            prompt_list_df = self.describe(
                evaluation_id=evaluation_id,
                limit=limit,
                format="dataframe",
                prettify=prettify,
                hits_only=hits_only,
            )
            filename = evaluation_id + "_report.csv"
            filepath = os.path.join(output_dir, filename)
            prompt_list_df.to_csv(filepath, index=False)
            print("report exported to " + filepath)
        elif format == "json":
            prompt_list = self.describe(
                evaluation_id=evaluation_id,
                limit=limit,
                format="list",
                prettify=prettify,
                hits_only=hits_only,
            )
            filename = evaluation_id + "_report.json"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                json.dump(prompt_list, f, indent=4)
            print("report exported to " + filepath)
        elif format == "jsonl":
            prompt_list = self.describe(
                evaluation_id=evaluation_id,
                limit=limit,
                format="list",
                prettify=prettify,
                hits_only=hits_only,
            )
            filename = evaluation_id + "_report.jsonl"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                for item in prompt_list:
                    f.write(json.dumps(item) + "\n")
            print("report exported to " + filepath)
        elif format == "parquet":
            prompt_list_df = self.describe(
                evaluation_id=evaluation_id,
                limit=limit,
                format="dataframe",
                prettify=prettify,
                hits_only=hits_only,
            )
            filename = evaluation_id + "_report.parquet"
            filepath = os.path.join(output_dir, filename)
            prompt_list_df.to_parquet(filepath, index=False)
            print("report exported to " + filepath)
        else:
            raise ValueError("format must be 'csv', 'parquet', 'json', or 'jsonl'")

    def cancel(self, evaluation_id: str):
        """
        Cancels an in-progress evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation is not in progress
        :returns: The response from the API
        :rtype: dict
        """

        # check eval status
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e

        if status_dict["status"] != "IN_PROGRESS":
            raise ValueError(
                f"Evaluation {evaluation_id} is not in progress. Cannot cancel."
            )

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=f"evaluations/{evaluation_id}/cancel",
            method="post",
            token=self.client.api_key,
        )

    def delete(self, evaluation_id: str):
        """
        Deletes an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation does not exist
        :returns: The response from the API
        :rtype: dict
        """

        # check eval status. This will raise an error if the eval doesn't exist.
        try:
            self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e

        payload = {
            "type": "DELETE_EVALUATION",
            "data": {"evaluation_id": evaluation_id},
        }

        return make_api_request(
            base_url=self.client.base_url,
            endpoint="events",
            method="post",
            data=payload,
            token=self.client.api_key,
        )

    def get_probes(self, evaluation_id: str):
        """
        Get all probes and probe metadata for a specific evaluation.
        Returns a dict with keys results, count.
        Results array contains probes and count indicates number of probes.
        """
        try:
            response = make_api_request(
                base_url=self.client.base_url,
                endpoint="probes",
                token=self.client.api_key,
                params={"evaluation_id": evaluation_id},
            )
        except Exception as e:
            raise ValueError(
                f"Error getting probes for evaluation {evaluation_id}: {e}"
            )

        # return only probe info
        return response["results"]

    def get_probes_info(self, evaluation_id: str):
        """
        Get metadata for all probes in a specific evaluation.
        Returns a list of dicts with keys: probe, name, description, scoring_function.
        """
        probes = self.get_probes(evaluation_id=evaluation_id)
        # return the following metadata: config_id, name, description, scoring_function
        return [
            {
                "probe": p["config_id"],
                "name": p["name"],
                "description": p["description"],
                "scoring_function": p["scoring_function"],
            }
            for p in probes
        ]

    def get_scenario_info(self, evaluation_id: str, full: bool = False):
        """
        Get metadata for all scenarios in a specific evaluation.
        Returns a list of dicts with keys: scenarios, name, description
        """
        try:
            response = make_api_request(
                base_url=self.client.base_url,
                endpoint="scenarios",
                token=self.client.api_key,
                params={"evaluation_id": evaluation_id},
            )
        except Exception as e:
            raise ValueError(
                f"Error getting scenarios for evaluation {evaluation_id}: {e}"
            )

        # return only scenario info
        if full:
            return response["results"]
        return [
            {
                "scenario": s["config_id"],
                "name": s["name"],
                "description": s["description"],
            }
            for s in response["results"]
        ]

    def get_harness_info(self, full: bool = False):
        """
        Get metadata for all harnesses in a specific evaluation.
        Returns a list of dicts with keys: harness, name, description
        """
        try:
            response = make_api_request(
                base_url=self.client.base_url,
                endpoint="harness-configs",
                token=self.client.api_key,
                params={
                    "limit": 10000
                },  # Harness endpoint is limited. Use a high limit to get all the harness info
            )
        except Exception as e:
            raise ValueError(f"Error getting harnesses : {e}")

        if full:
            return response["results"]
        return [
            {
                "harness": h["harness_config"]["id"],
                "name": h["harness_config"]["name"],
                "description": h["harness_config"]["description"],
            }
            for h in response["results"]
        ]

    def report(self, evaluation_id: str) -> AnalysisReports:
        metadata = self.get_metadata(evaluation_id)
        return AnalysisReports(self.client, evaluation_id, metadata)


class Detectors:
    """Class for handling API requests to get detector metadata."""

    def __init__(self, client: VijilClient) -> None:
        self.endpoint = "detectors"
        self.client = client

    def get_detector_info(self, detector_id: str, version: Optional[str] = None):
        """Gets all detector metadata"""
        if not version:
            version = self.client.get_latest_objects_version()
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + f"/{detector_id}",
            token=self.client.api_key,
            params={"version": version},
        )

    def list(self, version: Optional[str] = None):
        """Lists all available detectors"""
        if not version:
            version = self.client.get_latest_objects_version()
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            token=self.client.api_key,
            params={"version": version},
        )


class Detections:
    """Class for handling detections API requests.
    :param detector_id: The unique ID of the detector
    :type detector_id: str
    :param detector_inputs: Input payload to the detector
    :type detector_inputs: List[dict]
    :param detector_params: Optional parameters to be passed for the detector
    :type detector_params: dict
    """

    def __init__(self, client: VijilClient) -> None:
        """Initialize the Detections class.

        :param client: The Vijil client instance.
        :type client: VijilClient
        """
        self.endpoint = "detections"
        self.client = client
        self.api_proxy_dict: dict = field(default_factory=dict)
        self.detector_list = []
        for k, v in DETECTOR_LIST.items():
            self.detector_list += v

    def list_detectors(self):
        return self.detector_list

    def create(
        self,
        detector_id: str,
        detector_inputs: List[dict],
        detector_params: Optional[dict] = None,
    ):
        """Create a new detection.

        :param detector_id: The unique ID of the detector
        :type detector_id: str
        :param detector_inputs: Input payload to the detector
        :type detector_inputs: List[dict]
        :param detector_params: Optional parameters to be passed for the detector
        :type detector_params: dict
        :return: The response from the API
        :rtype: dict
        """

        # make full detector id
        full_detector_id = None
        for k, v in DETECTOR_LIST.items():
            for detname in v:
                if detname == detector_id:
                    full_detector_id = f"{k}.detectors.{detname}"
                    break
        if not full_detector_id:
            raise ValueError(
                f"Detector {detector_id} not found. use `detectors.list_detectors()` to see available detectors."
            )

        payload = {
            "id": str(uuid.uuid4()),
            "detector_id": full_detector_id,
            "detector_inputs": detector_inputs,
        }

        # add detector params if necessary
        if full_detector_id in DEFAULT_DETECTOR_PARAMS.keys():
            if detector_params is None:
                detector_params = DEFAULT_DETECTOR_PARAMS[full_detector_id]

            # add api key proxy TODO: refactor later, double code with evaluations.create

            # store all api keys in a dictionary if not there
            if self.api_proxy_dict.__class__.__name__ == "Field":
                try:
                    self.api_proxy_dict = get_api_proxy_dict(
                        base_url=self.client.base_url, token=self.client.api_key
                    )
                except TypeError:
                    raise TypeError(
                        "No API keys found. Please upload an API key first."
                    )

            # get api key proxy dict for the model hub
            hub = modify_hub(detector_params["hub"])
            try:
                hub_api_proxy_dict = self.api_proxy_dict[hub]
            except KeyError:
                raise ValueError(f"No API key stored for model hub {hub}")

            # get api key proxy for the model hub
            if detector_params.get("api_key_name"):
                api_key_name = detector_params["api_key_name"]
                # find api key id for the api key name
                if api_key_name not in hub_api_proxy_dict.keys():
                    raise ValueError(f"No API key found for name {api_key_name}")
                else:
                    api_key_proxy = hub_api_proxy_dict[api_key_name]
            else:  # if no key specified, use first value in hub dictionary
                api_key_proxy = next(iter(hub_api_proxy_dict.values()))

            detector_params = {
                "api_key_proxy": api_key_proxy,
                "hub": hub,
                "model": detector_params["model"],
            }
        else:
            detector_params = {"api_key_proxy": "", "hub": "", "model": ""}
        payload["detector_params"] = detector_params  # type: ignore

        msg = make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key,
        )
        return {"id": msg["id"], "status": msg["status"]}

    def get_status(self, detection_id: str):
        """Retrieve the status of a detection.

        :param detection_id: The unique ID of the detection
        :type detection_id: str
        :return: The response from the API
        :rtype: dict
        """

        raw_output = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"detections/{detection_id}",
            token=self.client.api_key,
        )
        return {"id": raw_output["id"], "status": raw_output["status"]}

    def describe(self, detection_id: str, format: str = "dataframe"):
        """Describe a detection.

        :param detection_id: The unique ID of the detection
        :type detection_id: str
        :return: The response from the API
        :rtype: dict
        """
        input_fields = [
            "response",
            "triggers",
            "ground_truth",
            "question",
            "contexts",
            "instructions",
            "kwargs",
            "forbidden_prompt",
            "role",
            "expected_tools",
            "input",
            "policy",
        ]
        output_fields = ["score", "reason", "error"]

        raw_output = make_api_request(
            base_url=self.client.base_url,
            endpoint=f"detections/{detection_id}",
            token=self.client.api_key,
        )
        if raw_output["status"] != "COMPLETED":
            raise ValueError(
                f"Detection {detection_id} is not completed yet. Please check back later."
            )
        else:
            raw_detector_inputs = raw_output["detector_inputs"]
            raw_detector_outputs = raw_output["detector_outputs"]

            # process inputs
            detector_inputs = []
            for input_dict in raw_detector_inputs:
                detector_inputs.append(
                    {
                        "input_id": input_dict["id"],
                        "detector_input": {
                            k: input_dict[k] for k in input_dict if k in input_fields
                        },
                        "status": raw_output["status"],
                    }
                )

            # process outputs
            detector_outputs = []
            for output_dict in raw_detector_outputs:
                detector_outputs.append(
                    {
                        "input_id": output_dict["input_id"],
                        "detector_output": {
                            k: output_dict[k] for k in output_dict if k in output_fields
                        },
                    }
                )

            # merge and reorder
            output_df = pd.DataFrame(detector_inputs).merge(
                pd.DataFrame(detector_outputs), on="input_id"
            )
            output_df["detector_id"] = raw_output["detector_id"]
            output_df = output_df[
                ["detector_id", "status", "detector_input", "detector_output"]
            ]

            # return
            if format == "list":
                return output_df.to_dict(orient="records")
            elif format == "dataframe":
                return output_df
            else:
                raise ValueError("format must be 'list' or 'dataframe'")


class Agents:
    # Class for local agent execution and evaluation
    def __init__(
        self, base_url: str, evaluation_client: Evaluations, api_key_client: APIKeys
    ) -> None:
        self.base_url = base_url
        self.evaluation_client = evaluation_client
        self.api_key_client = api_key_client

    def register(
        self,
        agent_name: str,
        evaluator: LocalAgentExecutor,
        rate_limit: Optional[int] = None,
        rate_limit_interval: Optional[int] = None,
    ):
        if rate_limit is None or rate_limit_interval is None:
            # Use defaults but notify the user
            print("[!] Rate limit and interval not provided. Using default of 30 RPM.")
            rate_limit = 30
            rate_limit_interval = 1

        # Attempt to get a Vijil ngrok token
        ngrok_token = None
        ngrok_domain = None
        try:
            response = make_api_request(
                self.evaluation_client.client.base_url,
                endpoint="local-eval-token",
                token=self.evaluation_client.client.api_key,
            )
            if response is not None:
                ngrok_token = response.get("token")
                ngrok_domain = response.get("domain")
        except Exception as e:
            print(
                f"[!] A Vijil issued ngrok token could not be obtained - you may need to subscribe to Vijil Evaluate Premium.\nException: {str(e)}"
            )

        server = start_ngrok_server(evaluator, ngrok_token, ngrok_domain)
        # API key name
        api_key_name = f"{agent_name}-api-key-{uuid.uuid4()}"
        self.api_key_client.create(
            name=api_key_name,
            model_hub="custom",
            rate_limit_per_interval=rate_limit,
            rate_limit_interval=60,
            api_key=server.api_key,
            hub_config=None,
            url=f"{server.url}/v1",
        )
        print(
            f"[✓] Registered agent {agent_name} at {server.url} with API key {api_key_name}"
        )
        return server, api_key_name

    def deregister(self, server: LocalServer, api_key_name: str):
        # Stop the server and remove the API key
        server.shutdown()
        # Wait a bit to allow the evaluation itself to cancel
        time.sleep(5)
        # Delete the API key
        self.api_key_client.delete(api_key_name)

    async def _monitor_progress(self, evaluation_id: str, poll_interval: float):
        bar = tqdm(total=100, desc="Evaluation Progress", dynamic_ncols=True)

        while True:
            status_data = self.evaluation_client.get_status(evaluation_id)
            status = status_data.get("status")

            total = status_data.get("total_test_count", 0)
            complete = status_data.get("completed_test_count", 0)
            errors = status_data.get("error_test_count", 0)

            done = complete + errors
            progress_percent = (done / total) * 100 if total else 0
            bar.n = int(progress_percent)
            bar.refresh()

            if status in TERMINAL_STATUSES:
                bar.n = 100
                bar.refresh()
                bar.close()
                print(f"[✓] Evaluation ended with status: {status}")
                if self.base_url in API_URL_TO_USER_URL_MAP:
                    print(
                        f"View your evaluation at {API_URL_TO_USER_URL_MAP[self.base_url]}/evaluations/{evaluation_id}"
                    )
                return

            await asyncio.sleep(poll_interval)

    def create(
        self,
        agent_function: Callable,
        input_adapter: Callable,
        output_adapter: Callable,
    ) -> LocalAgentExecutor:
        evaluator = LocalAgentExecutor(
            agent_function=agent_function,
            input_adapter=input_adapter,
            output_adapter=output_adapter,
        )
        return evaluator

    def evaluate(
        self,
        agent_name: str,
        evaluation_name: str,
        agent: LocalAgentExecutor,
        harnesses: list,
        harness_parameters: dict = {},
        rate_limit: Optional[int] = None,
        rate_limit_interval: Optional[int] = None,
        poll_interval: float = 5.0,
        keep_alive: bool = False,
        tags: Optional[List[str]] = None,
    ):
        try:
            # If keep alive is true, ensure the system does not sleep
            with keep.running() if keep_alive else nullcontext():
                # Register and create the server
                server, api_key_name = self.register(
                    agent_name=agent_name,
                    evaluator=agent,
                    rate_limit=rate_limit,
                    rate_limit_interval=rate_limit_interval,
                )

                # Sleep for a bit to allow agent registration
                time.sleep(5)
                print(
                    f"[~] Starting evaluation '{evaluation_name}' for agent '{agent_name}'"
                )
                # Send the eval request to Vijil API
                evaluation = self.evaluation_client.create(
                    model_hub="custom",
                    model_name=agent_name,
                    name=evaluation_name,
                    api_key_name=api_key_name,
                    model_url=f"{server.url}/v1",
                    harnesses=harnesses,
                    harness_params=harness_parameters,
                    tags=tags
                )
                evaluation_id = evaluation.get("id")
                print(f"[✓] Evaluation '{evaluation_name}' started with ID {evaluation_id}")
                # Starting the status check immediately after eval creation can lead to a 404
                time.sleep(5)  # Wait for the evaluation to start
                loop = asyncio.get_event_loop()
                task = loop.create_task(
                    self._monitor_progress(evaluation_id, poll_interval)
                )
                loop.run_until_complete(task)

                return self.evaluation_client.get_status(evaluation_id)

        except KeyboardInterrupt:
            # Kill the eval if the user interrupts
            print("\n[!] Keyboard interrupt detected. Cancelling evaluation...")
            task.cancel()
            try:
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                print("[~] Monitoring task was cancelled.")
            if evaluation_id:
                try:
                    self.evaluation_client.cancel(evaluation_id)
                    print(f"Evaluation {evaluation_id} canceled.")
                except Exception as e:
                    print(f"[!] Failed to cancel evaluation: {e}")
            raise

        finally:
            # Shutdown and deregister
            self.deregister(server, api_key_name)


class Vijil:
    """Base class for the Vijil API client.

    :param base_url: The base URL for the Vijil API
    :type base_url: str
    :param api_key: The API key for the Vijil API
    :type api_key: str
    """

    client: VijilClient
    evaluations: Evaluations
    harnesses: Harnesses
    detections: Detections
    api_keys: APIKeys

    def __init__(self, base_url: str = BASE_URL, api_key: Optional[str] = None):
        """Constructor class for VijilClient

        :param base_url: Base URL for API, defaults to BASE_URL as specified in `api.py`
        :type base_url: str, optional
        :param api_key: Vijil API key, defaults to None
        :type api_key: str, optional
        :raises ValueError: if no Vijil API key is provided in api_key and VIJIL_API_KEY is not set as an environment variable
        """

        if api_key is None:
            api_key = os.environ["VIJIL_API_KEY"]
        if api_key is None:
            raise ValueError(
                "No API key found! Please set VIJIL_API_KEY as environment variable or supply the `api_key` parameter."
            )

        self.client = VijilClient(base_url=base_url, api_key=api_key)
        self.evaluations = Evaluations(self.client)
        self.harnesses = Harnesses(self.client)
        self.detections = Detections(self.client)
        self.api_keys = APIKeys(self.client)
        self.detectors = Detectors(self.client)

        self.agents = Agents(self.client.base_url, self.evaluations, self.api_keys)
