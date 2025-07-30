from setuptools import setup, find_packages
import platform

architecture = platform.machine().lower()

is_arm = 'arm' in architecture or 'aarch64' in architecture

if is_arm:
    reqs = [
        "numpy<2",
        "faiss-cpu",
        "pytest",
        "pytest-cov",
        "scikit-learn",
        "thefuzz[speedup]"
    ]
else:
    reqs = [
        "numpy<2",
        "onnx",
        "onnxruntime",
        "onnxruntime-extensions",
        "faiss-cpu",
        "pytest",
        "pytest-cov",
        "scikit-learn",
        "thefuzz[speedup]",
        "usearch"
    ]

setup(
    name='minivectordb_simple',
    version='1.1.0',
    author='Carlo Moro',
    author_email='cnmoro@gmail.com',
    description="This is a Python project aimed at extracting embeddings from textual data and performing semantic search.",
    packages=find_packages(),
    package_data={
        'minivectordb': ['resources/embedding_model_quantized.onnx']
    },
    include_package_data=True,
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)