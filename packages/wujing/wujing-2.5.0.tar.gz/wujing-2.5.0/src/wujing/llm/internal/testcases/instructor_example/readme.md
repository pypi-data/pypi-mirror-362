## instructor.Mode.JSON

```json
{
    "messages": [
        {
            "role": "system",
            "content": "\n        As a genius expert, your task is to understand the content and provide\n        the parsed objects in json that match the following json_schema:\n\n\n        {\n  \"properties\": {\n    \"name\": {\n      \"title\": \"Name\",\n      \"type\": \"string\"\n    },\n    \"age\": {\n      \"title\": \"Age\",\n      \"type\": \"integer\"\n    }\n  },\n  \"required\": [\n    \"name\",\n    \"age\"\n  ],\n  \"title\": \"UserDetail\",\n  \"type\": \"object\"\n}\n\n        Make sure to return an instance of the JSON, not the schema itself\n"
        },
        {
            "role": "user",
            "content": "Extract Jason is 25 years old"
        }
    ],
    "model": "deepseek-v3-250324",
    "response_format": {
        "type": "json_object"
    }
}
```

## instructor.Mode.TOOLS

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Extract Jason is 25 years old"
        }
    ],
    "model": "deepseek-v3-250324",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "UserDetail",
                "description": "Correctly extracted `UserDetail` with all the required parameters with correct types",
                "parameters": {
                    "properties": {
                        "name": {
                            "title": "Name",
                            "type": "string"
                        },
                        "age": {
                            "title": "Age",
                            "type": "integer"
                        }
                    },
                    "required": [
                        "age",
                        "name"
                    ],
                    "type": "object"
                }
            }
        }
    ],
    "tool_choice": {
        "type": "function",
        "function": {
            "name": "UserDetail"
        }
    }
}
```

## instructor.Mode.MD_JSON

```json
{
    "messages": [
        {
            "role": "system",
            "content": "\n        As a genius expert, your task is to understand the content and provide\n        the parsed objects in json that match the following json_schema:\n\n\n        {\n  \"properties\": {\n    \"name\": {\n      \"title\": \"Name\",\n      \"type\": \"string\"\n    },\n    \"age\": {\n      \"title\": \"Age\",\n      \"type\": \"integer\"\n    }\n  },\n  \"required\": [\n    \"name\",\n    \"age\"\n  ],\n  \"title\": \"UserDetail\",\n  \"type\": \"object\"\n}\n\n        Make sure to return an instance of the JSON, not the schema itself\n"
        },
        {
            "role": "user",
            "content": "Extract Jason is 25 years old\n\nReturn the correct JSON response within a ```json codeblock. not the JSON_SCHEMA"
        }
    ],
    "model": "deepseek-v3-250324"
}
```