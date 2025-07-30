# EPINF-NeuFlow

The pytorch implementation of the paper "EPINF: Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations"

This repo is also a pypi package [NeuFlow](https://pypi.org/project/neuflow) that can be installed via pip:
```shell
python -m pip install neuflow
```

## Environment Setup

### System Requirements

- System
  - Windows 11 (Fully Tested)
  - Ubuntu 24.04.2 (Fully Tested)
- Python: 3.13
- PyTorch: 2.7.1 + CUDA 12.8

### Pip Packages

```shell
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -m pip install lightning lightning[extra] dearpygui tyro matplotlib av huggingface_hub wandb opencv-python phiflow

set TCNN_CUDA_ARCHITECTURES=86
python -m pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

python -m pip install ./cuda_extensions/freqencoder ./cuda_extensions/gridencoder ./cuda_extensions/raymarching ./cuda_extensions/shencoder
```
For Windows user, open `X64 Native Tools Command Prompt for VS 2022` then activate your python venv if any, and set `TCNN_CUDA_ARCHITECTURES` to your GPU architecture.

|    **GPU**    | H100 | 40X0 | 30X0 | A100 | 20X0 | TITAN V / V100 | 10X0 / TITAN Xp | 9X0 | K80 |
|:---------:|:----:|:----:|:----:|:----:|:----:|:----------------:|:-----------------:|:---:|:---:|
| **CUDA arch** |  `90`  |  `89`  |  `86`  |  `80`  |  `75`  |        `70`        |        `61`         | `52`  | `37`  |

### Optional Packages

#### [triton-windows](https://github.com/woct0rdho/triton-windows) - Activate `torch.compile` for Windows

```shell
python -m pip install -U "triton-windows<3.3"
```

### Wandb Logger
To use the Wandb logger, you need to set up your [Wandb account](https://wandb.ai/) and login. You can do this by running the following command:

```shell
wandb login
```

## Datasets

We provide two datasets for training and testing the model:

- the NeRF-Synthetic is available
  at [Hugging Face - nerf_synthetic](https://huggingface.co/datasets/XayahHina/nerf_synthetic).
- The PI-Neuflow dataset is available
  at [Hugging Face - PI-NeuFlow](https://huggingface.co/datasets/XayahHina/PI-NeuFlow).

ALL datasets are downloaded **_AUTOMATICALLY_** when running the training script.

## Training
### NGP Model
```shell
python -O app.py ngp --dataset.dataset=chair --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=drums --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=ficus --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=hotdog --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=lego --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=materials --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=mic --epochs=500 --gpu_id=0
python -O app.py ngp --dataset.dataset=ship --epochs=500 --gpu_id=0
```

### EPINF Model
```shell
python -O app.py epinf --dataset.dataset=sphere --epochs=500 --gpu_id=0
python -O app.py epinf --dataset.dataset=game --epochs=500 --gpu_id=0
python -O app.py epinf --dataset.dataset=torch2 --epochs=500 --gpu_id=0
python -O app.py epinf --dataset.dataset=fireplace --epochs=500 --gpu_id=0
```