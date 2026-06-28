<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warehouse Flow - AI Vision Automation</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome for Premium Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <!-- TensorFlow.js and COCO-SSD for Computer Vision -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.10.0/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js"></script>
    <!-- JsBarcode for rendering ID Barcodes -->
    <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>

    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0f172a; /* Slate 900 */
        }
        .code-font {
            font-family: 'JetBrains Mono', monospace;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #1e293b;
        }
        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
    </style>
</head>
<body class="text-slate-100 min-h-screen flex flex-col antialiased">

    <!-- Top Navigation Bar -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                    <i class="fa-solid fa-boxes-stack text-lg text-white"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                        WAREHOUSE<span class="text-indigo-400 font-extrabold text-xs bg-indigo-500/10 px-2 py-0.5 rounded-full border border-indigo-500/20">FLOW AI</span>
                    </h1>
                    <p class="text-xs text-slate-400">Automated Smart Detection & ID Generation</p>
                </div>
            </div>
            
            <div class="flex items-center gap-3">
                <div id="modelStatusBadge" class="flex items-center gap-2 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-lg text-xs font-semibold text-amber-400">
                    <span class="relative flex h-2 w-2">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                    </span>
                    <span id="modelStatusText">Initializing AI Vision Model...</span>
                </div>
                <div class="text-xs bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-lg text-slate-300 flex items-center gap-2">
                    <i class="fa-regular fa-clock text-indigo-400"></i>
                    <span id="liveClock">00:00:00 AM</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left Column: Camera Feed & AI Control Interface (7 Cols) -->
        <div class="lg:col-span-7 flex flex-col gap-6">
            
            <!-- Real-time Video Stream & Canvas Card -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl relative">
                <!-- Header/Controls -->
                <div class="px-5 py-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="flex h-2.5 w-2.5 rounded-full bg-red-500 animate-pulse"></span>
                        <h3 class="font-bold text-slate-200 text-sm tracking-wide uppercase">Live Scanning Terminal</h3>
                    </div>
                    <div class="flex items-center gap-2">
                        <!-- Camera Selector -->
                        <select id="cameraSelect" class="bg-slate-800 border border-slate-700 text-xs text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                            <option value="">Default Camera</option>
                        </select>
                        <button id="toggleCameraBtn" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-colors">
                            <i class="fa-solid fa-camera"></i> <span id="cameraBtnText">Start Feed</span>
                        </button>
                    </div>
                </div>

                <!-- Video Viewport Container -->
                <div class="relative bg-slate-950 aspect-video w-full flex items-center justify-center overflow-hidden">
                    
                    <!-- Loading / Placeholder Overlay -->
                    <div id="videoPlaceholder" class="absolute inset-0 z-10 flex flex-col items-center justify-center bg-slate-950 text-slate-500 p-6 text-center">
                        <div class="h-16 w-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mb-4 text-slate-400 text-xl">
                            <i class="fa-solid fa-video-slash"></i>
                        </div>
                        <h4 class="text-slate-300 font-semibold mb-1">Webcam Feed is Offline</h4>
                        <p class="text-xs text-slate-500 max-w-sm mb-4">Enable camera permissions and click "Start Feed" to begin real-time object detection and inventory serialization.</p>
                        <button id="quickStartBtn" class="bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 hover:bg-indigo-600/30 text-xs font-semibold px-4 py-2 rounded-xl transition-all">
                            Allow & Start Camera
                        </button>
                    </div>

                    <!-- Video stream (hidden, rendered onto Canvas) -->
                    <video id="videoFeed" class="hidden" autoplay playsinline muted></video>
                    
                    <!-- Dynamic Live Render Canvas -->
                    <canvas id="detectionCanvas" class="w-full h-full object-cover"></canvas>

                    <!-- Scanning HUD Overlays -->
                    <div id="scanningHUD" class="hidden absolute top-4 left-4 z-20 bg-slate-900/90 border border-indigo-500/30 backdrop-blur-md rounded-xl p-3 flex flex-col gap-1 text-xs">
                        <div class="text-indigo-400 font-bold flex items-center gap-1.5">
                            <i class="fa-solid fa-compass animate-spin"></i> COMPUTER VISION ENGAGED
                        </div>
                        <div class="text-slate-400 font-mono" id="hudFPS">FPS: --</div>
                        <div class="text-slate-400 font-mono" id="hudResolution">Res: --</div>
                    </div>

                    <!-- Target Box Sight -->
                    <div class="absolute inset-0 pointer-events-none flex items-center justify-center">
                        <div class="w-72 h-72 border-2 border-dashed border-indigo-500/25 rounded-2xl relative">
                            <div class="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-indigo-500 -mt-1 -ml-1 rounded-tl-md"></div>
                            <div class="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-indigo-500 -mt-1 -mr-1 rounded-tr-md"></div>
                            <div class="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-indigo-500 -mb-1 -ml-1 rounded-bl-md"></div>
                            <div class="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-indigo-500 -mb-1 -mr-1 rounded-br-md"></div>
                        </div>
                    </div>
                </div>

                <!-- Custom Notification Toast Inside Video Controls -->
                <div id="scannerNotification" class="bg-slate-900/90 border-t border-slate-800 px-4 py-3 flex items-center justify-between text-xs transition-all duration-300 opacity-0 transform translate-y-2 pointer-events-none">
                    <span class="text-indigo-400 flex items-center gap-2 font-medium">
                        <i class="fa-solid fa-barcode"></i>
                        <span id="scannerNotificationText">No active target</span>
                    </span>
                    <span class="text-slate-500 font-mono">Press Trigger manually or capture auto</span>
                </div>
            </div>

            <!-- AI Detection Parameters & Custom Override Inputs -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h3 class="text-sm font-bold tracking-wide uppercase text-slate-400 mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-indigo-500"></i> Generation & Detection Settings
                </h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">Target Detection Confidence threshold</label>
                        <div class="flex items-center gap-3">
                            <input type="range" id="confidenceThreshold" min="20" max="95" value="60" class="w-full accent-indigo-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer">
                            <span id="confidenceValue" class="text-xs font-bold code-font text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded border border-indigo-500/20">60%</span>
                        </div>
                        <span class="text-[10px] text-slate-500 block mt-1">Filters out transient background noise and objects.</span>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">Autonomous Capture Engine</label>
                        <div class="flex items-center justify-between bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                            <div class="text-xs text-slate-400">
                                <span class="font-medium text-slate-300">Auto ID Lock</span>
                                <p class="text-[10px] text-slate-500">Log instantly upon lock-on</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" id="autoCaptureToggle" class="sr-only peer">
                                <div class="w-9 h-5 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-slate-400 after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600 peer-checked:after:bg-white"></div>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="border-t border-slate-800/60 my-5"></div>

                <!-- Custom Product Serializer Form -->
                <div>
                    <div class="flex justify-between items-center mb-3">
                        <h4 class="text-xs font-bold tracking-wide uppercase text-slate-400">Current Isolated Target Info</h4>
                        <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full" id="formLockStatus">Status: Awaiting Lock</span>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
                        <div>
                            <label class="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Identified Class</label>
                            <input type="text" id="targetClassInput" placeholder="Awaiting detect..." class="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs text-slate-300 rounded-xl px-3 py-2.5 outline-none font-medium transition-colors">
                        </div>
                        <div>
                            <label class="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Target Weight (est. kg)</label>
                            <input type="number" id="targetWeightInput" step="0.1" value="1.2" class="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs text-slate-300 rounded-xl px-3 py-2.5 outline-none font-medium transition-colors">
                        </div>
                        <div>
                            <label class="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Warehouse Zone</label>
                            <select id="targetZoneSelect" class="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs text-slate-300 rounded-xl px-3 py-2.5 outline-none font-medium transition-colors">
                                <option value="Zone-A">Zone A (High Priority)</option>
                                <option value="Zone-B">Zone B (Standard)</option>
                                <option value="Zone-C">Zone C (Bulk)</option>
                                <option value="Zone-D">Zone D (Cold Store)</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
                        <div>
                            <label class="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Warehouse Shelf / Location</label>
                            <input type="text" id="targetShelfInput" value="SHELF-B12" class="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs text-slate-300 rounded-xl px-3 py-2.5 outline-none font-medium transition-colors code-font">
                        </div>
                        <div>
                            <label class="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Manufacture / Supplier Name</label>
                            <input type="text" id="targetSupplierInput" value="Automated Intake" class="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs text-slate-300 rounded-xl px-3 py-2.5 outline-none font-medium transition-colors">
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex flex-wrap gap-2.5 justify-end">
                        <button id="resetTargetBtn" class="bg-slate-850 hover:bg-slate-800 border border-slate-800 text-slate-400 text-xs font-semibold px-4 py-2.5 rounded-xl transition-all flex items-center gap-2">
                            <i class="fa-solid fa-rotate-left"></i> Reset Fields
                        </button>
                        <button id="manualCaptureBtn" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-6 py-2.5 rounded-xl transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2">
                            <i class="fa-solid fa-plus"></i> Generate SKU & Register Product
                        </button>
                    </div>
                </div>

            </div>
        </div>

        <!-- Right Column: Generated ID Display & Real-time Database Registry (5 Cols) -->
        <div class="lg:col-span-5 flex flex-col gap-6">
            
            <!-- Real-time ID Generation / Serializer Terminal Card -->
            <div class="bg-gradient-to-br from-indigo-950/40 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
                <!-- Visual mesh glow -->
                <div class="absolute -right-16 -top-16 w-36 h-36 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold tracking-wide uppercase text-slate-400 flex items-center gap-2">
                        <i class="fa-solid fa-fingerprint text-indigo-400 animate-pulse"></i> Hardware SKU Generator
                    </h3>
                    <span class="text-[10px] bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 px-2.5 py-1 rounded-full font-semibold">Ready</span>
                </div>

                <!-- Product Tracking ID Card Display -->
                <div class="bg-slate-950/80 border border-slate-800/80 rounded-xl p-5 mb-4 relative">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <span class="text-[9px] uppercase text-slate-500 tracking-wider">System Assigned UID</span>
                            <div id="genUUID" class="text-lg font-bold code-font text-white tracking-tight mt-0.5">AWAITING_LOCK</div>
                        </div>
                        <div class="bg-indigo-600/10 text-indigo-400 px-2 py-0.5 rounded text-[10px] font-mono border border-indigo-500/20" id="genSKUPrefix">
                            SKU-GEN
                        </div>
                    </div>

                    <!-- Dynamic barcode container -->
                    <div class="bg-white p-3 rounded-lg flex flex-col items-center justify-center min-h-[90px] mb-3 border border-slate-800/50">
                        <svg id="barcodeCanvas" class="max-w-full"></svg>
                        <span id="barcodeFallback" class="text-xs text-slate-400 font-mono hidden">Barcode placeholder</span>
                    </div>

                    <div class="grid grid-cols-2 gap-4 text-xs mt-3 border-t border-slate-800/50 pt-3">
                        <div>
                            <span class="text-[9px] uppercase text-slate-500 block">Identified Item</span>
                            <span class="font-semibold text-slate-200" id="genClassName">No active target</span>
                        </div>
                        <div>
                            <span class="text-[9px] uppercase text-slate-500 block">Verification Status</span>
                            <span class="text-emerald-400 font-semibold flex items-center gap-1" id="genVerified">
                                <i class="fa-solid fa-circle-check"></i> Standard Auto-Pass
                            </span>
                        </div>
                    </div>
                </div>

                <div class="flex items-center gap-2">
                    <button id="copyUIDBtn" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-semibold py-2.5 px-3 rounded-xl transition-all flex items-center justify-center gap-1.5">
                        <i class="fa-regular fa-copy"></i> Copy UID
                    </button>
                    <button id="printLabelBtn" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-semibold py-2.5 px-3 rounded-xl transition-all flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-print"></i> Print Label
                    </button>
                </div>
            </div>

            <!-- Warehouse Inventory Insights & Stats -->
            <div class="grid grid-cols-3 gap-3">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-center">
                    <span class="text-[9px] text-slate-500 uppercase tracking-wider block mb-1">Total Tracked</span>
                    <span id="statTotal" class="text-xl font-extrabold text-white code-font">0</span>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-center">
                    <span class="text-[9px] text-slate-500 uppercase tracking-wider block mb-1">High Conf Locked</span>
                    <span id="statHighConf" class="text-xl font-extrabold text-indigo-400 code-font">0</span>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-center">
                    <span class="text-[9px] text-slate-500 uppercase tracking-wider block mb-1">Zone Clusters</span>
                    <span id="statZones" class="text-xl font-extrabold text-emerald-400 code-font">4</span>
                </div>
            </div>

            <!-- Product Registry Feed Panel -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl flex-grow flex flex-col overflow-hidden shadow-xl min-h-[380px] max-h-[500px]">
                <div class="p-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
                    <div>
                        <h3 class="text-xs font-bold tracking-wide uppercase text-slate-300">Live Intake Log</h3>
                        <p class="text-[10px] text-slate-500">Chronological history of registered items</p>
                    </div>
                    <div class="flex items-center gap-1.5">
                        <button id="exportCsvBtn" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-[10px] text-slate-300 font-semibold px-2.5 py-1.5 rounded-lg flex items-center gap-1 transition-colors">
                            <i class="fa-solid fa-file-csv"></i> Export CSV
                        </button>
                        <button id="clearLogsBtn" class="bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-[10px] text-red-400 font-semibold px-2.5 py-1.5 rounded-lg flex items-center gap-1 transition-colors">
                            <i class="fa-solid fa-trash-can"></i> Clear
                        </button>
                    </div>
                </div>

                <!-- Live Search -->
                <div class="px-4 py-2.5 bg-slate-950/20 border-b border-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-magnifying-glass text-xs text-slate-500"></i>
                    <input type="text" id="registrySearch" placeholder="Filter by product name, zone or system ID..." class="bg-transparent text-xs text-slate-300 outline-none w-full placeholder-slate-600">
                </div>

                <!-- Database Registry Items List -->
                <div class="flex-grow overflow-y-auto p-4 flex flex-col gap-3" id="registryList">
                    <!-- Static empty state -->
                    <div id="registryEmptyState" class="flex flex-col items-center justify-center text-center py-12 text-slate-500">
                        <div class="text-3xl text-slate-600 mb-2">
                            <i class="fa-solid fa-cubes"></i>
                        </div>
                        <p class="text-xs font-medium">No serialized inventory records yet.</p>
                        <p class="text-[10px] text-slate-600 mt-1">Scan or manually record an object to construct a ledger.</p>
                    </div>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950/60 py-4 px-6 text-center text-xs text-slate-500">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <p>&copy; 2026 WarehouseFlow AI Automation Inc. Local sandboxed machine learning workspace.</p>
            <div class="flex gap-4">
                <a href="#" class="hover:text-slate-400">Security Protocols</a>
                <span class="text-slate-700">|</span>
                <a href="#" class="hover:text-slate-400">Hardware Requirements</a>
            </div>
        </div>
    </footer>

    <!-- Print View / Target Sticker Template (Hidden by default, used for printing labels) -->
    <div id="printStickerTemplate" class="hidden">
        <div style="font-family: monospace; width: 320px; padding: 20px; border: 2px solid #000; background: #fff; color: #000;">
            <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 5px; margin-bottom: 10px;">
                <h2 style="margin: 0; font-size: 16px; font-weight: bold;">WAREHOUSEFLOW AI LABEL</h2>
                <span style="font-size: 9px; text-transform: uppercase;">Intake Serial Sticker</span>
            </div>
            <div style="margin-bottom: 10px;">
                <table style="width: 100%; font-size: 10px;">
                    <tr><td style="font-weight: bold;">UID:</td><td id="printUID" class="code-font">AWAIT_GEN</td></tr>
                    <tr><td style="font-weight: bold;">SKU:</td><td id="printSKU">AWAIT_GEN</td></tr>
                    <tr><td style="font-weight: bold;">ITEM:</td><td id="printItem">N/A</td></tr>
                    <tr><td style="font-weight: bold;">ZONE:</td><td id="printZone">N/A</td></tr>
                    <tr><td style="font-weight: bold;">SHELF:</td><td id="printShelf">N/A</td></tr>
                    <tr><td style="font-weight: bold;">WEIGHT:</td><td id="printWeight">N/A</td></tr>
                    <tr><td style="font-weight: bold;">DATE:</td><td id="printDate">N/A</td></tr>
                </table>
            </div>
            <div style="display: flex; justify-content: center; padding: 5px; border: 1px solid #000; border-radius: 4px; background: white;">
                <svg id="printBarcodeCanvas"></svg>
            </div>
            <div style="text-align: center; font-size: 8px; margin-top: 10px; color: #666;">
                SANDBOX INTELLECTUAL PROPERTY &bull; NOT FOR PUBLIC TRANSIT
            </div>
        </div>
    </div>

    <!-- Main Logic Script -->
    <script>
        // --- CONSTANTS & CONFIGURATION ---
        const DEMO_ITEMS = [
            { class: 'cup', zone: 'Zone-B', shelf: 'SHELF-M02', weight: 0.3, supplier: 'Continental Glass' },
            { class: 'bottle', zone: 'Zone-A', shelf: 'SHELF-A01', weight: 1.0, supplier: 'Refresh Co.' },
            { class: 'chair', zone: 'Zone-C', shelf: 'SHELF-C22', weight: 4.5, supplier: 'Modular Furniture' },
            { class: 'laptop', zone: 'Zone-A', shelf: 'SHELF-A15', weight: 2.1, supplier: 'Apex Tech' },
            { class: 'book', zone: 'Zone-B', shelf: 'SHELF-N09', weight: 0.8, supplier: 'Vellum Books' },
            { class: 'cell phone', zone: 'Zone-A', shelf: 'SHELF-A08', weight: 0.2, supplier: 'Quantum Mobile' },
            { class: 'person', zone: 'Zone-D', shelf: 'RESTRICTED', weight: 75.0, supplier: 'Warehouse Personnel' },
            { class: 'keyboard', zone: 'Zone-B', shelf: 'SHELF-M10', weight: 0.6, supplier: 'Tactile Labs' },
            { class: 'mouse', zone: 'Zone-B', shelf: 'SHELF-M11', weight: 0.1, supplier: 'Tactile Labs' },
            { class: 'backpack', zone: 'Zone-B', shelf: 'SHELF-E04', weight: 1.4, supplier: 'Voyager Gear' }
        ];

        // System State
        let model = null;
        let isModelLoading = true;
        let isCameraActive = false;
        let videoStream = null;
        let currentPredictions = [];
        let detectedItemsLog = [];
        let autoLockOnTimer = null;
        let autoCaptureEnabled = false;
        let lastLoggedTime = 0;
        let selectedCameraId = "";
        let currentTargetObject = null;
        let lastFrameTime = performance.now();
        let fpsCount = 0;

        // Cache DOM Elements
        const modelStatusBadge = document.getElementById('modelStatusBadge');
        const modelStatusText = document.getElementById('modelStatusText');
        const liveClock = document.getElementById('liveClock');
        const cameraSelect = document.getElementById('cameraSelect');
        const toggleCameraBtn = document.getElementById('toggleCameraBtn');
        const cameraBtnText = document.getElementById('cameraBtnText');
        const videoPlaceholder = document.getElementById('videoPlaceholder');
        const quickStartBtn = document.getElementById('quickStartBtn');
        const videoFeed = document.getElementById('videoFeed');
        const detectionCanvas = document.getElementById('detectionCanvas');
        const scanningHUD = document.getElementById('scanningHUD');
        const hudFPS = document.getElementById('hudFPS');
        const hudResolution = document.getElementById('hudResolution');
        const confidenceThreshold = document.getElementById('confidenceThreshold');
        const confidenceValue = document.getElementById('confidenceValue');
        const autoCaptureToggle = document.getElementById('autoCaptureToggle');
        
        // Input form controls
        const targetClassInput = document.getElementById('targetClassInput');
        const targetWeightInput = document.getElementById('targetWeightInput');
        const targetZoneSelect = document.getElementById('targetZoneSelect');
        const targetShelfInput = document.getElementById('targetShelfInput');
        const targetSupplierInput = document.getElementById('targetSupplierInput');
        const formLockStatus = document.getElementById('formLockStatus');
        const resetTargetBtn = document.getElementById('resetTargetBtn');
        const manualCaptureBtn = document.getElementById('manualCaptureBtn');

        // Output Display panel
        const genUUID = document.getElementById('genUUID');
        const genSKUPrefix = document.getElementById('genSKUPrefix');
        const genClassName = document.getElementById('genClassName');
        const genVerified = document.getElementById('genVerified');
        const scannerNotification = document.getElementById('scannerNotification');
        const scannerNotificationText = document.getElementById('scannerNotificationText');
        const barcodeCanvas = document.getElementById('barcodeCanvas');
        const barcodeFallback = document.getElementById('barcodeFallback');

        // Buttons
        const copyUIDBtn = document.getElementById('copyUIDBtn');
        const printLabelBtn = document.getElementById('printLabelBtn');
        const exportCsvBtn = document.getElementById('exportCsvBtn');
        const clearLogsBtn = document.getElementById('clearLogsBtn');
        
        // Statistics
        const statTotal = document.getElementById('statTotal');
        const statHighConf = document.getElementById('statHighConf');
        const statZones = document.getElementById('statZones');

        // Search & Registry
        const registrySearch = document.getElementById('registrySearch');
        const registryList = document.getElementById('registryList');
        const registryEmptyState = document.getElementById('registryEmptyState');

        // Canvas 2D contexts
        const ctx = detectionCanvas.getContext('2d');

        // --- CORE INITIALIZATION ---
        window.addEventListener('DOMContentLoaded', async () => {
            updateClock();
            setInterval(updateClock, 1000);
            
            // Check Local Storage for existing items
            loadInventoryFromLocalStorage();
            
            // Populate Camera selector dropdown
            await initCameraDevices();

            // Load TensorFlow.js Coco-SSD model
            await loadAIModel();

            // Setup Event Listeners
            setupEventListeners();
        });

        // Live clock generator
        function updateClock() {
            const now = new Date();
            liveClock.innerHTML = `<i class="fa-regular fa-clock text-indigo-400"></i> ${now.toLocaleTimeString()}`;
        }

        // --- MODEL LOADING ---
        async function loadAIModel() {
            try {
                modelStatusText.innerText = "Downloading Neural Model...";
                // Load mobilenet_v2 based model for good accuracy vs speed ratio
                model = await cocoSsd.load({ base: 'lite_mobilenet_v2' });
                isModelLoading = false;
                
                modelStatusBadge.classList.remove('bg-amber-500/10', 'border-amber-500/20', 'text-amber-400');
                modelStatusBadge.classList.add('bg-emerald-500/10', 'border-emerald-500/20', 'text-emerald-400');
                modelStatusText.innerText = "Vision Engine Ready";
            } catch (err) {
                console.error("Failed to compile ML model: ", err);
                modelStatusText.innerText = "Fallback Mode Engaged";
                modelStatusBadge.classList.remove('bg-amber-500/10', 'text-amber-400');
                modelStatusBadge.classList.add('bg-rose-500/10', 'border-rose-500/20', 'text-rose-400');
            }
        }

        // --- WEBCAM MANAGEMENT ---
        async function initCameraDevices() {
            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
                    return;
                }
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                
                cameraSelect.innerHTML = '<option value="">Standard Cam</option>';
                videoDevices.forEach((device, index) => {
                    const label = device.label || `Camera ${index + 1}`;
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = label;
                    cameraSelect.appendChild(option);
                });
            } catch (err) {
                console.warn("Device mapping error: ", err);
            }
        }

        async function startWebcam() {
            try {
                // Remove fallback placeholder UI
                videoPlaceholder.classList.add('hidden');
                scanningHUD.classList.remove('hidden');

                const constraints = {
                    audio: false,
                    video: selectedCameraId ? { deviceId: { exact: selectedCameraId } } : { facingMode: "environment" }
                };

                videoStream = await navigator.mediaDevices.getUserMedia(constraints);
                videoFeed.srcObject = videoStream;
                videoFeed.addEventListener('loadedmetadata', () => {
                    // Update canvas coordinates once video bounds are acquired
                    detectionCanvas.width = videoFeed.videoWidth;
                    detectionCanvas.height = videoFeed.videoHeight;
                    hudResolution.innerText = `Res: ${videoFeed.videoWidth}x${videoFeed.videoHeight}`;
                });

                isCameraActive = true;
                cameraBtnText.innerText = "Pause Feed";
                toggleCameraBtn.classList.remove('bg-indigo-600', 'hover:bg-indigo-500');
                toggleCameraBtn.classList.add('bg-rose-600', 'hover:bg-rose-500');

                // Fire animation / inference cycle
                requestAnimationFrame(renderDetectionLoop);
            } catch (err) {
                console.error("Camera access failed: ", err);
                showNotification("Camera error: Verify hardware & permissions", "error");
                videoPlaceholder.classList.remove('hidden');
                scanningHUD.classList.add('hidden');
            }
        }

        function stopWebcam() {
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
            }
            videoFeed.srcObject = null;
            isCameraActive = false;
            cameraBtnText.innerText = "Start Feed";
            toggleCameraBtn.classList.remove('bg-rose-600', 'hover:bg-rose-500');
            toggleCameraBtn.classList.add('bg-indigo-600', 'hover:bg-indigo-500');
            videoPlaceholder.classList.remove('hidden');
            scanningHUD.classList.add('hidden');
            
            // Clean viewport canvas
            ctx.clearRect(0, 0, detectionCanvas.width, detectionCanvas.height);
        }

        // --- COMPUTER VISION & RENDERING LOOP ---
        async function renderDetectionLoop() {
            if (!isCameraActive) return;

            // Compute FPS
            const now = performance.now();
            const fps = Math.round(1000 / (now - lastFrameTime));
            lastFrameTime = now;
            hudFPS.innerText = `FPS: ${fps}`;

            // Draw video source frames to active UI Canvas
            ctx.drawImage(videoFeed, 0, 0, detectionCanvas.width, detectionCanvas.height);

            // Execute ML inference only if the model has loaded successfully
            if (model && !isModelLoading) {
                try {
                    const threshold = parseFloat(confidenceThreshold.value) / 100;
                    const predictions = await model.detect(videoFeed);
                    
                    // Filter predictions by user confidence threshold
                    currentPredictions = predictions.filter(pred => pred.score >= threshold);
                    
                    // Highlight bounding boxes on Canvas overlay
                    drawDetectionBoundingBoxes();

                    // Logic to locks/isolate highest confidence product
                    evaluateTargetIsolation();
                } catch (e) {
                    console.error("Inference loop error:", e);
                }
            } else {
                // If AI hasn't completed loading, display simple warning
                ctx.fillStyle = "rgba(0,0,0,0.5)";
                ctx.fillRect(0, 0, detectionCanvas.width, detectionCanvas.height);
                ctx.fillStyle = "#fbbf24"; // Amber
                ctx.font = "14px 'Plus Jakarta Sans'";
                ctx.textAlign = "center";
                ctx.fillText("Deep Learning Model Loading...", detectionCanvas.width / 2, detectionCanvas.height / 2);
            }

            requestAnimationFrame(renderDetectionLoop);
        }

        function drawDetectionBoundingBoxes() {
            currentPredictions.forEach(pred => {
                const [x, y, w, h] = pred.bbox;
                
                // Draw elegant, high-tech glowing bounds
                ctx.strokeStyle = '#6366f1'; // Indigo 500
                ctx.lineWidth = 3;
                ctx.shadowColor = 'rgba(99, 102, 241, 0.4)';
                ctx.shadowBlur = 10;
                ctx.strokeRect(x, y, w, h);
                
                // Draw solid corner brackets
                ctx.strokeStyle = '#a5b4fc'; // Indigo 300
                ctx.lineWidth = 4;
                ctx.beginPath();
                // Top-Left corner
                ctx.moveTo(x, y + 15); ctx.lineTo(x, y); ctx.lineTo(x + 15, y);
                // Top-Right corner
                ctx.moveTo(x + w, y + 15); ctx.lineTo(x + w, y); ctx.lineTo(x + w - 15, y);
                // Bottom-Left corner
                ctx.moveTo(x, y + h - 15); ctx.lineTo(x, y + h); ctx.lineTo(x + 15, y + h);
                // Bottom-Right corner
                ctx.moveTo(x + w, y + h - 15); ctx.lineTo(x + w, y + h); ctx.lineTo(x + w - 15, y + h);
                ctx.stroke();

                // Draw overlay badge
                ctx.shadowBlur = 0; // reset shadow
                ctx.fillStyle = 'rgba(15, 23, 42, 0.85)'; // Slate 900 translucent
                ctx.fillRect(x, y - 25, Math.max(w, 140), 25);
                
                // Label string
                ctx.fillStyle = '#f8fafc'; // White/Slate 50
                ctx.font = "bold 11px 'JetBrains Mono'";
                ctx.textAlign = "left";
                const label = `${pred.class.toUpperCase()} (${(pred.score * 100).toFixed(0)}%)`;
                ctx.fillText(label, x + 6, y - 8);
            });
        }

        // Isolate single high-conf object and map parameters to registration panels
        function evaluateTargetIsolation() {
            if (currentPredictions.length === 0) {
                formLockStatus.innerHTML = `<span class="text-amber-500 font-semibold flex items-center gap-1"><i class="fa-solid fa-hourglass"></i> Scanning...</span>`;
                return;
            }

            // Pick the target closest to center frame or largest surface area
            const primaryTarget = currentPredictions.reduce((prev, current) => {
                return (prev.bbox[2] * prev.bbox[3] > current.bbox[2] * current.bbox[3]) ? prev : current;
            });

            // If a different class is isolated, populate variables & database builder forms
            if (!currentTargetObject || currentTargetObject.class !== primaryTarget.class) {
                currentTargetObject = primaryTarget;
                
                // Fill details from dynamic list if available, or generate standard values
                const defaults = DEMO_ITEMS.find(item => item.class === primaryTarget.class.toLowerCase()) || {
                    class: primaryTarget.class,
                    zone: 'Zone-B',
                    shelf: `SHELF-${String.fromCharCode(65 + Math.floor(Math.random() * 26))}${Math.floor(100 + Math.random() * 800)}`,
                    weight: parseFloat((0.5 + Math.random() * 15).toFixed(1)),
                    supplier: 'Unspecified Intake'
                };

                targetClassInput.value = primaryTarget.class;
                targetWeightInput.value = defaults.weight;
                targetZoneSelect.value = defaults.zone;
                targetShelfInput.value = defaults.shelf;
                targetSupplierInput.value = defaults.supplier;

                formLockStatus.innerHTML = `<span class="text-emerald-400 font-bold flex items-center gap-1"><i class="fa-solid fa-lock"></i> Locked On Target</span>`;

                // Update real-time visualization preview panel
                stageVisualTrackingCard(primaryTarget.class, defaults.zone, defaults.shelf);

                // Auto-Intake logic: Capture immediately if toggled
                if (autoCaptureEnabled) {
                    const rightNow = Date.now();
                    // Enforce debounced log rate (min 3.5 seconds between continuous logs)
                    if (rightNow - lastLoggedTime > 3500) {
                        lastLoggedTime = rightNow;
                        executeIntakeAction();
                    }
                }
            }
        }

        // Stage details to the interactive Card on the Right Column (before committing to inventory list)
        function stageVisualTrackingCard(className, zone, shelf) {
            // Instantly spawn a temporary high-tech UUID
            const generatedUID = generateAlphanumericUID(className, zone);
            const generatedSKU = `SKU-${className.substring(0, 3).toUpperCase()}-${shelf}`;

            genUUID.innerText = generatedUID;
            genSKUPrefix.innerText = generatedSKU;
            genClassName.innerText = className.charAt(0).toUpperCase() + className.slice(1);
            
            // Build real barcode
            renderBarcode(generatedUID);
        }

        // Barcode Generation wrapper
        function renderBarcode(text) {
            try {
                JsBarcode("#barcodeCanvas", text, {
                    format: "CODE128",
                    width: 1.5,
                    height: 50,
                    displayValue: true,
                    lineColor: "#0f172a", // Dark charcoal lines
                    font: "monospace",
                    fontSize: 11
                });
                barcodeCanvas.classList.remove('hidden');
                barcodeFallback.classList.add('hidden');
            } catch (err) {
                barcodeCanvas.classList.add('hidden');
                barcodeFallback.classList.remove('hidden');
                barcodeFallback.innerText = text;
            }
        }

        // Helper Alphanumeric ID Serializer
        function generateAlphanumericUID(itemClass, zone) {
            const dateStr = new Date().toISOString().slice(2,10).replace(/-/g, "");
            const randomID = Math.random().toString(36).substr(2, 5).toUpperCase();
            const clName = itemClass.slice(0, 2).toUpperCase();
            const znCode = zone.replace('Zone-', '');
            
            // Format: WF-[CLASS][ZONE]-[DATE]-[RANDOM_5]
            // e.g: WF-BOA-260628-9X3T2
            return `WF-${clName}${znCode}-${dateStr}-${randomID}`;
        }

        // --- INTAKE & SYSTEM ACTIONS ---
        function executeIntakeAction() {
            const itemClass = targetClassInput.value.trim();
            if (!itemClass) {
                showNotification("No isolated object to register", "warning");
                return;
            }

            const currentId = genUUID.innerText;
            if (currentId === "AWAITING_LOCK" || currentId === "") {
                showNotification("Awaiting vision system calibration", "warning");
                return;
            }

            // Check if item was already registered
            if (detectedItemsLog.find(item => item.id === currentId)) {
                return; // Guard duplicate registers on instant frames
            }

            const sku = genSKUPrefix.innerText;
            const weight = parseFloat(targetWeightInput.value) || 0.5;
            const zone = targetZoneSelect.value;
            const shelf = targetShelfInput.value.trim() || 'SHELF-00';
            const supplier = targetSupplierInput.value.trim() || 'Automated Line';
            const timestamp = new Date().toLocaleString();

            const record = {
                id: currentId,
                sku: sku,
                class: itemClass,
                weight: weight,
                zone: zone,
                shelf: shelf,
                supplier: supplier,
                timestamp: timestamp,
                confidence: currentPredictions.length > 0 ? (currentPredictions[0].score * 100).toFixed(0) : "Manual Override"
            };

            // Push to head of register log
            detectedItemsLog.unshift(record);
            
            // Save & update display tables
            saveInventoryToLocalStorage();
            renderInventoryRegistry();
            calculateWarehouseStatistics();

            // Sound feedback using Web Audio API synthesis
            playBeepTone(440, 100);

            showNotification(`Intaked: ${itemClass.toUpperCase()} locked to ${zone}`, "success");
        }

        // Synthesize dynamic beep on lock
        function playBeepTone(freq, dur) {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();

                oscillator.type = 'sine';
                oscillator.frequency.value = freq;
                oscillator.connect(gainNode);
                
                gainNode.connect(audioCtx.destination);
                gainNode.gain.setValueAtTime(0.08, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur/1000);

                oscillator.start(audioCtx.currentTime);
                oscillator.stop(audioCtx.currentTime + dur/1000);
            } catch (err) {
                // AudioContext blocked or not supported
            }
        }

        // --- EVENT LISTENERS REGISTRATION ---
        function setupEventListeners() {
            // Camera toggle
            toggleCameraBtn.addEventListener('click', () => {
                if (isCameraActive) {
                    stopWebcam();
                } else {
                    startWebcam();
                }
            });

            quickStartBtn.addEventListener('click', () => {
                startWebcam();
            });

            // Camera selector change
            cameraSelect.addEventListener('change', (e) => {
                selectedCameraId = e.target.value;
                if (isCameraActive) {
                    stopWebcam();
                    startWebcam();
                }
            });

            // Target slider threshold change
            confidenceThreshold.addEventListener('input', (e) => {
                confidenceValue.innerText = `${e.target.value}%`;
            });

            // Toggle autonomous auto logging
            autoCaptureToggle.addEventListener('change', (e) => {
                autoCaptureEnabled = e.target.checked;
                showNotification(
                    autoCaptureEnabled ? "Autonomous capture active!" : "System switched to manual logs",
                    autoCaptureEnabled ? "success" : "warning"
                );
            });

            // Reset manual form inputs
            resetTargetBtn.addEventListener('click', () => {
                currentTargetObject = null;
                targetClassInput.value = "";
                targetWeightInput.value = "1.0";
                targetZoneSelect.value = "Zone-B";
                targetShelfInput.value = "SHELF-B01";
                targetSupplierInput.value = "Automated Line";
                genUUID.innerText = "AWAITING_LOCK";
                genSKUPrefix.innerText = "SKU-GEN";
                genClassName.innerText = "No active target";
                
                // Clear SVG Canvas barcode
                const bSvg = document.getElementById('barcodeCanvas');
                bSvg.innerHTML = "";
            });

            // Manual ingest button click
            manualCaptureBtn.addEventListener('click', () => {
                // If form class is typed but no UUID is set, synthesize a mock one on the spot
                if (genUUID.innerText === "AWAITING_LOCK" && targetClassInput.value.trim() !== "") {
                    stageVisualTrackingCard(targetClassInput.value.trim(), targetZoneSelect.value, targetShelfInput.value);
                }
                executeIntakeAction();
            });

            // Clipboard copies
            copyUIDBtn.addEventListener('click', () => {
                const uid = genUUID.innerText;
                if (uid === "AWAITING_LOCK") {
                    showNotification("Nothing to copy", "warning");
                    return;
                }
                
                // Use standard executeCommand fallback for Canvas environment security rules
                const el = document.createElement('textarea');
                el.value = uid;
                document.body.appendChild(el);
                el.select();
                document.execCommand('copy');
                document.body.removeChild(el);

                showNotification("UID Copied to Clipboard!", "success");
            });

            // Print Label
            printLabelBtn.addEventListener('click', () => {
                const uid = genUUID.innerText;
                if (uid === "AWAITING_LOCK") {
                    showNotification("Nothing to print yet. Scan an object.", "warning");
                    return;
                }
                triggerStickerPrint();
            });

            // CSV Export
            exportCsvBtn.addEventListener('click', () => {
                exportRegistryAsCSV();
            });

            // Clear Log
            clearLogsBtn.addEventListener('click', () => {
                if (confirm("Are you sure you want to flush all inventory records?")) {
                    detectedItemsLog = [];
                    saveInventoryToLocalStorage();
                    renderInventoryRegistry();
                    calculateWarehouseStatistics();
                    showNotification("Local ledger flushed successfully", "warning");
                }
            });

            // Live Search filter
            registrySearch.addEventListener('input', () => {
                renderInventoryRegistry();
            });
        }

        // --- LOCAL STORAGE PERSISTENCE ---
        function saveInventoryToLocalStorage() {
            localStorage.setItem('warehouse_flow_registry', JSON.stringify(detectedItemsLog));
        }

        function loadInventoryFromLocalStorage() {
            const data = localStorage.getItem('warehouse_flow_registry');
            if (data) {
                detectedItemsLog = JSON.parse(data);
                renderInventoryRegistry();
                calculateWarehouseStatistics();
            }
        }

        // --- LEDGER TABLE RENDER & UI UPDATES ---
        function renderInventoryRegistry() {
            const searchTerm = registrySearch.value.trim().toLowerCase();
            
            // Clear prior dynamic list
            const existingRows = registryList.querySelectorAll('.registry-item-row');
            existingRows.forEach(row => row.remove());

            const filteredItems = detectedItemsLog.filter(item => {
                return item.id.toLowerCase().includes(searchTerm) ||
                       item.class.toLowerCase().includes(searchTerm) ||
                       item.sku.toLowerCase().includes(searchTerm) ||
                       item.zone.toLowerCase().includes(searchTerm) ||
                       item.shelf.toLowerCase().includes(searchTerm);
            });

            if (filteredItems.length === 0) {
                registryEmptyState.classList.remove('hidden');
                return;
            } else {
                registryEmptyState.classList.add('hidden');
            }

            filteredItems.forEach(item => {
                const row = document.createElement('div');
                row.className = "registry-item-row bg-slate-950/70 border border-slate-800 hover:border-slate-700/80 p-3 rounded-xl flex flex-col md:flex-row justify-between gap-3 text-xs transition-colors";
                
                // Color mapping for zones
                let zoneColor = "bg-slate-800 text-slate-300";
                if (item.zone === "Zone-A") zoneColor = "bg-indigo-500/10 text-indigo-300 border border-indigo-500/20";
                if (item.zone === "Zone-B") zoneColor = "bg-sky-500/10 text-sky-300 border border-sky-500/20";
                if (item.zone === "Zone-C") zoneColor = "bg-teal-500/10 text-teal-300 border border-teal-500/20";
                if (item.zone === "Zone-D") zoneColor = "bg-rose-500/10 text-rose-300 border border-rose-500/20";

                row.innerHTML = `
                    <div class="flex-grow flex flex-col gap-1.5">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="font-bold text-slate-200 text-sm uppercase flex items-center gap-1">
                                <i class="fa-solid fa-cube text-slate-400"></i> ${item.class}
                            </span>
                            <span class="text-[9px] px-2 py-0.5 rounded font-bold code-font bg-slate-800 text-indigo-300">
                                ${item.sku}
                            </span>
                            <span class="text-[9px] px-2 py-0.5 rounded-full font-semibold ${zoneColor}">
                                ${item.zone} &bull; ${item.shelf}
                            </span>
                        </div>
                        <div class="text-[10px] text-slate-400 flex flex-wrap items-center gap-x-3 gap-y-1 font-mono">
                            <span class="text-indigo-400 font-bold">${item.id}</span>
                            <span>&bull;</span>
                            <span>Weight: <strong class="text-slate-300">${item.weight} kg</strong></span>
                            <span>&bull;</span>
                            <span>Intake: <strong class="text-slate-300">${item.timestamp}</strong></span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 self-end md:self-center">
                        <button onclick="printRowLabel('${item.id}')" title="Print Sticker Label" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 p-2 text-slate-300 hover:text-white rounded-lg transition-all">
                            <i class="fa-solid fa-print"></i>
                        </button>
                        <button onclick="deleteRowRecord('${item.id}')" title="Delete Entry" class="bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 p-2 text-red-400 rounded-lg transition-all">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                `;

                registryList.appendChild(row);
            });
        }

        function calculateWarehouseStatistics() {
            statTotal.innerText = detectedItemsLog.length;
            
            // Count entries mapped to highest accuracy threshold >= 80%
            const highConfCount = detectedItemsLog.filter(item => {
                if (item.confidence === "Manual Override") return false;
                return parseInt(item.confidence) >= 80;
            }).length;
            
            statHighConf.innerText = highConfCount;

            // Compute unique zones currently holding cargo
            const uniqueZonesSet = new Set(detectedItemsLog.map(item => item.zone));
            statZones.innerText = uniqueZonesSet.size || 0;
        }

        // --- GLOBAL REGISTER OPERATIONS ---
        window.deleteRowRecord = function(id) {
            detectedItemsLog = detectedItemsLog.filter(item => item.id !== id);
            saveInventoryToLocalStorage();
            renderInventoryRegistry();
            calculateWarehouseStatistics();
            showNotification("Item record deleted", "warning");
        };

        window.printRowLabel = function(id) {
            const item = detectedItemsLog.find(item => item.id === id);
            if (!item) return;

            // Render details to sticker template
            document.getElementById('printUID').innerText = item.id;
            document.getElementById('printSKU').innerText = item.sku;
            document.getElementById('printItem').innerText = item.class.toUpperCase();
            document.getElementById('printZone').innerText = item.zone;
            document.getElementById('printShelf').innerText = item.shelf;
            document.getElementById('printWeight').innerText = `${item.weight} kg`;
            document.getElementById('printDate').innerText = item.timestamp;

            // Generate clean printing barcode representation
            setTimeout(() => {
                try {
                    JsBarcode("#printBarcodeCanvas", item.id, {
                        format: "CODE128",
                        width: 1.6,
                        height: 40,
                        displayValue: false,
                        lineColor: "#000000"
                    });
                    
                    const printContents = document.getElementById('printStickerTemplate').innerHTML;
                    const originalContents = document.body.innerHTML;
                    
                    // Create window/iframe mechanism to print sticker frame cleanly
                    const printWindow = window.open('', '_blank', 'width=450,height=600');
                    printWindow.document.write('<html><head><title>Sticker Label Printing</title>');
                    printWindow.document.write('</head><body>');
                    printWindow.document.write(printContents);
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    
                    printWindow.focus();
                    // Let assets render
                    setTimeout(() => {
                        printWindow.print();
                        printWindow.close();
                    }, 400);

                } catch (err) {
                    console.error(err);
                    showNotification("Failure preparing label template", "error");
                }
            }, 100);
        };

        function triggerStickerPrint() {
            // Pick currently visual staged product parameters from left screen details
            const uid = genUUID.innerText;
            const sku = genSKUPrefix.innerText;
            const itemClass = targetClassInput.value;
            const zone = targetZoneSelect.value;
            const shelf = targetShelfInput.value;
            const weight = targetWeightInput.value;

            // Render sticker elements
            document.getElementById('printUID').innerText = uid;
            document.getElementById('printSKU').innerText = sku;
            document.getElementById('printItem').innerText = itemClass.toUpperCase();
            document.getElementById('printZone').innerText = zone;
            document.getElementById('printShelf').innerText = shelf;
            document.getElementById('printWeight').innerText = `${weight} kg`;
            document.getElementById('printDate').innerText = new Date().toLocaleString();

            setTimeout(() => {
                try {
                    JsBarcode("#printBarcodeCanvas", uid, {
                        format: "CODE128",
                        width: 1.6,
                        height: 40,
                        displayValue: false,
                        lineColor: "#000000"
                    });
                    
                    const printContents = document.getElementById('printStickerTemplate').innerHTML;
                    const printWindow = window.open('', '_blank', 'width=450,height=600');
                    printWindow.document.write('<html><head><title>Sticker Label Printing</title></head><body>');
                    printWindow.document.write(printContents);
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    
                    printWindow.focus();
                    setTimeout(() => {
                        printWindow.print();
                        printWindow.close();
                    }, 400);
                } catch (e) {
                    showNotification("Failed creating print window", "error");
                }
            }, 100);
        }

        // --- CSV SPREADSHEET EXPORTER ---
        function exportRegistryAsCSV() {
            if (detectedItemsLog.length === 0) {
                showNotification("No records available to export", "warning");
                return;
            }

            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "UUID,SKU,Item Class,Estimated Weight(kg),Warehouse Zone,Shelf Location,Supplier,Log Time,ML Confidence\n";

            detectedItemsLog.forEach(row => {
                const fields = [
                    `"${row.id}"`,
                    `"${row.sku}"`,
                    `"${row.class}"`,
                    `"${row.weight}"`,
                    `"${row.zone}"`,
                    `"${row.shelf}"`,
                    `"${row.supplier}"`,
                    `"${row.timestamp}"`,
                    `"${row.confidence}%"`
                ];
                csvContent += fields.join(",") + "\n";
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `warehouse_flow_registry_${new Date().toISOString().slice(0,10)}.csv`);
            document.body.appendChild(link); // Required for FF
            link.click();
            document.body.removeChild(link);
            showNotification("Inventory database CSV generated", "success");
        }

        // --- IN-APP INTEGRATED TOAST ---
        function showNotification(msg, type = "success") {
            scannerNotificationText.innerText = msg;
            
            // Adjust visual themes based on priority
            scannerNotification.className = "px-4 py-3 flex items-center justify-between text-xs transition-all duration-300 rounded-b-2xl border-t";
            if (type === "success") {
                scannerNotification.classList.add("bg-indigo-950/90", "text-indigo-300", "border-indigo-500/25");
            } else if (type === "warning") {
                scannerNotification.classList.add("bg-amber-950/90", "text-amber-300", "border-amber-500/25");
            } else {
                scannerNotification.classList.add("bg-rose-950/90", "text-rose-300", "border-rose-500/25");
            }

            // Slide up & show
            scannerNotification.style.opacity = "1";
            scannerNotification.style.transform = "translateY(0px)";

            // Dismiss automatically
            setTimeout(() => {
                scannerNotification.style.opacity = "0";
                scannerNotification.style.transform = "translateY(8px)";
            }, 3000);
        }

    </script>
</body>
</html>
