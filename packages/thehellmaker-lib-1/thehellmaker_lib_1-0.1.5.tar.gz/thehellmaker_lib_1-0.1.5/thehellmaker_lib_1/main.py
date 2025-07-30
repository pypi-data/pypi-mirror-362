from importlib.metadata import version

class Lib1:
    def __init__(self):
        pass

    def main(self):
        pkg_version = version("thehellmaker-lib-1")
        print(f"Hello from lib-1 version {pkg_version}!")


if __name__ == "__main__":
    lib1 = Lib1()
    lib1.main()
