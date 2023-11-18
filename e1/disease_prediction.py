import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch
from torch.utils.data import TensorDataset, random_split


class SampleModel(nn.Module):

    def __init__(self, in_features):
        super(SampleModel, self).__init__()
        self.linear1 = nn.Linear(in_features=in_features, out_features=20)
        self.linear2 = nn.Linear(in_features=20, out_features=1)
        self.activation1 = nn.ReLU()
        self.activation2 = nn.Sigmoid()

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation1(x)
        x = self.linear2(x)
        x = self.activation2(x)
        return x


if __name__ == '__main__':
    features = torch.rand((1000, 50))
    labels = (features.sum(dim=1) > 25).float()
    model = SampleModel(50)
    criterion = nn.BCELoss()

    learning_rate = 0.1
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    dataset = TensorDataset(features, labels)

    # split data
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    # data loader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32)

    for epoch in range(100):
        for batch_features, batch_labels in train_loader:
            y_pred = model(batch_features)
            y_pred = y_pred.squeeze(1)

            loss = criterion(y_pred, batch_labels)

            # Zero gradients
            optimizer.zero_grad()
            # Compute gradients
            loss.backward()
            # Update parameters
            optimizer.step()

    # compute acc on test set
    correct = 0
    total = 0

    model.eval()
    with torch.no_grad():
        for batch_features, batch_labels in test_loader:
            y_pred = model(batch_features)
            y_pred = y_pred.squeeze(1)
            y_pred_binary = (y_pred > 0.5).float()
            correct += (y_pred_binary == batch_labels).sum().item()
            total += batch_labels.size(0)

    accuracy = correct / total
    print(f'Accuracy: {accuracy * 100:.2f}%')







