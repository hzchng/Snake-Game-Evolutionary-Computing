from torch import nn
from torch.nn import functional as F


class CNN(nn.Module):
    def __init__(self, n_input, n_output=3):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(n_input, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, n_output)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = x.view(-1, 64 * 8 * 8)
        x = self.relu(self.fc1(x))
        x = self.softmax(self.fc2(x))
        return x


class ForwardNet(nn.Module):
    def __init__(self, n_input=7, n_h=9, n_h2=15, n_output=3):
        super(ForwardNet, self).__init__()
        self.fc1 = nn.Linear(n_input, n_h)
        self.fc2 = nn.Linear(n_h, n_h2)
        self.fc3 = nn.Linear(n_h2, n_output)

    def forward(self, x):
        x = F.tanh(self.fc1(x))
        x = F.tanh(self.fc2(x))
        x = F.softmax(self.fc3(x))
        return x