import json
import logging

import osparc_filecomms.tools as osfct
import pydantic as pyda
import pydantic_settings

import papermill_start

logging.basicConfig(
    level=logging.INFO, format="[%(filename)s:%(lineno)d] %(message)s"
)
logger = logging.getLogger(__name__)

INPUT_CONF_KEY = "settings"
CONF_SCHEMA_FILENAME = "settings_json_schema.json"


def main():
    """Main"""

    settings = PapermillDynamicSettings()

    # Wait for and read the settings file
    logger.info(
        f"Waiting for settings file to appear at {settings.settings_file_path}"
    )
    settings.read_settings_file()
    logger.info("Settings file was read")

    # Create and start the dakota service
    papermill_service = papermill_start.PapermillService(settings)
    papermill_service.start()


class PapermillDynamicSettings:
    def __init__(self):
        self._settings = self.PapermillMainSettings()
        conf_json_schema_path = (
            self._settings.output_path / CONF_SCHEMA_FILENAME
        )

        settings_schema = self._settings.model_json_schema()

        # Hide some settings from the user
        for field_name in [
            "INPUT_FOLDER",
            "OUTPUT_FOLDER",
        ]:
            settings_schema["properties"].pop(field_name)

        conf_json_schema_path.write_text(json.dumps(settings_schema, indent=2))

        self.settings_file_path = self._settings.input_path / "settings.json"

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

    class PapermillMainSettings(pydantic_settings.BaseSettings):
        input_path: pyda.DirectoryPath = pyda.Field(alias="INPUT_FOLDER")
        output_path: pyda.DirectoryPath = pyda.Field(alias="OUTPUT_FOLDER")
        notebook_path: pyda.types.Path = pyda.Field(default="", strict=False)

if __name__ == "__main__":
    main()
