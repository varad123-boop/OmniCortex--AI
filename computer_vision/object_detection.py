<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MotionTrack AI - Real-Time Webcam Object Tracker</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Custom UI Glow Styles */
        .glow-cyan {
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        }
        .glow-red {
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
        }
        .glow-green {
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
        }
        .glow-yellow {
            box-shadow: 0 0 15px rgba(234, 179, 8, 0.4);
        }
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <!-- Header Navigation -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex flex-wrap justify-between items-center gap-4">
        <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-lg bg-cyan-500 flex items-center justify-center glow-cyan">
                <i class="fa-solid fa-crosshairs text-slate-950 text-xl animate-pulse"></i>
            </div>
            <div>
                <h1 class="text-xl font-black tracking-wider text-cyan-400">MOTION-TRACK <span class="text-xs font-bold bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">v1.6 LIVE</span></h1>
                <p class="text-xs text-slate-400">Webcam Optical Flow & Color Lock-on Trajectory Painter</p>
            </div>
        </div>
        <div class="flex items-center gap-3">
            <div class="hidden md:flex flex-col text-right font-mono text-[10px] text-slate-500">
                <div>ENGINE: VANILLA JS CANVAS-CV</div>
                <div>LATENCY: <span id="telemetry-latency" class="text-cyan-400">0ms</span></div>
            </div>
            <div class="flex items-center gap-2 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg">
                <span class="flex h-2 w-2 relative">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                <span id="system-status" class="text-xs font-mono text-green-400">STREAMING ACTIVE</span>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <main class="flex-1 grid grid-cols-1 xl:grid-cols-12 gap-6 p-6">
        
        <!-- Left Column: Controls (4 cols) -->
        <div class="xl:col-span-4 flex flex-col gap-6">
            
            <!-- Source & Target Settings -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <i class="fa-solid fa-camera text-cyan-400"></i>
                    <h2 class="text-sm font-bold tracking-wide uppercase">Source & Capture Configuration</h2>
                </div>

                <!-- Source Toggle -->
                <div class="grid grid-cols-2 gap-2">
                    <button id="btn-webcam" class="py-2 px-3 rounded-lg bg-cyan-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-cyan-400 glow-cyan">
                        <i class="fa-solid fa-video"></i> Live Webcam
                    </button>
                    <button id="btn-demo" class="py-2 px-3 rounded-lg bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-700 border border-slate-700">
                        <i class="fa-solid fa-drone"></i> Drone Sim
                    </button>
                </div>

                <!-- Custom Notification / Status -->
                <div id="status-message" class="hidden p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-xs text-cyan-300 flex items-start gap-2">
                    <i class="fa-solid fa-info-circle mt-0.5"></i>
                    <span id="status-text">Ready to track optical movements.</span>
                </div>

                <!-- Camera Select (Dynamic) -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Video Input Device</label>
                    <select id="camera-select" class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 outline-none focus:border-cyan-500">
                        <option value="">Default Webcam</option>
                    </select>
                </div>

                <!-- Active Tracking Algorithm -->
                <div class="flex flex-col gap-1.5">
                    <label class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Tracking Mode</label>
                    <select id="tracking-mode" class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 outline-none focus:border-cyan-500">
                        <option value="color" selected>Chromatic Target Lock (Click to Select Color)</option>
                        <option value="differencing">Frame Differencing (Optical Motion Detection)</option>
                    </select>
                </div>

                <!-- Color Lock-on Preview (Active in Color mode) -->
                <div id="color-lock-container" class="bg-slate-950 border border-slate-800 rounded-xl p-3 flex items-center justify-between">
                    <div class="flex items-center gap-2.5">
                        <div id="color-preview" class="w-8 h-8 rounded-lg border border-slate-700 transition" style="background-color: #06b6d4;"></div>
                        <div>
                            <div class="text-xs font-bold text-slate-300">Target Lock Tint</div>
                            <div id="color-rgb-val" class="text-[10px] text-slate-500 font-mono">RGB: 6, 182, 212</div>
                        </div>
                    </div>
                    <button id="btn-reset-color" class="text-[10px] text-slate-400 bg-slate-900 border border-slate-800 hover:border-slate-700 px-2 py-1.5 rounded-lg transition">
                        Reset Default
                    </button>
                </div>
            </div>

            <!-- Tracker Tuning Sliders -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <i class="fa-solid fa-sliders text-green-400"></i>
                    <h2 class="text-sm font-bold tracking-wide uppercase">Tracker Fine-Tuning</h2>
                </div>

                <!-- Sensitivity Slider -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Sensitivity / Match Tolerance</span>
                        <span id="tolerance-val" class="text-green-400 font-mono">45</span>
                    </div>
                    <input id="tolerance" type="range" min="15" max="120" value="45" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-green-500">
                </div>

                <!-- Search Box Size (Temporal Gating Window) -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Local Search Box Size (Gate Window)</span>
                        <span id="window-val" class="text-green-400 font-mono">160 px</span>
                    </div>
                    <input id="search-window-size" type="range" min="60" max="320" value="160" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-green-500">
                </div>

                <!-- Trail Length Slider -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Vector Trail History Length</span>
                        <span id="trail-val" class="text-green-400 font-mono">60 frames</span>
                    </div>
                    <input id="trail-length" type="range" min="10" max="150" value="60" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-green-500">
                </div>

                <!-- Minimum Blob Size -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-400">Target Noise Threshold (Min Size)</span>
                        <span id="noise-val" class="text-green-400 font-mono">15 pixels</span>
                    </div>
                    <input id="noise-threshold" type="range" min="5" max="100" value="15" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-green-500">
                </div>

                <!-- Toggle Options -->
                <div class="grid grid-cols-2 gap-3 pt-1">
                    <div class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                        <input id="chk-audio" type="checkbox" class="w-4 h-4 rounded text-cyan-500 focus:ring-cyan-500 bg-slate-900 border-slate-700">
                        <div class="flex flex-col">
                            <span class="text-xs font-bold text-slate-300">Audible Alarm</span>
                            <span class="text-[9px] text-slate-500">Sound on target</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                        <input id="chk-grid" type="checkbox" checked class="w-4 h-4 rounded text-cyan-500 focus:ring-cyan-500 bg-slate-900 border-slate-700">
                        <div class="flex flex-col">
                            <span class="text-xs font-bold text-slate-300">Target Grid</span>
                            <span class="text-[9px] text-slate-500">HUD coordinate box</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Live Telemetry Coordinates -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col gap-3 font-mono">
                <div class="flex items-center gap-2 border-b border-slate-800 pb-3 mb-1">
                    <i class="fa-solid fa-gauge-high text-purple-400"></i>
                    <h2 class="text-sm font-bold tracking-wide uppercase font-sans">Active Telemetry</h2>
                </div>

                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="bg-slate-950 border border-slate-800/60 rounded-lg p-2.5 flex flex-col gap-0.5">
                        <span class="text-slate-500 text-[10px]">COORDINATE X:</span>
                        <span id="tel-x" class="text-purple-400 font-bold">N/A</span>
                    </div>
                    <div class="bg-slate-950 border border-slate-800/60 rounded-lg p-2.5 flex flex-col gap-0.5">
                        <span class="text-slate-500 text-[10px]">COORDINATE Y:</span>
                        <span id="tel-y" class="text-purple-400 font-bold">N/A</span>
                    </div>
                    <div class="bg-slate-950 border border-slate-800/60 rounded-lg p-2.5 flex flex-col gap-0.5">
                        <span class="text-slate-500 text-[10px]">TARGET SPEED:</span>
                        <span id="tel-speed" class="text-green-400 font-bold">0.0 px/f</span>
                    </div>
                    <div class="bg-slate-950 border border-slate-800/60 rounded-lg p-2.5 flex flex-col gap-0.5">
                        <span class="text-slate-500 text-[10px]">HEADING VECT:</span>
                        <span id="tel-heading" class="text-blue-400 font-bold">STATIONARY</span>
                    </div>
                </div>

                <div class="bg-slate-950 border border-slate-800 rounded-xl p-3 flex flex-col gap-2">
                    <div class="flex justify-between text-xs">
                        <span class="text-slate-500">Active Motion Magnitude:</span>
                        <span id="tel-magnitude-text" class="text-cyan-400 font-bold">0.0%</span>
                    </div>
                    <div class="w-full bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-800">
                        <div id="tel-magnitude-bar" class="bg-cyan-500 h-full transition-all duration-75" style="width: 0%"></div>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Column: Visualizer Viewport (8 cols) -->
        <div class="xl:col-span-8 flex flex-col gap-6">
            
            <!-- Video Input & Tracking Overlay -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col gap-3 relative min-h-[400px]">
                <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                    <div class="flex items-center gap-2">
                        <span class="h-2.5 w-2.5 rounded-full bg-red-500 animate-pulse"></span>
                        <span class="text-xs font-bold tracking-wider uppercase text-slate-300" id="video-feed-label">Live Visual Tracking Feed</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] font-mono text-slate-500" id="fps-counter">PROCS RATE: 0 FPS</span>
                    </div>
                </div>

                <!-- Hidden video tag used for webcam buffer source -->
                <video id="webcam-video" autoplay playsinline muted class="hidden"></video>

                <!-- Processing Canvas Stack -->
                <div class="relative flex-1 bg-slate-950 rounded-xl overflow-hidden flex items-center justify-center border border-slate-950 group">
                    
                    <!-- Core Canvas layer -->
                    <canvas id="canvas-tracker" class="w-full h-auto max-h-[500px] object-contain rounded-xl cursor-crosshair"></canvas>
                    
                    <!-- Dynamic Reticle Hover Tip (Click anywhere to track) -->
                    <div class="absolute top-3 left-3 bg-slate-950/80 backdrop-blur border border-slate-800 rounded px-2.5 py-1.5 text-[10px] text-cyan-400 pointer-events-none tracking-wide select-none">
                        <i class="fa-solid fa-circle-dot mr-1 text-cyan-400 animate-ping"></i> TIP: CLICK TARGET OBJECT ON FEED TO LOCK-ON
                    </div>

                    <!-- Target Status Floating HUD -->
                    <div class="absolute bottom-3 right-3 bg-slate-950/80 backdrop-blur border border-slate-800 rounded p-2 text-[10px] font-mono text-cyan-400 flex flex-col gap-0.5 select-none pointer-events-none">
                        <div>LOCK: <span id="hud-lock" class="text-slate-500 font-bold">DISENGAGED</span></div>
                        <div>GRID: <span id="hud-grid-status" class="text-cyan-400">READY</span></div>
                    </div>
                </div>
            </div>

            <!-- Lower Action Station & Data Exporter -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-wrap justify-between items-center gap-4">
                <div class="flex flex-col gap-1">
                    <h3 class="text-sm font-bold text-slate-200">Motion Log & Export Center</h3>
                    <p class="text-xs text-slate-400">Download captured lock coordinates or reset active target sweeps.</p>
                </div>
                
                <div class="flex flex-wrap gap-3">
                    <button id="btn-freeze" class="py-2.5 px-4 bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-yellow">
                        <i id="freeze-icon" class="fa-solid fa-pause"></i> 
                        <span id="freeze-text">FREEZE FRAME</span>
                    </button>
                    <button id="btn-clear-trail" class="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-black text-xs rounded-xl flex items-center gap-2 transition">
                        <i class="fa-solid fa-eraser"></i> CLEAR TRAILS
                    </button>
                    <button id="btn-export-csv" class="py-2.5 px-4 bg-cyan-600 hover:bg-cyan-500 text-white font-black text-xs rounded-xl flex items-center gap-2 transition glow-cyan">
                        <i class="fa-solid fa-file-csv"></i> EXPORT COORDINATE PATH
                    </button>
                    <button id="btn-export-png" class="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-black text-xs rounded-xl flex items-center gap-2 transition">
                        <i class="fa-solid fa-image"></i> SNAPSHOT FRAME
                    </button>
                </div>
            </div>

            <!-- Custom Message Console Log -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-2">
                    <div class="flex items-center gap-2 text-xs text-slate-400 uppercase font-mono">
                        <i class="fa-solid fa-terminal text-cyan-400 animate-pulse"></i> TRACKER DIAGNOSTIC FEED
                    </div>
                    <span class="text-[9px] text-slate-600 font-mono">CONSOLE OUT</span>
                </div>
                <div id="terminal-out" class="font-mono text-[11px] text-cyan-500/90 h-24 overflow-y-auto flex flex-col gap-1 pr-2">
                    <div>[SYS] Initializing MotionTrack AI Kernels... Done.</div>
                    <div>[SYS] Webcam interface checking... Standby.</div>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-slate-500 mt-auto">
        <div>&copy; 2026 MotionTrack AI. Computer Vision & Motion Vector Mapping Suite.</div>
        <div class="flex items-center gap-4">
            <span class="hover:text-slate-400 cursor-pointer transition">Diagnostic Logs</span>
            <span class="hover:text-slate-400 cursor-pointer transition">Coordinate Matrix WGS-84</span>
        </div>
    </footer>

    <!-- App Scripts -->
    <script>
        // --- Web Audio Synthesizer for Digital Telemetry Alert Sound ---
        let audioCtx = null;
        function playTelemetryChirp(pitch = 900, duration = 0.08) {
            if (!document.getElementById('chk-audio').checked) return;
            try {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(pitch, audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration + 0.01);
            } catch (err) {
                console.warn("Audio feedback initialization blocked by browser.");
            }
        }

        // --- Console Terminal Logger ---
        const terminal = document.getElementById('terminal-out');
        function logToTerminal(message, type = 'sys') {
            const time = new Date().toLocaleTimeString();
            const div = document.createElement('div');
            let colorClass = 'text-cyan-500/90';
            if (type === 'err') colorClass = 'text-red-400';
            if (type === 'success') colorClass = 'text-green-400';
            if (type === 'lock') colorClass = 'text-purple-400';
            div.className = colorClass;
            div.innerHTML = `<span class="text-slate-600">[${time}]</span> [${type.toUpperCase()}] ${message}`;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        // --- Custom Interactive Message HUD Alert ---
        function showNotification(text, duration = 3000) {
            const box = document.getElementById('status-message');
            const boxText = document.getElementById('status-text');
            box.classList.remove('hidden');
            boxText.innerText = text;
            setTimeout(() => {
                box.classList.add('hidden');
            }, duration);
        }

        // --- Global Application States ---
        let isWebcam = true;
        let isFrozen = false;
        let lastFrameData = null;
        let trackingMode = 'color'; // 'color' or 'differencing'
        
        // Color lock coordinates state (Defaults to a vivid Cyan-Blue tint)
        let targetColor = { r: 6, g: 182, b: 212 };
        let hasLockedColor = false;
        let lastTargetCoords = null; // Stores {x, y} to maintain localized search window

        // Path Trajectory Data Arrays
        let pathTrajectory = []; // Array of {x, y, timestamp}
        let trackingStatistics = {
            totalPointsLogged: 0,
            activeMagnitude: 0,
            speed: 0,
            heading: 'STATIONARY'
        };

        // Drone simulation states
        let droneSim = {
            x: 100,
            y: 100,
            targetX: 320,
            targetY: 240,
            angle: 0,
            color: { r: 239, g: 68, b: 68 }, // Bright red simulated balloon/drone
            size: 25
        };

        // Framerate Benchmarking
        let procsFPS = 0;
        let frameCount = 0;
        let lastFPSUpdateTime = Date.now();
        let trackerLoopId = null;

        // Canvas Layers
        const mainCanvas = document.getElementById('canvas-tracker');
        const mainCtx = mainCanvas.getContext('2d', { willReadFrequently: true });
        const videoElement = document.getElementById('webcam-video');

        // Setup canvas internal buffer dimensions
        const bufferWidth = 640;
        const bufferHeight = 480;
        mainCanvas.width = bufferWidth;
        mainCanvas.height = bufferHeight;

        // Initialize Live Webcam
        let webcamStream = null;
        async function initWebcam(deviceId = null) {
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
            }

            const constraints = {
                audio: false,
                video: deviceId ? { deviceId: { exact: deviceId }, width: bufferWidth, height: bufferHeight } : { width: bufferWidth, height: bufferHeight }
            };

            try {
                webcamStream = await navigator.mediaDevices.getUserMedia(constraints);
                videoElement.srcObject = webcamStream;
                videoElement.play();
                isWebcam = true;
                
                document.getElementById('btn-webcam').className = "py-2 px-3 rounded-lg bg-cyan-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-cyan-400 glow-cyan";
                document.getElementById('btn-demo').className = "py-2 px-3 rounded-lg bg-slate-950 text-slate-400 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-900 border border-slate-800";
                document.getElementById('video-feed-label').innerText = "LIVE WEBCAM SCANNED VIEWPORT";
                logToTerminal("Dynamic video source loaded. Initializing optical pipeline.", "success");
                
                populateDevices();
            } catch (err) {
                logToTerminal("Webcam access declined or unavailable. Activating target tracker drone simulation.", "err");
                showNotification("Could not start Webcam. Switching to Drone Simulation!");
                activateDemoMode();
            }
        }

        async function populateDevices() {
            try {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(d => d.kind === 'videoinput');
                const cameraSelect = document.getElementById('camera-select');
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
            document.getElementById('btn-demo').className = "py-2 px-3 rounded-lg bg-cyan-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-cyan-400 glow-cyan";
            document.getElementById('btn-webcam').className = "py-2 px-3 rounded-lg bg-slate-950 text-slate-400 font-bold text-xs flex items-center justify-center gap-2 transition hover:bg-slate-900 border border-slate-800";
            document.getElementById('video-feed-label').innerText = "DRONE FLIGHT TARGET TRACKER SIMULATION";
            logToTerminal("Autonomous target simulation launched. Drone trajectory unlocked.", "success");
        }

        // --- Core Computer Vision (CV) Tracking Loop ---
        function runTrackingEngine() {
            if (isFrozen) {
                trackerLoopId = requestAnimationFrame(runTrackingEngine);
                return;
            }

            let startTime = performance.now();

            // Clear buffer layer
            mainCtx.clearRect(0, 0, bufferWidth, bufferHeight);

            // Fetch dynamic tuning sliders
            const tolerance = parseInt(document.getElementById('tolerance').value);
            const noiseLimit = parseInt(document.getElementById('noise-threshold').value);
            const maxTrail = parseInt(document.getElementById('trail-length').value);
            const isGridEnabled = document.getElementById('chk-grid').checked;
            const searchBoxSize = parseInt(document.getElementById('search-window-size').value);

            // Step 1: Draw the background source
            if (isWebcam && videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
                // Mirror webcam view organically for intuitive interaction
                mainCtx.save();
                mainCtx.translate(bufferWidth, 0);
                mainCtx.scale(-1, 1);
                mainCtx.drawImage(videoElement, 0, 0, bufferWidth, bufferHeight);
                mainCtx.restore();
            } else {
                // Update Drone Simulation coordinates
                updateDronePhysics();
                // Draw Synthetic tracking space
                drawDroneSimulationSpace();
            }

            // Grab current frame buffer pixels
            let frameImageData = mainCtx.getImageData(0, 0, bufferWidth, bufferHeight);
            let pixels = frameImageData.data;

            // Coordinates accumulator for tracking centroid
            let sumX = 0;
            let sumY = 0;
            let matchCount = 0;

            // --- ALGORITHM MODE 1: Chromatic Target Lock-on (UPDATED WITH LOCALIZED WINDOW GATING) ---
            if (trackingMode === 'color') {
                // Define search boundaries based on last known position (if locked)
                let useLocalGate = lastTargetCoords !== null;
                let minX = 0, maxX = bufferWidth;
                let minY = 0, maxY = bufferHeight;

                if (useLocalGate) {
                    minX = Math.max(0, lastTargetCoords.x - searchBoxSize / 2);
                    maxX = Math.min(bufferWidth, lastTargetCoords.x + searchBoxSize / 2);
                    minY = Math.max(0, lastTargetCoords.y - searchBoxSize / 2);
                    maxY = Math.min(bufferHeight, lastTargetCoords.y + searchBoxSize / 2);
                }

                for (let y = minY; y < maxY; y++) {
                    for (let x = minX; x < maxX; x++) {
                        let i = (y * bufferWidth + x) * 4;
                        let r = pixels[i];
                        let g = pixels[i + 1];
                        let b = pixels[i + 2];

                        // Euclidean color difference metric
                        let rDiff = r - targetColor.r;
                        let gDiff = g - targetColor.g;
                        let bDiff = b - targetColor.b;
                        let dist = Math.sqrt(rDiff*rDiff + gDiff*gDiff + bDiff*bDiff);

                        if (dist < tolerance) {
                            sumX += x;
                            sumY += y;
                            matchCount++;

                            // Highlight matching colors
                            if (matchCount % 12 === 0) {
                                pixels[i] = 6;
                                pixels[i + 1] = 182;
                                pixels[i + 2] = 212;
                            }
                        }
                    }
                }

                // If locked but no points matched in localized window, enter full-screen re-acquisition
                if (useLocalGate && matchCount <= noiseLimit) {
                    lastTargetCoords = null; // Lose local gate to fallback to global scan next frame
                }
            } 
            // --- ALGORITHM MODE 2: Frame Differencing (Optical Motion Detection) ---
            else if (trackingMode === 'differencing') {
                if (lastFrameData) {
                    let activeMotionCount = 0;
                    for (let i = 0; i < pixels.length; i += 4) {
                        let r = pixels[i];
                        let g = pixels[i+1];
                        let b = pixels[i+2];

                        let lr = lastFrameData.data[i];
                        let lg = lastFrameData.data[i+1];
                        let lb = lastFrameData.data[i+2];

                        // Absolute luminance variance
                        let delta = Math.abs(r - lr) + Math.abs(g - lg) + Math.abs(b - lb);

                        // If variance exceeds threshold, we found active movement!
                        if (delta > tolerance * 1.5) {
                            let idx = i / 4;
                            let pxX = idx % bufferWidth;
                            let pxY = Math.floor(idx / bufferWidth);

                            sumX += pxX;
                            sumY += pxY;
                            matchCount++;
                            activeMotionCount++;

                            // Highlight motion points on screen with high-vis laser green
                            pixels[i] = 34;
                            pixels[i+1] = 197;
                            pixels[i+2] = 94;
                        }
                    }
                    // Calculate relative amount of movement inside view box
                    trackingStatistics.activeMagnitude = (activeMotionCount / (bufferWidth * bufferHeight)) * 100;
                }
                // Save current frame for comparison during next cycle
                lastFrameData = frameImageData;
            }

            // Repaint customized pixels matching target criteria
            mainCtx.putImageData(frameImageData, 0, 0);

            // Calculate Target Coordinates & Locks
            let isTargetAcquired = matchCount > noiseLimit;
            let hudLockSpan = document.getElementById('hud-lock');

            if (isTargetAcquired) {
                // Calculate Average Coordinates (Centroid center point of target blob)
                let targetX = Math.round(sumX / matchCount);
                let targetY = Math.round(sumY / matchCount);

                // Update last known target location
                lastTargetCoords = { x: targetX, y: targetY };

                // Add lock coords to track vectors
                pathTrajectory.push({ x: targetX, y: targetY, time: Date.now() });
                if (pathTrajectory.length > maxTrail) {
                    pathTrajectory.shift();
                }

                // Smooth out Speed Metric
                if (pathTrajectory.length > 2) {
                    let p1 = pathTrajectory[pathTrajectory.length - 2];
                    let p2 = pathTrajectory[pathTrajectory.length - 1];
                    let d = Math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2);
                    trackingStatistics.speed = (trackingStatistics.speed * 0.8) + (d * 0.2); // Low pass filter
                    
                    // Determine travelling heading/direction
                    let dx = p2.x - p1.x;
                    let dy = p2.y - p1.y;
                    if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
                        let angle = Math.atan2(dy, dx) * 180 / Math.PI;
                        if (angle >= -22.5 && angle < 22.5) trackingStatistics.heading = "EAST \u279E";
                        else if (angle >= 22.5 && angle < 67.5) trackingStatistics.heading = "SOUTHEAST \u2198";
                        else if (angle >= 67.5 && angle < 112.5) trackingStatistics.heading = "SOUTH \u2193";
                        else if (angle >= 112.5 && angle < 157.5) trackingStatistics.heading = "SOUTHWEST \u2199";
                        else if (angle >= 157.5 || angle < -157.5) trackingStatistics.heading = "WEST \u219C";
                        else if (angle >= -157.5 && angle < -112.5) trackingStatistics.heading = "NORTHWEST \u2196";
                        else if (angle >= -112.5 && angle < -67.5) trackingStatistics.heading = "NORTH \u2191";
                        else trackingStatistics.heading = "NORTHEAST \u2197";
                    } else {
                        trackingStatistics.heading = "STATIONARY";
                    }
                }

                // Update Lock Telemetry HTML Displays
                document.getElementById('tel-x').innerText = `${targetX}px`;
                document.getElementById('tel-y').innerText = `${targetY}px`;
                document.getElementById('tel-speed').innerText = `${trackingStatistics.speed.toFixed(1)} px/f`;
                document.getElementById('tel-heading').innerText = trackingStatistics.heading;

                // Adjust Lock Status Class
                hudLockSpan.innerText = "LOCKED";
                hudLockSpan.className = "text-green-400 font-black animate-pulse";

                // Draw high-tech targeted bounding crosshair on target
                drawTargetLockCrosshair(targetX, targetY);

                // Draw local search box boundaries (Visual SLAM Gate feedback)
                if (trackingMode === 'color') {
                    drawSearchBoxGate(targetX, targetY, searchBoxSize);
                }

                // Play faint lock tone if alarm checked
                if (Math.round(trackingStatistics.speed) > 12) {
                    playTelemetryChirp(700 + Math.min(300, targetY), 0.05);
                }

                trackingStatistics.totalPointsLogged++;
            } else {
                // Decay target status
                hudLockSpan.innerText = "DISENGAGED";
                hudLockSpan.className = "text-slate-500 font-bold";
                document.getElementById('tel-heading').innerText = "STATIONARY";
                document.getElementById('tel-speed').innerText = "0.0 px/f";
                lastTargetCoords = null; // Clear tracking lock position
            }

            // Display grid/sectors overlay lines (resembling tactical radar HUD overlays)
            if (isGridEnabled) {
                drawSectorsGridOverlay();
            }

            // Draw beautiful vector trace lines showing object path history
            drawTrajectoryTrail();

            // Render live Motion Graph indicators
            if (trackingMode === 'differencing') {
                document.getElementById('tel-magnitude-text').innerText = `${trackingStatistics.activeMagnitude.toFixed(1)}%`;
                document.getElementById('tel-magnitude-bar').style.width = `${Math.min(100, trackingStatistics.activeMagnitude * 4)}%`;
            } else {
                // In color lock, render fullness of lock pixels matches
                let matchRatio = Math.min(100, (matchCount / (bufferWidth * bufferHeight)) * 250);
                document.getElementById('tel-magnitude-text').innerText = `${matchRatio.toFixed(1)}%`;
                document.getElementById('tel-magnitude-bar').style.width = `${matchRatio}%`;
            }

            // Benchmarking loops
            let latencyTime = Math.round(performance.now() - startTime);
            document.getElementById('telemetry-latency').innerText = `${latencyTime}ms`;

            frameCount++;
            let now = Date.now();
            if (now - lastFPSUpdateTime >= 1000) {
                procsFPS = Math.round((frameCount * 1000) / (now - lastFPSUpdateTime));
                document.getElementById('fps-counter').innerText = `PROCS RATE: ${procsFPS} FPS`;
                frameCount = 0;
                lastFPSUpdateTime = now;
            }

            trackerLoopId = requestAnimationFrame(runTrackingEngine);
        }

        // --- Drone Simulation Engine (Mathematical Sandbox) ---
        function updateDronePhysics() {
            droneSim.angle += 0.035;
            
            // Generate elegant compound orbit motions (lissajous shapes representing balloon drift)
            droneSim.x = bufferWidth / 2 + Math.cos(droneSim.angle) * 190 + Math.sin(droneSim.angle * 1.8) * 35;
            droneSim.y = bufferHeight / 2 + Math.sin(droneSim.angle * 1.2) * 120 + Math.cos(droneSim.angle * 0.5) * 20;

            // Bound checking
            droneSim.x = Math.max(20, Math.min(bufferWidth - 20, droneSim.x));
            droneSim.y = Math.max(20, Math.min(bufferHeight - 20, droneSim.y));
        }

        function drawDroneSimulationSpace() {
            // Draw clean space grid
            mainCtx.fillStyle = "#020617";
            mainCtx.fillRect(0, 0, bufferWidth, bufferHeight);

            // Draw cyber scanning light source
            let gradient = mainCtx.createRadialGradient(droneSim.x, droneSim.y, 2, droneSim.x, droneSim.y, 90);
            gradient.addColorStop(0, "rgba(6, 182, 212, 0.15)");
            gradient.addColorStop(1, "rgba(6, 182, 212, 0)");
            mainCtx.fillStyle = gradient;
            mainCtx.beginPath();
            mainCtx.arc(droneSim.x, droneSim.y, 90, 0, Math.PI * 2);
            mainCtx.fill();

            // Draw simulated physical drone body (Red sphere target)
            mainCtx.fillStyle = `rgb(${droneSim.color.r}, ${droneSim.color.g}, ${droneSim.color.b})`;
            mainCtx.beginPath();
            mainCtx.arc(droneSim.x, droneSim.y, droneSim.size, 0, Math.PI * 2);
            mainCtx.fill();

            // Small glowing drone indicators
            mainCtx.strokeStyle = "#ffffff";
            mainCtx.lineWidth = 2;
            mainCtx.beginPath();
            mainCtx.arc(droneSim.x, droneSim.y, droneSim.size + 4, 0, Math.PI * 2);
            mainCtx.stroke();

            // Propellers details
            mainCtx.fillStyle = "#e2e8f0";
            mainCtx.font = "bold 9px monospace";
            mainCtx.fillText("M-1", droneSim.x - 12, droneSim.y - 10);
            mainCtx.fillText("M-2", droneSim.x + 3, droneSim.y + 12);
        }

        // --- Reticle & Coordinate Painting functions ---
        
        // Draw Sector overlays
        function drawSectorsGridOverlay() {
            mainCtx.strokeStyle = "rgba(6, 182, 212, 0.08)";
            mainCtx.lineWidth = 1;
            
            // Grid lines
            mainCtx.beginPath();
            // Vertical divisions
            mainCtx.moveTo(bufferWidth / 3, 0); mainCtx.lineTo(bufferWidth / 3, bufferHeight);
            mainCtx.moveTo((bufferWidth / 3) * 2, 0); mainCtx.lineTo((bufferWidth / 3) * 2, bufferHeight);
            // Horizontal divisions
            mainCtx.moveTo(0, bufferHeight / 3); mainCtx.lineTo(bufferWidth, bufferHeight / 3);
            mainCtx.moveTo(0, (bufferHeight / 3) * 2); mainCtx.lineTo(bufferWidth, (bufferHeight / 3) * 2);
            mainCtx.stroke();

            // Center targeting reticle ticks
            mainCtx.strokeStyle = "rgba(6, 182, 212, 0.25)";
            mainCtx.beginPath();
            mainCtx.arc(bufferWidth / 2, bufferHeight / 2, 8, 0, Math.PI * 2);
            mainCtx.stroke();
        }

        // Target Lock circle crosshair with rotating brackets
        function drawTargetLockCrosshair(tx, ty) {
            let colorHex = trackingMode === 'color' ? "#06b6d4" : "#22c55e";
            mainCtx.strokeStyle = colorHex;
            mainCtx.lineWidth = 2.5;

            // Dynamic rotating brackets based on clock
            let rAngle = (Date.now() / 320) % (Math.PI * 2);

            mainCtx.save();
            mainCtx.translate(tx, ty);
            mainCtx.rotate(rAngle);

            // Bounding target brackets
            mainCtx.beginPath();
            mainCtx.arc(0, 0, 22, 0, Math.PI / 2);
            mainCtx.stroke();
            mainCtx.beginPath();
            mainCtx.arc(0, 0, 22, Math.PI, Math.PI * 1.5);
            mainCtx.stroke();
            mainCtx.restore();

            // Horizontal & Vertical intersecting lines
            mainCtx.strokeStyle = "rgba(255, 255, 255, 0.4)";
            mainCtx.lineWidth = 1;
            mainCtx.beginPath();
            mainCtx.moveTo(tx - 35, ty); mainCtx.lineTo(tx + 35, ty);
            mainCtx.moveTo(tx, ty - 35); mainCtx.lineTo(tx, ty + 35);
            mainCtx.stroke();

            // Center lock-on coordinate tag
            mainCtx.fillStyle = colorHex;
            mainCtx.font = "bold 9px monospace";
            mainCtx.fillText(`LOCK: [${tx}, ${ty}]`, tx + 28, ty - 12);
        }

        // Draw Search Box Gate
        function drawSearchBoxGate(tx, ty, size) {
            mainCtx.strokeStyle = "#eab308"; // Vivid yellow search window box
            mainCtx.lineWidth = 1.2;
            mainCtx.setLineDash([4, 4]); // Dashed sci-fi looking box
            mainCtx.strokeRect(tx - size / 2, ty - size / 2, size, size);
            mainCtx.setLineDash([]); // Reset line dash

            mainCtx.fillStyle = "#eab308";
            mainCtx.font = "9px monospace";
            mainCtx.fillText("GATE WINDOW", tx - size / 2 + 4, ty - size / 2 + 12);
        }

        // Beautiful path history vector drawing
        function drawTrajectoryTrail() {
            if (pathTrajectory.length < 2) return;

            let colorHex = trackingMode === 'color' ? "6, 182, 212" : "34, 197, 94";

            for (let i = 1; i < pathTrajectory.length; i++) {
                let p1 = pathTrajectory[i - 1];
                let p2 = pathTrajectory[i];

                // Calculate opacity fade based on age of path points
                let opacity = i / pathTrajectory.length;

                mainCtx.strokeStyle = `rgba(${colorHex}, ${opacity})`;
                mainCtx.lineWidth = 3 + (opacity * 3.5); // Older parts are thinner
                mainCtx.beginPath();
                mainCtx.moveTo(p1.x, p1.y);
                mainCtx.lineTo(p2.x, p2.y);
                mainCtx.stroke();
            }
        }

        // --- Object color selection trigger by clicking video feed (UPDATED WITH PATERN SAMPLING) ---
        mainCanvas.addEventListener('mousedown', (e) => {
            // Get mouse click coords scaled perfectly to internal coordinates buffer
            const rect = mainCanvas.getBoundingClientRect();
            const clickX = Math.round(((e.clientX - rect.left) / rect.width) * bufferWidth);
            const clickY = Math.round(((e.clientY - rect.top) / rect.height) * bufferHeight);

            // Fetch average color surrounding cursor to bypass camera grain
            try {
                let rSum = 0, gSum = 0, bSum = 0, samples = 0;
                let sampleRadius = 3; // Grabs a 7x7 pixel grid cluster

                for (let dy = -sampleRadius; dy <= sampleRadius; dy++) {
                    for (let dx = -sampleRadius; dx <= sampleRadius; dx++) {
                        let sampleX = clickX + dx;
                        let sampleY = clickY + dy;

                        if (sampleX >= 0 && sampleX < bufferWidth && sampleY >= 0 && sampleY < bufferHeight) {
                            let frameData = mainCtx.getImageData(sampleX, sampleY, 1, 1);
                            rSum += frameData.data[0];
                            gSum += frameData.data[1];
                            bSum += frameData.data[2];
                            samples++;
                        }
                    }
                }

                let r = Math.round(rSum / samples);
                let g = Math.round(gSum / samples);
                let b = Math.round(bSum / samples);

                targetColor = { r, g, b };
                hasLockedColor = true;
                lastTargetCoords = { x: clickX, y: clickY }; // Instantly assign initial lock location

                // Update visual preview box elements
                document.getElementById('color-preview').style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
                document.getElementById('color-rgb-val').innerText = `RGB: ${r}, ${g}, ${b}`;
                
                logToTerminal(`Target locked with neighborhood smoothing: RGB [${r}, ${g}, ${b}] at coordinate [${clickX}px, ${clickY}px]`, "lock");
                showNotification("Target Lock RGB updated!");
                playTelemetryChirp(1100, 0.15);
            } catch (err) {
                console.warn("Unable to extract pixel details from canvas bounds.");
            }
        });


        // --- UI Controllers & Interactive Handlers ---

        // Switch to Webcam Input source
        document.getElementById('btn-webcam').addEventListener('click', () => {
            initWebcam();
        });

        // Switch to synthetic Drone flight source
        document.getElementById('btn-demo').addEventListener('click', () => {
            activateDemoMode();
        });

        // Toggle tracking system algorithms
        document.getElementById('tracking-mode').addEventListener('change', (e) => {
            trackingMode = e.target.value;
            const container = document.getElementById('color-lock-container');
            
            if (trackingMode === 'color') {
                container.classList.remove('opacity-40', 'pointer-events-none');
                logToTerminal("Switched algorithm to target color tracking sweep.", "sys");
            } else {
                container.classList.add('opacity-40', 'pointer-events-none');
                logToTerminal("Switched algorithm to optical movement differencing.", "sys");
            }
            // Flush trails and locks
            pathTrajectory = [];
            lastTargetCoords = null;
        });

        // Reset default locked color (vivid tracking cyan)
        document.getElementById('btn-reset-color').addEventListener('click', () => {
            targetColor = { r: 6, g: 182, b: 212 };
            document.getElementById('color-preview').style.backgroundColor = "rgb(6, 182, 212)";
            document.getElementById('color-rgb-val').innerText = "RGB: 6, 182, 212";
            lastTargetCoords = null;
            logToTerminal("Restored target lock color template to factory defaults.", "sys");
        });

        // Slider real-time updates HUD labels
        document.getElementById('tolerance').addEventListener('input', (e) => {
            document.getElementById('tolerance-val').innerText = e.target.value;
        });

        document.getElementById('search-window-size').addEventListener('input', (e) => {
            document.getElementById('window-val').innerText = `${e.target.value} px`;
        });

        document.getElementById('trail-length').addEventListener('input', (e) => {
            document.getElementById('trail-val').innerText = `${e.target.value} frames`;
        });

        document.getElementById('noise-threshold').addEventListener('input', (e) => {
            document.getElementById('noise-val').innerText = `${e.target.value} pixels`;
        });

        // Clear active trail vectors
        document.getElementById('btn-clear-trail').addEventListener('click', () => {
            pathTrajectory = [];
            lastTargetCoords = null;
            logToTerminal("Cleaned spatial coordinate path trail histories.", "sys");
            showNotification("Visual trails cleared!");
        });

        // Freeze controller
        document.getElementById('btn-freeze').addEventListener('click', () => {
            isFrozen = !isFrozen;
            const text = document.getElementById('freeze-text');
            const icon = document.getElementById('freeze-icon');
            const btn = document.getElementById('btn-freeze');

            if (isFrozen) {
                text.innerText = "RESUME SYSTEM";
                icon.className = "fa-solid fa-play";
                btn.className = "py-2.5 px-4 bg-green-500 hover:bg-green-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-green";
                logToTerminal("Telemetry frame extraction pipelines paused.", "sys");
            } else {
                text.innerText = "FREEZE FRAME";
                icon.className = "fa-solid fa-pause";
                btn.className = "py-2.5 px-4 bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-2 transition glow-yellow";
                logToTerminal("Scanning pipelines restarted.", "sys");
            }
        });

        // Export tracked path coordinates directly as structured CSV
        document.getElementById('btn-export-csv').addEventListener('click', () => {
            if (pathTrajectory.length === 0) {
                logToTerminal("Cannot export empty path trail database.", "err");
                showNotification("No tracked coordinates recorded yet!");
                return;
            }

            logToTerminal("Formatting tracking trail log database as CSV...", "success");
            
            let csvData = "Frame_Index,Timestamp_Epoch_ms,Coordinate_X,Coordinate_Y\n";
            pathTrajectory.forEach((point, index) => {
                csvData += `${index},${point.time},${point.x},${point.y}\n`;
            });

            // Trigger safe web file downloader
            const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", `motiontrack-trajectory-${Date.now()}.csv`);
            link.click();
            
            logToTerminal("CSV telemetry export delivered successfully.", "success");
            showNotification("CSV path data exported!");
        });

        // Snapshot PNG image heightmap
        document.getElementById('btn-export-png').addEventListener('click', () => {
            const dataUrl = mainCanvas.toDataURL("image/png");
            const link = document.createElement("a");
            link.href = dataUrl;
            link.download = `motiontrack-snapshot-${Date.now()}.png`;
            link.click();
            logToTerminal("Visual HUD frame snapshot captured successfully.", "success");
            showNotification("Snapshot PNG exported!");
        });

        // Dynamic Camera select dropdown
        const cameraSelect = document.getElementById('camera-select');
        cameraSelect.addEventListener('change', (e) => {
            if(e.target.value) {
                initWebcam(e.target.value);
            }
        });

        // --- Initialize Engine ---
        window.onload = function() {
            // Trigger camera
            initWebcam();
            // Fire tracking processing loop
            runTrackingEngine();
        };

    </script>
</body>
</html>
