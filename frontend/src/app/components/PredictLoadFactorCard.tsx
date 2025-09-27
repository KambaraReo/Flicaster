"use client";

import { useState } from "react";
import { Flight, fetchPredictedLoadFactor, PredictResponse } from "@/lib/api";
import type { ShapValue } from "@/app/components/ShapBarChart";
import { ShapBarChart } from "@/app/components/ShapBarChart";

interface Props {
  date: string;
  departure: string;
  arrival: string;
  flight: Flight | null;
}

const PredictLoadFactorCard = ({ date, departure, arrival, flight }: Props) => {
  const [loading, setLoading] = useState(false);
  const [predictedLoadFactor, setPredictedLoadFactor] = useState<number | null>(
    null
  );
  const [shapValues, setShapValues] = useState<ShapValue[] | null>(null);

  const handlePredict = async () => {
    if (!date || !departure || !arrival || !flight) return;

    setLoading(true);
    setPredictedLoadFactor(null);
    setShapValues(null);

    try {
      const data: PredictResponse = await fetchPredictedLoadFactor({
        date,
        departure,
        arrival,
        flight_no: flight.flight_no,
      });
      setPredictedLoadFactor(data.prediction);

      const shapArray: ShapValue[] = Object.entries(data.shap_values).map(
        ([feature, value]) => ({ feature, value })
      );
      setShapValues(shapArray);
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
        className="px-6 py-2 bg-gradient-to-r from-blue-900 to-blue-950 text-white font-semibold rounded-lg shadow-md hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 transition-colors"
        disabled={isDisabled}
      >
        {loading ? "予測中..." : "予測"}
      </button>

      {predictedLoadFactor !== null && (
        <div className="mt-4 text-xl font-bold text-[color:var(--color-gray-700)]">
          予測LF:
          <span className="text-3xl ml-2 font-bold text-blue-900">
            {(predictedLoadFactor * 100).toFixed(1)} %
          </span>
        </div>
      )}

      {shapValues && shapValues.length > 0 && (
        <div className="mt-4 mb-4">
          <ShapBarChart shapValues={shapValues} />
        </div>
      )}
    </div>
  );
};

export { PredictLoadFactorCard };
