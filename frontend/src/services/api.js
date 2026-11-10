
const API_BASE_URL = "http://127.0.0.1:8001";

const TOKEN_KEY = "nityasadhana_access_token";
const USER_KEY = "nityasadhana_user";

export const getToken = () => localStorage.getItem(TOKEN_KEY);

export const getStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch {
    return null;
  }
};

export const setAuthData = (token, user) => {
  localStorage.setItem(TOKEN_KEY, token);
  if (user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
};

export const clearAuthData = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

export async function apiRequest(endpoint, options = {}) {
  const token = getToken();

  const headers = {
    Accept: "application/json",
    ...options.headers,
  };

  if (options.body) {
    headers["Content-Type"] = "application/json";
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const text = await response.text();
  let data = null;

  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      `Request failed: ${response.status}`;

    throw new Error(message);
  }

  return data;
}

// AUTHENTICATION

export const authAPI = {
  register: (email, password) =>
    apiRequest("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: async (email, password) => {
    const result = await apiRequest("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    setAuthData(result.access_token);
    return result;
  },

  me: async () => {
    const user = await apiRequest("/api/auth/me");
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    return user;
  },

  logout: async () => {
    try {
      if (getToken()) {
        await apiRequest("/api/auth/logout", {
          method: "POST",
        });
      }
    } finally {
      clearAuthData();
    }
  },
};

// DAILY REPORTS

export const reportAPI = {
  save: (reportDate, reportData) =>
    apiRequest("/api/reports/save", {
      method: "POST",
      body: JSON.stringify({
        report_date: reportDate,
        report_data: reportData,
      }),
    }),

  submit: (reportDate, reportData) =>
    apiRequest("/api/reports/submit", {
      method: "POST",
      body: JSON.stringify({
        report_date: reportDate,
        report_data: reportData,
      }),
    }),

  today: () => apiRequest("/api/reports/today"),

  previous: () => apiRequest("/api/reports/previous"),

  history: () => apiRequest("/api/reports/me"),

  getById: (reportId) =>
    apiRequest(`/api/reports/${reportId}`),
};

// DEVOTEE PROFILE

export const profileAPI = {
  create: (profile) =>
    apiRequest("/api/profile/", {
      method: "POST",
      body: JSON.stringify(profile),
    }),

  me: () => apiRequest("/api/profile/me"),

  update: (profile) =>
    apiRequest("/api/profile/me", {
      method: "PUT",
      body: JSON.stringify(profile),
    }),
};

// DASHBOARD

export const dashboardAPI = {
  get: (startDate, endDate) => {
    const params = new URLSearchParams();

    if (startDate) params.set("start_date", startDate);
    if (endDate) params.set("end_date", endDate);

    const query = params.toString();
    return apiRequest(
      `/api/dashboard/me${query ? `?${query}` : ""}`
    );
  },

  weekly: () => apiRequest("/api/dashboard/weekly"),

  monthly: () => apiRequest("/api/dashboard/monthly"),

  custom: (startDate, endDate) =>
    apiRequest(
      `/api/dashboard/custom?start_date=${startDate}&end_date=${endDate}`
    ),
};

export default apiRequest;
