from pyspark.sql.functions import col, lit

SPARK_POSTGRES_DRIVER = "org.postgresql.Driver"
CACHED_CSV_FOLDER = "cache_all"

DATATABLE_COLUMNS_LIST = ["__id", "__ts"]
DATATABLE_COLUMNS_SCHEMA = "__id INT, __ts TIMESTAMP"
CODELIST_SCHEMA = "id INT, code STRING, selection_only BOOLEAN, description_en STRING, description_fr STRING, description_es STRING, description_zh STRING, description_ru STRING, description_ar STRING, start_date DATE, end_date DATE, sort INT, unit_of_measure INT, type STRING"
FLAGLIST_SCHEMA = "code STRING, description STRING"


class IcebergDatabases:
    CATALOG = "AwsDataCatalog"
    STAGING_SCHEME = "sws_dissemination_tags_bronze"
    BRONZE_SCHEME = "sws_dissemination_tags_bronze"
    SILVER_SCHEME = "sws_dissemination_tags_silver"
    GOLD_SCHEME = "sws_dissemination_tags_gold"
    STAGING_DATABASE = f"{CATALOG}.{STAGING_SCHEME}"
    BRONZE_DATABASE = f"{CATALOG}.{BRONZE_SCHEME}"
    SILVER_DATABASE = f"{CATALOG}.{SILVER_SCHEME}"
    GOLD_DATABASE = f"{CATALOG}.{GOLD_SCHEME}"


class DomainFilters:
    GENERIC = lambda domain_code: (
        col("domain").isNull()
        | (col("domain") == lit(""))
        | (col("domain") == lit(domain_code))
    )
    MATCH = lambda domain_code: (col("domain") == lit(domain_code))
    EMPTY = lambda: (col("domain").isNull() | (col("domain") == lit("")))


class DatasetDatatables:

    class __SWSDatatable:
        def __init__(self, id: str, name: str, schema: str):
            self.id = id
            self.name = name
            self.schema = schema

    # Dissemination Tables
    DISSEMINATION_TYPE_LIST = __SWSDatatable(
        id="datatables.dissemination_{type}_list",
        name="Dissemination - {type} list",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, code STRING, name STRING, aggregation_type STRING, dissemination BOOLEAN, aggregation BOOLEAN",
    )
    DISSEMINATION_EXCEPTIONS = __SWSDatatable(
        id="datatables.dissemination_exception",
        name="Dissemination - Exceptions",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, dim1_code STRING, dim2_code STRING, dim3_code STRING, dim4_code STRING, dim5_code STRING, dim6_code STRING, dim7_code STRING, status_flag STRING, method_flag STRING, dissemination BOOLEAN, aggregation BOOLEAN, note STRING",
    )
    DISSEMINATION_ITEM_LIST_FAOSTAT = __SWSDatatable(
        id="datatables.dissemination_item_list_faostat",
        name="Dissemination - Item list - FAOSTAT",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, code STRING, name STRING, aggregation_type STRING, dissemination BOOLEAN, aggregation BOOLEAN",
    )

    # Mapping Tables
    MAPPING_DOMAINS_ID = __SWSDatatable(
        id="datatables.aggregates_mapping_domains_id",
        name="Mapping - Domains ID",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, domain_name STRING, sws_source_id STRING, sws_destination_id STRING",
    )
    MAPPING_CODELIST_TYPE = __SWSDatatable(
        id="datatables.mapping_codelist_type",
        name="Mapping Codelist type",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, col_name STRING, col_type STRING",
    )
    MAPPING_CODE_CORRECTION = __SWSDatatable(
        id="datatables.aggregates_mapping_code_correction",
        name="Mapping - Code correction",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, old_code STRING, new_code STRING, var_type STRING, delete BOOLEAN, multiplier FLOAT, mapping_type STRING",
    )
    MAPPING_SDMX_COLUMN_NAMES = __SWSDatatable(
        id="datatables.mapping_sdmx_col_names",
        name="Mapping - SDMX column names",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, internal_name STRING, external_name STRING, delete BOOLEAN, add BOOLEAN, default_value STRING",
    )
    MAPPING_SDMX_CODES = __SWSDatatable(
        id="datatables.mapping_pre_dissemination",
        name="Mapping - Pre dissemination",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, internal_code STRING, external_code STRING, var_type STRING, delete BOOLEAN, multiplier FLOAT, mapping_type STRING",
    )
    MAPPING_UNITS_OF_MEASURE = __SWSDatatable(
        id="datatables.mapping_units_of_measure",
        name="Mapping - Units of measure",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, domain STRING, sws_code STRING, sws_multiplier INT, sdmx_code STRING, sdmx_multiplier INT, value_multiplier INT, delete BOOLEAN, mapping_type STRING",
    )

    # Non-SWS Sources Tables
    FAOSTAT_CODE_MAPPING = __SWSDatatable(
        id="datatables.faostat_code_mapping",
        name="FAOSTAT Code Mapping",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, faostat_code_type STRING, faostat_code STRING, mapping_type STRING, mapped_code STRING",
    )
    FS_INPUT_MAPPING = __SWSDatatable(
        id="datatables.fs_input_mapping",
        name="FS Input Mapping",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, DomainCode STRING, Code STRING, Var2Code STRING, Var3Code STRING, Mult INT, 3YrAvgFlag INT, Flag STRING",
    )
    HCES_INPUT_MAPPING = __SWSDatatable(
        id="datatables.hces_input_mapping",
        name="HCES Input Mapping",
        schema=f"{DATATABLE_COLUMNS_SCHEMA}, variable STRING, indicator STRING, element STRING, decimals STRING",
    )


