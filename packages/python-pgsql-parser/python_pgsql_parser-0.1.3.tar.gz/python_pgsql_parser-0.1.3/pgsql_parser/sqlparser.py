import re
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any, Generator


class TokenType(Enum):
    HIDDEN = 0
    KEYWORD = 1
    IDENTIFIER = 2
    QUOTED_IDENTIFIER = 3
    STRING_LITERAL = 4
    NUMERIC_LITERAL = 5
    OPERATOR = 6
    PUNCTUATION = 7
    COMMENT = 8
    BLOCK_CONTROL = 9


class Token:
    __slots__ = ('token_type', 'value', 'position')

    def __init__(self, token_type: TokenType, value: str, position: int):
        self.token_type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.token_type.name}, '{self.value}', pos={self.position})"


class SQLLexer:
    def __init__(self):
        self.keywords = [
            # Data types
            'INT', 'INTEGER', 'SMALLINT', 'BIGINT', 'SERIAL', 'BIGSERIAL',
            'VARCHAR', 'CHARACTER', 'VARYING',  'CHAR', 'TEXT', 'BOOLEAN', 'NUMERIC', 'DECIMAL',
            'REAL', 'FLOAT', 'DOUBLE', 'PRECISION', 'DATE', 'TIME', 'TIMESTAMP',
            'INTERVAL', 'JSON', 'JSONB', 'UUID', 'BYTEA',
            # DDL commands
            'CREATE', 'DROP', 'ALTER', 'TABLE', 'COLUMN', 'CONSTRAINT',
            'INDEX', 'SEQUENCE', 'VIEW', 'TRIGGER', 'FUNCTION', 'SCHEMA',
            'DOMAIN', 'TYPE', 'EXTENSION', 'DATABASE', 'SERVER', 'FOREIGN',
            'DATA', 'WRAPPER', 'ROLE', 'USER', 'GROUP',
            # Constraints
            'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'UNIQUE', 'CHECK',
            'DEFAULT', 'NOT', 'NULL', 'CONSTRAINT',
            # DML commands
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'INTO',
            'VALUES', 'SET', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT',
            'OFFSET', 'RETURNING',
            # Joins
            'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'USING',
            # Conditionals
            'AND', 'OR', 'BETWEEN', 'IN', 'LIKE', 'ILIKE', 'IS', 'EXISTS',
            # Functions
            'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'DISTINCT',
            # Control
            'BEGIN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
            # Other
            'AS', 'ASC', 'DESC', 'WITH', 'WITHOUT', 'TIME', 'ZONE', 'IF',
            'EXISTS', 'CASCADE', 'RESTRICT', 'ADD', 'RENAME', 'TO', 'COLUMN',
            # PostgreSQL specific
            'TEMPORARY', 'TEMP', 'VIEW', 'MATERIALIZED', 'UNLOGGED', 'INDEX',
            'CONCURRENTLY', 'USING', 'UNIQUE', 'CLUSTER', 'WITH'
        ]
        # Sort keywords by length (descending) for regex priority
        self.keywords.sort(key=len, reverse=True)
        # keyword_pattern = r'\b(?i:' + '|'.join(self.keywords) + r')\b'

        self.token_specs = [
            (TokenType.COMMENT, r'--[^\r\n]*|/\*[\s\S]*?\*/'),
            (TokenType.STRING_LITERAL, r"'(?:''|[^'])*'"),
            (TokenType.QUOTED_IDENTIFIER, r'"(?:[^"]|"")*"'),
            (TokenType.NUMERIC_LITERAL,
             r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'),
            (TokenType.OPERATOR,
             r'\|\||\*\*|->>|->|#>>|#>|::|!=|>=|<=|<>|[-+*/%<>=~!@#^&|?]'),
            (TokenType.PUNCTUATION, r'[(),;.]'),
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            (TokenType.BLOCK_CONTROL, r'[$]{2}'),
        ]
        # Build master regex with DOTALL to handle multi-line tokens
        regex_parts = [f'(?P<{tok.name}>{pat})' for tok,
                       pat in self.token_specs]
        self.regex = re.compile('|'.join(regex_parts),
                                re.DOTALL | re.IGNORECASE)

        # Set for quick keyword lookups (case-insensitive)
        self.keyword_set = {kw.lower() for kw in self.keywords}

    def tokenize(self, sql: str, include_space: bool = False) -> List[Token]:
        tokens = []
        pos = 0
        line_start = 0
        line_num = 1

        while pos < len(sql):
            # Handle whitespace and newlines
            if sql[pos].isspace():
                if include_space is True:
                    # print(Token(TokenType.HIDDEN, sql[pos], pos))
                    tokens.append(Token(TokenType.HIDDEN, sql[pos], pos))
                if sql[pos] == '\n':
                    line_start = pos + 1
                    line_num += 1
                pos += 1
                continue

            # Try to match token patterns
            match = self.regex.match(sql, pos)
            if not match:
                col = pos - line_start + 1
                raise ValueError(
                    f"Syntax error at line {line_num}, col {col}: {sql[pos:pos+20]!r}")

            # Get matched token type and value
            token_type_name = match.lastgroup
            value = match.group(token_type_name)
            token_type = TokenType[token_type_name]

            # Convert unquoted identifiers to keywords if they match
            if token_type == TokenType.IDENTIFIER and value.lower() in self.keyword_set:
                token_type = TokenType.KEYWORD
            token = Token(token_type, value, pos)
            # print(token)
            tokens.append(token)
            pos = match.end()

        return tokens

    def split_sql_statements(self, sql: str) -> List[str]:
        """Split SQL script into individual statements"""
        # Remove comments
        sql = re.sub(r'--.*?$', '', sql, flags=re.MULTILINE)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)

        # Split on semicolons that are outside of quotes and parentheses
        tokens = self.tokenize(sql.strip(), include_space=True)
        statements = []
        current = []
        in_blocks = []

        for token in tokens:
            if token.token_type == TokenType.BLOCK_CONTROL and not in_blocks:
                in_blocks.append(True)
                current.append(token)
            elif token.token_type == TokenType.BLOCK_CONTROL and in_blocks:
                in_blocks.pop()
                current.append(token)
            elif in_blocks:
                current.append(token)
            elif not in_blocks and token.token_type == TokenType.PUNCTUATION and token.value == ';':

                statement = "".join([tok.value for tok in current]).strip()
                if statement:
                    statements.append(statement)
                current = []
            else:
                current.append(token)

        final_stmt = "".join([tok.value for tok in current]).strip()
        if final_stmt:
            statements.append(final_stmt)
        return statements

