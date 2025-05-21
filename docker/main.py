import json
import logging

import osparc_filecomms.tools as osfct
import pydantic as pyda
import pydantic_settings
import pathlib as pl

import jsonifier_start

logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)d] %(message)s")
logger = logging.getLogger(__name__)

INPUT_CONF_KEY = "settings"
CONF_SCHEMA_FILENAME = "settings_json_schema.json"
DEFAULT_SETTINGS_FILEPATH = "settings_default.json"


def main():
    """Main"""

    settings = JsonifierDynamicSettings()

    # Wait for and read the settings file
    logger.info(f"Waiting for settings file to appear at {settings.settings_file_path}")
    settings.read_settings_file()
    logger.info("Settings file was read")

    # Create and start the dakota service
    jsonifier_service = jsonifier_start.JsonifierService(settings)
    jsonifier_service.start()


class JsonifierDynamicSettings:
    def __init__(self):
        self._settings = self.JsonifierMainSettings()

        settings_schema = self._settings.model_json_schema()

        # Hide some settings from the user
        for field_name in [
            "INPUT_FOLDER",
            "OUTPUT_FOLDER",
            "INPUTS_JSON_FILENAME"
        ]:
            settings_schema["properties"].pop(field_name)

        self.settings_file_path = self._settings.input_path / "settings.json"
        if not self.settings_file_path.exists():
            self.settings_file_path = pl.Path(
                pl.Path(__file__).parent / DEFAULT_SETTINGS_FILEPATH
            )

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            self.read_settings_file()
            return getattr(self._settings, name)

    def read_settings_file(self):
        self._settings = self._settings.model_validate(
            osfct.load_json(self.settings_file_path)
        )

    class JsonifierMainSettings(pydantic_settings.BaseSettings):
        input_path: pyda.DirectoryPath = pyda.Field(alias="INPUT_FOLDER")
        output_path: pyda.DirectoryPath = pyda.Field(alias="OUTPUT_FOLDER")
        inputs_json_filename: pyda.types.Path = pyda.Field(
            default="inputs.json", strict=False, alias="INPUTS_JSON_FILENAME"
        )
        outputs_json_filename: str = pyda.Field(
            default="outputs.json", strict=False
        )
        output_values_json_filename: str = pyda.Field(
            default="values.json", strict=False
        )
        input_values_json_filename: str = pyda.Field(
            default="values.json", strict=False
        )


if __name__ == "__main__":
    main()
