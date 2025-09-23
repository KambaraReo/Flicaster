"use client";

import { useState } from "react";
import { Flight, fetchPredictedLoadFactor, PredictResponse } from "@/lib/api";

interface Props {
  date: string;
  departure: string;
  arrival: string;
  flight: Flight | null;
}

export const PredictButton = ({date, departure, arrival, flight }: Props) => {
  const [loading, setLoading] = useState(false);
  const [predictedLoadFactor, setPredictedLoadFactor] = useState<number | null>(null);

  const handlePredict = async () => {
    if (!date || !departure || !arrival || !flight) return;

    setLoading(true);
    setPredictedLoadFactor(null);

    try {
      const data: PredictResponse = await fetchPredictedLoadFactor({
        date,
        departure,
        arrival,
        flight_no: flight.flight_no,
      });
      setPredictedLoadFactor(data.prediction);
    } catch (err) {
      console.error(err);
      alert("予測に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = loading || !date || !departure || !arrival || !flight;

  return (
    <div className="mt-6 text-center">
      <button
        onClick={handlePredict}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        disabled={isDisabled}
      >
        {loading ? "予測中..." : "予測"}
      </button>

      {predictedLoadFactor !== null && (
        <div className="mt-4 text-xl font-bold">
          予測LF: {(predictedLoadFactor * 100).toFixed(1)} %
        </div>
      )}
    </div>
  );
};
