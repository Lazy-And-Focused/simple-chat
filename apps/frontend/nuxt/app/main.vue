<template>
  <main class="app-main">
    <div>
      <div>
        <span> Текст крутой </span>
        <span> и вообще классный </span>
      </div>

      <div>
        <span> Текст крутой </span>
        <span> и вообще классный </span>
      </div>
    </div>
  </main>
</template>

<style scoped>
.app-main {
  width: 100%;

  --padding-x: calc(var(--sizing) * 4);
  --padding-y: calc(var(--sizing) * 2);

  padding-left: var(--padding-x);
  padding-right: var(--padding-x);
  padding-top: var(--padding-y);
  padding-bottom: var(--padding-y);

  border: none;
  border-radius: calc(var(--rounded) * 2);

  background-color: var(--background);
  color: var(--background-foreground);
}
</style>
