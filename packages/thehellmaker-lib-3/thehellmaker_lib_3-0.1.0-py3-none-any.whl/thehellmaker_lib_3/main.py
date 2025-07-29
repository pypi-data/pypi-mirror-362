from importlib.metadata import version
from thehellmaker_lib_1.main import Lib1

def main():
    lib1 = Lib1()
    lib1.main()
    pkg_version = version("thehellmaker-lib-3")
    print(f"Hello from lib-3 version {pkg_version}!")


if __name__ == "__main__":
    main()
