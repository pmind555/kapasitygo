// src/utils/api.js
import axios from 'axios';

// Retrieve environment variables using Vite's import.meta.env
const API_KEY = import.meta.env.VITE_PUBLIC_API_KEY;

// Create an Axios instance with default configurations
const apiClient = axios.create({
    baseURL: '/api', // Use the /api prefix to utilize the proxy
    headers: {
        'Content-Type': 'application/json', // Optional: Set Content-Type
    },
});

// Add a request interceptor to include the API key in headers
apiClient.interceptors.request.use(
    (config) => {
        config.headers['x-api-key'] = API_KEY;
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Export API functions using the Axios instance

export const getAllDevices = async () => {
    try {
        const response = await apiClient.get('/devices/');

        if (Array.isArray(response.data)) {
            return response.data;
        } else if (response.data && Array.isArray(response.data.devices)) {
            // If the API wraps devices in a 'devices' field
            return response.data.devices;
        } else {
            console.error('Unexpected API response structure:', response.data);
            return [];
        }
    } catch (error) {
        console.error('Error fetching devices:', error);
        return [];
    }
};

export const getAllReadings = async () => {
    try {
        const response = await apiClient.get('/readings/?limit=50000');

        if (Array.isArray(response.data)) {
            return response.data;
        } else if (response.data && Array.isArray(response.data.readings)) {
            // If the API wraps readings in a 'readings' field
            return response.data.readings;
        } else {
            console.error('Unexpected API response structure (Readings):', response.data);
            return [];
        }
    } catch (error) {
        console.error('Error fetching readings:', error);
        return [];
    }
};

// New API function to get alerts
export const getAlerts = async (minFullness = 0, maxFullness = 100, skip = 0, limit = 100) => {
    try {
        const response = await apiClient.get('/devices/alerts', {
            params: {
                min_fullness: minFullness,
                max_fullness: maxFullness,
                skip: skip,
                limit: limit,
            },
        });

        if (Array.isArray(response.data)) {
            return response.data;
        } else if (response.data && Array.isArray(response.data.alerts)) {
            // If the API wraps alerts in an 'alerts' field
            return response.data.alerts;
        } else {
            console.error('Unexpected API response structure (Alerts):', response.data);
            return [];
        }
    } catch (error) {
        console.error('Error fetching alerts:', error);
        return [];
    }
};

// Add other API functions as needed
