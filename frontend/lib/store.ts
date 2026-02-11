import { create } from "zustand";

type AuthState = {
  token: string;
  setToken: (token: string) => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  token: "",
  setToken: (token) => set({ token }),
}));
