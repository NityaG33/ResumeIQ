import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1",
});

// Resume Text
export const analyzeResumeText = async (payload) => {
    const response = await api.post("/match", payload);
    return response.data;
};

// Resume PDF
export const analyzeResumePDF = async (formData) => {
    const response = await api.post("/match-pdf", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};

export default api;