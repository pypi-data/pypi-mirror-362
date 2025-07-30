import torch
from .trainer import SimpleNet  # Make sure trainer.py is in the same package/folder

class VSI:
    def __init__(self, model_path="model.pth", input_size=512, num_classes=2, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SimpleNet(input_size, num_classes).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def predict(self, input_vector):
        """
        input_vector: list or np array of floats with shape [input_size]
        returns: predicted class index (int)
        """
        if not isinstance(input_vector, torch.Tensor):
            input_tensor = torch.tensor(input_vector, dtype=torch.float32).unsqueeze(0)
        else:
            input_tensor = input_vector.unsqueeze(0)

        input_tensor = input_tensor.to(self.device)

        with torch.no_grad():
            output = self.model(input_tensor)
            predicted_class = torch.argmax(output, dim=1).item()
        return predicted_class
