import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/v1'

// Создаем экземпляр axios
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Интерцептор для добавления токена к запросам
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `JWT ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Интерцептор для обновления токена при истечении
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
                try {
                    console.log('🔄 Access token истек, обновляем...')
                    const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                        refresh: refreshToken
                    })

                    const newAccessToken = response.data.access
                    localStorage.setItem('access_token', newAccessToken)

                    // Обновляем заголовок для повторного запроса
                    originalRequest.headers.Authorization = `JWT ${newAccessToken}`

                    console.log('✅ Token успешно обновлен')
                    return api(originalRequest)
                } catch (refreshError) {
                    console.error('❌ Ошибка обновления token:', refreshError)
                    // Если refresh токен невалиден, разлогиниваем пользователя
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    window.location.href = '/login'
                    return Promise.reject(refreshError)
                }
            } else {
                // Нет refresh token, перенаправляем на логин
                window.location.href = '/login'
            }
        }

        return Promise.reject(error)
    }
)

export const authAPI = {
    // Регистрация нового пользователя
    register(userData) {
        return api.post('/auth/users/', userData)
    },

    // Активация аккаунта
    activate(uid, token) {
        return api.post('/auth/users/activation/', { uid, token })
    },

    // Получение JWT токенов
    login(credentials) {
        return api.post('/auth/jwt/create/', credentials)
    },

    // Обновление токена
    refreshToken(refreshToken) {
        return api.post('/auth/token/refresh/', { refresh: refreshToken })
    },

    // Верификация токена
    verifyToken(token) {
        return api.post('/auth/jwt/verify/', { token })
    },

    // Получение данных текущего пользователя
    getProfile() {
        return api.get('/auth/users/me/')
    },

    // Обновление данных пользователя
    updateProfile(userData) {
        return api.patch('/auth/users/me/', userData)
    },

    // Смена пароля
    changePassword(passwordData) {
        return api.post('/auth/users/set_password/', passwordData)
    },

    // Восстановление пароля
    resetPassword(email) {
        return api.post('/auth/users/reset_password/', { email })
    },

    // Подтверждение сброса пароля
    resetPasswordConfirm(uid, token, new_password) {
        return api.post('/auth/users/reset_password_confirm/', {
            uid,
            token,
            new_password
        })
    },

    // Получение списка пользователей (только для админов)
    getUsers() {
        return api.get('/auth/users/')
    },

    // Получение пользователя по ID
    getUser(userId) {
        return api.get(`/auth/users/${userId}/`)
    },

    // Удаление пользователя
    deleteUser(userId) {
        return api.delete(`/auth/users/${userId}/`)
    }
}

// Вспомогательные функции для работы с токенами
export const tokenUtils = {
    // Проверка валидности токена
    isTokenValid() {
        const token = localStorage.getItem('access_token')
        if (!token) return false

        try {
            // Декодируем JWT токен чтобы проверить expiration
            const payload = JSON.parse(atob(token.split('.')[1]))
            const exp = payload.exp * 1000 // конвертируем в миллисекунды
            return Date.now() < exp
        } catch (error) {
            console.error('Ошибка проверки токена:', error)
            return false
        }
    },

    // Получение данных из токена
    getTokenData() {
        const token = localStorage.getItem('access_token')
        if (!token) return null

        try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            return {
                userId: payload.user_id,
                username: payload.username,
                exp: new Date(payload.exp * 1000),
                issuedAt: new Date(payload.iat * 1000)
            }
        } catch (error) {
            console.error('Ошибка декодирования токена:', error)
            return null
        }
    },

    // Очистка токенов
    clearTokens() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    },

    // Сохранение токенов
    saveTokens(access, refresh) {
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
    }
}

// Экспортируем api для использования в других местах
export default api