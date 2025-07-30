# waylay-ml-adapter-numpy

This provides the `ml_adapter.numpy` module as [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) for models that use numpy as data representation.

This `waylay-ml-adapter-numpy` module provides marshalling for (custom) models that use [numpy](https://numpy.org/) as native data representation.

```
pip install waylay-ml-adapter-numpy
```

## Exported classes

This module exports the following classes:


## Classes exported by `ml_adapter.numpy`

The module `ml_adapter.numpy` exports the following classes
    
### `V1NumpyModelAdapter`
`ml_adapter.numpy.adapter.V1NumpyModelAdapter` extending `ml_adapter.base.adapter.ModelAdapterBase`
> Adapts a callable with numpy arrays as input and output.

Supports dill, joblib or selfserializing model assets.



### `V1NumpyMarshaller`
`ml_adapter.numpy.marshall.V1NumpyMarshaller` extending `ml_adapter.base.marshall.v1.base.V1ValueOrDictRequestMarshallerBase`, `ml_adapter.base.marshall.v1.base.V1ValueOrDictResponseMarshallerBase`, `ml_adapter.numpy.marshall.V1NumpyEncoding`
> Converts v1 payload from and to numpy arrays.


### `V1NumpyNoLoadAdapter`
`ml_adapter.numpy.adapter.V1NumpyNoLoadAdapter` extending `ml_adapter.numpy.adapter.V1NumpyModelAdapter`
> Adapts a callable with numpy arrays as input and output.

This adapter does not manage the model as a standard asset.
Relies on the `model` or `model_class` constructor arguments
to define the model.
When `model` is not provided, any `model_path` is passed as a constructor
argument to `model_class` if the signature allows it.


