import torch.nn as nn
import torch
from tensorboardX import SummaryWriter
from os import path

from config import get_params, get_args_str
from preprocess import preprocess_cezo_fl

from cezo_fl.server import CeZO_Server
from cezo_fl.client import Client

from shared.model_helpers import get_current_datetime_str
from models.cnn_mnist import CNN_MNIST
from models.lenet import LeNet
from models.cnn_fashion import CNN_FMNIST
from models.lstm import CharLSTM
from tqdm import tqdm
from gradient_estimators.random_gradient_estimator import RandomGradientEstimator as RGE


def prepare_settings_underseed(args, device):
    torch.manual_seed(args.seed)
    if args.dataset == "mnist":
        model = CNN_MNIST().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(
            model.parameters(), lr=args.lr, weight_decay=1e-5, momentum=args.momentum
        )
        # scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.8)
    elif args.dataset == "cifar10":
        model = LeNet().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(
            model.parameters(), lr=args.lr, weight_decay=5e-4, momentum=args.momentum
        )
        # scheduler = torch.optim.lr_scheduler.MultiStepLR(
        #     optimizer, milestones=[200], gamma=0.1
        # )
    elif args.dataset == "fashion":
        model = CNN_FMNIST().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(
            model.parameters(), lr=args.lr, weight_decay=1e-5, momentum=args.momentum
        )
        # scheduler = torch.optim.lr_scheduler.MultiStepLR(
        #     optimizer, milestones=[200], gamma=0.1
        # )
    elif args.dataset == "shakespeare":
        model = CharLSTM().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4)
        # scheduler = torch.optim.lr_scheduler.MultiStepLR(
        #     optimizer, milestones=[200], gamma=0.1
        # )

    if args.grad_estimate_method in ["rge-central", "rge-forward"]:
        method = args.grad_estimate_method[4:]
        print(f"Using RGE {method}")
        grad_estimator = RGE(
            model,
            mu=args.mu,
            num_pert=args.num_pert,
            grad_estimate_method=method,
            device=device,
        )
    else:
        raise Exception(f"Grad estimate method {args.grad_estimate_method} not supported")
    return model, criterion, optimizer, grad_estimator


def setup_server_and_clients(args, device, train_loaders) -> CeZO_Server:
    clients = []

    for i in range(args.num_clients):
        client_model, client_criterion, client_optimizer, client_grad_estimator = (
            prepare_settings_underseed(args, device)
        )
        client_model.to(device)

        client = Client(
            client_model,
            train_loaders[i],
            client_grad_estimator,
            client_optimizer,
            client_criterion,
            device,
        )
        clients.append(client)

    server = CeZO_Server(
        clients,
        device,
        num_sample_clients=args.num_sample_clients,
        local_update_steps=args.local_update_steps,
    )

    # set server tools
    server_model, server_criterion, server_optimizer, server_grad_estimator = (
        prepare_settings_underseed(args, device)
    )
    server_model.to(device)
    server.set_server_model_and_criterion(
        server_model, server_criterion, server_optimizer, server_grad_estimator
    )
    return server


# def get_warmup_lr(
#     args, current_epoch: int, current_iter: int, iters_per_epoch: int
# ) -> float:
#     overall_iterations = args.warmup_epochs * iters_per_epoch + 1
#     current_iterations = current_epoch * iters_per_epoch + current_iter + 1
#     return args.lr * current_iterations / overall_iterations


if __name__ == "__main__":
    args = get_params().parse_args()
    device, train_loaders, test_loader = preprocess_cezo_fl(args)

    server = setup_server_and_clients(args, device, train_loaders)

    args_str = get_args_str(args) + "-" + server.server_model.model_name

    if args.log_to_tensorboard:
        tensorboard_sub_folder = args_str + "-" + get_current_datetime_str()
        writer = SummaryWriter(
            path.join(
                "tensorboards",
                "cezo_fl",
                args.dataset,
                args.log_to_tensorboard,
                tensorboard_sub_folder,
            )
        )

    eval_iterations = 20

    with tqdm(total=args.iterations, desc="Training:") as t, torch.no_grad():
        for ite in range(args.iterations):
            step_loss, step_accuracy = server.train_one_step(ite)
            t.set_postfix({"Loss": step_loss, "Accuracy": step_accuracy})
            t.update(1)

            if args.log_to_tensorboard:
                writer.add_scalar("Loss/train", step_loss, ite)
                writer.add_scalar("Accuracy/train", step_accuracy, ite)
            # eval
            if (ite + 1) % eval_iterations == 0:
                eval_loss, eval_accuracy = server.eval_model(test_loader)
                if args.log_to_tensorboard:
                    writer.add_scalar("Loss/test", eval_loss, ite)
                    writer.add_scalar("Accuracy/test", eval_accuracy, ite)
