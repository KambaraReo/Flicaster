"use client";

import { useEffect, useState } from "react";
import { Flight, fetchFlights } from "@/lib/api";

type Props = {
  departure?: string;
  arrival?: string;
  onSelect: (flight: Flight | null) => void;
};

const FlightSelect: React.FC<Props> = ({ departure, arrival, onSelect }) => {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [selected, setSelected] = useState<string>("");

  useEffect(() => {
    if (!departure || !arrival) {
      setFlights([]);
      setSelected("");
      onSelect(null);
      return;
    }

    const loadFlights = async () => {
      try {
        const data = await fetchFlights(departure, arrival);
        setFlights(data);
      } catch (e) {
        console.error(e);
      }
    };
    loadFlights();
  }, [departure, arrival, onSelect]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const flight = flights.find((f) => f.flight_no === e.target.value) || null;
    setSelected(e.target.value);
    onSelect(flight);
  };

  return (
    <div className="mt-4">
      <label
        htmlFor="flight-select"
        className="block text-gray-700 text-sm font-bold mb-2"
      >
        フライト
      </label>
      <select
        id="flight-select"
        value={selected}
        onChange={handleChange}
        disabled={!departure || !arrival}
        className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300 disabled:bg-gray-100"
      >
        <option value="">フライトを選択してください</option>
        {flights.map((flight) => (
          <option key={flight.flight_no} value={flight.flight_no}>
            {`${flight.flight_no} | ${flight.airline_code} | ${flight.distance_cat} | ${flight.seat_capacity} seats`}
          </option>
        ))}
      </select>
    </div>
  );
};

export { FlightSelect };
