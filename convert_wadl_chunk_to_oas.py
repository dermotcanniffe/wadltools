import json
import yaml
import os
import re
import argparse

def pascal_to_camel(s):
    return s[0].lower() + s[1:] if s else s

def sanitize_type(t, ns=""):
    if "Nullable" in t and "DateTime" in ns:
        return {"type": "string", "format": "date-time"}
    mapping = {
        "String": {"type": "string"},
        "Int32": {"type": "integer"},
        "Boolean": {"type": "boolean"},
        "DateTime": {"type": "string", "format": "date-time"},
        "Nullable`1": {"type": "string"},
        "List`1": {"type": "array"},
    }
    return mapping.get(t, {"type": "string"})

def convert_parameters(params):
    return [
        {
            "name": p["name"],
            "in": "path",
            "required": True,
            "schema": { "type": "string" }
        }
        for p in params.values()
    ]

def convert_members(members):
    props = {}
    for key, val in members.items():
        schema = sanitize_type(val["type"], val.get("namespace", ""))
        props[pascal_to_camel(key)] = schema  # Preserve member name style here if desired
    return {
        "type": "object",
        "properties": props
    }

def convert_wadl_to_oas(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        wadl = json.load(f)

    resource_name, resource = list(wadl.items())[0]
    methods = resource.get("methods", {})

    paths = {}
    schemas = {}

    for method_id, method in methods.items():
        path = "/" + method["path"]
        http_method = method["name"].lower()

        # Parameters
        parameters = []
        if "request" in method and "parameters" in method["request"]:
            parameters = convert_parameters(method["request"]["parameters"])

        # Request body
        request_body = None
        rep = method.get("request", {}).get("representation", {})
        if isinstance(rep, dict):
            for key, val in rep.items():
                if "members" in val:
                    schema_name = key  # ✅ Keep the original schema name
                    if schema_name not in schemas:
                        schemas[schema_name] = convert_members(val["members"])
                    request_body = {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": { "$ref": f"#/components/schemas/{schema_name}" }
                            }
                        }
                    }

        # Response
        response = method.get("response", {}).get("representation", {})
        response_schema = None
        if isinstance(response, list):
            for item in response:
                if "members" in item:
                    schema_name = item["type"]  # ✅ Keep the original schema name
                    if schema_name not in schemas:
                        schemas[schema_name] = convert_members(item["members"])
                    response_schema = {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": { "$ref": f"#/components/schemas/{schema_name}" }
                            }
                        }
                    }
        elif isinstance(response, dict) and "members" in response:
            schema_name = response.get("type", method_id + "Response")
            if schema_name not in schemas:
                schemas[schema_name] = convert_members(response["members"])
            response_schema = {
                "application/json": {
                    "schema": { "$ref": f"#/components/schemas/{schema_name}" }
                }
            }

        # Path entry
        paths.setdefault(path, {})[http_method] = {
            "operationId": method_id,
            "summary": method_id.replace("_", " "),
            "parameters": parameters,
        }

        if request_body:
            paths[path][http_method]["requestBody"] = request_body

        paths[path][http_method]["responses"] = {
            "200": {
                "description": "Successful response",
                "content": response_schema or {
                    "application/json": {
                        "schema": { "type": "object" }
                    }
                }
            }
        }

    # Output
    oas = {
        "openapi": "3.0.3",
        "info": {
            "title": resource_name,
            "version": "1.0.0"
        },
        "paths": paths,
        "components": {
            "schemas": schemas
        }
    }

    out_filename = os.path.splitext(os.path.basename(input_file))[0] + "_openapi.yaml"
    with open(out_filename, "w", encoding="utf-8") as f:
        yaml.dump(oas, f, sort_keys=False)

    print(f"✅ OpenAPI spec written to: {out_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert WADL-style JSON to OpenAPI 3 YAML.")
    parser.add_argument("input", help="Path to resource chunk JSON file")
    args = parser.parse_args()

    convert_wadl_to_oas(args.input)

