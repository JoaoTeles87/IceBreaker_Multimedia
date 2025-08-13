import { useState } from 'react';
import { Link } from 'react-router-dom';
import './VotingPage.css';

function VotingPage() {
  const [selected, setSelected] = useState<number | null>(null);

  const options = ['Opção 1', 'Opção 2', 'Opção 3'];

  return (
    <div className="voting-container">
      <h1>Vote na melhor resposta</h1>
      <div className="options-list">
        {options.map((option, index) => (
          <button
            key={index}
            className={`option-btn ${selected === index ? 'selected' : ''}`}
            onClick={() => setSelected(index)}
          >
            {option}
          </button>
        ))}
      </div>
      <button
        className="vote-btn"
        disabled={selected === null}
      >
        Confirmar Voto
      </button>
      <br />
      <Link to="/results" className="link-btn">Ver Ranking</Link>
    </div>
  );
}

export default VotingPage;
