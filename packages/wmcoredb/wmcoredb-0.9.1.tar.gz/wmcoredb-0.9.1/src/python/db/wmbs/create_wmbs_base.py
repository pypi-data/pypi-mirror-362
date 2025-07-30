"""
_CreateWMBS_

Base class for creating the WMBS database.
"""

import os
import threading

from WMCore.Database.DBCreator import DBCreator
from WMCore.JobStateMachine.Transitions import Transitions
from WMCore.WMException import WMException


class CreateWMBSBase(DBCreator):
    def __init__(self, logger=None, dbi=None, params=None):
        """
        Initialize the database creator
        """
        myThread = threading.currentThread()

        if logger is None:
            logger = myThread.logger
        if dbi is None:
            dbi = myThread.dbi

        tablespaceIndex = ""
        if params:
            if "tablespace_index" in params:
                tablespaceIndex = "USING INDEX TABLESPACE %s" % params["tablespace_index"]

        DBCreator.__init__(self, logger, dbi)

        # Get database type (oracle or mariadb)
        self.db_type = self.dbi.engine.dialect.name
        
        # Required tables list - used for validation
        self.requiredTables = [
            "01wmbs_fileset",
            "02wmbs_file_details",
            "03wmbs_fileset_files",
            "04wmbs_file_parent",
            "05wmbs_file_runlumi_map",
            "05wmbs_location_state",
            "06wmbs_location",
            "06wmbs_pnns",
            "07wmbs_location_pnns",
            "07wmbs_file_location",
            "07wmbs_users",
            "07wmbs_workflow",
            "08wmbs_sub_types",
            "08wmbs_workflow_output",
            "09wmbs_subscription",
            "10wmbs_subscription_validation",
            "10wmbs_sub_files_acquired",
            "10wmbs_sub_files_available",
            "11wmbs_sub_files_failed",
            "12wmbs_sub_files_complete",
            "13wmbs_jobgroup",
            "14wmbs_job_state",
            "15wmbs_job",
            "16wmbs_job_assoc",
            "17wmbs_job_mask",
            "18wmbs_checksum_type",
            "19wmbs_file_checksums",
            "21wmbs_workunit",
            "22wmbs_job_workunit_assoc",
            "23wmbs_frl_workunit_assoc",
        ]
        
        # Load SQL files
        self.load_sql_files()

    def load_sql_files(self):
        """Load SQL statements from files"""
        base_dir = os.path.dirname(__file__)
        sql_dir = os.path.join(base_dir, 'sql', self.db_type)
        
        # Load table creation statements
        with open(os.path.join(sql_dir, 'create_wmbs_tables.sql')) as f:
            for statement in f.read().split(';'):
                if statement.strip():
                    # Use first 30 chars of statement as key
                    key = statement.strip().split()[2]  # Get table name
                    self.create[key] = statement.strip()
        
        # Load index creation statements
        with open(os.path.join(sql_dir, 'create_wmbs_indexes.sql')) as f:
            for statement in f.read().split(';'):
                if statement.strip():
                    # Use index name as key
                    key = statement.strip().split()[2]  # Get index name
                    self.constraints[key] = statement.strip()
        
        # Load initial data
        with open(os.path.join(sql_dir, 'initial_data.sql')) as f:
            for statement in f.read().split(';'):
                if statement.strip():
                    # Generate key based on the type of insert
                    words = statement.strip().split()
                    table = words[words.index('INTO') + 1]
                    values = statement.split('VALUES')[1]
                    key = f"{table}_{values.strip('() ;')[:20]}"
                    self.inserts[key] = statement.strip()

    def execute(self, conn=None, transaction=None):
        """
        Execute the database creation
        """
        for requiredTable in self.requiredTables:
            if requiredTable not in self.create:
                raise WMException("The table '%s' is not defined." % requiredTable, "WMCORE-2")

        DBCreator.execute(self, conn, transaction)
        return True
