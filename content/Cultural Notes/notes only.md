## Title

```dataviewjs
(async () => {
  this.container.innerHTML = `<div id="status" style="font-family:monospace;color:#888;">⏳ Initializing...</div>`;
  const statusEl = this.container.querySelector("#status");
  const setStatus = (m)=>statusEl.textContent=m;

  async function loadVis() {
    if (window.vis) { setStatus("✅ Vis.js already loaded"); return; }

    setStatus("📥 Loading Vis.js from jsDelivr...");
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.css";
    document.head.appendChild(css);

    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js";
    document.head.appendChild(script);

    await new Promise((resolve, reject)=>{
      script.onload = resolve;
      script.onerror = ()=>reject(new Error("Vis.js load failed"));
    });
    setStatus("✅ Vis.js loaded");
  }

  try {
    await loadVis();
  } catch(e) {
    setStatus("❌ Failed to load Vis.js");
    console.error(e);
    return;
  }

  setStatus("⚙️ Preparing data...");
  const data = {
    nodes: [
      { id: 1, label: "Note A" },
      { id: 2, label: "Note B" },
      { id: 3, label: "Note C" }
    ],
    edges: [
      { from: 1, to: 2 },
      { from: 2, to: 3 },
      { from: 3, to: 1 }
    ]
  };

  const options = {
    nodes: { shape: "dot", size: 18, font: { size: 14 } },
    edges: { arrows: "to", color: { opacity: 0.6 } },
    physics: { stabilization: true }
  };

  this.container.style.height = "400px";
  this.container.style.border = "1px solid #555";
  const net = document.createElement("div");
  net.style.height = "100%";
  this.container.appendChild(net);

  setStatus("🧩 Rendering network...");
  new vis.Network(net, data, options);
  setStatus("✅ Done! Interactive network ready 🎉");
})();


```


works in notes, not in advanced slides.



--
# slides 2

```---
theme: white
title: Vis.js Graph Demo
---

# Network Graph Demo
This slide will show an **interactive Vis.js network** right inside the presentation.

<div id="vis-network" style="width:100%; height:400px; border:1px solid #888;"></div>

<!-- Load Vis.js (from jsDelivr CDN) -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.css"
/>
<script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>

<script>
(function() {
  // Wait until the slide is fully loaded
  function initVis() {
    if (!window.vis) return requestAnimationFrame(initVis);

    const container = document.getElementById("vis-network");
    if (!container) return;

    const data = {
      nodes: [
        { id: 1, label: "Node A" },
        { id: 2, label: "Node B" },
        { id: 3, label: "Node C" },
      ],
      edges: [
        { from: 1, to: 2 },
        { from: 2, to: 3 },
        { from: 3, to: 1 },
      ],
    };

    const options = {
      nodes: { shape: "dot", size: 18 },
      edges: { arrows: "to" },
      physics: { stabilization: true },
    };

    new vis.Network(container, data, options);
  }

  initVis();
})();
</script>

---

# Another Slide
You can move to the next slide →  
This one has **no graph**, just content.

```


---
## slides 3
[[春节]]

```dataviewjs
// 1️⃣ Load Vis.js dynamically if not already loaded
async function loadVis() {
  if (window.vis) return; // already loaded

  const cssLink = document.createElement("link");
  cssLink.rel = "stylesheet";
  cssLink.href = "https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/vis-network.min.css";
  document.head.appendChild(cssLink);

  const script = document.createElement("script");
  script.src = "https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/vis-network.min.js";
  document.head.appendChild(script);

  // Wait until the script loads
  await new Promise((resolve) => {
    script.onload = resolve;
  });
}

// 2️⃣ Wait for Vis.js to load
await loadVis();

// 3️⃣ Define the data
const data = {
  nodes: [
    { id: 1, label: "Note A" },
    { id: 2, label: "Note B" },
    { id: 3, label: "Note C" },
  ],
  edges: [
    { from: 1, to: 2 },
    { from: 2, to: 3 },
  ],
};

// 4️⃣ Configure the graph
const options = {
  nodes: { shape: "dot", size: 20, font: { size: 16 } },
  edges: { arrows: "to", color: { opacity: 0.6 } },
  physics: { stabilization: true },
};

// 5️⃣ Render in the container
this.container.style.height = "400px";
this.container.style.border = "1px solid #444";
new vis.Network(this.container, data, options);


```

---

### 🧠 Why this works
- It **waits** until the Vis.js library is completely loaded before using it.
- It loads the **CSS + JS** files from CDN only once per session.
- It’s fully self-contained inside one DataviewJS block.

---

### ⚙️ If you want offline mode
You can replace the CDN URLs with your local file paths:
```js
cssLink.href = app.vault.adapter.getResourcePath("_resources/libs/vis-network.min.css");
script.src = app.vault.adapter.getResourcePath("_resources/libs/vis-network.min.js");
