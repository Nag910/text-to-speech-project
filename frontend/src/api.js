/**
 * api.js
 * ------
 * Small wrapper around fetch() for talking to the Flask backend.
 * Centralizing this here means components never build URLs themselves,
 * and network/HTTP errors are normalized into one shape.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function parseJsonSafely(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchVoices() {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/api/voices`);
  } catch {
    throw new ApiError("Could not reach the server. Please check your connection.", 0);
  }

  const data = await parseJsonSafely(response);
  if (!response.ok || !data?.success) {
    throw new ApiError(data?.error || "Failed to load languages and voices.", response.status);
  }
  return data;
}

export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
}

export async function generateSpeech({ text, language, voice }) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/api/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, language, voice }),
    });
  } catch {
    throw new ApiError("Network error. Please check your connection and try again.", 0);
  }

  const data = await parseJsonSafely(response);

  if (response.status === 429) {
    throw new ApiError("Too many requests. Please wait a moment and try again.", 429);
  }
  if (!response.ok || !data?.success) {
    throw new ApiError(data?.error || "Something went wrong while generating speech.", response.status);
  }

  return `${API_BASE_URL}${data.audio_url}`;
}

export { ApiError, API_BASE_URL };
