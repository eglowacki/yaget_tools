import argparse
from os import path
import os
import filecmp
import shutil
import json
import pprint
import copy
deployTag = 'BUILD'
# # Actualy copy/move files from root/files to destination/files
# # unsing time stamp for already existing files at destination
# def UpdateDeploymentFiles(files, root, destination, silentPrint, test):

    # for file in files:
        # sourceFile = path.join(root, file)
        # targetFile = path.join(destination, path.basename(sourceFile))
        # sourceExist = path.isfile(sourceFile)
        # targetExist = path.isfile(targetFile)
        # if sourceExist and targetExist:
            # isSame = filecmp.cmp(sourceFile, targetFile, shallow=True)
            # if isSame:
                # if not silentPrint:
                    # print("[{}] OK  current: '{}' upto date.".format(deployTag, ConvertPath(targetFile)))
            # else:
                # if not silentPrint:
                    # print("[{}] OK  updated: '{}' needs update.".format(deployTag, ConvertPath(targetFile)))
                # if not test:
                    # shutil.copy(sourceFile, targetFile, follow_symlinks=True)

        # elif sourceExist and not targetExist:
            # if not silentPrint:
                # print("[{}] OK   copied: '{}' to: '{}'.".format(deployTag, ConvertPath(sourceFile), ConvertPath(targetFile)))
            # if not test:
                # shutil.copy(sourceFile, targetFile, follow_symlinks=True)

        # elif not sourceExist:
            # if not silentPrint:
                # print("[{}] ERR missing: '{}' does not exist.".format(deployTag, ConvertPath(sourceFile)))

# Load actuall meta configuration file (.build)
# from disk and return json object or None
def LoadMetaFile(fileName):
    try:
        with open(fileName, 'r') as f:
            try:
                datastore = json.load(f)
                return datastore

            except json.JSONDecodeError as jex:
                print("** DEPLOY ERROR **")
                print("Invalid build file:\n{}({}, {}): error {}".format(ConvertPath(fileName), jex.lineno, jex.colno, jex))
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

# def GetMetaFilesFor(datastore, configuration):
    # if configuration in datastore:
        # return datastore[configuration]

    # return []

# def CombineMetaConfiguration(baseDatastore, optionalDatastore):

    # if 'Configuration' in optionalDatastore:
        # for key in optionalDatastore['Configuration']:
            # files = GetMetaFilesFor(optionalDatastore['Configuration'], key)
            # baseDatastore['Configuration'][key].extend(files)

    # return baseDatastore

def ConvertPath(path):
    return path.replace(os.path.sep, '/')


