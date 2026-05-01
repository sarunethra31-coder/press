document.addEventListener('DOMContentLoaded', () => {
    if (window.location.protocol === 'file:') {
        document.body.innerHTML = `<h1 style="color:red; text-align:center; margin-top:50px; font-family:sans-serif;">STOP! You cannot open this file directly from your folder.</h1><h2 style="text-align:center; font-family:sans-serif;">FormSubmit will block the email if you do this.<br><br>You MUST open your browser and type this exact URL to see the form:<br><br><b style="font-size:30px; background:#f0f0f0; padding:10px; border-radius:10px; user-select:all;">http://127.0.0.1:5000</b></h2>`;
        return;
    }
    const form = document.getElementById('contact-form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const phone = document.getElementById('phone').value;
        const address = document.getElementById('address').value;
        const email = document.getElementById('email').value;
        const printType = document.getElementById('print_type').value;
        const details = document.getElementById('details').value;
        
        const btn = document.getElementById('submit-btn');
        const originalContent = btn.innerHTML;
        
        // Loading state
        btn.innerHTML = '<span>Sending...</span>';
        btn.style.opacity = '0.8';
        btn.style.pointerEvents = 'none';
        
        // 1. Success state (Immediate)
        btn.innerHTML = `
            <span>Sending Order...</span>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        btn.style.background = 'linear-gradient(135deg, #10b981, #059669)'; /* Emerald green */
        btn.style.boxShadow = '0 10px 15px -3px rgba(16, 185, 129, 0.3)';
        
        // 2. Decorative Falling Lights / Balloons Effect
        var duration = 2 * 1000;
        var end = Date.now() + duration;

        (function frame() {
          confetti({
            particleCount: 5,
            startVelocity: 0,
            ticks: 300,
            origin: { x: Math.random(), y: (Math.random() * 0.2) - 0.2 },
            colors: ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#f472b6', '#2dd4bf'],
            shapes: ['circle'],
            gravity: 0.6,
            scalar: Math.random() * 1.5 + 0.8,
            drift: (Math.random() - 0.5) * 2
          });
          if (Date.now() < end) { requestAnimationFrame(frame); }
        }());
        
        // 3. Let FormSubmit securely deliver the email automatically!
        setTimeout(() => {
            form.submit();
        }, 1500);
    });
});
