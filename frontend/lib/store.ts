/**
 * Global state management with Zustand
 */
import { create } from 'zustand'

export interface Source {
  id: string
  workspace_id: string
  filename: string
  file_type: string
  file_url: string
  extracted_text: string
  created_at: string
}

export interface Workspace {
  id: string
  user_id: string
  name: string
  description: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: string
  workspace_id: string
  role: 'user' | 'assistant'
  content: string
  source_ids: string[]
  created_at: string
}

interface StudioStore {
  // Current workspace
  currentWorkspace: Workspace | null
  setCurrentWorkspace: (workspace: Workspace | null) => void

  // Sources
  sources: Source[]
  setSources: (sources: Source[]) => void
  addSource: (source: Source) => void
  removeSource: (sourceId: string) => void

  // Selected sources for operations
  selectedSourceIds: string[]
  setSelectedSourceIds: (ids: string[]) => void
  toggleSourceSelection: (id: string) => void

  // Chat
  chatMessages: ChatMessage[]
  setChatMessages: (messages: ChatMessage[]) => void
  addChatMessage: (message: ChatMessage) => void

  // UI state
  activePanel: 'chat' | 'audio' | 'video' | 'mindmap' | 'flashcards' | 'quiz' | 'report'
  setActivePanel: (panel: 'chat' | 'audio' | 'video' | 'mindmap' | 'flashcards' | 'quiz' | 'report') => void

  // Loading states
  isLoading: boolean
  setIsLoading: (loading: boolean) => void

  // Current outputs
  currentMindmap: any
  setCurrentMindmap: (mindmap: any) => void

  currentFlashcards: any[]
  setCurrentFlashcards: (flashcards: any[]) => void

  currentQuiz: any[]
  setCurrentQuiz: (quiz: any[]) => void

  currentReport: string
  setCurrentReport: (report: string) => void

  currentAudioOverview: string
  setCurrentAudioOverview: (audio: string) => void

  currentVideoOverview: string
  setCurrentVideoOverview: (video: string) => void
}

export const useStudioStore = create<StudioStore>((set) => ({
  // Workspace
  currentWorkspace: null,
  setCurrentWorkspace: (workspace) => set({ currentWorkspace: workspace }),

  // Sources
  sources: [],
  setSources: (sources) => set({ sources }),
  addSource: (source) => set((state) => ({ sources: [...state.sources, source] })),
  removeSource: (sourceId) =>
    set((state) => ({
      sources: state.sources.filter((s) => s.id !== sourceId),
      selectedSourceIds: state.selectedSourceIds.filter((id) => id !== sourceId),
    })),

  // Selected sources
  selectedSourceIds: [],
  setSelectedSourceIds: (ids) => set({ selectedSourceIds: ids }),
  toggleSourceSelection: (id) =>
    set((state) => ({
      selectedSourceIds: state.selectedSourceIds.includes(id)
        ? state.selectedSourceIds.filter((sid) => sid !== id)
        : [...state.selectedSourceIds, id],
    })),

  // Chat
  chatMessages: [],
  setChatMessages: (messages) => set({ chatMessages: messages }),
  addChatMessage: (message) =>
    set((state) => ({ chatMessages: [...state.chatMessages, message] })),

  // UI
  activePanel: 'chat',
  setActivePanel: (panel) => set({ activePanel: panel }),

  // Loading
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),

  // Outputs
  currentMindmap: null,
  setCurrentMindmap: (mindmap) => set({ currentMindmap: mindmap }),

  currentFlashcards: [],
  setCurrentFlashcards: (flashcards) => set({ currentFlashcards: flashcards }),

  currentQuiz: [],
  setCurrentQuiz: (quiz) => set({ currentQuiz: quiz }),

  currentReport: '',
  setCurrentReport: (report) => set({ currentReport: report }),

  currentAudioOverview: '',
  setCurrentAudioOverview: (audio) => set({ currentAudioOverview: audio }),

  currentVideoOverview: '',
  setCurrentVideoOverview: (video) => set({ currentVideoOverview: video }),
}))
