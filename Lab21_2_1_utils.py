import torch.nn as nn 

SD_PATH = "linear_reg_state.pth"

def get_sd_path():
    return SD_PATH

def create_model():
    return nn.Linear(1, 1)