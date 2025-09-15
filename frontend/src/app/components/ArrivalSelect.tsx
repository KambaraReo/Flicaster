"use client";

import { useEffect, useState } from "react";
import type { Airport } from "@/lib/api";
import { fetchArrivalAirports } from "@/lib/api";

interface Props {
  departure: string; // 出発空港コード
  value: string; // 選択中の到着空港コード
  setValue: (value: string) => void;
}

const ArrivalSelect: React.FC<Props> = ({ departure, value, setValue }) => {
  const [arrivalAirports, setArrivalAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!departure) {
      setArrivalAirports([]);
      setValue(""); // 出発空港が未選択ならリセット
      return;
    }

    setLoading(true);
    fetchArrivalAirports(departure)
      .then((data) => {
        setArrivalAirports(data);
        setValue(""); // 新しい出発空港に応じて到着空港をリセット
      })
      .finally(() => setLoading(false));
  }, [departure, setValue]);

  return (
    <div className="mt-4">
      <label
        htmlFor="arr-select"
        className="block text-gray-700 text-sm font-bold mb-2"
      >
        到着空港
      </label>
      <select
        id="arr-select"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={loading || !departure || arrivalAirports.length === 0}
        className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300 disabled:bg-gray-100"
      >
        <option value="">選択してください</option>
        {arrivalAirports.map((airport) => (
          <option key={airport.code} value={airport.code}>
            {airport.code}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ArrivalSelect;
