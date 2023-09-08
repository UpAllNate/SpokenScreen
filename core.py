
from pathlib import Path
from common.ss_PathClasses import PathElement, PathType, SSPath
from common.ss_ProfileClasses import ProfileInstance
from common.ss_ColorClasses import Color
from common.ss_namespace_methods import NamespaceMethods
from enum import Enum, auto as enum_auto

namespace_operators = [
    "(", ")", "[", "]", ",", ".", "=", "+", "-", "/", ":", ";", "!"
]

namespace_forbidden = [
    "from", "import"
]

class LOS_TokenTypes(Enum):
    OPERATOR = enum_auto()
    VARIABLE = enum_auto()
    METHOD = enum_auto()

class LOS_Token:
    def __init__(self, string : str, type : LOS_TokenTypes) -> None:
        self.string = string
        self.type = type

class SpokenScreenApplication:

    def __init__(self, file_los : PathElement ) -> None:
        self.file_los : PathElement = file_los
        self.setup_complete = False
        self.namespace_variables = {}

    def tokenize_program(self) -> tuple[bool,  list[LOS_Token]]:

        success, prog_str = False, ""

        if not self.file_los.detect() or self.file_los.type is not PathType.FILE:
            return success, prog_str

        with open(self.file_los.path_str, 'r') as los:

            for line in los:
                
                # Purge comments and white space
                if "#" in line:
                    line_parts = [p.strip() for p in line.split("#")]
                    if line_parts[0] == "":
                        continue
                    else:
                        line = line_parts[0]
                else:
                    line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # line += " @line_end "

                if prog_str == "":
                    prog_str = line
                else:
                    prog_str += " " + line
        
        # Separate the operators and punctuation
        for c in namespace_operators:
            prog_str = prog_str.replace(c, f" {c} ")

        # Reduce all spaces to single space
        while "  " in prog_str:
            prog_str = prog_str.replace("  ", " ")

        # Split by spaces
        tokens_str = prog_str.split(" ")
        
        # Generate token objects for each substring in the program
        # And generate the application's variable namespace dictionary
        program_tokens : list[LOS_Token] = []

        for token_str in tokens_str:

            if token_str in namespace_forbidden:
                continue

            elif token_str in namespace_operators:
                program_tokens.append(LOS_Token(token_str, LOS_TokenTypes.OPERATOR))

            elif token_str in NamespaceMethods.methods.keys():
                program_tokens.append(LOS_Token(token_str, LOS_TokenTypes.METHOD))

            else:
                program_tokens.append(LOS_Token(token_str, LOS_TokenTypes.VARIABLE))

                if token_str not in self.namespace_variables:
                    self.namespace_variables[token_str] = None

        success = True

        return success, program_tokens


    def parse_program(prog : list[LOS_Token]) -> None:
        prog = prog.split(" ")

        scanning_setup = False
        parsing_var_Color = False

        # # Detect when scanning lines within setup (executes once)
        # if line == "@setup_start":
        #     scanning_setup = True
        #     continue

        # if line == "@setup_end" and scanning_setup:
        #     scanning_setup = False
        #     self.setup_complete = True
        #     continue

        # # Ignore setup lines if setup has already been parsed
        # if scanning_setup and self.setup_complete:
        #     continue

        # # Detect if there is an assignment in this line
        # if "=" in line:

        #     # Detect if this is a function call
        #     if "(" in line:

    
if __name__ == "__main__":
    
    mainLOS = PathElement(
        type= PathType.FILE,
        path_obj=Path.joinpath(SSPath.profiles.path_obj, "PokeFR", "main.los")
    )

    app_blueTB = SpokenScreenApplication(mainLOS)

    success, prog = app_blueTB.tokenize_program()
    print(prog)