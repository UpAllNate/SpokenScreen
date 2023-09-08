
from pathlib import Path
from common.ss_PathClasses import PathElement, PathType, SSPath
from common.ss_ProfileClasses import ProfileInstance
from common.ss_ColorClasses import Color
import common.ss_Hashing
import common.ss_Image
import common.ss_Pixel
import common.ss_Arithmetic
from common.ss_namespace_methods import NamespaceMethods
from enum import Enum, auto as enum_auto
from typing import Union
import copy

namespace_reserved_strings = [
    "(", ")", "[", "]", "=", ",", "!", """ ' """, ''' " '''
]

namespace_forbidden = [
    "from", "import"
]

class LOS_TokenTypes(Enum):
    VARIABLE = enum_auto()
    METHOD = enum_auto()
    OPEN_BRACKET_PARENTHESES = enum_auto()
    CLOSE_BRACKET_PARENTHESES = enum_auto()
    OPEN_BRACKET_SQUARE = enum_auto()
    CLOSE_BRACKET_SQUARE = enum_auto()
    ASSIGN = enum_auto()
    COMMA = enum_auto()
    NOT_OPERATOR = enum_auto()
    IMMEDIATE_INTEGER = enum_auto()
    IMMEDIATE_FLOAT = enum_auto()
    SINGLE_QUOTE = enum_auto()
    DOUBLE_QUOTE = enum_auto()

class LOS_ExpressionTypes(Enum):
    ASSIGNMENT = enum_auto()
    METHOD_CALL = enum_auto()

namespace_TokenType_Strings = {}
namespace_TokenType_Strings["("] = LOS_TokenTypes.OPEN_BRACKET_PARENTHESES
namespace_TokenType_Strings[")"] = LOS_TokenTypes.CLOSE_BRACKET_PARENTHESES
namespace_TokenType_Strings["["] = LOS_TokenTypes.OPEN_BRACKET_SQUARE
namespace_TokenType_Strings["]"] = LOS_TokenTypes.CLOSE_BRACKET_SQUARE
namespace_TokenType_Strings["="] = LOS_TokenTypes.ASSIGN
namespace_TokenType_Strings[","] = LOS_TokenTypes.COMMA
namespace_TokenType_Strings["!"] = LOS_TokenTypes.NOT_OPERATOR
namespace_TokenType_Strings[''' " '''] = LOS_TokenTypes.DOUBLE_QUOTE
namespace_TokenType_Strings[""" ' """] = LOS_TokenTypes.SINGLE_QUOTE

class LOS_Token:
    def __init__(self, type : Union[LOS_TokenTypes, LOS_ExpressionTypes], string : str = None ) -> None:
        self.string = string
        self.type = type

    def __str__(self) -> str:
        return f"Type: {self.type.name}:: {self.string}"

class LOS_ExpressionBase(LOS_Token):
    def __init__(self, string: str, type: LOS_TokenTypes | LOS_ExpressionTypes) -> None:
        super().__init__(string, type)
        self.start_token_num = None
        self.end_token_num = None
        self.parsing = False
        self.resolved = False
        self.dependencies = []

class LOS_Expression_Function(LOS_ExpressionBase):
    def __init__(self, string: str, type: LOS_ExpressionTypes, method : function) -> None:
        super().__init__(string, type)
        self.start_params_token_num = None
        self.start_params_bracket_level = None
        self.end_params_token_num = None
        self.params : dict = None
        self.method = method
        self.result = None

