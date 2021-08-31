import os
import time

from setuptools import find_packages, setup

root_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))


def get_version() -> str:
    version_file = os.path.join(root_dir, 'VERSION_PYPI')
    if not os.path.isfile(version_file):
        return f"0.0.0b{int(time.time())}"
    return open(version_file).read().strip()


# We lock these in the requirements.txt file
install_requires = [
    "python-dotenv~=0.19.0",
    "pika~=1.2.0",
    "retry~=0.9.2",
    "smart-open[s3]~=5.2.0",
    "yolo-v4~=0.5",
    "numpy~=1.21.2",
    "opencv-python~=4.5.3.56",
    "scikit-image~=0.18.3",
    "attrs~=21.2.0",
    "Pillow~=8.3.1",
]

# Because we do not have a dev dependencies lock file, lock them here
dev_requires = [
    "pip-tools==6.2.0",
    "coverage==5.5",
    "flake8==3.9.2",
    "black==21.7b0",
    "pytest==6.2.4",
    "pytest-mock==3.6.1",
    "pygount==1.2.4",
    "isort==5.9.3",
    "mypy==0.910",
]

setup(
    name='image_analyzer',
    description="Image Analyzer",
    long_description=open(f"{root_dir}/README.md").read().strip(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
      "dev": dev_requires
    },
    python_requires=">=3.0",
    platforms="any",
    version=get_version(),
    author="Jeremy Sells",
    author_email='mrjeremysells@gmail.com',
    license="MIT license",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
)

