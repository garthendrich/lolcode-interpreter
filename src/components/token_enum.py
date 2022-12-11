class TOKEN:
    LINEBREAK = "linebreak"
    CODE_DELIMITER = "code delimiter"
    COMMENT_KEYWORD = "comment keyword"
    MULTILINE_COMMENT_DELIMITER = "multiline comment delimiter"
    VARIABLE_DECLARATION = "variable declaration"
    VARIABLE_ASSIGNMENT = "variable assignment"
    IT_VARIABLE = "IT"
    ADDITION_OPERATION = "addition operation"
    SUBTRACTION_OPERATION = "subtraction operation"
    MULTIPLICATION_OPERATION = "multiplication operation"
    QUOTIENT_OPERATION = "quotient operation"
    MODULO_OPERATION = "modulo operation"
    MAX_OPERATION = "max operation"
    MIN_OPERATION = "min operation"
    AND_OPERATION = "and operation"
    OR_OPERATION = "or operation"
    XOR_OPERATION = "xor operation"
    NOT_OPERATION = "not operation"
    INFINITE_ARITY_AND_OPERATION = "infinite arity and operation"
    INFINITE_ARITY_OR_OPERATION = ("infinite arity or operation",)
    EQUAL_TO_OPERATION = "equal to operation"
    NOT_EQUAL_TO_OPERATION = "not equal to operation"
    BREAK_STATEMENT = "break statement"
    GREATER_THAN_OR_EQUAL_TO_OPERATION = EQUAL_TO_OPERATION + MAX_OPERATION
    GREATER_THAN = NOT_EQUAL_TO_OPERATION + MAX_OPERATION
    LESS_THAN_OR_EQUAL_TO_OPERATION = EQUAL_TO_OPERATION + MIN_OPERATION
    LESS_THAN = NOT_EQUAL_TO_OPERATION + MIN_OPERATION

    CONCATENATION_OPERATION = "concantenation operaion"
    EXPLICIT_TYPECASTING_KEYWORD = "explicit typecasting keyword"
    OPTIONAL_A_KEYWORD = "optional A keyword"
    OPERAND_SEPARATOR = "operand seperator"
    INFINITE_ARITY_DELIMITER = "infinite arity delimiter"
    RECASTING_KEYWORD = "re-casting keyword"
    OUTPUT_KEYWORD = "output keyword"
    INPUT_KEYWORD = "input keyword"
    IF_ELSE_DELIMITER = "if-else delimiter"
    IF_STATEMENT_KEYWORD = "if statement keyword"
    ELSE_IF_STATEMENT_KEYWORD = "else-if statement keyword"
    ELSE_STATEMENT_KEYWORD = "else statement keyword"
    FLOW_CONTROL_STATEMENTS_DELIMITER = "flow-control statements delimiter"
    SWITCH_CASE_STATEMENT_DELIMITER = "switch-case statement delimiter"
    CASE_KEYWORD = "case keyword"
    DEFAULT_CASE_KEYWORD = "default case keyword"
    LOOP_DECLARATION_AND_DELIMITER = "loop declaration and delimiter"
    INCREMENT_KEYWORD = "increment keyword"
    DECREMENT_KEYWORD = "decrement keyword"
    KEYWORD_IN_LOOP = "keyword in loop"
    LOOP_CONDITION_KEYWORD = "loop condition keyword"
    LOOP_DELIMITER = "loop delimiter"
    FLOAT_LITERAL = "float literal"
    INTEGER_LITERAL = "integer literal"
    STRING_LITERAL = "string literal"
    BOOL_LITERAL = "bool literal"
    TYPE_LITERAL = "type literal"
    VARIABLE_IDENTIFIER = "variable identifier"
    LOOP_IDENTIFIER = "loop identifier"
