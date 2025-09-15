"use client";

import { useEffect, useState } from "react";
import { Flight, fetchFlights } from "@/lib/api";

type FlightSelectProps = {
  onSelect: (flight: Flight | null) => void;
};

const FlightSelect = ({ onSelect }: FlightSelectProps) => {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [selected, setSelected] = useState<string>("");

  useEffect(() => {
    const loadFlights = async () => {
      try {
        const data = await fetchFlights();
        setFlights(data);
      } catch (e) {
        console.error(e);
      }
    };
    loadFlights();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const flight = flights.find((f) => f.flight_no === e.target.value) || null;
    setSelected(e.target.value);
    onSelect(flight);
  };

  return (
    <select
      value={selected}
      onChange={handleChange}
      className="border p-2 rounded"
    >
      <option value="">フライトを選択してください</option>
      {flights.map((flight) => (
        <option key={flight.flight_no} value={flight.flight_no}>
          {`${flight.flight_no} | ${flight.airline_code} | ${flight.distance_cat} | ${flight.seat_capacity} seats`}
        </option>
      ))}
    </select>
  );
};

export { FlightSelect };
