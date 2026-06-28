<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Vision: Thermal Intelligence</title>
    <!-- Load TensorFlow.js and COCO-SSD -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
    <!-- Load face-api.js -->
    <script src="https://cdn.jsdelivr.net/npm/@vladmandic/face-api/dist/face-api.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .video-container {
            position: relative;
            width: 640px;
            height: 480px;
            background: #020617;
            border-radius: 1.5rem;
            overflow: hidden;
            box-shadow: 0 0 60px -10px rgba(245, 158, 11, 0.4);
            border: 2px solid #451a03;
        }
        #webcam {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            visibility: hidden; /* Keep hidden while we process thermal frames */
        }
        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            z-index: 10;
            width: 100%;
            height: 100%;
        }
        .glow-text {
            text-shadow: 0 0 10px rgba(245, 158, 11, 0.8);
        }
        .hud-overlay {
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 20;
            background: 
                linear-gradient(to right, #f59e0b 2px, transparent 2px) 0 0,
                linear-gradient(to bottom, #f59e0b 2px, transparent 2px) 0 0,
                linear-gradient(to left, #f59e0b 2px, transparent 2px) 100% 0,
                linear-gradient(to bottom, #f59e0b 2px, transparent 2px) 100% 0,
                linear-gradient(to right, #f59e0b 2px, transparent 2px) 0 100%,
                linear-gradient(to top, #f59e0b 2px, transparent 2px) 0 100%,
                linear-gradient(to left, #f59e0b 2px, transparent 2px) 100% 100%,
                linear-gradient(to top, #f59e0b 2px, transparent 2px) 100% 100%;
            background-repeat: no-repeat;
            background-size: 20px 20px;
            opacity: 0.4;
        }
    </style>
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-center p-4">

    <div class="max-w-5xl w-full space-y-6 text-center">
        <header class="space-y-1">
            <h1 class="text-6xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-orange-400 via-red-500 to-amber-600 italic">
                THERMAL SCAN AI
            </h1>
            <p class="text-orange-500 font-mono tracking-[0.3em] uppercase text-[10px] glow-text">Infrared Spectral Matrix v5.2</p>
        </header>

        <!-- Boot Sequence -->
        <div id="loading-overlay" class="py-16 flex flex-col items-center space-y-6">
            <div class="relative w-24 h-24">
                <div class="absolute inset-0 border-4 border-orange-500/20 rounded-full"></div>
                <div class="absolute inset-0 border-4 border-t-orange-400 rounded-full animate-spin"></div>
            </div>
            <p id="status-text" class="text-orange-400 font-mono text-sm animate-pulse">Engaging Optical Sensors...</p>
        </div>

        <!-- Advanced UI -->
        <div id="main-ui" class="hidden flex flex-col items-center space-y-6">
            <div class="video-container">
                <div class="hud-overlay"></div>
                <video id="webcam" autoplay muted playsinline></video>
                <canvas id="overlay"></canvas>
                
                <!-- On-Screen Telemetry -->
                <div class="absolute top-6 left-6 z-30 font-mono text-[10px] text-orange-400 text-left space-y-1">
                    <p>MODE: THERMAL_STREAMS</p>
                    <p>TEMP: <span id="temp-val">36.2</span>°C</p>
                    <p>SIGNAL: STABLE</p>
                </div>
                <div class="absolute bottom-6 right-6 z-30 font-mono text-[10px] text-orange-400 text-right">
                    <p class="animate-pulse">● FEED_ACTIVE</p>
                    <p id="clock">00:00:00</p>
                </div>
            </div>

            <!-- Data Dashboard -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-4xl">
                <div class="bg-slate-900/80 backdrop-blur-xl p-4 rounded-xl border border-orange-500/30">
                    <h3 class="text-[10px] text-slate-500 font-bold uppercase mb-2 tracking-widest">Heat Targets</h3>
                    <div id="object-count" class="text-4xl font-black text-orange-500">00</div>
                </div>
                
                <div class="bg-slate-900/80 backdrop-blur-xl p-4 rounded-xl border border-red-500/30">
                    <h3 class="text-[10px] text-slate-500 font-bold uppercase mb-2 tracking-widest">Biometric Data</h3>
                    <div id="emotion-status" class="text-2xl font-black text-red-500 truncate">INIT</div>
                </div>

                <div class="bg-slate-900/80 backdrop-blur-xl p-4 rounded-xl border border-amber-500/30">
                    <h3 class="text-[10px] text-slate-500 font-bold uppercase mb-2 tracking-widest">System Status</h3>
                    <div id="system-status" class="text-xs font-mono text-amber-500 py-2">OPTIMAL</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const video = document.getElementById('webcam');
        const canvas = document.getElementById('overlay');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const statusText = document.getElementById('status-text');
        
        const objectCountDisp = document.getElementById('object-count');
        const emotionStatusDisp = document.getElementById('emotion-status');

        let objectModel;
        let lastSpeakTime = 0;
        let lastDominantObject = "";

        function getThermalColor(v) {
            let r = 0, g = 0, b = 0;
            if (v < 64) {
                b = 255; g = 4 * v;
            } else if (v < 128) {
                b = 255 - 4 * (v - 64); g = 255;
            } else if (v < 192) {
                r = 4 * (v - 128); g = 255;
            } else {
                r = 255; g = 255 - 4 * (v - 192);
            }
            return [r, g, b];
        }

        function speak(text) {
            if (Date.now() - lastSpeakTime < 5000) return;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0; 
            utterance.pitch = 0.8; 
            window.speechSynthesis.speak(utterance);
            lastSpeakTime = Date.now();
        }

        async function startVideo() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { width: 640, height: 480, frameRate: { ideal: 30 } },
                    audio: false
                });
                video.srcObject = stream;
                return new Promise((resolve) => {
                    video.onloadedmetadata = () => {
                        video.play();
                        resolve();
                    };
                });
            } catch (err) {
                statusText.innerText = "CAMERA ACCESS DENIED: " + err.message;
                throw err;
            }
        }

        async function init() {
            try {
                statusText.innerText = "Loading AI Core...";
                objectModel = await cocoSsd.load();

                statusText.innerText = "Setting Up Biometrics...";
                const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/';
                await Promise.all([
                    faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
                    faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
                ]);

                statusText.innerText = "Requesting Video Feed...";
                await startVideo();

                canvas.width = 640;
                canvas.height = 480;
                document.getElementById('loading-overlay').classList.add('hidden');
                document.getElementById('main-ui').classList.remove('hidden');
                
                speak("Thermal imaging active. Video signal locked.");
                detectLoop();
            } catch (err) {
                console.error("Initialization Failed:", err);
            }
        }

        async function detectLoop() {
            if (video.paused || video.ended) return requestAnimationFrame(detectLoop);

            // 1. Capture and Process Mirroring
            ctx.save();
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            ctx.restore();

            // 2. Thermal Conversion
            const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = frame.data;
            for (let i = 0; i < data.length; i += 4) {
                const avg = (0.3 * data[i] + 0.59 * data[i+1] + 0.11 * data[i+2]);
                const [r, g, b] = getThermalColor(avg);
                data[i] = r; data[i+1] = g; data[i+2] = b;
            }
            ctx.putImageData(frame, 0, 0);

            // 3. AI Analysis
            const [objects, faces] = await Promise.all([
                objectModel.detect(video, 5, 0.4),
                faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions()
            ]);

            // HUD Data Update
            objectCountDisp.innerText = objects.length.toString().padStart(2, '0');
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
            document.getElementById('temp-val').innerText = (36 + Math.random()).toFixed(1);

            // 4. Drawing Overlays
            objects.forEach(obj => {
                let [x, y, w, h] = obj.bbox;
                x = canvas.width - x - w; // Mirror Adjustment

                ctx.strokeStyle = '#fbbf24';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, w, h);
                ctx.fillStyle = '#fbbf24';
                ctx.font = 'bold 10px monospace';
                ctx.fillText(obj.class.toUpperCase(), x, y - 5);
            });

            if (faces.length > 0) {
                const expressions = faces[0].expressions;
                const dominant = Object.entries(expressions).reduce((a, b) => a[1] > b[1] ? a : b);
                emotionStatusDisp.innerText = dominant[0].toUpperCase();
            }

            requestAnimationFrame(detectLoop);
        }

        window.onload = init;
    </script>
</body>
</html>
