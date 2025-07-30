# WMCoreDB Diagrams

This directory contains visual representations of the WMCoreDB database schema and its components.

## Contents

1. **wmcoredb_erd.md**
   - Complete Entity Relationship Diagram (ERD) of the database
   - Module-specific ERDs for better clarity
   - Cardinality notation explanation
   - Database backend compatibility diagram
   - Schema initialization flow diagram

## Diagram Types

### 1. Entity Relationship Diagrams (ERD)
- Shows relationships between database entities
- Includes cardinality indicators
- Separated into module-specific views for better clarity
- Includes entity attributes and key information

### 2. Database Backend Compatibility
- Visual representation of supported database backends
- Shows specific features for each backend
- Highlights compatibility requirements

### 3. Schema Initialization Flow
- Shows the sequence of schema creation
- Illustrates module dependencies
- Displays the initialization process

## Usage

These diagrams are created using Mermaid.js syntax and can be viewed in any markdown viewer that supports Mermaid.js, such as:
- GitHub
- GitLab
- VS Code (with Mermaid extension)
- Mermaid Live Editor

## Cardinality Notation

The ERDs use the following notation for relationships:

- `||--o{` : One-to-many relationship (one entity can have many related entities)
- `||--||` : One-to-one relationship (one entity is associated with exactly one other entity)
- `}o--o{` : Many-to-many relationship (entities can have multiple relationships with each other)
- `||--o|` : One-to-many relationship with mandatory participation
- `o|--o{` : One-to-many relationship with optional participation

## Contributing

When adding new diagrams:
1. Use Mermaid.js syntax
2. Include clear labels and descriptions
3. Maintain consistent notation
4. Update this README if adding new diagram types 