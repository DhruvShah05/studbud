'use client'

import { useEffect, useState } from 'react'
import { useUser } from '@clerk/nextjs'
import { UserButton } from '@clerk/nextjs'
import { useStudioStore } from '../../lib/store'
import { workspaceAPI, sourceAPI } from '../../lib/api'
import SourcesPanel from '../../components/SourcesPanel'
import ChatPanel from '../../components/ChatPanel'
import StudioToolsPanel from '../../components/StudioToolsPanel'
import WorkspaceSelector from '../../components/WorkspaceSelector'
import { Loader2 } from 'lucide-react'

export default function StudioPage() {
  const { user, isLoaded } = useUser()
  const [isInitializing, setIsInitializing] = useState(true)
  const { currentWorkspace, setCurrentWorkspace, setSources } = useStudioStore()

  useEffect(() => {
    if (isLoaded && user) {
      initializeWorkspace()
    }
  }, [isLoaded, user])

  const initializeWorkspace = async () => {
    if (!user) return

    try {
      // Get or create default workspace using Clerk user ID
      const workspaces = await workspaceAPI.list(user.id)
      
      let workspace
      if (workspaces.length > 0) {
        workspace = workspaces[0]
      } else {
        // Create default workspace
        workspace = await workspaceAPI.create('My Workspace', 'Default workspace', user.id)
      }

      setCurrentWorkspace(workspace)

      // Load sources for this workspace
      const sources = await sourceAPI.list(workspace.id)
      setSources(sources)

    } catch (error) {
      console.error('Failed to initialize workspace:', error)
    } finally {
      setIsInitializing(false)
    }
  }

  if (isInitializing) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading workspace...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[var(--background)] flex flex-col">
      {/* Header */}
      <header className="bg-[var(--surface)] border-b border-[var(--border)] px-8 py-5 shadow-sm">
        <div className="flex items-center justify-between max-w-[2000px] mx-auto">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] rounded-xl flex items-center justify-center shadow-md">
                <span className="text-white font-bold text-lg">S</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-[var(--text-primary)] tracking-tight">StudBud</h1>
                <p className="text-xs text-[var(--text-tertiary)]">Your AI Study Companion</p>
              </div>
            </div>
            <div className="h-8 w-px bg-[var(--border)]"></div>
            <WorkspaceSelector />
          </div>
          <div className="flex items-center gap-4">
            {user && (
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-[var(--text-primary)]">{user.firstName || user.emailAddresses[0].emailAddress}</p>
                  <p className="text-xs text-[var(--text-tertiary)]">{user.emailAddresses[0].emailAddress}</p>
                </div>
                <UserButton 
                  appearance={{
                    elements: {
                      avatarBox: "w-10 h-10"
                    }
                  }}
                />
              </div>
            )}
            <div className="px-3 py-1.5 bg-[var(--surface-hover)] rounded-lg border border-[var(--border)]">
              <span className="text-xs font-medium text-[var(--text-secondary)]">Powered by Gemini 2.5</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main 3-Panel Layout - Balanced Proportions */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Sources (25%) */}
        <div className="w-[25%] min-w-[320px] max-w-[400px] bg-[var(--surface)] border-r border-[var(--border)] flex flex-col">
          <SourcesPanel />
        </div>

        {/* Middle Panel - Chat (50%) */}
        <div className="flex-1 flex flex-col bg-[var(--background)]">
          <ChatPanel />
        </div>

        {/* Right Panel - Studio Tools (25%) */}
        <div className="w-[25%] min-w-[320px] max-w-[400px] bg-[var(--surface)] border-l border-[var(--border)] flex flex-col">
          <StudioToolsPanel />
        </div>
      </div>
    </div>
  )
}
