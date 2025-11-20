/**
 * API client for backend communication
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ==================== WORKSPACE API ====================

export const workspaceAPI = {
  create: async (name: string, description?: string, userId?: string) => {
    const response = await api.post('/workspace/create', { name, description, user_id: userId || 'default_user' })
    return response.data
  },

  list: async (userId?: string) => {
    const response = await api.get(`/workspace/list?user_id=${userId || 'default_user'}`)
    return response.data
  },

  get: async (workspaceId: string) => {
    const response = await api.get(`/workspace/${workspaceId}`)
    return response.data
  },

  update: async (workspaceId: string, name?: string, description?: string) => {
    const response = await api.put(`/workspace/${workspaceId}`, { name, description })
    return response.data
  },

  delete: async (workspaceId: string) => {
    const response = await api.delete(`/workspace/${workspaceId}`)
    return response.data
  },
}

// ==================== SOURCE API ====================

export const sourceAPI = {
  upload: async (workspaceId: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('workspace_id', workspaceId)

    const response = await api.post('/sources/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  list: async (workspaceId: string) => {
    const response = await api.get(`/sources/list/${workspaceId}`)
    return response.data
  },

  get: async (sourceId: string) => {
    const response = await api.get(`/sources/${sourceId}`)
    return response.data
  },

  delete: async (sourceId: string) => {
    const response = await api.delete(`/sources/${sourceId}`)
    return response.data
  },
}

// ==================== STUDIO API ====================

export const studioAPI = {
  chat: async (workspaceId: string, prompt: string, sourceIds: string[]) => {
    // Returns EventSource for streaming
    const url = `${API_URL}/api/studio/chat`
    
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        workspace_id: workspaceId,
        prompt,
        source_ids: sourceIds,
      }),
    })
  },

  getChatHistory: async (workspaceId: string, limit?: number) => {
    const response = await api.get(`/studio/chat/history/${workspaceId}`, {
      params: { limit },
    })
    return response.data
  },

  clearChatHistory: async (workspaceId: string) => {
    const response = await api.delete(`/studio/chat/clear/${workspaceId}`)
    return response.data
  },

  generateMindmap: async (workspaceId: string, sourceIds: string[]) => {
    const response = await api.post('/studio/mindmap', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
    })
    return response.data
  },

  generateFlashcards: async (workspaceId: string, sourceIds: string[], count?: number) => {
    const response = await api.post('/studio/flashcards', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
      count,
    })
    return response.data
  },

  generateQuiz: async (workspaceId: string, sourceIds: string[], count?: number) => {
    const response = await api.post('/studio/quiz', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
      count,
    })
    return response.data
  },

  generateReport: async (workspaceId: string, sourceIds: string[], reportType?: string) => {
    const response = await api.post('/studio/report', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
      report_type: reportType,
    })
    return response.data
  },

  generateAudioOverview: async (workspaceId: string, sourceIds: string[]) => {
    const response = await api.post('/studio/audio-overview', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
    })
    return response.data
  },

  generateVideoOverview: async (workspaceId: string, sourceIds: string[]) => {
    const response = await api.post('/studio/video-overview', {
      workspace_id: workspaceId,
      source_ids: sourceIds,
    })
    return response.data
  },

  getOutputs: async (workspaceId: string, type?: string) => {
    const response = await api.get(`/studio/outputs/${workspaceId}`, {
      params: { type },
    })
    return response.data
  },

  deleteOutput: async (outputId: string) => {
    const response = await api.delete(`/studio/outputs/${outputId}`)
    return response.data
  },
}

export default api
