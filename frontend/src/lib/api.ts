interface Airport {
  code: string;
  name: string;
  region: string;
  scale: string;
  lat: number;
  lon: number;
}

interface Flight {
  flight_no: string;
  departure: string;
  arrival: string;
  airline_code: string;
  distance_km: number;
  distance_cat: "short" | "medium" | "long";
  seat_capacity: number;
}

interface PredictRequest {
  date: string;
  departure: string;
  arrival: string;
  flight_no: string;
}

interface PredictResponse {
  features: {
    month: number;
    weekday: number;
    holiday_flag: number;
    weather_flag: number;
    reservations: number;
    lag_7: number;
    lag_14: number;
    lag_30: number;
    departure: string;
    arrival: string;
  };
  prediction: number;
  shap_values: {
    month: number;
    weekday: number;
    holiday_flag: number;
    weather_flag: number;
    reservations: number;
    lag_7: number;
    lag_14: number;
    lag_30: number;
    dep_encoded: number;
    arr_encoded: number;
  };
}

interface PredictInRangeRequest {
  start_date: string;
  end_date: string;
  departure: string;
  arrival: string;
  flight_no: string;
}

interface PredictInRangeResponse {
  predictions: {
    date: string;
    prediction: number;
  }[];
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8100";

// 全空港リストを取得
const fetchAirports = async (): Promise<Airport[]> => {
  try {
    const res = await fetch(`${API_BASE_URL}/airports`);
    if (!res.ok) throw new Error("空港リストの取得に失敗しました");
    const data: Airport[] = await res.json();
    return data;
  } catch (e) {
    console.log(e);
    return [];
  }
};

// 出発空港に応じた到着空港リストを取得
const fetchArrivalAirports = async (departure: string): Promise<Airport[]> => {
  try {
    const res = await fetch(
      `${API_BASE_URL}/airports/arrivals?departure=${departure}`
    );
    if (!res.ok) throw new Error("到着空港リストの取得に失敗しました");
    const data: Airport[] = await res.json();
    return data;
  } catch (e) {
    console.error(e);
    return [];
  }
};

// 出発&到着に応じて便リストを返す
const fetchFlights = async (
  departure: string,
  arrival: string
): Promise<Flight[]> => {
  try {
    const res = await fetch(
      `${API_BASE_URL}/flights/by_route?departure=${departure}&arrival=${arrival}`
    );
    if (!res.ok) throw new Error("便リストの取得に失敗しました");
    const data: Flight[] = await res.json();
    return data;
  } catch (e) {
    console.log(e);
    return [];
  }
};

// Load Factor予測APIを呼び出す
const fetchPredictedLoadFactor = async (
  params: PredictRequest
): Promise<PredictResponse> => {
  const res = await fetch(`${API_BASE_URL}/predict/load_factor/from_db`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });

  if (!res.ok) {
    throw new Error("予測APIの呼び出しに失敗しました");
  }

  const data: PredictResponse = await res.json();
  return data;
};

// 日付範囲での Load Factor予測APIを呼び出す
const fetchPredictedLoadFactorInRange = async (
  params: PredictInRangeRequest
): Promise<PredictInRangeResponse> => {
  const res = await fetch(`${API_BASE_URL}/predict/load_factor_range/from_db`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });

  if (!res.ok) {
    throw new Error("予測APIの呼び出しに失敗しました");
  }

  const data: PredictInRangeResponse = await res.json();
  return data;
};

export type {
  Airport,
  Flight,
  PredictRequest,
  PredictResponse,
  PredictInRangeRequest,
  PredictInRangeResponse,
};
export {
  fetchAirports,
  fetchArrivalAirports,
  fetchFlights,
  fetchPredictedLoadFactor,
  fetchPredictedLoadFactorInRange,
};
