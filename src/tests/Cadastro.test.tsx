import { render, fireEvent } from "@testing-library/react";
import Cadastro from "../app/home/pages/Cadastro";
import { describe, it, expect, vi } from "vitest";
import { cadastrar } from "../shared/services/autorizacao"; 
import { MemoryRouter } from "react-router-dom";

vi.mock("../shared/services/autorizacao", () => ({
  cadastrar: vi.fn(),
}));

describe("Cadastro Component", () => {
  it("Realiza o cadastro com sucesso", async () => {
    vi.mocked(cadastrar).mockResolvedValueOnce({
      success: true,
      message: "Cadastro realizado com sucesso!",
    });

    const { getByPlaceholderText, getByText, findByText } = render(
      <MemoryRouter>
        <Cadastro />
      </MemoryRouter>
    );

    fireEvent.change(getByPlaceholderText("Nome"), { target: { value: "João" } });
    fireEvent.change(getByPlaceholderText("CPF"), { target: { value: "123.456.789-00" } });
    fireEvent.change(getByPlaceholderText("Email"), { target: { value: "joao@gmail.com" } });
    fireEvent.change(getByPlaceholderText("Senha"), { target: { value: "123456" } });
    fireEvent.change(getByPlaceholderText("Confirmar senha"), { target: { value: "123456" } });

    fireEvent.click(getByText("Criar"));

    expect(await findByText("Cadastro realizado com sucesso!")).toBeInTheDocument();
  });

  it("Exibe mensagem de erro ao tentar cadastrar um usuário já existente", async () => {
    vi.mocked(cadastrar).mockResolvedValueOnce({
      success: false,
      error: "email/cpf já está registrado.",
    });

    const { getByPlaceholderText, getByText, findByText } = render(
      <MemoryRouter>
        <Cadastro />
      </MemoryRouter>
    );

    fireEvent.change(getByPlaceholderText("Nome"), { target: { value: "João" } });
    fireEvent.change(getByPlaceholderText("CPF"), { target: { value: "123.456.789-00" } });
    fireEvent.change(getByPlaceholderText("Email"), { target: { value: "joao@gmail.com" } });
    fireEvent.change(getByPlaceholderText("Senha"), { target: { value: "123456" } });
    fireEvent.change(getByPlaceholderText("Confirmar senha"), { target: { value: "123456" } });

    fireEvent.click(getByText("Criar"));

    expect(await findByText("email/cpf já está registrado.")).toBeInTheDocument();
  });
});