import json
from jsonschema import validate, ValidationError
from datetime import datetime
import pandas as pd
import xmltodict
import traceback

def convert_file_to_json(input_file: str,
                         output_file: str,
                         id: str,
                         event_file: str = None,
                         pick_file: str = None,
                         error_log_file: str = None):
    """
    Auto-detect format (csv, quakeml, arcout) and convert to standard JSON response.

    Parameters:
        input_file (str): Main input file (for quakeml or arcout).
        output_file (str): Output JSON filename.
        id (str): Event ID to use in the JSON.
        event_file (str): (Optional) For CSV: Path to events CSV file.
        pick_file (str): (Optional) For CSV: Path to picks CSV file.
        error_log_file (str): Optional path to write traceback if an error occurs.
    """
    try:
        detected_format = None
        body = None

        # Case 1: CSV — both event_file and pick_file must be provided
        if event_file and pick_file:
            df_events = pd.read_csv(event_file)
            df_picks = pd.read_csv(pick_file)

            events_list = df_events.to_dict(orient="records")
            picks_list = df_picks.to_dict(orient="records")

            for pick in picks_list:
                for key in ["Amplitude", "Filter", "Quality", "Site", "Source"]:
                    if key in pick and not isinstance(pick[key], str):
                        pick[key] = json.dumps(pick[key])

            body = [events_list, picks_list]
            detected_format = "csv"

        # Case 2: Try XML parsing
        elif input_file:
            try:
                with open(input_file, "r") as f:
                    xml_str = f.read()
                body_dict = xmltodict.parse(xml_str)

                extracted_id = (
                    body_dict.get('q:quakeml', {})
                    .get('eventParameters', {})
                    .get('event', {})
                    .get('@ns0:eventid', 'unknown_id')
                )
                id = id or extracted_id
                body = body_dict
                detected_format = "quakeml"

            except Exception:
                # Fallback to arcout if XML parsing fails
                with open(input_file, "r") as f:
                    lines = f.readlines()
                body = [lines]
                detected_format = "arcout"

        else:
            raise ValueError("No input_file or CSV files provided.")

        # Build final response
        response = {
            "status": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body_meta": {
                "id": id,
                "format": detected_format
            },
            "body": body
        }

        with open(output_file, "w") as f:
            json.dump(response, f, indent=2)

        print(f"[✓] Format: {detected_format} — Saved output to {output_file}")

    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"[✗] Error encountered: {e}")
        if error_log_file:
            with open(error_log_file, "w") as f:
                f.write(error_msg)
            print(f"[!] Error logged to {error_log_file}")
        else:
            print("[!] No error_log_file specified; error not saved.")


def build_message(body, id_str, format_str):
    """
    Constructs the full JSON message given body content, ID, and format.
    """
    return {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body_meta": {"id": id_str, "format": format_str},
        "body": body
    }

'''
- Build a full message with metadata and body using `build_message`
- Build a full message with status, headers, body_meta and body using `convert_file_to_json`, with provided csv, arcout or quakeml files
- Extract the `body` section from a structured JSON file using `extract_body_from_file`
'''

PICK_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "Amplitude": {
            "type": ["object", "null"],
            "properties": {
                "Amplitude": {"type": "number"},
                "SNR": {"type": "number"}
            },
            "required": ["Amplitude", "SNR"]
        },
        "Filter": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "HighPass": {"type": "number"},
                    "Type": {"type": "string"}
                },
                "required": ["HighPass", "Type"]
            }
        },
        "Onset": {"type": ["string", "null"]},
        "Phase": {"type": "string"},
        "Picker": {"type": ["string", "null"]},
        "Polarity": {"type": "string"},
        "Quality": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Standard": {"type": "string"},
                    "Value": {"type": ["number", "integer"]}
                },
                "required": ["Standard", "Value"]
            }
        },
        "Site": {
            "type": "object",
            "properties": {
                "Channel": {"type": "string"},
                "Location": {"type": "string"},
                "Network": {"type": "string"},
                "Station": {"type": "string"}
            },
            "required": ["Channel", "Location", "Network", "Station"]
        },
        "Source": {
            "type": "object",
            "properties": {
                "AgencyID": {"type": "string"},
                "Author": {"type": "string"}
            },
            "required": ["AgencyID", "Author"]
        },
        "Time": {"type": "string", "format": "date-time"},
        "Type": {"type": "string"}
    },
    "required": [
        "Amplitude", "Filter", "Onset", "Phase", "Picker", "Polarity",
        "Quality", "Site", "Source", "Time", "Type"
    ]
}

# Output schema (includes wrapping structure)
PICK_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "RetrieveParameters": {
            "type": "object",
            "properties": {
                "evid": {"type": "string"},
                "pickFile": {"type": "string"},
                "pickDataStr": {
                    "type": "array",
                    "items": PICK_INPUT_SCHEMA
                }
            },
            "required": ["pickDataStr"]
        }
    },
    "required": ["RetrieveParameters"]
}

# --- HELPERS ---

def log_error(message):
    with open("wrap_data_errors.log", "a") as log_file:
        timestamp = datetime.utcnow().isoformat()
        log_file.write(f"[{timestamp}] {message}\n")

