import json
import re
from jsonschema import validate, ValidationError


class Validator:

    def __init__(self, config_path):

        with open(config_path, "r") as file:
            self.config = json.load(file)

        self.schema = self.build_schema()

    # ----------------------------------------------------
    # Build JSON Schema Dynamically
    # ----------------------------------------------------

    def build_schema(self):

        properties = {}
        required = []

        type_mapping = {
            "string": "string",
            "number": "number",
            "boolean": "boolean",
            "object": "object",
            "array": "array",
            "string[]": "array",
            "object[]": "array"
        }

        for field in self.config["fields"]:

            field_name = field["path"]
            field_type = field.get("type", "string")

            schema = {
                "type": type_mapping.get(field_type, "string")
            }

            # Array of strings
            if field_type == "string[]":

                schema["items"] = {
                    "type": "string"
                }

            # Array of objects
            elif field_type == "object[]":

                schema["items"] = {
                    "type": "object"
                }

            properties[field_name] = schema

            if field.get("required", False):
                required.append(field_name)

        if self.config.get("include_confidence", False):

            properties["overall_confidence"] = {
                "type": "number"
            }

        if self.config.get("include_provenance", False):

            properties["provenance"] = {
                "type": "array"
            }

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    # ----------------------------------------------------
    # JSON Schema Validation
    # ----------------------------------------------------

    def validate_schema(self, candidate):

        try:

            validate(
                instance=candidate,
                schema=self.schema
            )

            return True

        except ValidationError as e:

            print("\nSchema Validation Error")
            print("--------------------------------")

            print(e.message)

            return False

    # ----------------------------------------------------
    # Email Validation
    # ----------------------------------------------------

    def validate_email(self, candidate):

        email_fields = [

            key

            for key in candidate

            if "email" in key.lower()

        ]

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        for field in email_fields:

            value = candidate[field]

            if value is None:
                continue

            if isinstance(value, list):

                for email in value:

                    if not re.match(pattern, email):

                        print(f"Invalid email : {email}")

                        return False

            else:

                if not re.match(pattern, value):

                    print(f"Invalid email : {value}")

                    return False

        return True

    # ----------------------------------------------------
    # Phone Validation
    # ----------------------------------------------------

    def validate_phone(self, candidate):

        phone_fields = [

            key

            for key in candidate

            if "phone" in key.lower()

        ]

        pattern = r'^\+\d{10,15}$'

        for field in phone_fields:

            value = candidate[field]

            if value is None:
                continue

            if isinstance(value, list):

                for phone in value:

                    if not re.match(pattern, phone):

                        print(f"Invalid phone : {phone}")

                        return False

            else:

                if not re.match(pattern, value):

                    print(f"Invalid phone : {value}")

                    return False

        return True

    # ----------------------------------------------------
    # Validate Complete Candidate
    # ----------------------------------------------------

    def validate_candidate(self, candidate):

        print("\nValidating Candidate Profile...")
        print("--------------------------------")

        if not self.validate_schema(candidate):
            return False

        if not self.validate_email(candidate):
            return False

        if not self.validate_phone(candidate):
            return False

        print("Validation Successful")

        return True