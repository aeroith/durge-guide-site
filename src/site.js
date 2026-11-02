// Everything here is optional. Without it the tier switch still works, a shot is a plain link, and the pins sit side by side.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia("(prefers-reduced-motion: reduce)");
  const remember = {
    get: () => { try { return localStorage.getItem("durge-tier"); } catch { return null; } },
    set: (v) => { try { localStorage.setItem("durge-tier", v); } catch { /* private window */ } },
  };
  document.documentElement.classList.add("js");

  // The answer you gave on the home page follows you to the Tiers page. The home page itself always starts at Normal,
  // so nobody comes back to a scene they chose to forget.
  const saved = remember.get();
  const decide = $(".decide");
  if (decide && ["minimal", "normal", "extensive"].includes(saved)) {
    decide.dataset.tier = saved;
    const tag = () => Object.assign(document.createElement("span"), { className: "yours", textContent: "Your answer" });
    $(`.pick[data-t=${saved}] p`).after(tag());
    $(`.compare thead th:nth-child(${["minimal", "normal", "extensive"].indexOf(saved) + 2})`).append(tag());
  }

  const radios = $$(".answer input");
  if (radios.length) {
    radios.forEach((r) => r.addEventListener("change", () => remember.set(r.value)));
    // Inside the answer, 1, 2 and 3 pick a line, as they do in the game's own conversations.
    const answer = $(".answer");
    answer.addEventListener("keydown", (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || !["1", "2", "3"].includes(e.key)) return;
      const r = radios[+e.key - 1];
      r.checked = true;
      r.focus({ preventScroll: true });
      remember.set(r.value);
    });
  }

  // Tabs and contents follow the reader down the page
  $$(".strip[data-spy], .toc").forEach((nav) => {
    const links = $$('a[href^="#"]', nav);
    const targets = links.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
    if (!targets.length || !("IntersectionObserver" in window)) return;
    const mark = (id) => links.forEach((a) => {
      const on = a.hash === `#${id}`;
      if (on === a.hasAttribute("aria-current")) return;
      if (on) {
        a.setAttribute("aria-current", "location");
        if (nav.scrollWidth > nav.clientWidth) nav.scrollTo({ left: a.offsetLeft - (nav.clientWidth - a.offsetWidth) / 2, behavior: calm.matches ? "auto" : "smooth" });
      } else a.removeAttribute("aria-current");
    });
    const seen = new IntersectionObserver((entries) => {
      entries.filter((e) => e.isIntersecting).forEach((e) => mark(e.target.id));
    }, { rootMargin: "-15% 0px -75% 0px" });
    targets.forEach((t) => seen.observe(t));
  });

  // Two aligned shots become one, with a divide to drag. A range input does the work, so keys and touch come free.
  $$("[data-wipe]").forEach((row) => {
    const [a, b] = $$(".shot", row);
    if (!a || !b) return;
    const box = document.createElement("div");
    box.className = "wipe";
    const under = $("picture", b);
    const over = $("picture", a);
    over.classList.add("over");
    $$("img", row).forEach((img) => { img.loading = "eager"; });
    const input = Object.assign(document.createElement("input"), { type: "range", min: 0, max: 100, step: 5, value: 50 });
    input.setAttribute("aria-label", row.dataset.wipe);
    input.setAttribute("aria-valuetext", "Halfway");
    input.addEventListener("input", () => {
      box.style.setProperty("--x", `${input.value}%`);
      box.style.setProperty("--v", input.value);
      input.setAttribute("aria-valuetext", `${input.value}% ${$("figcaption", a).textContent.replace(/\.$/, "")}`);
    });
    const bar = Object.assign(document.createElement("span"), { className: "bar" });
    const said = [a, b].map((fig) => $("figcaption", fig).textContent);
    const side = (cls, words) => Object.assign(document.createElement("span"), { className: `side ${cls}`, textContent: words.split(" ")[0].replace(".", "") });
    box.append(under, over, bar, side("l", said[0]), side("r", said[1]), input);
    row.replaceWith(box);
    if (said[0].includes(" ")) box.after(Object.assign(document.createElement("p"), { className: "wipe-cap", textContent: said.join(" ") }));
  });

  // A shot opens where it is, and grows to fill the screen. Only shots you have chosen to see are in the sequence.
  const shots = () => $$(".shot a[href^='img/'], .stage a[href^='img/']").filter((a) => (a.checkVisibility ? a.checkVisibility({ visibilityProperty: true }) : a.offsetParent));
  let box, current = -1, list = [], opener = null;

  const morph = (change) => {
    if (!document.startViewTransition || calm.matches || document.hidden) { change(); return; }
    const t = document.startViewTransition(change);
    t.ready.catch(() => {}); // an interrupted morph is not an error: the change still happened
    t.finished.catch(() => {});
  };
  const thumb = (a) => (a ? $("img", a) : null);
  const onScreen = (el) => { const r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; };

  function build() {
    box = document.createElement("dialog");
    box.className = "lb";
    box.setAttribute("aria-label", "Screenshot");
    box.innerHTML = `<figure><div class="frame"><img alt=""></div><figcaption></figcaption></figure>
      <div class="lb-bar">
        <button type="button" class="prev">Previous</button>
        <span class="count" aria-live="polite"></span>
        <button type="button" class="next">Next</button>
        <button type="button" class="zoom" aria-pressed="false">Zoom</button>
        <button type="button" class="close" autofocus>Close</button>
      </div>`;
    document.body.append(box);
    $(".prev", box).addEventListener("click", () => step(-1));
    $(".next", box).addEventListener("click", () => step(1));
    $(".close", box).addEventListener("click", shut);
    $(".zoom", box).addEventListener("click", () => zoom());
    $("img", box).addEventListener("click", () => zoom());
    box.addEventListener("click", (e) => { if (e.target === box || e.target.tagName === "FIGURE") shut(); });
    box.addEventListener("cancel", (e) => { e.preventDefault(); shut(); });
    box.addEventListener("keydown", (e) => {
      if (box.classList.contains("zoomed")) return;
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
    // swipe, on touch only. A cancelled gesture is simply forgotten.
    let from = null;
    const img = $("img", box);
    img.addEventListener("pointerdown", (e) => { from = e.pointerType === "touch" && e.isPrimary ? { x: e.clientX, y: e.clientY } : null; });
    img.addEventListener("pointercancel", () => { from = null; });
    img.addEventListener("pointerup", (e) => {
      if (!from || box.classList.contains("zoomed")) return;
      const dx = e.clientX - from.x, dy = e.clientY - from.y;
      from = null;
      if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) step(dx < 0 ? 1 : -1);
    });
  }

  function zoom(on = !box.classList.contains("zoomed")) {
    box.classList.toggle("zoomed", on);
    $(".zoom", box).setAttribute("aria-pressed", on);
    $(".frame", box).scrollTo(0, 0); // the note is at the top left
  }

  function show(k) {
    current = k;
    zoom(false);
    const a = list[k];
    const t = thumb(a);
    const img = $("img", box);
    const fig = a.closest("figure");
    img.alt = t.alt;
    img.style.maxWidth = "";
    img.src = t.currentSrc || t.src; // what's already loaded first, then the full size over it
    const full = new Image();
    full.onload = () => {
      if (list[current] !== a) return;
      img.src = a.href;
      img.style.maxWidth = `${full.naturalWidth * 2}px`; // a small crop stays sharp rather than filling the screen
    };
    full.src = a.href;
    $("figcaption", box).textContent = a.dataset.caption ?? $("figcaption", fig)?.textContent ?? "";
    $(".count", box).textContent = `${k + 1} of ${list.length}`;
    $(".prev", box).disabled = k === 0;
    $(".next", box).disabled = k === list.length - 1;
  }

  function step(by) {
    const k = current + by;
    if (k >= 0 && k < list.length) morph(() => show(k));
  }

  function open(a) {
    if (!box) build();
    list = shots();
    opener = a;
    const t = thumb(a);
    const img = $("img", box);
    t.style.viewTransitionName = "shot";
    morph(() => {
      t.style.viewTransitionName = "";
      img.style.viewTransitionName = "shot";
      show(list.indexOf(a));
      box.showModal();
    });
  }

  function shut() {
    const t = thumb(list[current]);
    const img = $("img", box);
    const back = t && onScreen(t);
    img.style.viewTransitionName = back ? "shot" : "";
    const home = back ? list[current] : opener; // where keyboard focus returns
    morph(() => {
      box.close();
      img.style.viewTransitionName = "";
      if (back) t.style.viewTransitionName = "shot";
      home?.focus({ preventScroll: true });
    });
    setTimeout(() => { if (t) t.style.viewTransitionName = ""; }, 600);
  }

  document.addEventListener("click", (e) => {
    const a = e.target.closest(".shot a[href^='img/'], .stage a[href^='img/']");
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (!$("img", a) || typeof HTMLDialogElement !== "function") return;
    e.preventDefault();
    open(a);
  });
})();
