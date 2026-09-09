// DEVLENS API LAYER
import type { AnalysisResult } from "../types/analysis";

const API_BASE_URL = "http://localhost:8000/api/v1";

export async function analyzeProject(
  projectPath: string
): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/analysis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      project_path: projectPath,
    }),
  });

  const responseText = await response.text();

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    if (responseText) {
      try {
        const error = JSON.parse(responseText);
        message = error.detail || message;
      } catch {
        message = responseText;
      }
    }

    throw new Error(message);
  }

  if (!responseText) {
    throw new Error("DevLens API returned an empty response.");
  }

  return JSON.parse(responseText);
}