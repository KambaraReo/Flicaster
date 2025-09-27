import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts";

type ShapValue = {
  feature: string;
  value: number;
};

type Props = {
  shapValues: ShapValue[];
};

const ShapBarChart = ({ shapValues }: Props) => {
  return (
    <div className="w-full h-120 p-6 bg-blue-900 rounded-2xl shadow-xl border border-purple-200">
      <h2 className="text-xl font-semibold mb-4 text-white">
        特徴量の影響度（SHAP値）
      </h2>
      <ResponsiveContainer width="100%" height="90%">
        <BarChart
          data={shapValues}
          layout="vertical"
          margin={{ top: 10, right: 0, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
          <XAxis
            type="number"
            tick={{ fill: "#fff", fontSize: 12 }}
            axisLine={{ stroke: "#fff" }}
          />
          <YAxis
            dataKey="feature"
            type="category"
            width={120}
            tick={{ fill: "#fff", fontSize: 12, fontWeight: 500 }}
            axisLine={{ stroke: "#fff" }}
          />
          <Tooltip
            formatter={(value: number) => value.toFixed(3)}
            contentStyle={{
              backgroundColor: "#1e3a8a",
              borderRadius: "8px",
              border: "2px solid #fff",
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            }}
            labelStyle={{
              color: "#cbd5e1",
              fontWeight: 700,
              fontSize: "14px"
            }}
            itemStyle={{
              color: "#fff",
              fontWeight: 700,
            }}
          />
          <Bar dataKey="value" radius={[4, 4, 4, 4]}>
            {shapValues.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.value >= 0 ? "#4c68ec" : "#f9c490"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export type { ShapValue };
export { ShapBarChart };
