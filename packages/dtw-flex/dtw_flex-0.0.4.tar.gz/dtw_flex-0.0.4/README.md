# dtw_flex

## Description
This package allows to match flexibel user defined data patterns in a data array. The algorithm is based on dynamic time warping (dtw) but contains considerable changes. In contrast to classical dtw, an offset and amplitude are dynamically calculated. Moreover, the user can specify weights and allowable repetitions for each data point. Note that this algorithm is greedy and does not guarantee an optimal solution. 

The algorithm is also implemented in cython for better performance. The package also implements a running window in order to analyse longer data arrays. 
Pattern initialisation and point tracking can be set through a visual interface

## Getting Started

### Installing

```python
pip install dtw_flex
```

### Usage

Please check the following examples:
* [basic example](https://github.com/aifm00/dtw_flex/blob/main/dtw_flex/examples/example_basic.ipynb)
* [ECG example](https://github.com/aifm00/dtw_flex/blob/main/dtw_flex/examples/example_ECG.ipynb)
* [example with running window](https://github.com/aifm00/dtw_flex/blob/main/dtw_flex/examples/example_roll.ipynb)

## License

This project is licensed under the GPLv3 License - see the LICENSE file for details

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

