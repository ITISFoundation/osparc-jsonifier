import os

import papermill as pm


class PapermillService:
    def __init__(self, settings):
        self.settings = settings

        self.nb_dir_input_path = self.settings.input_path
        self.nb_dir_output_path = self.settings.output_path

        self.nb_input_path = (
            self.nb_dir_input_path / self.settings.notebook_path
        )
        self.nb_output_path = self.nb_dir_output_path / "test-output.ipynb"

    def start(self):
        os.environ["DY_SIDECAR_PATH_INPUTS"] = str(
            self.settings.input_path.resolve()
        )
        os.environ["DY_SIDECAR_PATH_OUTPUTS"] = str(
            self.settings.output_path.resolve()
        )
        pm.execute_notebook(
            self.nb_input_path,
            self.nb_output_path,
            progress_bar=False,
            kernel_name="python3",
            log_output=True,
        )
