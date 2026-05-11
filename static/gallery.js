let images = [];
let currentIndex = 0;
let mainImage = null;

function initGallery(imageList) {
    images = imageList;
    currentIndex = 0;
    mainImage = document.getElementById("mainImage");
}

function updateImage() {
    if (!mainImage || images.length === 0) return;
    mainImage.src = images[currentIndex];
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateImage();
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateImage();
}

function changeImage(src) {
    mainImage.src = src;
    currentIndex = images.indexOf(src);
}