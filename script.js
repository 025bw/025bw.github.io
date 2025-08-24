async function loadData() {
  const name = document.getElementById("pokemonInput").value.toLowerCase().replace(" ", "-");
  const res = document.getElementById("result");
  res.innerHTML = "Loading...";

  try {
    const response = await fetch(`data/${name}.json`);
    if (!response.ok) {
      res.innerHTML = "❌ No data found for " + name;
      return;
    }
    const data = await response.json();

    // Example: filter IV 44/45
    const filtered = data.filter(row => {
      const atk = parseInt(row["Atk"] || "0");
      const def = parseInt(row["Def"] || "0");
      const hp  = parseInt(row["Sta"] || "0");
      return (atk + def + hp) === 44;
    });

    let output = `<h2>${name}</h2><pre>${JSON.stringify(filtered, null, 2)}</pre>`;
    res.innerHTML = output;
  } catch (e) {
    res.innerHTML = "⚠️ Error: " + e;
  }
}