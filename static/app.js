const pageList = document.querySelector("#pageList");
const pageCount = document.querySelector("#pageCount");
const content = document.querySelector("#content");
const chips = document.querySelector("#chips");
const search = document.querySelector("#search");
const messages = document.querySelector("#messages");
const form = document.querySelector("#chatForm");
const question = document.querySelector("#question");
const reset = document.querySelector("#reset");

let pages = [];
let selected = "";

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function inlineMd(text) {
  return escapeHtml(text)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function articleMd(text) {
  return text
    .replace(/^# (.*)$/gm, "<h1>$1</h1>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^- (.*)$/gm, "<li>$1</li>")
    .replace(/\[\[([^\]]+)\]\]/g, '<button class="wikilink" data-slug="$1">$1</button>')
    .replace(/\n\n/g, "</p><p>")
    .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");
}

function chatMd(text) {
  const lines = String(text || "").trim().split(/\r?\n/);
  const html = [];
  let listOpen = false;

  for (const raw of lines) {
    const line = raw.trim();
    if (!line) {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
      continue;
    }

    if (line.startsWith("### ")) {
      if (listOpen) html.push("</ul>");
      listOpen = false;
      html.push(`<h3>${inlineMd(line.slice(4))}</h3>`);
    } else if (line.startsWith("## ")) {
      if (listOpen) html.push("</ul>");
      listOpen = false;
      html.push(`<h3>${inlineMd(line.slice(3))}</h3>`);
    } else if (line.startsWith("- ")) {
      if (!listOpen) {
        html.push("<ul>");
        listOpen = true;
      }
      html.push(`<li>${inlineMd(line.slice(2))}</li>`);
    } else {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
      html.push(`<p>${inlineMd(line)}</p>`);
    }
  }

  if (listOpen) html.push("</ul>");
  return html.join("");
}

function renderList(items) {
  pageList.innerHTML = "";
  items.forEach((page) => {
    const button = document.createElement("button");
    button.className = page.slug === selected ? "active" : "";
    button.textContent = page.title;
    button.addEventListener("click", () => loadPage(page.slug));
    pageList.append(button);
  });
}

async function loadPage(slug) {
  selected = slug;
  const page = await fetch(`/api/page/${slug}`).then((r) => r.json());
  chips.innerHTML = page.tags.map((tag) => `<span>${tag}</span>`).join("") + `<small>updated ${page.updated}</small>`;
  content.innerHTML = `<p>${articleMd(page.body)}</p>`;
  renderList(pages);
  document.querySelectorAll(".wikilink").forEach((el) => {
    el.addEventListener("click", () => loadPage(el.dataset.slug));
  });
}

async function init() {
  pages = await fetch("/api/pages").then((r) => r.json());
  pageCount.textContent = pages.length;
  renderList(pages);
  await loadPage("ml-index");
  addMessage("bot", "머신러닝 Wiki에 오신 것을 환영합니다. 궁금한 개념을 물어보면 Wiki 근거를 찾아 답변할게요.");
}

async function doSearch() {
  const query = search.value.trim();
  if (!query) return renderList(pages);
  const results = await fetch("/api/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({query}),
  }).then((r) => r.json());
  renderList(results);
}

function addMessage(role, text, sources = []) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  const refs = sources.map((s) => `<button data-slug="${s.slug}">[${escapeHtml(s.title)}]</button>`).join(" ");
  bubble.innerHTML = `${chatMd(text)}${refs ? `<div class="refs">${refs}</div>` : ""}`;
  messages.append(bubble);
  bubble.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => loadPage(b.dataset.slug)));
  messages.scrollTop = messages.scrollHeight;
}

search.addEventListener("input", doSearch);
reset.addEventListener("click", () => {
  messages.innerHTML = "";
  addMessage("bot", "대화를 초기화했습니다. Wiki page 근거로 다시 답변할게요.");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = question.value.trim();
  if (!text) return;
  question.value = "";
  addMessage("user", text);
  const result = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: text}),
  }).then((r) => r.json());
  addMessage("bot", result.answer || result.error, result.sources || []);
});

init();
