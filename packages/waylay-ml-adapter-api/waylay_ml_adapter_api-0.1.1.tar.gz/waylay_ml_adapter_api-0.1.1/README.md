# waylay-ml-adapter-api

Provides the `ml_adapter.api` module for the [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) solution.

This module is not meant to be used on its own.

To use an _ML Adapter_ in a Waylay _plugin_ or _webscript_, use the adapter relevant to your machine learning framework:
* [waylay-ml-adapter-numpy](https://pypi.org/project/waylay-ml-adapter-numpy/) for generic models that use [numpy](https://numpy.org/) data representation
* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-torch](https://pypi.org/project/waylay-ml-adapter-torch/) for [pytorch](https://pytorch.org/) models.

The [waylay-ml-adapter-base](https://pypi.org/project/waylay-ml-adapter-base/) module provides a basis to create adapters for other frameworks.

The [waylay-ml-adapter-sdk](https://pypi.org/project/waylay-ml-adapter-sdk/) module provides the `ml_tool` extension
to the [waylay-sdk](https://pypi.org/project/waylay-sdk/) SDK.
It helps to create and test adapters from e.g. a python notebook.


## Classes exported by `ml_adapter.api`

The module `ml_adapter.api` exports the following classes
    
### `v1`
> V1 Dataplane protocol for ML services.

See
 * [KServe V1](https://kserve.github.io/website/master/modelserving/data_plane/v1_protocol/)
 * [Tensorflow V1](https://www.tensorflow.org/tfx/serving/api_rest#predict_api)



### `v2`
> V2 Dataplane protocol for ML services.

See
 * [Open Inference Protocol](
https://github.com/kserve/open-inference-protocol/tree/main
   )



