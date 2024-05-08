import os

def extractFiles(path=os.getcwd()):
    fileList = []

    pathExists = os.path.exists(path)
    isFile = os.path.isfile(path)
    isDir = os.path.isdir(path)

    if pathExists and isDir:
        for root, dirs, files in os.walk(path):
            for file in files:
                if "dataset" in file:
                    fileList.append(file)

    return fileList

files = []
path = "/afs/cern.ch/user/d/diegof/Wprime/GE-method/nanoaod_base_analysis/data/tmp/GE2022_config/"
files = extractFiles(path)

with open("MCsamplesToCiemat1.txt", "w") as fw:
    for file in files:
        print(file)
        with open(path + file, "r") as fr:
            sample = fr.readlines()[0]
            print(sample)
            fw.write(sample + "\n")
        fr.close()
fw.close()
