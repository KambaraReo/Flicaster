interface Airport {
  code: string; // 空港コード（例: HND）
  name: string; // 空港名（例: Tokyo Haneda）
  region: string; // 地域（例: Kanto）
  scale: string; // 規模（例: hub）
  lat: number; // 緯度
  lon: number; // 経度
}

const fetchAirports = async (): Promise<Airport[]> => {
  try {
    const res = await fetch("api/airports");
    if (!res.ok) throw new Error("空港リストの取得に失敗しました");

    const data: Airport[] = await res.json();
    return data;
  } catch (e) {
    console.log(e);
    return [];
  }
};

export type { Airport };
export { fetchAirports };
