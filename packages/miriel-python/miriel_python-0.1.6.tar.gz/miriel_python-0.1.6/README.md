# Miriel Python Client

This is the official Python client library for interacting with the Miriel API.

## Installation

You can install the Miriel Python client using pip:

```bash
pip install .
```
in the directory into which you cloned this repo.

## Basic Usage

To use the Miriel Python client, you need to have an API key. You can get your API key by signing up for an account on the [Miriel website](https://miriel.ai).

Once you have your API key, you can use the client to interact with the API. Here is an example of how to use the client:

```python
from miriel import Miriel

# Initialize the client with your API key
miriel_client = Miriel(api_key="your_api_key")

#add data
miriel_client.learn("The Founders of Miriel are David Garcia, Josh Paulson, and Andrew Barkett")

#Query the documents
query_response = miriel_client.query("Who are the founders of Miriel?")
print(f"Query response: {query_response}")

```

## Calling search with an image

```python
    ...
    query_response = miriel_client.query("What does this image show?", input_images="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")
    print(f"Query response: {query_response}")
```

## Calling with a structured output

```python
    ...

    #define a schema for the structured output
    output_schema = {
        "founders" : ["string"],
        "number_of_founders": "integer"
    }
    query_response = miriel_client.query("Who are the founders of Miriel?", response_format=output_schema)
    print(f"Query response: {query_response}")
```
Only "integer", "float", "string", "boolean", "array" (list), and "object" (dict) are supported.  Default values not yet supported.

## Documentation
For more details on the API, see the [API Documentation](API.md).
