// src/components/DashboardDevicesAlerts.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getAlerts } from '../../utils/api'; // Import the new getAlerts method

const DashboardDevicesAlerts = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch alerts on component mount
    useEffect(() => {
        const fetchDevicesWithAlerts = async () => {
            try {
                // Fetch alerts with a fullness level of 90 or above
                const alertDevices = await getAlerts(90);
                setDevices(alertDevices);
            } catch (err) {
                console.error('Failed to fetch alerts:', err);
                setError('Failed to fetch alerts.');
            } finally {
                setLoading(false);
            }
        };

        fetchDevicesWithAlerts();
    }, []);

    if (loading) {
        return <p className="text-gray-500">Loading devices...</p>;
    }

    if (error) {
        return <p className="text-red-500">{error}</p>;
    }

    return (
        <div className="col-span-full xl:col-span-4 bg-white dark:bg-gray-800 shadow-sm rounded-xl">
            <header className="px-5 py-4 border-b border-gray-100 dark:border-gray-700/60">
                <h2 className="font-semibold text-gray-800 dark:text-gray-100">Alerts</h2>
            </header>
            <div className="p-3">
                <div>
                    <header className="text-xs uppercase text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-700 dark:bg-opacity-50 rounded-sm font-semibold p-2">
                        ALERTS
                    </header>
                    <ul className="my-1">
                        {devices.length === 0 ? (
                            <li className="flex px-2 py-2">
                                <p className="text-gray-500">No devices with high fullness levels.</p>
                            </li>
                        ) : (
                            devices.map((device, index) => {
                                const { device_id, location_name, fullness_level } = device;

                                return (
                                    <li key={`${device_id}-${index}`} className="flex px-2">
                                        <div className="w-9 h-9 rounded-full shrink-0 my-2 mr-3 flex items-center justify-center bg-red-500">
                                            <svg
                                                className="w-6 h-6 fill-current text-white"
                                                viewBox="0 0 36 36"
                                                xmlns="http://www.w3.org/2000/svg"
                                            >
                                                <g transform="rotate(90 18 18)">
                                                    <path
                                                        d="M18.3 11.3l-1.4 1.4 4.3 4.3H11v2h10.2l-4.3 4.3 1.4 1.4L25 18z"/>
                                                </g>
                                            </svg>
                                        </div>
                                        <div
                                            className="grow flex items-center border-b border-gray-100 dark:border-gray-700/60 text-sm py-2">
                                            <div className="grow flex justify-between">
                                                <div className="self-center">
                                                    <button
                                                        className="font-medium text-gray-800 hover:text-gray-900 dark:text-gray-100 dark:hover:text-white"
                                                        onClick={() => console.log('Selected device:', device)}
                                                        aria-label={`Select device at ${location_name}`}
                                                    >
                                                        {location_name}
                                                    </button>
                                                </div>
                                                <div className="shrink-0 self-start ml-2">
                                                    <span className="font-medium text-red-600">
                                                        {fullness_level}%
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                );
                            })
                        )}
                    </ul>
                </div>
            </div>
        </div>
    );
};

DashboardDevicesAlerts.propTypes = {
    devices: PropTypes.arrayOf(
        PropTypes.shape({
            device_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
            location_name: PropTypes.string.isRequired,
            fullness_level: PropTypes.number.isRequired,
        })
    ),
};

export default DashboardDevicesAlerts;