# def main():

    # global deployTag

    # parser = argparse.ArgumentParser(description='''Update deployment files from it's source folder to destination folder for a build configuration. Yaget (c)2019.
                                                    # Sample input [$(YAGET_ROOT_FOLDER)\DevTools\DependencyDeployment\deploy.py --root=$(YAGET_ROOT_FOLDER) --configuration=$(Configuration) --destination=$(YAGET_RUN_FOLDER) --metafile=$(ProjectDir)$(TargetName).deployment]
                                                    # expended to [c:\Development\yaget\DevTools\DependencyDeployment\deploy.py --root=c:\Development\yaget --configuration=Debug --destination=c:\Development\yaget\branch\version_0_2\bin\Coordinator\x64.Debug\ --metafile=C:\Development\yaget\branch\version_0_2\Research\Coordinator\build\Coordinator.deployment]''')
    # parser.add_argument('-r', '--root', dest='root', required=True, help='Root used in prefix of files to copy')
    # parser.add_argument('-c', '--configuration', dest='configuration', required=True, help='Build configuration to use as a source of dependencies')
    # parser.add_argument('-d', '--destination', dest='destination', required=True, help='Where to copy the dependent files')
    # parser.add_argument('-m', '--metafile', dest='meta', required=True, help='Json file name which contains list of configurations and files to copy from root/file_to_copy to destination/file_to_copy')
    # parser.add_argument('-s', '--silent', action='store_true', help='Supress print statements (does not apply to --help or error messages')
    # parser.add_argument('-t', '--test', action='store_true', help='Run through all steps but not actully update files, useful for diagnostics, checks')

    # args= parser.parse_args()

    # if not path.isfile(args.meta):
        # print("[{}] ERR: Metafile: '{}' is not a valid file.".format(deployTag, ConvertPath(args.meta)))
        # exit(1)

    # if args.test:
        # deployTag = 'DEPLOY-TEST'

    # silentPrint = args.silent

    # datastore = LoadMetaFile(args.meta)
    # if not datastore:
        # exit(1)

    # if not silentPrint:
        # print("[{}] Yaget deployment started for '{}' configuration using metafile: '{}'...".format(deployTag, args.configuration, ConvertPath(args.meta)))

    # if 'Include' in datastore:
        # includeFile = datastore['Include']
        # includeSourceFile = path.join(args.root, includeFile)
        # baseDatastore = LoadMetaFile(includeSourceFile)

        # datastore = CombineMetaConfiguration(baseDatastore, datastore)

    # if not 'Configuration' in datastore:
        # print("[{}] ERR: Metafile: '{}' does not have 'Configuration' block.".format(deployTag, ConvertPath(args.meta)))
        # exit(1)

    # confBlock = datastore['Configuration']
    # filesToDeploy = []

    # # collect all files into one list
    # filesToDeploy += GetMetaFilesFor(confBlock, 'Common')
    # filesToDeploy += GetMetaFilesFor(confBlock, args.configuration)

    # # remove any duplicate and transform to valid linux like path
    # filesToDeploy = list(dict.fromkeys(filesToDeploy))
    # filesToDeploy = [ConvertPath(a) for a in filesToDeploy]

    # # remove file which starts with -
    # removes = list((x for x in filesToDeploy if x.startswith('-')))
    # for rm in removes:
        # filesToDeploy.remove(rm)
        # if rm[1:] in filesToDeploy:
            # if not silentPrint:
                # print("[{}] OK  removed: '{}' from deployment.".format(deployTag, rm[1:]))

            # filesToDeploy.remove(rm[1:])

    # # finaly update deploy files
    # UpdateDeploymentFiles(filesToDeploy, args.root, args.destination, silentPrint, args.test)

    # if not silentPrint:
        # print("[{}] Yaget deployment finished.".format(deployTag))


#----------------------------------------------------------------------------------------------------
#---------------------------- assimp -------------------------------------------
# Dependencies> git clone https://github.com/assimp/assimp.git assimp-5.0.1
# Dependencies> rmdir /S /Q assimp-5.0.1\.git   ; check first for existance if this filter (hidden)
# Dependencies> mkdir assimp-5.0.1\builds       ; delete old builds folder if exist
# Dependencies> cd assimp5.0.1\builds
#
# Dependencies/assimp-5.0.1/builds> cmake ../ -G"Visual Studio 16 2019" -A x64 -DASSIMP_BUILD_ZLIB=ON
# Dependencies/assimp-5.0.1/builds> cmake --build . --config Debug
# Dependencies/assimp-5.0.1/builds> bin\Debug\unit.exe
# Dependencies/assimp-5.0.1/builds> cmake --build . --config Release
# Dependencies/assimp-5.0.1/builds> bin\Release\unit.exe


#----------------------------------------------------------------------------------------------------
#---------------------------- flatbuffers -------------------------------------------
# Dependencies> git clone https://github.com/google/flatbuffers.git flatbuffers-1.11.0
# Dependencies> rmdir /S /Q flatbuffers-1.11.0\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir flatbuffers-1.11.0\builds      ; delete old builds folder if exist
# Dependencies> cd flatbuffers-1.11.0\builds
#
# Dependencies/flatbuffers-1.11.0/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/flatbuffers-1.11.0/builds> cmake --build . --config Debug
# Dependencies/flatbuffers-1.11.0/builds> Debug\flattests.exe
# Dependencies/flatbuffers-1.11.0/builds> cmake --build . --config Release
# Dependencies/flatbuffers-1.11.0/builds> Release\flattests.exe


