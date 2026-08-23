
import torch
from Lab21_2_1_utils import create_model,get_sd_path

model = create_model()
model.load_state_dict(torch.load(get_sd_path(), weights_only=True))


while True:
    
    # # # Test with new input
    test_input = float(input("Give Test Number"))
    test = torch.tensor([[test_input]])
    # # Model should predict ~28.0
    prediction = model(test)
    print("\nTest Input: " + str(test_input))
    print("Predicted Output:", prediction.item())
    print("\n\n\n")