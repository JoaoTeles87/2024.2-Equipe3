import { useEffect, useState } from "react";

function App() {
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetch(import.meta.env.VITE_API_URL)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro na API: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => setMessage(data.message))
            .catch((error) => setError(error.message));
    }, []);

    return (
        <div>
            <h1>Testando API</h1>
            {error ? <p style={{ color: "red" }}>{error}</p> : <p>{message}</p>}
        </div>
    );
}

export default App;
