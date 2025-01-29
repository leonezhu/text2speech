<template>
  <div class="tts-container">
    <div class="input-section">
      <textarea
        v-model="text"
        placeholder="请输入要转换的文本..."
        rows="4"
        class="text-input"
      ></textarea>
      <button
        @click="convertToSpeech"
        :disabled="isLoading"
        class="convert-btn"
      >
        {{ isLoading ? "转换中..." : "转换为语音" }}
      </button>
    </div>

    <div v-if="audioUrl" class="audio-section">
      <audio controls :src="audioUrl" class="audio-player">
        您的浏览器不支持音频播放
      </audio>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextToSpeech",
  data() {
    return {
      text: "",
      audioUrl: "",
      isLoading: false,
    };
  },
  methods: {
    async convertToSpeech() {
      if (!this.text.trim()) {
        alert("请输入要转换的文本");
        return;
      }

      this.isLoading = true;
      try {
        const response = await fetch("http://localhost:5000/api/tts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: this.text }),
        });

        const data = await response.json();
        if (response.ok) {
          this.audioUrl = `http://localhost:5000${data.audio_url}`;
        } else {
          throw new Error(data.error);
        }
      } catch (error) {
        alert("转换失败: " + error.message);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.tts-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.text-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}                                    

.convert-btn {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.convert-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.audio-section {
  margin-top: 20px;
}

.audio-player {
  width: 100%;
}
</style>
