#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=2:00:00
#SBATCH --array=1-10
#SBATCH --mem=2G

# Load required modules
# module purge
# module load GCCcore/11.3.0
# module load Apptainer/1.2.3

# Shelling into the container, mounting directory and generating events
singularity exec --bind /home/unimelb.edu.au/smeighenberg/Projects:/mnt \
/home/unimelb.edu.au/smeighenberg/Projects/cdm_detector_example/containers/genie_test.sif \
gevgen -n 100 -p -12 -t 1000060120 -e 1,10 -f 'x*exp(-x)' -r 1337 --seed 1337 \
--cross-sections /mnt/cdm_detector_example/genie_data/genie_xsec/v3_02_00/NULL/G1810a0211a-k250-e1000/data/gxspl-FNALsmall.xml --tune G18_10a_02_11a \
--message-thresholds Messenger_laconic.xml -o /mnt/genie_output/gntp_1337_ghep.root

# Shelling into the container, mounting directory and converting event files
singularity exec --bind /home/unimelb.edu.au/smeighenberg/Projects:/mnt \
/home/unimelb.edu.au/smeighenberg/Projects/cdm_detector_example/containers/genie_test.sif \
gntpc -i /mnt/genie_output/gntp_1337_ghep.root -f rootracker -o /mnt/genie_output/gtrac_1337_nue.root