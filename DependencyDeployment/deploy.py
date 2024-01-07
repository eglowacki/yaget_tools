import argparse
from os import path
import os
import filecmp
import shutil
import json

deployTag = 'DEPLOY'
# Actualy copy/move files from root/files to destination/files
# unsing time stamp for already existing files at destination
def UpdateDeploymentFiles(files, root, destination, silentPrint, test):

    for file in files:
        sourceFile = path.join(root, file)
        targetFile = path.join(destination, path.basename(sourceFile))
        sourceExist = path.isfile(sourceFile)
        targetExist = path.isfile(targetFile)
        if sourceExist and targetExist:
            isSame = filecmp.cmp(sourceFile, targetFile, shallow=True)
            if isSame:
                if not silentPrint:
                    print("[{}] OK  current: '{}' upto date.".format(deployTag, ConvertPath(targetFile)))
            else:
                if not silentPrint:
                    print("[{}] OK  updated: '{}' needs update.".format(deployTag, ConvertPath(targetFile)))
                if not test:
                    shutil.copy(sourceFile, targetFile, follow_symlinks=True)

        elif sourceExist and not targetExist:
            if not silentPrint:
                print("[{}] OK   copied: '{}' to: '{}'.".format(deployTag, ConvertPath(sourceFile), ConvertPath(targetFile)))
            if not test:
                shutil.copy(sourceFile, targetFile, follow_symlinks=True)

        elif not sourceExist:
            if not silentPrint:
                print("[{}] ERROR missing: '{}' does not exist.".format(deployTag, ConvertPath(sourceFile)))

# Load actuall meta configuration file (.deployment)
# from disk and return json object or None
def LoadMetaFile(fileName):
    try:
        with open(fileName, 'r') as f:
            try:
                datastore = json.load(f)
                return datastore

            except json.JSONDecodeError as jex:
                print("** DEPLOY ERROR **")
                print("Invalid deploy file:\n{}({}, {}): error {}".format(ConvertPath(fileName), jex.lineno, jex.colno, jex))
                lines = jex.doc.splitlines()
                if jex.lineno > -1 and jex.lineno < len(lines):
                    wrongCodeLine = lines[jex.lineno]
                    print("Offending line (between * *):")
                    print("     *{}*".format(wrongCodeLine))
                    colNo = max(1, jex.colno)
                    print("      {}".format('-' * (colNo - 1) + '!'))

                return None
    except IOError:
        return None

def GetMetaFilesFor(datastore, configuration):
    if configuration in datastore:
        return datastore[configuration]

    return []

def CombineMetaConfiguration(baseDatastore, optionalDatastore):

    if 'Configuration' in optionalDatastore:
        for key in optionalDatastore['Configuration']:
            files = GetMetaFilesFor(optionalDatastore['Configuration'], key)
            baseDatastore['Configuration'][key].extend(files)

    return baseDatastore

def ConvertPath(path):
    return path.replace(os.path.sep, '/')


def main():

    global deployTag

    parser = argparse.ArgumentParser(description='''Update deployment files from it's source folder to destination folder for a build configuration. Yaget (c)2019.
                                                    Sample input --destination=bin --metafile=bins
                                                    or [$(YAGET_ROOT_FOLDER)\DevTools\DependencyDeployment\deploy.py --root=$(YAGET_ROOT_FOLDER) --configuration=$(Configuration) --destination=$(YAGET_RUN_FOLDER) --metafile=$(ProjectDir)$(TargetName).deployment]
                                                    expended to [c:\Development\yaget\DevTools\DependencyDeployment\deploy.py --root=c:\Development\yaget --configuration=Debug --destination=c:\Development\yaget\branch\version_0_2\bin\Coordinator\x64.Debug\ --metafile=C:\Development\yaget\branch\version_0_2\Research\Coordinator\build\Coordinator.deployment]''')
    parser.add_argument('-r', '--root', dest='root', default='.\\', help='Root used in prefix of files to copy')
    parser.add_argument('-c', '--configuration', dest='configuration', default='Release', help='Build configuration to use as a source of dependencies')
    parser.add_argument('-d', '--destination', dest='destination', required=True, help='Where to copy the dependent files')
    parser.add_argument('-m', '--metafile', dest='meta', required=True, help='Json file name which contains list of configurations and files to copy from root/file_to_copy to destination/file_to_copy. .deployment extension is appended if passed file name does not exist.')
    parser.add_argument('-s', '--silent', action='store_true', help='Supress print statements (does not apply to --help or error messages')
    parser.add_argument('-t', '--test', action='store_true', help='Run through all steps but not actully update files, useful for diagnostics, checks')

    args= parser.parse_args()

    if not path.isfile(args.meta):
        if path.isfile(args.meta + '.deployment'):
            args.meta += '.deployment'  
        else:
            print("[{}] INFO: Meta file '{}' does not exist, no dependency deploymnet will be performed.".format(deployTag, ConvertPath(args.meta)))
            exit(0)

    if args.test:
        deployTag = 'DEPLOY-TEST'

    silentPrint = args.silent

    datastore = LoadMetaFile(args.meta)
    if not datastore:
        exit(1)

    if not silentPrint:
        print("[{}] Yaget deployment started for '{}' configuration using metafile: '{}'...".format(deployTag, args.configuration, ConvertPath(args.meta)))

    if 'Include' in datastore:
        includeFile = datastore['Include']
        includeSourceFile = path.join(args.root, includeFile)
        baseDatastore = LoadMetaFile(includeSourceFile)

        datastore = CombineMetaConfiguration(baseDatastore, datastore)

    if not 'Configuration' in datastore:
        print("[{}] ERROR: Metafile: '{}' does not have 'Configuration' block.".format(deployTag, ConvertPath(args.meta)))
        exit(1)

    confBlock = datastore['Configuration']
    filesToDeploy = []

    # collect all files into one list
    filesToDeploy += GetMetaFilesFor(confBlock, 'Common')
    filesToDeploy += GetMetaFilesFor(confBlock, args.configuration)

    # remove any duplicate and transform to valid linux like path
    filesToDeploy = list(dict.fromkeys(filesToDeploy))
    filesToDeploy = [ConvertPath(a) for a in filesToDeploy]

    # remove file which starts with -
    removes = list((x for x in filesToDeploy if x.startswith('-')))
    for rm in removes:
        filesToDeploy.remove(rm)
        if rm[1:] in filesToDeploy:
            if not silentPrint:
                print("[{}] OK  removed: '{}' from deployment.".format(deployTag, rm[1:]))

            filesToDeploy.remove(rm[1:])

    # finaly update deploy files
    UpdateDeploymentFiles(filesToDeploy, args.root, args.destination, silentPrint, args.test)

    if not silentPrint:
        print("[{}] Yaget deployment finished.".format(deployTag))


if __name__ == "__main__":
    main()


