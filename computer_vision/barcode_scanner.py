<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Industrial QR Code Scanner & Tracker</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- jsQR Library for High Performance QR Scanning -->
    <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        industrial: {
                            50: '#fffbeb',
                            100: '#fef3c7',
                            500: '#f59e0b',
                            600: '#d97706',
                            900: '#78350f',
                            950: '#451a03'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        /* Custom scanline animation for the camera view */
        @keyframes scan {
            0% { top: 0%; }
            50% { top: 100%; }
            100% { top: 0%; }
        }
        .scanline {
            animation: scan 4s linear infinite;
        }
        /* Custom scrollbar */
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
    </style>
</head>
<body class="h-full flex flex-col font-sans overflow-x-hidden antialiased">

    <!-- Top Navigation Bar -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-4 py-3">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-3">
            <div class="flex items-center gap-3">
                <div class="bg-amber-500 text-slate-950 p-2 rounded-lg font-black tracking-wider shadow-lg shadow-amber-500/10">
                    <i data-lucide="qr-code" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight flex items-center gap-2">
                        SCAN-PRO <span class="text-xs bg-amber-500/20 text-amber-400 px-2 py-0.5 rounded border border-amber-500/30 font-mono">v3.1</span>
                    </h1>
                    <p class="text-xs text-slate-400">Industrial Automated QR Scanner with Deep Scan</p>
                </div>
            </div>
            <div class="flex items-center gap-4 text-xs font-mono">
                <div class="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-md border border-slate-800">
                    <span id="status-dot" class="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></span>
                    <span id="status-text" class="text-slate-300">Camera Offline</span>
                </div>
                <div class="hidden md:flex items-center gap-2 text-slate-400">
                    <i data-lucide="clock" class="w-4 h-4"></i>
                    <span id="current-time">--:--:--</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-y-auto">
        
        <!-- Left Column: Camera View & Controls (7 Cols) -->
        <div class="lg:col-span-7 flex flex-col gap-4">
            
            <!-- Camera Feed Card -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl relative flex flex-col">
                <!-- Card Header -->
                <div class="px-4 py-3 bg-slate-950/60 border-b border-slate-800/80 flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <i data-lucide="aperture" class="w-4 h-4 text-amber-500 animate-spin" style="animation-duration: 8s;"></i>
                        <span class="text-sm font-semibold text-slate-200">Live Acquisition Matrix</span>
                    </div>
                    <div class="flex items-center gap-3">
                        <span id="fps-counter" class="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-400">FPS: --</span>
                        <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
                    </div>
                </div>

                <!-- Video Viewport Container -->
                <div class="relative bg-black aspect-video flex items-center justify-center overflow-hidden group">
                    <!-- Hidden video element that streams the web camera -->
                    <video id="video-feed" playsinline class="hidden"></video>
                    
                    <!-- Main canvas for drawing video frame + real-time QR overlays -->
                    <canvas id="display-canvas" class="w-full h-full object-contain"></canvas>

                    <!-- Scan overlay element -->
                    <div id="scan-laser" class="absolute left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-emerald-500 to-transparent shadow-lg shadow-emerald-500/50 pointer-events-none scanline opacity-70"></div>

                    <!-- Target Focus Area for Deep Scan (always visible when Deep Scan is active) -->
                    <div id="deep-scan-zone" class="absolute border-2 border-dashed border-amber-500/40 w-48 h-48 pointer-events-none rounded-lg flex items-center justify-center opacity-0 transition-opacity duration-300">
                        <div class="absolute -top-6 bg-amber-500/95 text-slate-950 text-[9px] font-mono px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">
                            Deep Scan ROI
                        </div>
                        <i data-lucide="scan" class="w-8 h-8 text-amber-500/30 animate-pulse"></i>
                    </div>

                    <!-- No camera access fallback prompt -->
                    <div id="camera-fallback" class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center bg-slate-950/90 z-20 transition-opacity duration-300">
                        <div class="p-4 bg-slate-900 border border-slate-800 rounded-full text-slate-500 mb-4 shadow-inner">
                            <i data-lucide="video-off" class="w-12 h-12 text-slate-400"></i>
                        </div>
                        <h3 class="text-lg font-bold text-slate-200 mb-2">Camera Access Required</h3>
                        <p class="text-sm text-slate-400 max-w-md mb-6">
                            This application uses your webcam to automatically detect and snapshot QR codes. Please allow camera permissions when prompted.
                        </p>
                        <button onclick="startCamera()" class="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 active:scale-95 text-slate-950 font-bold rounded-lg shadow-lg shadow-amber-500/20 transition-all flex items-center gap-2">
                            <i data-lucide="video" class="w-4 h-4"></i> Initialize Device
                        </button>
                    </div>

                    <!-- Instant Snapping flash effect -->
                    <div id="snap-flash" class="absolute inset-0 bg-white opacity-0 pointer-events-none z-10 transition-opacity duration-75"></div>
                </div>

                <!-- Camera Controls Footer -->
                <div class="p-4 bg-slate-950/40 border-t border-slate-800 flex flex-col gap-4">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-1">Optical Input Device</label>
                            <div class="relative">
                                <select id="camera-select" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500 appearance-none cursor-pointer pr-8">
                                    <option value="">Detecting Devices...</option>
                                </select>
                                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-slate-400">
                                    <i data-lucide="chevron-down" class="w-4 h-4"></i>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-end gap-2">
                            <button id="toggle-scan-btn" onclick="toggleScanning()" class="flex-1 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white text-xs font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-emerald-600/10 h-9">
                                <i data-lucide="pause" class="w-4 h-4" id="btn-scan-icon"></i>
                                <span id="btn-scan-text">Pause Processing</span>
                            </button>
                            <button onclick="triggerManualSnapshot()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-1 transition-all border border-slate-700 h-9" title="Manual Snap">
                                <i data-lucide="camera" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Hardware Zoom Section (Shown dynamically if supported by hardware) -->
                    <div id="hw-zoom-container" class="hidden border-t border-slate-800/80 pt-3 flex items-center justify-between gap-4">
                        <div class="flex items-center gap-2 text-xs text-slate-300">
                            <i data-lucide="zoom-in" class="w-4 h-4 text-amber-500 animate-pulse"></i>
                            <span class="font-medium">Hardware Optical Zoom</span>
                        </div>
                        <div class="flex items-center gap-3 flex-1 justify-end max-w-xs">
                            <input type="range" id="hw-zoom-range" min="1" max="10" step="0.1" value="1" class="w-full accent-amber-500 bg-slate-800 rounded-lg appearance-none h-1.5 cursor-pointer">
                            <span id="hw-zoom-value" class="font-mono bg-slate-950 border border-slate-800 px-2 py-0.5 rounded text-amber-400 w-12 text-center text-xs">1.0x</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dashboard Analytics & Quick Stats -->
            <div class="grid grid-cols-3 gap-4">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
                    <div class="text-slate-500 text-[10px] uppercase tracking-wider font-bold">Total Scans</div>
                    <div class="text-2xl font-black text-slate-100 mt-1 font-mono" id="stat-total-scans">00</div>
                    <div class="text-[10px] text-emerald-400 flex items-center gap-1 mt-1">
                        <i data-lucide="trending-up" class="w-3 h-3"></i> This session
                    </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
                    <div class="text-slate-500 text-[10px] uppercase tracking-wider font-bold">Unique Assets</div>
                    <div class="text-2xl font-black text-amber-500 mt-1 font-mono" id="stat-unique-assets">00</div>
                    <div class="text-[10px] text-slate-400 flex items-center gap-1 mt-1">
                        <i data-lucide="fingerprint" class="w-3 h-3"></i> Unique Hash IDs
                    </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
                    <div class="text-slate-500 text-[10px] uppercase tracking-wider font-bold">Deep Scan Assist</div>
                    <div class="text-sm font-bold text-emerald-400 mt-2 font-mono flex items-center gap-1">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-ping"></span>
                        AUTO-SHARPEN
                    </div>
                    <div class="text-[10px] text-slate-400 mt-1">Fills Blur & Depth Gap</div>
                </div>
            </div>
        </div>

        <!-- Right Column: Live Decoded Data & Capture Panel (5 Cols) -->
        <div class="lg:col-span-5 flex flex-col gap-4">
            
            <!-- System Settings Panel -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                    <i data-lucide="sliders" class="w-4 h-4 text-amber-500"></i> Engine Adjustments
                </h3>
                <div class="space-y-4 text-xs">
                    <!-- Cooldown -->
                    <div class="flex items-center justify-between">
                        <span class="text-slate-300">Scan Cooldown (s)</span>
                        <div class="flex items-center gap-2">
                            <input type="range" id="cooldown-range" min="0.5" max="10" step="0.5" value="2.5" class="w-24 accent-amber-500 bg-slate-800 rounded-lg appearance-none h-1">
                            <span id="cooldown-value" class="font-mono bg-slate-950 border border-slate-800 px-2 py-0.5 rounded text-amber-400 w-10 text-center">2.5s</span>
                        </div>
                    </div>
                    
                    <!-- Advanced Distance Booster Switch -->
                    <div class="border-t border-slate-800 pt-3 flex items-center justify-between">
                        <div>
                            <span class="text-slate-200 font-semibold block">Distance & Blur Booster</span>
                            <span class="text-[10px] text-slate-500">Auto-enhances tiny/blurry codes</span>
                        </div>
                        <button onclick="toggleDeepScan()" id="deepscan-toggle-btn" class="px-3 py-1.5 rounded bg-amber-500 text-slate-950 font-bold flex items-center gap-1 shadow-lg shadow-amber-500/10">
                            <i data-lucide="zap" class="w-3.5 h-3.5"></i> Boost Active
                        </button>
                    </div>

                    <!-- Audio -->
                    <div class="border-t border-slate-800 pt-3 flex items-center justify-between">
                        <span class="text-slate-300">Audio Indicator (Beep)</span>
                        <button onclick="toggleAudioFeedback()" id="audio-toggle-btn" class="px-3 py-1 rounded bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 font-bold">
                            <i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Enabled
                        </button>
                    </div>
                </div>
            </div>

            <!-- Last Scanned Asset Panel -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl flex-1 flex flex-col min-h-[300px]">
                <div class="px-4 py-3 bg-slate-950/60 border-b border-slate-800 flex justify-between items-center">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <i data-lucide="database" class="w-4 h-4 text-emerald-400"></i> Live Matrix telemetry
                    </h3>
                    <span class="text-[10px] bg-slate-800 text-slate-400 font-mono px-2 py-0.5 rounded">AUTO SAVED</span>
                </div>

                <div id="last-scan-placeholder" class="flex-1 flex flex-col items-center justify-center p-6 text-center text-slate-500">
                    <div class="p-3 bg-slate-950 border border-slate-850 rounded-full mb-3 text-slate-600">
                        <i data-lucide="focus" class="w-8 h-8"></i>
                    </div>
                    <p class="text-sm font-semibold text-slate-400">Awaiting Target Detection</p>
                    <p class="text-xs text-slate-500 max-w-xs mt-1">Point your camera towards any industrial QR barcode to capture metadata and audit image.</p>
                </div>

                <!-- Last Scan Content (Populated dynamically) -->
                <div id="last-scan-content" class="hidden flex-1 flex flex-col p-4">
                    <!-- Photo Snapshot Preview with Data Overlay -->
                    <div class="relative bg-black rounded-lg overflow-hidden border border-slate-800 aspect-video mb-4 shadow-md">
                        <img id="last-scan-photo" src="" alt="Scan Capture" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none"></div>
                        <div class="absolute bottom-2 left-2 right-2 flex justify-between items-end text-[10px] font-mono text-slate-300">
                            <div class="flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                <span id="last-scan-overlay-id">ID: --</span>
                            </div>
                            <span id="last-scan-overlay-time">TIME: --</span>
                        </div>
                    </div>

                    <!-- Unique Special ID -->
                    <div class="mb-3">
                        <label class="block text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-1">Generated Tracking ID</label>
                        <div class="flex items-center gap-2">
                            <div id="last-scan-id" class="flex-1 bg-slate-950 border border-slate-850 rounded-lg px-3 py-2 font-mono text-xs text-amber-400 font-bold tracking-wider select-all">
                                --
                            </div>
                            <button onclick="copyToClipboard('last-scan-id')" class="bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-300 p-2 rounded-lg border border-slate-700" title="Copy ID">
                                <i data-lucide="copy" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Decoded Payload -->
                    <div class="mb-4 flex-1 flex flex-col">
                        <label class="block text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-1">Barcode Payload Data</label>
                        <div class="flex-1 bg-slate-950 border border-slate-850 rounded-lg p-3 font-mono text-xs text-slate-300 overflow-y-auto max-h-24 break-all">
                            <span id="last-scan-data">--</span>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="grid grid-cols-2 gap-2 mt-auto">
                        <button onclick="copyToClipboard('last-scan-data')" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs py-2 rounded-lg border border-slate-700 flex items-center justify-center gap-1">
                            <i data-lucide="file-text" class="w-4 h-4"></i> Copy Raw
                        </button>
                        <a id="last-scan-download" href="#" download="scan-capture.png" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs py-2 rounded-lg flex items-center justify-center gap-1 shadow-lg shadow-amber-500/10">
                            <i data-lucide="download" class="w-4 h-4"></i> Save Capture
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Lower Section: Historical Scan Logs & Data Exports -->
    <section class="max-w-7xl w-full mx-auto p-4 mb-8">
        <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <!-- Header section -->
            <div class="px-6 py-4 bg-slate-950/60 border-b border-slate-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                        <i data-lucide="list-collapse" class="w-4 h-4 text-amber-500"></i> Local Scan Database Ledger
                    </h3>
                    <p class="text-xs text-slate-500">Historical records & snapshots processed in the current scanning session</p>
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto">
                    <button onclick="clearLogs()" class="px-3 py-1.5 text-xs font-bold text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg hover:bg-red-500/20 active:scale-95 transition-all">
                        Clear Log
                    </button>
                    <div class="relative inline-block text-left text-xs">
                        <select id="export-select" onchange="handleExport(this)" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-1.5 px-3 rounded-lg border border-slate-700 focus:outline-none cursor-pointer pr-8 appearance-none">
                            <option value="">Export Ledger...</option>
                            <option value="csv">Export CSV</option>
                            <option value="json">Export JSON</option>
                        </select>
                        <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none text-slate-400">
                            <i data-lucide="download" class="w-3.5 h-3.5"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Table Logs Container -->
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead class="bg-slate-950/40 text-slate-400 font-mono border-b border-slate-800">
                        <tr>
                            <th class="px-6 py-3 font-semibold">Audit Snapshot</th>
                            <th class="px-6 py-3 font-semibold">Special Tracking ID</th>
                            <th class="px-6 py-3 font-semibold">Timestamp</th>
                            <th class="px-6 py-3 font-semibold">Payload Content</th>
                            <th class="px-6 py-3 font-semibold text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="log-table-body" class="divide-y divide-slate-850">
                        <tr id="empty-table-row">
                            <td colspan="5" class="px-6 py-12 text-center text-slate-500">
                                <div class="flex flex-col items-center justify-center gap-2">
                                    <i data-lucide="archive" class="w-8 h-8 text-slate-600"></i>
                                    <span>Audit Ledger is empty. Scan barcode to append logs.</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Hidden preprocessing helper canvas for Super Resolution & Crop enhancement -->
    <canvas id="deep-scan-helper-canvas" class="hidden" width="360" height="360"></canvas>

    <!-- Interactive On-Screen Status Toasts -->
    <div id="toast-container" class="fixed bottom-4 right-4 z-[9999] flex flex-col gap-2 max-w-sm pointer-events-none"></div>

    <script>
        // System Config & State
        let videoStream = null;
        let isProcessing = true;
        let isAudioEnabled = true;
        let isDeepScanEnabled = true; // Enabled by default to help with blur and distance
        let selectedCameraId = null;
        let scanHistory = [];
        let scanningLoopId = null;
        let fpsLastTime = performance.now();
        let fpsFrames = 0;
        let currentFps = 0;

        // Camera hardware control capabilities
        let cameraCapabilities = null;

        // Scan deduplication and cooldown controls
        let lastScannedPayload = null;
        let lastScanTimestamp = 0;
        let scanCooldownMs = 2500; // adjustable by user UI slider

        // DOM elements cache
        const video = document.getElementById('video-feed');
        const displayCanvas = document.getElementById('display-canvas');
        const ctx = displayCanvas.getContext('2d', { willReadFrequently: true });
        const deepScanCanvas = document.getElementById('deep-scan-helper-canvas');
        const deepCtx = deepScanCanvas.getContext('2d', { willReadFrequently: true });
        
        const cameraFallback = document.getElementById('camera-fallback');
        const cameraSelect = document.getElementById('camera-select');
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        const toggleScanBtn = document.getElementById('toggle-scan-btn');
        const btnScanIcon = document.getElementById('btn-scan-icon');
        const btnScanText = document.getElementById('btn-scan-text');
        const cooldownRange = document.getElementById('cooldown-range');
        const cooldownValue = document.getElementById('cooldown-value');
        const audioToggleBtn = document.getElementById('audio-toggle-btn');
        const deepScanToggleBtn = document.getElementById('deepscan-toggle-btn');
        const deepScanZone = document.getElementById('deep-scan-zone');
        const fpsCounter = document.getElementById('fps-counter');

        const hwZoomContainer = document.getElementById('hw-zoom-container');
        const hwZoomRange = document.getElementById('hw-zoom-range');
        const hwZoomValue = document.getElementById('hw-zoom-value');

        // Initial setup on boot
        window.onload = () => {
            lucide.createIcons();
            updateTime();
            setInterval(updateTime, 1000);
            
            // Wire UI Controls
            cooldownRange.addEventListener('input', (e) => {
                const val = parseFloat(e.target.value);
                scanCooldownMs = val * 1000;
                cooldownValue.textContent = val.toFixed(1) + 's';
            });

            // Hardware zoom action listener
            hwZoomRange.addEventListener('input', async (e) => {
                const zoomVal = parseFloat(e.target.value);
                hwZoomValue.textContent = zoomVal.toFixed(1) + 'x';
                await applyHardwareZoom(zoomVal);
            });

            // Enumerate cameras on startup
            enumerateCameras();
            // Try to auto-start camera
            startCamera();
        };

        // Realtime digital clock update
        function updateTime() {
            const timeSpan = document.getElementById('current-time');
            const now = new Date();
            timeSpan.textContent = now.toLocaleTimeString();
        }

        // Search for all video devices on client system
        async function enumerateCameras() {
            try {
                // Trigger quick permission call to ensure device names are disclosed
                const tempStream = await navigator.mediaDevices.getUserMedia({ video: true }).catch(() => null);
                if (tempStream) {
                    tempStream.getTracks().forEach(track => track.stop());
                }

                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                
                cameraSelect.innerHTML = '';
                if (videoDevices.length === 0) {
                    cameraSelect.innerHTML = '<option value="">No cameras detected</option>';
                    return;
                }

                videoDevices.forEach((device, index) => {
                    const label = device.label || `Camera ${index + 1}`;
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.textContent = label;
                    cameraSelect.appendChild(option);
                });

                // Attach change listener
                cameraSelect.onchange = (e) => {
                    selectedCameraId = e.target.value;
                    startCamera();
                };

                if (videoDevices.length > 0) {
                    // Preselect first camera/back camera if available
                    const backCam = videoDevices.find(device => device.label.toLowerCase().includes('back') || device.label.toLowerCase().includes('environment'));
                    selectedCameraId = backCam ? backCam.deviceId : videoDevices[0].deviceId;
                    cameraSelect.value = selectedCameraId;
                }
            } catch (err) {
                console.error("Camera enumeration failure: ", err);
                showToast("System failed to list video capture devices", "error");
            }
        }

        // Initialize user video source with resilient resolution fallback configurations
        async function startCamera() {
            // Stop active track loops if running
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
            }
            if (scanningLoopId) {
                cancelAnimationFrame(scanningLoopId);
            }

            // Progression of camera configurations to satisfy high and low-end hardware
            const constraintTiers = [
                // Tier 1: Target camera with High Definition (No rigid 'min' properties to avoid OverconstrainedError)
                {
                    video: selectedCameraId 
                        ? { deviceId: { ideal: selectedCameraId }, width: { ideal: 1920 }, height: { ideal: 1080 } }
                        : { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } }
                },
                // Tier 2: HD Ready (720p)
                {
                    video: selectedCameraId 
                        ? { deviceId: { ideal: selectedCameraId }, width: { ideal: 1280 }, height: { ideal: 720 } }
                        : { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
                },
                // Tier 3: Basic SD properties
                {
                    video: selectedCameraId 
                        ? { deviceId: { ideal: selectedCameraId } } 
                        : { facingMode: 'environment' }
                },
                // Tier 4: Generical default video fallback
                {
                    video: true
                }
            ];

            let success = false;
            let lastError = null;

            // Attempt to bind media source with successive fallback tiers
            for (let i = 0; i < constraintTiers.length; i++) {
                try {
                    videoStream = await navigator.mediaDevices.getUserMedia(constraintTiers[i]);
                    success = true;
                    break;
                } catch (err) {
                    console.warn(`Camera initialization constraint tier ${i} failed:`, err);
                    lastError = err;
                }
            }

            if (success && videoStream) {
                video.srcObject = videoStream;
                video.setAttribute('playsinline', true); // crucial for iOS
                video.play();

                cameraFallback.classList.add('opacity-0', 'pointer-events-none');
                statusDot.className = "w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse";
                statusText.textContent = "Scanner System Online";
                statusText.className = "text-emerald-400";

                // Wait for metadata to configure dimensions correctly
                video.onloadedmetadata = () => {
                    displayCanvas.width = video.videoWidth || 640;
                    displayCanvas.height = video.videoHeight || 480;
                    
                    // Position and scale visual guide overlay
                    updateDeepScanOverlayPosition();

                    // Detect advanced hardware attributes (like optical / digital zoom capabilities)
                    detectHardwareCapabilities();

                    // Run core scanning cycle
                    scanningLoopId = requestAnimationFrame(processFrame);
                };
            } else {
                console.error("Critical: Camera initialization error. Details:", lastError);
                cameraFallback.classList.remove('opacity-0', 'pointer-events-none');
                statusDot.className = "w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse";
                
                const errFriendlyName = lastError ? (lastError.name || lastError.message || "Access Blocked") : "Unknown Error";
                statusText.textContent = `Camera Offline (${errFriendlyName})`;
                statusText.className = "text-slate-300";
                showToast(`Camera connection failed: ${errFriendlyName}`, "error");
            }
        }

        // Scale the overlay box inside viewport
        function updateDeepScanOverlayPosition() {
            if (isDeepScanEnabled && isProcessing) {
                deepScanZone.classList.remove('opacity-0');
                deepScanZone.classList.add('opacity-100');
            } else {
                deepScanZone.classList.remove('opacity-100');
                deepScanZone.classList.add('opacity-0');
            }
        }

        // Detect dynamic parameters of camera stream
        function detectHardwareCapabilities() {
            try {
                const track = videoStream.getVideoTracks()[0];
                if (track && typeof track.getCapabilities === 'function') {
                    cameraCapabilities = track.getCapabilities();
                    
                    // Check if zoom capability is natively exposed
                    if (cameraCapabilities.zoom) {
                        hwZoomContainer.classList.remove('hidden');
                        hwZoomRange.min = cameraCapabilities.zoom.min || 1;
                        hwZoomRange.max = cameraCapabilities.zoom.max || 8;
                        hwZoomRange.step = cameraCapabilities.zoom.step || 0.1;
                        hwZoomRange.value = 1;
                        hwZoomValue.textContent = '1.0x';
                    } else {
                        hwZoomContainer.classList.add('hidden');
                    }
                } else {
                    hwZoomContainer.classList.add('hidden');
                }
            } catch (e) {
                console.log("Hardware controls detection bypass:", e);
                hwZoomContainer.classList.add('hidden');
            }
        }

        // Apply native hardware zoom attributes
        async function applyHardwareZoom(value) {
            try {
                const track = videoStream.getVideoTracks()[0];
                if (track && cameraCapabilities && cameraCapabilities.zoom) {
                    await track.applyConstraints({
                        advanced: [{ zoom: value }]
                    });
                }
            } catch (err) {
                console.error("Failed to apply hardware zoom constraints", err);
            }
        }

        // Pause / Resume Scanning logic
        function toggleScanning() {
            isProcessing = !isProcessing;
            if (isProcessing) {
                btnScanIcon.setAttribute('data-lucide', 'pause');
                btnScanText.textContent = "Pause Processing";
                toggleScanBtn.className = "flex-1 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white text-xs font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-emerald-600/10 h-9";
                showToast("Realtime code evaluation active", "success");
            } else {
                btnScanIcon.setAttribute('data-lucide', 'play');
                btnScanText.textContent = "Resume Processing";
                toggleScanBtn.className = "flex-1 bg-amber-600 hover:bg-amber-500 active:scale-95 text-white text-xs font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-amber-500/10 h-9";
                showToast("Realtime code evaluation suspended", "warning");
            }
            updateDeepScanOverlayPosition();
            lucide.createIcons();
        }

        // Toggle Distance Booster Engine
        function toggleDeepScan() {
            isDeepScanEnabled = !isDeepScanEnabled;
            if (isDeepScanEnabled) {
                deepScanToggleBtn.className = "px-3 py-1.5 rounded bg-amber-500 text-slate-950 font-bold flex items-center gap-1 shadow-lg shadow-amber-500/10";
                deepScanToggleBtn.innerHTML = '<i data-lucide="zap" class="w-3.5 h-3.5"></i> Boost Active';
                showToast("Deep scan distance auto-sharpening is active", "success");
            } else {
                deepScanToggleBtn.className = "px-3 py-1.5 rounded bg-slate-800 text-slate-400 border border-slate-700 font-semibold flex items-center gap-1";
                deepScanToggleBtn.innerHTML = '<i data-lucide="zap-off" class="w-3.5 h-3.5"></i> Standard Scan';
                showToast("Distance booster disabled. Switched to standard scan.", "info");
            }
            updateDeepScanOverlayPosition();
            lucide.createIcons();
        }

        // Toggle standard scanning audio beep
        function toggleAudioFeedback() {
            isAudioEnabled = !isAudioEnabled;
            if (isAudioEnabled) {
                audioToggleBtn.className = "px-3 py-1 rounded bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 font-bold";
                audioToggleBtn.innerHTML = '<i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Enabled';
                showToast("Audio feedback initialized", "success");
            } else {
                audioToggleBtn.className = "px-3 py-1 rounded bg-slate-800 text-slate-400 border border-slate-700 flex items-center gap-1 font-bold";
                audioToggleBtn.innerHTML = '<i data-lucide="volume-x" class="w-3.5 h-3.5"></i> Disabled';
                showToast("Audio feedback disabled", "warning");
            }
            lucide.createIcons();
        }

        // High frequency industrial buzzer beep generator
        function playScanBeep() {
            if (!isAudioEnabled) return;
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                // Sound design: Clean Double Beep
                const playBeep = (freq, start, duration) => {
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, start);
                    
                    gain.gain.setValueAtTime(0.15, start);
                    gain.gain.exponentialRampToValueAtTime(0.01, start + duration);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start(start);
                    osc.stop(start + duration);
                };

                const now = audioCtx.currentTime;
                playBeep(1200, now, 0.08);
                playBeep(1600, now + 0.05, 0.12);
            } catch (e) {
                console.error("Audio WebAPI Failure", e);
            }
        }

        // Fast pixel contrast stretch & highpass convolution filter to sharpen blur in memory
        function applySharpenAndContrastFilter(imgData) {
            const data = imgData.data;
            const w = imgData.width;
            const h = imgData.height;
            
            // Step 1: Maximize Contrast (Stretch)
            let minVal = 255;
            let maxVal = 0;
            for (let i = 0; i < data.length; i += 4) {
                const gray = 0.2126 * data[i] + 0.7152 * data[i+1] + 0.0722 * data[i+2];
                if (gray < minVal) minVal = gray;
                if (gray > maxVal) maxVal = gray;
            }
            const range = maxVal - minVal;
            const factor = range > 0 ? (255 / range) : 1;

            // Temp array for convolution
            const buffer = new Uint8ClampedArray(data.length);
            buffer.set(data);

            // Step 2: Apply a highpass sharpening convolution kernel (3x3 grid)
            // [ 0  -1   0 ]
            // [-1   5  -1 ]
            // [ 0  -1   0 ]
            for (let y = 1; y < h - 1; y++) {
                for (let x = 1; x < w - 1; x++) {
                    const idx = (y * w + x) * 4;
                    for (let c = 0; c < 3; c++) { // RGB elements
                        const center = buffer[idx + c];
                        const top = buffer[((y - 1) * w + x) * 4 + c];
                        const bottom = buffer[((y + 1) * w + x) * 4 + c];
                        const left = buffer[(y * w + (x - 1)) * 4 + c];
                        const right = buffer[(y * w + (x + 1)) * 4 + c];

                        // Sharp matrix formula
                        let sharpVal = 5 * center - top - bottom - left - right;

                        // Apply contrast enhancement
                        sharpVal = (sharpVal - minVal) * factor;

                        // Clamp values between [0, 255]
                        data[idx + c] = sharpVal < 0 ? 0 : (sharpVal > 255 ? 255 : sharpVal);
                    }
                    data[idx + 3] = 255; // Set Alpha to solid
                }
            }
        }

        // CORE PROCESSING LOOP: Capture, Paint, Detect, Act
        function processFrame() {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
                // Always resize display canvas to fit actual camera stream resolution dynamically
                if (displayCanvas.width !== video.videoWidth || displayCanvas.height !== video.videoHeight) {
                    displayCanvas.width = video.videoWidth;
                    displayCanvas.height = video.videoHeight;
                    updateDeepScanOverlayPosition();
                }

                // Render current frame to visible canvas
                ctx.drawImage(video, 0, 0, displayCanvas.width, displayCanvas.height);

                // Run FPS counter
                calculateFps();

                // Run scanning engine only when active
                if (isProcessing) {
                    try {
                        const imgData = ctx.getImageData(0, 0, displayCanvas.width, displayCanvas.height);
                        
                        // Pass 1: Try reading standard full-frame image
                        let code = jsQR(imgData.data, imgData.width, imgData.height, {
                            inversionAttempts: "dontInvert"
                        });

                        // Pass 2: If Pass 1 fails, and Distance Booster is on, execute Deep Scan ROI targeting
                        if (!code && isDeepScanEnabled) {
                            // Extract a square region (30% of resolution) from center of display canvas
                            const cropSize = Math.min(displayCanvas.width, displayCanvas.height) * 0.35;
                            const cropX = (displayCanvas.width - cropSize) / 2;
                            const cropY = (displayCanvas.height - cropSize) / 2;

                            // Draw cropped region stretched onto helper canvas (performs digital hardware resize zoom)
                            deepCtx.drawImage(
                                displayCanvas, 
                                cropX, cropY, cropSize, cropSize, // source crop coords
                                0, 0, deepScanCanvas.width, deepScanCanvas.height // dest upscale canvas coords
                            );

                            // Apply custom low-level image processing directly to the zoomed frame
                            const croppedImgData = deepCtx.getImageData(0, 0, deepScanCanvas.width, deepScanCanvas.height);
                            applySharpenAndContrastFilter(croppedImgData);
                            deepCtx.putImageData(croppedImgData, 0, 0);

                            // Scan the super-sharpened cropped image
                            const deepCode = jsQR(croppedImgData.data, croppedImgData.width, croppedImgData.height, {
                                inversionAttempts: "dontInvert"
                            });

                            if (deepCode) {
                                // Translate cropped local coords back to full-frame canvas coordinates
                                const scaleFactor = cropSize / deepScanCanvas.width;
                                const translatedLocation = {
                                    topLeftCorner: {
                                        x: deepCode.location.topLeftCorner.x * scaleFactor + cropX,
                                        y: deepCode.location.topLeftCorner.y * scaleFactor + cropY
                                    },
                                    topRightCorner: {
                                        x: deepCode.location.topRightCorner.x * scaleFactor + cropX,
                                        y: deepCode.location.topRightCorner.y * scaleFactor + cropY
                                    },
                                    bottomRightCorner: {
                                        x: deepCode.location.bottomRightCorner.x * scaleFactor + cropX,
                                        y: deepCode.location.bottomRightCorner.y * scaleFactor + cropY
                                    },
                                    bottomLeftCorner: {
                                        x: deepCode.location.bottomLeftCorner.x * scaleFactor + cropX,
                                        y: deepCode.location.bottomLeftCorner.y * scaleFactor + cropY
                                    }
                                };

                                code = {
                                    data: deepCode.data,
                                    location: translatedLocation
                                };

                                // Draw a temporary orange outline to show Deep Scan found it!
                                ctx.beginPath();
                                ctx.rect(cropX, cropY, cropSize, cropSize);
                                ctx.lineWidth = 2;
                                ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
                                ctx.stroke();
                            }
                        }

                        if (code) {
                            // Draws high visibility target boundaries directly over the identified QR location
                            drawTargetBoundingBox(code.location);

                            const currentTimeMs = Date.now();
                            const isNewPayload = code.data !== lastScannedPayload;
                            const isCooldownExpired = (currentTimeMs - lastScanTimestamp) > scanCooldownMs;

                            // Evaluate state: Only trigger capture if different QR code OR cooldown finished
                            if (isNewPayload || isCooldownExpired) {
                                executeAuditCapture(code.data, code.location);
                            }
                        }
                    } catch (err) {
                        console.error("Decoded frame crash: ", err);
                    }
                }
            }
            scanningLoopId = requestAnimationFrame(processFrame);
        }

        // Frame calculations (FPS)
        function calculateFps() {
            fpsFrames++;
            const now = performance.now();
            if (now >= fpsLastTime + 1000) {
                currentFps = Math.round((fpsFrames * 1000) / (now - fpsLastTime));
                fpsCounter.textContent = `FPS: ${currentFps}`;
                fpsFrames = 0;
                fpsLastTime = now;
            }
        }

        // Draw dynamic glowing borders and tracking indicators directly on detected QR coords
        function drawTargetBoundingBox(location) {
            const { topLeftCorner, topRightCorner, bottomRightCorner, bottomLeftCorner } = location;

            // Draw primary tracking line
            ctx.beginPath();
            ctx.moveTo(topLeftCorner.x, topLeftCorner.y);
            ctx.lineTo(topRightCorner.x, topRightCorner.y);
            ctx.lineTo(bottomRightCorner.x, bottomRightCorner.y);
            ctx.lineTo(bottomLeftCorner.x, bottomLeftCorner.y);
            ctx.closePath();
            ctx.lineWidth = 4;
            ctx.strokeStyle = '#10b981'; // Tailwind Emerald-500
            ctx.shadowColor = '#059669';
            ctx.shadowBlur = 15;
            ctx.stroke();
            
            // Clean shadow state
            ctx.shadowBlur = 0;

            // Draw visual corner brackets for targeting aesthetics
            const corners = [topLeftCorner, topRightCorner, bottomRightCorner, bottomLeftCorner];
            corners.forEach((corner, i) => {
                ctx.beginPath();
                ctx.arc(corner.x, corner.y, 6, 0, 2 * Math.PI);
                ctx.fillStyle = '#f59e0b'; // Tailwind Amber-500
                ctx.fill();
            });
        }

        // Generate high fidelity uniquely identifiable tracking hashes
        function generateIndustrialId(payload) {
            // Jenkins One-at-a-time hash algorithm for fast, non-cryptographic secure hashes
            let hash = 0;
            for (let i = 0; i < payload.length; i++) {
                hash += payload.charCodeAt(i);
                hash += (hash << 10);
                hash ^= (hash >> 6);
            }
            hash += (hash << 3);
            hash ^= (hash >> 11);
            hash += (hash << 15);
            
            const shortHex = Math.abs(hash).toString(16).toUpperCase().padStart(5, '0');
            const now = new Date();
            const dateStr = now.getFullYear() +
                            String(now.getMonth() + 1).padStart(2, '0') +
                            String(now.getDate()).padStart(2, '0');
            const randomSuffix = Math.floor(100 + Math.random() * 900);
            
            return `IND-${dateStr}-${shortHex.slice(0, 5)}-${randomSuffix}`;
        }

        // Capture audit log record, trigger alerts, populate tables
        function executeAuditCapture(payload, location) {
            // Play success audible trigger
            playScanBeep();

            // Trigger physical capture flash UI effect
            const flash = document.getElementById('snap-flash');
            flash.classList.remove('opacity-0');
            flash.classList.add('opacity-90');
            setTimeout(() => {
                flash.classList.remove('opacity-90');
                flash.classList.add('opacity-0');
            }, 80);

            // Record telemetry
            lastScannedPayload = payload;
            lastScanTimestamp = Date.now();

            // Generate clean Audit metadata
            const trackingId = generateIndustrialId(payload);
            const date = new Date();
            const formattedTime = date.toLocaleTimeString() + ' ' + date.toLocaleDateString();

            // Create offscreen canvas to render snapshot with a solid watermarked tracking footer
            const snapshotCanvas = document.createElement('canvas');
            const snapCtx = snapshotCanvas.getContext('2d');
            
            // Set snapshot size proportional to current visual layout dimensions
            snapshotCanvas.width = displayCanvas.width;
            snapshotCanvas.height = displayCanvas.height;

            // Draw current camera viewport frame
            snapCtx.drawImage(displayCanvas, 0, 0);

            // If location details exist, let's imprint a clean green target circle over the QR center
            if (location) {
                const centerX = (location.topLeftCorner.x + location.bottomRightCorner.x) / 2;
                const centerY = (location.topLeftCorner.y + location.bottomRightCorner.y) / 2;
                snapCtx.beginPath();
                snapCtx.arc(centerX, centerY, 30, 0, 2 * Math.PI);
                snapCtx.strokeStyle = '#10b981';
                snapCtx.lineWidth = 5;
                snapCtx.stroke();
            }

            // Draw high-contrast professional telemetry watermark overlay bar on snapshot
            const footerHeight = Math.max(30, snapshotCanvas.height * 0.08);
            snapCtx.fillStyle = 'rgba(15, 23, 42, 0.95)'; // dark slate tailwind
            snapCtx.fillRect(0, snapshotCanvas.height - footerHeight, snapshotCanvas.width, footerHeight);

            snapCtx.fillStyle = '#f59e0b'; // Amber text
            snapCtx.font = `bold ${Math.max(10, footerHeight * 0.35)}px monospace`;
            snapCtx.fillText(`AUDIT ID: ${trackingId}`, 15, snapshotCanvas.height - (footerHeight * 0.55));

            snapCtx.fillStyle = '#94a3b8'; // Slate Text
            snapCtx.font = `${Math.max(8, footerHeight * 0.30)}px monospace`;
            snapCtx.fillText(`TS: ${formattedTime} | PL: ${payload.length > 30 ? payload.substring(0,27)+'...' : payload}`, 15, snapshotCanvas.height - (footerHeight * 0.22));

            const snapshotDataUrl = snapshotCanvas.toDataURL('image/png');

            // Save to internal collection array
            const record = {
                id: trackingId,
                timestamp: formattedTime,
                payload: payload,
                image: snapshotDataUrl
            };

            scanHistory.unshift(record);

            // Update UI State Displays
            updateDashboardDisplays(record);
            appendLogToTable(record);
            updateStats();

            showToast(`Asset Registered: ${trackingId}`, "success");
        }

        // Manual capture trigger fallback bypass
        function triggerManualSnapshot() {
            if (!videoStream) {
                showToast("System Camera is not initialized", "error");
                return;
            }
            executeAuditCapture("MANUAL_AUDIT_LOG_RECORD_" + Date.now().toString(36).toUpperCase(), null);
        }

        // Dynamically update primary telemetry inspection pane
        function updateDashboardDisplays(record) {
            document.getElementById('last-scan-placeholder').classList.add('hidden');
            const content = document.getElementById('last-scan-content');
            content.classList.remove('hidden');

            // Set images and details
            document.getElementById('last-scan-photo').src = record.image;
            document.getElementById('last-scan-id').textContent = record.id;
            document.getElementById('last-scan-data').textContent = record.payload;
            document.getElementById('last-scan-overlay-id').textContent = `ID: ${record.id.split('-')[2]}`;
            document.getElementById('last-scan-overlay-time').textContent = record.timestamp.split(' ')[0];

            // Wire instant download file target
            const dlBtn = document.getElementById('last-scan-download');
            dlBtn.href = record.image;
            dlBtn.download = `QR_AUDIT_${record.id}.png`;
        }

        // Append historical metadata rows onto live system ledger
        function appendLogToTable(record) {
            const tableBody = document.getElementById('log-table-body');
            const emptyRow = document.getElementById('empty-table-row');
            if (emptyRow) {
                emptyRow.remove();
            }

            const tr = document.createElement('tr');
            tr.className = "hover:bg-slate-800/40 transition-colors border-b border-slate-850/60";
            tr.id = `row-${record.id}`;

            tr.innerHTML = `
                <td class="px-6 py-3">
                    <div class="relative w-20 h-11 bg-slate-950 rounded border border-slate-800 overflow-hidden group cursor-zoom-in" onclick="viewAuditImage('${record.id}')">
                        <img src="${record.image}" alt="Audit" class="w-full h-full object-cover group-hover:scale-110 transition-transform">
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                            <i data-lucide="eye" class="w-4 h-4 text-white"></i>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-3 font-mono font-bold text-amber-500 tracking-wider">
                    ${record.id}
                </td>
                <td class="px-6 py-3 text-slate-400 font-mono">
                    ${record.timestamp}
                </td>
                <td class="px-6 py-3 max-w-xs truncate text-slate-300 font-mono" title="${escapeHtml(record.payload)}">
                    ${escapeHtml(record.payload)}
                </td>
                <td class="px-6 py-3 text-right">
                    <div class="flex items-center justify-end gap-1.5">
                        <button onclick="copyRawText('${escapeHtml(record.payload)}')" class="bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 p-1.5 rounded transition-colors" title="Copy Content">
                            <i data-lucide="clipboard-copy" class="w-4 h-4"></i>
                        </button>
                        <a href="${record.image}" download="QR_AUDIT_${record.id}.png" class="bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 p-1.5 rounded transition-colors" title="Download Image">
                            <i data-lucide="download" class="w-4 h-4"></i>
                        </a>
                        <button onclick="deleteRecord('${record.id}')" class="bg-red-950/40 hover:bg-red-900/60 text-red-400 p-1.5 rounded border border-red-900/30 transition-colors" title="Delete">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </td>
            `;

            tableBody.insertBefore(tr, tableBody.firstChild);
            lucide.createIcons();
        }

        // Calculate analytical sums
        function updateStats() {
            document.getElementById('stat-total-scans').textContent = String(scanHistory.length).padStart(2, '0');
            
            // Unique tracking algorithm checks
            const uniquePayloads = new Set(scanHistory.map(item => item.payload));
            document.getElementById('stat-unique-assets').textContent = String(uniquePayloads.size).padStart(2, '0');
        }

        // Remove audit records permanently from active memory
        function deleteRecord(id) {
            scanHistory = scanHistory.filter(item => item.id !== id);
            const row = document.getElementById(`row-${id}`);
            if (row) {
                row.remove();
            }

            if (scanHistory.length === 0) {
                resetToEmptyTableState();
            }

            // Check if current display matches deleted
            const lastScanId = document.getElementById('last-scan-id');
            if (lastScanId && lastScanId.textContent.trim() === id) {
                document.getElementById('last-scan-content').classList.add('hidden');
                document.getElementById('last-scan-placeholder').classList.remove('hidden');
                lastScannedPayload = null;
            }

            updateStats();
            showToast("Record purged from database", "warning");
        }

        // Purge historical sessions
        function clearLogs() {
            scanHistory = [];
            resetToEmptyTableState();
            
            document.getElementById('last-scan-content').classList.add('hidden');
            document.getElementById('last-scan-placeholder').classList.remove('hidden');
            lastScannedPayload = null;

            updateStats();
            showToast("Telemetry database cleared", "warning");
        }

        function resetToEmptyTableState() {
            const tableBody = document.getElementById('log-table-body');
            tableBody.innerHTML = `
                <tr id="empty-table-row">
                    <td colspan="5" class="px-6 py-12 text-center text-slate-500">
                        <div class="flex flex-col items-center justify-center gap-2">
                            <i data-lucide="archive" class="w-8 h-8 text-slate-600"></i>
                            <span>Audit Ledger is empty. Scan barcode to append logs.</span>
                        </div>
                    </td>
                </tr>
            `;
            lucide.createIcons();
        }

        // Display Captured image in separate overlay
        function viewAuditImage(id) {
            const record = scanHistory.find(item => item.id === id);
            if (!record) return;

            // Create Modal Window Overlay Dynamically
            const modal = document.createElement('div');
            modal.className = "fixed inset-0 bg-black/90 backdrop-blur-sm z-[10000] flex items-center justify-center p-4 cursor-zoom-out";
            modal.onclick = () => modal.remove();

            modal.innerHTML = `
                <div class="relative max-w-4xl w-full bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl cursor-default" onclick="event.stopPropagation()">
                    <button class="absolute top-4 right-4 bg-black/60 hover:bg-black text-white rounded-full p-2" onclick="this.closest('.fixed').remove()">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                    <img src="${record.image}" alt="Modal audit snap" class="w-full object-contain max-h-[80vh]">
                    <div class="p-4 bg-slate-950/90 border-t border-slate-800 flex flex-col md:flex-row justify-between gap-4">
                        <div>
                            <span class="text-xs uppercase font-bold tracking-wider text-slate-500">Telemetry Tracking Node</span>
                            <h4 class="text-md font-bold text-amber-500 font-mono">${record.id}</h4>
                        </div>
                        <div class="text-right">
                            <span class="text-xs uppercase font-bold tracking-wider text-slate-500">Acquisition Stamp</span>
                            <p class="text-sm font-mono text-slate-300">${record.timestamp}</p>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            lucide.createIcons();
        }

        // Export system datasets (CSV or JSON formats)
        function handleExport(selectElem) {
            const value = selectElem.value;
            if (!value) return;

            if (scanHistory.length === 0) {
                showToast("No telemetry logs available to export", "error");
                selectElem.value = "";
                return;
            }

            let dataStr = "";
            let mimeType = "text/plain";
            let fileExt = "txt";

            if (value === "csv") {
                // Generate raw CSV representation without loading chunky external parsing libraries
                const csvRows = [
                    ["Special Tracking ID", "Timestamp", "Decoded Barcode Content", "DataURL Photo Frame"]
                ];
                
                scanHistory.forEach(item => {
                    csvRows.push([
                        `"${item.id}"`,
                        `"${item.timestamp}"`,
                        `"${item.payload.replace(/"/g, '""')}"`, // safe escape
                        `"${item.image}"`
                    ]);
                });

                dataStr = csvRows.map(row => row.join(",")).join("\n");
                mimeType = "text/csv;charset=utf-8;";
                fileExt = "csv";
            } else if (value === "json") {
                dataStr = JSON.stringify(scanHistory, null, 2);
                mimeType = "application/json;charset=utf-8;";
                fileExt = "json";
            }

            // Instigate physical download link callback
            const blob = new Blob([dataStr], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const exportLink = document.createElement("a");
            exportLink.setAttribute("href", url);
            exportLink.setAttribute("download", `SCANPRO_AUDIT_LOG_${Date.now()}.${fileExt}`);
            document.body.appendChild(exportLink);
            exportLink.click();
            document.body.removeChild(exportLink);
            
            // Reset dropdown state
            selectElem.value = "";
            showToast(`Asset Ledger exported successfully [.${fileExt.toUpperCase()}]`, "success");
        }

        // Reliable clipboard utility bypass
        function copyToClipboard(elementId) {
            const el = document.getElementById(elementId);
            if (!el) return;
            const textToCopy = el.textContent || el.value;
            copyRawText(textToCopy);
        }

        // Clipboard copy utility
        function copyRawText(text) {
            const dummy = document.createElement("textarea");
            document.body.appendChild(dummy);
            dummy.value = text;
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
            showToast("Copied content safely to clipboard", "success");
        }

        // Custom HTML Safe Character Escape utilities
        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return String(text).replace(/[&<>"']/g, function(m) { return map[m]; });
        }

        // Clean micro-toasting notifications
        function showToast(message, type = "info") {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            
            let colorClasses = "bg-slate-900 border-slate-800 text-slate-100";
            let iconName = "info";

            if (type === "success") {
                colorClasses = "bg-slate-900 border-emerald-500/30 text-emerald-400";
                iconName = "check-circle-2";
            } else if (type === "warning") {
                colorClasses = "bg-slate-900 border-amber-500/30 text-amber-400";
                iconName = "alert-triangle";
            } else if (type === "error") {
                colorClasses = "bg-slate-900 border-red-500/30 text-red-400";
                iconName = "alert-circle";
            }

            toast.className = `p-4 rounded-xl border flex items-center gap-3 shadow-2xl transition-all duration-300 transform translate-y-10 opacity-0 pointer-events-auto select-none ${colorClasses}`;
            toast.innerHTML = `
                <i data-lucide="${iconName}" class="w-5 h-5 shrink-0"></i>
                <span class="text-xs font-semibold font-mono tracking-wide">${message}</span>
            `;

            container.appendChild(toast);
            lucide.createIcons();

            // Animate In
            setTimeout(() => {
                toast.classList.remove('translate-y-10', 'opacity-0');
            }, 10);

            // Dismiss Timer
            setTimeout(() => {
                toast.classList.add('translate-y-[-10px]', 'opacity-0');
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 4000);
        }
    </script>
</body>
</html>
