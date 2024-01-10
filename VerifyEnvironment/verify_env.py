'''
verify yaget development and tools environment.
'''

import argparse
from os import path
from os import getenv


deployTag = 'DEPLOY'


def main():

    global deployTag

    parser = argparse.ArgumentParser(description='''Verify yaget development and tools environment and update settings if needed. Yaget (c)2024.
                                                    Sample input --destination=bin --metafile=bins''')
    parser.add_argument('-p', '--path_tool', dest='path_tool', default='.\\', help='Folder where yaget tools reside')
    #parser.add_argument('-c', '--configuration', dest='configuration', default='Release', help='Build configuration to use as a source of dependencies')
    #parser.add_argument('-d', '--destination', dest='destination', required=True, help='Where to copy the dependent files')
    #parser.add_argument('-m', '--metafile', dest='meta', required=True, help='Json file name which contains list of configurations and files to copy from root/file_to_copy to destination/file_to_copy. .deployment extension is appended if passed file name does not exist.')
    #parser.add_argument('-s', '--silent', action='store_true', help='Supress print statements (does not apply to --help or error messages')
    #parser.add_argument('-t', '--test', action='store_true', help='Run through all steps but not actully update files, useful for diagnostics, checks')

    args = parser.parse_args()

    tools_folder = path.normcase(path.abspath(args.path_tool))

    if not path.isdir(tools_folder):
        print("[{}] ERROR: Folder '{}' for tools does not exist.".format(deployTag, tools_folder))
        return False

    currentPath = path.normcase(getenv('PATH'))

    if currentPath:
        if tools_folder.lower() not in currentPath.lower():
            envPathFolders = currentPath.split(';')
            print("[{}] ERROR: yaget development tools folder '{}' is not in environment path.\nCurrent path is:\n--->\n{}\n<---".format(deployTag, tools_folder, envPathFolders))
        else:
            print("[{}] yaget development tools folder is setup.".format(deployTag))

    return True


if __name__ == "__main__":
    main()
