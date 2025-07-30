<script lang="ts">
  import { onDestroy } from 'svelte';

  export let numBars = 16;
  export let stream_state: "open" | "closed" | "waiting" = "closed";
  export let audio_source_callback: () => MediaStream;
  export let icon: string | undefined = undefined;
  export let icon_button_color: string = "var(--body-text-color)";
  export let pulse_color: string = "var(--body-text-color)";

  let audioContext: AudioContext;
  let analyser: AnalyserNode;
  let dataArray: Uint8Array;
  let animationId: number;
  let pulseScale = 1;
  let pulseIntensity = 0;

  $: containerWidth = icon 
    ? "128px"
    : `calc((var(--boxSize) + var(--gutter)) * ${numBars})`;

  $: if(stream_state === "open") setupAudioContext();

  onDestroy(() => {
    if (animationId) {
      cancelAnimationFrame(animationId);
    }
    if (audioContext) {
      audioContext.close();
    }
  });

  async function getCombinedAudioStream() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();

    // Obtenir le flux du micro
    const micStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Obtenir le flux des haut-parleurs (cela peut nécessiter des configurations spécifiques)
    // Par exemple, sur certains systèmes, tu pourrais utiliser un logiciel tiers pour rediriger le son des haut-parleurs vers un flux audio.
    const speakerStream = await audio_source_callback();

    // Créer des sources audio pour chaque flux
    const micSource = audioContext.createMediaStreamSource(micStream);
    const speakerSource = audioContext.createMediaStreamSource(speakerStream);

    // Créer un MediaStreamAudioDestinationNode pour combiner les flux
    const destination = audioContext.createMediaStreamDestination();

    // Connecter les sources au destination
    micSource.connect(destination);
    speakerSource.connect(destination);

    return destination.stream;
}

  async function setupAudioContext() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();

    // Utiliser le flux combiné
    const combinedStream = await getCombinedAudioStream();
    const source = audioContext.createMediaStreamSource(combinedStream);

    source.connect(analyser);

    analyser.fftSize = 64;
    analyser.smoothingTimeConstant = 0.8;
    dataArray = new Uint8Array(analyser.frequencyBinCount);

    updateVisualization();
  }

  function updateVisualization() {
    analyser.getByteFrequencyData(dataArray);
    
    if (icon) {
      // Calculate average amplitude for pulse effect
      const average = Array.from(dataArray).reduce((a, b) => a + b, 0) / dataArray.length;
      const normalizedAverage = average / 255;
      pulseScale = 1 + (normalizedAverage * 0.15);
      pulseIntensity = normalizedAverage;
    } else {
      // Update bars
      const bars = document.querySelectorAll('.gradio-audio-waveContainer .gradio-audio-box');
      for (let i = 0; i < bars.length; i++) {
        const barHeight = (dataArray[i] / 255);
        bars[i].style.transform = `scaleY(${Math.max(0.1, barHeight)})`;
      }
    }

    animationId = requestAnimationFrame(updateVisualization);
  }
</script>

<div class="gradio-audio-waveContainer">
{#if icon}
  <div class="gradio-audio-icon-container">
    {#if pulseIntensity > 0}
      {#each Array(3) as _, i}
        <div 
          class="pulse-ring"
          style:background={pulse_color}
          style:animation-delay={`${i * 0.4}s`}
        />
      {/each}
    {/if}
    
    <div 
      class="gradio-audio-icon" 
      style:transform={`scale(${pulseScale})`}
      style:background={icon_button_color}
    >
      <img 
        src={icon} 
        alt="Audio visualization icon"
        class="icon-image"
      />
    </div>
  </div>
{:else}
  <div class="gradio-audio-boxContainer" style:width={containerWidth}>
    {#each Array(numBars) as _}
      <div class="gradio-audio-box" style="transform: scaleY(0.1);"></div>
    {/each}
  </div>
{/if}
</div>

<style>
.gradio-audio-waveContainer {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gradio-audio-boxContainer {
  display: flex;
  justify-content: space-between;
  height: 20px;
  --boxSize: 8px;
  --gutter: 4px;
}

.gradio-audio-box {
  height: 100%;
  width: var(--boxSize);
  background: var(--body-text-color);
  border-radius: 8px;
  transition: transform 0.05s ease;
}

.gradio-audio-icon-container {
  position: relative;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gradio-audio-icon {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  transition: transform 0.1s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.icon-image {
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  opacity: 0.5;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(3);
    opacity: 0;
  }
}
</style>