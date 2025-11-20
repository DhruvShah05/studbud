'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useUser } from '@clerk/nextjs'
import { BookOpen, Sparkles, FileText, Brain, Mic, Video, Zap } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  const router = useRouter()
  const { isSignedIn, isLoaded } = useUser()

  useEffect(() => {
    // If user is signed in, redirect to studio
    if (isLoaded && isSignedIn) {
      router.push('/studio')
    }
  }, [isLoaded, isSignedIn, router])

  return (
    <main className="min-h-screen bg-[var(--background)] flex flex-col">
      {/* Hero Section */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-4xl">
          <div className="flex justify-center mb-8">
            <div className="relative">
              <div className="w-24 h-24 bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] rounded-2xl flex items-center justify-center shadow-2xl">
                <span className="text-white font-bold text-4xl">S</span>
              </div>
              <Sparkles className="w-10 h-10 text-[var(--accent)] absolute -top-2 -right-2 animate-pulse" />
            </div>
          </div>
          
          <h1 className="text-6xl font-bold mb-6 text-[var(--text-primary)]">
            Welcome to StudBud
          </h1>
          
          <p className="text-2xl text-[var(--text-secondary)] mb-12">
            Your AI-powered study companion. Transform documents into podcasts, flashcards, quizzes, and more.
          </p>
          
          <div className="flex gap-4 justify-center mb-16">
            <Link 
              href="/sign-up"
              className="px-8 py-4 bg-[var(--primary)] hover:bg-[var(--primary-hover)] text-white rounded-xl font-semibold text-lg shadow-lg transition-all hover:scale-105"
            >
              Get Started Free
            </Link>
            <Link 
              href="/sign-in"
              className="px-8 py-4 bg-[var(--surface)] hover:bg-[var(--surface-hover)] text-[var(--text-primary)] rounded-xl font-semibold text-lg border-2 border-[var(--border)] transition-all hover:scale-105"
            >
              Sign In
            </Link>
          </div>
          
          {/* Features Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            <div className="bg-[var(--surface)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
              <Mic className="w-10 h-10 text-purple-500 mx-auto mb-3" />
              <p className="text-sm font-semibold text-[var(--text-primary)]">Audio Overview</p>
              <p className="text-xs text-[var(--text-tertiary)] mt-1">AI Podcasts</p>
            </div>
            <div className="bg-[var(--surface)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
              <Video className="w-10 h-10 text-orange-500 mx-auto mb-3" />
              <p className="text-sm font-semibold text-[var(--text-primary)]">Video Scripts</p>
              <p className="text-xs text-[var(--text-tertiary)] mt-1">Study Videos</p>
            </div>
            <div className="bg-[var(--surface)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
              <Brain className="w-10 h-10 text-green-500 mx-auto mb-3" />
              <p className="text-sm font-semibold text-[var(--text-primary)]">Mind Maps</p>
              <p className="text-xs text-[var(--text-tertiary)] mt-1">Visual Learning</p>
            </div>
            <div className="bg-[var(--surface)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
              <Zap className="w-10 h-10 text-yellow-500 mx-auto mb-3" />
              <p className="text-sm font-semibold text-[var(--text-primary)]">Flashcards</p>
              <p className="text-xs text-[var(--text-tertiary)] mt-1">Quick Review</p>
            </div>
          </div>
          
          <div className="mt-12 flex items-center justify-center gap-2">
            <Sparkles className="w-5 h-5 text-[var(--accent)]" />
            <p className="text-sm text-[var(--text-tertiary)]">Powered by Gemini 2.5 Flash</p>
          </div>
        </div>
      </div>
    </main>
  )
}
