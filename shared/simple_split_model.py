import torch
import torch.nn as nn


class View(nn.Module):

    def __init__(self, next_layer_shape):
        self.next_layer_shape = next_layer_shape
        super(View, self).__init__()

    def forward(self, x):
        return x.view(-1, self.next_layer_shape)


class SplitSimpleCNN(nn.Module):

    def __init__(self, learning_rate=1e-2, mu=1e-5, compress=None):
        super(SplitSimpleCNN, self).__init__()

        self.grad_history = []
        self.parameter_l2_history = []

        self.compress = compress
        self.learning_rate = learning_rate
        self.mu = mu

        self.criterion = nn.CrossEntropyLoss()
        self.model1 = nn.Sequential(
            nn.Conv2d(3, 6, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            View(16 * 5 * 5),
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(),
        )

        self.model2 = nn.Sequential(
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 10),
        )

        self.parameters_shape = [p.shape for p in self.parameters()]
        # self.model1_parameters_shapes = [p.shape for p in self.model1.parameters()]
        # self.model2_parameters_shapes = [p.shape for p in self.model2.parameters()]

    def forward(self, x):
        x = self.model1(x)
        x = self.model2(x)
        return x

    def train_forward(self, x):
        if self.compress is None:
            return self.forward(x)

        m1_out = self.model1(x)
        comparessed_m1_out = self.compress(m1_out)
        m2_out = self.model2(comparessed_m1_out)
        return m2_out

    def add_model_params_(self, add_ons: list[torch.tensor]):
        with torch.no_grad():
            for p, add_on in zip(self.parameters(), add_ons):
                p.add_(add_on)

    def get_grad(self, new_loss, original_loss):
        return (new_loss - original_loss) / self.mu

    def sample_update_perturbation(self):
        return [torch.randn(p_shape) for p_shape in self.parameters_shape]

    def single_train_step(self, train_input, label):
        # cur_parameters = [p.clone() for p in self.parameters()]
        # original loss
        self.zero_grad()
        original_pred = self.train_forward(train_input)
        loss1 = self.criterion(original_pred, label)
        # update model parameters
        perturbation = self.sample_update_perturbation()
        # perturbation_l2 = sum([torch.sum(perturb**2) for perturb in perturbation])**0.5
        parameter_l2 = sum([torch.sum(param**2) for param in self.parameters()])**0.5
        # print('parameters l2', )
        # print('perturbation_l2', perturbation_l2)
        self.add_model_params_([self.mu * perturb for perturb in perturbation])
        # print((cur_parameters[0] + self.mu * perturbation[0] - [p for p in self.parameters()][0]).abs().sum())
        # updated loss
        new_pred = self.train_forward(train_input)
        loss2 = self.criterion(new_pred, label)

        grad = self.get_grad(loss2, loss1)
        # print('grad', grad)
        # update_parameters, need to minus perturbation(since model is already changed), then move to new_direction
        # x_t+1 = x_t - learning_rate * grad * perturbation
        # x_t+0.5 = x_t + mu * perturbation
        # x_t+1 = x_t+0.5 - mu * perturbation - learning_rate * grad * perturbation
        # x_t+1 = x_t+0.5 - (mu + learning_rate * grad) * perturbation
        self.parameter_l2_history += [parameter_l2]
        self.grad_history += [grad]
        self.add_model_params_([-(self.mu + self.learning_rate * grad) * perturb for perturb in perturbation])

        return loss1.item()

    def sgd_train_step(self, train_input, label):
        self.zero_grad()
        pred = self.forward(train_input)
        loss = self.criterion(pred, label)
        loss.backward()
        with torch.no_grad():
            self.add_model_params_([-p.grad * self.learning_rate for p in self.parameters()])

        return loss.item()

    # def batch_train_step(self, batch_inputs, batch_labels):
    #     preds = self.forward(batch_inputs)
    #     loss = self.criterion(preds, batch_labels)
    #     return loss