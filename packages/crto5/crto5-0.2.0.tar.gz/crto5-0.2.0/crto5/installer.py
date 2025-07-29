
import os
import urllib.request
import pathlib

def main():
    url = 'https://raw.githubusercontent.com/cmderr11/crt1/refs/heads/main/crt1.py'
    desktop = os.path.join(pathlib.Path.home(), 'Desktop')
    falsh_folder = os.path.join(desktop, 'falsh')
    os.makedirs(falsh_folder, exist_ok=True)
    target_file = os.path.join(falsh_folder, 'crt1.py')
    urllib.request.urlretrieve(url, target_file)
    print(f"Downloaded to {target_file}")

if __name__ == "__main__":
    main()
