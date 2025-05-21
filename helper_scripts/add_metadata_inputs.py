import pathlib as pl
import sys

import yaml


def main():
    template_path = pl.Path(sys.argv[1])
    new_metadata_path = pl.Path(sys.argv[2])
    template_content = yaml.safe_load(template_path.read_text())

    input_template = template_content["inputs"]["input_1"]
    for input_i in range(1, 21):
        input_string = f"input_{input_i}"
        if input_string in template_content["inputs"]:
            del template_content["inputs"][input_string]
        this_input = input_template.copy()
        this_input["label"] = input_string
        this_input["description"] = f"input {input_i}"
        this_input["fileToKeyMap"] = {
            f"{input_string}/{input_string}": input_string
        }
        template_content["inputs"][input_string] = this_input

    new_metadata_path.write_text(
        yaml.dump(template_content, default_flow_style=False, sort_keys=False)
    )


if __name__ == "__main__":
    main()
