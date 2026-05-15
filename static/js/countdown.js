function initCountdown() {
    const el = document.getElementById('countdown');
    if (!el) return;

    //function that sets the bidding timer and checks if the timer has expired
    function tick() {
        const expires = new Date(el.dataset.expires);
        const diff = expires - new Date();
        if (diff <= 0) {
            el.textContent = 'Expired';
            clearInterval(timer);
            return;
        }
        //math function for hours, minutes and seconds for the bidding
        const h = Math.floor((diff % 86400000) / 3600000);
        const m = Math.floor((diff % 3600000) / 60000);
        const s = Math.floor((diff % 60000) / 1000);
        el.textContent = `${h}h ${m}m ${s}s`;
    }

    // Calls the tick function and sets the tick speed at one second
    tick();
    const timer = setInterval(tick, 1000);
}

document.addEventListener('DOMContentLoaded', initCountdown);