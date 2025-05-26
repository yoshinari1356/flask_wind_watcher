import React, { useState, useEffect } from 'react';
import api from '../api/axios';

const Settings = () => {
    const [config, setConfig] = useState({
        tomorrow_api_key: '',
        pushover_app_token: '',
        pushover_user_key: '',
        lat: '',
        lon: '',
        alt: '',
        days: [],
        time: ''
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await api.get('/settings'); // APIから設定を取得
                setConfig(response.data);
            } catch (error) {
                console.error('Error fetching config:', error);
                setError('設定の取得に失敗しました。');
            } finally {
                setLoading(false);
            }
        };

        fetchConfig();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setConfig((prevConfig) => ({
            ...prevConfig,
            [name]: value
        }));
    };

    const handleUpdate = async (e) => {
        e.preventDefault(); // フォームのデフォルトの送信を防ぐ
        try {
            await api.post('/settings', config); // 設定を更新
            alert('設定が更新されました！');
        } catch (error) {
            console.error('Error updating settings:', error);
            setError('設定の更新に失敗しました。');
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <form onSubmit={handleUpdate}>
            <fieldset>
                <legend>API情報</legend>
                <label>
                    Tomorrow.io API Key:
                    <input
                        type="text"
                        name="tomorrow_api_key"
                        value={config.tomorrow_api_key}
                        onChange={handleChange}
                    />
                </label>
                <br />
                <label>
                    Pushover App Token:
                    <input
                        type="text"
                        name="pushover_app_token"
                        value={config.pushover_app_token}
                        onChange={handleChange}
                    />
                </label>
                <br />
                <label>
                    Pushover User Key:
                    <input
                        type="text"
                        name="pushover_user_key"
                        value={config.pushover_user_key}
                        onChange={handleChange}
                    />
                </label>
            </fieldset>
            <fieldset>
                <legend>飛行設定</legend>
                <label>
                    緯度:
                    <input
                        type="text"
                        name="lat"
                        value={config.lat}
                        onChange={handleChange}
                    />
                </label>
                <br />
                <label>
                    経度:
                    <input
                        type="text"
                        name="lon"
                        value={config.lon}
                        onChange={handleChange}
                    />
                </label>
                <br />
                <label>
                    高度(m):
                    <input
                        type="number"
                        name="alt"
                        value={config.alt}
                        onChange={handleChange}
                    />
                </label>
                <br />
                <fieldset>
                    <legend>通知曜日</legend>
                    {['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].map((day) => (
                        <label key={day}>
                            <input
                                type="checkbox"
                                name="days"
                                value={day}
                                checked={config.days.includes(day)}
                                onChange={(e) => {
                                    const { checked } = e.target;
                                    setConfig((prevConfig) => {
                                        const newDays = checked
                                            ? [...prevConfig.days, day]
                                            : prevConfig.days.filter((d) => d !== day);
                                        return { ...prevConfig, days: newDays };
                                    });
                                }}
                            />
                            {day}
                        </label>
                    ))}
                </fieldset>
                <br />
                <label>
                    通知時刻:
                    <input
                        type="time"
                        name="time"
                        value={config.time}
                        onChange={handleChange}
                    />
                </label>
            </fieldset>
            <button type="submit">更新</button>
        </form>
    );
};

export default Settings;
