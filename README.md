# football_analyzer
Analyze video of football match using Image Classification with YOLO, KMeans and Convolutional Neural Network.


## Setup:
1. Create new virtual env:
``` sh
python -m venv env
```

2. Activate your virtual env:
``` sh
env/Scripts/activate
```

3. Install packages
``` sh
pip install ultralytics
pip install roboflow
pip uninstall torch torchvision
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install supervision
```
