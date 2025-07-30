import ast
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

class SimpleNet(nn.Module):
    def __init__(self, in_size, out_size):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_size, 2048),  # Adjusted to accept new input size
            nn.ReLU(),
            nn.Linear(2048, 4096),
            nn.ReLU(),
            nn.Linear(4096, out_size)
        )

    def forward(self, x):
        return self.layers(x)

class Trainer:
    def __init__(self, dataset_file_path="test.txt"):
        self.dataset_path = dataset_file_path
        self.dataset = []

    def load_dataset(self):
        with open(self.dataset_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            parsed = ast.literal_eval(line.strip())
            self.dataset.append(parsed)

    def train(self, save_path="model.pth", epochs=10, lr=0.001, batch_size=16, device="cpu"):
        if not self.dataset:
            raise ValueError("Dataset is empty. Call load_dataset() first.")

        if device == "gpu":
            device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Split into X (features) and y (class labels)
        X = torch.tensor([sample[0] for sample in self.dataset], dtype=torch.float32)
        y = torch.tensor([sample[2] for sample in self.dataset], dtype=torch.long)

        input_size = X.shape[1]
        num_classes = len(set(y.tolist()))

        dataset = TensorDataset(X, y)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        model = SimpleNet(input_size, num_classes).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        best_loss = 1000000000000000000000000000000

        for epoch in range(epochs):
            total_loss = 0
            for batch_X, batch_y in dataloader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)

                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                if total_loss < best_loss:
                    torch.save(model.state_dict(), save_path)
                    best_loss = total_loss
                    print(f"New best loss: {total_loss}, saved model")

            print(f"Epoch {epoch + 1}/{epochs} - Loss: {total_loss:.4f} - Best loss: {best_loss:.4f}")

        # torch.save(model.state_dict(), save_path)
        # print(f"Model saved to {save_path}")
