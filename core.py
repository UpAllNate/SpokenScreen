
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
from typing import Union, Callable
import copy

@NamespaceMethods.register
def quit_if() -> None:
    pass

namespace_reserved_strings = [
    "(", ")", "[", "]", "=", ",", "!", """ ' """, ''' " '''
]

namespace_forbidden = [
    "from", "import"
]

class LOS_TokenTypes(Enum):
    VARIABLE = enum_auto()
    METHOD = enum_auto()
    OPEN_PARENTHESES = enum_auto()
    CLOSE_PARENTHESES = enum_auto()
    OPEN_BRACKET_SQUARE = enum_auto()
    CLOSE_BRACKET_SQUARE = enum_auto()
    ASSIGN = enum_auto()
    COMMA = enum_auto()
    NOT_OPERATOR = enum_auto()
    IMMEDIATE_INTEGER = enum_auto()
    IMMEDIATE_FLOAT = enum_auto()
    SINGLE_QUOTE = enum_auto()
    DOUBLE_QUOTE = enum_auto()
    SETUP = enum_auto()
    GETATTR = enum_auto()

class LOS_ExpressionTypes(Enum):
    ASSIGNMENT = enum_auto()
    METHOD_CALL = enum_auto()

namespace_TokenType_Strings = {}
namespace_TokenType_Strings["("] = LOS_TokenTypes.OPEN_PARENTHESES
namespace_TokenType_Strings[")"] = LOS_TokenTypes.CLOSE_PARENTHESES
namespace_TokenType_Strings["["] = LOS_TokenTypes.OPEN_BRACKET_SQUARE
namespace_TokenType_Strings["]"] = LOS_TokenTypes.CLOSE_BRACKET_SQUARE
namespace_TokenType_Strings["="] = LOS_TokenTypes.ASSIGN
namespace_TokenType_Strings[","] = LOS_TokenTypes.COMMA
namespace_TokenType_Strings["!"] = LOS_TokenTypes.NOT_OPERATOR
namespace_TokenType_Strings[''' " '''] = LOS_TokenTypes.DOUBLE_QUOTE
namespace_TokenType_Strings[""" ' """] = LOS_TokenTypes.SINGLE_QUOTE
namespace_TokenType_Strings["setup"] = LOS_TokenTypes.SETUP

class LOS_Token:
    def __init__(self, type : Union[LOS_TokenTypes, LOS_ExpressionTypes], string : str = None ) -> None:
        self.string = string
        self.type = type

    def __str__(self) -> str:
        try:
            return f"Type: {self.type.name}:: {self.string}"
        except:
            return f"Data class error, backup print content: {self.__dict__}"

class LOS_ExpressionBase(LOS_Token):
    def __init__(self, type: LOS_ExpressionTypes, string: str) -> None:
        super().__init__(string= string, type= type)
        self.start_token_num = None
        self.end_token_num = None
        self.parsing = False
        self.resolved = False
        self.result = None
        self.tokens : list[LOS_Token] = []

class LOS_Expression_Method(LOS_ExpressionBase):
    def __init__(self, method : Callable, string: str) -> None:
        super().__init__(string= string, type= LOS_ExpressionTypes.METHOD_CALL)
        self.start_params_token_num = None
        self.start_params_bracket_level = None
        self.end_params_token_num = None
        self.params : dict = None
        self.method = method
        self.result = None

class LOS_Expression_Assignment(LOS_ExpressionBase):
    def __init__(self, string: str, source_token = None, destination_token = None) -> None:
        super().__init__(string= string, type= LOS_ExpressionTypes.ASSIGNMENT)
        self.source_token = source_token
        self.destination_token = destination_token

