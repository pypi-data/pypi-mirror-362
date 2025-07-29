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
from typing import Dict, List, Optional

from pandas import DataFrame

from .client import Client
from .config import get_config


class Model:
    """
    A model instance for interacting with Comet MPM model-specific operations.

    This class provides high-level methods for querying model predictions, metrics,
    and feature analysis. It can be configured with panel options for default
    parameter values.

    Args:
        client: The Comet MPM client instance
        model_id: The ID of the model to work with
        panel_options: Optional dictionary containing default panel configuration
    """

    def __init__(
        self, client: Client, model_id: str, panel_options: Optional[Dict] = None
    ):
        """
        Initialize a Model instance.

        Args:
            client: The Comet MPM client instance for making API calls
            model_id: The ID of the model to work with
            panel_options: Optional dictionary containing default panel configuration
                that will be used when parameters are not explicitly provided
        """
        self._client = client
        self.model_id = model_id
        self.panel_options = panel_options

    def get_nb_predictions(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval_type: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
    ) -> int:
        """
        Get the number of predictions for a model within a specified time range.

        Args:
            start_date: Start date for filtering predictions (ISO format)
            end_date: End date for filtering predictions (ISO format)
            interval_type: Type of interval for aggregation (e.g., "DAY", "WEEK")
            filters: List of filters to apply to predictions
            model_version: Specific model version to query

        Returns:
            int: Number of predictions matching the criteria
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]

        data = self._client.get_nb_predictions(
            model_id=self.model_id,
            start_date=start_date,
            end_date=end_date,
            interval_type=interval_type,
            filters=filters,
            model_version=model_version,
        )
        # FIXME: Convert to dataframe
        return data

    def get_custom_metric(
        self,
        sql: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval_type: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
    ) -> DataFrame:
        """
        Execute a custom SQL query to retrieve model metrics.

        Args:
            sql: SQL query string to execute
            start_date: Start date for filtering results (ISO format)
            end_date: End date for filtering results (ISO format)
            interval_type: Type of interval for aggregation (e.g., "DAY", "WEEK")
            filters: List of filters to apply to results
            model_version: Specific model version to query

        Returns:
            DataFrame: Results of the SQL query
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]

        data = self._client.get_custom_metrics(
            model_id=self.model_id,
            sql=sql,
            start_date=start_date,
            end_date=end_date,
            interval_type=interval_type,
            filters=filters,
            model_version=model_version,
        )
        # FIXME: Convert to dataframe
        return data

    def get_feature_drift(
        self,
        feature_name: str,
        source_type: str = "INPUT",
        algorithm: str = "EMD",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval_type: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
    ) -> DataFrame:
        """
        Calculate drift metrics for a specific feature.

        Args:
            feature_name: Name of the feature to calculate drift for
            source_type: Type of feature source ("INPUT" or "OUTPUT")
            algorithm: Drift calculation algorithm ("EMD" or "PSI")
            start_date: Start date for drift calculation (ISO format)
            end_date: End date for drift calculation (ISO format)
            interval_type: Type of interval for aggregation (e.g., "DAY", "WEEK")
            filters: List of filters to apply to drift calculation
            model_version: Specific model version to query

        Returns:
            DataFrame: Drift metrics for the specified feature
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]

        data = self._client.get_feature_drift(
            feature_name=feature_name,
            source_type=source_type,
            algorithm=algorithm,
            model_id=self.model_id,
            start_date=start_date,
            end_date=end_date,
            interval_type=interval_type,
            filters=filters,
            model_version=model_version,
        )
        # FIXME: Convert to dataframe
        return data

    def get_feature_category_distribution(
        self,
        feature_name: str,
        normalize: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval_type: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
    ) -> DataFrame:
        """
        Get the distribution of categories for a categorical feature.

        Args:
            feature_name: Name of the categorical feature
            normalize: If True, returns percentages instead of counts
            start_date: Start date for distribution calculation (ISO format)
            end_date: End date for distribution calculation (ISO format)
            interval_type: Type of interval for aggregation (e.g., "DAY", "WEEK")
            filters: List of filters to apply to distribution calculation
            model_version: Specific model version to query

        Returns:
            DataFrame: Distribution of feature categories
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]

        data = self._client.get_feature_category_distribution(
            model_id=self.model_id,
            start_date=start_date,
            end_date=end_date,
            interval_type=interval_type,
            filters=filters,
            model_version=model_version,
        )
        # FIXME: Convert to dataframe
        return data

    def get_feature_density(
        self,
        feature_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
        interval_type: Optional[str] = None,
    ) -> DataFrame:
        """
        Get the probability density function (PDF) of a numeric feature.

        Args:
            feature_name: Name of the numeric feature
            start_date: Start date for density calculation (ISO format)
            end_date: End date for density calculation (ISO format)
            filters: List of filters to apply to density calculation
            model_version: Specific model version to query

        Returns:
            DataFrame: Probability density function of the feature values
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]

        data = self._client.get_feature_density(
            model_id=self.model_id,
            feature_name=feature_name,
            start_date=start_date,
            end_date=end_date,
            filters=filters,
            model_version=model_version,
            interval_type=interval_type,  # FIXME: are we sure?
        )
        # FIXME: Convert to dataframe
        return data

    def get_feature_percentiles(
        self,
        feature_name: str,
        percentiles=[0, 0.1, 0.25, 0.5, 0.75, 0.9, 1],  # Only these are supported
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        filters: Optional[List[str]] = None,
        model_version: Optional[str] = None,
        interval_type: Optional[str] = None,
    ) -> DataFrame:
        """
        Get the specified percentiles for a numeric feature.

        Args:
            feature_name: Name of the numeric feature
            percentiles: List of percentiles to calculate (default: [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1])
                Only these specific percentile values are supported
            start_date: Start date for percentile calculation (ISO format)
            end_date: End date for percentile calculation (ISO format)
            filters: List of filters to apply to percentile calculation
            model_version: Specific model version to query

        Returns:
            DataFrame: Percentile values for the specified feature
        """
        if self.panel_options is not None:
            if start_date is None:
                start_date = self.panel_options["startDate"]
            if end_date is None:
                end_date = self.panel_options["endDate"]
            if interval_type is None:
                interval_type = self.panel_options["intervalType"]
            if filters is None:
                filters = self.panel_options["filters"]
            if model_version is None:
                model_version = self.panel_options["modelVersion"]

        data = self._client.get_feature_percentiles(
            model_id=self.model_id,
            start_date=start_date,
            end_date=end_date,
            interval_type=interval_type,
            filters=filters,
            model_version=model_version,
        )
        # FIXME: Convert to dataframe
        return data


class API:
    """
    Main entry point for interacting with the Comet MPM API.

    Provides high-level methods for working with models and workspaces.

    Args:
        api_key: The Comet API key for authentication
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the Comet MPM API client.

        Args:
            api_key: The Comet API key for authentication
        """
        if api_key is None:
            api_key = get_config("comet.api_key")

        if api_key is None:
            api_key = os.environ.get("COMET_API_KEY")

        if api_key is None:
            raise Exception("COMET_API_KEY is not defined, and api_key is not given")

        self._client = Client(api_key)

    def get_panel_model(self):
        """
        Get a Model instance configured with panel options from configuration.

        This method creates a Model instance using the panel configuration
        stored in the COMET_PANEL_OPTIONS configuration key.

        Returns:
            Model: A Model instance configured with panel options

        Raises:
            KeyError: If required panel options are missing from configuration
            Exception: If panel options are not properly configured
        """
        panel_options = get_config("COMET_PANEL_OPTIONS")
        return Model(
            client=self._client,
            model_id=panel_options["modelId"],
            panel_options=panel_options,
        )
