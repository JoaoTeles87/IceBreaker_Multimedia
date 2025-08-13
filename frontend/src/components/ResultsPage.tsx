import { Link } from 'react-router-dom';
import './ResultsPage.css';

function ResultsPage() {
  const ranking = [
    { name: 'Jogador 1', points: 120 },
    { name: 'Jogador 2', points: 100 },
    { name: 'Jogador 3', points: 80 },
    { name: 'Jogador 4', points: 60 },
  ];

  return (
    <div className="ranking-container">
      <h1>Ranking Final da Rodada</h1>
      {ranking.map((player, index) => (
        <div
          key={index}
          className={`ranking-item ${
            index === 0
              ? 'first'
              : index === 1
              ? 'second'
              : index === 2
              ? 'third'
              : ''
          }`}
        >
          <span>{index + 1}. {player.name}</span>
          <span>{player.points} pts</span>
        </div>
      ))}
      <Link to="/" className="link-btn">Voltar para Home</Link>
    </div>
  );
}

export default ResultsPage;
