<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-grid">
        <!-- Branding -->
        <div class="footer-brand">
          <div class="brand-logo">
            <svg class="logo-icon" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z" fill="currentColor" />
            </svg>
            <h3 class="brand-name">PatrimoniosBA</h3>
          </div>
          <p class="brand-description">
            Preservando la memoria de Buenos Aires para las futuras generaciones.
          </p>
        </div>
        
        <!-- Enlaces -->
        <div class="footer-links">
          <h4>Enlaces</h4>
          <router-link to="/contacto">Contacto</router-link>
          <router-link to="/terminos">Términos de Servicio</router-link>
          <router-link to="/privacidad">Política de Privacidad</router-link>
        </div>
        
        <!-- Redes Sociales -->
        <div class="footer-social">
          <h4>Síguenos</h4>
          <div class="social-icons">
            <a href="#" aria-label="Facebook" class="social-link">
              <svg class="social-icon" fill="currentColor" viewBox="0 0 24 24">
                <path clip-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" fill-rule="evenodd" />
              </svg>
            </a>
            <a href="#" aria-label="Twitter" class="social-link">
              <svg class="social-icon" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.71v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
            <a href="#" aria-label="Instagram" class="social-link">
              <svg class="social-icon" fill="currentColor" viewBox="0 0 24 24">
                <path clip-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.024.06 1.378.06 3.808s-.012 2.784-.06 3.808c-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.024.048-1.378.06-3.808.06s-2.784-.013-3.808-.06c-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.048-1.024-.06-1.378-.06-3.808s.012-2.784.06-3.808c.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.86.399-1.249.789-.389.389-.607.782-.789 1.249-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.86.789 1.249.389.389.782.607 1.249.789.353.137.882.3 1.857.344 1.023.047 1.351.058 3.807.058h.468c2.456 0 2.784-.011 3.807-.058.975-.045 1.504-.207 1.857-.344.467-.182.86-.399 1.249-.789.389-.389.607-.782.789-1.249.137-.353.3-.882.344-1.857.047-1.023.058-1.351.058-3.807v-.468c0-2.456-.011-2.784-.058-3.807-.045-.975-.207-1.504-.344-1.857a3.097 3.097 0 00-.789-1.249 3.097 3.097 0 00-1.249-.789c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 100 10.27 5.135 5.135 0 000-10.27zm0 1.802a3.333 3.333 0 110 6.666 3.333 3.333 0 010-6.666zm5.338-3.205a1.2 1.2 0 100 2.4 1.2 1.2 0 000-2.4z" fill-rule="evenodd" />
              </svg>
            </a>
          </div>
        </div>
      </div>
      
      <!-- Copyright -->
      <div class="footer-bottom">
        <p>© 2024 PatrimoniosBA. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background: #2C3E50;
  color: #E5E7EB;
  padding: 60px 24px 40px;
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #4A90E2;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
  font-family: 'Lora', serif;
}

.brand-description {
  color: #9CA3AF;
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 350px;
}

.footer-links,
.footer-social {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-links h4,
.footer-social h4 {
  color: white;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.footer-links a {
  color: #9CA3AF;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: white;
}

.social-icons {
  display: flex;
  gap: 16px;
}

.social-link {
  color: #9CA3AF;
  transition: color 0.2s;
}

.social-link:hover {
  color: white;
}

.social-icon {
  width: 24px;
  height: 24px;
}

.footer-bottom {
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.footer-bottom p {
  color: #9CA3AF;
  font-size: 0.875rem;
}

@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  
  .footer-brand {
    grid-column: 1 / -1;
  }
}

@media (max-width: 640px) {
  .footer {
    padding: 40px 16px 30px;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
    text-align: center;
  }
  
  .brand-logo {
    justify-content: center;
  }
  
  .brand-description {
    margin: 0 auto;
  }
  
  .footer-links,
  .footer-social {
    align-items: center;
  }
}
</style>