# Parser Implementation


class Column:
    __slots__ = ('name', 'data_type', 'char_length', 'numeric_precision',
                 'numeric_scale', 'nullable', 'default_value', 'is_primary',
                 'primary_key_position', 'foreign_key_ref', 'constraints')

    def __init__(self, name: str,
                 data_type: Optional[str] = None,                 
                 nullable: bool = True,
                 default_value: Optional[str] = None,
                 is_primary: bool = False):
        self.name = name
        self.data_type: Optional[str] = data_type
        self.nullable: bool = nullable
        self.default_value: Optional[str] = default_value
        self.is_primary: bool = is_primary
        self.char_length: Optional[int] = None
        self.numeric_precision: Optional[int] = None
        self.numeric_scale: Optional[int] = None        
        self.primary_key_position: Optional[int] = None
        self.foreign_key_ref: Optional[Tuple[str, str, str]] = None
        self.constraints: List[Dict] = []  # For column-level constraints

    def __repr__(self):
        return (f"Column(name={self.name!r}, type={self.data_type!r}, "
                f"nullable={self.nullable})")


class PrimaryKey:
    __slots__ = ('name', 'columns')

    def __init__(self, name: Optional[str], columns: List[str]):
        self.name = name
        self.columns = columns

    def __repr__(self):
        return f"PrimaryKey(name={self.name!r}, columns={self.columns})"