class DatasetTables:
    class __SWSTable:
        def __init__(self, postgres_id: str, iceberg_id: str, schema: str):
            self.postgres_id = postgres_id
            self.iceberg_id = iceberg_id
            self.schema = schema

    def __get_obs_coord_schema(self) -> str:

        obs_coord_schema_prefix = (
            "id BIGINT, approved_observation BIGINT, num_version BIGINT, "
        )

        dimensions_schema = (
            " INT, ".join(self.__dataset_details["dimensionColumns"]) + " INT"
        )

        return obs_coord_schema_prefix + dimensions_schema

    def __init__(self, dataset_id: str, dataset_details: dict) -> None:
        self.__dataset_id = dataset_id
        self.__dataset_details = dataset_details

        # Data
        self.OBSERVATION = self.__SWSTable(
            postgres_id=f"{self.__dataset_id}.observation",
            iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.{self.__dataset_id}_observation",
            schema="id BIGINT, observation_coordinates BIGINT, version INT, value FLOAT, flag_obs_status STRING, flag_method STRING, created_on TIMESTAMP, created_by INT, replaced_on TIMESTAMP",
        )
        self.OBSERVATION_COORDINATE = self.__SWSTable(
            postgres_id=f"{self.__dataset_id}.observation_coordinate",
            iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.{self.__dataset_id}_observation_coordinate",
            schema=self.__get_obs_coord_schema(),
        )
        self.METADATA = self.__SWSTable(
            postgres_id=f"{self.__dataset_id}.metadata",
            iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.{self.__dataset_id}_metadata",
            schema="id BIGINT, observation BIGINT, metadata_type INT, language INT, copy_metadata BIGINT",
        )
        self.METADATA_ELEMENT = self.__SWSTable(
            postgres_id=f"{self.__dataset_id}.metadata_element",
            iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.{self.__dataset_id}_metadata_element",
            schema="id BIGINT, metadata INT, metadata_element_type INT, value STRING",
        )

        # Reference data
        self.CODELISTS = [
            self.__SWSTable(
                postgres_id=dimension["codelist"]["table"],
                iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.{dimension['codelist']['table'].split('.')[1]}",
                schema=CODELIST_SCHEMA,
            )
            for dimension in dataset_details["dimensions"]
        ]

    FLAG_METHOD = __SWSTable(
        postgres_id="reference_data.flag_method",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.flag_method",
        schema=FLAGLIST_SCHEMA,
    )
    FLAG_OBS_STATUS = __SWSTable(
        postgres_id="reference_data.flag_obs_status",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.flag_obs_status",
        schema=FLAGLIST_SCHEMA,
    )
    METADATA_TYPE = __SWSTable(
        postgres_id="reference_data.metadata_type",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.metadata_type",
        schema="id INT, code STRING, description STRING, mandatory BOOLEAN, repeatable BOOLEAN",
    )
    METADATA_ELEMENT_TYPE = __SWSTable(
        postgres_id="reference_data.metadata_element_type",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.metadata_element_type",
        schema="id INT, metadata_type INT, code STRING, description STRING, mandatory BOOLEAN, repeatable BOOLEAN, private BOOLEAN",
    )

    LANGUAGE = __SWSTable(
        postgres_id="reference_data.language",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.language",
        schema="id INT, country_code STRING, description STRING",
    )

    UNIT_OF_MEASURE = __SWSTable(
        postgres_id="reference_data.unit_of_measure",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.unit_of_measure",
        schema="id INT, code STRING, sdmx_code STRING, metric BOOLEAN, description STRING, symbol STRING, base_unit STRING, multiplier DECIMAL",
    )

    # Operational data
    USER = __SWSTable(
        postgres_id="operational_data.user",
        iceberg_id=f"{IcebergDatabases.STAGING_DATABASE}.user",
        schema="id INT, username STRING, preferences INT, email STRING, active BOOLEAN, settings STRING",
    )