#----------------------------------------------------------------------------------------------------
#---------------------------- DirectXTex -------------------------------------------
# Dependencies> git clone https://github.com/microsoft/DirectXTex.git DirectXTex-170
# Dependencies> rmdir /S /Q DirectXTex-170\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir DirectXTex-170\builds      ; delete old builds folder if exist
# Dependencies> cd DirectXTex-170\builds
#
# Dependencies/DirectXTex-170/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/DirectXTex-170/builds> cmake --build . --config Debug
# Dependencies/DirectXTex-170/builds> cmake --build . --config Release


#----------------------------------------------------------------------------------------------------
#---------------------------- DirectXTK11 -------------------------------------------
# Dependencies> git clone https://github.com/microsoft/DirectXTK.git DirectXTK11-5.10.2020
# Dependencies> rmdir /S /Q DirectXTK11-5.10.2020\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir DirectXTK11-5.10.2020\builds      ; delete old builds folder if exist
# Dependencies> cd DirectXTK11-5.10.2020\builds
#
# Dependencies/DirectXTK11-5.10.2020/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/DirectXTK11-5.10.2020/builds> cmake --build . --config Debug
# Dependencies/DirectXTK11-5.10.2020/builds> cmake --build . --config Release


#----------------------------------------------------------------------------------------------------
#---------------------------- DirectXTK12 -------------------------------------------
# Dependencies> git clone https://github.com/microsoft/DirectXTK12.git DirectXTK12-4.3.2020
# Dependencies> rmdir /S /Q DirectXTK12-4.3.2020\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir DirectXTK12-4.3.2020\builds      ; delete old builds folder if exist
# Dependencies> cd DirectXTK12-4.3.2020\builds
#
# Dependencies/DirectXTK12-4.3.2020/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/DirectXTK12-4.3.2020/builds> cmake --build . --config Debug
# Dependencies/DirectXTK12-4.3.2020/builds> cmake --build . --config Release

#----------------------------------------------------------------------------------------------------
#---------------------------- fmt -------------------------------------------
# Dependencies> git clone https://github.com/fmtlib/fmt.git fmt-6.2.0
# Dependencies> rmdir /S /Q fmt-6.2.0\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir fmt-6.2.0\builds      ; delete old builds folder if exist
# Dependencies> cd fmt-6.2.0\builds
#
# Dependencies/fmt-6.2.0/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/fmt-6.2.0/builds> cmake --build . --config Debug
# Dependencies/fmt-6.2.0/builds> bin\Debug\format-test.exe
# Dependencies/fmt-6.2.0/builds> cmake --build . --config Release
# Dependencies/fmt-6.2.0/builds> bin\Release\format-test.exe


#----------------------------------------------------------------------------------------------------
#---------------------------- nlohmann-json -------------------------------------------
# Dependencies> git clone https://github.com/nlohmann/json.git nlohmann-json-3.7.3
# Dependencies> rmdir /S /Q nlohmann-json-3.7.3\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir nlohmann-json-3.7.3\builds      ; delete old builds folder if exist
# Dependencies> cd nlohmann-json-3.7.3\builds
#
# Dependencies/nlohmann-json-3.7.3/builds> cmake ../ -G"Visual Studio 16 2019" -A x64
# Dependencies/nlohmann-json-3.7.3/builds> cmake --build . --config Debug
# Dependencies/nlohmann-json-3.7.3/builds> ctest --output-on-failure -C Debug   ; does not work
# Dependencies/nlohmann-json-3.7.3/builds> cmake --build . --config Release
# Dependencies/nlohmann-json-3.7.3/builds> ctest --output-on-failure -C Release ; does not work

