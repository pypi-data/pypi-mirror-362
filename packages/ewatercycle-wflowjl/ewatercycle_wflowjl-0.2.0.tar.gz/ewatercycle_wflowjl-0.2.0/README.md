# eWaterCycle plugin for the Wflow.jl hydrological model

Wflow.jl plugin for [eWatercycle](https://ewatercycle.readthedocs.io/).

The Wflow.jl documentation is available at https://deltares.github.io/Wflow.jl/ .

## Installation

Please first install ewatercycle, for more info see the [general ewatercycle documentation](https://ewatercycle.readthedocs.io/).

To install this package alongside your eWaterCycle installation, do:

```console
pip install ewatercycle-wflowjl
```

Then Wflow becomes available as one of the eWaterCycle models:

```python
import ewatercycle.models
ewatercycle.models.sources["WflowJl"]
```

## Usage

Usage of Wflow.jl forcing generation and model execution is shown in 
[docs/generate_era5_forcing.ipynb](https://github.com/eWaterCycle/ewatercycle-wflowjl/tree/main/docs/generate_era5_forcing.ipynb) and [docs/demo.ipynb](https://github.com/eWaterCycle/ewatercycle-wflow/tree/main/docs/demo.ipynb) respectively.

## License

`ewatercycle-wflowjl` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
