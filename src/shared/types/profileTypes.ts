// src/types/profileTypes.ts
export interface UserProfile {
    id: number;
    nome: string;
    cpf: string;
    email: string;
    professor: string;
    siape?: string;
  }
  
  export interface Sala {
    id: number;
    nome: string;
    tipo: string;
    lugares: number;
    andar: number;
    equipamentos: string[];
    average_rating: number;
    review_count: number;
  }
  
  export interface Reserva {
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
  
  export interface EditProfileData {
    nome: string;
    email: string;
    siape?: string;
  }
  
  export interface DeleteConfirmation {
    senha: string;
  }