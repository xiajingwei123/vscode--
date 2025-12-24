import React, { useState, useEffect, useRef, useCallback } from 'react';
import ChristmasCanvas from './components/ChristmasCanvas';
import { AudioFX } from './utils/audio';
// Use namespace imports to avoid "does not provide an export named" errors with some bundlers/CDNs
import * as handsLib from '@mediapipe/hands';
import * as cameraUtils from '@mediapipe/camera_utils';

// Safe access to the classes handling default export wrapping common in ESM CDN conversions
const Hands = (handsLib as any).Hands || (handsLib as any).default?.Hands;
const Camera = (cameraUtils as any).Camera || (cameraUtils as any).default?.Camera;

type GestureState = 'tree' | 'heart' | 'explode';

function App() {
  const [loading, setLoading] = useState(true);
  const [started, setStarted] = useState(false);
  const [currentState, setCurrentState] = useState<GestureState>('tree');
  const [showModal, setShowModal] = useState(true);
  const [showText, setShowText] = useState(false);
  const [noBtnPos, setNoBtnPos] = useState({ x: 0, y: 0 });

  const videoRef = useRef<HTMLVideoElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  
  // Hand tracking refs
  const lastStateRef = useRef<GestureState>('tree');

  // Load handlers
  const handleCanvasLoaded = useCallback(() => {
    setLoading(false);
  }, []);

  const handleStart = () => {
    setShowModal(false);
    AudioFX.init();
    if (audioRef.current) {
      audioRef.current.play().catch(e => console.log("Auto-play blocked:", e));
    }
    
    setTimeout(() => {
      setStarted(true);
      setShowText(true);
      // Start camera only after user interaction to avoid permission issues before start
      startCamera();
    }, 1000);
  };

  const handleNoHover = () => {
    if (window.innerWidth < 768) return;
    const x = Math.random() * 300 - 50;
    const y = Math.random() * 200 - 50;
    setNoBtnPos({ x, y });
  };

  const handleNoClick = () => {
    alert("骗你的，其实点了也没用！🎄🎄🎄");
  };

  // MediaPipe Logic
  const startCamera = useCallback(() => {
    if (!videoRef.current || !Hands || !Camera) {
      console.error("MediaPipe libraries not loaded correctly");
      return;
    }

    const hands = new Hands({
      locateFile: (file: string) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      }
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    hands.onResults((results: any) => {
      let newState: GestureState = 'tree';

      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        
        // Finger states
        const isIndexUp = landmarks[8].y < landmarks[6].y;
        const isMiddleUp = landmarks[12].y < landmarks[10].y;
        const isRingUp = landmarks[16].y < landmarks[14].y;
        const isPinkyUp = landmarks[20].y < landmarks[18].y;

        const fingersUp = [isIndexUp, isMiddleUp, isRingUp, isPinkyUp].filter(Boolean).length;

        if (fingersUp >= 4) {
          newState = 'explode';
        } else if (isIndexUp && isMiddleUp && !isRingUp && !isPinkyUp) {
          newState = 'heart';
        } else {
          newState = 'tree';
        }
      } else {
        newState = 'tree';
      }

      if (newState !== lastStateRef.current) {
        setCurrentState(newState);
        
        // Play SFX
        if (newState === 'explode') AudioFX.playScatter();
        if (newState === 'heart') AudioFX.playHeart();
        if (newState === 'tree' && lastStateRef.current !== 'tree') AudioFX.playTree();
        
        lastStateRef.current = newState;
      }
    });

    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        if (videoRef.current) {
          await hands.send({ image: videoRef.current });
        }
      },
      width: 640,
      height: 480
    });
    camera.start();
  }, []);

  return (
    <div className="w-full h-full relative overflow-hidden bg-[#050505] font-sans text-[#c5a880]">
      {/* Hidden Video for Input */}
      <video ref={videoRef} className="hidden" />

      {/* Audio */}
      <audio ref={audioRef} loop id="christmas-music">
        <source src="https://music.163.com/song/media/outer/url?id=2153919351.mp3" type="audio/mpeg" />
      </audio>

      {/* Loading */}
      {loading && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 text-white">
          加载中...
        </div>
      )}

      {/* 3D Scene */}
      <ChristmasCanvas targetState={currentState} onLoaded={handleCanvasLoaded} />

      {/* Gesture Guide */}
      <div className={`fixed bottom-[30px] right-[30px] z-50 text-sm leading-[1.8] text-[#c5a880]/90 text-right pointer-events-none drop-shadow-[0_0_8px_rgba(0,0,0,0.8)] font-['Microsoft_YaHei'] transition-opacity duration-1000 ${showText ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[20px]'}`}>
        <div className="flex items-center justify-end gap-[10px]">
          <span>✋ 散开·漫天星河</span>
        </div>
        <div className="flex items-center justify-end gap-[10px]">
          <span>✌️ 凝聚·爱心</span>
        </div>
        <div className="flex items-center justify-end gap-[10px]">
          <span>✊ 还原·圣诞树</span>
        </div>
      </div>

      {/* Start Modal */}
      <div 
        className={`fixed inset-0 bg-black/95 z-[999] flex flex-col justify-center items-center transition-opacity duration-1000 ${!showModal ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
      >
        <div className="bg-[linear-gradient(145deg,#1a1a1a,#2a2a2a)] p-10 rounded-[20px] border-2 border-[#c5a880] shadow-[0_0_30px_rgba(197,168,128,0.3)] text-center max-w-[90%] w-[400px]">
          <div className="text-[2rem] text-[#c5a880] mb-5 font-bold">🎁 圣诞礼物</div>
          <p className="text-[1.1rem] text-[#ccc] mb-[30px]">
            叮咚！TangLiang你有一份来自圣诞老人的专属礼物，是否查收？
          </p>
          <div className="flex justify-around gap-5 relative">
            <button 
              className="px-[30px] py-[12px] border-none rounded-[50px] text-[1rem] cursor-pointer transition-all duration-300 font-bold outline-none bg-[#333] text-[#888] border border-[#555]"
              style={{ transform: `translate(${noBtnPos.x}px, ${noBtnPos.y}px)` }}
              onMouseEnter={handleNoHover}
              onClick={handleNoClick}
            >
              俺不中嘞，点右边
            </button>
            <button 
              className="px-[30px] py-[12px] border-none rounded-[50px] text-[1rem] cursor-pointer transition-all duration-300 font-bold outline-none bg-gradient-to-r from-[#d4af37] to-[#c5a880] text-black shadow-[0_0_15px_rgba(212,175,55,0.5)] hover:scale-105 hover:shadow-[0_0_25px_rgba(212,175,55,0.8)]"
              onClick={handleStart}
            >
              哦豁，开心收下
            </button>
          </div>
        </div>
      </div>

      {/* Christmas Text */}
      <div 
        className={`absolute top-[10%] left-1/2 -translate-x-1/2 -translate-y-1/2 font-['Brush_Script_MT'] text-[3rem] bg-gradient-to-b from-white to-[#c5a880] bg-clip-text text-transparent drop-shadow-[0_0_20px_rgba(197,168,128,0.5)] z-10 pointer-events-none text-center w-full whitespace-nowrap transition-all duration-[3000ms] ease-in-out delay-1000 max-sm:text-[1.8rem] max-sm:top-[12%] max-sm:whitespace-normal max-sm:leading-[1.2] ${showText ? 'opacity-100 -translate-y-1/2' : 'opacity-0 -translate-y-[30%]'}`}
      >
        Merry Christmas To You~
      </div>
    </div>
  );
}

export default App;