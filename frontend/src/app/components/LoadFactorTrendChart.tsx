"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

type Prediction = {
  date: string;
  prediction: number;
};

interface Props {
  data: Prediction[];
}

const LoadFactorTrendChart = ({ data }: Props) => {
  if (data.length === 0) return null;

  return (
    <div className="mt-8 w-full h-100 p-6 bg-blue-900 rounded-2xl shadow-xl border border-purple-200">
      <h2 className="text-xl font-semibold mb-4 text-white text-center">
        Load Factor 予測推移
      </h2>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#fff", fontSize: 12 }}
            axisLine={{ stroke: "#fff" }}
          />
          <YAxis
            tick={{ fill: "#fff", fontSize: 12 }}
            domain={[0, 1]}
            axisLine={{ stroke: "#fff" }}
          />
          <Tooltip
            formatter={(value: number) => `${(value * 100).toFixed(1)} %`}
            contentStyle={{
              backgroundColor: "#1e3a8a",
              borderRadius: "8px",
              border: "2px solid #fff",
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            }}
            labelStyle={{
              color: "#cbd5e1",
              fontWeight: 700,
              fontSize: "14px",
            }}
            itemStyle={{
              color: "#fff",
              fontWeight: 700,
            }}
          />
          <Line
            type="monotone"
            dataKey="prediction"
            stroke="#f69442"
            strokeWidth={3}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export { LoadFactorTrendChart };
