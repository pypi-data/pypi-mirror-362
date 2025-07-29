import csv
import importlib
import os
import shutil
from os.path import isfile, join
from pathlib import Path

import pyodbc as odbc_library
from bclearer_core.nf.types.collection_types import (
    CollectionTypes,
)
from bclearer_core.nf.types.common_collection_types import (
    CommonCollectionTypes,
)
from bclearer_interop_services.excel_services.interop.excel_write import (
    save_table_in_excel,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access.csv_folder_to_database_loader import (
    load_database_with_table,
)
from pandas import DataFrame, concat

# TODO: make this database agnostic, use a generic database wrapper class


class NfRegistries:
    def __init__(self):
        self.dictionary_of_collections = (
            {}
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass

    def export_dataframes_to_new_database(
        self,
        short_name: str,
        output_folder_name: str,
        database_basename: str,
        add_xlsx_export=True,
    ):
        output_folder = Path(
            output_folder_name,
        )

        output_database_folder = (
            output_folder.joinpath(
                short_name,
                short_name
                + "_"
                + database_basename,
            )
        )

        output_csv_folder = output_database_folder.joinpath(
            "csvs",
        )

        if add_xlsx_export:
            self.__export_dataframes_as_csv_and_xlsx(
                output_csv_folder=output_csv_folder,
                output_database_folder=output_database_folder,
                short_name=short_name,
            )

        else:
            self.export_dataframes(
                short_name=short_name,
                output_folder_name=str(
                    output_csv_folder,
                )
                + os.sep,
            )

        module = importlib.import_module(
            name="bclearer_orchestration_services.resources.templates",
        )

        module_path_string = (
            module.__path__[0]
        )

        resource_full_file_name = (
            os.path.join(
                module_path_string,
                "empty.accdb",
            )
        )

        target_full_file_name = (
            os.path.join(
                output_database_folder,
                short_name
                + "_"
                + database_basename
                + ".accdb",
            )
        )

        shutil.copy(
            src=resource_full_file_name,
            dst=target_full_file_name,
        )

        db_connection_string = (
            "Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            + "Dbq="
            + target_full_file_name
            + ";"
        )

        db_connection = (
            odbc_library.connect(
                db_connection_string,
                autocommit=True,
            )
        )

        filenames = [
            f
            for f in os.listdir(
                output_csv_folder,
            )
            if isfile(
                join(
                    output_csv_folder,
                    f,
                ),
            )
        ]

        for filename in filenames:
            load_database_with_table(
                db_connection=db_connection,
                table_name=filename,
                csv_folder=Folders(
                    output_csv_folder,
                ),
            )

        db_connection.close()

    def __export_dataframes_as_csv_and_xlsx(
        self,
        output_csv_folder: Path,
        output_database_folder: Path,
        short_name: str,
    ):
        output_csv_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_xlsx_folder = output_database_folder.joinpath(
            "xlsxs",
        )

        output_xlsx_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        for (
            collection_type,
            dataframe,
        ) in (
            self.dictionary_of_collections.items()
        ):
            NfRegistries.__export_dataframe_as_csv_and_xlsx(
                collection_type=collection_type,
                short_name=short_name,
                output_csv_folder=output_csv_folder,
                dataframe=dataframe,
                output_xlsx_folder=output_xlsx_folder,
            )

    @staticmethod
    def __export_dataframe_as_csv_and_xlsx(
        collection_type: CollectionTypes,
        short_name: str,
        output_csv_folder: Path,
        dataframe: DataFrame,
        output_xlsx_folder: Path,
    ):
        if not isinstance(
            collection_type,
            CollectionTypes,
        ):
            raise TypeError

        collection_name = (
            collection_type.collection_name
        )

        if (
            len(collection_name)
            + len(short_name)
            > 59
        ):
            collection_name = (
                collection_name[
                    0 : 59
                    - len(short_name)
                ]
            )

        csv_filepath = (
            output_csv_folder.joinpath(
                short_name
                + "_"
                + str(collection_name)
                + ".csv",
            )
        )

        dataframe.to_csv(
            str(csv_filepath),
            sep=",",
            quotechar='"',
            index=False,
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
        )

        xlsx_filepath = (
            output_xlsx_folder.joinpath(
                short_name
                + "_"
                + str(collection_name)
                + ".xlsx",
            )
        )

        save_table_in_excel(
            table=dataframe,
            full_filename=str(
                xlsx_filepath,
            ),
            sheet_name=str(
                collection_type.collection_name,
            ),
        )

    def export_dataframes(
        self,
        short_name: str,
        output_folder_name: str,
    ):
        output_folder = Path(
            output_folder_name,
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        for (
            collection_type,
            dataframe,
        ) in (
            self.dictionary_of_collections.items()
        ):
            if not isinstance(
                collection_type,
                CollectionTypes,
            ):
                raise TypeError

            dataframe.to_csv(
                output_folder_name
                + short_name
                + "_"
                + str(
                    collection_type.collection_name,
                )
                + ".csv",
                sep=",",
                quotechar='"',
                index=False,
                quoting=csv.QUOTE_ALL,
            )

    def add_table(
        self,
        table: DataFrame,
        collection_type: CollectionTypes,
    ):
        self.dictionary_of_collections[
            collection_type
        ] = table

    def get_collection(
        self,
        collection_type: CollectionTypes,
        collection_factory,
    ):
        if (
            collection_type
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                collection_type
            ]

        collection = (
            collection_factory.create()
        )

        self.add_table(
            table=collection,
            collection_type=collection_type,
        )

        return collection

    def replace_collection(
        self,
        collection_type: CollectionTypes,
        collection: DataFrame,
    ):
        self.add_table(
            table=collection,
            collection_type=collection_type,
        )

    def create_or_update_summary_table(
        self,
    ):
        summary_dictionary = dict()

        for (
            collection_type,
            table,
        ) in (
            self.dictionary_of_collections.items()
        ):
            if not isinstance(
                collection_type,
                CollectionTypes,
            ):
                raise TypeError

            summary_dictionary = self.__add_counts_to_dictionary(
                summary_dictionary=summary_dictionary,
                collection_type=collection_type,
                table=table,
            )

        summary_table_columns = [
            "table_names",
            "column_count",
            "row_count",
        ]

        summary_table = DataFrame.from_dict(
            summary_dictionary,
            orient="index",
            columns=summary_table_columns,
        )

        self.dictionary_of_collections[
            CommonCollectionTypes.SUMMARY_TABLE
        ] = summary_table

    def update(
        self,
        collection_type: CollectionTypes,
        new_collection: DataFrame,
    ):
        if (
            collection_type
            not in self.dictionary_of_collections.keys()
        ):
            self.dictionary_of_collections[
                collection_type
            ] = new_collection

            return

        current_collection = self.dictionary_of_collections[
            collection_type
        ]

        merged_collections = concat(
            objs=[
                current_collection,
                new_collection,
            ],
            ignore_index=True,
            verify_integrity=True,
        )

        self.dictionary_of_collections[
            collection_type
        ] = merged_collections

    @staticmethod
    def __add_counts_to_dictionary(
        summary_dictionary: dict,
        collection_type: CollectionTypes,
        table: DataFrame,
    ) -> dict:
        summary_dictionary[
            collection_type
        ] = [
            collection_type.collection_name,
            table.shape[1],
            table.shape[0],
        ]

        return summary_dictionary
