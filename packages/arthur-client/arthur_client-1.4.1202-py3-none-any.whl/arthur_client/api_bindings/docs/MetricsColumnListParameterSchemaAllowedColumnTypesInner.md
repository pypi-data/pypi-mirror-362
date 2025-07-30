# MetricsColumnListParameterSchemaAllowedColumnTypesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dtype** | [**DType**](DType.md) |  | 
**object** | [**Dict[str, MetricsColumnListParameterSchemaAllowedColumnTypesInner]**](MetricsColumnListParameterSchemaAllowedColumnTypesInner.md) |  | 
**items** | [**Items1**](Items1.md) |  | 

## Example

```python
from arthur_client.api_bindings.models.metrics_column_list_parameter_schema_allowed_column_types_inner import MetricsColumnListParameterSchemaAllowedColumnTypesInner

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsColumnListParameterSchemaAllowedColumnTypesInner from a JSON string
metrics_column_list_parameter_schema_allowed_column_types_inner_instance = MetricsColumnListParameterSchemaAllowedColumnTypesInner.from_json(json)
# print the JSON string representation of the object
print(MetricsColumnListParameterSchemaAllowedColumnTypesInner.to_json())

# convert the object into a dict
metrics_column_list_parameter_schema_allowed_column_types_inner_dict = metrics_column_list_parameter_schema_allowed_column_types_inner_instance.to_dict()
# create an instance of MetricsColumnListParameterSchemaAllowedColumnTypesInner from a dict
metrics_column_list_parameter_schema_allowed_column_types_inner_from_dict = MetricsColumnListParameterSchemaAllowedColumnTypesInner.from_dict(metrics_column_list_parameter_schema_allowed_column_types_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


