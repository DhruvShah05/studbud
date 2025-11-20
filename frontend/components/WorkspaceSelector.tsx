'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'
import { useStudioStore } from '../lib/store'
import { workspaceAPI, sourceAPI } from '../lib/api'
import { ChevronDown, Plus, FolderOpen } from 'lucide-react'

export default function WorkspaceSelector() {
  const { user } = useUser()
  const { currentWorkspace, setCurrentWorkspace, setSources } = useStudioStore()
  const [workspaces, setWorkspaces] = useState<any[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [newWorkspaceName, setNewWorkspaceName] = useState('')

  useEffect(() => {
    if (user) {
      loadWorkspaces()
    }
  }, [user])

  const loadWorkspaces = async () => {
    if (!user) return
    
    try {
      const data = await workspaceAPI.list(user.id)
      setWorkspaces(data)
    } catch (error) {
      console.error('Failed to load workspaces:', error)
    }
  }

  const switchWorkspace = async (workspace: any) => {
    setCurrentWorkspace(workspace)
    const sources = await sourceAPI.list(workspace.id)
    setSources(sources)
    setIsOpen(false)
  }

  const createWorkspace = async () => {
    if (!newWorkspaceName.trim() || !user) return

    try {
      const workspace = await workspaceAPI.create(newWorkspaceName, '', user.id)
      setWorkspaces([...workspaces, workspace])
      setCurrentWorkspace(workspace)
      setSources([])
      setNewWorkspaceName('')
      setIsCreating(false)
      setIsOpen(false)
    } catch (error) {
      console.error('Failed to create workspace:', error)
    }
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
      >
        <FolderOpen className="w-4 h-4 text-gray-600" />
        <span className="font-medium text-sm">{currentWorkspace?.name || 'Select Workspace'}</span>
        <ChevronDown className="w-4 h-4 text-gray-500" />
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 left-0 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-2 max-h-64 overflow-y-auto">
            {workspaces.map((workspace) => (
              <button
                key={workspace.id}
                onClick={() => switchWorkspace(workspace)}
                className={`w-full text-left px-3 py-2 rounded hover:bg-gray-100 transition-colors ${
                  currentWorkspace?.id === workspace.id ? 'bg-blue-50 text-blue-600' : ''
                }`}
              >
                <div className="font-medium text-sm">{workspace.name}</div>
                {workspace.description && (
                  <div className="text-xs text-gray-500 truncate">{workspace.description}</div>
                )}
              </button>
            ))}
          </div>

          <div className="border-t border-gray-200 p-2">
            {isCreating ? (
              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={newWorkspaceName}
                  onChange={(e) => setNewWorkspaceName(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && createWorkspace()}
                  placeholder="Workspace name"
                  className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  autoFocus
                />
                <button
                  onClick={createWorkspace}
                  className="px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  Create
                </button>
              </div>
            ) : (
              <button
                onClick={() => setIsCreating(true)}
                className="w-full flex items-center space-x-2 px-3 py-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span className="text-sm font-medium">New Workspace</span>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
