#!/bin/bash

# Run script1.py with parameters
python ../visualization/plot_frequency.py ../dataset/cleaned/NCVoters_chunk NCVoters result/data0_data_frequency

# Check if script1.py ran successfully (optional, but recommended)
if [ $? -eq 0 ]; then
    
    # Run script2.py
    python ../visualization/plot_frequency.py ../dataset/cleaned/IPs_chunk IPs result/data0_data_frequency
else
    echo "plot_frequency.py failed."
    exit 1
fi