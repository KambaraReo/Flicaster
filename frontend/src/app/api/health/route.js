export async function GET() {
  const BACKEND_URL = process.env.BACKEND_URL; // サーバーサイド変数を参照

  try {
    const res = await fetch(`${BACKEND_URL}/health`);
    const data = await res.json();

    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {

    return new Response(JSON.stringify({ error: `Failed to fetch backend - ${error}` }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
