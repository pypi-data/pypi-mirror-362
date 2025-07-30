# multipca

A Python package for Multi-way Principal Component Analysis (Multiway PCA) with confidence intervals.

## Citation

If you use this package in your research, please cite:

```bibtex
@article{ouyang2023multiway,
  title={On the Multiway Principal Component Analysis},
  author={Ouyang, Jialin and Yuan, Ming},
  journal={Annals of Statistics (to appear)},
  year={2023},
  url={https://arxiv.org/abs/2302.07216}
}
```

## Installation

Requires Python ≥ 3.9. We recommend using a virtual environment:

```bash
# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install package
pip install multipca
```

## Quick Start

The package includes an example Citibike dataset that demonstrates multiway PCA analysis of bike sharing patterns in NYC. Here's how to get started:

```python
import multipca
import matplotlib.pyplot as plt

# Load the example Citibike data (shape: 24 hours × 35 stations × 522 days)
array = multipca.load_citibike_example()

# MPCA with confidence intervals
results = multipca.mpca_CI(array, r=4)

# Plot the first component's daily pattern with confidence bands
multipca.CI_band_plot(results, rank=1, mode=1)
plt.show()

# If you only need components without confidence intervals
components = multipca.mpca(array, r=4)
```

For more examples including World Bank economic indicators analysis, check out `examples/citibike_worldbank.ipynb` in the [GitHub repository](https://github.com/j-bagel/multipca).

## Documentation

Full documentation is available in the [GitHub repository](https://github.com/j-bagel/multipca).

## Examples

Check out the [example notebook](examples/citibike_worldbank.ipynb) for:
- Detailed usage examples
- Plotting functions
- Real-world applications with Citibike and World Bank data

## Features

- Multiway PCA implementation
- Confidence intervals for components
- Visualization tools:
  - Component plots with confidence bands
  - Loading plots

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
