// SalaCard.tsx
import { useState } from 'react';
import '../styles/SalaCard.css';

type Sala = {
  id: number;
  nome: string;
  tipo: string;
  lugares: number;
  andar: number;
  equipamentos: string[];
  average_rating: number;
  review_count: number;
  reviews?: {
    autor: string;
    rating: number;
    comentario: string;
    data: string;
  }[];
};

type SalaCardProps = {
  sala: Sala;
  onReservar: () => void;
};

const SalaCard = ({ sala, onReservar }: SalaCardProps) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div
      className="sala-card"
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "16px",
        border: "1px solid #cfd8dc",
        borderRadius: "8px",
        marginBottom: "12px",
        position: "relative",
        fontFamily: "inherit",
      }}
    >
      {/* Sala Info */}
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <strong style={{ fontSize: "20px" }}>Sala {sala.nome}</strong>

        <div style={{ fontSize: "18px" }}>
          {Array.from({ length: 5 }).map((_, index) => (
            <span key={index} style={{ color: index < sala.average_rating ? "#3B3B3B" : "#ccc" }}>
              ★
            </span>
          ))}
          <span style={{ marginLeft: "6px", fontSize: "16px" }}>({sala.review_count})</span>
        </div>

        <span
          onMouseEnter={() => setShowDetails(true)}
          onMouseLeave={() => setShowDetails(false)}
          style={{
            fontSize: "14px",
            color: "#3B3B3B",
            cursor: "pointer",
            textDecoration: "underline",
          }}
        >
          (ver detalhes)

          {showDetails && (
            <div
              style={{
                position: "absolute",
                top: "50px",
                left: "16px",
                backgroundColor: "#fff",
                border: "1px solid #ccc",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                padding: "16px",
                width: "300px",
                zIndex: 10
              }}
            >
              <h4 style={{ marginBottom: "8px" }}>{sala.nome}</h4>
              <p>⭐ {sala.average_rating} ({sala.review_count} avaliações)</p>
              <p>🪑 {sala.lugares} Lugares</p>
              <p>🏢 {sala.andar}º Andar</p>
              <p>📍 {sala.tipo}</p>
              <ul>
                {sala.equipamentos.map(eq => (
                  <li key={eq}>🔧 {eq}</li>
                ))}
              </ul>

              {sala.reviews && (
                <div style={{ marginTop: "10px" }}>
                  <h4>Avaliações ({sala.review_count})</h4>
                  {sala.reviews.map((r, i) => (
                    <div key={i} style={{ marginBottom: "8px" }}>
                      <strong>{r.autor}</strong> - ⭐ {r.rating} - {r.data}
                      <p>{r.comentario}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </span>
      </div>

      {/* Reservar Button */}
      <button
        onClick={onReservar}
        style={{
          padding: "8px 16px",
          border: "2px solid #6c47ff",
          backgroundColor: "transparent",
          color: "#6c47ff",
          fontWeight: "bold",
          borderRadius: "8px",
          cursor: "pointer",
        }}
      >
        Reservar
      </button>
    </div>
  );
};

export default SalaCard;