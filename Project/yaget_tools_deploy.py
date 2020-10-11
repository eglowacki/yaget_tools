# deploy yaget tools to a single folder, which is part of the path for yaget-dev machines

import os.path
from os import path
import os
import filecmp
import shutil


def GetYagetRoot(currentPath):
    filePath = path.join(currentPath, 'yaget_root.txt')
    result = path.isfile(filePath)
    if not result:
        checkPath = path.join(currentPath, '..')
        if path.exists(checkPath):
            os.chdir(checkPath)
            newUpPath = os.getcwd()
            if currentPath == newUpPath:
                return None
            return GetYagetRoot(newUpPath)
        else:
            return None
    else:
        return currentPath

print("Yaget dev deployment tool. It copies files listed in DevToolsDeployment.txt to DevTools. yaget 2019 (c)")
currentDirectory = os.getcwd()
currentPath = currentDirectory
lineList = []

deploymentFileName = 'DevToolsDeployment.txt'
copied = 0
marker = GetYagetRoot(currentPath)
if marker:
    devToolsFolder = path.join(marker, 'DevTools')
    sourceModules = path.join(devToolsFolder, deploymentFileName)
    if path.exists(devToolsFolder) and path.isfile(sourceModules):
        lineList = [line.rstrip('\n') for line in open(sourceModules)]

        for sourcePath in lineList:
            sourceFile = path.basename(sourcePath)
            targetPath = path.join(devToolsFolder, sourceFile)
            sourceExist = path.isfile(sourcePath)
            targetExist = path.isfile(targetPath)

            if sourceExist and targetExist:
                isSame = filecmp.cmp(sourcePath, targetPath, shallow=True)
                if isSame:
                    print("File '{}' upto date.".format(sourcePath))
                else:
                    print("File '{}' needs update.".format(sourcePath))
                    shutil.copy(sourcePath, targetPath, follow_symlinks=True)
                    copied += 1

            elif sourceExist and not targetExist:
                print("Copy '{}' to '{}'.".format(sourcePath, targetPath))
                shutil.copy(sourcePath, targetPath, follow_symlinks=True)
                copied += 1

print("{} total deployment files. {} where out of date and updated. The rest {} where up to date.".format(len(lineList), copied, len(lineList) - copied))
os.chdir(currentDirectory)
