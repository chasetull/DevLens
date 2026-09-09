import { useState } from "react";

import { analyzeProject } from "./api/devlens";
import { AnalysisForm } from "./components/AnalysisForm";
import type { AnalysisResult } from "./types/analysis";

function App() {
  const [analysis, setAnalysis] =
    useState<AnalysisResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze(projectPath: string) {
    setLoading(true);
    setError(null);

    try {
      const result = await analyzeProject(projectPath);
      setAnalysis(result);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>DevLens</h1>

      <p>Understand the health of your codebase.</p>

      <AnalysisForm
        onAnalyze={handleAnalyze}
        loading={loading}
      />

      {error && <p>{error}</p>}

      {analysis && (
        <section>
          <h2>{analysis.project_name}</h2>

          <p>{analysis.project_path}</p>

          <p>Files: {analysis.file_count}</p>

          <p>Directories: {analysis.directory_count}</p>

          <p>Lines: {analysis.total_lines}</p>

          <p>
            Git branch:{" "}
            {analysis.git?.branch ?? "Not a Git repository"}
          </p>
        </section>
      )}
    </main>
  );
}

export default App;