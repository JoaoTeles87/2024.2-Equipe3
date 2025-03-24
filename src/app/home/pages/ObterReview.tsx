import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styles from "/src/app/home/styles/ObterReview.module.css";
import Button from "../../../shared/components/Button/Button";
import globalStyles from "../../../shared/components/LoginCadastro.module.css";
import StarRating from "../../../shared/components/StarRating/StarRating";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";
import SideBar from "../../../shared/components/SideBar/SideBar";

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
      <div className={styles.pageContainer}>
        <div className={stylesSideBar.layoutContainer}>

          {/* Sidebar */}
          <div className={stylesSideBar.sidebarWrapper}>
            <SideBar />
          </div>

          {/* Conteúdo principal */}
          <div className={stylesSideBar.contentWrapper}>
            <div className={globalStyles.container}>
              <div className={globalStyles.card}>
                <p className={styles.error}>{error}</p>
                <div className={styles.footer}>
                  <Button className={styles.button} onClick={() => navigate(-1)}>
                    Voltar
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!review) {
    return (
      <div className={styles.pageContainer}>
        <div className={stylesSideBar.layoutContainer}>

          {/* Sidebar */}
          <div className={stylesSideBar.sidebarWrapper}>
            <SideBar />
          </div>

          {/* Conteúdo principal */}
          <div className={stylesSideBar.contentWrapper}>
            <div className={globalStyles.container}>
              <div className={globalStyles.card}>
                <p>Carregando avaliação...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }


  return (
    <div className={styles.pageContainer}>
      <div className={stylesSideBar.layoutContainer}>

        {/* Sidebar */}
        <div className={stylesSideBar.sidebarWrapper}>
          <SideBar />
        </div>

        {/* Conteúdo da Página */}
        <div className={stylesSideBar.contentWrapper}>
          <div className={globalStyles.container}>
            <div className={globalStyles.card}>
              <h2 className={styles.title}>Detalhes da Avaliação #{review.id}</h2>

              <div className={styles.detailItem}>
                <span className={styles.label}>ID da Reserva:</span>
                <span>{review.reserva_id}</span>
              </div>

              <div className={styles.detailItem}>
                <span className={styles.label}>ID da Sala:</span>
                <span>{review.sala_id}</span>
              </div>

              <div className={styles.detailItem}>
                <span className={styles.label}>ID do Usuário:</span>
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
                <div className={styles.comentario}>{review.comentario || "Sem comentário."}</div>
              </div>

              <div className={styles.detailItem}>
                <span className={styles.label}>Data da Avaliação:</span>
                <span>{new Date(review.data_avaliacao).toLocaleString()}</span>
              </div>

              <div className={styles.footer}>
                <Button variant="danger" onClick={() => navigate(`/avaliacoes/${review.id}/delete`)}>
                  Excluir Avaliação
                </Button>
                <Button onClick={() => navigate(`/avaliacoes/${review.id}/edit`)}>
                  Editar Avaliação
                </Button>
                <Button onClick={() => navigate('/avaliacoes')}>
                  Voltar
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  );
};

export default ReviewDetalhes;
