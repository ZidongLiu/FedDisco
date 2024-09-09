import torch.nn as nn
import torch
from tensorboardX import SummaryWriter
from os import path
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import get_params, get_args_str
from preprocess import preprocess
from cezo_fl.server import CeZO_Server
from cezo_fl.client import ResetClient
from cezo_fl.fl_helpers import get_client_name
from shared.model_helpers import get_current_datetime_str
from shared.language_utils import get_lm_loss, LM_TEMPLATE_MAP, SUPPORTED_LLM
from tqdm import tqdm
from gradient_estimators.random_gradient_estimator import RandomGradientEstimator as RGE
from shared import quantized_layer


def prepare_settings_underseed(args, device):
    torch_dtype = {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }[args.model_dtype]
    torch.manual_seed(args.seed)
    if args.dataset in LM_TEMPLATE_MAP.keys():
        large_model = args.large_model
        model_name = SUPPORTED_LLM[large_model]
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_dtype).to(device)
        # Quantize the LLM
        quantized_layer.modify_opt125m(model)
        model.model_name = large_model
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, padding_side="left", truncate_side="left"
        )
        template = LM_TEMPLATE_MAP[args.dataset]()
        verbalizer_id_map = template.get_verbalizer_id(tokenizer)
        criterion = get_lm_loss("last_token", verbalizer_id_map)
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=0, weight_decay=5e-4)
        accuracy_func = get_lm_loss("accuracy", verbalizer_id_map)
    else:
        raise Exception(f"Dataset {args.dataset} is not supported")

    if args.grad_estimate_method in ["rge-central", "rge-forward"]:
        method = args.grad_estimate_method[4:]
        print(f"Using RGE {method}")
        grad_estimator = RGE(
            model,
            mu=args.mu,
            num_pert=args.num_pert,
            grad_estimate_method=method,
            device=device,
            torch_dtype=torch_dtype,
        )
    else:
        raise Exception(f"Grad estimate method {args.grad_estimate_method} not supported")
    return model, criterion, optimizer, grad_estimator, accuracy_func


def setup_server_and_clients(
    args, device_map: dict[str, torch.device], train_loaders
) -> CeZO_Server:
    clients = []

    for i in range(args.num_clients):
        client_name = get_client_name(i)
        client_device = device_map[client_name]
        (
            client_model,
            client_criterion,
            client_optimizer,
            client_grad_estimator,
            client_accuracy_func,
        ) = prepare_settings_underseed(args, client_device)
        client_model.to(client_device)

        client = ResetClient(
            client_model,
            train_loaders[i],
            client_grad_estimator,
            client_optimizer,
            client_criterion,
            client_accuracy_func,
            client_device,
        )
        clients.append(client)

    server_device = device_map["server"]
    server = CeZO_Server(
        clients,
        server_device,
        num_sample_clients=args.num_sample_clients,
        local_update_steps=args.local_update_steps,
    )

    # set server tools
    (
        server_model,
        server_criterion,
        server_optimizer,
        server_grad_estimator,
        server_accuracy_func,
    ) = prepare_settings_underseed(args, server_device)
    server_model.to(server_device)
    server.set_server_model_and_criterion(
        server_model,
        server_criterion,
        server_accuracy_func,
        server_optimizer,
        server_grad_estimator,
    )
    return server


# get_warmup_lr is not used for now.
def get_warmup_lr(args, current_epoch: int, current_iter: int, iters_per_epoch: int) -> float:
    overall_iterations = args.warmup_epochs * iters_per_epoch + 1
    current_iterations = current_epoch * iters_per_epoch + current_iter + 1
    return args.lr * current_iterations / overall_iterations


def get_size_of_model(model):
    return sum(p.numel() * p.element_size() for p in model.parameters())


if __name__ == "__main__":
    args = get_params().parse_args()
    print(args)
    device_map, train_loaders, test_loader = preprocess(args)

    server = setup_server_and_clients(args, device_map, train_loaders)

    if args.log_to_tensorboard:
        tensorboard_sub_folder = "-".join(
            [get_args_str(args), server.server_model.model_name, get_current_datetime_str()]
        )
        writer = SummaryWriter(
            path.join(
                "tensorboards",
                "zo-compression",
                args.dataset,
                args.log_to_tensorboard,
                tensorboard_sub_folder,
            )
        )

    with tqdm(total=args.iterations, desc="Training:") as t, torch.no_grad():
        for ite in range(args.iterations):
            step_loss, step_accuracy = server.train_one_step(ite)
            t.set_postfix({"Loss": step_loss, "Accuracy": step_accuracy})
            t.update(1)
            if args.adjust_perturb:
                if ite == 500:
                    server.set_learning_rate(args.lr * 0.8)
                    server.set_perturbation(args.num_pert * 2)
                elif ite == 1000:
                    server.set_learning_rate(args.lr * 0.5)
                    server.set_perturbation(args.num_pert * 4)
                elif ite == 2000:
                    server.set_learning_rate(args.lr * 0.3)
                    server.set_perturbation(args.num_pert * 8)

            if args.log_to_tensorboard:
                writer.add_scalar("Loss/train", step_loss, ite)
                writer.add_scalar("Accuracy/train", step_accuracy, ite)
            # eval
            if args.eval_iterations != 0 and (ite + 1) % args.eval_iterations == 0:
                eval_loss, eval_accuracy = server.eval_model(test_loader)
                if args.log_to_tensorboard:
                    writer.add_scalar("Loss/test", eval_loss, ite)
                    writer.add_scalar("Accuracy/test", eval_accuracy, ite)