# waylay-ml-adapter-sklearn

Provides the `waylay-ml-adapter-sklearn` module as 
[Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) for [scikit-learn](https://scikit-learn.org/stable/).

## Installation
```
pip install waylay-ml-adapter-sklearn
```


## Classes exported by `ml_adapter.sklearn`

The module `ml_adapter.sklearn` exports the following classes
    
### `V1SklearnPredictAdapter`
`ml_adapter.sklearn.V1SklearnPredictAdapter` extending `ml_adapter.numpy.adapter.V1NumpyModelAdapter`
> ModelAdapter for sklearn models with a `predict` method.


### `V1SklearnPredictProbaAdapter`
`ml_adapter.sklearn.V1SklearnPredictProbaAdapter` extending `ml_adapter.numpy.adapter.V1NumpyModelAdapter`
> ModelAdapter for sklearn models with a `predict_proba` method.



## See also

* [waylay-ml-adapter-numpy](https://pypi.org/project/waylay-ml-adapter-numpy/) the [numpy](https://numpy.org/) data adapter that this model adapter uses.
* [waylay-ml-adapter-torch](https://pypi.org/project/waylay-ml-adapter-torch/) _ML adapter_ for [pytorch](https://pytorch.org/) models.
* [waylay-ml-adapter-sdk](https://pypi.org/project/waylay-ml-adapter-sdk/) provides the `ml_tool` extension to the [waylay-sdk](https://pypi.org/project/waylay-sdk/)
* [waylay-ml-adapter-base](https://pypi.org/project/waylay-ml-adapter-base/) provides the basic _ML adapter_ infrastructure.
* [waylay-ml-adapter-api](https://pypi.org/project/waylay-ml-adapter-api/) defines the remote data interfaces.
