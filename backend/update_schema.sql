-- Update studio_outputs table to support new output types
-- Run this in Supabase SQL Editor

ALTER TABLE studio_outputs DROP CONSTRAINT IF EXISTS studio_outputs_output_type_check;

ALTER TABLE studio_outputs ADD CONSTRAINT studio_outputs_output_type_check 
CHECK (output_type IN ('mindmap', 'flashcards', 'quiz', 'report', 'audio_overview', 'video_overview'));
