import os
import json


class JsonifierService:
    def __init__(self, settings):
        self.settings = settings

        self.inputs_json_path = (
            self.settings.input_path / self.settings.inputs_json_filename
        )

        self.outputs_json_path = (
            self.settings.output_path
            / "outputs_json"
            / self.settings.outputs_json_filename
        )

    def start(self):
        input_json = json.loads(self.inputs_json_path.read_text())
        print(f"Json inputs content: {input_json}")

        to_transfer_input_labels = [
            input_label
            for input_label in input_json.keys()
            if "number_input_" in input_label
        ]
        output_json = {
            input_label: input_json[input_label]
            for input_label in to_transfer_input_labels
        }
        print(f"Json outputs content: {output_json}")

        self.outputs_json_path.write_text(json.dumps(output_json))
