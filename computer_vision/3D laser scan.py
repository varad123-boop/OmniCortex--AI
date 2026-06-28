<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LidarCam 3D - Webcam LiDAR & Terrain Depth Scanner</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Three.js Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- Three.js OrbitControls -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        /* Custom neon sci-fi theme styling */
        .glow-green {
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.5);
        }
        .glow-blue {
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
        }
        .glow-red {
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
        }
        /* Custom scrollbars */
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
            background: #475569;
        }
        /* Scanner sweep animation */
        @keyframes sweep {
            0% { transform: translateY(-100%); opacity: 0; }
            50% { opacity: 0.8; }
            100% { transform: translateY(100%); opacity: 0; }
        }
        .scan-line {
            animation: sweep 3s infinite linear;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col overflow-x-hidden">

    <!-- Header Navigation -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex flex-wrap justify-between items-center gap-4">
        <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-lg bg-green-500 flex items-center justify-center glow-green">
                <i class="fa-solid fa-radar text-slate-950 text-xl animate-pulse"></i>
            </div>
            <div>
                <h1 class="text-xl font-black tracking-wider text-green-400">LIDAR-CAM <span class="text-xs font-bold bg-green-500/20 text-green-300 px-2 py-0.5 rounded border border-green-500/30">v3.0 PRO</span></h1>
                <p class="text-xs text-slate-400">Real-time Webcam 3D Depth & Terrain Map Generator</p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <span class="flex h-3 w-3 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span id="system-status" class="text-xs font-mono text-green-400">SYSTEM: ONLINE</span>
        </div>
    </header>

    <!-- Main Content Panel -->
    <main class="flex-1 grid grid-cols-1 xl:grid-cols-12 gap-6 p-6">
        
        <!-- Left Side Control Panel (4 cols) -->
        <div class="xl:col-span-4 flex flex-col gap-6">
            
            <!-- Input Source & Calibration -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <i class="fa-solid fa-sliders text-green-400"></i>
                    <h2 class="text-md font-bold tracking-wide uppercase">Source & Capture Controls</h2>
                </div>
                
                <!-- Source Selectors -->
                <div class="flex gap-2">
                    <button id="btn-webcam" class="flex-1 py-2 px-3 rounded-lg bg-green-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-green-400">
                        <i class="fa-solid fa-camera"></i> Webcam Feed
                    </button>
                    <button id="btn-demo" class="flex-1 py-2 px-3 rounded-lg bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-700 border border-slate-700">
                        <i class="fa-solid fa-bolt"></i> Substation Demo
                    </button>
                </div>

                <!-- Custom Alert Info Box (No Native Alert) -->
                <div id="status-message" class="hidden p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg text-xs text-blue-300 flex items-start gap-2">
                    <i class="fa-solid fa-info-circle mt-0.5"></i>
                    <span id="status-text">Webcam streaming initialized successfully.</span>
                </div>

                <!-- Camera Select (Dynamic) -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-slate-400 font-semibold uppercase">Video Input Device</label>
                    <select id="camera-select" class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 outline-none focus:border-green-500">
                        <option value="">Default Webcam</option>
                    </select>
                </div>

                <!-- Mapping Mode -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-slate-400 font-semibold uppercase">Depth Extraction Model</label>
                    <select id="depth-mode" class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 outline-none focus:border-green-500">
                        <option value="luminance" selected>Luminance Vector (Classic LiDAR)</option>
                        <option value="contrast">High-Contrast Elevation (Substation detail)</option>
                        <option value="motion">Active Motion Radar (Thermal Sweep)</option>
                        <option value="radial">Spherical Radial Scan</option>
                    </select>
                </div>
            </div>

            <!-- Signal Tuning -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <i class="fa-solid fa-wave-square text-blue-400"></i>
                    <h2 class="text-md font-bold tracking-wide uppercase">Signal Processing</h2>
                </div>

                <!-- Resolution Grid -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Scanning Density (Resolution)</span>
                        <span id="res-val" class="text-blue-400 font-mono">120 x 90 pts</span>
                    </div>
                    <input id="resolution" type="range" min="60" max="160" step="20" value="120" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                </div>

                <!-- Depth Extrusion Scale -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">LiDAR Z-Scale (Height Amplitude)</span>
                        <span id="z-scale-val" class="text-blue-400 font-mono">40</span>
                    </div>
                    <input id="z-scale" type="range" min="5" max="120" value="40" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                </div>

                <!-- Offset Shift -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Elevation Threshold (Floor Cutoff)</span>
                        <span id="floor-val" class="text-blue-400 font-mono">15%</span>
                    </div>
                    <input id="floor-cutoff" type="range" min="0" max="80" value="15" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                </div>

                <!-- Filter Settings -->
                <div class="grid grid-cols-2 gap-3 pt-2">
                    <div class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
                        <input id="chk-blur" type="checkbox" checked class="w-4 h-4 rounded text-blue-500 focus:ring-blue-500 bg-slate-900 border-slate-700">
                        <div class="flex flex-col">
                            <span class="text-xs font-bold text-slate-300">Spatial Filter</span>
                            <span class="text-[10px] text-slate-500">Smooths jitter</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
                        <input id="chk-invert" type="checkbox" class="w-4 h-4 rounded text-blue-500 focus:ring-blue-500 bg-slate-900 border-slate-700">
                        <div class="flex flex-col">
                            <span class="text-xs font-bold text-slate-300">Invert Phase</span>
                            <span class="text-[10px] text-slate-500">Reverse depth</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Colormap Palette & 3D Style -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <i class="fa-solid fa-palette text-purple-400"></i>
                    <h2 class="text-md font-bold tracking-wide uppercase">Visualization Options</h2>
                </div>

                <!-- Colormap Picker -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-slate-400 font-semibold uppercase">Elevation Palette</label>
                    <select id="colormap" class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 outline-none focus:border-purple-500">
                        <option value="jet" selected>Jet Spectrum (Authentic LiDAR)</option>
                        <option value="viridis">Viridis (High Precision)</option>
                        <option value="hot">Thermal Scan (Infrared)</option>
                        <option value="cool">Synthetic Ocean (Cyans & Blues)</option>
                        <option value="grayscale">Raw Laser Intensity</option>
                    </select>
                </div>

                <!-- Point Cloud Style -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-slate-400 font-semibold uppercase">3D Render Topology</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button id="btn-style-points" class="py-2 px-2 rounded bg-purple-500 text-slate-950 font-bold text-xs flex flex-col items-center gap-1 transition">
                            <i class="fa-solid fa-ellipsis"></i>
                            Points
                        </button>
                        <button id="btn-style-mesh" class="py-2 px-2 rounded bg-slate-850 text-slate-400 font-bold text-xs flex flex-col items-center gap-1 transition border border-slate-800">
                            <i class="fa-solid fa-network-wired"></i>
                            Mesh Wire
                        </button>
                        <button id="btn-style-solid" class="py-2 px-2 rounded bg-slate-850 text-slate-400 font-bold text-xs flex flex-col items-center gap-1 transition border border-slate-800">
                            <i class="fa-solid fa-cube"></i>
                            Solid Surf
                        </button>
                    </div>
                </div>

                <!-- Sonar Audio Checkbox -->
                <div class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
                    <input id="chk-audio" type="checkbox" class="w-4 h-4 rounded text-purple-500 focus:ring-purple-500 bg-slate-900 border-slate-700">
                    <div class="flex flex-col">
                        <span class="text-xs font-bold text-slate-300">Acoustic Echo Location (Sonar Ping)</span>
                        <span class="text-[10px] text-slate-500">Audio feedback frequency mapped to center depth</span>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Side Screens (8 cols) -->
        <div class="xl:col-span-8 flex flex-col gap-6">
            
            <!-- Dual Visualizer Display (Split Screens) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <!-- Left Screen: Live Input & 2D Heightmap -->
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col gap-3 relative min-h-[300px]">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                        <div class="flex items-center gap-2">
                            <span class="h-2 w-2 rounded-full bg-red-500 animate-pulse"></span>
                            <span id="feed-title" class="text-xs font-bold tracking-wider uppercase text-slate-300">Webcam Elevation Scanning</span>
                        </div>
                        <span class="text-[10px] font-mono text-slate-500" id="fps-counter">SCAN RATE: 0 FPS</span>
                    </div>

                    <!-- Video Hidden Node & Canvas Rendering Area -->
                    <video id="video" autoplay playsinline muted class="hidden"></video>
                    
                    <div class="relative flex-1 bg-slate-950 rounded-xl overflow-hidden flex items-center justify-center border border-slate-950">
                        <canvas id="canvas-depth" class="w-full h-full object-cover rounded-xl"></canvas>
                        
                        <!-- Radar Scanner Overlay lines -->
                        <div class="absolute inset-0 border border-green-500/20 pointer-events-none rounded-xl"></div>
                        <div class="absolute top-0 left-0 w-full h-0.5 bg-green-500/70 shadow-[0_0_10px_rgba(34,197,94,1)] pointer-events-none scan-line"></div>
                        
                        <!-- Real-time HUD stats -->
                        <div class="absolute bottom-3 left-3 bg-slate-950/80 backdrop-blur border border-slate-800 rounded p-2 text-[10px] font-mono text-green-400 flex flex-col gap-0.5">
                            <div>SCAN WIDTH: <span id="hud-width">0px</span></div>
                            <div>SCAN HEIGHT: <span id="hud-height">0px</span></div>
                            <div>SIGNAL GAIN: <span id="hud-gain">1.0x</span></div>
                        </div>

                        <!-- Topographical Overlays -->
                        <div class="absolute top-3 right-3 bg-slate-950/80 backdrop-blur border border-slate-800 rounded px-2 py-1 text-[10px] font-mono text-blue-400">
                            COORD REF: WGS-84
                        </div>
                    </div>
                </div>

                <!-- Right Screen: Interactive 3D Spatial Grid -->
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col gap-3 relative min-h-[300px]">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-cube text-blue-400"></i>
                            <span class="text-xs font-bold tracking-wider uppercase text-slate-300">3D Interactive Point Cloud</span>
                        </div>
                        <button id="btn-reset-cam" class="text-[10px] bg-slate-800 border border-slate-700 px-2 py-0.5 rounded text-slate-300 hover:bg-slate-700 hover:text-white transition">
                            <i class="fa-solid fa-arrows-rotate mr-1"></i>Reset View
                        </button>
                    </div>

                    <div id="three-container" class="relative flex-1 bg-slate-950 rounded-xl overflow-hidden min-h-[220px]">
                        <!-- Three JS will mount here dynamically -->
                        <div id="three-loader" class="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-slate-950 z-10">
                            <i class="fa-solid fa-circle-notch animate-spin text-blue-500 text-3xl"></i>
                            <p class="text-xs text-slate-400">Initializing 3D Projection Space...</p>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Lower Action Station & Data Exporter -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-wrap justify-between items-center gap-4">
                <div class="flex flex-col gap-1">
                    <h3 class="text-sm font-bold text-slate-200">Export & Diagnostic Capture Panel</h3>
                    <p class="text-xs text-slate-400">Save current scanner elevations and meshes directly into local disk formats.</p>
                </div>
                
                <div class="flex flex-wrap gap-3">
                    <button id="btn-freeze" class="py-2.5 px-4 bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-yellow">
                        <i id="freeze-icon" class="fa-solid fa-pause"></i> 
                        <span id="freeze-text">FREEZE FRAME</span>
                    </button>
                    <button id="btn-export-obj" class="py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-black text-xs rounded-xl flex items-center gap-2 transition glow-blue">
                        <i class="fa-solid fa-file-export"></i> EXPORT OBJ MESH
                    </button>
                    <button id="btn-export-png" class="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-black text-xs rounded-xl flex items-center gap-2 transition">
                        <i class="fa-solid fa-image"></i> EXPORT HEIGHTMAP
                    </button>
                </div>
            </div>

            <!-- Custom Message Console Log -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-2">
                    <div class="flex items-center gap-2 text-xs text-slate-400 uppercase font-mono">
                        <i class="fa-solid fa-terminal text-green-400"></i> Scanner System Diagnostics
                    </div>
                    <span class="text-[9px] text-slate-600">CONSOLE OUT</span>
                </div>
                <div id="terminal-out" class="font-mono text-[11px] text-green-500/90 h-24 overflow-y-auto flex flex-col gap-1 pr-2">
                    <div>[SYS] Initializing LidarCam 3D Kernels... Done.</div>
                    <div>[SYS] Buffer arrays pre-allocated for dynamic coordinate grid.</div>
                    <div>[SYS] WebGL 2.0 viewport setup ready.</div>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-slate-500 mt-auto">
        <div>&copy; 2026 LidarCam 3D Engine. Inspired by Topographic LiDAR Terrain Models.</div>
        <div class="flex items-center gap-4">
            <span class="hover:text-slate-400 cursor-pointer transition">Terms of Access</span>
            <span class="hover:text-slate-400 cursor-pointer transition">Diagnostic Logs</span>
        </div>
    </footer>

    <!-- App Scripts -->
    <script>
        // --- Web Audio Synthesizer for Sonar ping sound effect ---
        let audioCtx = null;
        function playSonarPing(frequency = 500) {
            if (!document.getElementById('chk-audio').checked) return;
            try {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(frequency, audioCtx.currentTime);
                
                // Classic sonar decay envelope
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.2);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 1.3);
            } catch (err) {
                console.warn("Audio Context init blocked or failed: ", err);
            }
        }

        // Play regular scan click sounds mapping center elevation
        let lastPingTime = 0;
        function updateAcousticScan(centerDepth) {
            let now = Date.now();
            if (now - lastPingTime > 1500) { // every 1.5s
                // Map center depth (0-1) to pitch
                let pitch = 300 + (centerDepth * 800);
                playSonarPing(pitch);
                lastPingTime = now;
            }
        }

        // Console logger
        const terminal = document.getElementById('terminal-out');
        function logToTerminal(message, type = 'sys') {
            const time = new Date().toLocaleTimeString();
            const div = document.createElement('div');
            let colorClass = 'text-green-500/90';
            if (type === 'err') colorClass = 'text-red-400';
            if (type === 'success') colorClass = 'text-blue-400';
            div.className = colorClass;
            div.innerHTML = `<span class="text-slate-600">[${time}]</span> [${type.toUpperCase()}] ${message}`;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        // --- Global App State ---
        let isWebcam = true;
        let isFrozen = false;
        let scanFPS = 0;
        let frameCount = 0;
        let lastFPSUpdateTime = Date.now();
        let demoAngle = 0;
        let animationFrameId = null;

        // Custom Modal alerts
        function showNotification(text, duration = 3000) {
            const box = document.getElementById('status-message');
            const boxText = document.getElementById('status-text');
            box.classList.remove('hidden');
            boxText.innerText = text;
            setTimeout(() => {
                box.classList.add('hidden');
            }, duration);
        }

        // --- Substation Generator Algorithm (Mathematical terrain generation based on uploaded image) ---
        // Generates the gorgeous Substation with structures, power lines, transformer boxes, hills
        function generateSubstationScan(x, y, cols, rows, time) {
            // Base Terrain - hilly landscape
            let nx = x / cols - 0.5;
            let ny = y / rows - 0.5;
            
            // Base hill elevation (sine wave combined with a flat plain on left)
            let baseTerrain = Math.sin(nx * 4 + 1.2) * 0.25 + Math.cos(ny * 3 - 0.5) * 0.15;
            // Introduce a slope from Left (Red/High) to Right (Blue/Low) matching the user's reference image
            let imageSlope = -nx * 0.45;
            let finalTerrain = 0.5 + baseTerrain + imageSlope;
            
            // Limit plain bounds
            if (finalTerrain < 0) finalTerrain = 0;
            if (finalTerrain > 1) finalTerrain = 1;

            // Generate structured assets: Transformer bays (Left upper plateau)
            // Transformer 1 block
            if (nx > -0.3 && nx < -0.1 && ny > -0.3 && ny < 0.1) {
                // High transformer box structure
                let shape = Math.sin((nx + 0.2) * 20) * Math.sin((ny + 0.1) * 20);
                if (shape > 0.3) {
                    finalTerrain += 0.22;
                }
            }

            // Power transmission tower 1 (Left middle)
            let tower1X = -0.35, tower1Y = 0.25;
            let distToTower1 = Math.sqrt((nx - tower1X)**2 + (ny - tower1Y)**2);
            if (distToTower1 < 0.05) {
                // High spike structure representing power transmission tower
                let towerHeight = (0.05 - distToTower1) * 7.5;
                finalTerrain += towerHeight;
            }

            // Power transmission tower 2 (Right lower)
            let tower2X = 0.2, tower2Y = -0.15;
            let distToTower2 = Math.sqrt((nx - tower2X)**2 + (ny - tower2Y)**2);
            if (distToTower2 < 0.04) {
                let towerHeight = (0.04 - distToTower2) * 8.0;
                finalTerrain += towerHeight;
            }

            // Power Lines sagging between towers (Visual structural lines)
            // Represent cables as mathematical elevation lines stretching across
            let lineEquation1 = (nx * 0.6 + ny - 0.05);
            if (Math.abs(lineEquation1) < 0.006) {
                // Suspended catenary curves
                let sagFactor = 1.0 - Math.abs(nx) * 0.3;
                finalTerrain += 0.08 * sagFactor;
            }

            let lineEquation2 = (nx * -0.4 + ny + 0.25);
            if (Math.abs(lineEquation2) < 0.007) {
                let sagFactor = 1.0 - Math.abs(ny) * 0.25;
                finalTerrain += 0.09 * sagFactor;
            }

            // Suburban neighborhood detail: rows of small box houses and vegetation (Bottom section)
            if (ny > 0.2) {
                // Adding repetitive tree/house elevations
                let houseRow = Math.sin(nx * 18) * Math.cos(ny * 16);
                if (houseRow > 0.15) {
                    finalTerrain += 0.14; // House roofs elevation
                }
            }

            // Dynamic moving scanner laser sweeps over
            let scanSweep = Math.sin(nx * 8 - time * 0.002) * 0.02;
            finalTerrain += scanSweep;

            return Math.max(0.01, Math.min(0.99, finalTerrain));
        }

        // Jet colormap function mimicking authentic LiDAR scans
        function getLiDARColor(value, palette = 'jet') {
            let r = 0, g = 0, b = 0;
            
            if (palette === 'jet') {
                // Precise Jet Rainbow: Dark Blue -> Blue -> Cyan -> Green -> Yellow -> Red -> Dark Red
                if (value < 0.15) {
                    b = 0.5 + (value / 0.15) * 0.5;
                } else if (value < 0.35) {
                    b = 1.0;
                    g = (value - 0.15) / 0.20;
                } else if (value < 0.55) {
                    g = 1.0;
                    b = 1.0 - (value - 0.35) / 0.20;
                } else if (value < 0.75) {
                    g = 1.0;
                    r = (value - 0.55) / 0.20;
                } else if (value < 0.90) {
                    r = 1.0;
                    g = 1.0 - (value - 0.75) / 0.15;
                } else {
                    r = 1.0 - (value - 0.90) / 0.10 * 0.5;
                }
            } else if (palette === 'viridis') {
                // High visibility perceptually uniform: purple to yellow
                r = 0.267 * (1.0 - value) + 0.993 * value;
                g = 0.004 * (1.0 - value) + 0.906 * value;
                b = 0.329 * (1.0 - value) + 0.143 * value;
            } else if (palette === 'hot') {
                // Black -> Dark Red -> Red -> Yellow -> White
                if (value < 0.33) {
                    r = value / 0.33;
                } else if (value < 0.66) {
                    r = 1.0;
                    g = (value - 0.33) / 0.33;
                } else {
                    r = 1.0;
                    g = 1.0;
                    b = (value - 0.66) / 0.34;
                }
            } else if (palette === 'cool') {
                // Cyan to Pink
                r = value;
                g = 1.0 - value;
                b = 1.0;
            } else {
                // Grayscale intensity map
                r = value;
                g = value;
                b = value;
            }

            return [Math.floor(r * 255), Math.floor(g * 255), Math.floor(b * 255)];
        }


        // --- Three.js 3D Grid Initialization ---
        let scene, camera, renderer, controls;
        let lidarPoints = null;
        let lidarMesh = null;
        let gridCols = 120;
        let gridRows = 90;
        let renderStyle = 'points'; // points, mesh, solid

        function initThree() {
            const container = document.getElementById('three-container');
            const width = container.clientWidth;
            const height = container.clientHeight || 280;

            // Scene & Camera
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x020617); // Slate-950

            camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            // Angle view resembling isometric GIS views
            camera.position.set(0, 100, 180);

            // Renderer setup
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(width, height);
            container.appendChild(renderer.domElement);

            // Orbit Controls
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxPolarAngle = Math.PI / 2; // Don't allow camera under floor

            // Lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(50, 150, 50);
            scene.add(directionalLight);

            // Add Ground Reference Grid Helper
            const gridHelper = new THREE.GridHelper(160, 40, 0x1e293b, 0x0f172a);
            gridHelper.position.y = -1;
            scene.add(gridHelper);

            // Add dynamic coordinates text overlay/compass
            const compassAxes = new THREE.AxesHelper(15);
            compassAxes.position.set(-75, 2, 55);
            scene.add(compassAxes);

            // Hide loader
            document.getElementById('three-loader').style.display = 'none';

            // Build Initial 3D Geometry Space
            build3DGeometry();

            // Resize callback
            window.addEventListener('resize', onWindowResize);
        }

        function onWindowResize() {
            const container = document.getElementById('three-container');
            if(!container) return;
            const width = container.clientWidth;
            const height = container.clientHeight || 280;
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height);
        }

        // Allocates Three.js Geometry based on Resolution variables
        function build3DGeometry() {
            if (lidarPoints) scene.remove(lidarPoints);
            if (lidarMesh) scene.remove(lidarMesh);

            const numPoints = gridCols * gridRows;
            const positions = new Float32Array(numPoints * 3);
            const colors = new Float32Array(numPoints * 3);

            let i = 0;
            for (let y = 0; y < gridRows; y++) {
                for (let x = 0; x < gridCols; x++) {
                    // Map points evenly centered at (0,0)
                    let xp = ((x / gridCols) - 0.5) * 150;
                    let zp = ((y / gridRows) - 0.5) * 110;

                    positions[i] = xp;
                    positions[i + 1] = 0; // Starts flat, animated dynamically
                    positions[i + 2] = zp;

                    // Initial deep blue color
                    colors[i] = 0.0;
                    colors[i + 1] = 0.1;
                    colors[i + 2] = 0.5;

                    i += 3;
                }
            }

            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            if (renderStyle === 'points') {
                // High-tech point scanner visual style
                const pMaterial = new THREE.PointsMaterial({
                    size: 1.4,
                    vertexColors: true,
                    transparent: true,
                    opacity: 0.9
                });
                lidarPoints = new THREE.Points(geometry, pMaterial);
                scene.add(lidarPoints);
            } else if (renderStyle === 'mesh' || renderStyle === 'solid') {
                // Build indexing for actual wireframe grid topology
                const indices = [];
                for (let y = 0; y < gridRows - 1; y++) {
                    for (let x = 0; x < gridCols - 1; x++) {
                        let idx = y * gridCols + x;
                        let right = idx + 1;
                        let bottom = idx + gridCols;
                        let bottomRight = bottom + 1;

                        // Two triangles per grid cell
                        indices.push(idx, bottom, right);
                        indices.push(right, bottom, bottomRight);
                    }
                }
                geometry.setIndex(indices);
                geometry.computeVertexNormals();

                const mMaterial = new THREE.MeshBasicMaterial({
                    vertexColors: true,
                    wireframe: renderStyle === 'mesh',
                    side: THREE.DoubleSide
                });
                lidarMesh = new THREE.Mesh(geometry, mMaterial);
                scene.add(lidarMesh);
            }
        }


        // --- Live Webcam Capture Initialization ---
        let webcamStream = null;
        const videoElement = document.getElementById('video');
        const cameraSelect = document.getElementById('camera-select');

        async function initWebcam(deviceId = null) {
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
            }

            const constraints = {
                audio: false,
                video: deviceId ? { deviceId: { exact: deviceId }, width: 640, height: 480 } : { width: 640, height: 480 }
            };

            try {
                webcamStream = await navigator.mediaDevices.getUserMedia(constraints);
                videoElement.srcObject = webcamStream;
                videoElement.play();
                isWebcam = true;
                
                // Toggle state styles
                document.getElementById('btn-webcam').className = "flex-1 py-2 px-3 rounded-lg bg-green-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition glow-green";
                document.getElementById('btn-demo').className = "flex-1 py-2 px-3 rounded-lg bg-slate-950 text-slate-400 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-900 border border-slate-800";
                document.getElementById('feed-title').innerText = "LIVE WEBCAM ELEVATION SCANNER";
                
                logToTerminal("Webcam access granted. High-frequency digital signal active.", "success");
                
                // Populate device selector once initialized
                populateDevices();
            } catch (err) {
                logToTerminal("No camera connected or access rejected. Activating synthetic demo engine.", "err");
                showNotification("Could not load Webcam. Launching Demo Scan!");
                activateDemoMode();
            }
        }

        async function populateDevices() {
            try {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(d => d.kind === 'videoinput');
                cameraSelect.innerHTML = "";
                
                if (videoDevices.length === 0) {
                    cameraSelect.innerHTML = "<option>No Camera Detected</option>";
                } else {
                    videoDevices.forEach((device, index) => {
                        const opt = document.createElement('option');
                        opt.value = device.deviceId;
                        opt.text = device.label || `Camera ${index + 1}`;
                        cameraSelect.appendChild(opt);
                    });
                }
            } catch (err) {
                console.warn("Unable to fetch visual capture hardware labels.");
            }
        }

        function activateDemoMode() {
            isWebcam = false;
            document.getElementById('btn-demo').className = "flex-1 py-2 px-3 rounded-lg bg-green-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition glow-green";
            document.getElementById('btn-webcam').className = "flex-1 py-2 px-3 rounded-lg bg-slate-950 text-slate-400 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-900 border border-slate-800";
            document.getElementById('feed-title').innerText = "DEMO INDUSTRIAL SUBSTATION SCAN";
            logToTerminal("Synthetic GIS substation radar simulator loaded.", "success");
        }


        // --- Core Render & Processing loop ---
        const depthCanvas = document.getElementById('canvas-depth');
        const depthCtx = depthCanvas.getContext('2d', { willReadFrequently: true });
        
        // Fast offscreen downsample processor
        const offCanvas = document.createElement('canvas');
        const offCtx = offCanvas.getContext('2d', { willReadFrequently: true });

        // Storage arrays to smooth scanning signals (temporal smoothing)
        let lastElevationMap = null;

        function runVisualProcessing() {
            if (isFrozen) {
                animationFrameId = requestAnimationFrame(runVisualProcessing);
                return;
            }

            // Keep sizes synchronized
            if (depthCanvas.width !== depthCanvas.clientWidth) {
                depthCanvas.width = depthCanvas.clientWidth;
                depthCanvas.height = depthCanvas.clientHeight;
                logToTerminal(`GIS Viewport adjusted to: ${depthCanvas.width}x${depthCanvas.height}`);
            }

            const zScale = parseFloat(document.getElementById('z-scale').value);
            const floorCutoff = parseFloat(document.getElementById('floor-cutoff').value) / 100;
            const enableFilter = document.getElementById('chk-blur').checked;
            const invertPhase = document.getElementById('chk-invert').checked;
            const colormapName = document.getElementById('colormap').value;
            const depthMode = document.getElementById('depth-mode').value;

            // Update stats displays
            document.getElementById('hud-width').innerText = `${depthCanvas.width}px`;
            document.getElementById('hud-height').innerText = `${depthCanvas.height}px`;
            document.getElementById('hud-gain').innerText = `${(zScale/40).toFixed(1)}x`;

            const width = depthCanvas.width;
            const height = depthCanvas.height;

            if (width === 0 || height === 0) {
                animationFrameId = requestAnimationFrame(runVisualProcessing);
                return;
            }

            // Downsample processing limits for high performance frame parsing
            offCanvas.width = gridCols;
            offCanvas.height = gridRows;

            // 1. Capture/Synthesize the base image source
            if (isWebcam && videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
                // Clear and mirror webcam
                offCtx.save();
                offCtx.translate(gridCols, 0);
                offCtx.scale(-1, 1);
                offCtx.drawImage(videoElement, 0, 0, gridCols, gridRows);
                offCtx.restore();
            } else {
                // Generate Synthetic LiDAR Substation Scene (Dynamic)
                demoAngle += 1.2;
                const demoImgData = offCtx.createImageData(gridCols, gridRows);
                for (let y = 0; y < gridRows; y++) {
                    for (let x = 0; x < gridCols; x++) {
                        let elev = generateSubstationScan(x, y, gridCols, gridRows, Date.now());
                        let colorVal = Math.floor(elev * 255);
                        let idx = (y * gridCols + x) * 4;
                        demoImgData.data[idx] = colorVal;     // R (elevation vector)
                        demoImgData.data[idx + 1] = colorVal; // G
                        demoImgData.data[idx + 2] = colorVal; // B
                        demoImgData.data[idx + 3] = 255;      // A
                    }
                }
                offCtx.putImageData(demoImgData, 0, 0);
            }

            // 2. Extract Depth & Elevation vector maps
            const imgData = offCtx.getImageData(0, 0, gridCols, gridRows);
            const pixels = imgData.data;

            // Setup current frame elevation buffer
            const currentElevations = new Float32Array(gridCols * gridRows);

            for (let y = 0; y < gridRows; y++) {
                for (let x = 0; x < gridCols; x++) {
                    let idx = (y * gridCols + x) * 4;
                    let r = pixels[idx];
                    let g = pixels[idx + 1];
                    let b = pixels[idx + 2];

                    let rawDepth = 0.5;

                    if (depthMode === 'luminance') {
                        // Standard luma formula: Brighter is closer
                        rawDepth = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0;
                    } else if (depthMode === 'contrast') {
                        // High pass filter simulating structural heights of pylons/edges
                        let edgeDetect = Math.abs(r - g) * 1.5;
                        rawDepth = (edgeDetect / 255.0) + (r / 255.0 * 0.4);
                    } else if (depthMode === 'motion') {
                        // Temporal active flow scanner
                        let frameIntensity = (r + g + b) / 3;
                        if (lastElevationMap) {
                            let lastIdx = y * gridCols + x;
                            let delta = Math.abs(frameIntensity / 255.0 - lastElevationMap[lastIdx]);
                            rawDepth = delta * 2.8 + 0.1;
                        } else {
                            rawDepth = frameIntensity / 255.0;
                        }
                    } else if (depthMode === 'radial') {
                        // Radial spatial grid projection
                        let distFromCenter = Math.sqrt((x - gridCols/2)**2 + (y - gridRows/2)**2) / (gridCols/2);
                        rawDepth = (1.0 - distFromCenter) * 0.6 + (r / 255.0 * 0.4);
                    }

                    if (invertPhase) {
                        rawDepth = 1.0 - rawDepth;
                    }

                    // Apply Spatial Smoothing Filter
                    if (enableFilter && lastElevationMap) {
                        let lastIdx = y * gridCols + x;
                        // Linear interpolation smoothing formula (Low-pass filter)
                        rawDepth = lastElevationMap[lastIdx] * 0.72 + rawDepth * 0.28;
                    }

                    // Lower threshold cutoff filter
                    if (rawDepth < floorCutoff) {
                        rawDepth = 0.0;
                    }

                    currentElevations[y * gridCols + x] = rawDepth;
                }
            }

            // Store current elevations as historical cache for filtering
            lastElevationMap = currentElevations;

            // Acoustic feedback calculation mapping center point elevation to pitch
            let centerIdx = Math.floor(gridRows / 2) * gridCols + Math.floor(gridCols / 2);
            updateAcousticScan(currentElevations[centerIdx]);

            // 3. Render 2D GIS Heightmap visualization
            const renderImgData = depthCtx.createImageData(width, height);
            
            // Map the downsampled elevation matrix to full viewport scale with LiDAR Jet colors
            for (let dy = 0; dy < height; dy++) {
                for (let dx = 0; dx < width; dx++) {
                    // Match screen space to low-res depth data index
                    let gx = Math.floor((dx / width) * gridCols);
                    let gy = Math.floor((dy / height) * gridRows);
                    let elevation = currentElevations[gy * gridCols + gx];

                    // Map value to gorgeous LiDAR Rainbow Spectrum
                    let colors = getLiDARColor(elevation, colormapName);

                    let pixelIdx = (dy * width + dx) * 4;
                    renderImgData.data[pixelIdx] = colors[0];     // R
                    renderImgData.data[pixelIdx + 1] = colors[1]; // G
                    renderImgData.data[pixelIdx + 2] = colors[2]; // B
                    renderImgData.data[pixelIdx + 3] = 255;       // A
                }
            }
            depthCtx.putImageData(renderImgData, 0, 0);

            // 4. Update Three.js 3D Mesh vertices
            const activeObject = (renderStyle === 'points') ? lidarPoints : lidarMesh;
            
            if (activeObject) {
                const positions = activeObject.geometry.attributes.position.array;
                const colors = activeObject.geometry.attributes.color.array;

                let arrayIdx = 0;
                for (let y = 0; y < gridRows; y++) {
                    for (let x = 0; x < gridCols; x++) {
                        let elevation = currentElevations[y * gridCols + x];

                        // Extrude heights
                        positions[arrayIdx + 1] = elevation * zScale - (zScale * 0.3);

                        // Color vertexes to match the colormap selected
                        let itemColors = getLiDARColor(elevation, colormapName);
                        colors[arrayIdx] = itemColors[0] / 255.0;
                        colors[arrayIdx + 1] = itemColors[1] / 255.0;
                        colors[arrayIdx + 2] = itemColors[2] / 255.0;

                        arrayIdx += 3;
                    }
                }

                activeObject.geometry.attributes.position.needsUpdate = true;
                activeObject.geometry.attributes.color.needsUpdate = true;
                
                if (renderStyle !== 'points') {
                    activeObject.geometry.computeVertexNormals();
                }
            }

            // 5. FPS update counter
            frameCount++;
            let now = Date.now();
            if (now - lastFPSUpdateTime >= 1000) {
                scanFPS = Math.round((frameCount * 1000) / (now - lastFPSUpdateTime));
                document.getElementById('fps-counter').innerText = `SCAN RATE: ${scanFPS} FPS`;
                frameCount = 0;
                lastFPSUpdateTime = now;
            }

            // Frame Loop
            controls.update();
            renderer.render(scene, camera);
            animationFrameId = requestAnimationFrame(runVisualProcessing);
        }

        // --- Export & File Download Utils (No external plugins needed) ---
        
        // Export current 3D scanned scene as .obj format
        function exportToOBJ() {
            logToTerminal("Parsing 3D grid spatial topology to OBJ vertices...", "success");
            
            let objData = "# LidarCam 3D Terrain Scanned Mesh File\n";
            objData += "# Generated at: " + new Date().toLocaleString() + "\n";
            
            const activeObject = (renderStyle === 'points') ? lidarPoints : lidarMesh;
            if(!activeObject) return;

            const positions = activeObject.geometry.attributes.position.array;
            const colors = activeObject.geometry.attributes.color.array;

            // Export vertices and vertex colors (supported by modern mesh renderers)
            for (let idx = 0; idx < positions.length; idx += 3) {
                let x = positions[idx].toFixed(3);
                let y = positions[idx + 1].toFixed(3);
                let z = positions[idx + 2].toFixed(3);
                let r = colors[idx].toFixed(3);
                let g = colors[idx + 1].toFixed(3);
                let b = colors[idx + 2].toFixed(3);
                
                objData += `v ${x} ${y} ${z} ${r} ${g} ${b}\n`;
            }

            // Export faces if in mesh/solid view topology
            if (renderStyle !== 'points') {
                const indices = activeObject.geometry.index.array;
                for (let idx = 0; idx < indices.length; idx += 3) {
                    // Obj format indexes starting at 1
                    let f1 = indices[idx] + 1;
                    let f2 = indices[idx + 1] + 1;
                    let f3 = indices[idx + 2] + 1;
                    objData += `f ${f1} ${f2} ${f3}\n`;
                }
            }

            // File Downloader Trigger
            const blob = new Blob([objData], { type: "text/plain" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `lidarcam-3d-scan-${Date.now()}.obj`;
            link.click();
            
            logToTerminal("OBJ 3D Model Download initiated.", "success");
            showNotification("3D Mesh saved successfully!");
        }

        // Export visual Heightmap as static Image
        function exportHeightmapImage() {
            const dataUrl = depthCanvas.toDataURL("image/png");
            const link = document.createElement("a");
            link.href = dataUrl;
            link.download = `lidarcam-heightmap-${Date.now()}.png`;
            link.click();
            logToTerminal("Heightmap PNG exported successfully.", "success");
            showNotification("Heightmap PNG saved!");
        }


        // --- Event Listeners and Button Handlers ---
        
        // Webcam toggle
        document.getElementById('btn-webcam').addEventListener('click', () => {
            initWebcam();
        });

        // Demo scene toggle
        document.getElementById('btn-demo').addEventListener('click', () => {
            activateDemoMode();
        });

        // Camera select change
        cameraSelect.addEventListener('change', (e) => {
            if(e.target.value) {
                initWebcam(e.target.value);
            }
        });

        // Resolution slider
        const resSlider = document.getElementById('resolution');
        resSlider.addEventListener('input', (e) => {
            gridCols = parseInt(e.target.value);
            gridRows = Math.round(gridCols * 0.75); // Maintain visual aspect ratio
            document.getElementById('res-val').innerText = `${gridCols} x ${gridRows} pts`;
            build3DGeometry();
            logToTerminal(`Grid matrix re-allocated to scale: ${gridCols}x${gridRows}`);
        });

        // Z-Scale slider updates HUD display
        document.getElementById('z-scale').addEventListener('input', (e) => {
            document.getElementById('z-scale-val').innerText = e.target.value;
        });

        // Floor slider updates HUD display
        document.getElementById('floor-cutoff').addEventListener('input', (e) => {
            document.getElementById('floor-val').innerText = `${e.target.value}%`;
        });

        // Style selector triggers
        function selectRenderStyle(style) {
            renderStyle = style;
            const btnPoints = document.getElementById('btn-style-points');
            const btnMesh = document.getElementById('btn-style-mesh');
            const btnSolid = document.getElementById('btn-style-solid');

            btnPoints.className = "py-2 px-2 rounded bg-slate-850 text-slate-400 font-bold text-xs flex flex-col items-center gap-1 transition border border-slate-800";
            btnMesh.className = "py-2 px-2 rounded bg-slate-850 text-slate-400 font-bold text-xs flex flex-col items-center gap-1 transition border border-slate-800";
            btnSolid.className = "py-2 px-2 rounded bg-slate-850 text-slate-400 font-bold text-xs flex flex-col items-center gap-1 transition border border-slate-800";

            if (style === 'points') {
                btnPoints.className = "py-2 px-2 rounded bg-purple-500 text-slate-950 font-bold text-xs flex flex-col items-center gap-1 transition glow-purple";
            } else if (style === 'mesh') {
                btnMesh.className = "py-2 px-2 rounded bg-purple-500 text-slate-950 font-bold text-xs flex flex-col items-center gap-1 transition glow-purple";
            } else if (style === 'solid') {
                btnSolid.className = "py-2 px-2 rounded bg-purple-500 text-slate-950 font-bold text-xs flex flex-col items-center gap-1 transition glow-purple";
            }

            build3DGeometry();
            logToTerminal(`3D Scene render topology modified to: ${style.toUpperCase()}`);
        }

        document.getElementById('btn-style-points').addEventListener('click', () => selectRenderStyle('points'));
        document.getElementById('btn-style-mesh').addEventListener('click', () => selectRenderStyle('mesh'));
        document.getElementById('btn-style-solid').addEventListener('click', () => selectRenderStyle('solid'));

        // Reset camera positions
        document.getElementById('btn-reset-cam').addEventListener('click', () => {
            camera.position.set(0, 100, 180);
            controls.target.set(0, 0, 0);
            controls.update();
            logToTerminal("3D Virtual Camera parameters reset.");
        });

        // Freeze frame controller
        document.getElementById('btn-freeze').addEventListener('click', () => {
            isFrozen = !isFrozen;
            const freezeText = document.getElementById('freeze-text');
            const freezeIcon = document.getElementById('freeze-icon');
            const btn = document.getElementById('btn-freeze');

            if (isFrozen) {
                freezeText.innerText = "RESUME SCANS";
                freezeIcon.className = "fa-solid fa-play";
                btn.className = "py-2.5 px-4 bg-green-500 hover:bg-green-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-green";
                logToTerminal("Capture pipelines frozen. Frame buffer preserved.", "success");
            } else {
                freezeText.innerText = "FREEZE FRAME";
                freezeIcon.className = "fa-solid fa-pause";
                btn.className = "py-2.5 px-4 bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-yellow";
                logToTerminal("Capture streams re-activated.", "success");
            }
        });

        // Exporter buttons
        document.getElementById('btn-export-obj').addEventListener('click', exportToOBJ);
        document.getElementById('btn-export-png').addEventListener('click', exportHeightmapImage);


        // --- Initialize Everything ---
        window.onload = function() {
            // Setup visual 3D canvas viewport
            initThree();
            // Connect to camera on boot
            initWebcam();
            // Start parsing frames immediately
            runVisualProcessing();
            logToTerminal("Initialization sequences complete. Radar sweeps active.");
        };

    </script>
</body>
</html>
