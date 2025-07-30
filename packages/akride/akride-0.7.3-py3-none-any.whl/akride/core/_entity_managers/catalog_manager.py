import os
import time
import types
from collections import defaultdict
from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
import pandas as pd
import requests
from akridata_akrimanager_v2.models import (
    CreateCatalogTableResponse,
    GetPreSignedUrlResponse,
    ListPreSignedUrlResponse,
)

from akride import Constants, logger
from akride._utils.catalog.catalog_tables_helper import CatalogTablesHelper
from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.catalogs import Catalog
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.exceptions import ServerError, UserError
from akride.core.models.catalogs.catalog_view_info import CatalogViewInfo
from akride.core.models.catalogs.import_catalog_job import (
    ImportCatalogJobDetails,
)
from akride.core.types import (
    CatalogTable,
    ClientManager,
    Column,
    JoinCondition,
    SampleInfoList,
)


class CatalogManager(Manager):
    """Class managing external catalog operations on DataExplorer"""

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.catalog_api = am.CatalogApi(cli_manager.am_client)
        self.ext_catalog_api = am.ExternalCatalogApi(cli_manager.am_client)
        self.catalog_source_api = dsp.CatalogSourceTagApi(
            cli_manager.dsp_client
        )
        self.views_api = am.ViewsApi(cli_manager.am_client)

    @translate_api_exceptions
    def create_entity(self, spec: Dict[str, Any]) -> Optional[Catalog]:
        """
        Creates a new catalog.

        Parameters
        ----------
        spec : Dict[str, Any]
            The catalog spec.

        Returns
        -------
        Entity
            The created catalog
        """
        return self._create_catalog(**spec)

    def _create_catalog(self, **kwargs) -> Optional[Catalog]:
        logger.debug("Got %s", kwargs)
        # TODO: Implement this
        return None

    @translate_api_exceptions
    def delete_entity(self, entity: Entity) -> bool:
        """
        Deletes an entity.

        Parameters
        ----------
        entity : Entity
            The entity object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        dataset_id = entity.dataset_id
        delete_request = am.DeleteCatalogTableRequest(dataset_id, [entity.id])
        api_response = self.catalog_api.delete_catalog_table(delete_request)
        return api_response.message == "Table deleted successfully."

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Catalog]:
        """
        Retrieves information about external catalogs.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                name : str
                    filter by catalog name
                status : str
                    filter by catalog status, can be one of
                    "active","inactive", "refreshing", "offline",
                    "invalid-config"

        Returns
        -------
        List[Entity]
            A list of Entity objects representing external catalogs.
        """
        logger.debug("got attributes %s", attributes)
        valid_keys = ["name", "status"]
        invalid_keys = [
            key for key in attributes.keys() if key not in valid_keys
        ]
        if invalid_keys:
            raise ValueError(f"Invalid attributes: {', '.join(invalid_keys)}")

        api_response: am.ListCatalogsResponse = (
            self.ext_catalog_api.list_external_catalogs()
        )  # type: ignore
        if api_response.response and len(api_response.response) == 0:
            return []
        filtered_catalogs = api_response.response
        assert filtered_catalogs is not None
        if attributes:
            for key, val in attributes.items():
                filtered_catalogs = [
                    obj
                    for obj in filtered_catalogs  # type: ignore
                    if getattr(obj, key) == val
                ]
        ext_catalog_list = [Catalog(info) for info in filtered_catalogs]
        return ext_catalog_list

    @translate_api_exceptions
    def get_catalogs(
        self, dataset: Dataset, attributes: Dict[str, Any] = {}
    ) -> List[Entity]:
        """
        Retrieves information about entities that have the given attributes.

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        attributes: Dict[str, Any]
            The filter specification.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing catalogs.
        """
        logger.debug("got attributes %s", attributes)
        api_response: am.CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset.get_id())
        )  # type: ignore

        # TODO: filter according to the attributes argument
        catalog_list = [
            Catalog(types.SimpleNamespace(id=table.abs_name, name=table.name))
            for table in api_response.dataset_tables
        ]

        for catalog in catalog_list:
            catalog.dataset_id = dataset.id
        return catalog_list

    @translate_api_exceptions
    def get_catalog_data_count(
        self,
        dataset: Dataset,
        table_name: str,
        filter_str: Optional[str] = None,
    ) -> int:
        """
        Retrieves the count of the number of rows in a catalog table based on filters

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        table_name: str
            The catalog table name
        filter_str: str
            Filter the rows based on values

        Returns
        -------
        int
            The number of rows filtered
        """
        req_data = am.CatalogCountRequestBody(
            dataset_id=dataset.get_id(),
            table_name=table_name,
            filter_str=filter_str,
        )

        resp: am.CatalogDataCountResponse = (
            self.catalog_api.get_catalog_data_count(req_data)
        )
        return resp.count

    @translate_api_exceptions
    def get_catalog_by_name(
        self, dataset: Dataset, name: str
    ) -> Optional[Entity]:
        """
        Retrieves an entity with the given name.

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        name : str
            The name of the catalog to retrieve.

        Returns
        -------
        Entity
            The Entity object.
        """
        attrs = {"search_key": name}
        entity_list = self.get_catalogs(dataset, attrs)
        if entity_list is None:
            return None

        for entity in entity_list:
            if entity.name == name:
                return entity
        return None

    @translate_api_exceptions
    def get_catalog_tags(self, samples: SampleInfoList) -> pd.DataFrame:
        """
        Retrieves the catalog tags corresponding to the samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve catalog tags for.

        Returns
        -------
        pd.DataFrame
            A dataframe of catalog tags.
        """
        job_id = samples.job_id
        points = ",".join(map(str, samples.get_point_ids()))
        api_response = (
            self.catalog_source_api.fetch_catalog_db_tags(  # noqa E501
                rid=job_id, points=points
            )
        )

        columns = [item.column_name for item in api_response.column_meta]
        data = api_response.data
        df_dict = {key: [] for key in columns}

        # Convert from list of list of lists to a list of lists
        rows = [row for data_rows in data for row in data_rows.tags]
        # Extract the values for every row
        for tags in rows:
            for tag in tags:
                tag: dsp.ColumnData
                df_dict[tag.column_name].append(tag.value)
        return pd.DataFrame.from_dict(df_dict)

    def _create_table(
        self,
        dataset_id: str,
        table_name: str,
        col_list: List[Dict[str, str]],
        visualizable: bool = False,
        indices: Optional[List[str]] = None,
    ):
        if indices is None:
            indices = []

        table = am.ExternalCatalogTable(
            name=table_name,
            columns=col_list,
            description=table_name,
            visualizable=visualizable,
            indices=indices,
        )
        catalog_request = am.CreateCatalogTableRequest(
            dataset_id=dataset_id, catalog_table=table
        )
        response: CreateCatalogTableResponse = (
            self.catalog_api.create_catalog_table(catalog_request)
        )
        return response.abs_table_name

    @translate_api_exceptions
    def import_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        import_identifier: Optional[str] = None,
    ) -> bool:
        """
        Imports a catalog into a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing the catalog data.
        import_identifier: str
            Unique identifier for importing data

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        sql_mapping = defaultdict(lambda: "VARCHAR(255)")
        sql_mapping.update(
            {
                "object": "VARCHAR(255)",
                "int64": "BIGINT",
                "float64": "DOUBLE",
                "datetime64[ns]": "DATETIME",
                "int32": "INT",
                "float32": "FLOAT",
                "timedelta[ns]": "TIME",
            }
        )
        df = pd.read_csv(csv_file_path)
        col_list = [
            {"name": col_name, "type": sql_mapping[str(col_type)]}
            for col_name, col_type in zip(df.columns, df.dtypes)
        ]
        self._create_table(
            dataset_id=dataset.get_id(),
            table_name=table_name,
            col_list=col_list,
        )

        return self.add_to_catalog(
            dataset, table_name, csv_file_path, df, import_identifier
        )

    @translate_api_exceptions
    def add_to_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        df: pd.DataFrame = None,
        import_identifier: Optional[str] = None,
    ) -> bool:
        """
        Adds new items to an existing catalog.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing new catalog data.
        df: pd.DataFrame
            Dataframe containing catalog data to import
        import_identifier: str
            Unique identifier for importing data

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        # upload CSV file to S3
        file_name = os.path.basename(csv_file_path)
        file_id = self._upload_to_s3(
            table_name, dataset.get_id(), file_name, csv_file_path
        )

        # create an import job
        if df is None:
            df = pd.read_csv(csv_file_path)
        header_map = [
            {"header_name": col_name, "position": i}
            for i, col_name in enumerate(df.columns)
        ]
        file_list_entry = {
            "file_id": file_id,
            "file_name": file_name,
            "url": None,
            "delimiter": ",",
            "header_map": header_map,
        }
        import_request = am.ImportCatalogJobRequest(
            table_name=table_name,
            dataset_id=dataset.id,
            file_list=[file_list_entry],
            import_identifier=import_identifier,
        )
        import_response = self.catalog_api.import_catalog_job(import_request)

        for _ in range(Constants.IMPORT_CATALOG_STATUS_CHECK_ATTEMPTS):
            job_details: ImportCatalogJobDetails = (
                self.get_catalog_table_import_job(
                    job_id=import_response.job_id
                )
            )

            if job_details.status == am.JobStatus.SUCCESS:
                return True
            elif job_details.status == am.JobStatus.FAILED:
                raise ServerError(
                    f"Add to catalog failed with "
                    f"error: {job_details.error}"
                )

            time.sleep(Constants.IMPORT_CATALOG_STATUS_CHECK_INTERVAL_S)

        return False

    @translate_api_exceptions
    def get_catalog_table_import_job(
        self,
        job_id: str,
    ) -> ImportCatalogJobDetails:
        """
        Get import catalog job details

        Parameters
        ----------
        job_id : str
            The identifier of the catalog import job

        Returns
        -------
        ImportCatalogJobDetails
            Returns the catalog job details
        """
        resp: am.GetImportJobDetailedResponse = (
            self.catalog_api.get_catalog_table_import_job(job_id=job_id)
        )

        return ImportCatalogJobDetails(
            job_id=job_id,
            status=resp.status,
            started_at=resp.started_at,
            completed_at=resp.completed_at,
            error=resp.failure_message if resp.failure_message else None,
        )

    def _upload_to_s3(
        self, table_name: str, dataset_id: str, file_name: str, file_path: str
    ):
        url_request = am.GetPreSignedUrlRequest(
            file_list=[file_name], table_name=table_name, dataset_id=dataset_id
        )
        url_response: ListPreSignedUrlResponse = (
            self.catalog_api.get_pre_signed_url(url_request)
        )

        pre_signed_url_resp: GetPreSignedUrlResponse = (
            url_response.presignedurls[0]
        )
        presigned_url = pre_signed_url_resp.url
        fields = pre_signed_url_resp.fields
        logger.debug(
            f"Uploading file {file_path} to s3, pre-signed url {presigned_url}"
        )

        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}
            upload_response = requests.post(
                url=presigned_url, data=fields, files=files
            )
            logger.debug(f"Upload response: {upload_response}")
        if upload_response.status_code not in range(200, 299):
            raise ServerError(
                f"Failed to upload to s3, Upload response: {upload_response}"
            )

        return pre_signed_url_resp.file_id

    @translate_api_exceptions
    def create_view(
        self,
        view_name: str,
        description: Optional[str],
        dataset: Dataset,
        left_table: CatalogTable,
        right_table: CatalogTable,
        join_condition: JoinCondition,
        inner_join: bool = False,
    ) -> str:  # -> Any | None:# -> Any | None:
        """Create a SQL view for visualization

        Args:
            view_name (str): Name of the view to create
            description (Optional[str]): Description text
            dataset (Dataset): Dataset object
            left_table (TableInfo): Left Table of the create view query
            right_table (TableInfo): Right Table of the create view query
            join_condition (JoinCondition): JoinCondition which includes the
            column from the left and the right table
            inner_join (bool): Use inner join for joining the tables
        Returns:
            str: view id
        """
        ds_id = dataset.get_id()

        left_table_cols: am.CatalogTableColumnsResponse = (
            self.catalog_api.get_columns_for_table(
                dataset_id=ds_id,
                table_name=left_table.table_name,
                pipeline_id=left_table.pipeline_id,
            )
        )  # type: ignore
        right_table_cols: am.CatalogTableColumnsResponse = (
            self.catalog_api.get_columns_for_table(
                dataset_id=ds_id,
                table_name=right_table.table_name,
                pipeline_id=right_table.pipeline_id,
            )
        )  # type: ignore
        left_table_info: am.TableInfo = left_table_cols.table_info  # type: ignore
        right_table_info: am.TableInfo = right_table_cols.table_info  # type: ignore
        if not self._check_col_exist(
            column_name=join_condition.left_column, table=left_table_info
        ):
            raise UserError(
                "Invalid Join Condition: Left Column Name is Invalid"
            )
        if not self._check_col_exist(
            column_name=join_condition.right_column, table=right_table_info
        ):
            raise UserError(
                "Invalid Join Condition: Right Column Name is Invalid"
            )
        query_tables = self._get_qms_table_info(
            left_table_info=left_table_info,
            right_table_info=right_table_info,
            join_condition=join_condition,
            left_table=left_table,
            right_table=right_table,
        )
        join_type = (
            am.ViewJoinType.INNER if inner_join else am.ViewJoinType.LEFT
        )

        cv_request: am.CreateViewRequest = am.CreateViewRequest(
            view_name=view_name,
            description=description,
            dataset_id=ds_id,
            table_info=[query_tables],
            join_type=join_type,
        )

        create_view_response: am.CreateViewResponse = (
            self.views_api.create_view(create_view_request=cv_request)
        )  # type: ignore

        return create_view_response.view_id  # type: ignore

    def _get_qms_table_info(
        self,
        left_table_info: am.TableInfo,
        right_table_info: am.TableInfo,
        join_condition: JoinCondition,
        left_table: CatalogTable,
        right_table: CatalogTable,
    ) -> List[am.QMSTableInfo]:
        left_table_alias = (
            left_table.alias_name
            if left_table.alias_name
            else str(left_table_info.name)
        )
        right_table_alias = (
            right_table.alias_name
            if right_table.alias_name
            else str(right_table_info.name)
        )
        if left_table_alias == right_table_alias:
            right_table_alias = right_table_alias + "_2"
        left_qms_tab_info = am.QMSTableInfo(
            abs_table_name=left_table_info.abs_name,
            alias_name=left_table_alias,  # type: ignore
            table_type=left_table.table_type.value,
            schema_name=left_table.schema_name,
            catalog_name=left_table.catalog_name,
            table_name=left_table_info.name,
            pipeline_id=left_table.pipeline_id,
        )
        right_qms_tab_info = am.QMSTableInfo(
            abs_table_name=right_table_info.abs_name,
            alias_name=right_table_alias,  # type: ignore
            table_type=right_table.table_type.value,
            table_name=right_table_info.name,
            schema_name=right_table.schema_name,
            catalog_name=right_table.catalog_name,
            pipeline_id=right_table.pipeline_id,
            join_conditions=[
                am.JoinCondition(
                    type=am.JoinOperandType.BASIC,
                    left=am.JoinOperand(
                        table=left_table_alias,
                        column=join_condition.left_column,
                    ),
                    right=am.JoinOperand(
                        table=right_table_alias,  # type: ignore
                        column=join_condition.right_column,
                    ),
                )
            ],
        )
        return [left_qms_tab_info, right_qms_tab_info]

    def _check_col_exist(self, column_name, table: am.TableInfo) -> bool:
        for col in table.columns:  # type: ignore
            col: am.ColumnInfo
            if col.name == column_name:
                return True

        return False

    def get_all_columns(
        self, dataset: Dataset, table: CatalogTable
    ) -> List[Column]:
        """Returns all columns for a table/view

        Args:
            dataset (Dataset): Dataset object
            table (TableInfo): Table Information

        Returns:
            List[Column]: List of columns of the table
        """
        if table.is_view:
            view: CatalogViewInfo = self.get_view_id(
                dataset=dataset, view_name=table.table_name
            )
            if not view.view_id:
                raise UserError(f"View {table.table_name} not found")
            view_details: am.ViewResponse = self.views_api.get_view(
                view.view_id
            )  # type: ignore
            ret_val = []
            for view_table in view_details.columns:  # type: ignore
                for col in view_table["column_list"]:
                    ret_val.append(Column(name=col["alias"], type=col["type"]))
            return ret_val
        else:
            table_cols: am.CatalogTableColumnsResponse = (
                self.catalog_api.get_columns_for_table(
                    dataset_id=dataset.get_id(),
                    table_name=table.table_name,
                    pipeline_id=table.pipeline_id,
                )
            )  # type: ignore
            columns: List[am.ColumnInfo] = table_cols.table_info.columns  # type: ignore

        return [
            Column(name=column.name, type=column.type)  # type: ignore
            for column in columns
        ]

    @translate_api_exceptions
    def create_table(
        self,
        dataset: Dataset,
        schema: Dict[str, str],
        table_name: str,
        indices: Optional[List[str]],
    ):
        sql_type_mappings: List[
            Dict[str, str]
        ] = CatalogTablesHelper.validate_and_create_sql_type_mapping(
            schema=schema
        )

        if indices:
            for index in indices:
                if index not in schema.keys():
                    raise UserError(
                        message=f"Invalid Index Column: '{index}'."
                        f"Column should be present in schema."
                    )

        tbl_abs_name: str = self._create_table(
            dataset_id=dataset.id,  # type: ignore
            table_name=table_name,
            col_list=sql_type_mappings,
            indices=indices,
        )
        return tbl_abs_name

    @translate_api_exceptions
    def get_view_id(
        self, dataset: Dataset, view_name: str
    ) -> Optional[CatalogViewInfo]:
        all_views: am.ListViewsResponse = self.views_api.list_views(
            dataset_id=dataset.get_id()
        )
        view_of_interest = [
            record
            for record in all_views.records  # type: ignore
            if record.view_name == view_name
        ]
        if view_of_interest:
            return CatalogViewInfo(view_id=view_of_interest[0].view_id)
        return None
