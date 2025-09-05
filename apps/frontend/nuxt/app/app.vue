<script setup lang="ts">
import Main from "./main.vue";
</script>

<template>
  <div class="app">
    <NuxtRouteAnnouncer />
    <header class="app-header">SimpleChat</header>

    <div class="app-content">
      <nav class="app-navigation">
        <a class="app-navigation--link active" href="/rooms/1">1</a>
        <a class="app-navigation--link" href="/rooms/2">2</a>
      </nav>

      <Main />
    </div>

    <footer class="app-footer">
      <a href="https://laf-team.ru" target="_blank" rel="noopener noreferrer">
        Lazy And Focused</a
      >
    </footer>
  </div>
</template>

<style scoped>
a {
  color: var(--primary);
  text-decoration: wavy;
  line-height: 1rem;

  &::after {
    content: "↗";
    margin-left: calc(var(--sizing) / 2);
  }
}

.app {
  min-height: 100dvh;
  padding: calc(var(--sizing) * 2);

  display: flex;
  gap: calc(var(--sizing) * 4);
  flex-direction: column;

  background-image: url("/backgrounds/default.jpg");
  background-color: var(--background);
  background-size: cover;
  background-position: center;

  color: var(--background-foreground);
}

.app-header,
.app-footer {
  width: 100%;
  padding: calc(var(--sizing) * 2);

  display: flex;
  justify-content: center;

  font-weight: 600;

  background-color: var(--primary-foreground);
  color: var(--primary);

  border: none;
  border-radius: calc(var(--rounded) * 2);
}

.app-content {
  height: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  gap: calc(var(--sizing) * 4);
}

.app-navigation {
  padding-top: var(--sizing);
  display: flex;
  flex-direction: column;
  gap: var(--sizing);
}

.app-navigation > .app-navigation--link {
  width: calc(var(--sizing) * 6);
  height: calc(var(--sizing) * 6);

  background-color: var(--primary);
  color: var(--primary-foreground);

  display: flex;
  justify-content: center;
  align-items: center;

  border: none;
  border-radius: calc(var(--rounded) * 2);

  &::after {
    content: none;
  }
}

.app-navigation > .app-navigation--link.active {
  border: double currentColor calc(var(--sizing) / 2);
  border-radius: calc(var(--rounded) * 2);
}
</style>
