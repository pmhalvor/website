import os 

def cd_up_dir(n=1, symbol="/"):
    current_dir = os.getcwd()

    split_dir = current_dir.split(symbol)

    to_dir = symbol.join(split_dir[:-n])

    print("Moving to {}...".format(to_dir))
    os.chdir(to_dir)
    print("Current working directory: {}".format(os.getcwd()))


def cd_to(subdir="", full_path=None):
    if full_path is None:
        current_dir = os.cwd()
        to_dir = os.path.join(current_dir, subdir)
    else:
        to_dir = full_path
    

    print("Moving to {}...".format(to_dir))
    os.chdir(to_dir)
    print("Current working directory: {}".format(os.getcwd()))
