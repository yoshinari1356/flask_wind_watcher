// ui/src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [windData, setWindData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWindData = async () => {
            try {
                const response = await axios.get('/api/wind');
                setWindData(response.data);
            } catch (error) {
                console.error('Error fetching wind data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchWindData();
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>Dashboard</h1>
            {windData ? (
                <div>
                    <p>Wind Speed: {windData.wind_speed} m/s</p>
                    <p>Wind Direction: {windData.wind_dir}°</p>
                </div>
            ) : (
                <p>No wind data available.</p>
            )}
        </div>
    );
};

export default Dashboard;