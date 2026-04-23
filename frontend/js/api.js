const BASE = 'http://127.0.0.1:8000/api';

const Api = {
    async login(email, password) {
        const res = await fetch(`${BASE}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        return { ok: res.ok, data: await res.json() };
    },

    async register(payload) {
        const res = await fetch(`${BASE}/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        return { ok: res.ok, data: await res.json() };
    },

    async getAdminDashboard() {
        const res = await authFetch(`${BASE}/farmers/dashboard/admin/`);
        return { ok: res.ok, data: await res.json() };
    },

    async getFarmerDashboard() {
        const res = await authFetch(`${BASE}/farmers/dashboard/farmer/`);
        return { ok: res.ok, data: await res.json() };
    },

    async getFarmers() {
        const res = await authFetch(`${BASE}/farmers/`);
        return { ok: res.ok, data: await res.json() };
    },

    async getFarmer(id) {
        const res = await authFetch(`${BASE}/farmers/${id}/`);
        return { ok: res.ok, data: await res.json() };
    },

    async createFarmer(payload) {
        const res = await authFetch(`${BASE}/farmers/`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
        return { ok: res.ok, data: await res.json() };
    },

    async updateFarmer(id, payload) {
        const res = await authFetch(`${BASE}/farmers/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(payload),
        });
        return { ok: res.ok, data: await res.json() };
    },

    async deleteFarmer(id) {
        const res = await authFetch(`${BASE}/farmers/${id}/`, { method: 'DELETE' });
        return { ok: res.ok };
    },
};