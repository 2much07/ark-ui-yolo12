### 3. setup.py
```python
from setuptools import setup, find_packages

setup(
    name="ark_ui_master",
    version="0.1.0",
    description="ARK: Survival Ascended UI Detection and Automation System",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "ultralytics>=8.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "opencv-python>=4.7.0",
        "numpy>=1.23.5",
        "pyautogui>=0.9.53",
        "pillow>=9.5.0",
        "matplotlib>=3.7.1",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "keyboard>=0.13.5",
        "mss>=6.1.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)