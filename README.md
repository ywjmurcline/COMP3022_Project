# COMP3022_Project
COMP3022 individual project on cardinality estimation.

This project aims to reproduce some of the classic cardinality estimation algorithms, and design experiments to evaluate their time consumption and memory comsumption.


## Basics

In the /experiment folder, there are several shell scripts with name exp{number}_{experiment name}.sh

These are the scripts corresponding to the experiments listed in Report.pdf.


Run under the main directory:

```
chmod +x experiment/exp{number}_{experiment name}.sh
experiment/exp{number}_{experiment name}.sh
```

Detailed explanation of the code are marked in cpp files, python files, and shell scripts, as comments.


Basically,

1. four cardinality estimation functions are implemented. Source code can be found in /algorithms/cpp_files.

2. shell scripts in /experiments call python scripts to run experiments. Typically, it calls two python scripts. One to run the experiment and gather data. One to visualize data.


## Code

All code can be found at https://github.com/ywjmurcline/COMP3022_Project.

```
git clone https://github.com/ywjmurcline/COMP3022_Project.git
cd COMP3022_Project
```

To run experiments, you need to download the datasets first. You can find the download instructions below.

After downloading and preparing all data, you can run experiments by running shell scripts in /experiment.

All algorithm implementations can be found in /algorithms/cpp_files.

Compiled executable can be found in /algorithms/executable.



## Data

The experiment used two datasets.

NCVoter can be found at https://dl.ncsbe.gov/index.html?prefix=data/.

IP combines two datasets, they can be found at https://www.kaggle.com/datasets/joebeachcapital/global-ip-dataset-by-location-2023 and https://www.kaggle.com/datasets/jsrojas/ip-network-traffic-flows-labeled-with-87-apps.

All data are processed before use.

For NCVoters, you can run

NCVoter_download.py  // if there's any error with this, use a VPN and run again
NCVoter_unzip.py
NCVoter_process.py
NCVoter_chunk.py

in the given order, to reproduce the required data.


For IPs, 

1. download zip from both kaggle sites, and unzip them
2. get all five csv files and put them under /dataset/download/IPs
3. run IP_process.py and IP_chunk.py


After that, all processed data can be found at /dataset/cleaned. And you are ready to run experiments.