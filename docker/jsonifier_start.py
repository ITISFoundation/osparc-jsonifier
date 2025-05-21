import logging
import json

logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)d] %(message)s")
logger = logging.getLogger(__name__)


class JsonifierService:
    def __init__(self, settings):
        self.settings = settings

        self.inputs_json_path = (
            self.settings.input_path / self.settings.inputs_json_filename
        )
        self.outputs_json_path = (
            self.settings.output_path / self.settings.outputs_json_filename
        )

        self.input_values_json_path = (
            self.settings.input_path / self.settings.input_values_json_filename
        )

        self.json_output_path = (
            self.settings.output_path
            / self.settings.output_values_json_filename
        )

    def start(self):
        input_json = json.loads(self.inputs_json_path.read_text())
        logger.info(f"Json inputs content: {input_json}")

        to_transfer_input_labels = [
            input_label
            for input_label in input_json.keys()
            if "number_input_" in input_label
        ]
        output_json = {
            input_label: input_json[input_label]
            for input_label in to_transfer_input_labels
        }
        logger.info(f"Json values content as input: {output_json}")
        self.json_output_path.write_text(json.dumps(output_json))

        if self.input_values_json_path.exists():
            output_json_input = json.loads(self.input_values_json_path.read_text())
            logger.info(f"Json values inputs content as output: {output_json}")
            self.outputs_json_path.write_text(json.dumps(output_json_input))
        else:
            logger.info("User didn't provide json file for outputs, skipping")
