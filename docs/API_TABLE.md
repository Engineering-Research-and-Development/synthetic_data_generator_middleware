# GENESIS Middleware API Documentation - Table Format

## API Endpoints Overview

| Endpoint | Method | Description | Request Body | Response Body | Status Codes |
|----------|--------|-------------|--------------|---------------|--------------|
| `/sdg_input/` | POST | Collect user input for synthetic data generation | `UserDataInput` | `GeneratorResponse` | 200, 400, 404, 503 |
| `/algorithms/` | POST | Create a new algorithm | `AlgorithmDataType` | `AlgorithmID` | 201, 400 |
| `/algorithms/` | GET | Get all algorithms | None | `AlgorithmList` | 200 |
| `/algorithms/{algorithm_id}` | GET | Get algorithm by ID | None | `AlgorithmDataTypeOut` | 200, 404 |
| `/algorithms/{algorithm_id}` | DELETE | Delete an algorithm | None | None | 204, 404 |
| `/functions/` | GET | Get all functions | None | `array[FunctionOut]` | 200 |
| `/functions/` | POST | Create a new function | `FunctionParameterDataTypeIn` | `FunctionOut` | 201 |
| `/functions/{function_id}` | GET | Get function by ID | None | `FunctionParameterDataTypeOut` | 200, 404 |
| `/functions/{function_id}` | DELETE | Delete a function | None | None | 204, 404 |
| `/trained_models/` | GET | Get all trained models | None | `TrainedModelVersionList` | 200 |
| `/trained_models/` | POST | Create a new trained model | `PostTrainedModelVersionDatatype` | `PostTrainedModelOut` | 201, 404 |
| `/trained_models/{model_id}` | GET | Get trained model by ID | None | `TrainedModelVersionDatatype` | 200, 404 |
| `/trained_models/{model_id}` | DELETE | Delete trained model | None | None | 204, 404 |

---

## Detailed Request/Response Schemas

### Algorithm Schemas

| Schema | Field | Type | Required | Description | Validation |
|--------|-------|------|----------|-------------|-----------|
| **Algorithm** | name | string | Yes | Algorithm name | `^[A-Za-z0-9._\-]+$` |
| | description | string | Yes | Algorithm description | `^[A-Za-z0-9._\- ]+$` |
| | default_loss_function | string | Yes | Default loss function | `^[A-Za-z0-9._\- ]+$` |
| **DataType** | type | string | Yes | Data type name | `^[A-Za-z0-9]+$` |
| | is_categorical | boolean | Yes | Whether categorical | - |
| **AlgorithmDataType** | algorithm | Algorithm | Yes | Algorithm object | - |
| | datatypes | array[DataType] | Yes | Allowed data types | - |
| **AlgorithmID** | id | number | Yes | Created algorithm ID | Positive integer |
| **AlgorithmOut** | id | number | Yes | Algorithm ID | Positive integer |
| | name | string | Yes | Algorithm name | - |
| | description | string | Yes | Algorithm description | - |
| | default_loss_function | string | Yes | Default loss function | - |
| **AlgorithmList** | algorithms | array[AlgorithmOut] | Yes | List of algorithms | - |
| **AlgorithmDataTypeOut** | algorithm | AlgorithmOut | Yes | Algorithm object | - |
| | datatypes | array[DataType] | Yes | Allowed data types | - |

---

### Function Schemas

| Schema | Field | Type | Required | Description | Validation |
|--------|-------|------|----------|-------------|-----------|
| **Function** | name | string | Yes | Function name | `^[A-Za-z0-9._-]+$` |
| | description | string | Yes | Function description | `^[A-Za-z0-9._\- +_*=()^:]+$` |
| | function_reference | string | Yes | Function reference | `^[A-Za-z0-9._\-]+$` |
| | is_generative | boolean | Yes | Whether generative | - |
| | priority | number | Yes | Function priority | Positive integer |
| **Parameter** | name | string | Yes | Parameter name | `^[a-z0-9._\-]+$` |
| | value | string | Yes | Parameter value | `^[A-Za-z0-9._\-,()]+$` |
| | parameter_type | string | Yes | Parameter type | `^[A-Za-z0-9._\-]+$` |
| **FunctionParameterDataTypeIn** | function | Function | Yes | Function object | - |
| | parameters | array[Parameter] | Yes | Function parameters | - |
| | datatypes | array[DataType] | Yes | Compatible data types | - |
| **FunctionId** | id | number | Yes | Function ID | Positive integer |
| **ParameterId** | id | number | Yes | Parameter ID | Positive integer |
| **DataTypeId** | id | number | Yes | Data type ID | Positive integer |
| **FunctionParameterDataTypeOut** | function | Function | Yes | Function object | - |
| | parameters | array[ParameterId] | Yes | Function parameters | - |
| | datatypes | array[DataTypeId] | Yes | Compatible data types | - |
| **FunctionOut** | function | FunctionId | Yes | Function object | - |