class ForeignKey:
    __slots__ = ('name', 'columns', 'ref_table', 'ref_columns')

    def __init__(self, name: Optional[str], columns: List[str],
                 ref_table: str, ref_columns: List[str]):
        self.name = name
        self.columns = columns
        self.ref_table = ref_table
        self.ref_columns = ref_columns

    def __repr__(self):
        return (f"ForeignKey(name={self.name!r}, columns={self.columns}, "
                f"ref_table={self.ref_table!r}, ref_columns={self.ref_columns})")


class Constraint:
    __slots__ = ('name', 'ctype', 'expression', 'columns')

    def __init__(self, name: str, ctype: str,
                 expression: Optional[str] = None,
                 columns: Optional[List[str]] = None):
        self.name = name
        self.ctype = ctype  # 'CHECK', 'UNIQUE', 'NOT NULL', etc.
        self.expression = expression
        self.columns = columns or []

    def __repr__(self):
        return f"Constraint({self.ctype}, name={self.name!r}, cols={self.columns})"


class Index:
    __slots__ = ('name', 'table', 'columns', 'is_unique', 'method')

    def __init__(self, name: str, table: str, columns: List[str],
                 is_unique: bool = False, method: Optional[str] = None):
        self.name = name
        self.table = table
        self.columns = columns
        self.is_unique = is_unique
        self.method = method

    def __repr__(self):
        return f"Index(name={self.name!r}, table={self.table}, columns={self.columns})"


class Table:
    __slots__ = ('database', 'schema', 'name', 'table_type', 'columns',
                 'primary_key', 'foreign_keys', 'constraints', 'is_view',
                 'view_definition', 'is_materialized')

    def __init__(self, name: str,
                 schema: Optional[str] = None,
                 database: Optional[str] = None,
                 table_type: str = 'TABLE'                 
                 ):
        self.database = database
        self.schema = schema
        self.name = name
        self.table_type = table_type
        self.primary_key = None
        self.columns: Dict[str, Column] = {}
        self.foreign_keys: List[ForeignKey] = []
        self.constraints: List[Constraint] = []
        self.is_view = False
        self.view_definition: Optional[str] = None
        self.is_materialized = False
        

    def add_column(self, column: Column):
        print("Adding column (281)", column)
        if isinstance(column, ForeignKey):
            self.foreign_keys.append(column)
        elif isinstance(column, PrimaryKey):
            self.primary_key = column
        else:
            self.columns[column.name] = column
        print("Added column (288)", self.columns)

    def get_qualified_name(self) -> str:
        parts = []
        if self.database:
            parts.append(self.database)
        if self.schema:
            parts.append(self.schema)
        parts.append(self.name)
        return '.'.join(parts)

    def __repr__(self):
        return (f"Table(name={self.get_qualified_name()}, type={self.table_type}, "
                f"columns={len(self.columns)}, pkey={self.primary_key!r})")


