<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OmniVision System: Tactical Multi-Spectral Console</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Tailwind Config -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            cyber: {
              black: '#080c14',
              dark: '#0f172a',
              blue: '#06b6d4',
              green: '#10b981',
              amber: '#f59e0b',
              red: '#ef4444',
              purple: '#8b5cf6',
            }
          },
          fontFamily: {
            mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
          }
        }
      }
    }
  </script>
  <!-- Google Fonts for Cyberpunk/Sci-Fi aesthetics -->
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'JetBrains Mono', monospace;
      background-color: #05070c;
    }
    .hud-title {
      font-family: 'Orbitron', sans-serif;
    }
    /* Custom scanline overlay for styling */
    .scanlines {
      position: relative;
      overflow: hidden;
    }
    .scanlines::after {
      content: " ";
      display: block;
      position: absolute;
      top: 0; left: 0; bottom: 0; right: 0;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
      background-size: 100% 4px, 6px 100%;
      z-index: 10;
      pointer-events: none;
    }
    /* CRT Flicker */
    @keyframes crt-flicker {
      0% { opacity: 0.98; }
      50% { opacity: 1; }
      100% { opacity: 0.99; }
    }
    .crt-glow {
      animation: crt-flicker 0.15s infinite;
    }
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #06b6d4;
    }
  </style>
