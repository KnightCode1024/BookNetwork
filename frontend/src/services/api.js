import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                const refreshToken = localStorage.getItem('refresh_token')
                if (refreshToken) {
                    const response = await axios.post('http://localhost:8000/api/v1/auth/jwt/refresh/', {
                        refresh: refreshToken
                    })

                    const newAccessToken = response.data.access
                    localStorage.setItem('access_token', newAccessToken)

                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
                    return api(originalRequest)
                }
            } catch (refreshError) {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                window.location.href = '/login'
            }
        }

        console.error('API Error:', error)
        return Promise.reject(error)
    }
)

export default api