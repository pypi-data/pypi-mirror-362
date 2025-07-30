import os
from devopstestor import Devopstestor
def main():
    current_path = os.path.abspath(os.path.realpath(__file__) + "/..")
    print("main on " + current_path)
    devopstestor = Devopstestor(client_path=current_path)
    devopstestor.start()