#------------------------------------ Evaluations  --------------------------------------------------
#----------------------------------------------------------------------------------------------------
#---------------------------- reactphysics3d -------------------------------------------
# Dependencies> git clone https://github.com/DanielChappuis/reactphysics3d.git reactphysics3d-0.7.1
# Dependencies> rmdir /S /Q reactphysics3d-0.7.1\.git  ; check first for existance if this filter (hidden)
# Dependencies> mkdir reactphysics3d-0.7.1\builds      ; delete old builds folder if exist
# Dependencies> cd reactphysics3d-0.7.1\builds
#
# Dependencies/reactphysics3d-0.7.1/builds> cmake ../ -G"Visual Studio 16 2019" -A x64 -DRP3D_COMPILE_TESTBED=ON -DRP3D_COMPILE_TESTS=ON -DRP3D_PROFILING_ENABLED=ON -DRP3D_LOGS_ENABLED=ON
# Dependencies/reactphysics3d-0.7.1/builds> cmake --build . --config Debug
# Dependencies/reactphysics3d-0.7.1/builds> test\Debug\tests.exe
# Dependencies/reactphysics3d-0.7.1/builds> cmake --build . --config Release
# Dependencies/reactphysics3d-0.7.1/builds> test\Release\tests.exe

#----------------------------------------------------------------------------------------------------
#---------------------------- PhysX -------------------------------------------
# Dependencies> git clone https://github.com/NVIDIAGameWorks/PhysX.git PhysX-4.1
# Dependencies> rmdir /S /Q PhysX-4.1\.git  ; check first for existance if this filter (hidden)
# Dependencies> cd PhysX-4.1\physx
#
# Dependencies/PhysX-4.1/physx> generate_projects.bat   ; will ask for msdev version selection
# Dependencies/PhysX-4.1/physx> cd compiler\vc16win64
# Dependencies/PhysX-4.1/physx/compiler\vc16win64>
#                                                 'create' include\typeinfo.h
                                                                #include <typeinfo>
#                               Change ''Treat Warnings As Errors' to No (/WX-) for Sample Renderer (All Configurations)
# Dependencies/PhysX-4.1/physx/compiler\vc16win64> devenv PhysXSDK.sln /build Debug
# Dependencies/PhysX-4.1/physx/compiler\vc16win64> devenv PhysXSDK.sln /build Release


#----------------------------------------------------------------------------------------------------
#---------------------------- bullet3 -------------------------------------------
# Dependencies> git clone https://github.com/bulletphysics/bullet3.git bullet3-2.8.9
# Dependencies> rmdir /S /Q bullet3-2.8.9\.git  ; check first for existance if this filter (hidden)
# Dependencies> cd bullet3-2.8.9






#cmake --build . --target MyExe --config Debug

deployTag = 'MODULE-BUILD'


def BuildDependency(title, jsonBlock):

    print(title + ':')
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(jsonBlock)


