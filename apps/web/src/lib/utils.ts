import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}


export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"

  export async function fetcher<T = unknown>(
    url: string,
    options?: RequestInit
  ): Promise<T> {
    const fullUrl = url.startsWith("http") ? url : `${API_URL}${url}`
  
    const res = await fetch(fullUrl, options)
  
    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`)
    }
  
    return res.json()
  }