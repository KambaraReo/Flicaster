const healtCheck = async () => {
  const res = await fetch("/api/health");

  return res.json();
}

export default healtCheck;
