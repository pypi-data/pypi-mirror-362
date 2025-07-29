#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type

import attrs
from loguru import logger

from data_diff.abcs.database_types import (
    JSON,
    Boolean,
    ColType_UUID,
    Date,
    Datetime,
    DbPath,
    Decimal,
    Float,
    FractionalType,
    Integer,
    Native_UUID,
    NumericType,
    String_UUID,
    TemporalType,
    Text,
    Time,
    Timestamp,
    TimestampTZ,
)
from data_diff.databases.base import (
    CHECKSUM_HEXDIGITS,
    CHECKSUM_OFFSET,
    BaseDialect,
    ConnectError,
    QueryError,
    QueryResult,
    ThreadedDatabase,
    import_helper,
)


@import_helper("sybase")
def import_sybase():
    import pyodbc

    return pyodbc


def generate_primes(limit: int) -> List[int]:
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i : limit + 1 : i] = [False] * len(range(i * i, limit + 1, i))
    return [i for i, is_prime in enumerate(sieve) if is_prime]


@attrs.define(frozen=False)
class Dialect(BaseDialect):
    name = "Sybase"
    ROUNDS_ON_PREC_LOSS = True
    SUPPORTS_PRIMARY_KEY: ClassVar[bool] = True
    SUPPORTS_INDEXES = True
    primes: List[int] = attrs.Factory(lambda: generate_primes(1000))
    column_prime_map: Dict[str, int] = attrs.Factory(dict)
    TYPE_CLASSES = {
        # Timestamps
        "datetimeoffset": TimestampTZ,
        "Datetimeoffset": TimestampTZ,
        "datetime2": Timestamp,
        "smalldatetime": Datetime,
        "datetime": Datetime,
        "timestamp": Datetime,
        "date": Date,
        "time": Time,
        "timestamp with time zone": TimestampTZ,
        # Numbers
        "float": Float,
        "real": Float,
        "decimal": Decimal,
        "money": Decimal,
        "smallmoney": Decimal,
        "numeric": Decimal,
        # int
        "int": Integer,
        "bigint": Integer,
        "tinyint": Integer,
        "smallint": Integer,
        "integer": Integer,
        "unsigned big int": Integer,
        "unsigned int": Integer,
        "unsigned small int": Integer,
        # Text
        "varchar": Text,
        "char": Text,
        "text": Text,
        "ntext": Text,  # ASE only
        "nvarchar": Text,  # ASE only
        "nchar": Text,  # ASE only
        "binary": Text,
        "varbinary": Text,
        "xml": Text,
        # UUID
        "uniqueidentifier": Native_UUID,
        # Bool
        "bit": Boolean,
        "varbit": Boolean,
        # JSON
        "json": JSON,
    }

    def quote(self, s: str, is_table: bool = False) -> str:
        if s in self.TABLE_NAMES and self.default_schema and is_table:
            return f"[{self.default_schema}].[{s}]"
        return f"[{s}]"

    def set_timezone_to_utc(self) -> str:
        raise NotImplementedError("Sybase does not support a session timezone setting.")

    def current_timestamp(self) -> str:
        return "GETDATE()"

    def current_database(self) -> str:
        return "DB_NAME()"

    def current_schema(self) -> str:
        return """default_schema_name
        FROM sys.database_principals
        WHERE name = CURRENT_USER"""

    def to_string(self, s: str, coltype: str = None) -> str:
        if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
            # Sybase IQ or FreeTDS detected as IQ: Use VARCHAR(2500)
            return f"CAST({s} AS VARCHAR(2500))"
        # Sybase ASE or FreeTDS detected as ASE: Handle nvarchar
        import re

        s_temp = re.sub(r'["\[\]`]', "", s)
        raw_col_info = self.get_column_raw_info(s_temp)
        if raw_col_info and raw_col_info.data_type in ["nvarchar", "nchar", "ntext"]:
            return f"CAST({s} AS NVARCHAR(5000))"  # ASE max for nvarchar
        return f"CAST({s} AS VARCHAR(2500))"

    def type_repr(self, t) -> str:
        try:
            if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
                return {bool: "bit", str: "varchar(2500)"}[t]
            return {bool: "bit", str: "nvarchar(5000)"}[t]
        except KeyError:
            return super().type_repr(t)

    def random(self) -> str:
        return "rand()"

    def is_distinct_from(self, a: str, b: str) -> str:
        return f"(({a}<>{b} OR {a} IS NULL OR {b} IS NULL) AND NOT({a} IS NULL AND {b} IS NULL))"

    def limit_select(
        self,
        select_query: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        has_order_by: Optional[bool] = None,
    ) -> str:
        import re

        def safe_trim(match):
            column_name = match.group(1)
            if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
                return f"TRIM(CAST({column_name} AS VARCHAR(2500)))"
            return f"TRIM(CAST({column_name} AS NVARCHAR(5000)))"

        select_query = re.sub(r"TRIM\(\[([\w]+)\]\)", safe_trim, select_query)

        select_query = re.sub(r"TRIM\(([\w]+)\)", safe_trim, select_query)

        if limit is not None:
            select_query = select_query.replace("SELECT", f"SELECT TOP {limit}", 1)

        # if not has_order_by:
        #     select_query += " ORDER BY RAND()"
        return select_query

    def constant_values(self, rows) -> str:
        values = ", ".join("(%s)" % ", ".join(self._constant_value(v) for v in row) for row in rows)
        return f"VALUES {values}"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        if isinstance(coltype, Datetime):
            if coltype.precision == 4:
                return f"CAST({value} AS VARCHAR(100))"
            if coltype.precision > 0:
                return (
                    f"CASE WHEN {value} IS NULL THEN NULL "
                    f"ELSE "
                    f"CAST(DATEPART(YEAR, {value}) AS CHAR(4)) + '-' + "
                    f"RIGHT('0' + CAST(DATEPART(MONTH, {value}) AS VARCHAR(2)), 2) + '-' + "
                    f"RIGHT('0' + CAST(DATEPART(DAY, {value}) AS VARCHAR(2)), 2) + ' ' + "
                    f"RIGHT('0' + CAST(DATEPART(HOUR, {value}) AS VARCHAR(2)), 2) + ':' + "
                    f"RIGHT('0' + CAST(DATEPART(MINUTE, {value}) AS VARCHAR(2)), 2) + ':' + "
                    f"RIGHT('0' + CAST(DATEPART(SECOND, {value}) AS VARCHAR(2)), 2) + '.' + "
                    f"RIGHT('00' + CAST(DATEPART(MILLISECOND, {value}) AS VARCHAR(3)), 3) "
                    f"END"
                )
            return (
                f"CASE WHEN {value} IS NULL THEN NULL "
                f"ELSE "
                f"CAST(DATEPART(YEAR, {value}) AS CHAR(4)) + '-' + "
                f"RIGHT('0' + CAST(DATEPART(MONTH, {value}) AS VARCHAR(2)), 2) + '-' + "
                f"RIGHT('0' + CAST(DATEPART(DAY, {value}) AS VARCHAR(2)), 2) + ' ' + "
                f"RIGHT('0' + CAST(DATEPART(HOUR, {value}) AS VARCHAR(2)), 2) + ':' + "
                f"RIGHT('0' + CAST(DATEPART(MINUTE, {value}) AS VARCHAR(2)), 2) + ':' + "
                f"RIGHT('0' + CAST(DATEPART(SECOND, {value}) AS VARCHAR(2)), 2) "
                f"END"
            )
        if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
            return f"CAST({value} AS VARCHAR(2500))"
        return f"CAST({value} AS NVARCHAR(5000))"

    def normalize_number(self, value: str, coltype: FractionalType) -> str:
        return self.to_string(f"CAST({value} AS DECIMAL(38, {coltype.precision}))")

    # def md5_as_int(self, s: str) -> str:
    #     """Returns an MD5 hash of the input string as an integer for Sybase IQ."""
    #     return f"CAST(HEXTOINT(LEFT(CAST(HASH({s}, 'MD5') AS VARCHAR(32)), 8)) AS BIGINT) - 140737488355327"

    # def md5_as_int(self, s: str) -> str:
    #     """Returns a hash-like integer based on ASCII values of the input string for Sybase."""
    #     # Create a simple hash using ASCII values and string length
    #     # This generates a pseudo-hash by combining ASCII values with position weights
    #     return (
    #         f"CAST(("
    #         f"  (LEN({s}) * 31) + "  # Length component
    #         f"  (ASCII(LEFT({s}, 1)) * 97) + "  # First character
    #         f"  (CASE WHEN LEN({s}) > 1 THEN ASCII(SUBSTRING({s}, 2, 1)) * 53 ELSE 0 END) + "  # Second character
    #         f"  (CASE WHEN LEN({s}) > 2 THEN ASCII(SUBSTRING({s}, 3, 1)) * 29 ELSE 0 END) + "  # Third character
    #         f"  (CASE WHEN LEN({s}) > 3 THEN ASCII(RIGHT({s}, 1)) * 17 ELSE 0 END)"  # Last character
    #         f") % 2147483647 AS BIGINT) - 1073741823"  # Modulo to keep in range and shift
    #     )

    # def md5_as_hex(self, s: str) -> str:
    #     return f"HashBytes('MD5', {s})"

    # def md5_as_hex(self, s: str) -> str:
    #     """Returns a hex representation based on ASCII values instead of MD5."""
    #     # Create a hex-like string using ASCII values
    #     return (
    #         f"RIGHT('0000000' + CONVERT(VARCHAR(8), "
    #         f"  (ASCII(LEFT({s}, 1)) * 256 + "
    #         f"   CASE WHEN LEN({s}) > 1 THEN ASCII(SUBSTRING({s}, 2, 1)) ELSE 0 END) % 65536"
    #         f"), 16), 8)"
    #     )

    def get_unique_prime_for_column(self, column_name: str) -> int:
        if column_name in self.column_prime_map:
            return self.column_prime_map[column_name]
        used_primes = set(self.column_prime_map.values())
        for p in self.primes:
            if p > 100 and p not in used_primes:
                self.column_prime_map[column_name] = p
                return p
        raise ValueError("Ran out of unique primes")

    def md5_as_int(self, s: str) -> str:
        if self.sybase_driver_type.is_ase or self.query_config_for_free_tds["ase_query_chosen"]:
            return f"CAST(HEXTOINT(LEFT(CAST(HASH({s}, 'MD5') AS VARCHAR(32)), 8)) AS BIGINT) - 140737488355327"
        base_prime = self.get_unique_prime_for_column(s)
        separator = " +\n        "
        parts = [f"LENGTH(COALESCE({s}, '')) * {base_prime}"]

        for i in range(15):
            parts.append(f"COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), {i + 1}, 1)), 0) * {self.primes[i]}")

        for i, pos in enumerate([20, 25, 30, 35, 40]):
            parts.append(
                f"(CASE WHEN LENGTH(COALESCE({s}, '')) >= {pos} "
                f"THEN COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), {pos}, 1)), 0) * {self.primes[15 + i]} ELSE 0 END)"
            )

        parts.append(
            f"(CASE WHEN LENGTH(COALESCE({s}, '')) > 15 "
            f"THEN COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), LENGTH(COALESCE({s}, '')), 1)), 0) * {self.primes[20]} ELSE 0 END)"
        )

        return f"CAST((\n        {separator.join(parts)}\n      ) % 2147483647 AS BIGINT)"

    def md5_as_hex(self, s: str) -> str:
        if self.sybase_driver_type.is_ase or self.query_config_for_free_tds["ase_query_chosen"]:
            return f"HashBytes('MD5', {s})"
        base_prime = self.get_unique_prime_for_column(s)
        separator = " +\n        "
        parts = [f"LENGTH(COALESCE({s}, '')) * {base_prime}"]

        for i in range(15):
            parts.append(f"COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), {i + 1}, 1)), 0) * {self.primes[i]}")

        for i, pos in enumerate([20, 25, 30, 35, 40]):
            parts.append(
                f"(CASE WHEN LENGTH(COALESCE({s}, '')) >= {pos} "
                f"THEN COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), {pos}, 1)), 0) * {self.primes[15 + i]} ELSE 0 END)"
            )

        parts.append(
            f"(CASE WHEN LENGTH(COALESCE({s}, '')) > 15 "
            f"THEN COALESCE(ASCII(SUBSTRING(COALESCE({s}, ''), LENGTH(COALESCE({s}, '')), 1)), 0) * {self.primes[20]} ELSE 0 END)"
        )

        return (
            f"RIGHT('00000000' + CONVERT(VARCHAR(8), (\n        {separator.join(parts)}\n      ) % 16777215), 16), 8)"
        )

    def concat(self, items: List[str]) -> str:
        """Provide SQL for concatenating multiple columns into a string for Sybase IQ."""
        assert len(items) > 1, "At least two columns are required for concatenation."
        return " || ".join(items)

    def normalize_uuid(self, value: str, coltype: ColType_UUID) -> str:
        if isinstance(coltype, String_UUID):
            if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
                return f"CAST({value} AS VARCHAR(2500))"  # IQ: Match column length
            return f"CAST({value} AS NVARCHAR(5000))"  # ASE: Match column length
        if self.sybase_driver_type.is_iq or self.query_config_for_free_tds["freetds_query_chosen"]:
            return f"CONVERT(VARCHAR(36), {value})"
        return f"CONVERT(NVARCHAR(36), {value})"

    def parse_table_name(self, name: str) -> DbPath:
        "Parse the given table name into a DbPath"
        self.TABLE_NAMES.append(name.split(".")[-1])
        return tuple(name.split("."))


