/* braille-flow — 6-dot braille generative strip.
   Dependency-free. Full option reference lives in the source this was
   lifted from; the ones used on this site are in _includes/braille.html.
*/
(function (global) {
  "use strict";

  // 6-dot braille: BITS[column 0..1][row 0..2]  ->  U+2800 + mask
  var BITS = [[0x01, 0x02, 0x04], [0x08, 0x10, 0x20]];

  var DEFAULTS = {
    orientation: "vertical",
    whitespace: 0.52,
    flowSpeed: 0.018,
    scale: 0.05,
    stretch: 0.7,
    cellSize: 15,
    color: "auto",
    gradient: null,
    opacity: 0.9,
    fade: 0.1,
    field: "filament",
    scrollContainer: null,
    swirl: 0,            // 0 = one fixed diagonal; >0 bends the bands, so they
                         // run in many directions instead of one repeating one
    bandScale: 1,        // <1 = fewer, fatter ribbons (spacing only; does not warp them)
    inkDensity: null,    // number 0..1 = hold this exact ink fraction on every
                         // page by calibrating the cut, instead of using
                         // `whitespace` as a raw threshold. Density otherwise
                         // swings with the seed (8%..46% observed), and a
                         // heavily-filled field just reads as noise.
    seedCandidates: 1,   // >1 = probe this many deterministic phases and keep
                         // the most coherent one (rejects speckly draws)
    minCoherence: 0.93,  // stop probing early once a candidate scores this
    recalibrateEvery: 30,// draws between threshold refreshes as the field moves
    fps: 24,
    seed: null,
    animate: true,       // false = paint one frame and never start the rAF loop.
                         // For a small field a still draw is visually the same
                         // and costs nothing to keep on screen.
    respectReducedMotion: true,
    pauseWhenOffscreen: true
  };

  // --- field functions -------------------------------------------------
  function hash(x, y, s) { var n = Math.sin(x * 127.1 + y * 311.7 + s) * 43758.5453; return n - Math.floor(n); }
  function vnoise(x, y, s) {
    var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    var u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    var a = hash(xi, yi, s), b = hash(xi + 1, yi, s), c = hash(xi, yi + 1, s), d = hash(xi + 1, yi + 1, s);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function fbm(x, y, s) { var t = 0, amp = 0.5, f = 1; for (var i = 0; i < 4; i++) { t += amp * vnoise(x * f, y * f, s); f *= 2; amp *= 0.5; } return t; }

  // Smooth domain-warped filament field: flowing ribbons with open space.
  //
  // The ink lands where sin(time - p) is near zero, so `p` decides which way
  // the ribbons run. With p = ux + uy every band sits on the same downward
  // diagonal, evenly spaced 2*PI apart — which reads as a repeating pattern
  // once the canvas is wide. `swirl` bends the bands by ADDING a bounded
  // low-frequency term.
  //
  // It must be added, never used to re-weight ux/uy. Any formulation that
  // multiplies uy (e.g. blending p between the two diagonals) amplifies the
  // spatial variation by |uy| — and uy carries the scroll offset, so a page
  // scrolled a few thousand pixels turns to pure noise. Measured coherence
  // with the multiplicative form: 0.89 at the top of the page, 0.19 by 30k px.
  // With this additive form it holds 0.89-0.94 at any depth.
  function filament(ux, uy, time, swirl, band) {
    for (var i = 1; i < 5; i++) {
      ux += 0.5 / i * Math.cos(i * 2.5 * uy + time);
      uy += 0.5 / i * Math.cos(i * 1.5 * ux + time);
    }
    var p = ux + uy;
    if (swirl) {
      p += swirl * Math.cos(ux * 0.19 - uy * 0.13)
         + swirl * 0.6 * Math.cos(uy * 0.11 + 1.7);
    }
    // Stretch the band spacing here rather than by lowering `scale`. The warp
    // above has a fixed amplitude, so shrinking `scale` makes the warp large
    // relative to the field and the ribbons break up into speckle; scaling `p`
    // widens them while leaving the warp-to-feature ratio alone.
    var s = 0.15 / Math.max(0.001, Math.abs(Math.sin(time - p * band)));
    s = Math.max(0, Math.min(1, (s - 0.02) / 0.98));
    return s * s * (3 - 2 * s);
  }

  function create(canvas, options) {
    if (!canvas || !canvas.getContext) return null;
    var o = Object.assign({}, DEFAULTS, options || {});
    var ctx = canvas.getContext("2d");

    var W = 0, H = 0, cellW = 0, cellH = 0, cols = 0, rows = 0;
    var ink = "rgba(120,120,120," + o.opacity + ")", grad = null;
    var phase = (o.seed == null ? Math.random() * 1000 : o.seed);
    // The animation clock starts at zero, NOT at the seed. `drift` is derived
    // from t and offsets the sample coordinates, so seeding t with a large
    // per-page hash starts the field thousands of units off origin — which
    // wrecks coherence the same way a deep scroll does. The seed varies the
    // pattern through `phase` instead, which only ever enters as a phase.
    var t = 0;
    var raf = 0, running = false, last = 0;
    var threshold = null, phasePicked = false, drawsSinceCal = 0;
    var reduce = !!(global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches);
    var darkMQ = global.matchMedia ? global.matchMedia("(prefers-color-scheme: dark)") : null;
    var ro = null, io = null, onScroll = null;

    function resolveColor() {
      if (o.gradient && o.gradient.length >= 2 && W && H) {
        var horiz = o.orientation === "horizontal";
        grad = ctx.createLinearGradient(0, 0, horiz ? W : 0, horiz ? 0 : H);
        grad.addColorStop(0, o.gradient[0]);
        grad.addColorStop(1, o.gradient[1]);
        ink = null;
      } else {
        grad = null;
        var col = o.color === "auto" ? (getComputedStyle(canvas).color || "rgb(120,120,120)") : o.color;
        var m = col.match(/[\d.]+/g);
        ink = (m && m.length >= 3) ? "rgba(" + m[0] + "," + m[1] + "," + m[2] + "," + o.opacity + ")" : col;
      }
    }

    function applyFade() {
      if (!o.fade || o.fade <= 0) { canvas.style.webkitMaskImage = ""; canvas.style.maskImage = ""; return; }
      var p = Math.max(0, Math.min(49, o.fade * 100));
      var dir = o.orientation === "horizontal" ? "to right" : "to bottom";
      var g = "linear-gradient(" + dir + ",transparent,#000 " + p + "%,#000 " + (100 - p) + "%,transparent)";
      canvas.style.webkitMaskImage = g; canvas.style.maskImage = g;
    }

    function setup() {
      var dpr = Math.max(1, Math.min(global.devicePixelRatio || 1, 2));
      W = canvas.clientWidth; H = canvas.clientHeight;
      if (!W || !H) return;
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.font = o.cellSize + "px " + "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
      ctx.textAlign = "left"; ctx.textBaseline = "top";
      cellW = ctx.measureText("\u28ff").width || o.cellSize * 0.6;
      cellH = o.cellSize * 0.72;                    // pull rows tight (6-dot leaves the bottom row empty)
      cols = Math.ceil(W / cellW) + 1;
      rows = Math.ceil(H / cellH) + 1;
      resolveColor(); applyFade();
      if (o.inkDensity != null) {
        if (!phasePicked) { phase = pickPhase(); phasePicked = true; }
        threshold = null;   // canvas size changed, re-measure from scratch
        recalibrate();
        drawsSinceCal = 0;
      }
      if (!running) draw();                          // keep a fresh frame when paused/reduced
    }

    function scrollProgress() {
      var el = o.scrollContainer; if (!el) return 0;
      var max = el.scrollHeight - el.clientHeight;
      return max > 0 ? Math.min(1, Math.max(0, el.scrollTop / max)) : 0;
    }

    // Offsets shared by draw() and the calibration sampler, so the cut is
    // measured on exactly the field that gets painted.
    function offsets() {
      var fx = o.scale, fy = o.scale * o.stretch;
      var horiz = o.orientation === "horizontal";
      // The flow animation rides on `time` (see draw), which enters the field
      // purely as a phase. Only the optional scroll nudge slides the sample
      // coordinates, and that is bounded.
      var d = -scrollProgress() * 40;
      return { fx: fx, fy: fy, ox: horiz ? d : 0, oy: horiz ? 0 : d };
    }

    // --- density calibration & seed selection -------------------------------
    // Sample the field on a strided dot grid.
    function sample(ph, tt, stride) {
      var f = offsets();
      var SW = Math.max(2, Math.floor(cols * 2 / stride));
      var SH = Math.max(2, Math.floor(rows * 3 / stride));
      var v = new Float64Array(SW * SH);
      for (var y = 0; y < SH; y++) {
        for (var x = 0; x < SW; x++) {
          var sx = (x * stride + ph) * f.fx + f.ox;
          var sy = (y * stride) * f.fy + f.oy;
          v[y * SW + x] = (o.field === "noise") ? fbm(sx, sy, ph)
                                                : filament(sx, sy, tt, o.swirl, o.bandScale);
        }
      }
      return { v: v, W: SW, H: SH };
    }

    // The cut that leaves exactly o.inkDensity of the field inked.
    function cutFor(g) {
      var a = Float64Array.from(g.v);
      a.sort();
      var i = Math.floor((1 - o.inkDensity) * a.length);
      return a[Math.max(0, Math.min(a.length - 1, i))];
    }

    // P(a 4-neighbour is also ink | this dot is ink). Flowing ribbons score
    // high (~.95); salt-and-pepper noise scores near the ink density.
    function coherenceOf(g, cut) {
      var SW = g.W, SH = g.H, v = g.v, pairs = 0, both = 0;
      for (var y = 0; y < SH; y++) {
        for (var x = 0; x < SW; x++) {
          if (v[y * SW + x] <= cut) continue;
          if (x + 1 < SW) { pairs++; if (v[y * SW + x + 1] > cut) both++; }
          if (y + 1 < SH) { pairs++; if (v[(y + 1) * SW + x] > cut) both++; }
        }
      }
      return pairs ? both / pairs : 0;
    }

    // Deterministically try a few phases and keep the most coherent, so a page
    // whose seed lands on a speckly region of the field gets a better one.
    function pickPhase() {
      if (!(o.seedCandidates > 1)) return phase;
      var bestPh = phase, bestC = -1;
      for (var k = 0; k < o.seedCandidates; k++) {
        // Step is deliberately not the offset callers use between sibling
        // instances (7919), or two strips seeded 7919 apart would walk the
        // same ladder and settle on the same phase as each other.
        var ph = (phase + k * 41957) % 100000;
        var g = sample(ph, ph * 2, 4);
        var c = coherenceOf(g, cutFor(g));
        if (c > bestC) { bestC = c; bestPh = ph; }
        if (c >= o.minCoherence) break;
      }
      return bestPh;
    }

    function recalibrate() {
      var g = sample(phase, t + phase, 4);
      var cut = cutFor(g);
      // Ease toward the new cut so an animating field doesn't pop.
      threshold = (threshold === null) ? cut : threshold + (cut - threshold) * 0.5;
    }

    function draw() {
      if (!W || !H) return;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = grad || ink;
      if (o.inkDensity != null && ++drawsSinceCal >= o.recalibrateEvery) {
        recalibrate();
        drawsSinceCal = 0;
      }
      var cut = (o.inkDensity != null && threshold !== null) ? threshold : o.whitespace;
      var f = offsets();
      var fx = f.fx, fy = f.fy, ox = f.ox, oy = f.oy;
      var swirl = o.swirl, band = o.bandScale;
      for (var cy = 0; cy < rows; cy++) {
        for (var cx = 0; cx < cols; cx++) {
          var mask = 0;
          for (var dx = 0; dx < 2; dx++) for (var dy = 0; dy < 3; dy++) {
            var gx = cx * 2 + dx, gy = cy * 3 + dy;
            var sx = (gx + phase) * fx + ox, sy = gy * fy + oy;
            var val = (o.field === "noise") ? fbm(sx, sy, phase) : filament(sx, sy, t + phase, swirl, band);
            if (val > cut) mask |= BITS[dx][dy];
          }
          if (mask) ctx.fillText(String.fromCharCode(0x2800 + mask), cx * cellW, cy * cellH);
        }
      }
    }

    function frame(ts) {
      raf = requestAnimationFrame(frame);
      if (ts - last < 1000 / o.fps) return;
      last = ts;
      t += o.flowSpeed;   // flowSpeed alone sets the pace; 0 is genuinely still
      draw();
    }

    function start() {
      if (running) return;
      if (!o.animate || (reduce && o.respectReducedMotion)) { draw(); return; } // one still frame
      running = true; last = performance.now(); raf = requestAnimationFrame(frame);
    }
    function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

    // observers ---------------------------------------------------------
    if (typeof ResizeObserver !== "undefined") { ro = new ResizeObserver(setup); ro.observe(canvas); }
    else global.addEventListener("resize", setup);

    if (o.pauseWhenOffscreen && typeof IntersectionObserver !== "undefined") {
      io = new IntersectionObserver(function (es) { es[0] && es[0].isIntersecting ? start() : stop(); });
      io.observe(canvas);
    }

    // A scroll of the page itself is fired at `document`, which never reaches
    // document.scrollingElement — so that has to be listened for on window.
    var scrollTarget = null;
    if (o.scrollContainer) {
      scrollTarget = (o.scrollContainer === document.scrollingElement ||
                      o.scrollContainer === document.documentElement ||
                      o.scrollContainer === document.body) ? global : o.scrollContainer;
      // Keep static / reduced-motion views in sync while scrolling. An
      // animating instance is already redrawing on its own timer.
      onScroll = function () { if (!running) draw(); };
      scrollTarget.addEventListener("scroll", onScroll, { passive: true });
    }

    if (darkMQ) darkMQ.addEventListener("change", function () { resolveColor(); if (!running) draw(); });

    setup();
    if (!o.pauseWhenOffscreen || typeof IntersectionObserver === "undefined") start();

    return {
      setOptions: function (partial) { Object.assign(o, partial || {}); setup(); },
      pause: stop,
      resume: start,
      destroy: function () {
        stop();
        if (ro) ro.disconnect(); else global.removeEventListener("resize", setup);
        if (io) io.disconnect();
        if (onScroll && scrollTarget) scrollTarget.removeEventListener("scroll", onScroll);
        ctx.clearRect(0, 0, W, H);
        canvas.style.webkitMaskImage = ""; canvas.style.maskImage = "";
      }
    };
  }

  function autoInit() {
    var list = document.querySelectorAll("canvas[data-braille-flow]");
    for (var i = 0; i < list.length; i++) {
      var opts = {}; var raw = list[i].getAttribute("data-braille-flow");
      if (raw) { try { opts = JSON.parse(raw); } catch (e) { /* leave defaults */ } }
      create(list[i], opts);
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", autoInit);
  else autoInit();

  global.BrailleFlow = { create: create, autoInit: autoInit };
})(window);
