import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styles from "/src/app/home/styles/ObterReview.module.css";
import Button from "../../../shared/components/Button/Button";
import globalStyles from "../../../shared/components/LoginCadastro.module.css";
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

const ReviewDetalhes = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [review, setReview] = useState<Review | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReview = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/reviews/${id}`);

        if (!response.ok) {
          const data = await response.json();
          setError(data.error || "Erro ao buscar avaliação.");
          return;
        }

        const data = await response.json();
        setReview(data);
      } catch (err) {
        setError("Erro ao conectar com o servidor.");
      }
    };

    fetchReview();
  }, [id]);

  if (error) {
    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.card}>
          <p className={styles.error}>{error}</p>
          <Button onClick={() => navigate(-1)}>Voltar</Button>
        </div>
      </div>
    );
  }

  if (!review) {
    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.card}>
          <p>Carregando avaliação...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={globalStyles.container}>
      <div className={globalStyles.card}>
        <h2 className={styles.title}>Detalhes da Avaliação #{review.id}</h2>

        <div className={styles.detailItem}>
          <span className={styles.label}>Reserva ID:</span>
          <span>{review.reserva_id}</span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.label}>Sala ID:</span>
          <span>{review.sala_id}</span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.label}>Usuário ID:</span>
          <span>{review.usuario_id}</span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.label}>Nota:</span>
          
          <div className={styles.starsWrapper}>
            <StarRating rating={review.nota} editable={false} />
          </div>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.label}>Comentário:</span>
          <span>{review.comentario || "Sem comentário."}</span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.label}>Data da Avaliação:</span>
          <span>{new Date(review.data_avaliacao).toLocaleString()}</span>
        </div>

        <div className={styles.footer}>
          <Button variant="danger" onClick={() => navigate(`/reviews/${review.id}/delete`)}>
            Excluir Avaliação
          </Button>
          <Button onClick={() => navigate(`/reviews/${review.id}/edit`)}>
            Editar Avaliação
          </Button>
          <Button onClick={() => navigate('/reviews')}>
            Voltar
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ReviewDetalhes;
