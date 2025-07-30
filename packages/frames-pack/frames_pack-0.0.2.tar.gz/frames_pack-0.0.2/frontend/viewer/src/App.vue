<script setup lang="ts">
import FramesPackViewer from './components/FramesPackViewer.vue'
</script>

<template>
  <v-app>
    <FramesPackViewer />
  </v-app>
</template>

<style>
html,
body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  height: 100%;
  width: 100%;
  position: relative;
}
</style>
