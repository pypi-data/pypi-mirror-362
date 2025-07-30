"""
SleepyDriver 라이브러리 설치 스크립트
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sleepy-driver",
    version="1.0.0",
    author="SleepyDriver Team",
    author_email="sleepy.driver@example.com",
    description="AI-powered drowsiness detection library for driver safety",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sleepy-driver/sleepy-driver",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sleepy_driver': [
            'models/*.pkl',
            'models/*.pth',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "mediapipe>=0.8.0",
    ],
    extras_require={
        "ml": [
            "joblib>=1.0.0", 
            "scikit-learn>=1.0.0"
        ],
        "dl": [
            "torch>=1.9.0",
            "torchvision>=0.10.0"
        ],
        "all": [
            "joblib>=1.0.0",
            "scikit-learn>=1.0.0", 
            "torch>=1.9.0",
            "torchvision>=0.10.0"
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sleepy-driver-demo=examples.demo:main",
        ],
    },
    keywords="drowsiness detection, driver safety, computer vision, AI, machine learning",
) 