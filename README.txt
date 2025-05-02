In the /experiment folder, there are several shell scripts with name exp{number}_{experiment name}.sh

These are the scripts corresponding to the experiments listed in Report.pdf.


Run under the main directory:

chmod +x experiment/exp{number}_{experiment name}.sh
experiment/exp{number}_{experiment name}.sh


Detailed explanation of the code are marked in cpp files, python files, and shell scripts, as comments.


Basically,

1. four cardinality estimation functions are implemented. Source code can be found in /algorithms/cpp_files.

2. shell scripts in /experiments call python scripts to run experiments. Typically, it calls two python scripts. One to run the experiment and gather data. One to visualize data.
