// The Bridge Between FastAPI and React Frontend
import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api/v1",
    withCredentials: true, // Send HttpOnly cookies
});


// ==================== AUTH ====================

export const register = async (payload) => {
    const response = await api.post("/auth/register", payload);
    return response.data;
};

export const login = async (payload) => {
    const response = await api.post("/auth/login", payload);
    return response.data;
};

export const logout = async () => {
    const response = await api.post("/auth/logout");
    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get("/auth/me");
    return response.data;
};


// ==================== RESUME TEXT ====================

export const analyzeResumeText = async (payload) => {
    const response = await api.post("/match", payload);
    return response.data;
};

export const analyzeResumeQualityText = async (payload) => {
    const response = await api.post("/resume-quality", payload);
    return response.data;
};


// ==================== RESUME PDF ====================

export const analyzeResumePDF = async (formData) => {
    const response = await api.post("/match-pdf", formData);
    return response.data;
};

export const analyzeResumeQualityPDF = async (formData) => {
    const response = await api.post("/resume-quality-pdf", formData);
    return response.data;
};


// ==================== ANALYSIS HISTORY ====================

export const getAnalyses = async () => {
    const response = await api.get("/analyses");
    return response.data;
};

export const getAnalysis = async (analysisId) => {
    const response = await api.get(`/analyses/${analysisId}`);
    return response.data;
};

export const deleteAnalysis = async (analysisId) => {
    const response = await api.delete(`/analyses/${analysisId}`);
    return response.data;
};


// ==================== RESUMES ====================

export const getResumes = async () => {
    const response = await api.get("/resumes");
    return response.data;
};

export const getResume = async (resumeId) => {
    const response = await api.get(`/resumes/${resumeId}`);
    return response.data;
};

export const deleteResume = async (resumeId) => {
    const response = await api.delete(`/resumes/${resumeId}`);
    return response.data;
};


export default api;