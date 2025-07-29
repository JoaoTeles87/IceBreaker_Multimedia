import { Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import QuestionRoom from './components/QuestionRoom'
import AnswerPage from './components/AnswerPage'
import VotingPage from './components/VotingPage'
import ResultsPage from './components/ResultsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/question" element={<QuestionRoom />} />
      <Route path="/answer" element={<AnswerPage />} />
      <Route path="/vote" element={<VotingPage />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  )
}

export default App
