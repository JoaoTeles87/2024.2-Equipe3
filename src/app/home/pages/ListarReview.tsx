import React, { useEffect, useState } from "react";
import styles from "/src/app/home/styles/ListarReview.module.css";
import globalStyles from "../../../shared/components/LoginCadastro.module.css";
import Button from "../../../shared/components/Button";
import { useNavigate } from "react-router-dom";
import StarRating from "../../../shared/components/StarRating";

interface Review {
  id: number;
  reserva_id: number;
  sala_id: number;
  usuario_id: number;
  nota: number;
  comentario: string;
  data_avaliacao: string;
}

const ListarReviews = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/reviews");
        if (!response.ok) {
          const data = await response.json();
          setError(data.error || "Erro ao buscar avaliações.");
          return;
        }

        const data = await response.json();
        setReviews(data);
      } catch (err) {
        setError("Erro ao conectar com o servidor.");
      }
    };

    fetchReviews();
  }, []);

  return (
    <div className={globalStyles.container}>
      <div className={globalStyles.card}>
        <h2 className={styles.title}>Lista de Avaliações</h2>

        {error && <p className={styles.error}>{error}</p>}

        {reviews.length === 0 && !error && (
          <p className={styles.subtitle}>Nenhuma avaliação encontrada.</p>
        )}

        <div className={styles.reviewsContainer}>
          {reviews.map((review) => (
            <div key={review.id} className={styles.reviewCard}>
              <h3 className={styles.reviewTitle}>Avaliação #{review.id}</h3>
              <p><strong>Reserva ID:</strong> {review.reserva_id}</p>
              <p><strong>Sala ID:</strong> {review.sala_id}</p>
              <p><strong>Usuário ID:</strong> {review.usuario_id}</p>
              <div className={styles.reviewItem}>
                <h3>Nota:</h3>
                
                <div className={styles.starsWrapper}>
                  <StarRating rating={review.nota} editable={false} />
                </div>
              </div>
              <p><strong>Comentário:</strong> {review.comentario || "Sem comentário."}</p>
              <p><strong>Data da Avaliação:</strong> {new Date(review.data_avaliacao).toLocaleDateString()}</p>
            </div>
          ))}
        </div>

        <div className={styles.footer}>
          <Button
            onClick={() => navigate("/home")}
            className={styles.button}
            style={{ backgroundColor: "#6200ea", color: "#fff", borderRadius: "5px" }}
          >
            Voltar ao Início
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ListarReviews;
