import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Layout } from '@/components/layout/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { VocabDeck } from '@/pages/VocabDeck'
import { WordDetail } from '@/pages/WordDetail'
import { Practice } from '@/pages/Practice'
import { QuestionBank } from '@/pages/QuestionBank'
import { ImportPage } from '@/pages/ImportPage'
import { Analytics } from '@/pages/Analytics'
import { Settings } from '@/pages/Settings'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/vocab" element={<VocabDeck />} />
          <Route path="/vocab/:wordId" element={<WordDetail />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/questions" element={<QuestionBank />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
