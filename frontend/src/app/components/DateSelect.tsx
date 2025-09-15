"use client";

type Props = {
  value: string;
  setValue: (value: string) => void;
};

const DateSelect: React.FC<Props> = ({ value, setValue }) => {
  return (
    <div className="mb-4">
      <label className="block text-gray-700 text-sm font-bold mb-2">日付</label>
      <input
        type="date"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
      />
    </div>
  );
};

export { DateSelect };
