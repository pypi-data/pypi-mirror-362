# PyMatterSim

## Summary
Physics-driven data analyis of computer simulations for materials science, chemistry, physics, and beyond.

## Installation [in a virtual environment]
Preparation: You need a C++compiler and cmake, which can be obtained from [the source code installation section](#Install-from-source).
- `python3.10 -m venv .venv`
- `source .venv/bin/activate`
- `pip install PyMatterSim`
- version upgrade `pip install --upgrade pymattersim`
### Install from source
- You need a C++compiler that supports at least the `C++11` standard and cmake.

   Recommend using `conda` or `mamba` for installation.
   
   Linux: `conda install gxx cmake` or `mamba install gxx cmake`

   Mac OS.`conda install clang cmake` or `mamba install clang cmake`

   Windows: `conda install gxx cmake` or `mamba install gxx cmake` or Download visual studio installer from [here](https://visualstudio.microsoft.com/vs/older-downloads/) and install the C++ compiler.

   A package manager is also a good choice, for example:

   ubuntu: `sudo apt-get install g++ cmake`

   centos: `sudo yum install gcc-c++ cmake3`

   macos: `brew install gcc cmake`

   Now that you have all the build tools, pip will help you complete everything for compilation.

```bash
git clone https://gitee.com/yuanchaohu/pymattersim  --recursive # get submodule
cd  pymattersim
pip install .
```
### Confirm installation
Acceleration is enabled by default. You can determine whether to enable acceleration by importing the _acc module and checking the variables.
```python
from PyMatterSim import _acc
print(_acc.ENABLE_ACC) # should be True
```
We also provide an environment variable `DISABLE_ACC` to disable acceleration code. Note that setting it to **any non-zero** value will result in disabling acceleration code.
```bash
export DISABLE_ACC=1 # will disable acceleration
# If you want to reactivate acceleration, do this.
unset(DISABLE_ACC) # will reactivate acceleration
```

## Documentation
The [documentation](https://doc-pymattersim.readthedocs.io/en/latest/) is now available online.

## Requirements
- python 3.8-3.11 (recommend **3.10**)
- numpy==1.26.4
- pandas==2.1.4
- freud-analysis==3.0.0
- scipy==1.15.2
- sympy==1.12
- gsd (optional)
- mdtraj (optional)
- voro++ (optional, standalone binary)

## Usage
Please refer to the `/docs/` for documentation and examples.
Some examples are provided from the unittest modules (`tests/`)

## Types of computer simulations
1. LAMMPS
   1. atom type & molecular type such as patchy particle, rigid body, molecules et al.
   2. x, xs, xu type particle positions
   3. orthagonal / triclinic box
2. Hoomd-blue
   1. GSD for structure analysis (need `gsd==3.2.0`)
   2. GSD + DCD for dynamics analysis (need `gsd==3.2.0` and `mdtraj==1.9.9`)
3. VASP (to be added)
4. Any type of simulators as long as the input were formatted well, modifying the `reader` module to use the computational modules.


## Notes
[Voro++](https://math.lbl.gov/voro++/) is recommended to install separately for specific Voronoi analysis. Some of the analysis from the original voro++ is maintained from the [freud-analysis package](https://freud.readthedocs.io/en/stable/gettingstarted/installation.html) developed by the Glozter group.

## Citation
```
@article{hu2024pymattersimpythondataanalysis,
      title={PyMatterSim: a Python Data Analysis Library for Computer Simulations of Materials Science, Physics, Chemistry, and Beyond}, 
      author={Y. -C. Hu and J. Tian},
      year={2024},
      eprint={2411.17970},
      archivePrefix={arXiv},
      primaryClass={cond-mat.mtrl-sci},
      url={https://arxiv.org/abs/2411.17970}, 
}
```

## References
- Y.-C. Hu et al. [Origin of the boson peak in amorphous solids](https://doi.org/10.1038/s41567-022-01628-6). **Nature Physics**, 18(6), 669-677 (2022) 
- Y.-C. Hu et al. [Revealing the role of liquid preordering in crystallisation of supercooled liquids](https://doi.org/10.1038/s41467-022-32241-z). **Nature Communications**, 13(1), 4519 (2022)
- Y.-C. Hu et al. [Physical origin of glass formation from multicomponent systems](https://www.science.org/doi/10.1126/sciadv.abd2928). **Science Advances** 6 (50), eabd2928 (2020)
- Y.-C. Hu et al. [Configuration correlation governs slow dynamics of supercooled metallic liquids](https://doi.org/10.1073/pnas.1802300115). **Proceedings of the National Academy of Sciences U.S.A.**, 115(25), 6375-6380 (2018)
- Y.-C. Hu et al. [Five-fold symmetry as indicator of dynamic arrest in metallic glass-forming liquids](https://doi.org/10.1038/ncomms9310). **Nature Communications**, 6(1), 8310 (2015) 


## UnitTest
Please run the bash scripts available from `shell/` for unittests. As follows are test statistics:
| Test              | # Tests and Runtime | Status |
| :---------------- | :-------------------------  | :----- |
| test_dynamics     |  Ran 15 tests in 10.303s    | OK     |
| test_neighbors    |  Ran 11 tests in 91.711s    | OK     |
| test_reader       |  Ran 11 tests in 0.270s     | OK     |
| test_static       |  Ran 28 tests in 298.248s   | OK     |
| test_utils        |  Ran 30 tests in 4.997s     | OK     |
| test_writer       |  Ran 3 tests in 0.005s      | OK     |

The activation of the acceleration code is slightly different for unit-test, and you need to manually compile the dynamic link library and place it in the _acc module.

```bash
# compile the dynamic link library
mkdir build
cd build
cmake ..
make
cp PyMatterSim/_acc/acc.cpython-313-x86_64-linux-gnu.so ../PyMatterSim/_acc/ # The dynamic library name varies depending on your platform.
```