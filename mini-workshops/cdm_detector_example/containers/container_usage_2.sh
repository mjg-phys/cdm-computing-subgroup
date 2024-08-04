# Shelling into the container, mounting directory and generating events
singularity exec --bind /home/unimelb.edu.au/smeighenberg/Projects:/mnt \
/home/unimelb.edu.au/smeighenberg/Projects/cdm_detector_example/containers/genie_test.sif \
python3 /mnt/cdm_detector_example/examples/executable.py