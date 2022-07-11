from general_util.repeated_timer import RepeatedTimer
from time import sleep


def hello(name):
    print(f"Hello {name}!")


def main():
    rt = RepeatedTimer(0.5, hello, "World")   # RepeatedTimer autostarts, no need to run rt.start()

    try:
        sleep(5)
    finally:
        rt.stop()
        print("Stuff runs after finally")


if __name__ == "__main__":
    main()
