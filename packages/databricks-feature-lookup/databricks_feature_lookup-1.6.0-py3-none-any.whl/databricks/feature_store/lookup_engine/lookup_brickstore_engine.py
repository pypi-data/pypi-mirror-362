import logging
import os
import random
from contextlib import contextmanager
from typing import Optional, Tuple

import jwt
import sqlalchemy

from databricks.feature_store.lookup_engine.lookup_sql_engine import LookupSqlEngine
from databricks.feature_store.lookup_engine.oauth_token_manager import OAuthTokenManager
from databricks.feature_store.utils.brickstore_constants import (
    LAKEBASE_OAUTH_TOKEN_FILE_PATH,
)
from databricks.feature_store.utils.logging_utils import get_logger
from databricks.ml_features_common.entities.online_feature_table import (
    OnlineFeatureTable,
)

LOOKUP_SSL_CERT_PATH_ENV = "LOOKUP_SSL_CERT_PATH"
FEATURE_SERVING_LAKEBASE_POOL_RECYCLE_SECONDS = (
    "FEATURE_SERVING_LAKEBASE_POOL_RECYCLE_SECONDS"
)


_logger = get_logger(__name__, log_level=logging.INFO)


class LookupBrickstoreEngine(LookupSqlEngine):
    def __init__(
        self, online_feature_table: OnlineFeatureTable, ro_user: str, ro_password: str
    ):
        self.engine = None
        self._oauth_token_manager = OAuthTokenManager(
            oauth_token_file_path=LAKEBASE_OAUTH_TOKEN_FILE_PATH,
            password_override=ro_password,
        )
        # The parent constructor calls get_connection which requires the oauth token to be set.
        # So we need to set the oauth token manager before calling super().__init__
        super().__init__(online_feature_table, ro_user, ro_password)
        self._oauth_token_manager.start_token_refresh_thread()

    # Override
    def _get_database_and_table_name(
        self, online_table_name
    ) -> Tuple[str, Optional[str], str]:
        name_components = online_table_name.split(".")
        if len(name_components) != 3:
            raise ValueError(
                f"Online table name {online_table_name} is misformatted and must be in 3L format for Lakebase stores"
            )
        return (name_components[0], name_components[1], name_components[2])

    # Override
    def is_lakebase_engine(self) -> bool:
        return True

    # Lakebase sql connection uses a connection pool
    # Override
    @contextmanager
    def _get_connection(self):
        if self.engine is None:
            _logger.info(f"Connecting to {self.host}")
            pool_recycle = int(
                os.environ.get(FEATURE_SERVING_LAKEBASE_POOL_RECYCLE_SECONDS, 900)
            )
            # Add randomization to distribute connection recycling
            pool_recycle_with_jitter = pool_recycle + random.randint(0, 20)
            self.engine = sqlalchemy.create_engine(
                self.engine_url,
                pool_size=10,
                max_overflow=20,
                pool_timeout=2,
                # This might need tuning. Smaller number causes more frequent reconnection, bigger number causes
                # slower reaction to scaling up or down.
                pool_recycle=pool_recycle_with_jitter,
            )

        connection = self.engine.connect()
        # When the caller invokes "with _get_connection() as x", the connection will be returned as "x"
        yield connection

        # Everything below here will be executed in contextmanager.__exit__()
        # With connection pooling, .close() only returns the connection to the pool instead of closing it.
        connection.close()

    @property
    def engine_url(self):
        oauth_token_or_password = (
            self._oauth_token_manager.get_oauth_token_or_password()
        )
        # self.user is parsed from EnvVar. If not set, parse the client_id
        # from the oauth token
        db_user = self.user
        if not db_user:
            content = jwt.decode(
                oauth_token_or_password,
                algorithms=["RS256"],
                # No worry, the token is validated by Postgres
                options={"verify_signature": False},
            )
            db_user = content["client_id"]
        _logger.info(f"Quering as user: {db_user}")
        base_str = f"postgresql+psycopg2://{db_user}:{oauth_token_or_password}@{self.host}:{self.port}/{self.database_name}?sslmode=require"
        cert_path = os.environ.get(LOOKUP_SSL_CERT_PATH_ENV)
        if cert_path:
            return f"{base_str}&ssl_ca={cert_path}&ssl_verify_identity=False"
        else:
            return base_str

    # Override
    def _database_contains_feature_table(self, sql_connection):
        # TODO[ML-53997]: implement validation
        return True

    # Override
    def _database_contains_primary_keys(self, sql_connection):
        # TODO[ML-53997]: implement validation
        return True

    # Override
    @classmethod
    def _sql_safe_name(cls, name):
        return name
