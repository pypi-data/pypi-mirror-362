import json


def load_configuration(json_file_path):
    with open(json_file_path) as file:
        config = json.load(file)
        pretty_config = json.dumps(
            config,
            indent=4,
        )
        print(
            "loaded configuration:\n",
            pretty_config,
        )
    return config
