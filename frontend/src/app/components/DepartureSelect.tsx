"use client";

import { useEffect, useState } from "react";
import type { Airport } from "@/lib/api";
import { fetchAirports } from "@/lib/api";

interface Props {
  value: string;
  setValue: (value: string) => void;
}

const DepartureSelect: React.FC<Props> = ({ value, setValue }) => {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAirports()
      .then((data) => setAirports(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <label className="block mb-1 font-medium">出発空港</label>
      <select
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={loading}
        className="w-full border rounded px-3 py-2"
      >
        <option value="">選択してください</option>
        {airports.map((airport) => (
          <option key={airport.code} value={airport.code}>
            {airport.code}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DepartureSelect;