class ModuleBuilder:
    """Represents module configuration and build rules.
    It is initialized from json blob with defaults"""

    def __init__(self, name, jsonBlock, defaultBlock):
        self.Name = name
        self.Version = '{}'.format(jsonBlock['version'])
        self.RootFolderName = '{}-{}'.format(name, self.Version)

        cmakeDefaults = {}
        if 'cmake' in defaultBlock:
            cmakeDefaults = defaultBlock['cmake']

        if 'cmake' in jsonBlock and 'build_folder' in jsonBlock['cmake']:
            self.BuildFolderName = path.join(self.RootFolderName, jsonBlock['cmake']['build_folder'])
        elif 'build_folder' in cmakeDefaults:
            self.BuildFolderName = path.join(self.RootFolderName, cmakeDefaults['build_folder'])
        else:
            self.BuildFolderName = self.RootFolderName

        self.BuildOptions = ''
        if 'options' in cmakeDefaults:
            self.BuildOptions = cmakeDefaults['options']

        if 'cmake' in jsonBlock and 'options' in jsonBlock['cmake']:
            self.BuildOptions += ' ' + jsonBlock['cmake']['options']

        self.BuildConfigurations = []
        if 'configurations' in defaultBlock:
            self.BuildConfigurations = copy.deepcopy(defaultBlock['configurations'])

        if 'configurations' in jsonBlock:
            self.BuildConfigurations.extend(jsonBlock['configurations'])

        self.CmakeCommand = 'cmake ../ -G"Visual Studio 16 2019" -A x64 ' + self.BuildOptions

        self.BuildCommands = []
        for configuration in self.BuildConfigurations:
            self.BuildCommands.append('cmake --build . --config {}'.format(configuration))

        self.TestCommands = []
        if 'tests' in defaultBlock:
            self.TestCommands = copy.deepcopy(defaultBlock['tests'])

        if 'tests' in jsonBlock:
            self.TestCommands.extend(jsonBlock['tests'])

    def __repr__(self):
        #return '<class \'%s\' instance at %s>' % (self.__class__.__name__, id(self))
        return '<class \'{}\' instance at {}>\nName: {}\nVersion: {}\nRoot Folder: {}\nBuild Folder: {}\nBuild options: {}\nBuild Configurations: {}\nGenerator: {}'.format(
            self.__class__.__name__, id(self), self.Name, self.Version, self.RootFolderName, self.BuildFolderName, self.BuildOptions, self.BuildConfigurations, self.CmakeCommand)



    #print('---------------------------------------------------------------------')
    #print('Module Name: {}'.format(name))
    #print('Module Version: {}'.format(version))
    #print('Module folder name: {}'.format(moduleFolderName))
    #print('Module build folder name: {}'.format(buildFolderName))
    #print('Module build options: {}'.format(buildOptions))
    #print('Module build configurations: {}'.format(buildConfigurations))
    #print('       Generator: {}'.format(generator))
    #for configuration in buildConfigurations:
        #buildCommand = 'cmake --build . --config {}'.format(configuration)

        #print('       Build Command: {}'.format(buildCommand))

    #for test in tests:
        #testCommand = test

        #print('       Test Command: {}'.format(testCommand))



def ParseBuildBlock():
    pass




