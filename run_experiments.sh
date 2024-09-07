python decomfl_main.py --no-optim --dataset=multirc --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.00001 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-multirc-0005
python decomfl_main.py --no-optim --dataset=multirc --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.00001 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-multirc-0006
python decomfl_main.py --no-optim --dataset=rte --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=1500 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-rte-0005
python decomfl_main.py --no-optim --dataset=rte --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=1500 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-rte-0006
python decomfl_main.py --no-optim --dataset=boolq --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=1500 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-boolq-0005
python decomfl_main.py --no-optim --dataset=boolq --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=1500 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-boolq-0006
python decomfl_main.py --no-optim --dataset=wsc --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=3000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.000005 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-wsc-0005
python decomfl_main.py --no-optim --dataset=wsc --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=3000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.000005 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-wsc-0006
python decomfl_main.py --no-optim --dataset=wic --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.0000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-wic-0005
python decomfl_main.py --no-optim --dataset=wic --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.0000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-wic-0006
python decomfl_main.py --no-optim --dataset=cb --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=3000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.000005 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-cb-0005
python decomfl_main.py --no-optim --dataset=cb --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=3000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.000005 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-cb-0006
python decomfl_main.py --no-optim --dataset=sst2 --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=5 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-sst2-0005
python decomfl_main.py --no-optim --dataset=sst2 --eval-iterations=25 --large-model=opt-1.3b --model-dtype=float32 --seed=365 --iterations=2000 --train-batch-size=32 --test-batch-size=64 --no-iid --dirichlet-alpha=1 --num-clients=8 --num-sample-clients=2 --local-update-steps=1 --num-pert=10 --lr=0.000002 --momentum=0 --grad-estimate-method=rge-forward --mu=0.001 --log-to-tensorboard=FedDisco-sst2-0006