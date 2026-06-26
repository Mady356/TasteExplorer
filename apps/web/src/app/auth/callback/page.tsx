'use client'

import { Suspense } from 'react'
import AuthCallbackContent from './AuthCallbackContent'

export const dynamic = 'force-dynamic'

export default function AuthCallbackPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-300">Loading...</div>}>
      <AuthCallbackContent />
    </Suspense>
  )
}