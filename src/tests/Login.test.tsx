import { render, fireEvent, waitFor } from "@testing-library/react";
import Login from "../app/home/pages/Login";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import { login } from "../shared/services/autorizacao";
import * as router from "react-router-dom";

// Mock da função login
vi.mock("../shared/services/autorizacao", () => ({
  login: vi.fn(),
}));

// Mock do useNavigate com tipagem explícita
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual<typeof router>("react-router-dom");
  return {
    ...actual,
    useNavigate: vi.fn(),
  };
});

describe("Login Component", () => {
  it("Realiza o login com sucesso e redireciona", async () => {
    const mockNavigate = vi.fn();
    vi.mocked(router.useNavigate).mockReturnValue(mockNavigate);

    vi.mocked(login).mockResolvedValueOnce({
      success: true,
      message: "Login realizado com sucesso!",
    });

    const { getByPlaceholderText, getByText } = render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(getByPlaceholderText("Email"), { target: { value: "joao@gmail.com" } });
    fireEvent.change(getByPlaceholderText("Senha"), { target: { value: "123456" } });

    fireEvent.click(getByText("Entrar"));

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith("/reservas"); 
    });
  });

  it("Exibe mensagem de erro ao falhar no login", async () => {
    vi.mocked(login).mockResolvedValueOnce({
      success: false,
      error: "Usuário ou senha inválidos.",
    });

    const { getByPlaceholderText, getByText, findByText } = render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(getByPlaceholderText("Email"), { target: { value: "email_invalido@gmail.com" } });
    fireEvent.change(getByPlaceholderText("Senha"), { target: { value: "senha_invalida" } });

    fireEvent.click(getByText("Entrar"));

    expect(await findByText("Usuário ou senha inválidos.")).toBeInTheDocument();
  });
});