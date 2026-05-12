function initCountdown() {
    const el = document.getElementById('countdown');
    if (!el) return;

    const expires = new Date(el.dataset.expires);

    setInterval(() => {
        const diff = expires - new Date();
        if (diff <= 0) {
            el.textContent = 'Expired';
            return;
        }
        const m = Math.floor((diff % 3600000) / 60000);
        const s = Math.floor((diff % 60000) / 1000);
        el.textContent = `${m}m ${s}s`;
    }, 1000);
}

document.addEventListener('DOMContentLoaded', initCountdown);