class LOS_Expression_Assignment(LOS_ExpressionBase):
    def __init__(self, string: str, type: LOS_ExpressionTypes, source_token = None, destination_token = None) -> None:
        super().__init__(string, type)
        self.source_token = source_token
        self.destination_token = destination_token

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

                if prog_str == "":
                    prog_str = line
                else:
                    prog_str += " " + line

        # Separate the operators and punctuation
        for c in namespace_reserved_strings:
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

            # Attempt to parse the token string as a number
            immediate_float = False
            immediate_int = False
            if "." in token_str:
                try:
                    immediate_float = True
                except:
                    pass
            else:
                try:
                    immediate_int = True
                except:
                    pass

            if token_str in namespace_forbidden:
                continue

            elif token_str in namespace_TokenType_Strings.keys():
                token_type = namespace_TokenType_Strings[token_str]

            elif token_str in NamespaceMethods.methods.keys():
                token_type = LOS_TokenTypes.METHOD

            elif immediate_float:
                token_type = LOS_TokenTypes.IMMEDIATE_FLOAT

            elif immediate_int:
                token_type = LOS_TokenTypes.IMMEDIATE_INTEGER

            else:
                token_type = LOS_TokenTypes.VARIABLE

                if token_str not in self.namespace_variables:
                    self.namespace_variables[token_str] = None

            program_tokens.append(LOS_Token(token_str, token_type))

        success = True

        return success, program_tokens


    def parse_token_expressions(tokens : list[LOS_Token]) -> None:

        expressions : list[LOS_ExpressionBase] = []
        parentheses_layer_count = 0
        square_bracket_layer_count = 0

        for t_num in range(len(tokens)):

            if tokens[t_num].type == LOS_TokenTypes.OPEN_BRACKET_PARENTHESES:
                parentheses_layer_count += 1
            elif tokens[t_num].type == LOS_TokenTypes.CLOSE_BRACKET_PARENTHESES:
                parentheses_layer_count -= 1

            if tokens[t_num].type == LOS_TokenTypes.OPEN_BRACKET_SQUARE:
                square_bracket_layer_count += 1
            elif tokens[t_num].type == LOS_TokenTypes.CLOSE_BRACKET_SQUARE:
                square_bracket_layer_count -= 1

            remaining_tokens = len(tokens) - t_num

            ### Create new expressions based on token type patterns ###

            # Begin parsing an assigment if a variable is followed by =
            if remaining_tokens >= 2:
                if tokens[t_num].type == LOS_TokenTypes.VARIABLE \
                    and tokens[t_num + 1].type == LOS_TokenTypes.ASSIGN:

                    new_expression = LOS_Expression_Assignment(type=LOS_ExpressionTypes.ASSIGNMENT)
                    new_expression.start_token_num = t_num
                    new_expression.destination_token = tokens[t_num]
                    new_expression.parsing = True

                    expressions.append(new_expression)

            if tokens[t_num].type == LOS_TokenTypes.METHOD:

                new_expression = LOS_Expression_Function(type=LOS_ExpressionTypes.METHOD_CALL)
                new_expression.start_token_num = t_num

            ### Terminatae parsing expressions on acceptable token type patterns ###

            # Assignments resolve simply if the source is an immediate value or variable
            for exp in expressions:

                if exp.parsing and exp.type == LOS_ExpressionTypes.ASSIGNMENT:
                    exp_ass : LOS_Expression_Assignment = exp

                    if tokens[t_num].type in [
                        LOS_TokenTypes.IMMEDIATE_FLOAT,
                        LOS_TokenTypes.IMMEDIATE_INTEGER,
                        LOS_TokenTypes.VARIABLE
                    ]:
                        exp_ass.end_token_num = t_num
                        exp_ass.source_token = tokens[t_num]
                        exp_ass.parsing = False
                        exp_ass.resolved = True
                        exp_ass.string = tokens[exp.start_token_num : t_num + 1]

                if exp.parsing and exp.type == LOS_ExpressionTypes.METHOD_CALL:
                    exp : LOS_Expression_Function

                    if tokens[t_num].type == LOS_TokenTypes.OPEN_BRACKET_PARENTHESES \
                        and exp.start_params_token_num is None:

                        exp.start_params_bracket_level = parentheses_layer_count
                        exp.start_params_token_num = t_num + 1

                    if tokens[t_num].type == LOS_TokenTypes.CLOSE_BRACKET_PARENTHESES \
                        and exp.start_params_token_num is not None \
                        and exp.end_params_token_num is None \
                        and exp.start_params_bracket_level == parentheses_layer_count:

                        exp.end_token_num = t_num
                        exp.end_params_token_num = t_num - 1
                        exp.parsing = False
                        exp.string = tokens[exp.start_token_num : t_num + 1]

                        # No parameters
                        if (exp.end_params_token_num - exp.start_params_token_num) == 1:
                            exp.resolved = True

                        # Immediate value or variable token within
                        if (exp.end_params_token_num - exp.start_params_token_num) == 2 \
                            and tokens[t_num - 1].type in [
                                LOS_TokenTypes.IMMEDIATE_FLOAT,
                                LOS_TokenTypes.IMMEDIATE_INTEGER,
                                LOS_TokenTypes.VARIABLE
                            ]:
                            exp.resolved = True






if __name__ == "__main__":

    mainLOS = PathElement(
        type= PathType.FILE,
        path_obj=Path.joinpath(SSPath.profiles.path_obj, "PokeFR", "main.los")
    )

    app_blueTB = SpokenScreenApplication(mainLOS)

    success, tokens = app_blueTB.tokenize_program()

    for t in tokens:
        print(t)