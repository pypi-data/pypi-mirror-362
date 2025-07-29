# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021-2025 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .api_key.comet_api_key import parse_api_key
from .config import get_config
from .connection_helpers import get_root_url, sanitize_url


def get_comet_base_url(api_key: str) -> str:
    """
    Extracts Comet base URL from API key and sanitizes it (appends / at the end)

    Args:
        api_key: The Comet API key string

    Returns:
        str: Sanitized Comet base URL
    """
    api_key_parsed = parse_api_key(api_key)
    if api_key_parsed is not None and api_key_parsed.base_url is not None:
        return sanitize_url(api_key_parsed.base_url)
    else:
        return get_root_url(
            get_config("comet.url_override") or os.environ.get("COMET_URL_OVERRIDE")
        )


class Client:
    """
    A REST client for interacting with the Comet MPM API.

    This client provides methods for making HTTP requests to the Comet MPM API endpoints,
    including model predictions, feature analysis, and custom metric queries.

    Args:
        api_key: The Comet API key for authentication
        retry_total: Total number of retries for failed requests (default: 3)
        status_codes: HTTP status codes to retry on (default: [429, 500, 502, 503, 504])
        backoff_factor: Wait time between retries (exponential backoff) (default: 1)
        raise_on_status: Whether to raise an exception on non-200 status codes (default: False)

    Note:
        The client automatically handles retries and authentication for all requests.
    """

    def __init__(
        self,
        api_key: str,
        retry_total: int = 3,
        status_codes: Optional[List[int]] = None,
        backoff_factor: int = 1,
        raise_on_status: bool = False,
    ) -> None:
        """
        Initialize the Comet MPM REST client with retry and error handling.

        Args:
            api_key: The Comet API key for authentication
            retry_total: Total number of retries for failed requests (default: 3)
            status_codes: HTTP status codes to retry on (default: [429, 500, 502, 503, 504])
            backoff_factor: Wait time between retries (exponential backoff) (default: 1)
            raise_on_status: Whether to raise an exception on non-200 status codes (default: False)

        Note:
            The client will automatically handle retries for failed requests based on the
            provided configuration parameters.
        """
        if status_codes is None:
            status_codes = [429, 500, 502, 503, 504]

        retry_strategy = Retry(
            total=retry_total,
            status_forcelist=status_codes,
            backoff_factor=backoff_factor,
            raise_on_status=raise_on_status,
        )

        self.adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("http://", self.adapter)
        self.session.mount("https://", self.adapter)

        self.base_url = get_comet_base_url(api_key)
        key_obj = parse_api_key(api_key)
        self.api_key = key_obj.short_api_key

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a GET request to the Comet MPM API.

        Args:
            endpoint: The API endpoint to request (e.g., 'api/mpm/v2/model/numberOfPredictions')
            params: Optional query parameters for the request

        Returns:
            Dict: JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the request fails
            requests.exceptions.HTTPError: If the server returns a non-200 status code
        """
        url = urljoin(self.base_url, endpoint)
        headers = {"Authorization": self.api_key, "Accept": "application/json"}
        response = self.session.get(url, headers=headers, params=params)
        return_data = response.json()
        return return_data

    def post(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a POST request to the Comet MPM API.

        Args:
            endpoint: The API endpoint to request (e.g., 'api/mpm/v2/features/drift')
            params: Request body parameters as a dictionary

        Returns:
            Dict: JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the request fails
            requests.exceptions.HTTPError: If the server returns a non-200 status code
        """
        url = urljoin(self.base_url, endpoint)
        headers = {"Authorization": self.api_key, "Accept": "application/json"}
        response = self.session.post(url, headers=headers, json=params)
        return_data = response.json()
        return return_data

    def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific model.

        Args:
            model_id: The ID of the model to retrieve details for

        Returns:
            Dict[str, Any]: Model details including metadata, configuration, and status

        Raises:
            requests.exceptions.HTTPError: If the model is not found or the request fails
        """
        endpoint = f"api/mpm/v2/model/details?modelId=${model_id}"
        response = self.get(endpoint)
        return response

    def get_nb_predictions(
        self,
        model_id: str,
        start_date: str,
        end_date: str,
        interval_type: str,
        filters: List[str],
        model_version: str,
    ) -> Dict[str, Any]:
        """
        Get the number of predictions for a model within a specified time range.

        Args:
            model_id: The ID of the model
            start_date: Start date for the query (ISO format)
            end_date: End date for the query (ISO format)
            interval_type: Time interval type (e.g., 'hour', 'day', 'week')
            filters: List of filter predicates to apply
            model_version: Model version identifier

        Returns:
            Dict[str, Any]: Number of predictions with time series data

        Raises:
            requests.exceptions.HTTPError: If the query fails or returns invalid results
        """
        endpoint = "api/mpm/v2/model/numberOfPredictions"
        params = {
            "modelId": model_id,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response

    def get_custom_metrics(
        self,
        model_id: str,
        sql: str,
        start_date: str,
        end_date: str,
        interval_type: str,
        filters: List[str],
        model_version: str,
    ) -> Dict[str, Any]:
        """
        Get custom metrics using SQL query.

        Args:
            model_id: ID of the model
            sql: SQL query string (e.g., "SELECT F1('label_value', 'prediction_value', 'true') FROM MODEL")
            start_date: Start date for the query (ISO format)
            end_date: End date for the query (ISO format)
            interval_type: Time interval type (e.g., 'hour', 'day', 'week')
            filters: List of filter predicates
            model_version: Model version identifier

        Returns:
            Dict: Metric results from the SQL query

        Raises:
            requests.exceptions.HTTPError: If the query fails or returns invalid results
        """
        endpoint = "api/mpm/v2/custom-metrics/query"
        params = {
            "modelId": model_id,
            "cometSql": sql,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response

    def get_feature_drift(
        self,
        model_id: str,
        feature_name: str,
        source_type: str,
        algorithm: str,
        start_date: str,
        end_date: str,
        interval_type: str,
        filters: List[str],
        model_version: str,
    ) -> Dict[str, Any]:
        """
        Get feature drift analysis between different data sources.

        Args:
            model_id: ID of the model
            feature_name: Name of the feature to analyze
            source_type: Type of source data (e.g., 'model_output_features')
            algorithm: Drift detection algorithm to use
            start_date: Start date for the analysis (ISO format)
            end_date: End date for the analysis (ISO format)
            interval_type: Time interval type (e.g., 'hour', 'day', 'week')
            filters: List of filter predicates
            model_version: Model version identifier

        Returns:
            Dict: Feature drift analysis results

        Raises:
            requests.exceptions.HTTPError: If the analysis fails or returns invalid results
        """
        endpoint = "api/mpm/v2/features/drift"
        params = {
            "modelId": model_id,
            "name": feature_name,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "algorithmType": algorithm,
            "source": source_type,
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response

    def get_feature_category_distribution(
        self,
        feature_name: str,
        normalize: bool,
        start_date: str,
        end_date: str,
        interval_type: str,
        filters: List[str],
        model_version: str,
    ) -> Dict[str, Any]:
        """
        Get the category distribution of a feature.

        Args:
            feature_name: Name of the feature to analyze
            normalize: Whether to normalize the distribution (default: False)
            start_date: Start date for the analysis (ISO format)
            end_date: End date for the analysis (ISO format)
            interval_type: Time interval type (e.g., 'hour', 'day', 'week')
            filters: List of filter predicates
            model_version: Model version identifier

        Returns:
            Dict: Category distribution of the feature

        Raises:
            requests.exceptions.HTTPError: If the analysis fails or returns invalid results

        Note:
            This method is specifically for numerical features.
        """
        endpoint = "api/mpm/v2/features/distribution"
        params = {
            "featureName": feature_name,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "featureSourceType": "model_output_features",
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response

    def get_feature_density(
        self,
        model_id: str,
        feature_name: str,
        start_date: str,
        end_date: str,
        filters: List[str],
        model_version: str,
        interval_type: str,
    ) -> Dict[str, Any]:
        """
        Get the probability density function (PDF) of a numerical feature.

        Args:
            model_id: ID of the model
            feature_name: Name of the numerical feature
            start_date: Start date for the analysis (ISO format)
            end_date: End date for the analysis (ISO format)
            filters: List of filter predicates
            model_version: Model version identifier
            interval_type: Time interval type (e.g., 'hour', 'day', 'week')

        Returns:
            Dict: Probability density function of the feature values

        Raises:
            requests.exceptions.HTTPError: If the analysis fails or returns invalid results

        Note:
            This method is specifically for numerical features and returns a PDF.
        """
        endpoint = "api/mpm/v2/features/numerical-distribution-pdf"
        params = {
            "modelId": model_id,
            "name": feature_name,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "source": "model_output_features",
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response

    def get_feature_percentiles(
        self,
        model_id: str,
        feature_name: str,
        percentiles: List[float],
        start_date: str,
        end_date: str,
        filters: List[str],
        model_version: str,
        interval_type: str,
    ) -> Dict[str, Any]:
        """
        Get percentile values for a numerical feature.

        Args:
            model_id: ID of the model
            feature_name: Name of the numerical feature
            percentiles: List of percentile values to calculate (e.g., [0.25, 0.5, 0.75])
            start_date: Start date for the analysis (ISO format)
            end_date: End date for the analysis (ISO format)
            filters: List of filter predicates
            model_version: Model version identifier

        Returns:
            Dict[str, Any]: Percentile values for the specified feature

        Raises:
            requests.exceptions.HTTPError: If the analysis fails or returns invalid results

        Note:
            This method is specifically for numerical features and returns percentile statistics.
        """
        endpoint = "api/mpm/v2/features/distribution"
        params = {
            "modelId": model_id,
            "name": feature_name,
            "from": start_date,
            "to": end_date,
            "intervalType": interval_type,
            "source": "model_output_features",
            "predicates": filters,
            "version": model_version,
        }
        response = self.post(endpoint, params)
        return response
