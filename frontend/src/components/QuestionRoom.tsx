import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

type Question = {
  category: string;
  difficulty: string;
  text: string;
};

function QuestionRoom() {
  const [question, setQuestion] = useState<Question | null>(null);

  useEffect(() => {
    fetch('/questions/random')
      .then(response => response.json())
      .then(data => setQuestion(data))
      .catch(error => console.error('Error fetching question:', error));
  }, []);

  return (
    <div>
      <h1>Question Room</h1>
      {question ? (
        <div>
          <p>Category: {question.category}</p>
          <p>Difficulty: {question.difficulty}</p>
          <p>Question: {question.text}</p>
        </div>
      ) : (
        <p>Loading question...</p>
      )}
      <Link to="/">Go to Home</Link>
    </div>
  )
}

export default QuestionRoom
