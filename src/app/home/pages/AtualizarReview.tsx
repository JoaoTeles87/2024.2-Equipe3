import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Button from "../../../shared/components/Button";
import ErrorMessage from "../../../shared/components/ErrorMessage";
import StarRating from "../../../shared/components/StarRating/StarRating";
import styles from "/src/app/home/styles/AtualizarReview.module.css";
import globalStyles from "../../../shared/components/LoginCadastro.module.css";
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

const AtualizarReview = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [review, setReview] = useState<Review | null>(null);
  const [nota, setNota] = useState<number>(0);
  const [comentario, setComentario] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const fetchReview = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/reviews/${id}`);

        if (!response.ok) {
          const data = await response.json();
          setError(data.error || "Erro ao buscar avaliação.");
          return;
        }

        const data = await response.json();
        setReview(data);
        setNota(data.nota);
        setComentario(data.comentario || "");
      } catch (err) {
        setError("Erro ao conectar com o servidor.");
      }
    };

    fetchReview();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      nota,
      comentario,
    };

    try {
      const response = await fetch(`http://localhost:5000/api/reviews/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Erro ao atualizar a avaliação.");
        return;
      }

      setSuccess("Avaliação atualizada com sucesso!");
      setError("");

      setTimeout(() => {
        navigate(`/avaliacoes/${id}`); // redireciona para o detalhe da review
      }, 2000);

    } catch (err) {
      setError("Erro ao conectar com o servidor.");
    }
  };

  if (error) {
    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.card}>
          <ErrorMessage message={error} />
          <Button onClick={() => navigate(-1)}>Voltar</Button>
        </div>
      </div>
    );
  }

  if (!review) {
    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.card}>
          <p>Carregando dados da avaliação...</p>
        </div>
      </div>
    );
  }

  return (

    <div className={stylesSideBar.layoutContainer}>
      {/* Sidebar fixa à esquerda */}
      <div className={stylesSideBar.sidebarWrapper}>
        <SideBar />
      </div>

      {/* Conteúdo da página */}
      <div className={stylesSideBar.contentWrapper}>

        <div className={globalStyles.container}>
          <div className={globalStyles.card}>
            <h2 className={styles.title}>Atualizar Avaliação #{review.id}</h2>

            {success && <p className={styles.successMessage}>{success}</p>}
            {error && <ErrorMessage message={error} />}

            <form onSubmit={handleSubmit} className={styles.form}>
              <div className={styles.starsWrapper}>
                <label className={styles.label}>Nota:</label>
                <StarRating
                  rating={nota}
                  onRatingChange={(newRating) => setNota(newRating)}
                  editable={true}
                />
              </div>

              <textarea
                className={styles.textarea}
                placeholder="Comentário"
                value={comentario}
                onChange={(e) => setComentario(e.target.value)}
              />

              <div className={styles.footer}>
                <Button
                  type="submit"
                  className={styles.button}
                  style={{ backgroundColor: "#4caf50", color: "#fff", borderRadius: "5px" }}
                >
                  Atualizar Avaliação
                </Button>

                <Button onClick={() => navigate(-1)} className={styles.buttonCancel}>
                  Cancelar
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AtualizarReview;
