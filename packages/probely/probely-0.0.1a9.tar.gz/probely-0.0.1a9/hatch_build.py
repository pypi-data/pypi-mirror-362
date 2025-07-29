from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    print("hello world")


#     def initialize(self, version, build_data):
#         print(build_data["version"])
#         with open("README.md") as f:
#             readme = f.read()
#             if "pip probely install *" not in readme:
#                 raise Exception(
#                     "README.md must contain a line with 'pip probely install *'"
#                 )
#         print("hello world")
