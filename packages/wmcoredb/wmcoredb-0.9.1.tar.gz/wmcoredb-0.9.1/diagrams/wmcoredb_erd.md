# WMCoreDB Entity Relationship Diagram

## Cardinality Notation
- `||--o{` : One-to-many relationship (one entity can have many related entities)
- `||--||` : One-to-one relationship (one entity is associated with exactly one other entity)
- `}o--o{` : Many-to-many relationship (entities can have multiple relationships with each other)
- `||--o|` : One-to-many relationship with mandatory participation
- `o|--o{` : One-to-many relationship with optional participation

## Core Schema ERD

```mermaid
erDiagram
    %% Core Entities
    wmbs_workflow ||--o{ wmbs_subscription : "has"
    wmbs_workflow ||--o{ wmbs_workflow_output : "produces"
    wmbs_fileset ||--o{ wmbs_subscription : "used_in"
    wmbs_fileset ||--o{ wmbs_fileset_files : "contains"
    wmbs_file_details ||--o{ wmbs_fileset_files : "referenced_by"
    wmbs_file_details ||--o{ wmbs_file_parent : "child"
    wmbs_file_details ||--o{ wmbs_file_parent : "parent"
    wmbs_file_details ||--o{ wmbs_file_location : "located_at"
    wmbs_file_details ||--o{ wmbs_file_runlumi_map : "has"
    wmbs_file_details ||--o{ wmbs_file_checksums : "has"
    
    %% Job Management
    wmbs_subscription ||--o{ wmbs_jobgroup : "contains"
    wmbs_jobgroup ||--o{ wmbs_job : "contains"
    wmbs_job ||--o{ wmbs_job_assoc : "has"
    wmbs_job ||--o{ wmbs_job_mask : "has"
    wmbs_job ||--o{ wmbs_job_workunit_assoc : "has"
    
    %% Location and Resource Management
    wmbs_location ||--o{ wmbs_location_pnns : "has"
    wmbs_pnns ||--o{ wmbs_location_pnns : "used_in"
    wmbs_location ||--o{ wmbs_subscription_validation : "validates"
    wmbs_location ||--o{ wmbs_job : "executes"
    wmbs_location_state ||--o{ wmbs_location : "has_state"
    
    %% Work Unit Management
    wmbs_workunit ||--o{ wmbs_job_workunit_assoc : "assigned_to"
    wmbs_workunit ||--o{ wmbs_frl_workunit_assoc : "assigned_to"
    
    %% BossAir Module
    bl_status ||--o{ bl_runjob : "has"
    wmbs_job ||--o{ bl_runjob : "tracked_by"
    wmbs_users ||--o{ bl_runjob : "owned_by"
    wmbs_location ||--o{ bl_runjob : "executed_at"
```

## Module-Specific ERDs

### WMBS Module
```mermaid
erDiagram
    wmbs_workflow ||--o{ wmbs_subscription : "has"
    wmbs_workflow ||--o{ wmbs_workflow_output : "produces"
    wmbs_fileset ||--o{ wmbs_subscription : "used_in"
    wmbs_fileset ||--o{ wmbs_fileset_files : "contains"
    wmbs_file_details ||--o{ wmbs_fileset_files : "referenced_by"
```

### BossAir Module
```mermaid
erDiagram
    bl_status ||--o{ bl_runjob : "has"
    wmbs_job ||--o{ bl_runjob : "tracked_by"
    wmbs_users ||--o{ bl_runjob : "owned_by"
    wmbs_location ||--o{ bl_runjob : "executed_at"
```

### Resource Control Module
```mermaid
erDiagram
    rc_threshold ||--o{ rc_threshold_metric : "has"
    rc_threshold ||--o{ rc_threshold_value : "has"
```

### Agent Database Module
```mermaid
erDiagram
    wm_init ||--o{ wm_components : "initializes"
    wm_components ||--o{ wm_workers : "manages"
```

### DBS3Buffer Module
```mermaid
erDiagram
    dbsbuffer_dataset ||--o{ dbsbuffer_block : "contains"
    dbsbuffer_block ||--o{ dbsbuffer_file : "contains"
    dbsbuffer_file ||--o{ dbsbuffer_file_parent : "has"
    dbsbuffer_file ||--o{ dbsbuffer_file_runlumi_map : "has"
    dbsbuffer_file ||--o{ dbsbuffer_file_checksums : "has"
    dbsbuffer_file ||--o{ dbsbuffer_file_location : "located_at"
    dbsbuffer_dataset ||--o{ dbsbuffer_algo : "processed_by"
```

### TestDB Module
```mermaid
erDiagram
    test_table ||--o{ test_table_child : "has"
```

## Database Backend Compatibility

```mermaid
graph TD
    A[WMCoreDB] --> B[Oracle Backend]
    A --> C[MariaDB Backend]
    B --> D[Oracle 19c]
    C --> E[MariaDB 10.6.21]
    B --> F[IDENTITY]
    B --> G[VARCHAR2]
    C --> H[AUTO_INCREMENT]
    C --> I[VARCHAR]
```

## Schema Initialization Flow

```mermaid
graph TD
    A[Start] --> B[Create Tables]
    B --> C[Create Indexes]
    C --> D[Load Initial Data]
    D --> E[Validate Schema]
    E --> F[End]

    subgraph WMBS
    B --> G[Create WMBS Tables]
    C --> H[Create WMBS Indexes]
    D --> I[Load WMBS Data]
    end

    subgraph BossAir
    B --> J[Create BossAir Tables]
    C --> K[Create BossAir Indexes]
    end

    subgraph ResourceControl
    B --> L[Create ResourceControl Tables]
    C --> M[Create ResourceControl Indexes]
    end

    subgraph Agent
    B --> N[Create Agent Tables]
    C --> O[Create Agent Indexes]
    end

    subgraph DBS3Buffer
    B --> P[Create DBS3Buffer Tables]
    C --> Q[Create DBS3Buffer Indexes]
    end
``` 