---

### Trained Model Schemas

| Schema | Field | Type | Required | Description | Validation |
|--------|-------|------|----------|-------------|-----------|
| **TrainedModel** | name | string | Yes | Model name | No leading/trailing spaces |
| | dataset_name | string | Yes | Dataset name | No leading/trailing spaces |
| | size | string | Yes | Dataset size | No leading/trailing spaces |
| | input_shape | string | Yes | Input shape | `\([0-9]+,(([0-9]+,?)+)?\)` |
| | algorithm | number | Yes | Algorithm ID | Positive integer |
| **ModelVersion** | version_name | string | Yes | Version name | - |
| | image_path | string | Yes | Model image path | - |
| | loss_function | string | Yes | Loss function | `^[A-Za-z0-9._\-]+$` |
| | train_loss | number | Yes | Training loss | Strict float |
| | val_loss | number | Yes | Validation loss | Strict float |
| | train_samples | number | Yes | Training samples | Strict integer |
| | val_samples | number | Yes | Validation samples | Strict integer |
| **TrainModelDatatype** | feature_name | string | Yes | Feature name | `^[A-Za-z0-9._\-]+$` |
| | feature_position | number | Yes | Feature position | Non-negative integer |
| | feature_size | string | Yes | Feature size | `^[A-Za-z0-9._\-(),]+$` |
| | feature_type | string | Yes | Feature type | `^[A-Za-z0-9._\-()]+$` |
| | type | string | Yes | Data type | - |
| | is_categorical | boolean | Yes | Whether categorical | - |
| **ModelVersionPublic** | id | number | Yes | Version ID | Positive integer |
| | version_name | string | Yes | Version name | - |
| | image_path | string | Yes | Model image path | - |
| | loss_function | string | Yes | Loss function | - |
| | train_loss | number | Yes | Training loss | - |
| | val_loss | number | Yes | Validation loss | - |
| | train_samples | number | Yes | Training samples | - |
| | val_samples | number | Yes | Validation samples | - |
| **TrainedModelPublic** | name | string | Yes | Model name | - |
| | dataset_name | string | Yes | Dataset name | - |
| | size | string | Yes | Dataset size | - |
| | input_shape | string | Yes | Input shape | - |
| | algorithm | number | Yes | Algorithm ID | - |
| **TrainModelOut** | id | number | Yes | Model ID | Positive integer |
| | name | string | Yes | Model name | - |
| | dataset_name | string | Yes | Dataset name | - |
| | size | string | Yes | Dataset size | - |
| | input_shape | string | Yes | Input shape | - |
| | algorithm | number | Yes | Algorithm ID | - |
| **TrainedModelVersion** | model | TrainModelOut | Yes | Model object | - |
| | versions | array[ModelVersionPublic] | Yes | Model versions | - |
| **TrainedModelVersionList** | models | array[TrainedModelVersion] | Yes | List of models | - |
| **MergedDataType** | feature_name | string | Yes | Feature name | - |
| | feature_position | number | Yes | Feature position | - |
| | feature_size | string | Yes | Feature size | - |
| | feature_type | string | Yes | Feature type | - |
| | type | string | Yes | Data type | - |
| | is_categorical | boolean | Yes | Whether categorical | - |
| **TrainedModelVersionDatatype** | model | TrainModelOut | Yes | Model object | - |
| | versions | array[ModelVersionPublic] | Yes | Model versions | - |
| | datatypes | array[MergedDataType] | Yes | Feature schema | - |
| **PostTrainedModelVersionDatatype** | model | TrainedModelPublic | Yes | Model object | - |
| | version | ModelVersion | Yes | Version object | - |
| | datatypes | array[MergedDataType] | Yes | Feature schema | - |
| **PostTrainedModelOut** | trained_model_id | number | Yes | Trained model ID | Positive integer |
| | model_version_id | number | Yes | Model version ID | Positive integer |

