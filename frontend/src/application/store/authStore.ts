import { create } from 'zustand';
import { TokenStorage } from '@domain/repositories/TokenStorage';
import { User } from '@domain/entities/User';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setAuthenticated: (isAuthenticated: boolean) => void;
  setLoading: (isLoading: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  setUser: (user) => set({ user }),
  setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),
  setLoading: (isLoading) => set({ isLoading }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));

export const initializeAuth = (tokenStorage: TokenStorage) => {
  const hasTokens = tokenStorage.hasTokens();
  useAuthStore.getState().setAuthenticated(hasTokens);
  useAuthStore.getState().setLoading(false);
};

