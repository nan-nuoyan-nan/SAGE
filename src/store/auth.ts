import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  name: string;
  targetLanguage: string;
  level: string;
  xp: number;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
  updateXP: (amount: number) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  // For demo purposes, let's start authenticated as a dummy user
  isAuthenticated: true,
  user: {
    id: 'user-1',
    email: 'demo@example.com',
    name: 'Alex',
    targetLanguage: 'Japanese',
    level: 'Beginner',
    xp: 450,
  },
  login: (user) => set({ isAuthenticated: true, user }),
  logout: () => set({ isAuthenticated: false, user: null }),
  updateXP: (amount) => set((state) => ({ 
    user: state.user ? { ...state.user, xp: state.user.xp + amount } : null 
  })),
}));
