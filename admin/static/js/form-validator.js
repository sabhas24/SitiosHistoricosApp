

window.FormValidator = (function() {
    'use strict';
    
    
    const validationRules = {
        email: {
            validator: (value) => validator.isEmail(value) && validator.isLength(value, { max: 120 }),
            message: 'Ingrese un email válido (máximo 120 caracteres)'
        },
        
        name: {
            validator: (value) => validator.matches(value, /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/) && 
                                 validator.isLength(value, { min: 2, max: 80 }),
            message: 'Solo letras y espacios (2-80 caracteres)'
        },
        
        text: {
            validator: (value) => validator.isLength(value, { min: 1, max: 255 }),
            message: 'Texto requerido (máximo 255 caracteres)'
        },
        
        longText: {
            validator: (value) => validator.isLength(value, { min: 1, max: 1000 }),
            message: 'Texto requerido (máximo 1000 caracteres)'
        },
        
        password: {
            validator: (value) => validator.isStrongPassword(value, {
                minLength: 8,
                minLowercase: 1,
                minUppercase: 1,
                minNumbers: 1,
                minSymbols: 0
            }),
            message: 'Mínimo 8 caracteres, una mayúscula, una minúscula y un número'
        },
        
        number: {
            validator: (value) => validator.isNumeric(value),
            message: 'Solo números permitidos'
        },
        
        required: {
            validator: (value) => !validator.isEmpty(value.trim()),
            message: 'Este campo es requerido'
        }
    };

    function validateField(field, rules) {
        if (!field) return true;
        
        const value = field.value.trim();
        
        // Si el campo está vacío y no es requerido, es válido
        if (value === '' && !rules.includes('required')) {
            field.classList.remove('is-invalid', 'is-valid');
            return true;
        }
        
        // Validar todas las reglas
        for (let rule of rules) {
            const validation = validationRules[rule];
            if (validation && !validation.validator(value)) {
                field.classList.remove('is-valid');
                field.classList.add('is-invalid');
                const feedback = field.parentNode.querySelector('.invalid-feedback');
                if (feedback) feedback.textContent = validation.message;
                return false;
            }
        }
        
        // Todas las validaciones pasaron
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        return true;
    }

    function validatePasswordMatch(password, confirmPassword) {
        if (!password || !confirmPassword) return true;
        
        if (password.value !== confirmPassword.value) {
            confirmPassword.classList.add('is-invalid');
            const feedback = confirmPassword.parentNode.querySelector('.invalid-feedback');
            if (feedback) feedback.textContent = 'Las contraseñas no coinciden';
            return false;
        } else {
            confirmPassword.classList.remove('is-invalid');
            confirmPassword.classList.add('is-valid');
            return true;
        }
    }

    function initForm(formSelector, validationConfig) {
        const form = document.querySelector(formSelector);
        if (!form) return;

        // Configurar validaciones en tiempo real
        Object.entries(validationConfig).forEach(([fieldName, rules]) => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (!field) return;

            const event = rules.includes('email') ? 'blur' : 'input';
            field.addEventListener(event, () => validateField(field, rules));
        });

        // Validación de contraseñas
        const passwords = [
            [form.querySelector('[name="password"]'), form.querySelector('[name="confirm_password"]')],
            [form.querySelector('[name="new_password"]'), form.querySelector('[name="confirm_new_password"]')]
        ];

        passwords.forEach(([pass, confirm]) => {
            if (pass && confirm) {
                [pass, confirm].forEach(field => {
                    field.addEventListener('input', () => {
                        if (pass.value || confirm.value) {
                            validatePasswordMatch(pass, confirm);
                        }
                    });
                });
            }
        });

        // Validación completa al enviar
        form.addEventListener('submit', function(e) {
            let isValid = true;
            let errors = [];

            // Validar todos los campos configurados
            Object.entries(validationConfig).forEach(([fieldName, rules]) => {
                const field = form.querySelector(`[name="${fieldName}"]`);
                if (field && !validateField(field, rules)) {
                    isValid = false;
                    const validation = validationRules[rules.find(rule => validationRules[rule])];
                    if (validation) {
                        errors.push(`${fieldName}: ${validation.message}`);
                    }
                }
            });

            // Validar confirmación de contraseñas
            if (password && confirmPassword && !validatePasswordMatch(password, confirmPassword)) {
                isValid = false;
                errors.push('Las contraseñas no coinciden');
            }

            if (newPassword && confirmNewPassword && !validatePasswordMatch(newPassword, confirmNewPassword)) {
                isValid = false;
                errors.push('Las nuevas contraseñas no coinciden');
            }

            if (!isValid) {
                e.preventDefault();
                // Usar toast si está disponible, sino alert
                if (typeof showToast !== 'undefined') {
                    errors.forEach(error => showToast(error, 'danger'));
                } else {
                    alert('Errores de validación:\n\n' + errors.join('\n'));
                }
            }
        });
    }

    // API pública
    return {
        init: initForm,
        validate: validateField,
        validatePassword: validatePasswordMatch,
        rules: validationRules
    };
})();