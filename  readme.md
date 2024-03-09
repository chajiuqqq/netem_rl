# Netem RL Part

see parent repo: https://github.com/chajiuqqq/netem

# Dependence

**install PYPI dependence**
```
pip install gymnasium redis stable-baselines3[extra] mininet -i https://pypi.tuna.tsinghua.edu.cn/simple
```
or

```
python3 -m venv python-env
source python-env/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**if using wsl2, enable GPU**

1. install nvidia driver in HOST machine
2. install CUDA ToolKit: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network