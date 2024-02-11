#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --array=1-2
#SBATCH --mem=2G

# Load required modules
module purge
module load singularity/3.8.5

# Shelling into the container, mounting directory and generating events
singularity exec --bind /data/gpfs/projects/punim0011/smeighenberg:/mnt \
/data/gpfs/projects/punim0011/smeighenberg/containers/genie_test.sif \
gevgen -n 1000 -p 14 -t 1000080160 -e 0,10 -f 'x*exp(-x)' -r ${SLURM_ARRAY_TASK_ID} --seed ${SLURM_ARRAY_TASK_ID} \
--cross-sections /mnt/genie_data/genie_xsec/v3_02_00/NULL/G1810a0211a-k250-e1000/data/gxspl-FNALsmall.xml --tune G18_10a_02_11a \
--message-thresholds Messenger_laconic.xml -o /mnt/genie_output/gntp_${SLURM_ARRAY_TASK_ID}_ghep.root

# Shelling into the container, mounting directory and converting event files
singularity exec --bind /data/gpfs/projects/punim0011/smeighenberg:/mnt \
/data/gpfs/projects/punim0011/smeighenberg/containers/genie_test.sif \
gntpc -i /mnt/genie_output/gntp_${SLURM_ARRAY_TASK_ID}_ghep.root -f rootracker -o /mnt/genie_output/gtrac_${SLURM_ARRAY_TASK_ID}.root