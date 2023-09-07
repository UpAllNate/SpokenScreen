
from pathlib import Path
from common.ss_PathClasses import PathElement, PathType, SSPath
from common.ss_CoreClasses import FunReturn
from common.ss_ProfileClasses import ProfileInstance

class SpokenScreenApplication:

    def __init__(self, file_los : PathElement ) -> None:
        self.file_los : PathElement = file_los
        self.setup_complete = False
        self.los_dict = {}

    def extract_program(self) -> tuple[bool,  str]:

        success, prog = False, ""

        if not self.file_los.detect() or self.file_los.type is not PathType.FILE:
            return success, prog

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

                if prog == "":
                    prog = line
                else:
                    prog += " " + line
        
        for c in ["[", "]", "(", ")", ","]:
            prog = prog.replace(c, f" {c} ")

        while "  " in prog:
            prog = prog.replace("  ", " ")

        prog = prog.split(" ")
            
        success = True

        return success, prog

    def execute_program(prog : str) -> None:
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

    success, prog = app_blueTB.extract_program()
    print(prog)