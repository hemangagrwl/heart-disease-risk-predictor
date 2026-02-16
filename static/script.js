// Enhanced Form Validation and User Experience
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.querySelector('.submit-btn');
    const inputs = document.querySelectorAll('input[type="number"]');
    
    // Smooth scroll to result on page load (if result exists)
    const resultContainer = document.querySelector('.result-container');
    if (resultContainer) {
        setTimeout(() => {
            resultContainer.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }
    
    // Loading state on form submission
    form.addEventListener('submit', function(e) {
        submitBtn.innerHTML = '⏳ Analyzing Patient Data...';
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.7';
    });
    
    // Real-time input validation with visual feedback
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
        });
        
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    // Validate individual input
    function validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.getAttribute('min'));
        const max = parseFloat(input.getAttribute('max'));
        const name = input.getAttribute('name');
        
        // Remove previous validation classes
        input.classList.remove('valid', 'warning', 'invalid');
        
        if (!input.value) {
            return;
        }
        
        // Check if value is in normal range
        if (name === 'age') {
            if (value >= 20 && value <= 80) {
                input.classList.add('valid');
            } else {
                input.classList.add('warning');
            }
        } else if (name === 'trestbps') {
            if (value >= 90 && value <= 120) {
                input.classList.add('valid');
            } else if (value > 120 && value <= 140) {
                input.classList.add('warning');
            } else {
                input.classList.add('invalid');
            }
        } else if (name === 'chol') {
            if (value >= 125 && value <= 200) {
                input.classList.add('valid');
            } else if (value > 200 && value <= 240) {
                input.classList.add('warning');
            } else {
                input.classList.add('invalid');
            }
        } else if (name === 'thalach') {
            if (value >= 60 && value <= 100) {
                input.classList.add('valid');
            } else if (value > 100 && value <= 180) {
                input.classList.add('warning');
            } else {
                input.classList.add('invalid');
            }
        }
        
        // Basic range validation
        if (value < min || value > max) {
            input.classList.add('invalid');
        }
    }
    
    // Animate result cards on display
    const infoCards = document.querySelectorAll('.info-card');
    infoCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 * (index + 1));
    });
    
    // Animate recommendations list items
    const recItems = document.querySelectorAll('.recommendations-list li');
    recItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.4s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 100 * index);
    });
    
    // Add tooltips for form labels (optional enhancement)
    const labels = document.querySelectorAll('.form-group label');
    labels.forEach(label => {
        label.style.cursor = 'help';
    });
    
    // Prevent form resubmission on page refresh
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
    
    // Add smooth hover effects to risk factor items
    const riskFactors = document.querySelectorAll('.risk-factor-item');
    riskFactors.forEach(factor => {
        factor.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        factor.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    // Print functionality (optional)
    const printBtn = document.createElement('button');
    if (resultContainer) {
        printBtn.innerHTML = '🖨️ Print Report';
        printBtn.className = 'print-btn';
        printBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 24px;
            background: #27ae60;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3);
            z-index: 1000;
        `;
        
        printBtn.addEventListener('click', function() {
            window.print();
        });
        
        document.body.appendChild(printBtn);
    }
});

// Add dynamic CSS for validation states
const validationStyles = document.createElement('style');
validationStyles.textContent = `
    input.valid {
        border-color: #27ae60 !important;
        background: #e8f5e9;
    }
    
    input.warning {
        border-color: #f39c12 !important;
        background: #fff3e0;
    }
    
    input.invalid {
        border-color: #e74c3c !important;
        background: #fee;
    }
    
    input.valid:focus {
        box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.1) !important;
    }
    
    input.warning:focus {
        box-shadow: 0 0 0 4px rgba(243, 156, 18, 0.1) !important;
    }
    
    input.invalid:focus {
        box-shadow: 0 0 0 4px rgba(231, 76, 60, 0.1) !important;
    }
    
    .print-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(39, 174, 96, 0.4);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .risk-zone-card {
        animation: pulse 2s ease-in-out infinite;
    }
`;
document.head.appendChild(validationStyles);

// Console log for debugging
console.log('🫀 Heart Disease Predictor initialized successfully!');
