import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Word {
  id: string
  word: string
  pos?: string
  gre_definition?: string
  pithy_definition?: string
  base_word?: string
  associations: string[]
  examples: string[]
  easy_synonyms: string[]
  gre_synonyms: string[]
  story?: string
  tags: string[]
  source?: string
  created_at: string
  updated_at: string
  embedding_vector_id?: number
  srs: {
    ease: number
    interval_days: number
    next_due?: string
    repetitions: number
    last_result?: boolean
  }
}

export interface Question {
  id: string
  question_text: string
  choices?: string[]
  answer: string
  explanation?: string
  source?: string
  source_url?: string
  concepts: string[]
  difficulty: 'low' | 'medium' | 'high' | 'unknown'
  tags: string[]
  created_at: string
  embedding_vector_id?: number
}

export interface MnemonicRequest {
  word: string
  pos?: string
  style?: 'prude' | 'compact' | 'story'
  temperature?: number
}

export interface ClipRequest {
  text: string
  url: string
  title?: string
  hint?: 'auto' | 'vocab' | 'quant' | 'verbal' | 'awa'
  save?: boolean
}

export interface ExplainRequest {
  selection_text: string
  domain: 'quant' | 'verbal' | 'vocab' | 'awa'
  depth?: 'short' | 'detailed' | 'step-by-step'
  save?: boolean
}

export interface SessionStartRequest {
  mode: 'flashcard' | 'multichoice' | 'typed'
  topics?: string[]
  limit?: number
}

// API Functions
export const mnemonicAPI = {
  generate: (data: MnemonicRequest) =>
    api.post('/api/v1/mnemonic/generate', data),
  
  save: (word: Partial<Word>) =>
    api.post('/api/v1/mnemonic/save', word),
}

export const wordsAPI = {
  search: (params: { q?: string; tags?: string; limit?: number }) =>
    api.get<Word[]>('/api/v1/words/search', { params }),
  
  get: (wordId: string) =>
    api.get<Word>(`/api/v1/words/${wordId}`),
  
  update: (wordId: string, data: Partial<Word>) =>
    api.put<Word>(`/api/v1/words/${wordId}`, data),
  
  delete: (wordId: string) =>
    api.delete(`/api/v1/words/${wordId}`),
}

export const clipAPI = {
  ingest: (data: ClipRequest) =>
    api.post('/api/v1/ingest/clip', data),
}

export const explainAPI = {
  explain: (data: ExplainRequest) =>
    api.post('/api/v1/explain', data),
}

export const sessionAPI = {
  start: (data: SessionStartRequest) =>
    api.post('/api/v1/session/start', data),
  
  recordAttempt: (params: {
    item_id: string
    item_type: string
    response: string
    correct: boolean
    latency_ms: number
    session_id?: string
  }) =>
    api.post('/api/v1/session/attempt', null, { params }),
  
  stats: () =>
    api.get('/api/v1/session/stats'),
  
  end: (sessionId: string) =>
    api.post(`/api/v1/session/${sessionId}/end`),
}

export const awaAPI = {
  grade: (data: { essay_text: string; task_type: 'issue' | 'argument' }) =>
    api.post('/api/v1/awa/grade', data),
}

export const importAPI = {
  pdf: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/v1/import/pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  anki: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/v1/import/anki', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
