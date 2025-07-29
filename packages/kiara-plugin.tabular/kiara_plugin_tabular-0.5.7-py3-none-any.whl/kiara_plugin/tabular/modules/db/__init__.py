# -*- coding: utf-8 -*-
import atexit
import builtins
import csv
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Type, Union

from pydantic import Field
from sqlalchemy import insert, text

from kiara.exceptions import KiaraException, KiaraProcessingException
from kiara.models.filesystem import KiaraFile, KiaraFileBundle
from kiara.models.module import KiaraModuleConfig
from kiara.models.module.jobs import JobLog
from kiara.models.rendering import RenderScene, RenderValueResult
from kiara.models.values.value import SerializedData, Value, ValueMap
from kiara.modules import KiaraModule, ValueMapSchema
from kiara.modules.included_core_modules.create_from import (
    CreateFromModule,
    CreateFromModuleConfig,
)
from kiara.modules.included_core_modules.export_as import DataExportModule
from kiara.modules.included_core_modules.render_value import RenderValueModule
from kiara.modules.included_core_modules.serialization import DeserializeValueModule
from kiara.utils import find_free_id, log_message
from kiara.utils.output import DictTabularWrap
from kiara_plugin.tabular.defaults import (
    DEFAULT_TABLE_NAME,
    DEFAULT_TABULAR_DATA_CHUNK_SIZE,
)
from kiara_plugin.tabular.models.db import KiaraDatabase
from kiara_plugin.tabular.models.table import KiaraTable
from kiara_plugin.tabular.models.tables import KiaraTables
from kiara_plugin.tabular.utils import (
    create_sqlite_schema_data_from_arrow_table,
    create_sqlite_table_from_tabular_file,
    insert_db_table_from_file_bundle,
)


class CreateDatabaseModuleConfig(CreateFromModuleConfig):
    ignore_errors: bool = Field(
        description="Whether to ignore convert errors and omit the failed items.",
        default=False,
    )
    merge_into_single_table: bool = Field(
        description="Whether to merge all csv files into a single table.", default=False
    )
    include_source_metadata: Union[bool, None] = Field(
        description="Whether to include a table with metadata about the source files.",
        default=None,
    )
    include_source_file_content: bool = Field(
        description="When including source metadata, whether to also include the original raw (string) content.",
        default=False,
    )


