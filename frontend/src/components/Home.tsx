// frontend/src/pages/Home.jsx
import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
console.log("import.meta.env =", import.meta.env);
console.log("VITE_API_URL raw =", import.meta.env.VITE_API_URL);
console.log("API_BASE(final) =", import.meta.env.VITE_API_URL || "http://localhost:8000");

export default function Home() {
  const [name, setName] = useState(() => localStorage.getItem("ib_name") || "");
  const [mode, setMode] = useState(() => localStorage.getItem("ib_mode") || null); // 'host'|'join'|null
  const [sessionCode, setSessionCode] = useState(() => localStorage.getItem("ib_code") || "");
  const [sessionId, setSessionId] = useState(() => {
    const v = localStorage.getItem("ib_sessionId");
    return v ? Number(v) : null;
  });
  const [players, setPlayers] = useState<string[]>([]);
  const [, setParticipantId] = useState(() => localStorage.getItem("ib_participantId") || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Poll: se somos host, buscar players. Se somos join, checar started e redirecionar quando iniciar.
  useEffect(() => {
    let timer = null;
    async function fetchPlayers() {
      if (!sessionId) return;
      try {
        const res = await fetch(`${API_BASE}/sessions/${sessionId}/players`);
        if (!res.ok) return;
        const data = await res.json();
        setPlayers(data.players || []);
      } catch (e) {
        console.error("fetchPlayers error", e);
      }
    }

    if ((mode === "host" || mode === "join") && sessionId) {
      // primeiro fetch imediato
      fetchPlayers();
      timer = setInterval(() => {
        fetchPlayers();
        // Se for join, também checar se session started via endpoint adicional (optional)
        if (mode === "join") checkIfStartedAndRedirect();
      }, 2000);
    }

    return () => {
      if (timer) clearInterval(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, sessionId]);

  // Helper: check if session started by trying to GET session info (if backend provides it).
  async function checkIfStartedAndRedirect() {
    // OPTIONAL: if your backend exposes GET /sessions/{id} returning started flag, this will work.
    try {
      const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
      if (!res.ok) return;
      const data = await res.json(); // expected { id, code, started: true/false }
      if (data.started) {
        // go to question room
        navigate("/question");
      }
    } catch (e) {
      // ignore - endpoint may not exist
    }
  }

  // Criar sessão (host)
  const handleHost = async () => {
    setError("");
    if (!name.trim()) { setError("Digite seu nome."); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hostName: name.trim() })
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Erro criando sessão.");
      }
      const data = await res.json(); // { id, code, participant_id }
      setSessionId(data.id);
      setSessionCode(data.code);
      setParticipantId(data.participant_id || "");
      setMode("host");
      setPlayers([name.trim()]);
      // persistir no localStorage
      localStorage.setItem("ib_name", name.trim());
      localStorage.setItem("ib_mode", "host");
      localStorage.setItem("ib_code", data.code);
      localStorage.setItem("ib_sessionId", String(data.id));
      if (data.participant_id) localStorage.setItem("ib_participantId", data.participant_id);
    } catch (err) {
      console.error(err);
      setError("Erro ao criar a sala.");
    } finally {
      setLoading(false);
    }
  };

  // Entrar (join)
  const handleJoin = async () => {
    setError("");
    if (!name.trim()) { setError("Digite seu nome."); return; }
    if (!sessionCode.trim()) { setError("Digite o código da sala."); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/sessions/${sessionCode.trim()}/join`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name.trim() })
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Erro ao entrar na sala.");
      }
      const data = await res.json(); // { sessionId, code, players, participant_id }
      setSessionId(data.sessionId || null);
      setPlayers(data.players || []);
      setParticipantId(data.participant_id || "");
      setMode("join");
      localStorage.setItem("ib_name", name.trim());
      localStorage.setItem("ib_mode", "join");
      localStorage.setItem("ib_code", data.code || sessionCode.trim());
      if (data.sessionId) localStorage.setItem("ib_sessionId", String(data.sessionId));
      if (data.participant_id) localStorage.setItem("ib_participantId", data.participant_id);
    } catch (err) {
      console.error(err);
      setError("Erro ao entrar na sala. Verifique o código.");
    } finally {
      setLoading(false);
    }
  };

  // Host inicia jogo
  const handleStartGame = async () => {
    if (!sessionId) { setError("Nenhuma sessão ativa."); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/sessions/${sessionId}/start`, {
        method: "POST"
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Erro ao iniciar.");
      }
      // navega para QuestionRoom (rota requisitada)
      navigate("/question");
    } catch (err) {
      console.error(err);
      setError("Falha ao iniciar o jogo.");
    } finally {
      setLoading(false);
    }
  };

  // Clean local storage / leave
  const handleLeave = () => {
    localStorage.removeItem("ib_name");
    localStorage.removeItem("ib_mode");
    localStorage.removeItem("ib_code");
    localStorage.removeItem("ib_sessionId");
    localStorage.removeItem("ib_participantId");
    setName("");
    setMode(null);
    setSessionCode("");
    setSessionId(null);
    setParticipantId("");
    setPlayers([]);
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <h1>IceBreaker — Home</h1>

      <div style={{
        border: "1px solid #444",
        borderRadius: 8,
        padding: 18,
        background: "#0f1720",
        color: "#e6eef8",
        maxWidth: 640
      }}>
        <label style={{ display: "block", marginBottom: 8 }}>Seu nome</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Digite seu nome..."
          style={{ padding: 8, width: "100%", marginBottom: 12 }}
        />

        <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <button type="button" onClick={handleHost} disabled={loading} style={{ padding: "8px 12px" }}>
            Host
          </button>

          <input
            value={sessionCode}
            onChange={(e) => setSessionCode(e.target.value)}
            placeholder="Código da sala (para entrar)"
            style={{ padding: 8, flex: 1 }}
          />
          <button onClick={handleJoin} disabled={loading} style={{ padding: "8px 12px" }}>
            Join
          </button>
        </div>

        {error && <div style={{ color: "#ffb4b4", marginTop: 8 }}>{error}</div>}
        {loading && <div style={{ color: "#9aa", marginTop: 8 }}>Aguarde...</div>}

        {/* Host view (permanece na mesma página) */}
        {mode === "host" && sessionId && (
          <div style={{ marginTop: 16 }}>
            <div style={{ marginBottom: 8 }}>
              <strong>Sala criada!</strong>
              <div>Código: <code style={{ color: "#9cf" }}>{sessionCode}</code></div>
            </div>

            <div style={{ marginBottom: 8 }}>
              <div><strong>Jogadores na sala:</strong></div>
              <ul>
                {players.length > 0 ? players.map((p, i) => <li key={i}>{p}</li>) : <li>{name} (você)</li>}
              </ul>
            </div>

            <div>
              <button onClick={handleStartGame} disabled={loading || players.length === 0}>Iniciar jogo</button>
              <button onClick={handleLeave} style={{ marginLeft: 12 }}>Sair</button>
            </div>
          </div>
        )}

        {/* Join view (aguardando início) */}
        {mode === "join" && sessionId && (
          <div style={{ marginTop: 16 }}>
            <div>Você entrou na sala <strong>{sessionCode}</strong> como <strong>{name}</strong>.</div>
            <div style={{ marginTop: 8 }}>
              <strong>Jogadores na sala:</strong>
              <ul>{players.map((p, i) => <li key={i}>{p}</li>)}</ul>
            </div>
            <div style={{ marginTop: 8 }}>
              Aguardando início do host...
            </div>
            <div style={{ marginTop: 8 }}>
              <button onClick={handleLeave}>Sair</button>
            </div>
          </div>
        )}

        {!mode && (
          <div style={{ marginTop: 12, color: "#9aa" }}>
            Crie uma sala como host ou entre com um código existente.
          </div>
        )}
      </div>

      <nav style={{ marginTop: 18 }}>
        <ul style={{ display: "flex", gap: 12 }}>
          <li><Link to="/question">Question Room</Link></li>
          <li><Link to="/answer">Answer Page</Link></li>
          <li><Link to="/vote">Voting Page</Link></li>
          <li><Link to="/results">Results Page</Link></li>
        </ul>
      </nav>
    </div>
  );
}
