import pytest
from pgsql_parser import SQLLexer, SQLParser, TokenType, Token

# Test SQLLexer
class TestSQLLexer:
    def test_tokenize_basic(self):
        lexer = SQLLexer()
        sql = "SELECT * FROM users;"
        tokens = lexer.tokenize(sql)
        
        assert len(tokens) == 5
        assert tokens[0].token_type == TokenType.KEYWORD
        assert tokens[0].value == "SELECT"
        assert tokens[1].token_type == TokenType.OPERATOR
        assert tokens[1].value == "*"
        assert tokens[2].token_type == TokenType.KEYWORD
        assert tokens[2].value == "FROM"
        assert tokens[3].token_type == TokenType.IDENTIFIER
        assert tokens[3].value == "users"
        assert tokens[4].token_type == TokenType.PUNCTUATION
        assert tokens[4].value == ";"

    def test_quoted_identifiers(self):
        lexer = SQLLexer()
        sql = 'SELECT "userName" FROM "public"."users";'
        tokens = lexer.tokenize(sql)
        
        assert tokens[1].token_type == TokenType.QUOTED_IDENTIFIER
        assert tokens[1].value == '"userName"'
        assert tokens[3].token_type == TokenType.QUOTED_IDENTIFIER
        assert tokens[3].value == '"public"'
        assert tokens[5].token_type == TokenType.QUOTED_IDENTIFIER
        assert tokens[5].value == '"users"'

    def test_string_literals(self):
        lexer = SQLLexer()
        sql = "WHERE name = 'John''s Cafe';"
        tokens = lexer.tokenize(sql)
        
        assert tokens[3].token_type == TokenType.STRING_LITERAL
        assert tokens[3].value == "'John''s Cafe'"

    def test_numeric_literals(self):
        lexer = SQLLexer()
        sql = "VALUES (123, 45.67, 1e-5);"
        tokens = lexer.tokenize(sql)
        
        assert tokens[2].token_type == TokenType.NUMERIC_LITERAL
        assert tokens[2].value == "123"
        assert tokens[4].token_type == TokenType.NUMERIC_LITERAL
        assert tokens[4].value == "45.67"
        assert tokens[6].token_type == TokenType.NUMERIC_LITERAL
        assert tokens[6].value == "1e-5"

    def test_comments(self):
        lexer = SQLLexer()
        sql = """
        -- This is a comment
        SELECT * FROM users; /* Multi-line
        comment */
        """
        tokens = lexer.tokenize(sql)
        
        assert tokens[0].token_type == TokenType.COMMENT
        assert tokens[0].value == "-- This is a comment"
        assert tokens[6].token_type == TokenType.COMMENT
        assert tokens[6].value.startswith("/* Multi-line")

    def test_split_statements(self):
        lexer = SQLLexer()
        sql = """
        CREATE TABLE users (id INT);
        INSERT INTO users VALUES (1);
        UPDATE users SET name = 'John' WHERE id = 1;
        """
        statements = lexer.split_sql_statements(sql)
        
        assert len(statements) == 3
        assert statements[0].startswith("CREATE TABLE")
        assert statements[1].startswith("INSERT INTO")
        assert statements[2].startswith("UPDATE users")

    def test_split_complex_statements(self):
        lexer = SQLLexer()
        sql = """
        CREATE FUNCTION add(a INT, b INT) RETURNS INT AS $$
        BEGIN
            RETURN a + b;
        END;
        $$ LANGUAGE plpgsql;
        
        SELECT add(1, 2);
        """
        statements = lexer.split_sql_statements(sql)
        
        assert len(statements) == 2
        assert statements[0].startswith("CREATE FUNCTION")
        assert statements[1].startswith("SELECT add")

