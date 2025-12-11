/* ===================================
   UniEvents - JavaScript Principal
   Validações
   =================================== */

// ===================================
// DARK MODE TOGGLE
// ===================================

function initThemeToggle() {
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;
  
  // Carregar tema salvo
  const savedTheme = localStorage.getItem('theme') || 'light';
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#theme-toggle i');
  if (icon) {
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
  }
}

// ===================================
// MÁSCARAS DE ENTRADA
// ===================================

function phoneMask(input) {
  let value = input.value.replace(/\D/g, '');
  
  if (value.length <= 10) {
    value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
  } else {
    value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
  }
  
  input.value = value;
}

// ===================================
// VALIDAÇÕES
// ===================================

function validatePhone(phone) {
  const cleaned = phone.replace(/\D/g, '');
  return cleaned.length === 10 || cleaned.length === 11;
}

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validatePassword(password) {
  const minLength = password.length >= 8;
  const hasLetter = /[a-zA-Z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  return {
    valid: minLength && hasLetter && hasNumber && hasSpecial,
    minLength,
    hasLetter,
    hasNumber,
    hasSpecial
  };
}

function showPasswordStrength(password, strengthElement) {
  const validation = validatePassword(password);
  const strength = [validation.minLength, validation.hasLetter, validation.hasNumber, validation.hasSpecial]
    .filter(Boolean).length;
  
  const messages = {
    0: { text: 'Muito fraca', color: '#dc3545', width: '25%' },
    1: { text: 'Fraca', color: '#ffc107', width: '25%' },
    2: { text: 'Média', color: '#ffc107', width: '50%' },
    3: { text: 'Boa', color: '#26C6DA', width: '75%' },
    4: { text: 'Forte', color: '#26C6DA', width: '100%' }
  };
  
  const msg = messages[strength];
  
  if (strengthElement) {
    strengthElement.innerHTML = `
      <div style="margin-top: 0.5rem;">
        <div style="height: 4px; background: var(--border-color); border-radius: 2px; overflow: hidden;">
          <div style="height: 100%; background: ${msg.color}; width: ${msg.width}; transition: all 0.3s;"></div>
        </div>
        <small style="color: ${msg.color}; font-weight: 600; margin-top: 0.25rem; display: block;">${msg.text}</small>
      </div>
    `;
  }
  
  return validation.valid;
}

function validatePasswordMatch(password, confirmPassword) {
  return password === confirmPassword && password.length > 0;
}

function validateParticipants(value) {
  const num = parseInt(value);
  return !isNaN(num) && num > 0 && num <= 10000;
}

function validateEventDate(dateString) {
  const selectedDate = new Date(dateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  return selectedDate >= today;
}

function validateImageFile(file) {
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  
  if (!file) {
    return { valid: false, error: 'Nenhum arquivo selecionado' };
  }
  
  if (!validTypes.includes(file.type)) {
    return { valid: false, error: 'Formato inválido. Use JPEG, PNG, GIF ou WebP' };
  }
  
  if (file.size > maxSize) {
    return { valid: false, error: 'Arquivo muito grande. Máximo 5MB' };
  }
  
  return { valid: true };
}

// ===================================
// PREVIEW DE IMAGEM
// ===================================

function previewImage(input, previewElement) {
  const file = input.files[0];
  
  if (file) {
    const validation = validateImageFile(file);
    
    if (!validation.valid) {
      input.value = '';
      if (previewElement) {
        previewElement.innerHTML = `
          <div class="alert alert-danger">
            <i class="fas fa-exclamation-circle"></i>
            <span>${validation.error}</span>
          </div>
        `;
      }
      return false;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
      if (previewElement) {
        previewElement.innerHTML = `
          <img src="${e.target.result}" class="file-preview" alt="Preview">
          <p style="margin-top: 0.5rem; color: var(--success); font-weight: 600;">
            <i class="fas fa-check-circle"></i> Imagem válida
          </p>
        `;
      }
    };
    reader.readAsDataURL(file);
    return true;
  }
  return false;
}

// ===================================
// APLICAÇÃO AUTOMÁTICA DE VALIDAÇÕES
// ===================================

function initFormValidations() {
  // Máscaras de telefone
  document.querySelectorAll('input[type="tel"], input[name*="phone"], input[name*="telefone"]').forEach(input => {
    input.addEventListener('input', function() {
      phoneMask(this);
    });
    
    input.addEventListener('blur', function() {
      const isValid = validatePhone(this.value);
      toggleValidationClass(this, isValid);
      
      if (!isValid && this.value) {
        showFieldError(this, 'Telefone inválido. Use (XX) XXXXX-XXXX');
      } else {
        hideFieldError(this);
      }
    });
  });
  
  // Validação de email
  document.querySelectorAll('input[type="email"]').forEach(input => {
    input.addEventListener('blur', function() {
      if (this.value) {
        const isValid = validateEmail(this.value);
        toggleValidationClass(this, isValid);
        
        if (!isValid) {
          showFieldError(this, 'Email inválido');
        } else {
          hideFieldError(this);
        }
      }
    });
  });
  
  // Validação de senha
  document.querySelectorAll('input[type="password"][name*="password"], input[type="password"][name*="senha"]').forEach(input => {
    if (input.name.includes('confirm') || input.name.includes('confirmacao')) return;
    
    const strengthDiv = document.createElement('div');
    strengthDiv.className = 'password-strength';
    input.parentNode.appendChild(strengthDiv);
    
    input.addEventListener('input', function() {
      const isValid = showPasswordStrength(this.value, strengthDiv);
      toggleValidationClass(this, isValid);
    });
  });
  
  // Confirmação de senha
  document.querySelectorAll('input[name*="confirm"], input[name*="confirmacao"]').forEach(input => {
    const passwordField = document.querySelector('input[type="password"][name*="password"]:not([name*="confirm"]), input[type="password"][name*="senha"]:not([name*="confirmacao"])');
    
    if (passwordField) {
      input.addEventListener('input', function() {
        const match = validatePasswordMatch(passwordField.value, this.value);
        toggleValidationClass(this, match);
        
        if (!match && this.value) {
          showFieldError(this, 'As senhas não coincidem');
        } else {
          hideFieldError(this);
        }
      });
    }
  });
  
  // Validação de participantes
  document.querySelectorAll('input[name*="participantes"], input[name*="vagas"]').forEach(input => {
    input.addEventListener('blur', function() {
      if (this.value) {
        const isValid = validateParticipants(this.value);
        toggleValidationClass(this, isValid);
        
        if (!isValid) {
          showFieldError(this, 'Número inválido (1-10000)');
        } else {
          hideFieldError(this);
        }
      }
    });
  });
  
  // Validação de datas
  document.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(input => {
    input.addEventListener('change', function() {
      const isValid = validateEventDate(this.value);
      toggleValidationClass(this, isValid);
      
      if (!isValid) {
        showFieldError(this, 'Data não pode ser anterior à data atual');
      } else {
        hideFieldError(this);
      }
    });
  });
  
  // Upload de imagens
  document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
    input.addEventListener('change', function() {
      const previewId = this.dataset.preview || this.id + '-preview';
      const previewElement = document.getElementById(previewId);
      previewImage(this, previewElement);
    });
  });
}

