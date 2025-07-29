import os.path

from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.folders_latest import (
    Folders,
)
from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


class BConfigurations:
    default_string_empty = str()

    default_data_inspection = True

    # INPUT_ROOT_FOLDER = \
    #     Folders(
    #         absolute_path_string=default_string_empty)

    INPUT_FILE_SYSTEM_OBJECT = FileSystemObjects(
        absolute_path_string=default_string_empty
    )

    OUTPUT_ROOT_FOLDER = Folders(
        absolute_path_string=default_string_empty
    )

    APP_RUN_OUTPUT_FOLDER_NAME = (
        default_string_empty
    )

    APP_RUN_OUTPUT_FOLDER = Folders(
        absolute_path_string=default_string_empty
    )

    APP_RUN_TIME_AS_STRING = (
        default_string_empty
    )

    APP_RUN_OUTPUT_FOLDER_PREFIX = (
        default_string_empty
    )

    APP_RUN_OUTPUT_FOLDER_SUFFIX = (
        default_string_empty
    )

    ENABLE_CSV_FILE_INSPECTION = (
        default_data_inspection
    )

    ENABLE_MS_ACCESS_DATABASE_INSPECTION = (
        default_data_inspection
    )

    ENABLE_SQLITE_DATABASE_INSPECTION = (
        default_data_inspection
    )

    @staticmethod
    def set_up_app_run_output_folder_name() -> (
        None
    ):
        datetime_stamp = (
            now_time_as_string_for_files()
        )

        output_folder_name = (
            datetime_stamp
        )

        if (
            BConfigurations.APP_RUN_OUTPUT_FOLDER_PREFIX
        ):
            output_folder_name = (
                BConfigurations.APP_RUN_OUTPUT_FOLDER_PREFIX
                + "_"
                + output_folder_name
            )

        if (
            BConfigurations.APP_RUN_OUTPUT_FOLDER_SUFFIX
        ):
            output_folder_name = (
                output_folder_name
                + "_"
                + BConfigurations.APP_RUN_OUTPUT_FOLDER_SUFFIX
            )

        BConfigurations.APP_RUN_OUTPUT_FOLDER_NAME = (
            output_folder_name
        )

        BConfigurations.APP_RUN_TIME_AS_STRING = (
            datetime_stamp
        )

    @staticmethod
    def set_app_run_output_folder() -> (
        None
    ):
        BConfigurations.APP_RUN_OUTPUT_FOLDER = Folders(
            absolute_path_string=os.path.join(
                BConfigurations.OUTPUT_ROOT_FOLDER.absolute_path_string,
                BConfigurations.APP_RUN_OUTPUT_FOLDER_NAME,
            )
        )

    @staticmethod
    def persist_dataframe_to_access_if_enabled() -> (
        None
    ):
        BConfigurations.ENABLE_MS_ACCESS_DATABASE_INSPECTION = (
            False
        )

        # TODO: Needs to work for NT
        # if os.name == 'nt':
        #     export_all_csv_files_from_folder_to_access(
        #             csv_folder=output_folder,
        #             database_already_exists=False,
        #             new_database_name_if_not_exists=output_folder.base_name + '_register_')
