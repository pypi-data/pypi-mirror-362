from functools import reduce
from typing import Any, Dict, List

import pandas as pd

from databricks.feature_store.entities.feature_table_metadata import (
    FeatureTableMetadata,
)
from databricks.feature_store.online_lookup_client import OnlineLookupClient
from databricks.feature_store.utils.collection_utils import LookupKeyList
from databricks.feature_store.utils.lookup_key_utils import LookupKeyType
from databricks.ml_features_common.entities.feature_spec import FeatureSpec
from databricks.ml_features_common.entities.online_feature_table import (
    PrimaryKeyDetails,
)


class _PgTableFetcher:
    """
    Each (feature_table, lookup_keys) pair is associated with a single _PgTableFetcher instance.
    """

    def __init__(
        self,
        lookup_key: LookupKeyType,
        primary_keys: List[PrimaryKeyDetails],
        feature_columns: List[str],
        lookup_client: OnlineLookupClient,
    ):
        """
        Args:
            lookup_key: A list of input column names. The ordering needs to match the ordering of the primary keys.
            primary_keys: Primary keys of the online table
            feature_columns: A list of feature columns to fetch
            lookup_client: Lookup client for the online table
        """
        self.lookup_key = lookup_key
        self.lookup_client = lookup_client
        self.feature_columns = feature_columns
        self._primary_key_names = [pk.name for pk in primary_keys]

    def _build_lookup_key_list(self, rows: List[Dict[str, Any]]) -> LookupKeyList:
        return LookupKeyList(
            columns=self._primary_key_names,
            rows=[[row[lookup_key] for lookup_key in self.lookup_key] for row in rows],
        )

    def fetch(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        lookup_key_list = self._build_lookup_key_list(rows)
        return self.lookup_client.lookup_feature_dicts(
            lookup_key_list, self.feature_columns
        )


class PostgresFetcher:
    def __init__(
        self,
        feature_spec: FeatureSpec,
        lookup_clients: Dict[str, OnlineLookupClient],
        ft_metadatas: Dict[str, FeatureTableMetadata],
    ):
        """
        Initialize the PostgresFetcher.
        Args:
            feature_spec: FeatureSpec
            lookup_clients: feature table name -> lookup client
            ft_metadatas: feature table name -> feature_table_metadata
        """
        self.table_fetchers = {}
        self._output_names = [
            ci.output_name for ci in feature_spec.column_infos if ci.include
        ]
        self._all_column_names = [ci.output_name for ci in feature_spec.column_infos]

        for ft, ft_metadata in ft_metadatas.items():
            for (
                lookup_key,
                feature_column_infos,
            ) in ft_metadata.feature_col_infos_by_lookup_key.items():
                feature_columns = [fci.output_name for fci in feature_column_infos]
                self.table_fetchers[(ft, lookup_key)] = _PgTableFetcher(
                    lookup_key,
                    ft_metadata.online_ft.primary_keys,
                    feature_columns,
                    lookup_clients[ft],
                )

    def lookup_features(self, df: pd.DataFrame) -> List[dict[str, Any]]:
        """
        Lookup features.

        Args:
            df: DataFrame with lookup keys.

        Returns:
            List of dictionaries with features.
        """
        input_rows = df.to_dict(orient="records")
        results = [
            fetcher.fetch(input_rows) for fetcher in self.table_fetchers.values()
        ]
        # Merge all results by rows.
        all_results = [
            reduce(lambda a, b: {**a, **b}, group, {})
            for group in zip(*results, input_rows)
        ]
        if all_results and len(self._all_column_names) == len(self._output_names):
            return all_results
        else:
            # TODO[ML-55717]: Optimize the filtering performance.
            # filter out the columns that are excluded.
            return [
                {k: v for k, v in result.items() if k in self._output_names}
                for result in all_results
            ]

    def get_model_input_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get the model input DataFrame.
        """
        feature_values = self.lookup_features(df)
        # convert the feature_values to a DataFrame
        return pd.DataFrame(feature_values)
