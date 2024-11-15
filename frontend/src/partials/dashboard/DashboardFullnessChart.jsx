import React, { useEffect, useState } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer,
} from 'recharts';
import { getAllReadings } from '../../utils/api';
import dayjs from 'dayjs';

const DashboardFullnessChart = ({ dateRange }) => {
    const [data, setData] = useState([]);
    const [groupedData, setGroupedData] = useState([]);
    const [deviceNames, setDeviceNames] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchReadings = async () => {
            try {
                const readings = await getAllReadings();

                // Format and filter the data based on the selected date range
                const [startDate, endDate] = dateRange;
                const filteredData = readings
                    .filter((r) => {
                        const readingDate = new Date(r.timestamp);
                        return readingDate >= startDate && readingDate <= endDate;
                    })
                    .map((r) => ({
                        device_id: r.device_id,
                        timestamp: new Date(r.timestamp),
                        timestamp_num: new Date(r.timestamp).getTime(), // Add numeric timestamp
                        time_formatted: dayjs(r.timestamp).format('DD-MM-YY HH:mm'),
                        fullness_level: r.fullness_level,
                    }));

                // Extract unique device IDs to plot separate lines for each
                const deviceIds = [...new Set(filteredData.map((d) => d.device_id))];
                const deviceNames = deviceIds.map((id) => `Device ${id}`);
                setDeviceNames(deviceNames);

                // Restructure data for Recharts
                const dataByTime = {};

                filteredData.forEach((entry) => {
                    const time = entry.timestamp_num; // Use numeric timestamp
                    if (!dataByTime[time]) {
                        dataByTime[time] = {
                            timestamp_num: time,
                        };
                    }
                    dataByTime[time][`Device ${entry.device_id}`] = entry.fullness_level;
                });

                // Convert to array and sort by numeric timestamp
                const groupedData = Object.values(dataByTime).sort((a, b) => a.timestamp_num - b.timestamp_num);

                setGroupedData(groupedData);
            } catch (err) {
                console.error('Failed to fetch readings:', err);
                setError('Failed to fetch readings.');
            } finally {
                setLoading(false);
            }
        };

        fetchReadings();
    }, [dateRange]);

    if (loading) {
        return <p className="text-gray-500">Loading fullness data...</p>;
    }

    if (error) {
        return <p className="text-red-500">{error}</p>;
    }

    if (groupedData.length === 0) {
        return <p className="text-gray-500">No fullness data available for the selected range.</p>;
    }

    // Colors for the lines, assign each device a different color
    const lineColors = ['#8884d8', '#82ca9d', '#ff7300', '#ff4d4f', '#faad14', '#52c41a'];

    return (
        <div className="col-span-full xl:col-span-12 bg-white dark:bg-gray-800 shadow-sm rounded-xl">
            <header className="px-5 py-4 border-b border-gray-100 dark:border-gray-700/60 flex items-center">
                <h2 className="font-semibold text-gray-800 dark:text-gray-100">
                    Fullness Over Time (All Devices)
                </h2>
            </header>
            <ResponsiveContainer width="97%" height={200}>
                <LineChart data={groupedData}>
                    <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
                    <XAxis
                        dataKey="timestamp_num"
                        type="number"
                        domain={['auto', 'auto']}
                        scale="time"
                        tickFormatter={(timestamp) => dayjs(timestamp).format('DD-MM-YY HH:mm')}
                    />
                    <YAxis domain={[0, 100]} />
                    <Tooltip
                        labelFormatter={(timestamp) => dayjs(timestamp).format('DD-MM-YY HH:mm')}
                    />
                    {deviceNames.map((deviceName, index) => (
                        <Line
                            key={deviceName}
                            type="monotone"
                            dataKey={deviceName}
                            name={deviceName}
                            stroke={lineColors[index % lineColors.length]}
                            strokeWidth={2}
                            dot={{ r: 3 }}
                            activeDot={{ r: 5 }}
                            connectNulls={true}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default DashboardFullnessChart;