</head>
<body class="text-slate-300 min-h-screen flex flex-col selection:bg-cyan-500 selection:text-black">

  <!-- TOP DECK: Status Bar & Header -->
  <header class="border-b border-cyan-900/40 bg-cyber-black/90 px-6 py-3 flex flex-wrap items-center justify-between gap-4 z-20 shadow-[0_4px_20px_rgba(6,182,212,0.05)]">
    <div class="flex items-center gap-3">
      <!-- Pulsing Indicator -->
      <div class="relative flex h-3 w-3">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
      </div>
      <div>
        <h1 class="hud-title text-xl font-black text-cyan-400 tracking-wider flex items-center gap-2">
          OMNIVISION <span class="text-xs bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded">v4.8 ACTIVE</span>
        </h1>
        <p class="text-[10px] text-cyan-600 font-bold uppercase tracking-widest mt-0.5">Tactical Intelligence & Spectral Analysis Console</p>
      </div>
    </div>

    <!-- Active telemetry -->
    <div class="flex flex-wrap items-center gap-6 text-xs text-slate-400">
      <div class="bg-slate-900/50 border border-slate-800 px-3 py-1.5 rounded flex items-center gap-2">
        <span class="text-cyan-500">SYSTEM:</span>
        <span id="system-status" class="text-emerald-400 font-bold">ONLINE</span>
      </div>
      <div class="bg-slate-900/50 border border-slate-800 px-3 py-1.5 rounded flex items-center gap-2">
        <span class="text-cyan-500">BANDWIDTH:</span>
        <span id="fps-counter" class="text-cyan-400 font-bold font-mono">0.0 FPS</span>
      </div>
      <div class="bg-slate-900/50 border border-slate-800 px-3 py-1.5 rounded flex items-center gap-2">
        <span class="text-cyan-500">COORDINATES:</span>
        <span id="geo-location" class="text-amber-500 font-mono">STABLE // LAT: --.- LON: --.-</span>
      </div>
      <!-- Audio Switch -->
      <button id="audio-toggle" class="bg-cyan-950/40 hover:bg-cyan-900/60 border border-cyan-800/80 hover:border-cyan-500 text-cyan-400 px-3 py-1.5 rounded flex items-center gap-2 transition-all duration-200">
        <svg id="audio-icon" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M12 18.75V5.25L7.5 9H4.5v6h3L12 18.75z" />
        </svg>
        <span class="font-bold">AUDIO ENGINE</span>
      </button>
    </div>
  </header>

  <!-- MAIN OPERATIONAL WORKSPACE -->
  <main class="flex-1 grid grid-cols-1 xl:grid-cols-4 gap-4 p-4 overflow-hidden h-[calc(100vh-69px)]">

    <!-- LEFT BAR: Controller Controls & Diagnostics -->
    <section class="xl:col-span-1 flex flex-col gap-4 overflow-y-auto pr-1">
      
      <!-- WEBCAM INITIALIZATION & FEED SETTINGS -->
      <div class="bg-slate-950/80 border border-cyan-900/30 rounded-lg p-4 shadow-lg backdrop-blur-md">
        <h2 class="hud-title text-sm font-bold text-cyan-400 border-b border-cyan-900/40 pb-2 mb-3 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
          SENSOR INTERFACE
        </h2>

        <!-- Camera Controls -->
        <div class="flex flex-col gap-3">
          <div>
            <label class="text-[10px] text-slate-400 font-bold block mb-1">SELECT CAPTURE SOURCE</label>
            <select id="camera-select" class="w-full bg-slate-900 text-cyan-300 border border-cyan-800/60 rounded px-2.5 py-1.5 text-xs font-mono focus:outline-none focus:border-cyan-400">
              <option value="">LOADING FEED DEVICES...</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <button id="btn-start-camera" class="bg-cyan-600 hover:bg-cyan-500 text-black font-bold py-2 px-3 rounded text-xs tracking-wider transition-all duration-200 shadow-md shadow-cyan-900/30">
              ACTIVATE FEED
            </button>
            <button id="btn-snapshot" class="bg-slate-800 hover:bg-slate-700 text-cyan-400 font-bold py-2 px-3 rounded text-xs border border-cyan-800/40 transition-all">
              SNAP FRAME
            </button>
          </div>
          <div id="camera-error-message" class="hidden text-xs text-red-400 bg-red-950/40 border border-red-900/60 rounded p-2.5 mt-1 font-sans"></div>
        </div>
      </div>

      <!-- HARDWARE TUNERS -->
      <div class="bg-slate-950/80 border border-cyan-900/30 rounded-lg p-4 shadow-lg backdrop-blur-md">
        <h2 class="hud-title text-sm font-bold text-cyan-400 border-b border-cyan-900/40 pb-2 mb-3 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
          SENSOR SPECTRUM TUNER
        </h2>

        <div class="space-y-4">
          <!-- GAIN/BRIGHTNESS -->
          <div>
            <div class="flex justify-between text-[10px] text-slate-400 font-bold mb-1">
              <span>SPECTRAL GAIN</span>
              <span id="val-gain" class="text-cyan-400 font-mono">1.0x</span>
            </div>
            <input type="range" id="slider-gain" min="0.5" max="3" step="0.1" value="1.0" class="w-full accent-cyan-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer">
          </div>

          <!-- STATIC NOISE -->
          <div>
            <div class="flex justify-between text-[10px] text-slate-400 font-bold mb-1">
              <span>ATMOSPHERIC GRAIN</span>
              <span id="val-noise" class="text-cyan-400 font-mono">15%</span>
            </div>
            <input type="range" id="slider-noise" min="0" max="100" step="1" value="15" class="w-full accent-cyan-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer">
          </div>

          <!-- SCANLINE DENSITY -->
          <div>
            <div class="flex justify-between text-[10px] text-slate-400 font-bold mb-1">
              <span>CRT MATRIX SCANLINES</span>
              <span id="val-scanlines" class="text-cyan-400 font-mono">50%</span>
            </div>
            <input type="range" id="slider-scanlines" min="0" max="100" step="5" value="50" class="w-full accent-cyan-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer">
          </div>

          <!-- CHROMATIC ABERRATION -->
          <div>
            <div class="flex justify-between text-[10px] text-slate-400 font-bold mb-1">
              <span>CHROMATIC SHIFT (Fringe)</span>
              <span id="val-chromatic" class="text-cyan-400 font-mono">2px</span>
            </div>
            <input type="range" id="slider-chromatic" min="0" max="15" step="1" value="2" class="w-full accent-cyan-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer">
          </div>

          <!-- ZOOM -->
          <div>
            <div class="flex justify-between text-[10px] text-slate-400 font-bold mb-1">
              <span>DIGITAL PARALLAX ZOOM</span>
              <span id="val-zoom" class="text-cyan-400 font-mono">1.00x</span>
            </div>
            <input type="range" id="slider-zoom" min="1" max="4" step="0.05" value="1.00" class="w-full accent-cyan-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer">
          </div>
        </div>

        <button id="btn-reset-sliders" class="w-full mt-4 bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-800 hover:border-slate-700 py-1.5 px-3 rounded text-[10px] font-bold uppercase tracking-wider transition-all duration-200">
          RECALIBRATE RECEPTORS
        </button>
      </div>

      <!-- ACTIVE TELEMETRY LOGS -->
      <div class="bg-slate-950/80 border border-cyan-900/30 rounded-lg p-4 shadow-lg flex-1 min-h-[160px] flex flex-col backdrop-blur-md">
        <h2 class="hud-title text-sm font-bold text-cyan-400 border-b border-cyan-900/40 pb-2 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-amber-500 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          SYSTEM TELEMETRY
        </h2>
        <div id="telemetry-logs" class="flex-1 overflow-y-auto text-[11px] space-y-1.5 font-mono text-cyan-500/85">
          <div>&gt; DECK INITIALIZED... STATUS OK.</div>
          <div>&gt; SPECTRUM SENSORS STANDBY...</div>
          <div>&gt; PRESS "ACTIVATE FEED" TO STREAM INTELLIGENCE.</div>
        </div>
      </div>

    </section>

    <!-- CENTER & RIGHT: Viewport & Spectral Selector -->
    <section class="xl:col-span-3 flex flex-col gap-4">

      <!-- MASTER VIEWPORT CANVAS -->
      <div class="relative flex-1 bg-slate-950 border-2 border-cyan-900/60 rounded-xl overflow-hidden shadow-[0_0_30px_rgba(6,182,212,0.15)] flex flex-col justify-between group">
        
        <!-- Live indicators on Canvas Overlay -->
        <div class="absolute top-4 left-4 z-20 flex flex-col gap-1 pointer-events-none">
          <div class="bg-black/80 border border-cyan-500/50 backdrop-blur px-2 py-1 rounded text-[10px] font-bold text-cyan-400 tracking-wider flex items-center gap-2">
            <span class="h-1.5 w-1.5 bg-cyan-400 rounded-full animate-ping"></span>
            MODE: <span id="current-mode-label" class="text-white">NORMAL SPECTRUM</span>
          </div>
          <div class="bg-black/70 border border-slate-800 backdrop-blur px-2 py-0.5 rounded text-[9px] text-slate-400 font-mono tracking-wide mt-1">
            RESOLUTION: <span id="canvas-dim-label">-- x --</span> | FILTER_ID: <span id="current-mode-id" class="text-amber-500">M_00</span>
          </div>
        </div>

        <div class="absolute top-4 right-4 z-20 flex flex-col items-end gap-1 pointer-events-none">
          <div class="bg-black/80 border border-red-500/50 backdrop-blur px-2 py-1 rounded text-[10px] font-bold text-red-400 tracking-wider flex items-center gap-2">
            <span class="h-1.5 w-1.5 bg-red-500 rounded-full"></span>
            FEED REC <span id="system-timestamp" class="text-white font-mono ml-2">--:--:--</span>
          </div>
          <div id="target-coordinates" class="bg-black/70 border border-slate-800 backdrop-blur px-2 py-0.5 rounded text-[9px] text-cyan-400/90 font-mono tracking-wide mt-1">
            TARGET RETICLE: DISENGAGED
          </div>
        </div>

        <!-- Diagnostic Warning Overlay (e.g. Sonar/Radiation alerts) -->
        <div id="hazard-banner" class="absolute inset-x-0 top-1/2 -translate-y-1/2 z-20 bg-red-950/90 border-y border-red-500/80 p-3 text-center pointer-events-none opacity-0 transition-opacity duration-300">
          <div class="hud-title text-red-500 font-black text-sm tracking-widest animate-pulse mb-1">☢ HAZARD WARNING: MAXIMUM SPECTRAL CONTAMINATION ☢</div>
          <div class="text-[10px] text-slate-300 uppercase tracking-widest">PROXIMITY RADIATION THRESHOLD BREACHED • EVACUATE IMMEDIATELY</div>
        </div>

        <!-- WEBCAM INVISIBLE TAG AND MASTER CANVAS -->
        <div class="relative flex-1 w-full h-full flex items-center justify-center overflow-hidden">
          <video id="video-feed" autoplay playsinline muted class="hidden"></video>
          <!-- The visual output display canvas -->
          <canvas id="view-canvas" class="w-full h-full object-contain cursor-crosshair scanlines crt-glow"></canvas>
          
          <!-- Instructions overlay when feed is inactive -->
          <div id="feed-placeholder" class="absolute inset-0 flex flex-col items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 z-10 transition-opacity duration-300 p-6 text-center">
            <div class="h-16 w-16 rounded-full bg-cyan-950 border border-cyan-500/30 flex items-center justify-center mb-4 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.2)] animate-pulse">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            </div>
            <h3 class="hud-title text-cyan-400 font-bold text-lg tracking-wider mb-2">SPECTRUM SYSTEM INACTIVE</h3>
            <p class="text-xs text-slate-400 max-w-md leading-relaxed mb-6">
              Connect your physical camera array and authorize browser access. Once calibrated, select from 22 futuristic visualization frequencies.
            </p>
            <button id="btn-trigger-active" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black py-2.5 px-6 rounded text-xs uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)]">
              INITIALIZE SCANNER FEED
            </button>
          </div>
        </div>

        <!-- GRID DECK: 22 Spectral Channels Selector (Responsive) -->
        <div class="border-t border-cyan-900/40 bg-cyber-black/95 p-3 flex flex-col gap-2 z-20">
          <div class="flex justify-between items-center px-1">
            <span class="text-[10px] text-cyan-500 font-black tracking-widest uppercase">SPECTRUM CONTROL PANEL</span>
            <span class="text-[9px] text-slate-500 font-bold tracking-widest uppercase">CLICK CHANNEL TO SWITCH MODALITY</span>
          </div>

          <!-- Channel Selection Grid -->
          <div id="mode-grid" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-11 gap-1.5 max-h-[140px] overflow-y-auto pr-1">
            <!-- Programmatically injected modes -->
          </div>
        </div>

      </div>

    </section>

  </main>

  <!-- FOOTER STATS -->
  <footer class="border-t border-cyan-950/80 bg-slate-950/90 px-6 py-2 flex flex-col sm:flex-row items-center justify-between text-[10px] text-slate-500 gap-2 z-20">
    <div>SYSTEM INTEL: HARDWARE RENDER ACCELERATED • NO EXTERNALLY TRANSMITTED FEED</div>
    <div class="flex items-center gap-4">
      <span>AI CORRELATOR: <span class="text-emerald-500">ACTIVE</span></span>
      <span>TARGET TRACKING DECK: <span class="text-cyan-400">OPERATIONAL</span></span>
      <span class="font-bold text-cyan-800">DESIGN: SECURE INDUSTRIAL MIL-SPEC</span>
    </div>
  </footer>

  <!-- JAVASCRIPT: MASTER RECEPTOR INTERFACE -->
  <script>
    // --- SPECTRAL MODE DATA ARCHITECTURE ---
    // Defined 22 vision modes
    const VISION_MODES = [
      { id: 'M01', name: 'NORMAL SPECTRUM', tag: 'RAW', desc: 'Raw uncalibrated camera input with status tracking HUD.', color: 'border-slate-800 text-slate-400', activeColor: 'bg-slate-900 text-white border-cyan-500' },
      { id: 'M02', name: 'NIGHT VISION G3', tag: 'NVG', desc: 'Gen-3 tactical green phosphor amplification with scanlines and atmospheric grain.', color: 'border-green-950 text-green-500', activeColor: 'bg-green-950/50 text-green-400 border-green-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]' },
      { id: 'M03', name: 'THERMAL SPECTRUM', tag: 'HEAT', desc: 'Standard thermal heatmap coloring, hot objects show red/white, cold blue/violet.', color: 'border-red-950 text-red-500', activeColor: 'bg-red-950/50 text-red-400 border-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]' },
      { id: 'M04', name: 'X-RAY (REVERSE)', tag: 'X-RAY', desc: 'Simulated high-contrast inverse skeletal structure imaging.', color: 'border-cyan-950 text-cyan-500', activeColor: 'bg-cyan-950/50 text-cyan-400 border-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.3)]' },
      { id: 'M05', name: 'INFRARED RADAR', tag: 'IR', desc: 'Long-wave IR duotone. Extreme light signatures mapped to high contrast white-burgundy.', color: 'border-rose-950 text-rose-500', activeColor: 'bg-rose-950/50 text-rose-400 border-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.3)]' },
      { id: 'M06', name: 'ULTRAVIOLET SPECTRA', tag: 'UV', desc: 'Deep violet/ultraviolet analysis focusing on simulated fluorescent emissions.', color: 'border-purple-950 text-purple-500', activeColor: 'bg-purple-950/50 text-purple-400 border-purple-500 shadow-[0_0_10px_rgba(139,92,246,0.3)]' },
      { id: 'M07', name: 'ACTIVE SONAR SCAN', tag: 'SONAR', desc: 'Acoustic contour tracking mapping audio sweeps and depth gradients.', color: 'border-sky-950 text-sky-400', activeColor: 'bg-sky-950/50 text-sky-400 border-sky-400 shadow-[0_0_10px_rgba(56,189,248,0.3)]' },
      { id: 'M08', name: 'NEON EDGE TRACER', tag: 'EDGES', desc: 'Real-time high pass edge filtration. Excellent for structural analysis.', color: 'border-teal-950 text-teal-400', activeColor: 'bg-teal-950/50 text-teal-400 border-teal-400 shadow-[0_0_10px_rgba(20,184,166,0.3)]' },
      { id: 'M09', name: 'LIDAR CLOUD', tag: 'LIDAR', desc: 'Pulsed laser scanner simulator creating distance particle points.', color: 'border-yellow-950 text-yellow-500', activeColor: 'bg-yellow-950/50 text-yellow-400 border-yellow-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]' },
      { id: 'M10', name: 'MATRIX STREAM', tag: 'MATRX', desc: 'Cascading code digital rain reacting directly to ambient light changes.', color: 'border-emerald-950 text-emerald-500', activeColor: 'bg-emerald-950/50 text-emerald-400 border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]' },
      { id: 'M11', name: 'PREDATOR TARGETING', tag: 'PRDTR', desc: 'Low-res multispectral thermal mapping utilizing classic pixel array scaling.', color: 'border-amber-950 text-amber-500', activeColor: 'bg-amber-950/50 text-amber-400 border-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]' },
      { id: 'M12', name: 'CYBERPUNK HUD AR', tag: 'HUD', desc: 'Tactical targeting grid overlay tracking real-time frame telemetry and wind indices.', color: 'border-cyan-950 text-cyan-400', activeColor: 'bg-cyan-950/50 text-cyan-400 border-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.3)]' },
      { id: 'M13', name: 'HAZMAT TOXICITY', tag: 'HAZ', desc: 'Environmental warning duotone displaying pulsing alerts and contamination vectors.', color: 'border-orange-950 text-orange-500', activeColor: 'bg-orange-950/50 text-orange-400 border-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)]' },
      { id: 'M14', name: 'SOLARIZED SURREAL', tag: 'SOLAR', desc: 'Photovoltaic inversion, turning highlights into deep color spectrum boundaries.', color: 'border-fuchsia-950 text-fuchsia-500', activeColor: 'bg-fuchsia-950/50 text-fuchsia-400 border-fuchsia-500 shadow-[0_0_10px_rgba(217,70,239,0.3)]' },
      { id: 'M15', name: 'EMP / GLITCH FEED', tag: 'EMP', desc: 'Severe electromagnetic pulse interference causing structural screen horizontal errors.', color: 'border-red-950 text-red-400', activeColor: 'bg-red-950/50 text-red-400 border-red-400 shadow-[0_0_10px_rgba(239,68,68,0.3)]' },
      { id: 'M16', name: 'BLUEPRINT MODEL', tag: 'BLUE', desc: 'Converts target field into classic cyan engineering blueprints and grid maps.', color: 'border-blue-950 text-blue-400', activeColor: 'bg-blue-950/50 text-blue-400 border-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.3)]' },
      { id: 'M17', name: 'QUANTUM PARTICLES', tag: 'QUANT', desc: 'Dynamic energetic particle fields emerging from high-movement contours.', color: 'border-pink-950 text-pink-500', activeColor: 'bg-pink-950/50 text-pink-400 border-pink-500 shadow-[0_0_10px_rgba(236,72,153,0.3)]' },
      { id: 'M18', name: 'RETRO CRT AMBER', tag: 'CRT', desc: 'Warm amber monochrome terminal rendering replicating old security arrays.', color: 'border-yellow-950 text-amber-500', activeColor: 'bg-yellow-950/50 text-amber-500 border-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]' },
      { id: 'M19', name: 'SECURITY ANALYST', tag: 'CCTV', desc: 'Low-rate compression display with digital motion vectors and analytical grids.', color: 'border-slate-800 text-slate-400', activeColor: 'bg-slate-900 text-white border-slate-400' },
      { id: 'M20', name: 'CHROMATIC SPECTRUM', tag: 'CHRM', desc: 'Heavy visual dispersion mapping RGB channels outwards on a parallax plane.', color: 'border-violet-950 text-violet-400', activeColor: 'bg-violet-950/50 text-violet-400 border-violet-400 shadow-[0_0_10px_rgba(139,92,246,0.3)]' },
      { id: 'M21', name: 'CHROMA SYNTHWAVE', tag: 'VAPOR', desc: 'Neon pink and turquoise solar mapping mimicking retro computer horizons.', color: 'border-fuchsia-950 text-cyan-400', activeColor: 'bg-fuchsia-950/50 text-cyan-300 border-fuchsia-500 shadow-[0_0_10px_rgba(217,70,239,0.3)]' },
      { id: 'M22', name: 'DEEP COLD SCAN', tag: 'COLD', desc: 'Deep-ocean zero spectrum. Eliminates reds entirely to isolate thermal vents.', color: 'border-indigo-950 text-indigo-400', activeColor: 'bg-indigo-950/50 text-indigo-300 border-indigo-400 shadow-[0_0_10px_rgba(99,102,241,0.3)]' }
    ];

    // --- APPLICATION STATE ---
    let stream = null;
    let animationFrameId = null;
    let selectedMode = 'M01';
    let targetLock = null; // Coordinates of screen click tracking
    let targetActive = false;
    let audioCtx = null;
    let telemetryHistory = [];
    let fpsHistory = [];
    let lastTime = performance.now();
    let frameCount = 0;
    let currentFps = 0.0;
    
    // Core parameters (tied to UI sliders)
    let config = {
      gain: 1.0,
      noise: 15,
      scanlines: 50,
      chromatic: 2,
      zoom: 1.0
    };

    // Matrix Rain State Cache
    let matrixColumns = [];
    const matrixChars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$#@&%+-*";

    // Quantum Particles cache
    let particles = [];
    const MAX_PARTICLES = 120;

    // Sonar Radar sweeps
    let sonarSweepAngle = 0;
    let sonarPulseRadius = 0;

    // --- DOM ELEMENT CACHE ---
    const video = document.getElementById('video-feed');
    const canvas = document.getElementById('view-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    const cameraSelect = document.getElementById('camera-select');
    const btnStartCamera = document.getElementById('btn-start-camera');
    const btnSnapshot = document.getElementById('btn-snapshot');
    const cameraErrorMessage = document.getElementById('camera-error-message');
    const feedPlaceholder = document.getElementById('feed-placeholder');
    const btnTriggerActive = document.getElementById('btn-trigger-active');
    
    const sliderGain = document.getElementById('slider-gain');
    const sliderNoise = document.getElementById('slider-noise');
    const sliderScanlines = document.getElementById('slider-scanlines');
    const sliderChromatic = document.getElementById('slider-chromatic');
    const sliderZoom = document.getElementById('slider-zoom');
    
    const valGain = document.getElementById('val-gain');
    const valNoise = document.getElementById('val-noise');
    const valScanlines = document.getElementById('val-scanlines');
    const valChromatic = document.getElementById('val-chromatic');
    const valZoom = document.getElementById('val-zoom');
    const btnResetSliders = document.getElementById('btn-reset-sliders');
    
    const telemetryLogs = document.getElementById('telemetry-logs');
    const currentModeLabel = document.getElementById('current-mode-label');
    const currentModeId = document.getElementById('current-mode-id');
    const canvasDimLabel = document.getElementById('canvas-dim-label');
    const fpsCounter = document.getElementById('fps-counter');
    const geoLocation = document.getElementById('geo-location');
    const systemTimestamp = document.getElementById('system-timestamp');
    const targetCoordinates = document.getElementById('target-coordinates');
    const hazardBanner = document.getElementById('hazard-banner');
    
    const audioToggle = document.getElementById('audio-toggle');
    const audioIcon = document.getElementById('audio-icon');

    // --- SOUND ENGINE (Web Audio API Synthesizer) ---
    let soundEnabled = false;
    let centralHumNode = null;

    function initAudio() {
      if (audioCtx) return;
      try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContextClass();
        
        // Setup continuous atmospheric hum
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(55, audioCtx.currentTime); // Low 55Hz military hum
        
        // Low pass filter to make it rumbling
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(120, audioCtx.currentTime);
        
        gainNode.gain.setValueAtTime(0.015, audioCtx.currentTime); // very subtle
        
        osc.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start();
        centralHumNode = { osc, gain: gainNode };
        
        addTelemetryLog("AUDIO SYNTH ENGINE INITIALIZED [55Hz RUMBLE]");
      } catch (e) {
        console.warn("Audio Context Failed: ", e);
      }
    }

    function toggleAudio() {
      if (!audioCtx) {
        initAudio();
        soundEnabled = true;
        audioToggle.classList.add('bg-cyan-500', 'text-black');
        audioToggle.classList.remove('bg-cyan-950/40', 'text-cyan-400');
        playSynthBeep(880, 0.1, 0.05);
      } else {
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
          soundEnabled = true;
          audioToggle.classList.add('bg-cyan-500', 'text-black');
          audioToggle.classList.remove('bg-cyan-950/40', 'text-cyan-400');
          playSynthBeep(880, 0.1, 0.05);
        } else if (audioCtx.state === 'running' && soundEnabled) {
          audioCtx.suspend();
          soundEnabled = false;
          audioToggle.classList.remove('bg-cyan-500', 'text-black');
          audioToggle.classList.add('bg-cyan-950/40', 'text-cyan-400');
        } else {
          audioCtx.resume();
          soundEnabled = true;
          audioToggle.classList.add('bg-cyan-500', 'text-black');
          audioToggle.classList.remove('bg-cyan-950/40', 'text-cyan-400');
          playSynthBeep(880, 0.1, 0.05);
        }
      }
    }

    function playSynthBeep(freq, duration, volume = 0.1, type = 'sine') {
      if (!audioCtx || !soundEnabled) return;
      try {
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        
        gainNode.gain.setValueAtTime(volume, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (err) {}
    }

    // Special sound pattern for sonar ping
    function playSonarPing() {
      if (!audioCtx || !soundEnabled) return;
      playSynthBeep(1200, 1.2, 0.08, 'sine');
      setTimeout(() => playSynthBeep(600, 0.6, 0.03, 'sine'), 100);
    }

    // Sound effect for glitches
    function playGlitchCrack() {
      if (!audioCtx || !soundEnabled) return;
      playSynthBeep(80, 0.05, 0.15, 'sawtooth');
      setTimeout(() => playSynthBeep(450, 0.02, 0.08, 'square'), 30);
    }

    // Geiger counter clicks (hazmat mode)
    function playGeigerClick() {
      if (!audioCtx || !soundEnabled) return;
      // Single random dry tick
      playSynthBeep(1800, 0.005, 0.12, 'triangle');
    }

    // --- ENUMERATED MODES INTERFACE GENERATOR ---
    function generateModeGrid() {
      const grid = document.getElementById('mode-grid');
      grid.innerHTML = '';
      
      VISION_MODES.forEach((mode, index) => {
        const btn = document.createElement('button');
        btn.id = `btn-mode-${mode.id}`;
        btn.className = `border ${mode.color} px-2 py-2 rounded text-left transition-all duration-150 relative group flex flex-col justify-between h-[54px] hover:border-cyan-400/80 bg-slate-900/40 hover:bg-slate-900/80`;
        btn.onclick = () => selectVisionMode(mode.id);
        
        btn.innerHTML = `
          <div class="flex items-center justify-between gap-1 w-full">
            <span class="text-[9px] font-black tracking-wider text-slate-500 group-hover:text-cyan-400 font-mono">${mode.id}</span>
            <span class="text-[8px] bg-slate-950 px-1 py-0.2 rounded font-bold text-slate-400 border border-slate-800/40">${mode.tag}</span>
          </div>
          <div class="text-[10px] font-bold truncate tracking-wide text-slate-300 w-full font-sans group-hover:text-white">${mode.name}</div>
        `;
        grid.appendChild(btn);
      });
    }

    function selectVisionMode(id) {
      const prevModeId = selectedMode;
      selectedMode = id;
      const targetMode = VISION_MODES.find(m => m.id === id);
      
      // Update Grid Buttons highlights
      VISION_MODES.forEach(m => {
        const element = document.getElementById(`btn-mode-${m.id}`);
        if (!element) return;
        // Reset classes
        element.className = `border ${m.color} px-2 py-2 rounded text-left transition-all duration-150 relative group flex flex-col justify-between h-[54px] hover:border-cyan-400/80 bg-slate-900/40 hover:bg-slate-900/80`;
        
        if (m.id === id) {
          element.className = `border px-2 py-2 rounded text-left transition-all duration-150 relative group flex flex-col justify-between h-[54px] ${m.activeColor}`;
        }
      });

      // Update HUD Labels
      currentModeLabel.textContent = targetMode.name;
      currentModeId.textContent = targetMode.id;
      
      // Audio trigger
      if (prevModeId !== id) {
        if (id === 'M07') {
          playSonarPing();
        } else if (id === 'M15') {
          playGlitchCrack();
        } else {
          playSynthBeep(440 + (parseInt(id.slice(1)) * 30), 0.15, 0.05, 'triangle');
        }
        addTelemetryLog(`CH_SWITCHED [MODE: ${targetMode.id} - ${targetMode.name}]`);
      }

      // Show hazard warning on Hazmat mode
      if (id === 'M13') {
        hazardBanner.classList.remove('opacity-0');
      } else {
        hazardBanner.classList.add('opacity-0');
      }
    }

    // --- TELEMETRY LOGGER ---
    function addTelemetryLog(message) {
      const time = new Date().toLocaleTimeString();
      telemetryHistory.push(`[${time}] ${message}`);
      if (telemetryHistory.length > 40) telemetryHistory.shift();
      
      // Re-render logs
      telemetryLogs.innerHTML = telemetryHistory.map(log => {
        if (log.includes('CH_SWITCHED') || log.includes('CALIBRATE')) {
          return `<div class="text-cyan-400">&gt; ${log}</div>`;
        }
        if (log.includes('WARNING') || log.includes('FAIL') || log.includes('ERR')) {
          return `<div class="text-red-400 font-bold">&gt; ${log}</div>`;
        }
        return `<div class="text-slate-400/90">&gt; ${log}</div>`;
      }).join('');
      
      // Auto Scroll
      telemetryLogs.scrollTop = telemetryLogs.scrollHeight;
    }

    // --- WEBCAM STREAM & DEVICE POPULATING ---
    async function populateCameras() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(d => d.kind === 'videoinput');
        
        cameraSelect.innerHTML = '';
        if (videoDevices.length === 0) {
          cameraSelect.innerHTML = '<option value="">NO DETECTED CAMERAS</option>';
          return;
        }

        videoDevices.forEach((device, index) => {
          const option = document.createElement('option');
          option.value = device.deviceId;
          option.textContent = device.label || `SPECTRAL SCANNER ${index + 1}`;
          cameraSelect.appendChild(option);
        });
        
        addTelemetryLog(`HARDWARE DISCOVERED: ${videoDevices.length} SENSOR STREAM(S)`);
      } catch (err) {
        console.error("Error enumerating devices: ", err);
        addTelemetryLog("HARDWARE QUERIES FAILED.");
      }
    }

    async function startCamera() {
      stopCamera();
      
      const constraints = {
        video: {
          deviceId: cameraSelect.value ? { exact: cameraSelect.value } : undefined,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      addTelemetryLog("CALIBRATING CAMERA SPECTRUM ARRAY...");
      initAudio(); // Initialize audio engine on click interaction

      try {
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        
        // Wait for metadata to configure dimensions
        video.onloadedmetadata = () => {
          canvas.width = video.videoWidth || 640;
          canvas.height = video.videoHeight || 480;
          canvasDimLabel.textContent = `${canvas.width} x ${canvas.height}`;
          
          // Hide placeholder
          feedPlaceholder.classList.add('opacity-0', 'pointer-events-none');
          
          // Re-initialize dynamic rendering matrices
          initMatrixColumns(canvas.width);
          
          addTelemetryLog(`STREAM MATCH SUCCESS: ${canvas.width}X${canvas.height}`);
          
          // Trigger rendering loop
          if (animationFrameId) cancelAnimationFrame(animationFrameId);
          animationFrameId = requestAnimationFrame(renderLoop);
        };
        
        document.getElementById('system-status').textContent = "ACTIVE";
        document.getElementById('system-status').className = "text-emerald-400 font-bold";
        btnStartCamera.textContent = "RESET CHANNELS";
        btnStartCamera.classList.add('bg-emerald-600', 'hover:bg-emerald-500');
        
      } catch (err) {
        console.error("Camera access error:", err);
        cameraErrorMessage.textContent = `CRITICAL CONFIG ERROR: Ensure camera permission is granted. [Detail: ${err.message}]`;
        cameraErrorMessage.classList.remove('hidden');
        addTelemetryLog(`ERR: CAPTURE FAILURE [${err.name}]`);
      }
    }

    function stopCamera() {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
      document.getElementById('system-status').textContent = "STANDBY";
      document.getElementById('system-status').className = "text-amber-500 font-bold";
    }

    // --- RECEPTOR TUNING ADJUSTMENTS ---
    function updateConfig() {
      config.gain = parseFloat(sliderGain.value);
      config.noise = parseInt(sliderNoise.value);
      config.scanlines = parseInt(sliderScanlines.value);
      config.chromatic = parseInt(sliderChromatic.value);
      config.zoom = parseFloat(sliderZoom.value);
      
      valGain.textContent = `${config.gain.toFixed(1)}x`;
      valNoise.textContent = `${config.noise}%`;
      valScanlines.textContent = `${config.scanlines}%`;
      valChromatic.textContent = `${config.chromatic}px`;
      valZoom.textContent = `${config.zoom.toFixed(2)}x`;
    }

    // --- GRACEFUL DATA READING INTERFACES ---
    function safeGetImageData(targetCtx, x, y, width, height) {
      if (width <= 0 || height <= 0) return null;
      try {
        return targetCtx.getImageData(x, y, width, height);
      } catch (e) {
        return null;
      }
    }

    // --- CANVAS PROCESSING & FILTER ALGORITHMS ---

    // 1. NIGHT VISION
    function filterNightVision(data, w, h) {
      if (!data) return;
      const gain = config.gain * 1.5;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        // Green amplification
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b);
        const amplifiedGreen = Math.min(255, luminance * gain);
        
        data[i] = Math.min(255, amplifiedGreen * 0.15); // tiny red
        data[i+1] = amplifiedGreen;                      // full green
        data[i+2] = Math.min(255, amplifiedGreen * 0.25); // low blue
      }
    }

    // 2. THERMAL SPECTRUM (Cyan-Green-Yellow-Red-White)
    function filterThermal(data, w, h) {
      if (!data) return;
      const gain = config.gain;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        let y = (0.299 * r + 0.587 * g + 0.114 * b) * gain;
        y = Math.max(0, Math.min(255, y));
        
        // Map brightness value to custom multi-spectral thermal gradient
        if (y < 42) {
          // Dark Blue to Purple
          data[i] = y * 1.2;
          data[i+1] = 0;
          data[i+2] = 50 + y * 4.5;
        } else if (y < 110) {
          // Cyan to dark green
          data[i] = 0;
          data[i+1] = (y - 42) * 3;
          data[i+2] = 230 - (y - 42) * 2.5;
        } else if (y < 180) {
          // Yellow-Orange
          data[i] = (y - 110) * 3.6;
          data[i+1] = 200 + (y - 180) * 0.5;
          data[i+2] = 0;
        } else {
          // Bright red to intense white
          data[i] = 255;
          data[i+1] = (y - 180) * 3.4;
          data[i+2] = (y - 180) * 3.4;
        }
      }
    }

    // 3. X-RAY (Negative mono high contrast)
    function filterXRay(data, w, h) {
      if (!data) return;
      const gain = config.gain * 1.2;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b);
        // Inverse grayscale
        let inv = 255 - mono;
        
        // High contrast mapping
        inv = (inv - 128) * gain + 128;
        const finalVal = Math.max(0, Math.min(255, inv));
        
        // Bone hue (bluish tint)
        data[i] = Math.min(255, finalVal * 0.85);
        data[i+1] = Math.min(255, finalVal * 0.95);
        data[i+2] = Math.min(255, finalVal * 1.15);
      }
    }

    // 4. INFRARED (Burgundy to white spectral)
    function filterInfrared(data, w, h) {
      if (!data) return;
      const gain = config.gain;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b) * gain;
        
        if (mono < 80) {
          // Deep burgundy / black
          data[i] = Math.min(255, mono * 0.4);
          data[i+1] = 0;
          data[i+2] = Math.min(255, mono * 0.1);
        } else if (mono < 190) {
          // Infrared red bloom
          data[i] = Math.min(255, 30 + (mono - 80) * 1.8);
          data[i+1] = Math.min(255, (mono - 80) * 0.3);
          data[i+2] = Math.min(255, (mono - 80) * 0.1);
        } else {
          // Intense thermal radiation (pure white highlight)
          data[i] = 255;
          data[i+1] = 255;
          data[i+2] = 180 + (mono - 190) * 1.15;
        }
      }
    }

    // 5. ULTRAVIOLET (Deep Purples & Fluorescent Yellows)
    function filterUltraviolet(data, w, h) {
      if (!data) return;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b);
        
        if (mono > 180) {
          // Fluorescent neon green/yellow glow on high-energy highlights
          data[i] = 180 + (mono - 180) * 1.5;
          data[i+1] = 255;
          data[i+2] = 0;
        } else {
          // Deep UV spectrum colors
          data[i] = Math.max(0, mono * 0.6);
          data[i+1] = Math.max(0, mono * 0.1);
          data[i+2] = Math.min(255, 60 + mono * 1.6);
        }
      }
    }

    // 6. NEON EDGE TRACER
    function filterNeonEdges(data, w, h) {
      if (!data || data.length === 0) return;
      // Sobel operator convolution on luminance mapping
      const buffer = new Uint8ClampedArray(data.length);
      for (let i = 0; i < data.length; i += 4) {
        buffer[i] = (0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2]);
      }
      
      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          const idx = (y * w + x) * 4;
          
          // Sobel Kernels
          // Horizontal
          const hX = (
            -1 * buffer[((y-1)*w + (x-1))*4] + 1 * buffer[((y-1)*w + (x+1))*4] +
            -2 * buffer[(y*w + (x-1))*4]     + 2 * buffer[(y*w + (x+1))*4] +
            -1 * buffer[((y+1)*w + (x-1))*4] + 1 * buffer[((y+1)*w + (x+1))*4]
          );
          
          // Vertical
          const hY = (
            -1 * buffer[((y-1)*w + (x-1))*4] - 2 * buffer[((y-1)*w + x)*4] - 1 * buffer[((y-1)*w + (x+1))*4] +
            1 * buffer[((y+1)*w + (x-1))*4] + 2 * buffer[((y+1)*w + x)*4] + 1 * buffer[((y+1)*w + (x+1))*4]
          );
          
          const val = Math.sqrt(hX*hX + hY*hY) * config.gain;
          
          // Put cyan-neon edge glowing lines on a black canvas
          data[idx] = Math.min(255, val * 0.1);    // minimal red
          data[idx+1] = Math.min(255, val * 1.1); // high emerald/cyan green
          data[idx+2] = Math.min(255, val * 1.3); // pure neon blue highlight
        }
      }
    }

    // 7. MATRIX CODE RAIN INITIALIZATION & TICK
    function initMatrixColumns(w) {
      const fontSize = 14;
      const columns = Math.floor((w || 640) / fontSize);
      matrixColumns = [];
      for (let i = 0; i < columns; i++) {
        matrixColumns.push({
          x: i * fontSize,
          y: Math.random() * -100,
          speed: 2 + Math.random() * 5
        });
      }
    }

    function renderMatrixRain(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      // Create offscreen mapping for brightness
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 160;
      tempCanvas.height = 120;
      const tempCtx = tempCanvas.getContext('2d');
      try {
        tempCtx.drawImage(vidElement, 0, 0, 160, 120);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(tempCtx, 0, 0, 160, 120);
      if (!imgData) {
        ctx.fillStyle = 'rgba(5, 7, 12, 0.2)';
        ctx.fillRect(0, 0, w, h);
        return;
      }
      
      const px = imgData.data;

      // Dark background with trail fade
      ctx.fillStyle = 'rgba(5, 7, 12, 0.2)';
      ctx.fillRect(0, 0, w, h);
      
      ctx.fillStyle = '#10b981';
      ctx.font = '14px monospace';

      matrixColumns.forEach(col => {
        // Find corresponding pixel in low-res analysis
        const pxX = Math.floor((col.x / w) * 160);
        const pxY = Math.floor((Math.max(0, col.y) / h) * 120);
        const pIndex = (pxY * 160 + pxX) * 4;
        
        let brightness = 128;
        if (px && pIndex < px.length) {
          brightness = (0.299 * px[pIndex] + 0.587 * px[pIndex+1] + 0.114 * px[pIndex+2]);
        }

        // Draw character
        const char = matrixChars[Math.floor(Math.random() * matrixChars.length)];
        
        // Brighter areas generate glowing white matrix characters
        if (brightness > 180) {
          ctx.fillStyle = '#ffffff';
          ctx.fillText(char, col.x, col.y);
        } else if (brightness > 90) {
          ctx.fillStyle = '#34d399';
          ctx.fillText(char, col.x, col.y);
        } else {
          ctx.fillStyle = '#065f46';
          ctx.fillText(char, col.x, col.y);
        }

        col.y += col.speed;
        if (col.y > h) {
          col.y = Math.random() * -50;
          col.speed = 2 + Math.random() * 5;
        }
      });
    }

    // 8. PREDATOR HEAT VISION (Low resolution thermal scaling)
    function renderPredatorThermal(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      const lowW = 80;
      const lowH = 60;
      
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = lowW;
      tempCanvas.height = lowH;
      const tempCtx = tempCanvas.getContext('2d');
      try {
        tempCtx.drawImage(vidElement, 0, 0, lowW, lowH);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(tempCtx, 0, 0, lowW, lowH);
      if (!imgData) return;
      const d = imgData.data;
      
      // Map low resolution image to thermal profile
      for (let i = 0; i < d.length; i += 4) {
        const y = (0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2]) * config.gain;
        
        // Classic Predator spectral mapping (Blue -> Green -> Yellow -> Extreme Red)
        if (y < 40) {
          d[i] = 0; d[i+1] = 0; d[i+2] = 120 + y*3;
        } else if (y < 120) {
          d[i] = 0; d[i+1] = (y-40)*2.5; d[i+2] = 240 - (y-40)*2;
        } else if (y < 200) {
          d[i] = (y-120)*3; d[i+1] = 200; d[i+2] = 0;
        } else {
          d[i] = 255; d[i+1] = 255 - (y-200)*3; d[i+2] = 0;
        }
      }
      
      tempCtx.putImageData(imgData, 0, 0);
      
      // Draw pixelated scaled frame
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(tempCanvas, 0, 0, w, h);
      ctx.imageSmoothingEnabled = true;
    }

    // 9. HAZMAT / TOXIC ENVIRONMENTAL SCAN
    function filterHazmat(data, w, h) {
      if (!data) return;
      const time = performance.now() * 0.004;
      const pulse = Math.sin(time) * 35;
      
      // Tick geiger clicks relative to ambient brightness logic
      if (Math.random() < 0.15) {
        playGeigerClick();
      }

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b);
        
        // Render in sick green and nuclear hazard amber
        data[i] = Math.min(255, mono * 0.7 + pulse);
        data[i+1] = Math.min(255, mono * 1.1 + pulse);
        data[i+2] = Math.max(0, mono * 0.15);
      }
    }

    // 10. SOLARIZED PHOTOVOLTAIC
    function filterSolarized(data, w, h) {
      if (!data) return;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        // Solarization curves
        data[i] = Math.abs(128 - r) * 2;
        data[i+1] = Math.abs(128 - g) * 2;
        data[i+2] = Math.abs(128 - b) * 2;
      }
    }

    // 11. LIDAR POINT CLOUD SCANNER
    function renderLidarCloud(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      // Render black background first
      ctx.fillStyle = '#05070c';
      ctx.fillRect(0, 0, w, h);
      
      // Analyze current frames by drawing small image array
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 120;
      tempCanvas.height = 90;
      const tempCtx = tempCanvas.getContext('2d');
      try {
        tempCtx.drawImage(vidElement, 0, 0, 120, 90);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(tempCtx, 0, 0, 120, 90);
      if (!imgData) return;
      const d = imgData.data;
      
      const stepX = w / 120;
      const stepY = h / 90;
      
      for (let y = 0; y < 90; y += 2) {
        for (let x = 0; x < 120; x += 2) {
          const idx = (y * 120 + x) * 4;
          const r = d[idx];
          const g = d[idx+1];
          const b = d[idx+2];
          const mono = (0.299 * r + 0.587 * g + 0.114 * b);
          
          if (mono > 40) {
            // Draw points. Color matches altitude/brightness
            ctx.beginPath();
            const radius = (mono / 255) * 3 * config.gain;
            
            // Map altitude color
            if (mono > 180) {
              ctx.fillStyle = '#f59e0b'; // Hot golden core
            } else if (mono > 100) {
              ctx.fillStyle = '#10b981'; // Mid distance emerald
            } else {
              ctx.fillStyle = '#06b6d4'; // Deep cyan points
            }
            
            ctx.arc(x * stepX, y * stepY, radius, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }
    }

    // 12. SOUND-EMITTING SONAR CONTURS
    function renderSonarRadar(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      // Custom green/blue contours on darkness
      ctx.fillStyle = '#05070c';
      ctx.fillRect(0, 0, w, h);
      
      // Perform Edge trace first
      try {
        ctx.drawImage(vidElement, 0, 0, w, h);
      } catch (e) {
        return;
      }
      
      const frame = safeGetImageData(ctx, 0, 0, w, h);
      if (frame && frame.data) {
        filterNeonEdges(frame.data, w, h);
        ctx.putImageData(frame, 0, 0);
      }
      
      // Layer a blue overlay for ocean sonar aesthetics
      ctx.fillStyle = 'rgba(6, 182, 212, 0.12)';
      ctx.fillRect(0, 0, w, h);

      // Radial sonar ping sweep
      sonarPulseRadius += 4;
      if (sonarPulseRadius > Math.max(w, h)) {
        sonarPulseRadius = 0;
        playSonarPing();
      }
      
      ctx.beginPath();
      ctx.arc(w / 2, h / 2, sonarPulseRadius, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(6, 182, 212, 0.5)';
      ctx.lineWidth = 3;
      ctx.stroke();
      
      // Fade-out second ring
      if (sonarPulseRadius > 150) {
        ctx.beginPath();
        ctx.arc(w / 2, h / 2, sonarPulseRadius - 150, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(6, 182, 212, 0.2)';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Sweep radar line
      sonarSweepAngle += 0.02;
      const endX = w / 2 + Math.cos(sonarSweepAngle) * Math.max(w, h);
      const endY = h / 2 + Math.sin(sonarSweepAngle) * Math.max(w, h);
      
      ctx.beginPath();
      ctx.moveTo(w / 2, h / 2);
      ctx.lineTo(endX, endY);
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // 13. HIGH DEGREE GLITCH / EMP DISRUPTION
    function renderEmpGlitch(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      try {
        ctx.drawImage(vidElement, 0, 0, w, h);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(ctx, 0, 0, w, h);
      if (!imgData) return;
      const d = imgData.data;

      // Heavy Chromatic Shift first
      const shift = Math.floor(config.chromatic * 4.5);
      if (shift > 0 && d) {
        const temp = new Uint8ClampedArray(d);
        for (let i = 0; i < d.length; i += 4) {
          // Shift blue and red in opposing directions
          if (i + shift * 4 < d.length) {
            d[i] = temp[i + shift * 4]; // Red channel shifted
          }
          if (i - shift * 4 >= 0) {
            d[i+2] = temp[i - shift * 4]; // Blue channel shifted
          }
        }
      }

      // Write shifted pixels back
      ctx.putImageData(imgData, 0, 0);

      // Randomly grab horizontal strips and slide them horizontally
      if (Math.random() < 0.35) {
        playGlitchCrack();
        const stripsCount = 2 + Math.floor(Math.random() * 5);
        for (let j = 0; j < stripsCount; j++) {
          const startY = Math.floor(Math.random() * h);
          const stripHeight = 5 + Math.floor(Math.random() * 25);
          const shiftX = (Math.random() > 0.5 ? 1 : -1) * (10 + Math.floor(Math.random() * 50));
          
          ctx.drawImage(canvas, 0, startY, w, stripHeight, shiftX, startY, w, stripHeight);
        }
      }

      // Layer black blocks periodically
      if (Math.random() < 0.1) {
        ctx.fillStyle = 'rgba(0,0,0,0.85)';
        ctx.fillRect(0, Math.random() * h, w, 4 + Math.random() * 30);
      }
    }

    // 14. BLUEPRINT / CAD ARCHITECT
    function renderBlueprint(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      // Blueprint blue background
      ctx.fillStyle = '#062863';
      ctx.fillRect(0, 0, w, h);
      
      // Draw Grid Lines
      ctx.strokeStyle = 'rgba(6, 182, 212, 0.15)';
      ctx.lineWidth = 0.5;
      const gridSize = 40;
      for (let x = 0; x < w; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }
      for (let y = 0; y < h; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      // Run Edges and map to White/Bright Cyan
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      
      const offCanvas = document.createElement('canvas');
      offCanvas.width = w;
      offCanvas.height = h;
      const offCtx = offCanvas.getContext('2d');
      try {
        offCtx.drawImage(vidElement, 0, 0, w, h);
      } catch (e) {
        ctx.restore();
        return;
      }
      
      const imgData = safeGetImageData(offCtx, 0, 0, w, h);
      if (!imgData) {
        ctx.restore();
        return;
      }
      const d = imgData.data;
      
      filterNeonEdges(d, w, h);
      
      // Turn neon outlines white/cyan
      for (let i = 0; i < d.length; i += 4) {
        const brightness = d[i+1]; // Green edge power
        d[i] = brightness * 0.8;   // Cyan R
        d[i+1] = brightness * 1.1; // Cyan G
        d[i+2] = brightness * 1.3; // Cyan B
      }
      
      offCtx.putImageData(imgData, 0, 0);
      ctx.drawImage(offCanvas, 0, 0);
      ctx.restore();
    }

    // 15. QUANTUM PARTICLES CONTOUR GENERATOR
    function renderQuantumParticles(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      ctx.fillStyle = 'rgba(5, 7, 12, 0.15)';
      ctx.fillRect(0, 0, w, h);

      // Edge mapping analysis to get particle coordinates
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 160;
      tempCanvas.height = 120;
      const tempCtx = tempCanvas.getContext('2d');
      try {
        tempCtx.drawImage(vidElement, 0, 0, 160, 120);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(tempCtx, 0, 0, 160, 120);
      if (!imgData) return;
      
      filterNeonEdges(imgData.data, 160, 120);
      const d = imgData.data;

      // Spawn particles on bright outlines
      for (let i = 0; i < d.length; i += 16) {
        if (d[i+1] > 100 && particles.length < MAX_PARTICLES) {
          const pixelIdx = i / 4;
          const py = Math.floor(pixelIdx / 160);
          const px = pixelIdx % 160;
          
          if (Math.random() < 0.08) {
            particles.push({
              x: (px / 160) * w,
              y: (py / 120) * h,
              vx: (Math.random() - 0.5) * 2.5,
              vy: -0.5 - Math.random() * 2,
              life: 1.0,
              color: `hsla(${260 + Math.random() * 80}, 90%, 65%, 0.8)`
            });
          }
        }
      }

      // Draw and tick particles
      particles.forEach((p, idx) => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2 * config.gain, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 4;
        ctx.shadowColor = '#d946ef';
        ctx.fill();
        ctx.shadowBlur = 0; // reset

        // Update Position
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 0.02;

        if (p.life <= 0 || p.y < 0 || p.x < 0 || p.x > w) {
          particles.splice(idx, 1);
        }
      });
    }

    // 16. RETRO CRT AMBER
    function filterRetroAmber(data, w, h) {
      if (!data) return;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b) * config.gain;
        
        // Phosphor amber grading
        data[i] = Math.min(255, mono * 1.15); // rich amber red
        data[i+1] = Math.min(255, mono * 0.75); // amber green
        data[i+2] = Math.min(255, mono * 0.15); // amber blue minimal
      }
    }

    // 17. ANALYTICAL CCTV SECURITY SYSTEM
    function renderSecurityCCTV(ctx, w, h, vidElement) {
      if (w <= 0 || h <= 0) return;
      // Greyscale with security interface lines
      try {
        ctx.drawImage(vidElement, 0, 0, w, h);
      } catch (e) {
        return;
      }
      
      const imgData = safeGetImageData(ctx, 0, 0, w, h);
      if (!imgData) return;
      const d = imgData.data;
      
      for (let i = 0; i < d.length; i += 4) {
        const mono = (0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2]);
        d[i] = Math.min(255, mono * 0.95);
        d[i+1] = Math.min(255, mono * 1.05); // slight green overlay
        d[i+2] = Math.min(255, mono * 0.95);
      }
      ctx.putImageData(imgData, 0, 0);

      // CCTV Static Interference line
      const lineY = (performance.now() * 0.15) % h;
      ctx.beginPath();
      ctx.moveTo(0, lineY);
      ctx.lineTo(w, lineY);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Dynamic Security HUD bounds
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.7)';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(30, 30, w - 60, h - 60);

      // Simulated target vectors
      ctx.fillStyle = '#10b981';
      ctx.font = '10px monospace';
      ctx.fillText("CAM-04 SECURITY PASSIVE STREAM", 45, 55);
      ctx.fillText("MOTION MONITORING SECURE: TR_LOCK_A", 45, h - 45);
    }

    // 18. SYNTHWAVE CHROMA SPECTRA
    function filterSynthwave(data, w, h) {
      if (!data) return;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        const mono = (0.299 * r + 0.587 * g + 0.114 * b);
        
        // Deep fluorescent pink to electric cyan mapping
        if (mono < 128) {
          data[i] = Math.min(255, mono * 2);      // Intense Pink R
          data[i+1] = Math.max(0, mono * 0.1);
          data[i+2] = Math.min(255, mono * 1.6);  // Intense Blue B
        } else {
          data[i] = Math.max(0, 255 - (mono - 128) * 2);
          data[i+1] = Math.min(255, (mono - 128) * 2); // Bright cyan
          data[i+2] = 255;
        }
      }
    }

    // 19. DEEP COLD ZERO SCAN (Blue-Green venting)
    function filterDeepCold(data, w, h) {
      if (!data) return;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i+1];
        const b = data[i+2];
        
        // Exclude Red channels completely to filter out heat signatures
        data[i] = 0;
        data[i+1] = Math.min(255, g * 1.1);
        data[i+2] = Math.min(255, b * 1.4);
      }
    }

    // --- CYBERPUNK HUD DECK OVERLAYS ---
    function drawHUDOverlay(ctx, w, h) {
      const time = performance.now();
      
      // Target Lock Reticle Rendering
      if (targetLock) {
        const { x, y } = targetLock;
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 1.5;
        
        // Tracking Box
        const size = 35 + Math.sin(time * 0.01) * 5;
        ctx.strokeRect(x - size/2, y - size/2, size, size);
        
        // Corner indicators
        ctx.beginPath();
        // Top Left
        ctx.moveTo(x - size, y - size/2);
        ctx.lineTo(x - size, y - size);
        ctx.lineTo(x - size/2, y - size);
        // Top Right
        ctx.moveTo(x + size/2, y - size);
        ctx.lineTo(x + size, y - size);
        ctx.lineTo(x + size, y - size/2);
        // Bottom Left
        ctx.moveTo(x - size, y + size/2);
        ctx.lineTo(x - size, y + size);
        ctx.lineTo(x - size/2, y + size);
        // Bottom Right
        ctx.moveTo(x + size/2, y + size);
        ctx.lineTo(x + size, y + size);
        ctx.lineTo(x + size, y + size/2);
        ctx.stroke();

        // Lock text
        ctx.fillStyle = '#ef4444';
        ctx.font = '9px monospace';
        ctx.fillText(`TARGET CORRELATE: UNKNOWN`, x + size + 4, y - 5);
        ctx.fillText(`COORD X:${x.toFixed(0)} Y:${y.toFixed(0)}`, x + size + 4, y + 8);
      }

      // Cyberpunk AR HUD Overlay (For Cyberpunk mode M12 specifically or overlaid subtly on all)
      if (selectedMode === 'M12') {
        ctx.strokeStyle = 'rgba(6, 182, 212, 0.4)';
        ctx.lineWidth = 1;
        
        // Center crosshair
        ctx.beginPath();
        ctx.arc(w/2, h/2, 40, 0, Math.PI * 2);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(w/2 - 60, h/2); ctx.lineTo(w/2 - 20, h/2);
        ctx.moveTo(w/2 + 20, h/2); ctx.lineTo(w/2 + 60, h/2);
        ctx.moveTo(w/2, h/2 - 60); ctx.lineTo(w/2, h/2 - 20);
        ctx.moveTo(w/2, h/2 + 20); ctx.lineTo(w/2, h/2 + 60);
        ctx.stroke();

        // HUD Text Metrics
        ctx.fillStyle = 'rgba(6, 182, 212, 0.85)';
        ctx.font = '10px monospace';
        ctx.fillText(`ELEV: 122M // BARO: 1012HPA`, 40, 95);
        ctx.fillText(`AZIMUTH: 314° NNE`, 40, 115);
        ctx.fillText(`SPECTRUM ACCEL: CUDA_GPU_ON`, 40, 135);

        ctx.fillText(`BATTERY CORES: 98.4%`, w - 180, 95);
        ctx.fillText(`GPS DISP: ACCURATE`, w - 180, 115);
        ctx.fillText(`TELEMETRY DECK: READY`, w - 180, 135);
      }
    }

    // --- MAIN RENDER AND FRAME TIMING LOOP ---
    function renderLoop(time) {
      if (!stream) return;

      const w = canvas.width;
      const h = canvas.height;
      
      // Ensure we have a valid width and height before processing image buffers
      if (w <= 0 || h <= 0) {
        animationFrameId = requestAnimationFrame(renderLoop);
        return;
      }

      // Handle Framerate Timing
      frameCount++;
      const elapsed = time - lastTime;
      if (elapsed >= 1000) {
        currentFps = (frameCount * 1000) / elapsed;
        fpsCounter.textContent = `${currentFps.toFixed(1)} FPS`;
        frameCount = 0;
        lastTime = time;
        
        // System telemetry auto logger
        if (Math.random() < 0.25) {
          const sysTemps = [38, 39, 40, 41, 42];
          const chosenTemp = sysTemps[Math.floor(Math.random() * sysTemps.length)];
          addTelemetryLog(`THERMALS NORMAL: CORE_TEMP ${chosenTemp}°C`);
        }
      }

      // Update Timestamp HUD
      const now = new Date();
      systemTimestamp.textContent = now.toTimeString().split(' ')[0];

      // Draw original video to primary Canvas (applying zoom factor)
      ctx.clearRect(0, 0, w, h);
      
      const zoom = config.zoom;
      try {
        if (zoom > 1.0) {
          const cropW = w / zoom;
          const cropH = h / zoom;
          const cropX = (w - cropW) / 2;
          const cropY = (h - cropH) / 2;
          ctx.drawImage(video, cropX, cropY, cropW, cropH, 0, 0, w, h);
        } else {
          ctx.drawImage(video, 0, 0, w, h);
        }
      } catch (err) {
        // Handle potential draw failures gracefully
        animationFrameId = requestAnimationFrame(renderLoop);
        return;
      }

      // Read ImageData buffer for direct filter processors
      let imgData = null;
      let data = null;
      const needsPixelBuffer = ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M08', 'M13', 'M14', 'M16', 'M18', 'M20', 'M21', 'M22'].includes(selectedMode);

      if (needsPixelBuffer) {
        imgData = safeGetImageData(ctx, 0, 0, w, h);
        if (imgData) {
          data = imgData.data;
        }
      }

      // --- MATCH SPECIFIC MODE FOR DRAW ---
      if (!needsPixelBuffer || (needsPixelBuffer && data)) {
        switch (selectedMode) {
          case 'M01':
            // Standard video (Passthrough) with Gain adjustment
            if (config.gain !== 1.0 && data) {
              for (let i = 0; i < data.length; i += 4) {
                data[i] = Math.min(255, data[i] * config.gain);
                data[i+1] = Math.min(255, data[i+1] * config.gain);
                data[i+2] = Math.min(255, data[i+2] * config.gain);
              }
            }
            break;
          case 'M02':
            filterNightVision(data, w, h);
            break;
          case 'M03':
            filterThermal(data, w, h);
            break;
          case 'M04':
            filterXRay(data, w, h);
            break;
          case 'M05':
            filterInfrared(data, w, h);
            break;
          case 'M06':
            filterUltraviolet(data, w, h);
            break;
          case 'M07':
            // Render Sonar
            renderSonarRadar(ctx, w, h, video);
            break;
          case 'M08':
            filterNeonEdges(data, w, h);
            break;
          case 'M09':
            // Lidar Cloud
            renderLidarCloud(ctx, w, h, video);
            break;
          case 'M10':
            // Matrix code
            renderMatrixRain(ctx, w, h, video);
            break;
          case 'M11':
            // Predator Heat low-res blocky
            renderPredatorThermal(ctx, w, h, video);
            break;
          case 'M12':
            // Cyberpunk HUD AR with standard colors (Gain applied)
            if (data) {
              for (let i = 0; i < data.length; i += 4) {
                data[i] = Math.min(255, data[i] * config.gain * 0.9);
                data[i+1] = Math.min(255, data[i+1] * config.gain * 1.1); // green bias
                data[i+2] = Math.min(255, data[i+2] * config.gain * 1.1); // blue bias
              }
            }
            break;
          case 'M13':
            filterHazmat(data, w, h);
            break;
          case 'M14':
            filterSolarized(data, w, h);
            break;
          case 'M15':
            // Glitch / EMP
            renderEmpGlitch(ctx, w, h, video);
            break;
          case 'M16':
            // Structural Blueprint
            renderBlueprint(ctx, w, h, video);
            break;
          case 'M17':
            // Quantum Contours
            renderQuantumParticles(ctx, w, h, video);
            break;
          case 'M18':
            filterRetroAmber(data, w, h);
            break;
          case 'M19':
            // CCTV Greyscale
            renderSecurityCCTV(ctx, w, h, video);
            break;
          case 'M20':
            // Chromatic dispersion (fringe offsets) done directly in custom copy
            break;
          case 'M21':
            filterSynthwave(data, w, h);
            break;
          case 'M22':
            filterDeepCold(data, w, h);
            break;
        }

        // Write processed pixel stream back to viewscreen canvas if loaded
        if (needsPixelBuffer && imgData) {
          ctx.putImageData(imgData, 0, 0);
        }
      }

      // Apply Chromatic Dispersion for general modes if slider > 0
      const chShift = config.chromatic;
      if (chShift > 0 && ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M08', 'M12', 'M13', 'M14', 'M18', 'M20', 'M21', 'M22'].includes(selectedMode)) {
        applyChromaticDispersion(w, h, chShift);
      }

      // Apply Global CRT static noise overlays
      const noiseStrength = config.noise;
      if (noiseStrength > 0) {
        applyStaticNoise(w, h, noiseStrength);
      }

      // Apply Global matrix scanlines if slider > 0
      const scanlineIntensity = config.scanlines;
      if (scanlineIntensity > 0) {
        applyScanlines(w, h, scanlineIntensity);
      }

      // Finally, draw Cyber HUD vector scopes and target tracks
      drawHUDOverlay(ctx, w, h);

      animationFrameId = requestAnimationFrame(renderLoop);
    }

    // High performance chromatic displacement
    function applyChromaticDispersion(w, h, shift) {
      if (w <= 0 || h <= 0) return;
      const imgData = safeGetImageData(ctx, 0, 0, w, h);
      if (!imgData) return;
      const d = imgData.data;
      const temp = new Uint8ClampedArray(d);
      
      for (let i = 0; i < d.length; i += 4) {
        if (i + shift * 4 < d.length) {
          d[i] = temp[i + shift * 4]; // displace red
        }
        if (i - shift * 4 >= 0) {
          d[i+2] = temp[i - shift * 4]; // displace blue
        }
      }
      ctx.putImageData(imgData, 0, 0);
    }

    // High-performance static noise pixel injection
    function applyStaticNoise(w, h, intensity) {
      if (w <= 0 || h <= 0) return;
      const imgData = safeGetImageData(ctx, 0, 0, w, h);
      if (!imgData) return;
      const d = imgData.data;
      const factor = intensity / 100;
      
      for (let i = 0; i < d.length; i += 4) {
        if (Math.random() < factor) {
          const noise = (Math.random() - 0.5) * 65;
          d[i] = Math.max(0, Math.min(255, d[i] + noise));
          d[i+1] = Math.max(0, Math.min(255, d[i+1] + noise));
          d[i+2] = Math.max(0, Math.min(255, d[i+2] + noise));
        }
      }
      ctx.putImageData(imgData, 0, 0);
    }

    // Direct scanlines blending on canvas
    function applyScanlines(w, h, intensity) {
      ctx.save();
      ctx.globalAlpha = intensity / 130; // Scale range
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
      ctx.lineWidth = 1;
      
      for (let y = 0; y < h; y += 3) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }
      ctx.restore();
    }

    // --- CAPTURE DISK WRITER ---
    function captureSnapshot() {
      if (!stream) {
        addTelemetryLog("ERR: NO ACTIVE FEED TO CAPTURE");
        return;
      }
      playSynthBeep(650, 0.4, 0.1, 'sawtooth');
      
      const link = document.createElement('a');
      link.download = `OMNIVISION_SCAN_${selectedMode}_${Date.now()}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      
      addTelemetryLog(`INTELLIGENCE CAPTURE SAVED: ${link.download}`);
    }

    // --- INTERACTIVE TARGET TRACKING CLICK COORDINATES ---
    canvas.addEventListener('mousedown', (e) => {
      if (!stream) return;
      const rect = canvas.getBoundingClientRect();
      // Translate screen coordinates to actual canvas aspect ratio coordinates
      const x = ((e.clientX - rect.left) / rect.width) * canvas.width;
      const y = ((e.clientY - rect.top) / rect.height) * canvas.height;
      
      targetLock = { x, y };
      targetCoordinates.textContent = `TARGET RETICLE: X:${x.toFixed(0)} Y:${y.toFixed(0)}`;
      targetCoordinates.classList.remove('text-cyan-400');
      targetCoordinates.classList.add('text-red-500');
      
      playSynthBeep(980, 0.25, 0.1, 'sine');
      addTelemetryLog(`LOCK ACQUIRED: COORDS X:${x.toFixed(0)} Y:${y.toFixed(0)}`);
    });

    // --- GLOBAL POSITION COORDINATES EMULATION ---
    function simulateLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
          geoLocation.textContent = `STABLE // LAT: ${pos.coords.latitude.toFixed(4)} LON: ${pos.coords.longitude.toFixed(4)}`;
        }, () => {
          // Fallback static secure locations
          geoLocation.textContent = `STABLE // SECURE SITE: AD-72 // LAT: 45.1097 LON: -122.6801`;
        });
      } else {
        geoLocation.textContent = `STABLE // SECURE SITE: AD-72 // LAT: 45.1097 LON: -122.6801`;
      }
    }

    // --- RESET SLIDERS ---
    function resetSliders() {
      sliderGain.value = 1.0;
      sliderNoise.value = 15;
      sliderScanlines.value = 50;
      sliderChromatic.value = 2;
      sliderZoom.value = 1.0;
      updateConfig();
      addTelemetryLog("CALIBRATE COMPLETE: SPECTRUM TUNERS RESET.");
      playSynthBeep(300, 0.15, 0.05);
    }

    // --- EVENT LISTENERS ---
    window.addEventListener('load', () => {
      generateModeGrid();
      populateCameras();
      selectVisionMode('M01');
      simulateLocation();
      updateConfig();
      
      // Auto register device select alterations
      navigator.mediaDevices.ondevicechange = populateCameras;
    });

    btnStartCamera.addEventListener('click', startCamera);
    btnTriggerActive.addEventListener('click', startCamera);
    btnSnapshot.addEventListener('click', captureSnapshot);
    audioToggle.addEventListener('click', toggleAudio);
    btnResetSliders.addEventListener('click', resetSliders);

    [sliderGain, sliderNoise, sliderScanlines, sliderChromatic, sliderZoom].forEach(slider => {
      slider.addEventListener('input', updateConfig);
    });
  </script>
</body>
</html>
