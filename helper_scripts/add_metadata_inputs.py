import pathlib as pl
import sys

import yaml
import json

def main():
    template_path = pl.Path(sys.argv[1])
    new_metadata_path = pl.Path(sys.argv[2])
    template_content = yaml.safe_load(template_path.read_text())

    input_template = template_content["inputs"]["number_input_1"]
    for input_i in range(1, 21):
        input_string = f"number_input_{input_i}"
        if input_string in template_content["inputs"]:
            del template_content["inputs"][input_string]
        this_input = input_template.copy()
        this_input["label"] = input_string
        this_input["description"] = f"number input {input_i}"
        this_input["type"] = "ref_contentSchema"
        this_input["contentSchema"] = {'title': f"number input {input_i}",
            'type': "number"
        }
        template_content["inputs"][input_string] = this_input
    
    output_template = template_content["outputs"]["number_output_1"]
    for output_i in range(1, 21):
        output_string = f"number_output_{output_i}"
        if output_string in template_content["outputs"]:
            del template_content["outputs"][output_string]
        this_output = output_template.copy()
        this_output["label"] = output_string
        this_output["description"] = f"number output {output_i}"
        this_output["type"] = "ref_contentSchema"
        this_output["contentSchema"] = {'title': f"number output {output_i}",
            'type': "number"
        }
        template_content["outputs"][output_string] = this_output

    new_metadata_path.write_text(
        yaml.dump(json.loads(json.dumps(template_content)), default_flow_style=False, sort_keys=False)
    )


if __name__ == "__main__":
    main()
