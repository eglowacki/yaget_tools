# provide a way to support arbitrary data folders (like Assets) within project/solution folders IOW, we want
# to have data for local project under that priject folder.
# Maybe we can use $(ProjectDir) or $(SolutionDir) VC++ macros and feed it to the script,
# which in turn would write that into Configuration.json file as one of Alias.
# What that alias should be name, since it needs to exist in C++ first
# $(Content) or maybe $(DevContent)
