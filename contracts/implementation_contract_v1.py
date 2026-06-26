class ImplementationContractV1:

    SCHEMA = {

        "generated_files": {

            "type": list,

            "item": {

                "path": str,

                "content": str

            }

        }

    }

    REQUIRED_FIELDS = [

        "generated_files"

    ]

    FIELD_TYPES = {

        "generated_files": list

    }