// ===================================
// FUNÇÕES AUXILIARES DE UI
// ===================================

function toggleValidationClass(element, isValid) {
  element.classList.remove('is-valid', 'is-invalid');
  if (isValid) {
    element.classList.add('is-valid');
  } else if (element.value) {
    element.classList.add('is-invalid');
  }
}

function showFieldError(element, message) {
  hideFieldError(element);
  
  const errorDiv = document.createElement('div');
  errorDiv.className = 'invalid-feedback';
  errorDiv.textContent = message;
  errorDiv.style.display = 'block';
  
  element.parentNode.appendChild(errorDiv);
}

function hideFieldError(element) {
  const existingError = element.parentNode.querySelector('.invalid-feedback');
  if (existingError) {
    existingError.remove();
  }
}

function validateForm(formElement) {
  let isValid = true;
  const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
  
  inputs.forEach(input => {
    if (!input.value) {
      isValid = false;
      toggleValidationClass(input, false);
      showFieldError(input, 'Este campo é obrigatório');
    } else {
      if (input.type === 'email') {
        const emailValid = validateEmail(input.value);
        if (!emailValid) isValid = false;
        toggleValidationClass(input, emailValid);
      }
      
      if (input.type === 'tel' || input.name.includes('phone') || input.name.includes('telefone')) {
        const phoneValid = validatePhone(input.value);
        if (!phoneValid) isValid = false;
        toggleValidationClass(input, phoneValid);
      }
      
      if (input.type === 'date' || input.type === 'datetime-local') {
        const dateValid = validateEventDate(input.value);
        if (!dateValid) isValid = false;
        toggleValidationClass(input, dateValid);
      }
    }
  });
  
  return isValid;
}

// ===================================
// SIDEBAR TOGGLE (MOBILE)
// ===================================

function initSidebarToggle() {
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }
}

// ===================================
// INICIALIZAÇÃO
// ===================================

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initFormValidations();
    initSidebarToggle();
  });
} else {
  initThemeToggle();
  initFormValidations();
  initSidebarToggle();
}

window.UniEvents = window.UniEvents || {}; 

window.UniEvents.validatePhone = validatePhone;
window.UniEvents.validateEmail = validateEmail;
window.UniEvents.validatePasswordMatch = validatePasswordMatch;
window.UniEvents.showPasswordStrength = showPasswordStrength; 
window.UniEvents.validateParticipants = validateParticipants;
window.UniEvents.validateEventDate = validateEventDate;
window.UniEvents.validateImageFile = validateImageFile;
window.UniEvents.previewImage = previewImage;
window.UniEvents.phoneMask = phoneMask;
window.UniEvents.validateForm = validateForm;