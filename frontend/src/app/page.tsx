"use client";

import { useState } from "react";
import DepartureSelect from "./components/DepartureSelect";
import ArrivalSelect from "./components/ArrivalSelect";

export default function Home() {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">Load Factor 予測</h1>

      <DepartureSelect value={departure} setValue={setDeparture} />
      <ArrivalSelect departure={departure} value={arrival} setValue={setArrival} />

      <p className="mt-4">選択中の出発空港: {departure}</p>
      <p>選択中の到着空港: {arrival}</p>
    </div>
  );
}
