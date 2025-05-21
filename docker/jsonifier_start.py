import os


class JsonifierService:
    def __init__(self, settings):
        self.settings = settings

        # self.nb_dir_input_path = self.settings.input_path
        # self.nb_dir_output_path = self.settings.output_path
        #
        # self.nb_input_path = (
        #     self.nb_dir_input_path / self.settings.notebook_path
        # )
        self.json_output_path = self.settings.output_path / "jsonified_values.json"

    def start(self):
        json_dict = []


