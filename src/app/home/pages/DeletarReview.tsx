import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styles from "/src/app/home/styles/DeletarReview.module.css";
import Button from "../../../shared/components/Button/Button";
import globalStyles from "../../../shared/components/LoginCadastro.module.css";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";
import SideBar from "../../../shared/components/SideBar/SideBar";

const DeletarReview = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleDelete = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/reviews/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.error || "Erro ao deletar a avaliação.");
        return;
      }

      const data = await response.json();
      setSuccess(data.mensagem || "Avaliação deletada com sucesso!");

      setTimeout(() => {
        navigate("/avaliacoes");
      }, 1500);
    } catch (err) {
      setError("Erro ao conectar com o servidor.");
    }
  };

  return (
    <div className={stylesSideBar.layoutContainer}>
      {/* Sidebar fixa à esquerda */}
      <div className={stylesSideBar.sidebarWrapper}>
        <SideBar />
      </div>

      {/* Conteúdo da página */}
      <div className={`${stylesSideBar.contentWrapper} ${styles.centeredContent}`}>
        <div className={globalStyles.card}>
          <h2 className={styles.title}>Deletar Avaliação #{id}</h2>

          {error && <p className={styles.error}>{error}</p>}
          {success && <p className={styles.success}>{success}</p>}

          {!success && (
            <>
              <p className={styles.confirmText}>
                Tem certeza que deseja excluir essa avaliação? Essa ação não pode ser desfeita!
              </p>
              <div className={styles.buttonGroup}>
                <Button onClick={handleDelete} variant="danger">
                  Confirmar Exclusão
                </Button>
                <Button onClick={() => navigate(-1)}>Cancelar</Button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>


  );
};

export default DeletarReview;