---

### Generator Input Schemas

| Schema | Field | Type | Required | Description | Validation |
|--------|-------|------|----------|-------------|-----------|
| **SupportedDatatypes** | - | enum | Yes | Data type enum | float32, int32, str, bool |
| **SupportedDatatypesCategory** | - | enum | Yes | Category enum | continuous, categorical, primary_key, group_index |
| **FeaturesCreated** | name | string | Yes | Feature name | `^[A-Za-z0-9._\-]+$` |
| | type | SupportedDatatypes | Yes | Data type | - |
| | category | SupportedDatatypesCategory | Yes | Data category | - |
| **FunctionIdRef** | id | number | Yes | Function ID | Positive integer |
| **ParametersInput** | id | number | Yes | Parameter ID | Positive integer |
| | value | string | Yes | Parameter value | - |
| **FunctionParametersIn** | function | FunctionIdRef | Yes | Function reference | - |
| | parameters | array[ParametersInput] | Yes | Parameters list | Min length 1 |
| **FunctionData** | feature_name | string | Yes | Feature name | `^[A-Za-z0-9._\-]+$` |
| | associated_functions | array[FunctionParametersIn] | Yes | Functions | - |
| **AiModel** | selected_model_id | number | Yes | Model ID | Positive integer |
| | new_model | boolean | No | Creating new model | Default: false |
| | new_model_name | string | No | New model name | `^[A-Za-z0-9._\-]+$` |
| | model_version | string | No | Model version | `^[A-Za-z0-9._\-]+$` |
| **UserFileInput** | input_type | string | Yes | Input type | Must be "user_file" |
| | user_file | array[object] | Yes | User data | Min length 1 |
| | ai_model | AiModel | Yes | AI model config | - |
| | functions | array[FunctionData] | No | Functions | - |
| **FeaturesCreatedInput** | input_type | string | Yes | Input type | Must be "features_created" |
| | features_created | array[FeaturesCreated] | Yes | Features | Min length 1 |
| | functions | array[FunctionData] | Yes | Functions | - |
| **UserFeatureInfo** | type | string | Yes | Feature type | - |
| **UserDataInput** | additional_rows | number | Yes | Rows to generate | Positive integer |
| | data | UserFileInput or FeaturesCreatedInput | Yes | Input data | Discriminated by input_type |
| | feature_types | object | No | Feature type mappings | - |
| **GeneratorResponse** | doc_id | string | Yes | Document ID | UUID string |

---

## HTTP Status Codes Reference

| Status Code | Description | Usage |
|-------------|-------------|-------|
| 200 OK | Success | GET requests successful |
| 201 Created | Resource created | POST requests successful |
| 204 No Content | Success, no content | DELETE requests successful |
| 400 Bad Request | Invalid input | Validation errors, missing required fields |
| 404 Not Found | Resource not found | Algorithm, function, or model not found |
| 503 Service Unavailable | Backend error | Generator service connection error |

---

## Path Parameters

| Parameter | Type | Location | Description | Example |
|-----------|------|----------|-------------|---------|
| algorithm_id | number | path | Algorithm identifier | 1 |
| function_id | number | path | Function identifier | 1 |
| model_id | number | path | Trained model identifier | 1 |

## Query Parameters

| Parameter | Type | Location | Description | Example |
|-----------|------|----------|-------------|---------|
| version_name | string | query | Specific version to delete (for DELETE /trained_models/{model_id}) | v1.0 |

---

## Validation Rules Summary

### String Patterns
- **Algorithm names**: `^[A-Za-z0-9._\-]+$`
- **Feature names**: `^[A-Za-z0-9._\-]+$`
- **Model names**: No leading/trailing spaces, `^[^ ](.*[^ ])?$`
- **Input shapes**: Tuple format, `\([0-9]+,(([0-9]+,?)+)?\)`
- **Function names**: `^[A-Za-z0-9._-]+$`
- **Parameter names**: `^[a-z0-9._\-]+$`

### Numeric Constraints
- All IDs must be positive integers
- Feature positions must be non-negative integers
- Training/validation losses must be strict floats
- Sample counts must be strict integers

### Enum Values
- **SupportedDatatypes**: float32, int32, str, bool
- **SupportedDatatypesCategory**: continuous, categorical, primary_key, group_index
- **SupportedDataset**: table, time_series
