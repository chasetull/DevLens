// ANALYZE FORM
import { useState } from "react";

interface AnalysisFormProps {
  onAnalyze: (projectPath: string) => void;
  loading: boolean;
}

export function AnalysisForm({
  onAnalyze,
  loading,
}: AnalysisFormProps) {
  const [projectPath, setProjectPath] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (!projectPath.trim()) {
      return;
    }

    onAnalyze(projectPath.trim());
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={projectPath}
        onChange={(event) =>
          setProjectPath(event.target.value)
        }
        placeholder="/Users/you/projects/my-project"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Project"}
      </button>
    </form>
  );
}