import { api } from "./axios";

export const postReport = async (reportData) => {
  try {
    const res = await api.post(`/api/report`, reportData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return res.data;
  } catch (err) {
    console.error("API 요청 실패:", err);
    throw err;
  }
};

// ✅ 예측 요청
export const DetectFile = async (formData) => {
  try {
    const res = await api.post(`/api/predict`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (err) {
    console.error("예측 요청 실패:", err);
    throw err;
  }
};

export const restoreFile = async (formData) => {
  try {
    const res = await api.post(`/api/restore`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (err) {
    console.error("복원 요청 실패:", err);
    throw err;
  }
};
