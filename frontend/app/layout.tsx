import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ClerkProvider } from '@clerk/nextjs'
import UserSync from '../components/UserSync'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'StudBud - Your AI Study Companion',
  description: 'Transform your documents into podcasts, flashcards, quizzes, and more with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          <UserSync />
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
