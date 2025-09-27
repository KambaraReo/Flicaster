"use client";

import { useState } from "react";
import { DateSelect } from "./components/DateSelect";
import DepartureSelect from "./components/DepartureSelect";
import ArrivalSelect from "./components/ArrivalSelect";
import { Flight } from "@/lib/api";
import { FlightSelect } from "./components/FlightSelect";
import { PredictLoadFactorCard } from "./components/PredictLoadFactorCard";

export default function Home() {
  const [date, setDate] = useState("");
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">Load Factor 予測</h1>

      <DateSelect value={date} setValue={setDate} />

      <DepartureSelect value={departure} setValue={setDeparture} />
      <ArrivalSelect departure={departure} value={arrival} setValue={setArrival} />

      <div className="mt-4">
        <FlightSelect departure={departure} arrival={arrival} onSelect={setSelectedFlight} />
      </div>

      <PredictLoadFactorCard
        date={date}
        departure={departure}
        arrival={arrival}
        flight={selectedFlight}
      />
    </div>
  );
}
