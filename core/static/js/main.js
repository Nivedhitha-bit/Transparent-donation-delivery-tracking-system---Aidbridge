/* ===== AidBridge Main JS ===== */

// Theme Toggle
const THEME_KEY = 'aidbridge_theme';

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(saved);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const icon = document.getElementById('theme-icon');
  if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem(THEME_KEY, theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

// Carousel
function initCarousel() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  if (!slides.length) return;

  let current = 0;
  let interval = null;

  function showSlide(n) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('active');
    if (dots[current]) dots[current].classList.add('active');
  }

  function next() { showSlide(current + 1); }
  function prev() { showSlide(current - 1); }

  function startAuto() { interval = setInterval(next, 4500); }
  function stopAuto() { clearInterval(interval); }

  document.querySelector('.carousel-next')?.addEventListener('click', () => { stopAuto(); next(); startAuto(); });
  document.querySelector('.carousel-prev')?.addEventListener('click', () => { stopAuto(); prev(); startAuto(); });
  dots.forEach((dot, i) => dot.addEventListener('click', () => { stopAuto(); showSlide(i); startAuto(); }));

  showSlide(0);
  startAuto();
}

// Dropdown
function initDropdowns() {
  document.querySelectorAll('[data-dropdown-toggle]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const target = document.getElementById(btn.dataset.dropdownToggle);
      if (target) target.classList.toggle('show');
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.show').forEach(m => m.classList.remove('show'));
  });
}

// Role Toggle (Login/Register)
function initRoleToggle() {
  const btns = document.querySelectorAll('.role-btn');
  const input = document.getElementById('role-input');
  const ngoFields = document.querySelector('.ngo-fields');

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const role = btn.dataset.role;
      if (input) input.value = role;
      if (ngoFields) {
        ngoFields.classList.toggle('show', role === 'ngo');
        // Make ngo description required when shown
        const desc = document.getElementById('ngo-description');
        if (desc) desc.required = role === 'ngo';
      }
    });
  });
}

// Chatbot
function initChatbot() {
  const fab = document.getElementById('chatbot-trigger');
  const win = document.getElementById('chatbot-window');
  const closeBtn = document.getElementById('chatbot-close');
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');
  const messages = document.getElementById('chat-messages');

  if (!fab) return;

  function toggleChatbot() {
    win.classList.toggle('open');
    if (win.classList.contains('open') && messages.children.length === 0) {
      appendMessage('bot', '👋 Hi! I\'m the AidBridge assistant. Ask me anything about donating, volunteering, NGOs, or how the platform works!');
    }
  }

  function appendMessage(type, text) {
    const msg = document.createElement('div');
    msg.className = `chat-msg ${type}`;
    msg.innerHTML = `<div class="chat-bubble">${text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</div>`;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    appendMessage('user', text);
    input.value = '';
    // Typing indicator
    const typing = document.createElement('div');
    typing.className = 'chat-msg bot';
    typing.id = 'typing';
    typing.innerHTML = '<div class="chat-bubble">✦ typing...</div>';
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      const resp = await fetch('/chatbot/api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ message: text })
      });
      const data = await resp.json();
      document.getElementById('typing')?.remove();
      appendMessage('bot', data.response || 'Sorry, I could not understand that.');
    } catch (e) {
      document.getElementById('typing')?.remove();
      appendMessage('bot', '⚠️ Connection error. Please try again.');
    }
  }

  fab.addEventListener('click', toggleChatbot);
  closeBtn?.addEventListener('click', () => win.classList.remove('open'));
  sendBtn?.addEventListener('click', sendMessage);
  input?.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });
}

// CSRF Cookie helper
function getCookie(name) {
  let val = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) val = decodeURIComponent(v);
  });
  return val;
}

// Alerts auto-dismiss
function initAlerts() {
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(alert => {
    setTimeout(() => alert.remove(), 4000);
  });
}

// Sidebar mobile toggle
function initSidebar() {
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  
  toggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
    overlay?.classList.toggle('show');
  });
  overlay?.addEventListener('click', () => {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('show');
  });
}

// Scroll animations
function initScrollAnimations() {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in-delay-1, .fade-in-delay-2, .fade-in-delay-3').forEach(el => {
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    obs.observe(el);
  });
}

// Confirm delete dialogs
function confirmDelete(form, itemName) {
  if (confirm(`Are you sure you want to delete "${itemName}"? This cannot be undone.`)) {
    form.submit();
  }
}

// Init on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initCarousel();
  initDropdowns();
  initRoleToggle();
  initChatbot();
  initAlerts();
  initSidebar();
  initScrollAnimations();
});
