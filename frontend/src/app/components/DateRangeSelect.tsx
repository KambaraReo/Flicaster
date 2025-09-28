"use client";

import { useState } from "react";

interface Props {
  startDate: string;
  endDate: string;
  setStartDate: (date: string) => void;
  setEndDate: (date: string) => void;
}

const DateRangeSelect: React.FC<Props> = ({
  startDate,
  endDate,
  setStartDate,
  setEndDate,
}) => {
  const [error, setError] = useState("");

  const validateDateRange = (start: string, end: string) => {
    if (start && end && start > end) {
      setError("※ 終了日は開始日より後の日付を選択してください。");
      return false;
    }
    setError("");
    return true;
  };

  const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setStartDate(value);
    validateDateRange(value, endDate);
  };

  const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEndDate(value);
    validateDateRange(startDate, value);
  };

  return (
    <>
      <div className="flex flex-col sm:flex-row gap-4 mb-4">
        <div className="flex-1">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="start-date-select"
          >
            開始日
          </label>
          <input
            id="start-date-select"
            type="date"
            value={startDate}
            onChange={handleStartChange}
            className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300 ${
              error ? "border-red-500" : ""
            }`}
          />
        </div>

        <div className="flex-1">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="end-date-select"
          >
            終了日
          </label>
          <input
            id="end-date-select"
            type="date"
            value={endDate}
            onChange={handleEndChange}
            className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300 ${
              error ? "border-red-500" : ""
            }`}
          />
        </div>
      </div>

      <div>
        {error && <p className="text-red-500 text-sm px-1">{error}</p>}
      </div>
    </>
  );
};

export { DateRangeSelect };
