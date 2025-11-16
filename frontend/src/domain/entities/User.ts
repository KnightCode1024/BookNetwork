export interface User {
  id: number;
  username: string;
  email: string | null;
  is_active: boolean;
  created_at?: string; // Опциональное поле, если бэкенд его возвращает
}

