docker build -t myimg:latest .
sudo singularity build img.sif docker-daemon://myimg:latest