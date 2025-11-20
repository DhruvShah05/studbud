'use client'

import { useEffect, useState } from 'react'
import { useUser } from '@clerk/nextjs'
import axios from 'axios'

export default function UserSync() {
  const { user, isLoaded } = useUser()
  const [syncError, setSyncError] = useState<string | null>(null)

  useEffect(() => {
    if (isLoaded && user) {
      syncUser()
    }
  }, [isLoaded, user])

  const syncUser = async () => {
    if (!user) return

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
      
      const response = await axios.post(`${API_URL}/api/auth/sync-user`, {
        clerk_user_id: user.id,
        email: user.emailAddresses[0]?.emailAddress,
        first_name: user.firstName,
        last_name: user.lastName,
        profile_image_url: user.imageUrl
      })
      
      console.log('✅ User synced successfully:', response.data)
      setSyncError(null)
    } catch (error: any) {
      const errorMsg = error.response?.data?.error || error.message || 'Unknown error'
      console.error('❌ Failed to sync user:', errorMsg)
      setSyncError(errorMsg)
      
      // Show alert for critical sync errors
      if (error.response?.status === 500) {
        alert(`Failed to sync user account: ${errorMsg}\n\nPlease refresh the page or contact support.`)
      }
    }
  }

  // Show error banner if sync fails
  if (syncError) {
    return (
      <div className="fixed top-0 left-0 right-0 bg-red-600 text-white px-4 py-2 text-center text-sm z-50">
        ⚠️ Account sync error: {syncError}
      </div>
    )
  }

  return null
}
