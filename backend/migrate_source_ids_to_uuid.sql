-- Migration script to convert source_ids from TEXT[] to UUID[]
-- Run this ONLY if you have an existing database with TEXT[] source_ids
-- For new databases, use the updated rds_schema.sql instead

-- Backup recommendation: Create a backup before running this migration
-- pg_dump -h <host> -U <user> -d studbud > backup_before_migration.sql

-- Step 1: Alter chat_history table
ALTER TABLE chat_history 
    ALTER COLUMN source_ids TYPE UUID[] 
    USING source_ids::UUID[];

-- Step 2: Alter studio_outputs table
ALTER TABLE studio_outputs 
    ALTER COLUMN source_ids TYPE UUID[] 
    USING source_ids::UUID[];

-- Verify the changes
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
    AND column_name = 'source_ids'
ORDER BY table_name;
