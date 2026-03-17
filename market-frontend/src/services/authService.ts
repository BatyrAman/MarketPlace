import { api } from './api';
import { storage } from './storage';
import type { TokenResponse, User } from '../types';

export const authService = {
  isAuthenticated: () => Boolean(storage.getAccessToken()),
  async login(payload: { email: string; password: string }) {
    const tokens = await api.post<TokenResponse>('/auth/login', payload);
    storage.setTokens(tokens.access_token, tokens.refresh_token);
    return tokens;
  },
  async register(payload: { email: string; username: string; password: string; full_name?: string }) {
    return api.post<User>('/auth/register', payload);
  },
  logout() {
    storage.clearTokens();
  },
};
