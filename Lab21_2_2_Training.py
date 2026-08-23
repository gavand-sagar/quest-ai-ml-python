
import torch  # Main PyTorch library
import torch.nn as nn  # Neural network module (models, layers, loss functions)
import torch.optim as optim

from Lab21_2_1_utils import create_model,get_sd_path  # Optimizers (used to update weights)

model = create_model()

loss_fn = nn.MSELoss()

optimizer = optim.SGD(model.parameters(), lr=0.1)

totalIterations = 1000

# Input features (X) → 3 samples, 1 feature each
X = torch.tensor([[1.0],[2.0],[3.0]])

# Target values (y) → expected output
y = torch.tensor([[2.0], [4.0], [6.0]])

for epoch in range(totalIterations):
    y_pred = model(X)
    loss = loss_fn(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch == totalIterations - 1:
        print(f"Epoch {epoch}, Loss = {loss.item()}")


# saving just the state_dict


torch.save(model.state_dict(), get_sd_path())  
