import { useState, useEffect } from 'react';
import { FaEdit, FaTrash, FaStar, FaUser, FaTimes } from 'react-icons/fa';
import styles from '../styles/Perfil.module.css';
import Button from '../../../shared/components/Button/Button';
import Input from '../../../shared/components/Input';
import ErrorMessage from '../../../shared/components/ErrorMessage';
import Modal from '../../../shared/components/Modal/Modal';
import SideBar from "../../../shared/components/SideBar/SideBar";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";
import Dropdown from 'react-bootstrap/Dropdown';

interface UserProfile {
  id: number;
  nome: string;
  cpf: string;
  email: string;
  professor: string;
  siape?: string;
}

interface Sala {
  id: number;
  nome: string;
  tipo: string;
  lugares: number;
  andar: number;
  equipamentos: string[];
  average_rating: number;
  review_count: number;
}

interface Reserva {
  id: number;
  sala_id: number;
  professor_id: number;
  data: string;
  start_time: string;
  end_time: string;
  status: string;
  sala?: Sala;
  comentario?: string;
  avaliacao?: number;
}

interface EditProfileData {
  nome: string;
  email: string;
  siape?: string;
}

interface DeleteConfirmation {
  senha: string;
}

const Perfil = () => {
  const [profile, setProfile] = useState<UserProfile | null>({
    id: 1,
    nome: "Carlos Santos",
    cpf: "022.488.144-29",
    email: "CarloSan@gmail.com",
    professor: "S",
    siape: "123456"
  });
  const [nextReservation, setNextReservation] = useState<Reserva | null>(null);
  const [reservationHistory, setReservationHistory] = useState<Reserva[]>([]);
  const [error, setError] = useState('');
  const [editData, setEditData] = useState<EditProfileData>({
    nome: "Carlos Santos",
    email: "CarloSan@gmail.com",
    siape: "123456"
  });
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState<DeleteConfirmation>({ senha: '' });
  const [deleteError, setDeleteError] = useState('');

  useEffect(() => {
    if (profile) {
      fetchReservations();
    }
  }, [profile]);

  const formatarData = (dataString: string) => {
    const [ano, mes, dia] = dataString.split('-');
    return `${dia}/${mes}/${ano}`;
  };

  const fetchReservations = async () => {
    try {
      const reservas: Reserva[] = [
        {
          id: 1,
          sala_id: 1,
          professor_id: 1,
          data: "2024-12-01",
          start_time: "10:00",
          end_time: "12:00",
          status: "ativa",
          sala: {
            id: 1,
            nome: "Sala 101",
            tipo: "Sala de Aula",
            lugares: 30,
            andar: 1,
            equipamentos: ["Projetor", "Quadro Branco"],
            average_rating: 4.5,
            review_count: 10
          }
        },
        {
          id: 2,
          sala_id: 2,
          professor_id: 1,
          data: "2023-09-25",
          start_time: "14:00",
          end_time: "16:00",
          status: "inativa",
          sala: {
            id: 2,
            nome: "Sala 102",
            tipo: "Laboratório",
            lugares: 20,
            andar: 2,
            equipamentos: ["Computadores", "Projetor"],
            average_rating: 4.0,
            review_count: 8
          },
          comentario: "Boa sala, mas faltou ar condicionado.",
          avaliacao: 4
        }
      ];

      const nextReserva = reservas.find(r => r.status === 'ativa');
      const historico = reservas.filter(r => r.status === 'inativa');

      setNextReservation(nextReserva || null);
      setReservationHistory(historico);

    } catch (err) {
      setError('Erro ao carregar reservas');
    }
  };

  const handleEdit = () => {
    setEditData({
      nome: profile?.nome || '',
      email: profile?.email || '',
      siape: profile?.siape
    });
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = async () => {
    try {
      setProfile(prev => prev ? { ...prev, ...editData } : null);
      setIsEditModalOpen(false);
    } catch (err) {
      setError('Erro ao atualizar perfil');
    }
  };

  const handleDeleteReservation = async (id: number) => {
    if (!window.confirm('Tem certeza que deseja cancelar esta reserva?')) return;

    try {
      setReservationHistory(prev => prev.filter(reserva => reserva.id !== id));
      if (nextReservation?.id === id) {
        setNextReservation(null);
      }
    } catch (err) {
      setError('Erro ao cancelar reserva');
    }
  };

  const handleDeleteClick = () => {
    setIsDeleteModalOpen(true);
    setDeleteError('');
  };

  const handleConfirmDelete = async () => {
    try {
      if (nextReservation) {
        setDeleteError('Não é possível excluir a conta enquanto houver reservas ativas. Por favor, cancele as reservas antes de excluir a conta.');
        return;
      }

      if (deleteConfirmation.senha !== "123456") {
        setDeleteError('Senha incorreta. Por favor, tente novamente.');
        return;
      }

      setProfile(null);
      setNextReservation(null);
      setReservationHistory([]);
      setDeleteConfirmation({ senha: '' });
      setIsDeleteModalOpen(false);

      window.location.href = 'http://localhost:3000';
    } catch (err: any) {
      setDeleteError(err.message);
    }
  };

  const renderStars = (rating: number) => {
    return Array(5).fill(0).map((_, index) => (
      <FaStar
        key={index}
        className={index < rating ? styles.starFilled : styles.starEmpty}
      />
    ));
  };

  return (
    <div className={styles.layoutContainer}>
    {/* Sidebar fixa à esquerda */}
    <div className={stylesSideBar.sidebarWrapper}>
        <SideBar />
    </div>
    
    {/* Conteúdo da página */}
    <div className={stylesSideBar.contentWrapper}>
    <div className={styles.container}>
      {error && <ErrorMessage message={error} />}

      {profile ? (
        <>
          <div className={styles.profileSection}>
            <div className={styles.profileField}>
              <span className={styles.label}>Nome:</span>
              <span className={styles.value}>{profile.nome}</span>
              <div className={styles.actionButtons}>
                <div className={styles.editButton} onClick={handleEdit}>
                  <FaEdit className={styles.editIcon} />
                  <span>Editar</span>
                </div>
                <Button
                  onClick={handleDeleteClick}
                  variant="danger"
                  className={styles.deleteAccountOutline}
                >
                  Excluir conta
                </Button>
              </div>
            </div>

            <div className={styles.profileField}>
              <span className={styles.label}>CPF:</span>
              <span className={styles.value}>{profile.cpf}</span>
            </div>

            <div className={styles.profileField}>
              <span className={styles.label}>E-mail:</span>
              <span className={styles.value}>{profile.email}</span>
            </div>

            {profile.professor === 'S' && (
              <div className={styles.profileField}>
                <span className={styles.label}>SIAPE:</span>
                <span className={styles.value}>{profile.siape}</span>
              </div>
            )}
          </div>

          <div className={styles.reservationSection}>
            <h2 className={styles.reservationTitle}>Próxima Reserva</h2>
            {nextReservation ? (
              <div className={styles.reservationCard}>
                <div className={styles.reservationHeader}>
                  <p>Sala: {nextReservation.sala?.nome}</p>
                  <Button
                    onClick={() => handleDeleteReservation(nextReservation.id)}
                    variant="danger"
                    className={styles.deleteButton}
                  >
                    <FaTrash /> Excluir
                  </Button>
                </div>
                <p>Data: {formatarData(nextReservation.data)}</p>
                <p>Horário: {nextReservation.start_time} às {nextReservation.end_time}</p>
              </div>
            ) : (
              <div className={styles.emptyMessage}>
                <p>Não há reservas ativas no momento</p>
              </div>
            )}
          </div>

          <div className={styles.historySection}>
            <h2 className={styles.reservationTitle}>Histórico de Reservas</h2>
            {reservationHistory.length > 0 ? (
              reservationHistory.map((reserva) => (
                <div key={reserva.id} className={styles.reservationCard}>
                  <div className={styles.reservationContent}>
                    <div className={styles.reservationInfo}>
                      <p>Sala: {reserva.sala?.nome}</p>
                      <p>Data: {formatarData(reserva.data)}</p>
                      <p>Horário: {reserva.start_time} às {reserva.end_time}</p>
                    </div>
                    <div className={styles.reservationDetails}>
                      {reserva.avaliacao && (
                        <div className={styles.rating}>
                          {renderStars(reserva.avaliacao)}
                        </div>
                      )}
                      {reserva.comentario && (
                        <p className={styles.comment}>{reserva.comentario}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className={styles.emptyMessage}>
                <p>Não há histórico de reservas</p>
              </div>
            )}
          </div>
        </>
      ) : (
        <div className={styles.emptyMessage}>
          <p>Perfil excluído com sucesso.</p>
        </div>
      )}

      <Modal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)}>
        <div className={styles.modalContent}>
          <h2>Editar Informações</h2>
          <div className={styles.modalForm}>
            <div className={styles.modalField}>
              <label>Nome:</label>
              <Input
                type="text"
                value={editData.nome}
                onValueChange={(value) => setEditData(prev => ({ ...prev, nome: value }))}
              />
            </div>
            <div className={styles.modalField}>
              <label>E-mail:</label>
              <Input
                type="email"
                value={editData.email}
                onValueChange={(value) => setEditData(prev => ({ ...prev, email: value }))}
              />
            </div>
            {profile?.professor === 'S' && (
              <div className={styles.modalField}>
                <label>SIAPE:</label>
                <Input
                  type="text"
                  value={editData.siape || ''}
                  onValueChange={(value) => setEditData(prev => ({ ...prev, siape: value }))}
                />
              </div>
            )}
          </div>
          <div className={styles.modalActions}>
            <Button variant="secondary" onClick={() => setIsEditModalOpen(false)}>
              Cancelar
            </Button>
            <Button variant="primary" onClick={handleSaveEdit}>
              Salvar alterações
            </Button>
          </div>
        </div>
      </Modal>

      <Modal isOpen={isDeleteModalOpen} onClose={() => setIsDeleteModalOpen(false)}>
        <div className={styles.modalContent}>
          <div className={styles.deleteIcon}>
            <FaUser />
            <FaTimes className={styles.times} />
          </div>
          <h2 className={styles.deleteTitle}>Excluir Conta</h2>
          <p className={styles.deleteWarning}>
            Tem certeza que deseja excluir conta? Essa ação é irreversível.
          </p>
          <div className={styles.modalField}>
            <label>Digite sua senha para confirmar:</label>
            <Input
              type="password"
              value={deleteConfirmation.senha}
              onValueChange={(value) => setDeleteConfirmation({ senha: value })}
            />
          </div>
          {deleteError && <p className={styles.errorMessage}>{deleteError}</p>}
          <div className={styles.modalActions}>
            <Button variant="secondary" onClick={() => setIsDeleteModalOpen(false)}>
              Cancelar
            </Button>
            <Button variant="danger" onClick={handleConfirmDelete}>
              Excluir conta
            </Button>
          </div>
        </div>
      </Modal>
    </div>
    </div>
    </div>
  );
};

export default Perfil;