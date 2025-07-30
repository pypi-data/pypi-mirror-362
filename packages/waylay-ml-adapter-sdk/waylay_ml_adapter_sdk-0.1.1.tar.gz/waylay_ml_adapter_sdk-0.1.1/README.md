# waylay-ml-adapter-sdk

ML Model Adapter plugin for [waylay-sdk](https://pypi.org/project/waylay-sdk/).

## Installation

```
# installs the ml tool, and the required sdk modules:
pip install waylay-ml-adapter-sdk

# install the adapter module you need:
pip install waylay-ml-adapter-sklearn[dill]
```


## Classes exported by `ml_adapter.sdk`

The module `ml_adapter.sdk` exports the following classes
    
### `MLTool`
`ml_adapter.sdk.tool.MLTool`
> MLAdapter utility service for the waylay client.

Helps creating waylay webscripts and plugs that wrap a machine learning model.

Loaded as tool with name `ml_tool` in the python sdk.

#### Example
```python
# create and test a simple model
import numpy as np
test_data = [1,2,3]
expected_result = [2,4,6]
doubler = lambda x: x*2
assert np.array_equal(
    np.array(expected_result),
    doubler(np.array(test_data))
)

# wrap in an adapter, test remoting
from ml_adapter.numpy import V1NumpyModelAdapter
adapter=V1NumpyModelAdapter(model=doubler)
test_resp == await adapter.call({"instances": test_data.tolist()})
assert test_resp['predictions'] = expected_result.tolist()

# use the ml_tool to deploy and test a webscript
# configure logging to see what is happening
import logging
logging.basicConfig(level='INFO')
from waylay.sdk import WaylayClient
client = WaylayClient.from_profile('demo')

ref = await client.ml_tool.create_webscript(
    adapter, name='MyMLWebscript', draft=True
)
ref = await client.ml_tool.wait_until_ready(ref)
result = await client.ml_tool.test_webscript(ref, test_data)
if expected_result.to_list() == result:
    await client.ml_tool.publish(ref)
else:
    await client.ml_tool.remove(ref)
```




## See also

* [waylay-sdk](https://pypi.org/project/waylay-sdk/) the Waylay python SDK.
* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) _ML adapter_ for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-torch](https://pypi.org/project/waylay-ml-adapter-torch/) _ML adapter_ for [pytorch](https://pytorch.org/) models.
* [waylay-ml-adapter-base](https://pypi.org/project/waylay-ml-adapter-base/) provides the basic  _ML adapter_ infrastructure.
* [waylay-ml-adapter-api](https://pypi.org/project/waylay-ml-adapter-api/) defines the remote data interfaces.