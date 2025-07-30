"""
_execute_wmbs_sql_

Script to parse and execute WMBS SQL files for database creation.
"""

import os
import logging
from typing import List, Optional

from WMCore.Database.DBFormatter import DBFormatter
from WMCore.WMException import WMException


class ExecuteWMBSSQL:
    """Class to handle execution of WMBS SQL files"""

    def __init__(self, logger: Optional[logging.Logger] = None, dbi=None):
        """
        Initialize with logger and database interface
        """
        self.logger = logger or logging.getLogger()
        self.dbi = dbi
        self.formatter = DBFormatter(self.logger, self.dbi)

    def parse_sql_file(self, filepath: str) -> List[str]:
        """
        Parse SQL file and return list of statements
        
        Args:
            filepath: Path to SQL file
            
        Returns:
            List of SQL statements
        """
        with open(filepath, 'r') as f:
            content = f.read()

        # Split on semicolon but handle PL/SQL blocks (for Oracle triggers)
        statements = []
        current_statement = []
        in_plsql_block = False

        for line in content.split('\n'):
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith('--'):
                continue

            if line.upper().startswith('CREATE OR REPLACE TRIGGER'):
                in_plsql_block = True
                
            if in_plsql_block:
                current_statement.append(line)
                if line == '/':  # End of PL/SQL block
                    statements.append('\n'.join(current_statement))
                    current_statement = []
                    in_plsql_block = False
            else:
                if ';' in line:
                    parts = line.split(';')
                    current_statement.append(parts[0])
                    statements.append(' '.join(current_statement))
                    current_statement = []
                    # Handle any remaining parts
                    for part in parts[1:]:
                        if part.strip():
                            current_statement.append(part)
                else:
                    current_statement.append(line)

        # Add any remaining statement
        if current_statement:
            statements.append(' '.join(current_statement))

        return [stmt.strip() for stmt in statements if stmt.strip()]

    def execute_sql_file(self, filepath: str, transaction=None) -> None:
        """
        Execute all statements in a SQL file
        
        Args:
            filepath: Path to SQL file
            transaction: Database transaction to use
        """
        statements = self.parse_sql_file(filepath)
        
        for statement in statements:
            try:
                self.logger.debug(f"Executing SQL: {statement[:100]}...")
                self.formatter.dbi.processData(statement, transaction=transaction)
            except Exception as ex:
                self.logger.error(f"Error executing SQL: {statement[:100]}...")
                self.logger.error(str(ex))
                raise

    def execute_wmbs_files(self) -> None:
        """
        Execute all WMBS SQL files in correct order
        """
        db_type = self.dbi.engine.dialect.name
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # Get project root
        sql_dir = os.path.join(base_dir, 'sql', db_type)  # Updated path to reflect new structure

        if not os.path.exists(sql_dir):
            raise WMException(f"SQL directory not found: {sql_dir}")

        # Assuming the sub-directories are named in a specific order or pattern
        sub_dirs = sorted([d for d in os.listdir(sql_dir) if os.path.isdir(os.path.join(sql_dir, d))])

        transaction = self.dbi.beginTransaction()
        try:
            for sub_dir in sub_dirs:
                sub_dir_path = os.path.join(sql_dir, sub_dir)
                files_to_execute = sorted([f for f in os.listdir(sub_dir_path) if f.endswith('.sql')])

                for filename in files_to_execute:
                    filepath = os.path.join(sub_dir_path, filename)
                    if not os.path.exists(filepath):
                        raise WMException(f"SQL file not found: {filepath}")

                    self.logger.info(f"Executing {filename} in {sub_dir}...")
                    self.execute_sql_file(filepath, transaction)

            transaction.commit()
            self.logger.info("Successfully executed all WMBS SQL files")

        except:
            transaction.rollback()
            raise


def main():
    """Main function to execute SQL files"""
    import threading
    from WMCore.WMInit import WMInit

    # Initialize database connection
    wmInit = WMInit()
    wmInit.setLogging()
    wmInit.setDatabaseConnection()

    myThread = threading.currentThread()
    executor = ExecuteWMBSSQL(logger=myThread.logger, dbi=myThread.dbi)
    
    try:
        executor.execute_wmbs_files()
    except Exception as ex:
        myThread.logger.error(f"Failed to execute WMBS SQL files: {str(ex)}")
        raise


if __name__ == "__main__":
    main() 