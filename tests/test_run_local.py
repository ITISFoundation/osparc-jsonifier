import pathlib as pl
import json


def test_files():
    tests_dir = pl.Path(__file__).parent
    validation_tmp_dir = tests_dir.parent / "validation-tmp"
    inputs_dir = validation_tmp_dir / "inputs"
    outputs_dir = validation_tmp_dir / "outputs"

    input_values_json = json.loads((inputs_dir / "values.json").read_text())
    input_inputs_json = json.loads((inputs_dir / "inputs.json").read_text())

    output_outputs_json = json.loads((outputs_dir / "outputs.json").read_text())
    output_values_json = json.loads((outputs_dir / "values.json").read_text())

    for key, value in input_values_json.items():
        assert key in output_outputs_json
        assert output_outputs_json[key] == value

    for key, value in input_inputs_json.items():
        if key != 'settings':
            assert key in output_values_json
            assert output_values_json[key] == value

def main():
    test_files()

if __name__ == '__main__':
    main()
