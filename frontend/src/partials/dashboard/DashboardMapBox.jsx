// src/components/DashboardMapBox.jsx
import React, { useState, useEffect } from 'react';
import ReactMapGL, { Marker, Popup } from 'react-map-gl';
import { getAllDevices } from '../../utils/api';
import 'mapbox-gl/dist/mapbox-gl.css';

const DashboardMapBox = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [viewport, setViewport] = useState({
        latitude: 60.1699,
        longitude: 24.9384,
        zoom: 10,
    });
    const [selectedDevice, setSelectedDevice] = useState(null);

    // Fetch devices on component mount
    useEffect(() => {
        const fetchDevices = async () => {
            try {
                const data = await getAllDevices();
                setDevices(data);
            } catch (err) {
                console.error('Failed to fetch devices:', err);
                setError('Failed to fetch devices.');
            } finally {
                setLoading(false);
            }
        };

        fetchDevices();
    }, []);

    if (loading) {
        return <p className="text-gray-500">Loading devices...</p>;
    }

    if (error) {
        return <p className="text-red-500">{error}</p>;
    }

    return (
        <div className="col-span-full xl:col-span-12 bg-white dark:bg-gray-800 shadow-sm rounded-xl">
            <header className="px-5 py-4 border-b border-gray-100 dark:border-gray-700/60">
                <h2 className="font-semibold text-gray-800 dark:text-gray-100">Device Locations</h2>
            </header>
            <div className="p-3">
                <div className="w-full h-96">
                    <ReactMapGL
                        {...viewport}
                        mapboxAccessToken={process.env.VITE_PUBLIC_MAPBOX_TOKEN} // Make sure to add your Mapbox token in .env
                        mapStyle="mapbox://styles/mapbox/streets-v11"
                        width="100%"
                        height="100%"
                        onMove={(evt) => setViewport(evt.viewState)}
                    >
                        {devices.map((device) => (
                            <Marker key={device.device_id} latitude={device.latitude} longitude={device.longitude}>
                                <button
                                    onClick={() => setSelectedDevice(device)}
                                    className="text-red-500 focus:outline-none"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="currentColor"
                                         viewBox="0 0 24 24" stroke="none">
                                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zM12 11.5c-1.93 0-3.5-1.57-3.5-3.5S10.07 4.5 12 4.5 15.5 6.07 15.5 8 13.93 11.5 12 11.5z"/>
                                    </svg>
                                </button>
                            </Marker>
                        ))}

                        {selectedDevice && (
                            <Popup
                                latitude={selectedDevice.latitude}
                                longitude={selectedDevice.longitude}
                                onClose={() => setSelectedDevice(null)}
                                closeOnClick={false}
                                anchor="top"
                            >
                                <div>
                                    <h3 className="font-bold">{selectedDevice.location_name}</h3>
                                    <p>Status: {selectedDevice.status}</p>
                                </div>
                            </Popup>
                        )}
                    </ReactMapGL>
                </div>
            </div>
        </div>
    );
};

export default DashboardMapBox;
