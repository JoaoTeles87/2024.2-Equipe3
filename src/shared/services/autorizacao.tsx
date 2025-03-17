import axios from "axios";

const apiInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { "Content-Type": "application/json" },
});

export interface ApiResponse {
  success: boolean;
  error?: string;
  message?: string;
}


export const login = async (email: string, senha: string): Promise<ApiResponse> => {
  try {
    const response = await apiInstance.post("/", { email, senha });

    if (response.status === 200 && response.data.success) {
      return { success: true, message: "Login realizado com sucesso!" };
    }

    return { success: false, error: response.data.error || "Erro no login" };
  } catch (error) {
    const errorMessage =
      axios.isAxiosError(error)
        ? error.response?.data?.error || error.message || "Erro desconhecido ao conectar ao servidor."
        : "Erro desconhecido ao conectar ao servidor.";
    return { success: false, error: errorMessage };
  }
};
export const cadastrar = async (dadosUsuario: any): Promise<ApiResponse> => {
  try {
    const response = await apiInstance.post("/cadastro", dadosUsuario);

    if (response.status === 201 && response.data.success) {
      return { success: true, message: "Cadastro realizado com sucesso!" };
    }

    return { success: false, error: response.data.error || "Erro no cadastro" };
  } catch (error) {
    const errorMessage =
      axios.isAxiosError(error)
        ? error.response?.data?.error || error.message || "Erro desconhecido ao conectar ao servidor."
        : "Erro desconhecido ao conectar ao servidor.";
    return { success: false, error: errorMessage };
  }
};
