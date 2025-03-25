import { useState, useEffect } from 'react';
import { FaEdit, FaTrash, FaStar, FaUser, FaTimes } from 'react-icons/fa';
import styles from '../styles/Perfil.module.css';
import Button from '../../../shared/components/Button/Button';
import Input from '../../../shared/components/Input';
import ErrorMessage from '../../../shared/components/ErrorMessage';
import Modal from '../../../shared/components/Modal/Modal';
import SideBar from "../../../shared/components/SideBar/SideBar";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";

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
  horario?: string;
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

const API_URL = 'http://127.0.0.1:5000';

const Perfil = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [nextReservation, setNextReservation] = useState<Reserva | null>(null);
  const [reservationHistory, setReservationHistory] = useState<Reserva[]>([]);
  const [error, setError] = useState('');
  const [editData, setEditData] = useState<EditProfileData>({
    nome: '',
    email: '',
    siape: ''
  });
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState<DeleteConfirmation>({ senha: '' });
  const [deleteError, setDeleteError] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    if (profile) {
      fetchReservations();
      fetchHistorico();
    }
  }, [profile]);

  const fetchProfile = async () => {
    try {
      setError('');
      const response = await fetch(`${API_URL}/api/perfil`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao carregar perfil');
      }

      const data = await response.json();
      setProfile(data);
      setEditData({
        nome: data.nome || '',
        email: data.email || '',
        siape: data.siape || ''
      });
    } catch (err) {
      setError('Erro ao carregar dados do perfil');
    }
  };

  const fetchReservations = async () => {
    if (!profile) return;
    try {
      setError('');
      const response = await fetch(`${API_URL}/api/reservas/ativas`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      if (Array.isArray(data)) {
        const activeReservations = data.filter(r => r.status === 'ativa');
        const inactiveReservations = data.filter(r => r.status === 'inativa');
        setNextReservation(activeReservations[0] || null);
        setReservationHistory(inactiveReservations);
      }
    } catch (err) {
      setError('Erro ao carregar reservas');
    }
  };

  const fetchHistorico = async () => {
    if (!profile) return;
    
    try {
      const response = await fetch(`${API_URL}/api/reservas/historico/${profile.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao carregar histórico');
      }

      const data = await response.json();
      setReservationHistory(data.historico || []);
    } catch (err) {
      setError('Erro ao carregar histórico de reservas');
    }
  };

  const formatarData = (dataString: string) => {
    const [ano, mes, dia] = dataString.split('-');
    return `${dia}/${mes}/${ano}`;
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
      const response = await fetch(`${API_URL}/api/perfil`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao atualizar perfil');
      }

      setProfile(prev => prev ? { ...prev, ...editData } : null);
      setIsEditModalOpen(false);
      alert('Perfil atualizado com sucesso!');
    } catch (err: any) {
      setError(err.message || 'Erro ao atualizar perfil');
    }
  };

  const handleDeleteReservation = async (id: number) => {
    if (!window.confirm('Tem certeza que deseja cancelar esta reserva?')) return;

    try {
      const response = await fetch(`${API_URL}/api/reservas/ativas/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao cancelar reserva');
      }

      await fetchReservations();
      setNextReservation(null);
      alert('Reserva cancelada com sucesso!');
    } catch (err: any) {
      setError(err.message || 'Erro ao cancelar reserva');
    }
  };

  const handleDeleteClick = () => {
    setIsDeleteModalOpen(true);
    setDeleteError('');
  };

  const handleConfirmDelete = async () => {
    try {
      // Verifica se há reserva ativa
      if (nextReservation) {
        setDeleteError('Não é possível excluir a conta enquanto houver reservas ativas. Por favor, cancele todas as reservas primeiro.');
        return;
      }

      const response = await fetch(`${API_URL}/api/perfil`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: profile?.id,
          senha: deleteConfirmation.senha
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        setDeleteError(errorData.error);
        return;
      }

      setProfile(null);
      setNextReservation(null);
      setReservationHistory([]);
      setDeleteConfirmation({ senha: '' });
      setIsDeleteModalOpen(false);
      window.location.href = '/';
    } catch (err: any) {
      setDeleteError(err.message || 'Erro ao excluir perfil');
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
      <div className={stylesSideBar.sidebarWrapper}>
        <SideBar />
      </div>
      
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
                          <p>Horário: {reserva.horario || `${reserva.start_time} às ${reserva.end_time}`}</p>
                        </div>
                        <div className={styles.reservationDetails}>
                          {(reserva.avaliacao && reserva.avaliacao > 0) && (
                            <div className={styles.rating}>
                              {renderStars(reserva.avaliacao)}
                              <span className={styles.ratingValue}>
                                ({reserva.avaliacao}/5)
                              </span>
                            </div>
                          )}
                          {reserva.comentario && (
                            <div className={styles.commentContainer}>
                              {/* <strong>Comentário:</strong> */}
                              <p className={styles.comment}>{reserva.comentario}</p>
                            </div>
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
              <p>Perfil não encontrado</p>
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