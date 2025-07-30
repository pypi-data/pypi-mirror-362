import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("__version__", "r") as f:
    old_version = f.read()

# 매뉴얼로 버전을 지정할 경우 아래 블럭을 주석처리하고 new_version을 직접 입력
new_version = old_version[:].split(".")
new_version[-1] = str(int(new_version[-1]) + 1)
new_version = ".".join(new_version)

yn = input(f"old version={old_version}, new version={new_version}. 업데이트 할까요? [y/n]:  ")
if yn in {"y", "Y", "ㅛ"}:
    with open("__version__", "w") as f:
        f.write(new_version)

    with open("kmspy/__init__.py", "r") as f:
        old_init = f.read()
        new_init = old_init.replace(f'__version__ = "{old_version}"', f'__version__ = "{new_version}"')

    with open("kmspy/__init__.py", "w") as f:
        f.write(new_init)

setuptools.setup(
    name="kmspy",
    version=new_version,
    author="KMS",
    author_email="su4651@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy"
    ],
)