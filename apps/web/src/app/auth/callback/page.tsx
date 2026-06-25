'use client'

import { useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Loader2 } from 'lucide-react'

export default function AuthCallbackPage() {
  const searchParams = useSearchParams()
  const router = useRouter()

  useEffect(() => {
    const userId = searchParams.get('user_id')

    if (userId) {
      // Store user ID in localStorage
      localStorage.setItem('user_id', userId)

      // Redirect to dashboard
      router.push('/dashboard')
    } else {
      // Authentication failed
      router.push('/?error=auth_failed')
    }
  }, [searchParams, router])

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="h-12 w-12 text-purple-400 animate-spin mx-auto mb-4" />
        <p className="text-slate-300 text-lg">Completing authentication...</p>
      </div>
    </div>
  )
}
