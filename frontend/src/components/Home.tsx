import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Home() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('/questions/all')
      .then(response => response.json())
      .then(data => setMessage(JSON.stringify(data)))
      .catch(error => console.error('Error fetching message:', error));
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      <p>Message from backend: {message}</p>
      <nav>
        <ul>
          <li><Link to="/question">Question Room</Link></li>
          <li><Link to="/answer">Answer Page</Link></li>
          <li><Link to="/vote">Voting Page</Link></li>
          <li><Link to="/results">Results Page</Link></li>
        </ul>
      </nav>
    </div>
  )
}

export default Home
