// In development:  points to local server
// In production:   points to Render backend URL

const IS_PRODUCTION = window.location.hostname !== '127.0.0.1'
                   && window.location.hostname !== 'localhost';

const DEV_API_URL  = 'http://127.0.0.1:8000/api';
const PROD_API_URL = 'https://YOUR-APP-NAME.onrender.com/api'; // ← replace after Render deploy

const API_BASE = IS_PRODUCTION ? PROD_API_URL : DEV_API_URL;