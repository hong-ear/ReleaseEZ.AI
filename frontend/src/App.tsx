import { useState } from "react";

function App() {
  const [bundleText, setBundleText] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    try {
      setError(null);
      const parsed = JSON.parse(bundleText);

      const res = await fetch("http://localhost:8000/fhir/bundle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed),
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Submission failed: ${errText}`);
    }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message || "Invalid input or server error.");
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-4">
      <div className="p-4 space-y-4 border rounded shadow">
        <h2 className="text-xl font-semibold">FHIR Bundle Submission</h2>
        <textarea
          value={bundleText}
          onChange={(e) => setBundleText(e.target.value)}
          placeholder="Paste your FHIR JSON bundle here..."
          rows={15}
          className="w-full border p-2 rounded font-mono text-sm"
        />
        <button
          onClick={handleSubmit}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Submit to API
        </button>
        {response && (
          <div className="bg-green-100 p-4 rounded text-sm mt-4">
            ✅ Stored: <br />
            <strong>Raw ID:</strong> {response.raw_id} <br />
            <strong>Simplified ID:</strong> {response.simplified_id}
          </div>
        )}
        {error && (
          <div className="bg-red-100 p-4 rounded text-sm mt-4 text-red-800">
            ❌ Error: {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;