import axios from "axios";
import { ApiService } from "./ApiService";
import { SuccessResult, FailureResult } from "../types/result";
import { HttpError } from "../errors/http-error";

const apiInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

const api = new ApiService({ httpClient: apiInstance });

export const login = async (email: string, senha: string) => {
  try {
      const response = await apiInstance.post("", { email, senha });

      if (response instanceof SuccessResult) {
          return response.data;
      } 
      
      if (response instanceof FailureResult) {
          const error = response.error as HttpError;
          return { success: false, error: error.message || "Erro desconhecido" };
      }

      throw new Error("Resposta inválida do servidor.");
  } catch (error) {
       // ✅ Verifica se `error` é uma instância de `Error` antes de acessar `.message`
       const errorMessage = error instanceof Error ? error.message : "Erro desconhecido";
       return { success: false, error: errorMessage };
  }
};

export interface ApiResponse {
  success: boolean;
  error: string;
  message?: string;
}


export const cadastrar = async (dadosUsuario: any): Promise<ApiResponse> => {
  try {
      const response = await fetch(import.meta.env.VITE_API_URL + "/cadastro", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dadosUsuario),
      });

      const data = await response.json();

      return {
          success: response.ok,
          error: !response.ok ? data.error : undefined,
          message: response.ok ? data.message : undefined,
      };
  } catch (err) {
      return { success: false, error: "Erro ao conectar ao servidor." };
  }
};