def validate_pick_data(pick_data, schema):
    """Validates pick data list against a specified schema."""
    if not isinstance(pick_data, list):
        raise ValueError("Input JSON must be a list of pick objects.")
    for idx, pick in enumerate(pick_data):
        try:
            validate(instance=pick, schema=schema)
        except ValidationError as e:
            raise ValueError(f"Pick at index {idx} is invalid: {e.message}")

def validate_output_structure(wrapped_data):
    """Validate the final output structure using output schema."""
    try:
        validate(instance=wrapped_data, schema=PICK_OUTPUT_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Output structure validation error: {e.message}")


# --- PRIMARY FUNCTIONS ---

def wrap_data(input_file_path, output_file_path, evid, module='associator'):
    """
    Load, validate, wrap, and export pick data for use in associator or pickfilter modules.

    This function reads a list of pick dictionaries from a JSON file, validates them against
    a schema, wraps the data into a module-specific JSON structure, validates the output, and
    writes it to a new file.

    Args:
        input_file_path (str): Path to the input JSON file containing pick data.
        output_file_path (str): Path to write the validated and wrapped output JSON.
        evid (str): Event ID used in the output structure (e.g., file name or evid key).
        module (str, optional): Mode to wrap the data. Must be either:
            - 'associator': wraps with an "evid" key.
            - 'pickfilter': wraps with a "pickFile" key.
            Defaults to 'associator'.

    Raises:
        ValueError: If the module is not 'associator' or 'pickfilter'.
        ValueError: If input data fails validation.
        Exception: For any other unexpected errors during processing.

    Side Effects:
        - Logs errors to a file named 'wrap_data_errors.log'.
        - Prints validation or error status to the console.

    Example:
        wrap_data("input.json", "output.json", "event_123", module="pickfilter")
        wrap_data("input.json", "output.json", "event_456", module="associator")
    """
    try:
        with open(input_file_path, 'r') as infile:
            pick_data = json.load(infile)

        # Validate input picks
        validate_pick_data(pick_data, PICK_INPUT_SCHEMA)

        # Wrap the data
        if module == 'associator':
            wrapped = {
                "RetrieveParameters": {
                    "evid": evid,
                    "pickDataStr": pick_data
                }
            }
        elif module == 'pickfilter':
            wrapped = {
                "RetrieveParameters": {
                    "pickFile": f"{evid}_picks.json",
                    "pickDataStr": pick_data
                }
            }
        else:
            raise ValueError("Invalid module. Use 'associator' or 'pickfilter'.")

        # Validate output
        validate_output_structure(wrapped)

        # Write to file
        with open(output_file_path, 'w') as outfile:
            json.dump(wrapped, outfile, indent=2)

        print(f"Data validated and written to '{output_file_path}' for module '{module}'.")

    except Exception as e:
        error_message = f"Error in wrap_data (module: {module}): {e}"
        print(error_message)
        log_error(error_message)


def extract_body_from_file(filepath):
    """
    Extracts and returns the 'body' field from a JSON file.

    This function reads a JSON file from the specified filepath, parses its contents,
    and returns the value associated with the top-level "body" key, if present.

    Args:
        filepath (str): Path to the JSON file to be read.

    Returns:
        Any: The value of the "body" field in the JSON file, which may be a dictionary,
        list, string, number, or None depending on the file contents. If the "body"
        key is not present, returns None.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contents are not valid JSON.
        Exception: For other unexpected I/O or parsing errors.

    Example:
        Given a file `example.json` with contents:
        {
            "body": {
                "message": "Hello, world!"
            },
            "status": "ok"
        }

        Calling `extract_body_from_file("example.json")` returns:
        {
            "message": "Hello, world!"
        }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("body", None)



'''
### Creation of full response format

Below shows how to build out the Response format for provided files. In all cases below, you provide an ID and an output file name (of type json). Also, provide the error log file, in case any errors occur. A file of the name you specified will be generated which reports the errors. If no errors exist, the output JSON file will be generated at the path where you run the python script. 

If you are converting from csv to json, you provide the `_events.csv` and `_picks.csv` that are generated from pinging the associator API, and set them to `event_file` and `pick_file`. Leave the input_file blank. For quakeML or arcout conversion to json, specify the input_file. 

```
from postprocessing_seismo_lib import convert_file_to_json

# For CSV
convert_file_to_json(
    input_file="",  # not used for CSV
    output_file="[Output file name].json",
    id="[Name of choice]",
    event_file="[xxxx]_gamma_events.csv",
    pick_file="[xxxx]_gamma_picks.csv",
    error_log_file="csv_error_log.txt"
)

# For QuakeML XML (this input file has no XML signifiers but was parsed successfully as XML here)
convert_file_to_json(
    input_file="[xxxx]_events_test",
    output_file="[xxxx]_quakeml.json",
    id="[Name of choice]",
    error_log_file="quakeml_error_log.txt"
)

#Conventional QuakeML XML here
convert_file_to_json(
    input_file="[xxxx]_events_test.xml",
    output_file="[xxxx]_quakeml.json",
    id="[Name of choice]",
    error_log_file="quakeml_error_log.txt"
)


# For ArcOut
convert_file_to_json(
    input_file="[xxxx]_api_stproc_9999.arcout",
    output_file="[Output file name].json",
    id="[Name of choice]",
    error_log_file="arcout_error_log.txt"
)
```

## Installation

You can install the library locally for development:

```bash
pip install -e .
'''