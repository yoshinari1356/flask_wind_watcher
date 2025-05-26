import axios from 'axios';

console.log('API URL:', process.env.REACT_APP_FLASK_API_URL); // 環境変数を確認

const api = axios.create({
    baseURL: process.env.REACT_APP_FLASK_API_URL, // 環境変数からベースURLを取得
    timeout: 1000,
});

export default api;