class CreateDatabaseModule(CreateFromModule):
    _module_type_name = "create.database"
    _config_cls = CreateDatabaseModuleConfig

    def create__database__from__file(
        self, source_value: Value, optional: ValueMap
    ) -> Any:
        """Create a database from a file.

        Currently, only csv files are supported.
        """
        import csv as py_csv

        temp_f = tempfile.mkdtemp()
        db_path = os.path.join(temp_f, "db.sqlite")

        def cleanup():
            shutil.rmtree(db_path, ignore_errors=True)

        atexit.register(cleanup)

        file_item: KiaraFile = source_value.data
        if not file_item.file_name.endswith(".csv"):
            raise KiaraProcessingException(
                "Only csv files are supported (at the moment)."
            )

        table_name = file_item.file_name_without_extension

        table_name = table_name.replace("-", "_")
        table_name = table_name.replace(".", "_")

        has_header = optional.get_value_data("first_row_is_header")
        if has_header is None:
            try:
                has_header = True
                with open(source_value.data.path, "rt") as csvfile:
                    sniffer = py_csv.Sniffer()
                    has_header = sniffer.has_header(csvfile.read(2048))
                    csvfile.seek(0)
            except Exception as e:
                # TODO: add this to the procss log
                log_message(
                    "csv_sniffer.error",
                    file=source_value.data.path,
                    error=str(e),
                    details="assuming csv file has header",
                )

        try:
            create_sqlite_table_from_tabular_file(
                target_db_file=db_path,
                file_item=file_item,
                table_name=table_name,
                no_headers=not has_header,
            )
        except Exception as e:
            if self.get_config_value("ignore_errors") is True or True:
                log_message("ignore.import_file", file=file_item.path, reason=str(e))
            else:
                raise KiaraProcessingException(e)

        include_raw_content_in_file_info: bool = self.get_config_value(
            "include_source_metadata"
        )
        if include_raw_content_in_file_info:
            db = KiaraDatabase(db_file_path=db_path)
            db.create_if_not_exists()
            include_content: bool = self.get_config_value("include_source_file_content")
            db._unlock_db()
            included_files = {file_item.file_name: file_item}
            file_bundle = KiaraFileBundle.create_from_file_models(
                files=included_files, bundle_name=file_item.file_name
            )
            insert_db_table_from_file_bundle(
                database=db,
                file_bundle=file_bundle,
                table_name="source_files_metadata",
                include_content=include_content,
            )
            db._lock_db()

        return db_path

    def create__database__from__file_bundle(
        self, source_value: Value, job_log: JobLog
    ) -> Any:
        """Create a database from a file_bundle value.

        Currently, only csv files are supported, files in the source file_bundle that have different extensions will be ignored.

        Unless 'merge_into_single_table' is set to 'True' in the module configuration, each csv file will create one table
        in the resulting database. If this option is set, only a single table with all the values of all
        csv files will be created. For this to work, all csv files should follow the same schema.

        """

        merge_into_single_table = self.get_config_value("merge_into_single_table")
        if merge_into_single_table:
            raise NotImplementedError("Not supported (yet).")

        include_raw_content_in_file_info: Union[bool, None] = self.get_config_value(
            "include_source_metadata"
        )

        temp_f = tempfile.mkdtemp()
        db_path = os.path.join(temp_f, "db.sqlite")

        def cleanup():
            shutil.rmtree(db_path, ignore_errors=True)

        atexit.register(cleanup)

        db = KiaraDatabase(db_file_path=db_path)
        db.create_if_not_exists()

        # TODO: check whether/how to add indexes

        bundle: KiaraFileBundle = source_value.data

        table_names: List[str] = []
        included_files: Dict[str, bool] = {}
        errors: Dict[str, Union[None, str]] = {}
        for rel_path in sorted(bundle.included_files.keys()):
            if not rel_path.endswith(".csv"):
                job_log.add_log(
                    f"Ignoring file (not csv): {rel_path}", log_level=logging.INFO
                )
                included_files[rel_path] = False
                errors[rel_path] = "Not a csv file."
                continue

            file_item = bundle.included_files[rel_path]
            table_name = find_free_id(
                stem=file_item.file_name_without_extension, current_ids=table_names
            )
            try:
                table_names.append(table_name)
                create_sqlite_table_from_tabular_file(
                    target_db_file=db_path, file_item=file_item, table_name=table_name
                )
                included_files[rel_path] = True
            except Exception as e:
                included_files[rel_path] = False
                errors[rel_path] = KiaraException.get_root_details(e)

                if self.get_config_value("ignore_errors") is True or True:
                    log_message("ignore.import_file", file=rel_path, reason=str(e))
                    continue

                raise KiaraProcessingException(e)

        if include_raw_content_in_file_info in [None, True]:
            include_content: bool = self.get_config_value("include_source_file_content")
            db._unlock_db()

            insert_db_table_from_file_bundle(
                database=db,
                file_bundle=source_value.data,
                table_name="source_files_metadata",
                include_content=include_content,
                included_files=included_files,
                errors=errors,
            )
            db._lock_db()

        return db_path

    def create_optional_inputs(
        self, source_type: str, target_type
    ) -> Union[Mapping[str, Mapping[str, Any]], None]:
        inputs = {}
        if source_type == "file":
            inputs["first_row_is_header"] = {
                "type": "boolean",
                "optional": True,
                "doc": "Whether the first row of the file is a header row. If not provided, kiara will try to auto-determine.",
            }

        if target_type == "database" and source_type == "table":
            inputs["table_name"] = {
                "type": "string",
                "doc": "The name of the table in the new database.",
                "default": "imported_table",
            }

        return inputs

    def create__database__from__tables(
        self, source_value: Value, optional: ValueMap
    ) -> Any:
        """Create a database value from a list of tables."""

        from kiara_plugin.tabular.utils.tables import create_database_from_tables

        tables: KiaraTables = source_value.data
        db = create_database_from_tables(tables=tables)

        return db

    def create__database__from__table(
        self, source_value: Value, optional: ValueMap
    ) -> Any:
        """Create a database value from a table."""

        table_name = optional.get_value_data("table_name")
        if not table_name:
            table_name = DEFAULT_TABLE_NAME

        table: KiaraTable = source_value.data
        arrow_table = table.arrow_table

        column_map = None
        index_columns = None

        sqlite_schema = create_sqlite_schema_data_from_arrow_table(
            table=arrow_table, index_columns=index_columns, column_map=column_map
        )

        db = KiaraDatabase.create_in_temp_dir()
        db._unlock_db()
        engine = db.get_sqlalchemy_engine()

        _table = sqlite_schema.create_table(table_name=table_name, engine=engine)

        with engine.connect() as conn:
            for batch in arrow_table.to_batches(
                max_chunksize=DEFAULT_TABULAR_DATA_CHUNK_SIZE
            ):
                conn.execute(insert(_table), batch.to_pylist())
                conn.commit()

        db._lock_db()
        return db


