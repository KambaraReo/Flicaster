"use client";

import { useState } from "react";
import DepartureSelect from "./components/DepartureSelect";
import ArrivalSelect from "./components/ArrivalSelect";
import { Flight } from "@/lib/api";
import { FlightSelect } from "./components/FlightSelect";

export default function Home() {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">Load Factor 予測</h1>

      <DepartureSelect value={departure} setValue={setDeparture} />
      <ArrivalSelect departure={departure} value={arrival} setValue={setArrival} />

      <p className="mt-4">選択中の出発空港: {departure}</p>
      <p>選択中の到着空港: {arrival}</p>

      <div className="mt-4">
        <FlightSelect onSelect={setSelectedFlight} />
      </div>

      {selectedFlight && (
        <div className="border p-2 rounded bg-gray-50">
          <h2 className="font-semibold">選択された便</h2>
          <p>
            {selectedFlight.flight_no} | {selectedFlight.airline_code} |{" "}
            {selectedFlight.distance_cat} | {selectedFlight.seat_capacity} seats
          </p>
        </div>
      )}
    </div>
  );
}
