<template>
  <footer class="app-footer">
    <a href="https://laf-team.ru" target="_blank" rel="noopener noreferrer">
      Lazy And Focused</a
    >
  </footer>
</template>

<style scoped>
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
</style>
