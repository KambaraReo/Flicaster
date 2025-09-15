interface Airport {
  code: string; // 空港コード（例: HND）
  name: string; // 空港名（例: Tokyo Haneda）
  region: string; // 地域（例: Kanto）
  scale: string; // 規模（例: hub）
  lat: number; // 緯度
  lon: number; // 経度
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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8100";

// 空港一覧を返す
const fetchAirports = async (): Promise<Airport[]> => {
  try {
    const res = await fetch(`${API_BASE_URL}/api/airports`);
    if (!res.ok) throw new Error("空港リストの取得に失敗しました");

    const data: Airport[] = await res.json();
    return data;
  } catch (e) {
    console.log(e);
    return [];
  }
};

// 出発&到着に応じて便リストを返す
const fetchFlights = async (
  departure: string,
  arrival: string
): Promise<Flight[]> => {
  try {
    const res = await fetch(`${API_BASE_URL}/api/flights`);
    if (!res.ok) throw new Error("便リストの取得に失敗しました");

    const data: Flight[] = await res.json();
    return data;
  } catch (e) {
    console.log(e);
    return [];
  }
};

export type { Airport, Flight };
export { fetchAirports, fetchFlights };
