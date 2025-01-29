<template>
  <div id="app">
    <h1>文本转语音</h1>
    <TextToSpeech />
  </div>
</template>

<script>
import TextToSpeech from './components/TextToSpeech.vue'

export default {
  name: 'App',
  components: {
    TextToSpeech
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>