@attrs.define(frozen=False, init=False, kw_only=True)
class Sybase(ThreadedDatabase):
    DIALECT_CLASS: ClassVar[Type[BaseDialect]] = Dialect
    CONNECT_URI_HELP = "sybase://<user>:<password>@<host>/<database>/<schema>"
    CONNECT_URI_PARAMS = ["database", "schema"]

    default_database: str
    _args: Dict[str, Any]
    _sybase: Any
    _conn: Any

    def __init__(self, host, port, user, password, *, database, thread_count, **kw) -> None:
        super().__init__(thread_count=thread_count)
        args = dict(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            **kw,
        )
        self._args = {k: v for k, v in args.items() if v}
        if self._args.get("odbc_driver", None) is not None:
            self._args["driver"] = self._args.pop("odbc_driver")
        else:
            self._args["driver"] = "FreeTDS"
        try:
            self.default_database = self._args["database"]
            self.default_schema = self._args["schema"]
            self.dialect.default_schema = self.default_schema
        except KeyError:
            raise ValueError("Specify a default database and schema.")
        self._sybase = import_sybase()
        self._detect_driver_type(self._args.get("driver", None))
        self._conn = self.create_connection()

    def create_connection(self):
        server = self._args.get("server", None) or ""
        host = self._args.get("host", None) or ""
        port = self._args.get("port", 5000)
        database = self._args.get("database", None)
        username = self._args.get("user", None)
        password = self._args.get("password", None)
        driver = self._args.get("driver", None)
        max_query_timeout = 60 * 60  # 3600 seconds

        if self.dialect.sybase_driver_type.is_freetds:
            conn_dict = {
                "driver": "FreeTDS",
                "database": database,
                "user": username,
                "password": password,
                "port": port,
                "tds_version": "auto",
            }

            conn_dict["host"] = host or server
            try:
                logger.debug(f"Attempting FreeTDS connection with config: {conn_dict}")
                self._conn = self._sybase.connect(**conn_dict)
                self._conn.timeout = max_query_timeout
                logger.info(f"Successfully connected to Sybase using FreeTDS: {conn_dict}")
                return self._conn
            except Exception as e:
                error_msg = f"Failed to connect to Sybase with FreeTDS: {str(e)}"
                logger.error(error_msg)
                raise ConnectError(error_msg) from e

        base_params = {
            "DRIVER": self._prepare_driver_string(driver),
            "DATABASE": database,
            "UID": username,
            "PWD": password,
        }
        connection_attempts = []
        if self.dialect.sybase_driver_type.is_ase:
            connection_attempts = [
                {
                    "key": "SERVER",
                    "value": host,
                    "port": port,
                },  # ASE typically uses SERVER
                {"key": "SERVERNAME", "value": host, "port": port},
                {
                    "key": "HOST",
                    "value": f"{host}:{port}",
                    "port": None,
                },  # Host:Port format
            ]
        else:
            connection_attempts = [
                {"key": "HOST", "value": f"{host}:{port}", "port": None},
                {"key": "HOST", "value": host, "port": port},
                {"key": "SERVER", "value": server, "port": port},
                {"key": "SERVERNAME", "value": server, "port": port},
            ]

        errors = []

        for attempt in connection_attempts:
            if not attempt["value"]:
                continue

            conn_dict = base_params.copy()
            conn_dict[attempt["key"]] = attempt["value"]

            # Handle port configuration
            if attempt["port"] is not None:
                port_configs = [
                    {"PORT": attempt["port"]},
                    {"Server port": attempt["port"]},
                    {},  # Try without explicit port
                ]
            else:
                port_configs = [{}]  # Port is already in the host string

            for port_config in port_configs:
                current_config = conn_dict.copy()
                current_config.update(port_config)

                # Add ASE-specific parameters if driver is ASE
                if self.dialect.sybase_driver_type.is_ase:
                    ase_configs = [
                        {},  # Basic config
                        {"NetworkAddress": f"{host},{port}"},  # Alternative format
                        {"ServerName": host},  # Another common ASE parameter
                    ]
                else:
                    ase_configs = [{}]

                for ase_config in ase_configs:
                    final_config = current_config.copy()
                    final_config.update(ase_config)

                    try:
                        logger.debug(f"Attempting connection with config: {final_config}")
                        self._conn = self._sybase.connect(**final_config)
                        self._conn.timeout = max_query_timeout
                        logger.info(
                            f"Successfully connected to Sybase using: "
                            f"driver={driver}, "
                            f"{attempt['key']}={attempt['value']}, "
                            f"port_config={port_config}, "
                            f"ase_config={ase_config}"
                        )
                        return self._conn
                    except Exception as e:
                        error_msg = (
                            f"Failed with {attempt['key']}={attempt['value']}, "
                            f"port_config={port_config}, "
                            f"ase_config={ase_config}: {str(e)}"
                        )
                        logger.debug(error_msg)
                        errors.append(error_msg)
                        continue
        raise ConnectError(f"Failed to connect to Sybase with all attempts. Errors: {errors}")

    def _normalize_driver(self, driver: str) -> str:
        """Normalize driver string by removing braces, spaces, and converting to lowercase."""
        return driver.replace("{", "").replace("}", "").replace(" ", "").strip().lower()

    def _detect_driver_type(self, driver: str) -> None:
        """Detect and set the appropriate driver type."""
        normalized_driver = self._normalize_driver(driver)
        self.dialect.sybase_driver_type.is_ase = "adaptive" in normalized_driver
        self.dialect.sybase_driver_type.is_iq = "iq" in normalized_driver
        self.dialect.sybase_driver_type.is_freetds = "freetds" in normalized_driver

    def _prepare_driver_string(self, driver: str) -> str:
        """Ensure driver string is properly formatted with braces."""
        return f"{{{driver}}}" if not driver.startswith("{") else driver

    def select_table_schema(self, path: DbPath) -> str:
        database, schema, name = self._normalize_table_path(path)
        if self.dialect.sybase_driver_type.is_iq:
            return (
                f"SELECT c.column_name, d.domain_name AS data_type, "
                f"CASE WHEN d.domain_name IN ('DATE', 'TIME', 'TIMESTAMP') THEN c.scale ELSE NULL END AS datetime_precision, "
                f"CASE WHEN t.name IN ('float') THEN 15 WHEN t.name IN ('real') THEN 7 ELSE c.prec END AS numeric_precision, "
                f"CASE WHEN t.name IN ('float', 'real') THEN NULL ELSE c.scale END AS numeric_scale, "
                f"NULL AS collation_name, c.width AS character_maximum_length "
                f"FROM {database}.SYS.SYSTABLE t "
                f"JOIN {database}.SYS.SYSCOLUMN c ON t.table_id = c.table_id "
                f"JOIN {database}.SYS.SYSDOMAIN d ON c.domain_id = d.domain_id "
                f"JOIN {database}.SYS.SYSUSER u ON t.creator = u.user_id "
                f"WHERE t.table_name = '{name}' "
                f"AND u.user_name = '{schema}'"
            )
        elif self.dialect.sybase_driver_type.is_ase:
            return (
                f"SELECT c.name AS column_name, t.name AS data_type, "
                f"CASE WHEN c.type IN (61, 111) THEN c.prec ELSE NULL END AS datetime_precision, "
                f"CASE WHEN t.name IN ('float') THEN 15 WHEN t.name IN ('real') THEN 7 ELSE c.prec END AS numeric_precision, "
                f"CASE WHEN t.name IN ('float', 'real') THEN NULL ELSE c.scale END AS numeric_scale, "
                f"NULL AS collation_name, c.length AS character_maximum_length "
                f"FROM {database}..sysobjects o "
                f"JOIN {database}..syscolumns c ON o.id = c.id "
                f"JOIN {database}..systypes t ON c.usertype = t.usertype "
                f"JOIN {database}..sysusers u ON o.uid = u.uid "
                f"WHERE o.name = '{name}' "
                f"AND u.name = '{schema}'"
            )
        elif self.dialect.sybase_driver_type.is_freetds:
            ase_query = (
                f"SELECT c.name AS column_name, t.name AS data_type, "
                f"CASE WHEN c.type IN (61, 111) THEN c.prec ELSE NULL END AS datetime_precision, "
                f"CASE WHEN t.name IN ('float') THEN 15 WHEN t.name IN ('real') THEN 7 ELSE c.prec END AS numeric_precision, "
                f"CASE WHEN t.name IN ('float', 'real') THEN NULL ELSE c.scale END AS numeric_scale, "
                f"NULL AS collation_name, c.length AS character_maximum_length "
                f"FROM {database}..sysobjects o "
                f"JOIN {database}..syscolumns c ON o.id = c.id "
                f"JOIN {database}..systypes t ON c.usertype = t.usertype "
                f"JOIN {database}..sysusers u ON o.uid = u.uid "
                f"WHERE o.name = '{name}' "
                f"AND u.name = '{schema}'"
            )
            iq_query = (
                f"SELECT c.name AS column_name, t.name AS data_type, "
                f"CASE WHEN c.type IN (61, 111) THEN c.prec ELSE NULL END AS datetime_precision, "
                f"CASE WHEN t.name IN ('float') THEN 15 WHEN t.name IN ('real') THEN 7 ELSE c.prec END AS numeric_precision, "
                f"CASE WHEN t.name IN ('float', 'real') THEN NULL ELSE c.scale END AS numeric_scale, "
                f"NULL AS collation_name, c.length AS character_maximum_length "
                f"FROM {database}.dbo.sysobjects o "
                f"JOIN {database}.dbo.syscolumns c ON o.id = c.id "
                f"JOIN {database}.dbo.systypes t ON c.usertype = t.usertype "
                f"JOIN {database}.dbo.sysusers u ON o.uid = u.uid "
                f"WHERE o.name = '{name}' AND u.name = '{schema}'"
            )
            if self.dialect.query_config_for_free_tds["ase_query_chosen"]:
                return ase_query
            elif self.dialect.query_config_for_free_tds["freetds_query_chosen"]:
                return iq_query
            try:
                if self._query_cursor(self._conn.cursor(), ase_query, test_query=True):
                    logger.info("Sybase ASE Detected")
                    self.dialect.query_config_for_free_tds["ase_query_chosen"] = True
                    return ase_query
                else:
                    logger.info("Sybase IQ Detected")
                    self.dialect.query_config_for_free_tds["freetds_query_chosen"] = True
                    return iq_query
            except Exception as e:
                logger.error(f"Failed to execute test query: {e}")
                raise QueryError(f"Failed to execute test query: {e}")
        else:
            ValueError(
                f"{self.name}: Unsupported driver type: {self._args['driver']}. Supported drivers: ASE, IQ, FreeTDS."
            )

    def _normalize_table_path(self, path: DbPath) -> DbPath:
        if len(path) == 1:
            return self.default_database, self.default_schema, path[0]
        elif len(path) == 2:
            return self.default_database, path[0], path[1]
        elif len(path) == 3:
            return path

        raise ValueError(
            f"{self.name}: Bad table path for {self}: '{'.'.join(path)}'. Expected format: table, schema.table, or database.schema.table"
        )

    def _query_cursor(self, c, sql_code, test_query: bool = False):
        if test_query:
            try:
                c.execute(sql_code)
                return True
            except Exception as e:
                logger.warning(f"Test query failed: {sql_code}, error: {e}")
                return False
        try:
            c.execute(sql_code)
            if sql_code.lower().startswith(("select", "explain", "show")):
                columns = c.description and [col[0] for col in c.description]
                return QueryResult(c.fetchall(), columns)
            elif sql_code.lower().startswith(("create", "drop")):
                try:
                    c.connection.commit()
                except AttributeError:
                    ...
        except Exception as _e:
            try:
                c.connection.rollback()
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {rollback_error}")
            raise

    def close(self):
        super().close()
        if self._conn is not None:
            self._conn.close()