# Test SQLParser
class TestSQLParser:
    @pytest.fixture
    def parser(self):
        return SQLParser()

    def test_create_table_basic(self, parser):
        sql = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(255)
        );
        """
        parser.parse_script(sql)
        tables = parser.get_tables()
        
        assert len(tables) == 1
        table = tables[0]
        assert table.name == "users"
        assert len(table.columns) == 3
        
        # Verify columns
        assert "id" in table.columns
        assert table.columns["id"].data_type == "serial"
        assert table.columns["id"].is_primary
        assert not table.columns["name"].nullable
        assert table.columns["email"].nullable
        
        # Verify primary key
        assert table.primary_key is not None
        assert table.primary_key.columns == ["id"]

    def test_create_table_full_qualified(self, parser):
        sql = """
        CREATE TABLE public.users (
            id INT,
            name VARCHAR(50)
        );
        """
        parser.reset()
        parser.parse_script(sql)
        table = parser.get_table("users", "public")
        
        assert table is not None
        assert table.name == "users"
        assert table.schema == "public"
        assert len(table.columns) == 2

    def test_create_table_with_constraints(self, parser):
        sql = """
        CREATE TABLE orders (
            order_id INT PRIMARY KEY,
            user_id INT NOT NULL,
            amount DECIMAL(10,2),
            order_date DATE NOT NULL,
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
            CONSTRAINT chk_amount CHECK (amount > 0)
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("orders")
        
        # Verify columns
        assert table.columns["order_id"].is_primary
        assert not table.columns["user_id"].nullable
        assert table.columns["amount"].data_type == "decimal"
        assert table.columns["amount"].numeric_precision == 10
        assert table.columns["amount"].numeric_scale == 2
        
        # Verify foreign key
        assert len(table.foreign_keys) == 1
        fk = table.foreign_keys[0]
        assert fk.name == "fk_user"
        assert fk.columns == ["user_id"]
        assert fk.ref_table == "users"
        assert fk.ref_columns == ["id"]
        
        # Verify check constraint
        assert len(table.constraints) == 1
        constraint = table.constraints[0]
        assert constraint.name == "chk_amount"
        assert constraint.ctype == "CHECK"
        assert "amount > 0" in constraint.expression

    def test_create_table_temp(self, parser):
        sql = """
        CREATE TEMPORARY TABLE temp_data (
            id INT,
            value TEXT
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("temp_data")
        
        assert table is not None
        assert table.table_type == "TEMPORARY TABLE"

    def test_create_view(self, parser):
        sql = """
        CREATE VIEW active_users AS
        SELECT id, name FROM users WHERE active = TRUE;
        """
        parser.parse_script(sql)
        table = parser.get_table("active_users")
        
        assert table is not None
        assert table.is_view
        assert not table.is_materialized
        
        assert "SELECT id , name" in table.view_definition

    def test_create_materialized_view(self, parser):
        sql = """
        CREATE MATERIALIZED VIEW user_stats AS
        SELECT user_id, COUNT(*) AS order_count
        FROM orders
        GROUP BY user_id;
        """
        parser.parse_script(sql)
        table = parser.get_table("user_stats")
        
        assert table is not None
        assert table.is_view
        assert table.is_materialized
        assert "GROUP BY user_id" in table.view_definition

    def test_alter_table_add_column(self, parser):
        sql = """
        CREATE TABLE users (id INT);
        ALTER TABLE users ADD COLUMN name VARCHAR(50);
        """
        parser.parse_script(sql)
        table = parser.get_table("users")
        
        assert len(table.columns) == 2
        assert "name" in table.columns
        assert table.columns["name"].data_type == "varchar"
        assert table.columns["name"].char_length == 50

    def test_alter_table_add_constraint(self, parser):
        sql = """
        CREATE TABLE users (id INT, email VARCHAR(255));
        ALTER TABLE users 
        ADD CONSTRAINT pk_users PRIMARY KEY (id),
        ADD CONSTRAINT uk_email UNIQUE (email);
        """
        parser.parse_script(sql)
        table = parser.get_table("users")
        
        assert table.primary_key is not None
        assert table.primary_key.columns == ["id"]
        
        assert len(table.constraints) == 1
        constraint = table.constraints[0]
        assert constraint.ctype == "UNIQUE"
        assert constraint.columns == ["email"]

    def test_alter_table_drop_column(self, parser):
        sql = """
        CREATE TABLE users (id INT, name VARCHAR(50), email VARCHAR(255));
        ALTER TABLE users DROP COLUMN email;
        """
        parser.reset()
        parser.parse_script(sql)
        table = parser.get_table("users")
        
        assert len(table.columns) == 2
        assert "email" not in table.columns
        assert "name" in table.columns

    def test_create_index(self, parser):
        sql = """
        CREATE TABLE users (id INT, email VARCHAR(255));
        CREATE INDEX idx_users_email ON users(email);
        CREATE UNIQUE INDEX idx_users_id ON users(id);
        """
        parser.parse_script(sql)
        # Indexes are not directly stored in table, but we can verify parsing doesn't fail
        
        # For this test, we'll just make sure no exceptions are raised
        assert len(parser.get_tables()) == 1

    def test_get_table_by_qualified_name(self, parser):
        sql = """
        CREATE TABLE public.users (id INT);
        CREATE TABLE sales.orders (order_id INT);
        CREATE TABLE reporting.metrics (metric_id INT);
        """
        parser.parse_script(sql)
        
        # Get by full qualified name
        table1 = parser.get_table("users", "public")
        assert table1 is not None
        
        # Get by table name only (should return first match)
        table2 = parser.get_table("orders")
        assert table2 is None  # Shouldn't find without schema
        
        # Get with schema
        table3 = parser.get_table("orders", "sales")
        assert table3 is not None
        
        # Non-existent table
        table4 = parser.get_table("non_existent")
        assert table4 is None

    def test_table_type_detection(self, parser):
        sql = """
        CREATE TABLE regular_table (id INT);
        CREATE TEMPORARY TABLE temp_table (id INT);
        CREATE VIEW my_view AS SELECT 1;
        CREATE MATERIALIZED VIEW mat_view AS SELECT 1;
        """
        parser.parse_script(sql)
        
        tables = {t.name: t for t in parser.get_tables()}
        
        assert tables["regular_table"].table_type == "TABLE"
        assert tables["temp_table"].table_type == "TEMPORARY TABLE"
        assert tables["my_view"].table_type == "VIEW"
        assert tables["mat_view"].table_type == "MATERIALIZED VIEW"

    def test_column_metadata(self, parser):
        sql = """
        CREATE TABLE products (
            product_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) CHECK (price > 0),
            category_id INT REFERENCES categories(id)
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("products")
        columns = table.columns
        
        # Verify column properties
        assert columns["product_id"].is_primary
        assert columns["product_id"].primary_key_position == 1
        assert not columns["name"].nullable
        assert columns["description"].nullable
        assert columns["price"].data_type == "decimal"
        assert columns["price"].numeric_precision == 10
        assert columns["price"].numeric_scale == 2
        assert columns["category_id"].foreign_key_ref is not None
        assert columns["category_id"].foreign_key_ref[0] == "categories"

    def test_statement_generator(self, parser):
        sql = """
        CREATE TABLE table1 (id INT);
        CREATE TABLE table2 (id INT);
        CREATE TABLE table3 (id INT);
        """
        statements = list(parser.statement_generator(sql))
        
        assert len(statements) == 3
        assert all(s.startswith("CREATE TABLE") for s in statements)

    def test_parse_invalid_sql(self, parser):
        sql = "INVALID SQL SYNTAX;"
        # Should not raise exception
        parser.parse_script(sql)
        assert len(parser.get_tables()) == 0

    def test_quoted_identifiers_in_parser(self, parser):
        sql = """
        CREATE TABLE "MyTable" (
            "Id" SERIAL PRIMARY KEY,
            "Full Name" VARCHAR(100)
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("MyTable")
        
        assert table is not None
        assert "Full Name" in table.columns
        assert table.columns["Full Name"].data_type == "varchar"

    def test_foreign_key_column_reference(self, parser):
        sql = """
        CREATE TABLE orders (
            order_id INT PRIMARY KEY,
            user_id INT REFERENCES users(id)
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("orders")
        column = table.columns["user_id"]
        
        assert column.foreign_key_ref is not None
        ref_table, ref_col, _ = column.foreign_key_ref
        assert ref_table == "users"
        assert ref_col == "id"

    def test_multiple_foreign_keys(self, parser):
        sql = """
        CREATE TABLE order_items (
            item_id INT PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            product_id INT REFERENCES products(id)
        );
        """
        parser.reset()
        print(parser.get_table("order_items"))
        parser.parse_script(sql)
        table = parser.get_table("order_items")
        
        assert len(table.foreign_keys) == 2
        fk1, fk2 = table.foreign_keys
        
        assert fk1.columns == ["order_id"]
        assert fk1.ref_table == "orders"
        
        assert fk2.columns == ["product_id"]
        assert fk2.ref_table == "products"

    def test_alter_table_rename_column(self, parser):
        sql = """
        CREATE TABLE users (user_id INT, full_name VARCHAR(100));
        ALTER TABLE users RENAME COLUMN full_name TO name;
        """
        parser.parse_script(sql)
        table = parser.get_table("users")
        
        assert "name" in table.columns
        assert "full_name" not in table.columns
        assert table.columns["name"].data_type == "varchar"

    def test_composite_primary_key(self, parser):
        sql = """
        CREATE TABLE order_items (
            order_id INT,
            item_id INT,
            PRIMARY KEY (order_id, item_id)
        );
        """
        parser.reset()
        parser.parse_script(sql)
        table = parser.get_table("order_items")
        
        assert table.primary_key is not None
        assert table.primary_key.columns == ["order_id", "item_id"]
        
        # Verify column properties
        assert table.columns["order_id"].is_primary
        assert table.columns["order_id"].primary_key_position == 1
        assert table.columns["item_id"].is_primary
        assert table.columns["item_id"].primary_key_position == 2

    def test_parse_large_script(self, parser):
        large_sql = """
        /* Create schemas */
        CREATE SCHEMA sales;
        CREATE SCHEMA hr;
        
        /* Create tables */
        CREATE TABLE sales.customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE
        );
        
        CREATE TABLE sales.orders (
            order_id INT PRIMARY KEY,
            customer_id INT REFERENCES sales.customers(customer_id),
            order_date DATE NOT NULL
        );
        
        CREATE TABLE hr.employees (
            emp_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(50)
        );
        
        /* Create views */
        CREATE VIEW sales.customer_orders AS
        SELECT c.name, COUNT(o.order_id) AS order_count
        FROM sales.customers c
        JOIN sales.orders o ON c.customer_id = o.customer_id
        GROUP BY c.name;
        
        /* Alter tables */
        ALTER TABLE sales.customers ADD COLUMN phone VARCHAR(20);
        ALTER TABLE hr.employees ADD COLUMN hire_date DATE;
        """
        
        parser.parse_script(large_sql)
        tables = parser.get_tables()
        
        assert len(tables) == 4
        assert parser.get_table("customers", "sales") is not None
        assert parser.get_table("orders", "sales") is not None
        assert parser.get_table("employees", "hr") is not None
        assert parser.get_table("customer_orders", "sales") is not None
        
        # Verify column additions
        customers = parser.get_table("customers", "sales")
        assert "phone" in customers.columns
        
        employees = parser.get_table("employees", "hr")
        assert "hire_date" in employees.columns

    def test_default_values(self, parser):
        sql = """
        CREATE TABLE products (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL DEFAULT 'Unnamed Product',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        parser.parse_script(sql)
        table = parser.get_table("products")
        
        assert table.columns["name"].default_value == "'Unnamed Product'"
        assert table.columns["created_at"].default_value == "CURRENT_TIMESTAMP"