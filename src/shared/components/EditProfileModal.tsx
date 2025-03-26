import { FaEdit } from 'react-icons/fa';
import Modal from '../../../shared/components/Modal/Modal';
import Input from '../../../shared/components/Input';
import Button from '../../../shared/components/Button/Button';
import styles from '../styles/Perfil.module.css';

interface EditProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  editData: {
    nome: string;
    email: string;
    siape?: string;
  };
  setEditData: React.Dispatch<React.SetStateAction<{
    nome: string;
    email: string;
    siape?: string;
  }>>;
  onSave: () => Promise<void>;
  isProfessor: boolean;
}

export const EditProfileModal = ({
  isOpen,
  onClose,
  editData,
  setEditData,
  onSave,
  isProfessor
}: EditProfileModalProps) => {
  const handleInputChange = (field: keyof typeof editData) => (value: string) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className={styles.modalContent}>
        <h2><FaEdit /> Editar Informações</h2>
        <div className={styles.modalForm}>
          <div className={styles.modalField}>
            <label>Nome:</label>
            <Input
              type="text"
              value={editData.nome}
              onValueChange={handleInputChange('nome')}
              placeholder="Digite seu nome"
            />
          </div>
          
          <div className={styles.modalField}>
            <label>E-mail:</label>
            <Input
              type="email"
              value={editData.email}
              onValueChange={handleInputChange('email')}
              placeholder="Digite seu e-mail"
            />
          </div>
          
          {isProfessor && (
            <div className={styles.modalField}>
              <label>SIAPE:</label>
              <Input
                type="text"
                value={editData.siape || ''}
                onValueChange={handleInputChange('siape')}
                placeholder="Digite seu SIAPE"
              />
            </div>
          )}
        </div>
        
        <div className={styles.modalActions}>
          <Button variant="secondary" onClick={onClose}>
            Cancelar
          </Button>
          <Button 
            variant="primary" 
            onClick={onSave}
            data-testid="save-profile-button"
          >
            Salvar Alterações
          </Button>
        </div>
      </div>
    </Modal>
  );
};