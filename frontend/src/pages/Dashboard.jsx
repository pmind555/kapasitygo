import React, { useState } from 'react';

import Sidebar from '../partials/Sidebar';
import Header from '../partials/Header';
import Datepicker from '../components/Datepicker';
import DashboardFullnessChart from "../partials/dashboard/DashboardFullnessChart";
import DashboardMapBox from '../partials/dashboard/DashboardMapBox';
import DashboardDevices from '../partials/dashboard/DashboardDevices';
import DashboardDevicesAlerts from '../partials/dashboard/DashboardDevicesAlerts';
import Banner from '../partials/Banner';

function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dateRange, setDateRange] = useState([
    new Date().setDate(new Date().getDate() - 1),
    new Date()
  ]);

  // Function to handle the Apply button click
  const handleApply = () => {
    // Triggered when the Apply button is clicked
    console.log("Applying date range: ", dateRange);
  };

  return (
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Content area */}
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
          {/* Site header */}
          <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

          <main className="grow">
            <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">

              {/* Dashboard actions */}
              <div className="sm:flex sm:justify-between sm:items-center mb-8">

                {/* Left: Title */}
                <div className="mb-4 sm:mb-0">
                  <h1 className="text-2xl md:text-3xl text-gray-800 dark:text-gray-100 font-bold">Dashboard</h1>
                </div>

                {/* Right: Actions */}
                <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
                  {/* Datepicker built with flatpickr */}
                  <Datepicker align="right" dateRange={dateRange} setDateRange={setDateRange} />
                  {/* Apply button */}
                  <button
                      onClick={handleApply}
                      className="btn bg-gray-900 text-gray-100 hover:bg-gray-800 dark:bg-gray-100 dark:text-gray-800 dark:hover:bg-white"
                  >
                    Apply
                  </button>
                </div>

              </div>

              {/* Cards */}
              <div className="grid grid-cols-12 gap-6">
                <DashboardFullnessChart dateRange={dateRange} />
                <DashboardMapBox />
                <DashboardDevices />
                <DashboardDevicesAlerts />
              </div>
            </div>
          </main>
          <Banner />
        </div>
      </div>
  );
}

export default Dashboard;
