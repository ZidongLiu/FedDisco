#!/bin/bash -l

#SBATCH --job-name=       # Name of your job
#SBATCH --time=0-24:00:00               # Time limit, format is Days-Hours:Minutes:Seconds

#SBATCH --ntasks=1                      # 1 task (default of 1 CPU per task)
#SBATCH --mem=8g                        # 32GB of RAM for the whole job
#SBATCH --gres=gpu:p4:1

#SBATCH --output=%x_%j.out	# Output file

#SBATCH --account=fl-het          # Slurm account
#SBATCH --partition=tier3             # Partition to run on
#SBATCH --cpus-per-task=2

module load python/3.10.12-gcc-11.2.0-ubv7zcio

python cezo_fl_main.py --dataset=shakespeare --iterations=1000 --eval-iterations=200 --num-clients=5 --num-sample-clients=3 --local-update-steps=1 --num-pert=5 --grad-estimate-method=rge-forward