class LoadDatabaseFromDiskModule(DeserializeValueModule):
    _module_type_name = "load.database"

    @classmethod
    def retrieve_supported_target_profiles(cls) -> Mapping[str, Type]:
        return {"python_object": KiaraDatabase}

    @classmethod
    def retrieve_serialized_value_type(cls) -> str:
        return "database"

    @classmethod
    def retrieve_supported_serialization_profile(cls) -> str:
        return "copy"

    def to__python_object(self, data: SerializedData, **config: Any):
        assert "db.sqlite" in data.get_keys() and len(list(data.get_keys())) == 1

        chunks = data.get_serialized_data("db.sqlite")

        # TODO: support multiple chunks
        assert chunks.get_number_of_chunks() == 1
        files = list(chunks.get_chunks(as_files=True, symlink_ok=True))
        assert len(files) == 1

        db_file = files[0]

        db = KiaraDatabase(db_file_path=db_file)
        return db


class QueryDatabaseConfig(KiaraModuleConfig):
    query: Union[str, None] = Field(description="The query.", default=None)


class QueryDatabaseModule(KiaraModule):
    """Execute a sql query against a (sqlite) database."""

    _config_cls = QueryDatabaseConfig
    _module_type_name = "query.database"

    def create_inputs_schema(
        self,
    ) -> ValueMapSchema:
        result: Dict[str, Dict[str, Any]] = {
            "database": {"type": "database", "doc": "The database to query."}
        }

        if not self.get_config_value("query"):
            result["query"] = {"type": "string", "doc": "The query to execute."}

        return result

    def create_outputs_schema(
        self,
    ) -> ValueMapSchema:
        return {"query_result": {"type": "table", "doc": "The query result."}}

    def process(self, inputs: ValueMap, outputs: ValueMap):
        import pyarrow as pa

        database: KiaraDatabase = inputs.get_value_data("database")
        query = self.get_config_value("query")
        if query is None:
            query = inputs.get_value_data("query")

        # TODO: make this memory efficent

        result_columns: Dict[str, List[Any]] = {}
        with database.get_sqlalchemy_engine().connect() as con:
            result = con.execute(text(query))
            for r in result:
                for k, v in dict(r).items():
                    result_columns.setdefault(k, []).append(v)

        table = pa.Table.from_pydict(result_columns)
        outputs.set_value("query_result", table)


class RenderDatabaseModuleBase(RenderValueModule):
    _module_type_name: str = None  # type: ignore

    def preprocess_database(
        self,
        value: Value,
        table_name: Union[str, None],
        input_number_of_rows: int,
        input_row_offset: int,
    ):
        database: KiaraDatabase = value.data
        table_names = database.table_names

        if not table_name:
            table_name = builtins.next(iter(table_names))

        if table_name not in table_names:
            raise Exception(
                f"Invalid table name: {table_name}. Available: {', '.join(table_names)}"
            )

        related_scenes_tables: Dict[str, Union[RenderScene, None]] = {
            t: RenderScene(
                title=t,
                description=f"Display the '{t}' table.",
                manifest_hash=self.manifest.manifest_hash,
                render_config={"table_name": t},
            )
            for t in database.table_names
        }

        query = f"""SELECT * FROM {table_name} LIMIT {input_number_of_rows} OFFSET {input_row_offset}"""
        result: Dict[str, List[Any]] = {}
        # TODO: this could be written much more efficient
        with database.get_sqlalchemy_engine().connect() as con:
            num_rows_result = con.execute(text(f"SELECT count(*) from {table_name}"))
            table_num_rows = num_rows_result.fetchone()[0]
            rs = con.execute(text(query))
            for r in rs:
                for k, v in dict(r).items():
                    result.setdefault(k, []).append(v)

        wrap = DictTabularWrap(data=result)

        row_offset = table_num_rows - input_number_of_rows
        related_scenes: Dict[str, Union[RenderScene, None]] = {}
        if row_offset > 0:
            if input_row_offset > 0:
                related_scenes["first"] = RenderScene.model_construct(
                    title="first",
                    description=f"Display the first {input_number_of_rows} rows of this table.",
                    manifest_hash=self.manifest.manifest_hash,
                    render_config={
                        "row_offset": 0,
                        "number_of_rows": input_number_of_rows,
                        "table_name": table_name,
                    },
                )

                p_offset = input_row_offset - input_number_of_rows
                p_offset = max(p_offset, 0)

                previous = {
                    "row_offset": p_offset,
                    "number_of_rows": input_number_of_rows,
                    "table_name": table_name,
                }
                related_scenes["previous"] = RenderScene.model_construct(
                    title="previous",
                    description=f"Display the previous {input_number_of_rows} rows of this table.",
                    manifest_hash=self.manifest.manifest_hash,
                    render_config=previous,
                )  # type: ignore
            else:
                related_scenes["first"] = None
                related_scenes["previous"] = None

            n_offset = input_row_offset + input_number_of_rows
            if n_offset < table_num_rows:
                next = {
                    "row_offset": n_offset,
                    "number_of_rows": input_number_of_rows,
                    "table_name": table_name,
                }
                related_scenes["next"] = RenderScene.model_construct(
                    title="next",
                    description=f"Display the next {input_number_of_rows} rows of this table.",
                    manifest_hash=self.manifest.manifest_hash,
                    render_config=next,
                )  # type: ignore
            else:
                related_scenes["next"] = None

            last_page = int(table_num_rows / input_number_of_rows)
            current_start = last_page * input_number_of_rows
            if (input_row_offset + input_number_of_rows) > table_num_rows:
                related_scenes["last"] = None
            else:
                related_scenes["last"] = RenderScene.model_construct(
                    title="last",
                    description="Display the final rows of this table.",
                    manifest_hash=self.manifest.manifest_hash,
                    render_config={
                        "row_offset": current_start,  # type: ignore
                        "number_of_rows": input_number_of_rows,  # type: ignore
                        "table_name": table_name,
                    },
                )
        related_scenes_tables[table_name].disabled = True  # type: ignore
        related_scenes_tables[table_name].related_scenes = related_scenes  # type: ignore
        return wrap, related_scenes_tables


