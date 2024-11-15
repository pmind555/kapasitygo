// src/components/DashboardDevices.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getAllDevices } from '../../utils/api'; // Ensure the correct path

// Helper component to render the appropriate icon based on status
const StatusIcon = ({ status }) => {
    switch (status.toLowerCase()) {
        case 'active':
            return (
                <svg
                    className="w-6 h-6 fill-current text-white"
                    viewBox="0 0 36 36"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <g transform="rotate(-90 18 18)">
                        <path d="M18.3 11.3l-1.4 1.4 4.3 4.3H11v2h10.2l-4.3 4.3 1.4 1.4L25 18z" />
                    </g>
                </svg>
            );
        case 'disabled':
            return (
                <svg
                    className="w-6 h-6 fill-current text-gray-400"
                    viewBox="0 0 36 36"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="M21.477 22.89l-8.368-8.367a6 6 0 008.367 8.367zm1.414-1.413a6 6 0 00-8.367-8.367l8.367 8.367zM18 26a8 8 0 110-16 8 8 0 010 16z" />
                </svg>
            );
        case 'error':
            return (
                <svg
                    className="w-6 h-6 fill-current text-white"
                    viewBox="0 0 36 36"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <g transform="rotate(90 18 18)">
                        <path d="M18.3 11.3l-1.4 1.4 4.3 4.3H11v2h10.2l-4.3 4.3 1.4 1.4L25 18z" />
                    </g>
                </svg>
            );
        default:
            return null;
    }
};

StatusIcon.propTypes = {
    status: PropTypes.string.isRequired,
};

const DashboardDevices = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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

    // Helper function to determine the background color based on status
    const getStatusBackground = (status) => {
        switch (status.toLowerCase()) {
            case 'active':
                return 'bg-green-500';
            case 'inactive':
                return 'bg-gray-200';
            case 'error':
                return 'bg-red-500';
            default:
                return 'bg-gray-200';
        }
    };

    // Helper function to determine the text color based on status
    const getStatusTextColor = (status) => {
        switch (status.toLowerCase()) {
            case 'active':
                return 'text-green-600';
            case 'inactive':
                return 'text-gray-800';
            case 'error':
                return 'text-white';
            default:
                return 'text-gray-800';
        }
    };

    if (loading) {
        return <p className="text-gray-500">Loading devices...</p>;
    }

    if (error) {
        return <p className="text-red-500">{error}</p>;
    }

    return (

        <div className="col-span-full xl:col-span-4 bg-white dark:bg-gray-800 shadow-sm rounded-xl">
            <header className="px-5 py-4 border-b border-gray-100 dark:border-gray-700/60">
                <h2 className="font-semibold text-gray-800 dark:text-gray-100">Devices</h2>
            </header>
            <div className="p-3">
                {/* Card content */}
                {/* "ALL" group */}
                <div>
                    <header className="text-xs uppercase text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-700 dark:bg-opacity-50 rounded-sm font-semibold p-2">
                        ALL
                    </header>
                    <ul className="my-1">
                        {devices.length === 0 ? (
                            <li className="flex px-2 py-2">
                                <p className="text-gray-500">No devices available.</p>
                            </li>
                        ) : (
                            devices.map((device) => {

                                // Destructure device properties
                                const { device_id, location_name, status } = device;

                                // Validate device properties
                                if (!device_id || !location_name || !status) {
                                    console.error('Device is missing required properties:', device);
                                    return (
                                        <li key={device_id || Math.random()} className="flex px-2 py-2">
                                            <p className="text-red-500">Invalid device data.</p>
                                        </li>
                                    );
                                }

                                return (
                                    <li key={device_id} className="flex px-2">
                                        <div
                                            className={`w-9 h-9 rounded-full shrink-0 my-2 mr-3 flex items-center justify-center ${getStatusBackground(
                                                status
                                            )}`}
                                        >
                                            <StatusIcon status={status} />
                                        </div>
                                        <div
                                            className="grow flex items-center border-b border-gray-100 dark:border-gray-700/60 text-sm py-2"
                                        >
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
                                                    <span
                                                        className={`font-medium ${getStatusTextColor(status)}`}
                                                    >
                                                        {status.charAt(0).toUpperCase() + status.slice(1)}
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

export default DashboardDevices;
