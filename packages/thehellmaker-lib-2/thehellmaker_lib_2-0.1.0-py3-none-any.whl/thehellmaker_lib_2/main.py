from importlib.metadata import version
from thehellmaker_lib_1.main import Lib1

class Lib2:
    def __init__(self):
        pass

    def main(self):
        lib1 = Lib1()
        lib1.main()
        pkg_version = version("thehellmaker-lib-2")
        print(f"Hello from lib-2 version {pkg_version}!")


if __name__ == "__main__":
    lib2 = Lib2()
    lib2.main()