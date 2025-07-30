# cutflow_compare

## Overview
`cutflow_compare` is a Python package designed to compare cutflow histograms from ROOT files. It provides a straightforward command-line interface for users to analyze and visualize differences in cutflow data across different regions and files.

## Features
- Compare cutflow histograms from two or more ROOT files simultaneously.
- Custom labels for each file using the `--labels` argument.
- Generate a CSV report of the comparison results.
- Calculate relative errors and standard deviations across all files for each selection and region.
- Easy to use with command-line arguments for file input and region selection.

## Installation
You can install the package using pip:

```sh
pip install cutflow_compare
```

## Usage

After installation, you can use the command-line tool directly:

```sh
cutflow_compare --files histoOut-compared.root histoOut-reference.root -r region1 region2 region3 --labels Compared Reference
```

Or, if running from source:

```sh
python cutflow_compare.py --files histoOut-compared.root histoOut-reference.root -r region1 region2 region3 --labels Compared Reference
```

### Note: 
Make sure the same regions are present in all files with the same name.

### Arguments
- `--files`: List of input ROOT files to compare. Required.
- `--regions`: List of regions to compare within the cutflow histograms. Required.
- `--labels`: Custom labels for each file, used in the output CSV. Optional.
- `--separate-selections`: Optional flag to keep selections separate instead of merging them.
- `--relative-error`: Optional flag to include relative error calculations in the output.

### Output
The tool generates a CSV file named `cutflow_comparison_result.csv` containing the comparison results.  
If multiple files are compared, the CSV will include columns for each file and region, as well as calculated relative errors and standard deviations for each selection and region.  
For two files, the relative error column shows the usual comparison; for more files, the relative error is computed as the standard deviation divided by the mean across all files.

## Example
```bash
cutflow_compare --files histoOut-compared.root histoOut-reference.root histoOut-third.root -r region1 region2 region3 --labels Compared Reference Third --relative-error
```

This command compares the specified regions (`region1`, `region2`, `region3`) in the three provided ROOT files (`histoOut-compared.root`, `histoOut-reference.root`, `histoOut-third.root`). It outputs the results to `cutflow_comparison_result.csv`, including relative error and standard deviation calculations for each selection and region.

## Requirements

- Python 3.6+
- [ROOT](https://root.cern/) (must be installed separately, e.g., via conda: `conda install -c conda-forge root`)
- pandas (install via pip: `pip install pandas`)
- uncertainties (install via pip: `pip install uncertainties`)

Make sure all dependencies are installed before running the tool.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## Acknowledgments
This package utilizes the ROOT framework for data analysis and visualization.
