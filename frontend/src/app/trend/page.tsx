"use client";

import { useState } from "react";
import { DateRangeSelect } from "../components/DateRangeSelect";
import DepartureSelect from "../components/DepartureSelect";
import ArrivalSelect from "../components/ArrivalSelect";
import { Flight } from "@/lib/api";
import { FlightSelect } from "../components/FlightSelect";
import { PredictButton } from "../components/PredictionButton";
import { LoadFactorTrendChart } from "../components/LoadFactorTrendChart";
import { fetchPredictedLoadFactorInRange } from "@/lib/api";

const TrendPage = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<{ date: string; prediction: number }[]>([]);

  const handlePredict = async () => {
    if (!startDate || !endDate || !departure || !arrival || !selectedFlight)
      return;

    setLoading(true);
    setPredictions([]);

    try {
      const data = await fetchPredictedLoadFactorInRange({
        start_date: startDate,
        end_date: endDate,
        departure,
        arrival,
        flight_no: selectedFlight.flight_no,
      });

      setPredictions(data.predictions);
    } catch (err) {
      console.error(err);
      alert("予測推移の取得に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = loading || !startDate || !endDate || !departure || !arrival || !selectedFlight;

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-blue-50 via-white to-blue-100 rounded-2xl shadow-xl border border-blue-200">
      <h1 className="text-2xl font-bold mb-6 text-center text-blue-900">
        ✈ Load Factor 予測推移
      </h1>

      <DateRangeSelect
        startDate={startDate}
        endDate={endDate}
        setStartDate={setStartDate}
        setEndDate={setEndDate}
      />

      <DepartureSelect value={departure} setValue={setDeparture} />
      <ArrivalSelect departure={departure} value={arrival} setValue={setArrival} />

      <div className="mt-4">
        <FlightSelect
          departure={departure}
          arrival={arrival}
          onSelect={setSelectedFlight}
        />
      </div>

      <PredictButton
        onClick={handlePredict}
        loading={loading}
        disabled={isDisabled}
      />

      <LoadFactorTrendChart data={predictions} />
    </div>
  );
};

export default TrendPage;
