import os, subprocess
from setuptools import Extension, setup, find_packages
from pathlib import Path
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:

        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)
        extdir = ext_fullpath.parent.resolve()

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        if self.compiler.compiler_type == "msvc":
            LIGRARY_OUTPUT_DIRECTORY = f"{extdir}{os.sep}/PyMatterSim/_acc"
            if cfg == "Release":
                cmake_args = [
                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={LIGRARY_OUTPUT_DIRECTORY}",
                ]
            else:
                cmake_args = [
                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG={LIGRARY_OUTPUT_DIRECTORY}",
                ]
        else:
            LIGRARY_OUTPUT_DIRECTORY = f"{extdir}{os.sep}/PyMatterSim/_acc"
            cmake_args = [
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={LIGRARY_OUTPUT_DIRECTORY}",
                f"-DCMAKE_BUILD_TYPE={cfg}",
            ]
        build_args = []

        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            if hasattr(self, "parallel") and self.parallel:
                build_args += [f"-j{self.parallel}"]
        if self.compiler.compiler_type == "msvc":
            build_args += [f"--config {cfg}"]

        build_temp = Path(self.build_temp) / ext.name
        if not build_temp.exists():
            build_temp.mkdir(parents=True)
        subprocess.run(
            ["cmake", ext.sourcedir, *cmake_args], cwd=build_temp, check=True
        )
        subprocess.run(
            ["cmake", "--build", ".", *build_args], cwd=build_temp, check=True
        )


setup(
    name="PyMatterSim",
    version="0.2.3",
    author="Yuan-Chao Hu",
    author_email="ychu0213@gmail.com",
    description="A python data analysis library for computer simulations",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/yuanchaohu/pymattersim",
    packages=find_packages(),  # Automatically discover packages
    install_requires=[
        i.strip("\n") for i in open("requirements.txt", "r", encoding="utf-8").readlines()
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    ext_modules=[CMakeExtension("PyMatterSim")],
    cmdclass={"build_ext": CMakeBuild},
)