class SpokenScreenApplication:

    def __init__(self, file_los : PathElement ) -> None:
        self.file_los : PathElement = file_los
        self.setup_complete = False
        self.namespace_variables = {}
        self.tokens : list[LOS_Token] = []

    # Generate token objects for each substring in the program
    def tokenize_program(self) -> bool:

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

        self.tokens = []

        for token_str in tokens_str:

            # Attempt to parse the token string as a number
            immediate_float = False
            immediate_int = False
            if "." in token_str:
                try:
                    _ = float(token_str)
                    immediate_float = True
                except:
                    pass
            else:
                try:
                    _ = int(token_str)
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

                # And generate the application's variable namespace dictionary
                if token_str not in self.namespace_variables.keys():
                    self.namespace_variables[token_str] = None

            self.tokens.append(LOS_Token(type= token_type, string= token_str))

        success = True

        return success


    def parse_token_expressions(self, tokens : list[LOS_Token]) -> tuple[bool, list[LOS_ExpressionBase]]:

        expressions : list[LOS_ExpressionBase] = []
        parentheses_layer_count = 0
        square_bracket_layer_count = 0
        parsing_complete = False
        
        while not parsing_complete:
            for t_num, token in enumerate(tokens):

                print(f"evaluating token: {token}. There are currently {len(expressions)} expressions.")

                if token.type == LOS_TokenTypes.OPEN_PARENTHESES:
                    parentheses_layer_count += 1
                    print(f"Incrementing parentheses counter, now {parentheses_layer_count}")
                elif token.type == LOS_TokenTypes.CLOSE_PARENTHESES:
                    parentheses_layer_count -= 1
                    print(f"Decrementing parentheses counter, now {parentheses_layer_count}")

                if token.type == LOS_TokenTypes.OPEN_BRACKET_SQUARE:
                    square_bracket_layer_count += 1
                    print(f"Incrementing bracket counter, now {square_bracket_layer_count}")
                elif token.type == LOS_TokenTypes.CLOSE_BRACKET_SQUARE:
                    square_bracket_layer_count -= 1
                    print(f"Decrementing bracket counter, now {square_bracket_layer_count}")

                remaining_tokens = len(tokens) - t_num

                ### Create new expressions based on token type patterns ###

                # Begin parsing an assigment if a variable is followed by =
                if remaining_tokens >= 2:
                    if token.type == LOS_TokenTypes.VARIABLE \
                        and tokens[t_num + 1].type == LOS_TokenTypes.ASSIGN:

                        new_expression = LOS_Expression_Assignment(
                            string=token.string
                        )

                        new_expression.start_token_num = t_num
                        new_expression.destination_token = token
                        new_expression.parsing = True

                        expressions.append(new_expression)

                if token.type == LOS_TokenTypes.METHOD:

                    new_expression = LOS_Expression_Method(
                        method= NamespaceMethods.methods[token.string],
                        string= token.string
                    )

                    new_expression.start_token_num = t_num
                    new_expression.parsing = True

                    expressions.append(new_expression)

                ### Terminatae parsing expressions on acceptable token type patterns ###

                # Assignments resolve simply if the source is an immediate value, variable, or expression token
                for exp in expressions:

                    if not exp.parsing:
                        continue

                    if exp.type == LOS_ExpressionTypes.ASSIGNMENT and t_num == exp.start_token_num + 2:
                        exp : LOS_Expression_Assignment = exp

                        if token.type in [
                            LOS_TokenTypes.IMMEDIATE_FLOAT,
                            LOS_TokenTypes.IMMEDIATE_INTEGER,
                            LOS_TokenTypes.VARIABLE,
                            LOS_ExpressionBase
                        ] \
                        or issubclass(exp.__class__, LOS_ExpressionBase):

                            # Assignment is not resolved if this variable if there's a bracket getattr
                            if remaining_tokens > 2:
                                if tokens[t_num+1].type == LOS_TokenTypes.OPEN_BRACKET_SQUARE:
                                    continue

                            exp.end_token_num = t_num
                            exp.source_token = token
                            exp.parsing = False
                            exp.resolved = True
                            build_str = ""
                            for i in range(t_num - exp.start_token_num + 1):
                                build_str += tokens[i+exp.start_token_num].string
                            exp.string = build_str

                            print(f"Parsing complete for expression {exp.__dict__}, index {t_num}. Started {exp.start_token_num}, length {t_num - exp.start_token_num + 1}")

                    if exp.type == LOS_ExpressionTypes.METHOD_CALL:
                        exp : LOS_Expression_Method

                        if token.type == LOS_TokenTypes.OPEN_PARENTHESES \
                            and exp.start_params_token_num is None:

                            print("Got opening parantheses for method call")

                            exp.start_params_bracket_level = parentheses_layer_count
                            exp.start_params_token_num = t_num + 1

                        if token.type == LOS_TokenTypes.CLOSE_PARENTHESES \
                            and exp.start_params_token_num is not None \
                            and exp.end_params_token_num is None \
                            and exp.start_params_bracket_level == parentheses_layer_count + 1:

                            exp.end_token_num = t_num
                            exp.end_params_token_num = t_num - 1
                            exp.parsing = False
                            build_str = ""
                            for i in range(t_num - exp.start_token_num + 1):
                                build_str += tokens[i+exp.start_token_num].string
                            exp.string = build_str
                            count_tokens = t_num - exp.start_token_num + 1
                            count_param_tokens = exp.end_params_token_num - exp.start_params_token_num + 1

                            print(f"Parsing complete for expression {exp.__dict__}, index {t_num}. Started {exp.start_token_num}, length {count_tokens}")

                            # No parameters
                            if (exp.end_params_token_num - exp.start_params_token_num) == 1:
                                exp.resolved = True
                                exp.parsing = False

                            # Immediate value or variable tokens within
                            if count_param_tokens > 0:

                                for t in range(count_param_tokens):
                                    res = False

                                    # Resolved if only content is an immediate or variable
                                    if tokens[t + exp.start_params_token_num].type in [
                                        LOS_TokenTypes.IMMEDIATE_FLOAT,
                                        LOS_TokenTypes.IMMEDIATE_INTEGER,
                                        LOS_TokenTypes.VARIABLE,
                                    ]:
                                        res = True

                                    # Resolved if 
                                    if tokens[t + exp.start_params_token_num].type in [
                                        LOS_TokenTypes.COMMA,
                                        LOS_ExpressionTypes.ASSIGNMENT
                                    ]:
                                        res = True

                                exp.resolved = res
                                exp.parsing = False
            parsing_complete = True

            new_tokens = copy.deepcopy(tokens)

            for exp in expressions:
                if not exp.resolved:
                    continue

                for t in range(exp.end_token_num - exp.start_token_num + 1):
                    exp.tokens.append(tokens[t + exp.start_token_num])

        return expressions






if __name__ == "__main__":

    mainLOS = PathElement(
        type= PathType.FILE,
        path_obj=Path.joinpath(SSPath.profiles.path_obj, "PokeFR", "main.los")
    )

    app_blueTB = SpokenScreenApplication(mainLOS)

    success = app_blueTB.tokenize_program()

    for t in app_blueTB.tokens:
        print(t.__dict__)
    
    expressions = app_blueTB.parse_token_expressions(app_blueTB.tokens)
    print(f"There are {len(expressions)} expressions")
    for e in expressions:
        print(f"{str(e) :{' '}<90}, resolved: {e.resolved}")