import torch

print(torch.__version__)

print("CUDA Tersedia:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Nama GPU:", torch.cuda.get_device_name(0))