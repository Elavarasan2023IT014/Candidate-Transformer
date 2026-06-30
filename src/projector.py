import json


class Projector:

    def __init__(self, config_path):

        with open(config_path) as f:
            self.config = json.load(f)

    # ----------------------------------------

    def project(self, candidate):

        output = {}

        for field in self.config["fields"]:

            output_name = field["path"]

            source = field.get("from", output_name)

            value = self.resolve(candidate, source)

            if value is None:

                action = self.config.get(
                    "on_missing",
                    "null"
                )

                if action == "omit":
                    continue

                elif action == "error":
                    raise Exception(
                        f"Missing required field {source}"
                    )

                else:
                    output[output_name] = None
                    continue

            normalize = field.get("normalize")

            if normalize:

                value = self.normalize(
                    value,
                    normalize
                )

            output[output_name] = value

        if self.config["include_confidence"]:

            output["overall_confidence"] = candidate["overall_confidence"]

        if self.config["include_provenance"]:

            output["provenance"] = candidate["provenance"]

        return output

    # ----------------------------------------

    def resolve(self, data, path):

        if path.endswith("[0]"):

            key = path[:-3]

            return data.get(key, [None])[0]

        if path.endswith("[].name"):

            key = path[:-7]

            return [

                item["name"]

                for item in data.get(key, [])

            ]

        return data.get(path)

    # ----------------------------------------

    def normalize(self, value, rule):

        if rule == "canonical":

            return sorted(set(value))

        if rule == "E164":

            return value.replace(" ", "")

        return value

    # ----------------------------------------

    def save(self, output, path):

        with open(path, "w") as f:

            json.dump(
                output,
                f,
                indent=4
            )