class IcebergTable:
    def __init__(self, level: str, iceberg_id: str, path: str, csv_path: str):
        self.level = level.lower()
        self.iceberg_id = iceberg_id
        self.table = iceberg_id.split(".")[-1]
        self.path = path
        self.csv_prefix = csv_path.rsplit("/", 1)[0]
        self.csv_path = csv_path


class IcebergTables:

    def __init__(self, dataset_id: str, tag_name: str, domain: str = "") -> None:
        self.__dataset_id = dataset_id
        self.__tag_name = tag_name

        # TODO Fix later with a more appropriate DATABASE
        self.TABLE = self._create_iceberg_table("BRONZE")
        self.TABLE_FILTERED = self._create_iceberg_table("BRONZE", suffix="filtered")
        self.BRONZE = self._create_iceberg_table("BRONZE")
        self.BRONZE_DISS_TAG = self._create_iceberg_table("BRONZE", suffix="diss_tag")
        self.SILVER = self._create_iceberg_table("SILVER", prefix=domain)

        # GOLD tables with specific suffixes
        self.GOLD_SWS = self._create_iceberg_table(
            "GOLD", prefix=domain, suffix="sws"
        )
        self.GOLD_SDMX = self._create_iceberg_table(
            "GOLD", prefix=domain, suffix="sdmx_disseminated"
        )
        self.GOLD_SWS_VALIDATED = self._create_iceberg_table(
            "GOLD", prefix=domain, suffix="sws_validated"
        )
        self.GOLD_SWS_DISSEMINATED = self._create_iceberg_table(
            "GOLD", prefix=domain, suffix="sws_disseminated"
        )
        self.GOLD_PRE_SDMX = self._create_iceberg_table(
            "GOLD", prefix=domain, suffix="pre_sdmx"
        )

    def _create_iceberg_table(
        self, level: str, prefix: str = "", suffix: str = ""
    ) -> IcebergTable:
        database = getattr(IcebergDatabases, f"{level}_DATABASE")
        scheme = getattr(IcebergDatabases, f"{level}_SCHEME")

        if prefix != "":
            prefix = f"{prefix}_".lower()
        if suffix != "":
            suffix = f"_{suffix}".lower()

        iceberg_id = f"{database}.{prefix}{self.__dataset_id}{suffix}"
        path = f"{scheme}/{prefix}{self.__dataset_id}{suffix}"
        csv_path = f"{CACHED_CSV_FOLDER}/{scheme}/{prefix}{self.__dataset_id}{suffix}/{self.__tag_name}.csv"

        return IcebergTable(level, iceberg_id, path, csv_path)