def main():

    global deployTag

    parser = argparse.ArgumentParser(description='''Automation of git, build and deploy of yaget dependency libraries. Yaget (c)2020.
                                                  # Sample input [$(YAGET_ROOT_FOLDER)\DevTools\DependencyDeployment\deploy.py --root=$(YAGET_ROOT_FOLDER) --configuration=$(Configuration) --destination=$(YAGET_RUN_FOLDER) --metafile=$(ProjectDir)$(TargetName).deployment]
                                                  # expended to [c:\Development\yaget\DevTools\DependencyDeployment\deploy.py --root=c:\Development\yaget --configuration=Debug --destination=c:\Development\yaget\branch\version_0_2\bin\Coordinator\x64.Debug\ --metafile=C:\Development\yaget\branch\version_0_2\Research\Coordinator\build\Coordinator.deployment]''')
    parser.add_argument('-r', '--root', dest='root', required=True, help='Root used in prefix of files to copy')
    parser.add_argument('-c', '--configuration', dest='configuration', required=True, help='Build configuration to use as a source of dependencies')
    parser.add_argument('-d', '--destination', dest='destination', required=True, help='Where to copy the dependent files')
    parser.add_argument('-m', '--metafile', dest='meta', required=True, help='Json file name which contains list of configurations and files to copy from root/file_to_copy to destination/file_to_copy')
    parser.add_argument('-s', '--silent', action='store_true', help='Supress print statements (does not apply to --help or error messages')
    parser.add_argument('-t', '--test', action='store_true', help='Run through all steps but not actully update files, useful for diagnostics, checks')

    args = parser.parse_args()

    if not path.isfile(args.meta):
        print("[{}] ERR: Metafile: '{}' is not a valid file.".format(deployTag, ConvertPath(args.meta)))
        exit(1)

    if args.test:
        deployTag = 'BUILD-TEST'

    silentPrint = args.silent

    datastore = LoadMetaFile(args.meta)
    if not datastore:
        exit(1)

    pullFromGit = False

    # default sections
    defaultBlock = {}
    if 'Defaults' in datastore:
        defaultBlock = datastore['Defaults']

    cmakeDefaults = {}
    if 'cmake' in defaultBlock:
        cmakeDefaults = defaultBlock['cmake']

    configurationsDefault = []
    if 'configurations' in defaultBlock:
        configurationsDefault = defaultBlock['configurations']

    testsDefault = []
    if 'tests' in defaultBlock:
        testsDefault = defaultBlock['tests']


    modules = {}
    if 'Modules' in datastore:
        modules = datastore['Modules']

    evaluations = {}
    if 'Evaluations' in datastore:
        evaluations = datastore['Evaluations']

    generators = []

    moduleNames = modules.keys()
    for name in moduleNames:
        jsonBlock = modules[name]

        generator = ModuleBuilder(name, jsonBlock, defaultBlock)

        generators.append(generator)

        #version = settings['version']
        #moduleFolderName = name + '-' + '{}'.format(version)

        #if 'cmake' in settings and 'build_folder' in settings['cmake']:
            #buildFolderName = path.join(moduleFolderName, settings['cmake']['build_folder'])
        #elif 'build_folder' in cmakeDefaults:
            #buildFolderName = path.join(moduleFolderName, cmakeDefaults['build_folder'])
        #else:
            #buildFolderName = moduleFolderName

        #buildOptions = ''
        #if 'options' in cmakeDefaults:
            #buildOptions = cmakeDefaults['options']

        #if 'cmake' in settings and 'options' in settings['cmake']:
            #buildOptions += ' ' + settings['cmake']['options']

        #buildConfigurations = copy.deepcopy(configurationsDefault)
        #if 'configurations' in settings:
            #buildConfigurations.extend(settings['configurations'])

        #tests = copy.deepcopy(testsDefault)
        #if 'tests' in settings:
            #tests.extend(settings['tests'])

        #generator = 'cmake ../ -G"Visual Studio 16 2019" -A x64 ' + buildOptions

        #print('---------------------------------------------------------------------')
        #print('Module Name: {}'.format(name))
        #print('Module Version: {}'.format(version))
        #print('Module folder name: {}'.format(moduleFolderName))
        #print('Module build folder name: {}'.format(buildFolderName))
        #print('Module build options: {}'.format(buildOptions))
        #print('Module build configurations: {}'.format(buildConfigurations))
        #print('       Generator: {}'.format(generator))
        #for configuration in buildConfigurations:
            #buildCommand = 'cmake --build . --config {}'.format(configuration)

            #print('       Build Command: {}'.format(buildCommand))

        #for test in tests:
            #testCommand = test

            #print('       Test Command: {}'.format(testCommand))

        #z = 0
        #z




    #----------------------------------------------------------------------------------------------------
    #---------------------------- assimp -------------------------------------------
    # Dependencies> git clone https://github.com/assimp/assimp.git assimp-5.0.1
    # Dependencies> rmdir /S /Q assimp-5.0.1\.git   ; check first for existance if this filter (hidden)
    # Dependencies> mkdir assimp-5.0.1\builds       ; delete old builds folder if exist
    # Dependencies> cd assimp5.0.1\builds
    #
    # Dependencies/assimp-5.0.1/builds> cmake ../ -G"Visual Studio 16 2019" -A x64 -DASSIMP_BUILD_ZLIB=ON
    # Dependencies/assimp-5.0.1/builds> cmake --build . --config Debug
    # Dependencies/assimp-5.0.1/builds> bin\Debug\unit.exe
    # Dependencies/assimp-5.0.1/builds> cmake --build . --config Release
    # Dependencies/assimp-5.0.1/builds> bin\Release\unit.exe


    #BuildDependency('Defaults', defaults)
    #BuildDependency('Modules', modules)
    #BuildDependency('Evaluations', evaluations)

    #print('Finished deployment build.')
    #silentPrint


if __name__ == "__main__":
    main()


