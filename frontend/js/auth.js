// Depends on: js/config.js (must be loaded first in HTML)

function saveTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function getAccess()  { return localStorage.getItem('access_token'); }
function getRefresh() { return localStorage.getItem('refresh_token'); }

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

function saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
}

function isLoggedIn() { return !!getAccess(); }

function requireAuth(role) {
    if (!isLoggedIn()) {
        window.location.href = 'index.html';
        return false;
    }
    const user = getUser();
    if (role && user?.role !== role) {
        alert('Access denied.');
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

async function refreshAccessToken() {
    const refresh = getRefresh();
    if (!refresh) return false;
    try {
        const res = await fetch(`${API_BASE}/auth/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
    } catch (_) {}
    return false;
}

async function authFetch(url, options = {}) {
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${getAccess()}`,
        'Content-Type': 'application/json',
    };
    let res = await fetch(url, options);
    if (res.status === 401) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            options.headers['Authorization'] = `Bearer ${getAccess()}`;
            res = await fetch(url, options);
        } else {
            clearTokens();
            window.location.href = 'index.html';
        }
    }
    return res;
}

async function logout() {
    try {
        await authFetch(`${API_BASE}/auth/logout/`, {
            method: 'POST',
            body: JSON.stringify({ refresh: getRefresh() }),
        });
    } catch (_) {}
    clearTokens();
    window.location.href = 'index.html';
}