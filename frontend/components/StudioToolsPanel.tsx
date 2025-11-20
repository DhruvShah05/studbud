'use client'

import { useState } from 'react'
import { useStudioStore } from '@/lib/store'
import { studioAPI } from '@/lib/api'
import { Brain, FileText, HelpCircle, FileBarChart, Loader2, Mic, Video, MessageSquare } from 'lucide-react'
import MindmapViewer from '../components/viewers/MindmapViewer'
import FlashcardsViewer from '../components/viewers/FlashcardsViewer'
import QuizViewer from '../components/viewers/QuizViewer'
import ReportViewer from '../components/viewers/ReportViewer'
import AudioOverviewViewer from '../components/viewers/AudioOverviewViewer'
import VideoOverviewViewer from '../components/viewers/VideoOverviewViewer'

export default function StudioToolsPanel() {
  const {
    currentWorkspace,
    selectedSourceIds,
    activePanel,
    setActivePanel,
    currentMindmap,
    setCurrentMindmap,
    currentFlashcards,
    setCurrentFlashcards,
    currentQuiz,
    setCurrentQuiz,
    currentReport,
    setCurrentReport,
    currentAudioOverview,
    setCurrentAudioOverview,
    currentVideoOverview,
    setCurrentVideoOverview,
  } = useStudioStore()

  const [isGenerating, setIsGenerating] = useState(false)

  const tools = [
    { id: 'chat', name: 'Chat', icon: MessageSquare, description: 'Ask questions', color: 'from-blue-400 to-blue-500' },
    { id: 'audio', name: 'Audio Overview', icon: Mic, description: 'Podcast script', color: 'from-purple-400 to-purple-500' },
    { id: 'video', name: 'Video Overview', icon: Video, description: 'Video script', color: 'from-orange-400 to-orange-500' },
    { id: 'mindmap', name: 'Mind Map', icon: Brain, description: 'Visual overview', color: 'from-green-400 to-green-500' },
    { id: 'flashcards', name: 'Flashcards', icon: FileText, description: 'Study cards', color: 'from-indigo-400 to-indigo-500' },
    { id: 'quiz', name: 'Quiz', icon: HelpCircle, description: 'Test yourself', color: 'from-yellow-400 to-yellow-500' },
    { id: 'report', name: 'Report', icon: FileBarChart, description: 'Summary report', color: 'from-teal-400 to-teal-500' },
  ]

  const generateContent = async (type: string) => {
    if (!currentWorkspace || selectedSourceIds.length === 0) {
      alert('Please select at least one source')
      return
    }

    setIsGenerating(true)
    try {
      switch (type) {
        case 'audio':
          const audioData = await studioAPI.generateAudioOverview(currentWorkspace.id, selectedSourceIds)
          setCurrentAudioOverview(audioData.content.script)
          break
        case 'video':
          const videoData = await studioAPI.generateVideoOverview(currentWorkspace.id, selectedSourceIds)
          setCurrentVideoOverview(videoData.content.script)
          break
        case 'mindmap':
          const mindmapData = await studioAPI.generateMindmap(currentWorkspace.id, selectedSourceIds)
          setCurrentMindmap(mindmapData.content)
          break
        case 'flashcards':
          const flashcardsData = await studioAPI.generateFlashcards(currentWorkspace.id, selectedSourceIds, 10)
          setCurrentFlashcards(flashcardsData.content.flashcards)
          break
        case 'quiz':
          const quizData = await studioAPI.generateQuiz(currentWorkspace.id, selectedSourceIds, 5)
          setCurrentQuiz(quizData.content.questions)
          break
        case 'report':
          const reportData = await studioAPI.generateReport(currentWorkspace.id, selectedSourceIds, 'summary')
          setCurrentReport(reportData.content.report)
          break
      }
    } catch (error) {
      console.error('Generation failed:', error)
      alert('Failed to generate content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleToolClick = (toolId: string) => {
    setActivePanel(toolId as any)
    if (toolId !== 'chat') {
      generateContent(toolId)
    }
  }

  return (
    <div className="flex flex-col h-full bg-[var(--surface)]">
      <div className="p-6 border-b border-[var(--border)]">
        <h2 className="text-xl font-bold text-[var(--text-primary)]">Studio Tools</h2>
        <p className="text-sm text-[var(--text-tertiary)] mt-1">Generate insights from your sources</p>
      </div>

      {/* Tool Grid */}
      <div className="grid grid-cols-2 gap-3 p-4">
        {tools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => handleToolClick(tool.id)}
            disabled={isGenerating || (tool.id !== 'chat' && selectedSourceIds.length === 0)}
            className={`group relative overflow-hidden rounded-xl p-4 transition-all duration-200 hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100 ${
              activePanel === tool.id
                ? 'ring-2 ring-[var(--primary)] shadow-md bg-[var(--surface-hover)]'
                : 'bg-[var(--surface)] border border-[var(--border)] hover:bg-[var(--surface-hover)] hover:border-[var(--primary)]'
            }`}
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${tool.color} opacity-0 group-hover:opacity-20 transition-opacity`} />
            
            <div className="relative z-10 flex flex-col items-start gap-2">
              <div className={`p-2.5 rounded-lg bg-gradient-to-br ${tool.color} shadow-sm`}>
                <tool.icon className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-sm text-[var(--text-primary)]">{tool.name}</h3>
                <p className="text-xs text-[var(--text-tertiary)] mt-0.5">{tool.description}</p>
              </div>
            </div>
            
            {isGenerating && activePanel === tool.id && (
              <div className="absolute inset-0 bg-white/90 flex items-center justify-center backdrop-blur-sm">
                <Loader2 className="w-6 h-6 animate-spin text-[var(--primary)]" />
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-hidden bg-[var(--background)]">
        {isGenerating ? (
          <div className="flex flex-col items-center justify-center h-full">
            <Loader2 className="w-16 h-16 text-[var(--primary)] animate-spin mb-4" />
            <p className="text-[var(--text-primary)] text-lg font-medium">Generating {activePanel}...</p>
            <p className="text-[var(--text-tertiary)] text-sm mt-2">This may take a moment</p>
          </div>
        ) : (
          <>
            {activePanel === 'chat' && (
              <div className="text-center py-16 text-[var(--text-tertiary)]">
                <MessageSquare className="w-20 h-20 mx-auto mb-4 opacity-30" />
                <p className="text-lg font-medium">Use the chat panel</p>
                <p className="text-sm mt-2">Ask questions about your sources</p>
              </div>
            )}

            {activePanel === 'audio' && currentAudioOverview && (
              <AudioOverviewViewer script={currentAudioOverview} />
            )}

            {activePanel === 'video' && currentVideoOverview && (
              <VideoOverviewViewer script={currentVideoOverview} />
            )}

            {activePanel === 'mindmap' && (
              <MindmapViewer data={currentMindmap} />
            )}

            {activePanel === 'flashcards' && (
              <FlashcardsViewer cards={currentFlashcards} />
            )}

            {activePanel === 'quiz' && (
              <QuizViewer questions={currentQuiz} />
            )}

            {activePanel === 'report' && (
              <ReportViewer content={currentReport} />
            )}
          </>
        )}
      </div>
    </div>
  )
}
