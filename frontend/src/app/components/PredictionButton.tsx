"use client";

interface Props {
  onClick: () => void;
  loading?: boolean;
  disabled?: boolean;
}

const PredictButton = ({
  onClick,
  loading = false,
  disabled = false,
}: Props) => {
  return (
    <div className="mt-6 text-center">
      <button
        onClick={onClick}
        disabled={disabled || loading}
        className="px-6 py-2 bg-gradient-to-r from-blue-900 to-blue-950 text-white font-semibold rounded-lg shadow-md hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 transition-colors"
      >
        {loading ? "予測中..." : "予測"}
      </button>
    </div>
  );
};

export { PredictButton };