class SQLParser:
    def __init__(self):
        self.lexer = SQLLexer()
        self.tokens: List[Token] = []
        self.current = 0
        self.current_table: Optional[Table] = None
        self.tables: Dict[str, Table] = {}
        self.indexes: Dict[str, Index] = {}
        self.statements: List[str] = []

    def reset(self):
        self.tokens: List[Token] = []
        self.current = 0
        self.current_table: Optional[Table] = None
        self.tables: Dict[str, Table] = {}
        self.indexes: Dict[str, Index] = {}
        self.statements: List[str] = []
        
    def parse_script(self, sql_script: str) -> None:
        """Parse entire SQL script"""
        self.statements = self.lexer.split_sql_statements(sql_script)
        for stmt in self.statements:
            self.parse_statement(stmt)

    def statement_generator(self, sql_script: str) -> Generator[str, None, None]:
        """Generator to iterate through SQL statements"""
        statements = self.lexer.split_sql_statements(sql_script)
        for stmt in statements:
            yield stmt

    def parse_statement(self, sql: str) -> Optional[Table]:
        """Parse a single SQL statement"""
        self.tokens = self.lexer.tokenize(sql)
        for tok in self.tokens:
            print(tok)

        self.current = 0
        try:
            if self.match('CREATE'):
                return self.parse_create()
            elif self.match('ALTER'):
                self.parse_alter()
            elif self.match('DROP'):
                # Handle DROP statements if needed
                pass
        except Exception as e:
            import traceback
            traceback.print_exception(e)
            # Skip statements that cause parsing errors
            pass

        return None

    def parse_create(self) -> Optional[Table]:
        # CREATE [OR REPLACE] [TEMP|TEMPORARY] [TABLE|VIEW|MATERIALIZED VIEW] [IF NOT EXISTS] table_name
        is_or_replace = self.match('OR')
        if is_or_replace:
            self.consume('REPLACE', "Expected 'REPLACE' after 'OR'")

        table_type = 'TABLE'
        is_temp = False
        is_materialized = False
        is_view = False

        if self.match('TEMP', 'TEMPORARY'):
            is_temp = True

        if self.match('MATERIALIZED'):
            is_materialized = True
            table_type = 'MATERIALIZED VIEW'
            self.consume('VIEW', "Expected 'VIEW' after 'MATERIALIZED'")
        elif self.match('VIEW'):
            is_view = True
            table_type = 'VIEW'
        else:
            # Default to TABLE
            self.consume('TABLE', "Expected TABLE, VIEW, or MATERIALIZED VIEW")

        # Skip IF NOT EXISTS
        if self.match('IF'):
            self.consume('NOT', "Expected 'NOT' after 'IF'")
            self.consume('EXISTS', "Expected 'EXISTS' after 'NOT'")

        # Parse table name (could be schema-qualified)
        table_name, schema, database = self.parse_object_name()
        print("DEBUG (377)", table_name, schema, database)
        # Create table object
        table = self.get_table(table_name, schema, database)
        print("DEBUG (395)", table)
        if table is None:
            table = Table(
                name=table_name,
                schema=schema,
                database=database,
                table_type=table_type
            )
            print("DEBUG (403)", table, table.foreign_keys)
            self.add_table(table)

        # import pdb;pdb.set_trace()
        table.is_view = is_view or is_materialized
        table.is_materialized = is_materialized
        if is_temp:
            table.table_type = 'TEMPORARY ' + table.table_type

        self.current_table = table
        print("411", table.foreign_keys)
        print("412", self.current_table.foreign_keys)
        # Handle different create types
        if is_view:
            self.parse_create_view()
        else:
            # Parse table definition
            if self.match('('):
                self.parse_table_elements()
                self.consume(')', "Expected ')' after table definition")
                if (self.current_table.primary_key is None
                        and self.current_table.columns):
                    pk_cols = [
                        col.name for col in self.current_table.columns.values() if col.is_primary]
                    if pk_cols:
                        self.current_table.primary_key = PrimaryKey(
                            None, pk_cols)

            elif self.match('AS'):
                # CREATE TABLE AS SELECT
                table.view_definition = self.parse_remaining()

        # Handle additional table options
        while not self.is_at_end():
            if self.match(';'):
                break
            self.advance()

        return table

    def parse_create_view(self):
        """Parse CREATE VIEW statement"""
        # [COLUMNS] or AS SELECT
        if self.match('('):
            # Parse column list
            while not self.check(')') and not self.is_at_end():
                col_name = self.consume_identifier()
                self.current_table.add_column(Column(col_name))
                self.match(',')
            self.consume(')', "Expected ')' after column list")

        if self.match('WITH'):
            # WITH options
            while not self.match('AS') and not self.is_at_end():
                self.advance()

        if self.match('AS'):
            # Store view definition
            self.current_table.view_definition = self.parse_remaining()

    def parse_alter(self):
        """Parse ALTER TABLE statement"""
        self.consume('TABLE', "Expected TABLE after ALTER")

        # Parse table name
        table_name, schema, database = self.parse_object_name()
        table = self.get_table(table_name, schema, database)
        if table is None:
            # Create new table if not exists
            table = Table(table_name, schema, database)
            self.add_table(table)

        self.current_table = table

        # Parse ALTER operations
        while not self.is_at_end() and not self.check(';'):
            if self.match('ADD'):
                self.parse_alter_add()
            elif self.match('DROP'):
                self.parse_alter_drop()
            elif self.match('ALTER'):
                self.parse_alter_column()
            elif self.match('RENAME'):
                self.parse_alter_rename()
            else:
                self.advance()

    def parse_alter_add(self):
        """Parse ADD operations in ALTER TABLE"""
        if self.match('CONSTRAINT'):
            self.parse_constraint()
        elif self.match('PRIMARY'):
            self.parse_primary_key()
        elif self.match('FOREIGN'):
            self.parse_foreign_key()
        elif self.match('UNIQUE'):
            self.parse_unique_constraint()
        elif self.match('CHECK'):
            self.parse_check_constraint()
        elif self.match('COLUMN'):
            col_name = self.consume_identifier()
            column = Column(col_name)
            self.current_table.add_column(column)
            self.parse_column_definition(column)
        else:
            # Might be a column without COLUMN keyword
            if self.check(TokenType.IDENTIFIER) or self.check(TokenType.QUOTED_IDENTIFIER):
                col_name = self.consume_identifier()
                column = Column(col_name)
                self.current_table.add_column(column)
                self.parse_column_definition(column)

    def parse_alter_drop(self):
        """Parse DROP operations in ALTER TABLE"""
        if self.match('CONSTRAINT'):
            constr_name = self.consume_identifier()
            # Remove constraint from table
            self.current_table.constraints = [
                c for c in self.current_table.constraints if c.name != constr_name
            ]
        elif self.match('COLUMN'):
            col_name = self.consume_identifier()
            if col_name in self.current_table.columns:
                del self.current_table.columns[col_name]
        elif self.match('PRIMARY'):
            self.consume('KEY', "Expected KEY after PRIMARY")
            self.current_table.primary_key = None
            # Reset primary key flags in columns
            for col in self.current_table.columns.values():
                col.is_primary = False
                col.primary_key_position = None

    def parse_alter_column(self):
        """Parse ALTER COLUMN operations"""
        self.consume('COLUMN', "Expected COLUMN after ALTER")
        col_name = self.consume_identifier()

        if col_name not in self.current_table.columns:
            # Add column if not exists
            self.current_table.add_column(Column(col_name))

        column = self.current_table.columns[col_name]

        # Parse column alterations
        while not self.is_at_end() and not self.check(';'):
            if self.match('SET'):
                if self.match('NOT'):
                    self.consume('NULL', "Expected NULL after NOT")
                    column.nullable = False
                elif self.match('DATA'):
                    self.consume('TYPE', "Expected TYPE after DATA")
                    data_type, _ = self.parse_data_type()
                    column.data_type = data_type
                else:
                    self.advance()
            elif self.match('DROP'):
                if self.match('NOT'):
                    self.consume('NULL', "Expected NULL after NOT")
                    column.nullable = True
                elif self.match('DEFAULT'):
                    column.default_value = None
                else:
                    self.advance()
            else:
                self.advance()

    def parse_alter_rename(self):
        """Parse RENAME operations in ALTER TABLE"""
        if self.match('COLUMN'):
            old_name = self.consume_identifier()
            self.consume('TO', "Expected TO after column name")
            new_name = self.consume_identifier()

            if old_name in self.current_table.columns:
                column = self.current_table.columns.pop(old_name)
                column.name = new_name
                self.current_table.columns[new_name] = column
        elif self.match('TO'):
            new_name = self.consume_identifier()
            self.current_table.name = new_name
            # Update table key
            self.tables.pop(self.current_table.get_qualified_name(), None)
            self.add_table(self.current_table)

    def parse_table_elements(self):
        """Parse elements inside table definition (columns, constraints)"""
        while not self.check(')') and not self.is_at_end():
            if self.match('CONSTRAINT'):
                self.parse_constraint()
            elif self.check(TokenType.QUOTED_IDENTIFIER) or self.check(TokenType.IDENTIFIER):
                self.parse_column_definition()
            elif self.match('PRIMARY'):
                self.parse_primary_key()
            elif self.match('FOREIGN'):
                self.parse_foreign_key()
            elif self.match('UNIQUE'):
                self.parse_unique_constraint()
            elif self.match('CHECK'):
                self.parse_check_constraint()
            else:
                self.advance()

            # Skip commas between elements
            self.match(',')

    def parse_column_definition(self, column: Optional[Column] = None):
        """Parse a column definition"""
        # print("---------col--------------", self.peek())
        if column is None:
            # Parse column name
            col_name = self.consume_identifier()
            column = Column(col_name)
            # print("Adding column", column)
            self.current_table.add_column(column)

        # Parse data type
        data_type, params = self.parse_data_type()
        column.data_type = data_type

        # Handle type parameters
        if data_type in ['varchar', 'char', 'character', 'character varying'] and params:
            column.char_length = int(params[0])
        elif data_type in ['numeric', 'decimal', 'number'] and params:
            column.numeric_precision = int(
                params[0]) if len(params) > 0 else None
            column.numeric_scale = int(params[1]) if len(params) > 1 else None

        # Parse column constraints
        if self.check(',') or self.check(')') or self.is_at_end():
            return
        if self.match('CONSTRAINT'):
            constr_name = self.consume_identifier()
        else:
            constr_name = None

        while not (self.check(',') or self.check(')') or self.is_at_end()):
            #print("DEBUG-----", self.peek())
            if self.match('PRIMARY'):
                self.consume('KEY', "Expected KEY after PRIMARY")
                column.is_primary = True
                column.primary_key_position = 1
                # Add to constraint list
                if constr_name is not None:
                    self.current_table.constraints.append(
                        Constraint(constr_name, 'PRIMARY KEY', columns=[column.name]))
            elif self.match('REFERENCES'):
                print("646", self.current_table.foreign_keys)
                self.parse_foreign_key_ref(column, constr_name)
            elif self.match('NOT'):
                self.consume('NULL', "Expected NULL after NOT")
                column.nullable = False
                # Add to constraint list
                if constr_name:
                    self.current_table.constraints.append(
                        Constraint(constr_name, 'NOT NULL', columns=[column.name]))
            elif self.match('NULL'):
                column.nullable = True
            elif self.match('DEFAULT'):
                column.default_value = self.parse_default_value()
            elif self.match('UNIQUE'):
                # Add unique constraint
                if constr_name:
                    self.current_table.constraints.append(
                        Constraint(constr_name, 'UNIQUE', columns=[column.name]))
            elif self.match('CHECK'):
                expr = self.parse_expression()
                if constr_name:
                    self.current_table.constraints.append(
                        Constraint(constr_name, 'CHECK', expression=expr))
            else:
                self.advance()

    def parse_foreign_key_ref(self, column: Column, constraint_name: Optional[str]):
        ref_table, ref_schema, ref_db = self.parse_object_name()
        ref_col = None

        if self.match('('):
            ref_col = self.consume_identifier()
            self.consume(')', "Expected ')' after referenced column")

        # Create explicit foreign key constraint
        fk = ForeignKey(
            name=constraint_name,
            columns=[column.name],
            ref_table=ref_table,
            ref_columns=[ref_col] if ref_col else [column.name]
        )
        self.current_table.foreign_keys.append(fk)

        # Add reference to column
        column.foreign_key_ref = (
            ref_table, ref_col or column.name, constraint_name)

    def parse_primary_key(self):
        self.consume('KEY', "Expected KEY after PRIMARY")
        if self.match('('):
            columns = []
            while not self.check(')') and not self.is_at_end():
                col_name = self.consume_identifier()
                columns.append(col_name)
                self.match(',')

            self.consume(')', "Expected ')' after primary key columns")

        # Get constraint name if available
        name = self.try_get_constraint_name()

        # Create primary key
        self.current_table.primary_key = PrimaryKey(name, columns)

        # Update columns with primary key positions
        for i, col_name in enumerate(columns, 1):
            if col_name in self.current_table.columns:
                col = self.current_table.columns[col_name]
                col.is_primary = True
                col.primary_key_position = i

    def parse_foreign_key(self):
        self.consume('KEY', "Expected KEY after FOREIGN")

        if self.match('('):
            columns = []
            while not self.check(')') and not self.is_at_end():
                col_name = self.consume_identifier()
                columns.append(col_name)
                self.match(',')

            self.consume(')', "Expected ')' after foreign key columns")

        self.consume('REFERENCES', "Expected REFERENCES in foreign key")

        ref_table, ref_schema, _ = self.parse_object_name()

        if self.match('('):
            ref_columns = []
            while not self.check(')') and not self.is_at_end():
                ref_col = self.consume_identifier()
                ref_columns.append(ref_col)
                self.match(',')

            self.consume(')', "Expected ')' after referenced columns")

        # Get constraint name if available
        name = self.try_get_constraint_name()

        # Add foreign key
        fk = ForeignKey(name, columns, ref_table, ref_columns)
        self.current_table.foreign_keys.append(fk)

    def parse_unique_constraint(self):
        if self.match('('):
            columns = []
            while not self.check(')') and not self.is_at_end():
                col_name = self.consume_identifier()
                columns.append(col_name)
                self.match(',')

            self.consume(')', "Expected ')' after unique columns")

        # Get constraint name if available
        name = self.try_get_constraint_name()

        self.current_table.constraints.append(
            Constraint(name, 'UNIQUE', columns=columns))

    def parse_check_constraint(self):
        expr = self.parse_expression()

        # Get constraint name if available
        name = self.try_get_constraint_name()

        self.current_table.constraints.append(
            Constraint(name, 'CHECK', expression=expr))

    def parse_constraint(self):
        constr_name = self.consume_identifier()

        if self.match('PRIMARY'):
            self.parse_primary_key()
            if self.current_table.primary_key:
                self.current_table.primary_key.name = constr_name
        elif self.match('FOREIGN'):
            print("Here ................", len(
                self.current_table.foreign_keys))
            self.parse_foreign_key()
            if self.current_table.foreign_keys and self.current_table.foreign_keys[-1].name is None:
                self.current_table.foreign_keys[-1].name = constr_name

        elif self.match('UNIQUE'):
            self.parse_unique_constraint()
            if self.current_table.constraints and self.current_table.constraints[-1].name is None:
                self.current_table.constraints[-1].name = constr_name
        elif self.match('CHECK'):
            self.parse_check_constraint()
            if self.current_table.constraints and self.current_table.constraints[-1].name is None:
                self.current_table.constraints[-1].name = constr_name

    def try_get_constraint_name(self) -> Optional[str]:
        if self.match('CONSTRAINT'):
            return self.consume_identifier()
        return None

    def parse_data_type(self) -> Tuple[str, Optional[List[str]]]:
        type_tokens = []
        params = []

        # Read data type name

        type_first_token = None

        if self.match(TokenType.IDENTIFIER) or self.match(TokenType.QUOTED_IDENTIFIER) or self.match(TokenType.KEYWORD):
            type_first_token = self.previous()
            type_tokens.append(type_first_token.value)

        if type_first_token.token_type == TokenType.KEYWORD:
            if type_first_token.value.upper() == "CHARACTER":
                ahead_tok = self.look_ahead()
                if ahead_tok.value.upper() == "VARYING":
                    type_tokens.append(ahead_tok.value)
                    self.advance()
            elif type_first_token.value.upper() == "DOUBLE":
                ahead_tok = self.look_ahead()
                if ahead_tok.value.upper() == "PRECISION":
                    type_tokens.append(ahead_tok.value)
                    self.advance()

        data_type = ' '.join(type_tokens).lower()
        # Parse type parameters if present
        if self.match('('):
            param_tokens = []
            while not self.check(')') and not self.is_at_end():
                if self.match(','):
                    if param_tokens:
                        params.append(''.join(param_tokens))
                        param_tokens = []
                else:
                    token = self.advance()
                    param_tokens.append(token.value)

            if param_tokens:
                params.append(''.join(param_tokens))
            self.consume(')', "Expected ')' after type parameters")
        return data_type, params

    def parse_object_name(self) -> Tuple[str, Optional[str], Optional[str]]:
        parts = []
        while True:
            if self.match(TokenType.QUOTED_IDENTIFIER):
                parts.append(self.previous().value.strip('"'))
            elif self.match(TokenType.IDENTIFIER):
                parts.append(self.previous().value)
            else:
                break

            if not self.match('.'):
                break

        if len(parts) == 1:
            return parts[0], None, None
        if len(parts) == 2:
            return parts[1], parts[0], None
        return parts[2], parts[1], parts[0]

    def parse_expression(self) -> str:
        tokens = []
        depth = []
        while not self.is_at_end():
            if not depth and (self.check(',') or self.check(')')):
                break
            elif self.check('('):
                tokens.append(self.peek())
                self.advance()
                depth.append(True)
            elif self.check(')'):
                depth.pop()
                tokens.append(self.peek())
                self.advance()
            else:
                tokens.append(self.peek())
                self.advance()

        return ' '.join([tok.value for tok in tokens])

    def parse_default_value(self) -> str:
        tokens = []

        while not self.is_at_end():
            if self.check(',') or self.check(')') or self.peek().value.upper() in (
                'CONSTRAINT', 'PRIMARY', 'FOREIGN', 'REFERENCES',
                'NOT', 'NULL', 'UNIQUE', 'CHECK'
            ):
                break
            tokens.append(self.advance().value)

        return ' '.join(tokens)

    def parse_remaining(self) -> str:
        """Parse remaining tokens as a string"""
        tokens = []
        while not self.is_at_end():
            tokens.append(self.advance().value)
        return ' '.join(tokens)

    # Token navigation helpers
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def check(self, value: Any) -> bool:
        if self.is_at_end():
            return False
        token = self.peek()
        if isinstance(value, TokenType):
            return token.token_type == value
        return token.value.upper() == value.upper()

    def look_ahead(self, ahead: int = 1):
        if self.is_at_end() or self.current+1 >= len(self.tokens):
            return None
        return self.tokens[self.current+1]

    def check_ahead(self,  tok_value,  ahead: int = 1):
        tok = self.look_ahead(ahead)
        if tok is None:
            return False
        return tok.value == tok_value

    def match(self, *args: Any) -> bool:
        for value in args:
            if self.check(value):
                self.advance()
                return True
        return False

    def consume(self, value: Any, message: str) -> Token:
        if self.check(value):
            return self.advance()
        raise ValueError(f"{message} at position {self.peek().position}")

    def consume_identifier(self) -> str:
        if self.match(TokenType.QUOTED_IDENTIFIER):
            return self.previous().value.strip('"')
        if self.match(TokenType.IDENTIFIER):
            return self.previous().value
        raise ValueError(
            f"Expected identifier at position {self.peek().position}")

    # Table management
    def add_table(self, table: Table):
        key = table.get_qualified_name()
        self.tables[key] = table

    def get_tables(self) -> List[Table]:
        return list(self.tables.values())

    def get_table(self, table_name: str, schema: Optional[str] = None,
                  database: Optional[str] = None) -> Optional[Table]:
        keys_to_try = []

        # Fully qualified name
        if database and schema:
            keys_to_try.append(f"{database}.{schema}.{table_name}")

        # Schema-qualified name
        if schema:
            keys_to_try.append(f"{schema}.{table_name}")

        # Simple table name
        keys_to_try.append(table_name)

        # Search for existing table
        for key in keys_to_try:
            if key in self.tables:
                return self.tables[key]

        return None