class RenderDatabaseModule(RenderDatabaseModuleBase):
    _module_type_name = "render.database"

    def render__database__as__string(
        self, value: Value, render_config: Mapping[str, Any]
    ):
        input_number_of_rows = render_config.get("number_of_rows", 20)
        input_row_offset = render_config.get("row_offset", 0)

        table_name = render_config.get("table_name", None)

        wrap, data_related_scenes = self.preprocess_database(
            value=value,
            table_name=table_name,
            input_number_of_rows=input_number_of_rows,
            input_row_offset=input_row_offset,
        )
        pretty = wrap.as_string(max_row_height=1)

        return RenderValueResult(
            value_id=value.value_id,
            rendered=pretty,
            related_scenes=data_related_scenes,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
        )

    def render__database__as__terminal_renderable(
        self, value: Value, render_config: Mapping[str, Any]
    ):
        input_number_of_rows = render_config.get("number_of_rows", 20)
        input_row_offset = render_config.get("row_offset", 0)

        table_name = render_config.get("table_name", None)

        wrap, data_related_scenes = self.preprocess_database(
            value=value,
            table_name=table_name,
            input_number_of_rows=input_number_of_rows,
            input_row_offset=input_row_offset,
        )
        pretty = wrap.as_terminal_renderable(max_row_height=1)

        return RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            rendered=pretty,
            related_scenes=data_related_scenes,
            render_manifest=self.manifest.manifest_hash,
        )


class ExportNetworkDataModule(DataExportModule):
    """Export database values."""

    _module_type_name = "export.database"

    def export__database__as__sqlite_db(
        self, value: KiaraDatabase, base_path: str, name: str
    ):
        """Export network data as a sqlite database file."""

        target_path = os.path.abspath(os.path.join(base_path, f"{name}.sqlite"))
        shutil.copy2(value.db_file_path, target_path)

        return {"files": target_path}

    def export__database__as__sql_dump(
        self, value: KiaraDatabase, base_path: str, name: str
    ):
        """Export network data as a sql dump file."""

        import sqlite_utils

        db = sqlite_utils.Database(value.db_file_path)
        target_path = Path(os.path.join(base_path, f"{name}.sql"))
        with target_path.open("wt") as f:
            for line in db.conn.iterdump():
                f.write(line + "\n")

        return {"files": target_path.as_posix()}

    def export__database__as__csv_files(
        self, value: KiaraDatabase, base_path: str, name: str
    ):
        """Export network data as 2 csv files (one for edges, one for nodes."""

        import sqlite3

        files = []

        for table_name in value.table_names:
            target_path = os.path.join(base_path, f"{name}__{table_name}.csv")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # copied from: https://stackoverflow.com/questions/2952366/dump-csv-from-sqlalchemy
            con = sqlite3.connect(value.db_file_path)
            outfile = open(target_path, "wt")
            outcsv = csv.writer(outfile)

            cursor = con.execute(f"select * from {table_name}")
            # dump column titles (optional)
            outcsv.writerow(x[0] for x in cursor.description)
            # dump rows
            outcsv.writerows(cursor.fetchall())

            outfile.close()
            files.append(target_path)

        return {"files": files}
