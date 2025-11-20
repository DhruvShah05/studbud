-- PostgreSQL Database Schema for AWS RDS
-- StudBud Application

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (for Clerk integration)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Workspaces table
CREATE TABLE IF NOT EXISTS workspaces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Sources table (uploaded documents)
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_url TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chat history table
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    source_ids UUID[] DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Studio outputs table (mindmaps, flashcards, quizzes, reports, audio, video)
CREATE TABLE IF NOT EXISTS studio_outputs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    output_type VARCHAR(50) NOT NULL CHECK (output_type IN ('mindmap', 'flashcards', 'quiz', 'report', 'audio_overview', 'video_overview')),
    content JSONB NOT NULL,
    source_ids UUID[] DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_workspaces_user_id ON workspaces(user_id);
CREATE INDEX IF NOT EXISTS idx_workspaces_updated_at ON workspaces(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_workspace_id ON sources(workspace_id);
CREATE INDEX IF NOT EXISTS idx_sources_created_at ON sources(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_history_workspace_id ON chat_history(workspace_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at ASC);
CREATE INDEX IF NOT EXISTS idx_studio_outputs_workspace_id ON studio_outputs(workspace_id);
CREATE INDEX IF NOT EXISTS idx_studio_outputs_created_at ON studio_outputs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_users_clerk_id ON users(clerk_user_id);

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts synced from Clerk authentication';
COMMENT ON TABLE workspaces IS 'User workspaces for organizing documents';
COMMENT ON TABLE sources IS 'Uploaded documents with extracted text';
COMMENT ON TABLE chat_history IS 'Chat messages between user and AI';
COMMENT ON TABLE studio_outputs IS 'Generated content (mindmaps, flashcards, etc.)';
