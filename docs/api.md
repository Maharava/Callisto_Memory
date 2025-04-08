# API Documentation for Callisto

## Overview
This document provides an overview of the API exposed by the Callisto memory management system. It includes method signatures, descriptions, and usage examples for the interfaces that facilitate communication with the Jupiter master program.

## Interfaces

### Jupiter API

#### `send_memory_request(request: MemoryRequest) -> MemoryResponse`
- **Description**: Sends a memory-related request to the Jupiter master program.
- **Parameters**:
  - `request`: An instance of `MemoryRequest` containing the details of the memory operation.
- **Returns**: An instance of `MemoryResponse` with the result of the operation.
- **Example**:
  ```python
  response = jupiter_api.send_memory_request(memory_request)
  ```

#### `receive_memory_response() -> MemoryResponse`
- **Description**: Receives a memory-related response from the Jupiter master program.
- **Returns**: An instance of `MemoryResponse` containing the result of the last memory operation.
- **Example**:
  ```python
  response = jupiter_api.receive_memory_response()
  ```

### Query Engine

#### `process_query(query: str) -> QueryResult`
- **Description**: Processes a user query related to memory management.
- **Parameters**:
  - `query`: A string representing the user's query.
- **Returns**: An instance of `QueryResult` containing the results of the query.
- **Example**:
  ```python
  result = query_engine.process_query("Retrieve memories from last week")
  ```

#### `parse_query(query: str) -> ParsedQuery`
- **Description**: Parses the user query into a structured format for processing.
- **Parameters**:
  - `query`: A string representing the user's query.
- **Returns**: An instance of `ParsedQuery` containing the structured representation of the query.
- **Example**:
  ```python
  parsed_query = query_engine.parse_query("What did I do yesterday?")
  ```

## Error Handling
All API methods should handle exceptions gracefully and return appropriate error messages in the `MemoryResponse` or `QueryResult` objects.

## Conclusion
This API documentation serves as a guide for developers integrating with the Callisto memory management system. For further details on the data structures used, please refer to the `memory_types.py` module documentation.