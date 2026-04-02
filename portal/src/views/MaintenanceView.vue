<template>
  <div class="maintenance-container">
    <div class="maintenance-content">
      <div class="icon">🚧</div>
      <h1>Sitio en Mantenimiento</h1>
      <p>Estamos realizando mejoras en nuestra plataforma.</p>
      <p>Por favor, vuelve a intentarlo más tarde.</p>
    </div>
  </div>
</template>

<style scoped>
.maintenance-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
  font-family: 'Inter', sans-serif;
}

.maintenance-content {
  text-align: center;
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-width: 500px;
  width: 90%;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

h1 {
  color: #111827;
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

p {
  color: #4b5563;
  font-size: 1.125rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}
</style>
