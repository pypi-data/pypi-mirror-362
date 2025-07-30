[![SQL Linting](https://github.com/dmwm/wmcoredb/actions/workflows/sql-lint.yml/badge.svg)](https://github.com/dmwm/wmcoredb/actions/workflows/sql-lint.yml)
[![MariaDB Schema Validation](https://github.com/dmwm/wmcoredb/actions/workflows/mariadb-schema-test.yml/badge.svg)](https://github.com/dmwm/wmcoredb/actions/workflows/mariadb-schema-test.yml)
[![Oracle Schema Validation](https://github.com/dmwm/wmcoredb/actions/workflows/oracle-schema-test.yml/badge.svg)](https://github.com/dmwm/wmcoredb/actions/workflows/oracle-schema-test.yml)
[![Test Package Build](https://github.com/dmwm/wmcoredb/actions/workflows/test-build.yml/badge.svg)](https://github.com/dmwm/wmcoredb/actions/workflows/test-build.yml)
[![Release to PyPI](https://github.com/dmwm/wmcoredb/actions/workflows/release.yml/badge.svg)](https://github.com/dmwm/wmcoredb/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/wmcoredb.svg)](https://pypi.org/project/wmcoredb/)

# WMCore Database Schema

Database schema definitions for WMCore components, including both MariaDB and Oracle backends.

WMBS (Workload Management Bookkeeping Service) provides the database schema for managing 
workloads and jobs.

## Python Package

This repository is also available as a Python package on PyPI:

```bash
pip install wmcoredb
```

### Usage

The package provides utility functions to easily locate and access SQL schema files:

```python
import wmcoredb

# Get the path to a specific SQL file
file_path = wmcoredb.get_sql_file("wmbs", "create_wmbs_tables.sql", "mariadb")

# Get the content of a SQL file
sql_content = wmcoredb.get_sql_content("wmbs", "create_wmbs_tables.sql", "mariadb")

# List available modules
modules = wmcoredb.list_modules("mariadb")  # ['agent', 'bossair', 'dbs3buffer', 'resourcecontrol', 'testdb', 'wmbs']

# List SQL files in a module
sql_files = wmcoredb.list_sql_files("wmbs", "mariadb")  # ['create_wmbs_indexes.sql', 'create_wmbs_tables.sql', 'initial_wmbs_data.sql']

# List available backends
backends = wmcoredb.list_backends()  # ['mariadb', 'oracle']
```

### API Reference

- `get_sql_file(module_name, file_name, backend="mariadb")` - Get file path
- `get_sql_content(module_name, file_name, backend="mariadb")` - Get file content
- `list_sql_files(module_name=None, backend="mariadb")` - List SQL files
- `list_modules(backend="mariadb")` - List available modules
- `list_backends()` - List available backends

## Development

For local development and testing:

```bash
# Build the package
python -m build

# Install locally for testing
pip install dist/wmcoredb-*.whl
```

## CI/CD Pipeline

The continuous integration pipeline is split into three workflows:

### SQL Linting
Validates SQL syntax and formatting using SQLFluff:
* MariaDB files using default SQLFluff rules
* Oracle files using custom rules defined in `.sqlfluff.oracle`
* Enforces consistent SQL style and formatting
* Runs on every push and pull request

### MariaDB Schema Validation
Automatically tests schema deployment in MariaDB:
* Runs only after successful linting
* Tests against multiple MariaDB versions:
  - 10.6 (LTS)
  - 10.11 (LTS)
  - 11.4 (Latest)
* Deploys and validates:
  - TestDB Schema
  - WMBS Schema
  - Agent Schema
  - DBS3Buffer Schema
  - BossAir Schema
  - ResourceControl Schema
* Verifies table structures and relationships
* Checks for any critical database errors

### Oracle Schema Validation
Tests schema deployment in Oracle:
* Runs only after successful linting
* Uses Oracle XE 18.4.0-slim container
* Deploys and validates the same schemas as the MariaDB workflow:
  - TestDB Schema
  - WMBS Schema (tables, indexes, and initial data)
  - Tier0 Schema (tables, indexes, functions, and initial data)
  - Agent Schema
  - DBS3Buffer Schema
  - BossAir Schema
  - ResourceControl Schema
* Comprehensive verification steps:
  - Table structure validation
  - Index creation and type verification
  - Foreign key relationship checks
  - Initial data population verification
  - Cross-database compatibility with MariaDB
* Includes proper error handling and cleanup procedures
* Uses SQL*Plus for schema deployment and verification

## Directory Structure

The database schema files are organized as follows:

```
project_root/
├── src/
│   └── sql/              # Database schema files
│       ├── oracle/        # Oracle-specific SQL files
│       │   ├── wmbs/     # WMBS schema definitions
│       │   │   ├── create_wmbs_tables.sql     # Table definitions with constraints
│       │   │   ├── create_wmbs_indexes.sql    # Index definitions
│       │   │   └── initial_wmbs_data.sql      # Static data for some tables
│       │   ├── agent/    # WMCore.Agent.Database schema
│       │   ├── bossair/  # WMCore.BossAir schema
│       │   ├── dbs3buffer/ # WMComponent.DBS3Buffer schema
│       │   ├── resourcecontrol/ # WMCore.ResourceControl schema
│       │   ├── testdb/   # WMQuality.TestDB schema
│       │   └── tier0/    # Tier0 schema definitions
│       │       ├── create_tier0_tables.sql    # Table definitions with constraints
│       │       ├── create_tier0_indexes.sql   # Index definitions
│       │       ├── create_tier0_functions.sql # Helper functions
│       │       └── initial_tier0_data.sql     # Initial data for Tier0 tables
│       └── mariadb/      # MariaDB-specific SQL files
│           ├── wmbs/     # WMBS schema definitions
│           │   ├── create_wmbs_tables.sql     # Table definitions with constraints
│           │   ├── create_wmbs_indexes.sql    # Index definitions
│           │   └── initial_wmbs_data.sql      # Static data for some tables
│           ├── agent/    # WMCore.Agent.Database schema
│           ├── bossair/  # WMCore.BossAir schema
│           ├── dbs3buffer/ # WMComponent.DBS3Buffer schema
│           ├── resourcecontrol/ # WMCore.ResourceControl schema
│           ├── testdb/   # WMQuality.TestDB schema
│           └── tier0/    # Tier0 schema definitions (NOT IMPLEMENTED)
└── src/python/           # Schema generation code (not included in package)
    └── db/               # Legacy schema generation code
        ├── wmbs/
        ├── agent/
        ├── bossair/
        ├── dbs3buffer/
        ├── resourcecontrol/
        └── testdb/
        └── execute_wmbs_sql.py
```

## Schema Components

The WMAgent database schema consists of several components:

1. **WMBS** (`src/sql/{oracle,mariadb}/wmbs/`)
   - Core workload and job management
   - Tables for jobs, subscriptions, and file tracking
   - Initial data for job states and subscription types

2. **Agent Database** (`src/sql/{oracle,mariadb}/agent/`)
   - Core agent functionality
   - Component and worker management

3. **BossAir** (`src/sql/{oracle,mariadb}/bossair/`)
   - Job submission and tracking
   - Grid and batch system integration

4. **DBS3Buffer** (`src/sql/{oracle,mariadb}/dbs3buffer/`)
   - Dataset and file management
   - Checksum and location tracking

5. **ResourceControl** (`src/sql/{oracle,mariadb}/resourcecontrol/`)
   - Site and resource management
   - Threshold control

6. **Test Database** (`src/sql/{oracle,mariadb}/testdb/`)
   - Simple test tables for database validation
   - Used for testing database connectivity and basic operations
   - Includes tables with different data types and constraints
   - Available for both Oracle and MariaDB backends

7. **Tier0 Schema** (`src/sql/{oracle,mariadb}/tier0/`)
   - Run management and tracking
   - Stream and dataset associations
   - Lumi section processing
   - Configuration management
   - Workflow monitoring

## WMBS Schema Initialization

The WMBS schema is initialized first and consists of three files:

```
src/sql/{oracle,mariadb}/wmbs/
├── create_wmbs_tables.sql   # Core WMBS tables
├── create_wmbs_indexes.sql  # Indexes for performance
└── initial_wmbs_data.sql    # Initial data for job states
```

These files are executed in order by `execute_wmbs_sql.py` to set up the base WMBS schema before other components are initialized.

## Database Backend Support

The schema supports two database backends:

- **Oracle** (`src/sql/oracle/`)
  - Uses `NUMBER(11)` for integers
  - Uses `VARCHAR2` for strings
  - Uses `GENERATED BY DEFAULT AS IDENTITY` for auto-increment
  - Includes sequences and functions where needed
  - Uses slash (/) as statement terminator for DDL statements (CREATE TABLE, CREATE INDEX)
  - Uses both semicolon (;) and slash (/) for PL/SQL blocks (functions, procedures, packages)
    - Semicolon terminates the PL/SQL block
    - Slash executes the block

- **MariaDB** (`src/sql/mariadb/`)
  - Uses `INT` for integers
  - Uses `VARCHAR` for strings
  - Uses `AUTO_INCREMENT` for auto-increment
  - Uses `ENGINE=InnoDB ROW_FORMAT=DYNAMIC`
  - Includes equivalent functionality without sequences

## Database Compatibility

The SQL files are designed to be compatible with:

### MariaDB
- 10.6 (LTS)
- 10.11 (LTS)
- 11.4 (Latest)

### Oracle
- Oracle XE 18.4.0-slim container
- Oracle 19c

The CI pipeline automatically tests schema deployment against these versions to ensure compatibility.

## Database Documentation

For detailed database documentation, including Entity Relationship Diagrams (ERD), schema initialization flows, and module-specific diagrams, please refer to the [diagrams documentation](diagrams/README.md).

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Usage

To create the database schema:

1. For Oracle:
```sql
@src/sql/oracle/testdb/create_testdb.sql
@src/sql/oracle/tier0/create_tier0_tables.sql
@src/sql/oracle/tier0/create_tier0_indexes.sql
@src/sql/oracle/tier0/create_tier0_functions.sql
@src/sql/oracle/tier0/initial_tier0_data.sql
@src/sql/oracle/wmbs/create_wmbs_tables.sql
@src/sql/oracle/wmbs/create_wmbs_indexes.sql
@src/sql/oracle/wmbs/initial_wmbs_data.sql
```

2. For MariaDB:
```sql
source src/sql/mariadb/testdb/create_testdb.sql
source src/sql/mariadb/tier0/create_tier0_tables.sql
source src/sql/mariadb/tier0/create_tier0_indexes.sql
source src/sql/mariadb/tier0/create_tier0_functions.sql
source src/sql/mariadb/tier0/initial_tier0_data.sql
source src/sql/mariadb/wmbs/create_wmbs_tables.sql
source src/sql/mariadb/wmbs/create_wmbs_indexes.sql
source src/sql/mariadb/wmbs/initial_wmbs_data.sql
```

## Schema Generation

The SQL schema files are generated from Python code in `src/python/db/` (not included in the package). Each component has its own schema generation code:

```python
from WMCore.Database.DBCreator import DBCreator

class Create(DBCreator):
    def __init__(self, logger=None, dbi=None, params=None):
        # Schema definition in Python
```

The schema files can be executed using `execute_wmbs_sql.py`, which handles:
- Database backend detection
- Schema file location
- Transaction management
- Error handling

**Note:** The schema generation code in `src/python/db/` is for reference only and is not included in the PyPI package. The package only contains the final SQL files in `src/sql/`.

## Logs

Some relevant logs from the WMAgent 2.3.9.2 installation:
```
Start: Performing init_agent
init_agent: triggered.
Initializing WMAgent...
init_wmagent: MYSQL database: wmagent has been created
DEBUG:root:Log file ready
DEBUG:root:Using SQLAlchemy v.1.4.54
INFO:root:Instantiating base WM DBInterface
DEBUG:root:Tables for WMCore.WMBS created
DEBUG:root:Tables for WMCore.Agent.Database created
DEBUG:root:Tables for WMComponent.DBS3Buffer created
DEBUG:root:Tables for WMCore.BossAir created
DEBUG:root:Tables for WMCore.ResourceControl created
checking default database connection
default database connection tested
...
_sql_write_agentid: Preserving the current WMA_BUILD_ID and HostName at database: wmagent.
_sql_write_agentid: Creating wma_init table at database: wmagent
_sql_write_agentid: Inserting current Agent's build id and hostname at database: wmagent
_sql_dumpSchema: Dumping the current SQL schema of database: wmagent to /data/srv/wmagent/2.3.9/config/.wmaSchemaFile.sql
Done: Performing init_agent
```
## WMAgent DB Initialization

It starts in the CMSKubernetes [init.sh](https://github.com/dmwm/CMSKubernetes/blob/master/docker/pypi/wmagent/init.sh#L465) script, which executes `init_agent()` method from the CMSKubernetes [manage](https://github.com/dmwm/CMSKubernetes/blob/master/docker/pypi/wmagent/bin/manage#L112) script.

The database optios are enriched dependent on the database flavor, such as:
```bash
    case $AGENT_FLAVOR in
        'mysql')
            _exec_mysql "create database if not exists $wmaDBName"
            local database_options="--mysql_url=mysql://$MDB_USER:$MDB_PASS@$MDB_HOST/$wmaDBName "
        'oracle')
            local database_options="--coredb_url=oracle://$ORACLE_USER:$ORACLE_PASS@$ORACLE_TNS "
```

It then executes WMCore code, calling a script called [wmagent-mod-config](https://github.com/dmwm/WMCore/blob/master/bin/wmagent-mod-config).

with command line arguments like:
```bash
    wmagent-mod-config $database_options \
                       --input=$WMA_CONFIG_DIR/config-template.py \
                       --output=$WMA_CONFIG_DIR/config.py \
```

which internally parses the command line arguments into `parameters` and modifies the standard [WMAgentConfig.py](https://github.com/dmwm/WMCore/blob/master/etc/WMAgentConfig.py), saving it out as the new WMAgent configuration file, with something like:
```
    cfg = modifyConfiguration(cfg, **parameters)
    saveConfiguration(cfg, outputFile)
```

With the WMAgent configuration file properly updated, named `config.py`, now the `manage` script calls [wmcore-db-init](https://github.com/dmwm/WMCore/blob/master/bin/wmcore-db-init), with arguments like:

```bash
wmcore-db-init --config $WMA_CONFIG_DIR/config.py --create --modules=WMCore.WMBS,WMCore.Agent.Database,WMComponent.DBS3Buffer,WMCore.BossAir,WMCore.ResourceControl;
```

This `wmcore-db-init` script itself calls the [WMInit.py](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMInit.py) script, executing basically the next four commands:
```python
wmInit = WMInit()
wmInit.setLogging('wmcoreD', 'wmcoreD', logExists = False, logLevel = logging.DEBUG)
wmInit.setDatabaseConnection(dbConfig=config.CoreDatabase.connectUrl, dialect=dialect, socketLoc = socket)
wmInit.setSchema(modules, params = params)
```

In summary, the WMAgent database schema is an aggregation of the schema defined under each of the following WMAgent python directories:
```
WMCore.WMBS             --> originally under src/python/db/wmbs
WMCore.Agent.Database   --> originally under src/python/db/agent
WMCore.BossAir          --> originally under src/python/db/bossair
WMCore.ResourceControl  --> originally under src/python/db/resourcecontrol
WMComponent.DBS3Buffer  --> originally under src/python/db/dbs3buffer
```

The `wmcore-db-init` script itself calls the [WMInit.py](https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMInit.py) script, executing basically the next four commands:
```python
wmInit = WMInit()
wmInit.setLogging('wmcoreD', 'wmcoreD', logExists = False, logLevel = logging.DEBUG)
```

## Tier0 Schema

The Tier0 schema is designed to support the Tier0 data processing system. It includes tables for:

- Run management and tracking
- Stream and dataset associations
- Lumi section processing
- Configuration management
- Workflow monitoring

### Oracle Implementation

The Oracle implementation uses modern features like:
- IDENTITY columns for auto-incrementing IDs
- Inline foreign key constraints
- Organization index tables for performance
- Deterministic functions for state validation

The schema initialization includes:
- Table definitions with constraints
- Index definitions for performance
- Helper functions for state validation
- Initial data for run states, processing styles, and event scenarios

### MariaDB Implementation

Tier0 system does not - yet - support multiple database backends. For the moment, we have not converted the Tier0 schema to be compliant with MariaDB/MySQL.

## Test Database Schema

The Test Database schema provides a simple set of tables for testing database connectivity and basic operations. It includes:

- Tables with different data types (INT, VARCHAR, DECIMAL)
- Primary key constraints
- Table and column comments
- Cross-database compatibility

### Oracle Implementation

The Oracle implementation uses:
- NUMBER for numeric columns
- VARCHAR2 for string columns
- Table and column comments
- Primary key constraints

### MariaDB Implementation

The MariaDB implementation provides equivalent functionality using:
- INT and DECIMAL for numeric columns
- VARCHAR for string columns
- InnoDB engine specification
- Compatible comment syntax
