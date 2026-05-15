let images = [];
let currentIndex = 0;
let mainImage = null;

// function that displays all images
function initGallery(imageList) {
    images = imageList;
    currentIndex = 0;
    mainImage = document.getElementById("mainImage");
}

// function that shows what image is being viewed depending on the index
function updateImage() {
    if (!mainImage || images.length === 0) return;
    mainImage.src = images[currentIndex];
}

// function to go to the next image
function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateImage();
}

// function to go to the previous image
function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateImage();
}

// function to change what image is being viewed
function changeImage(src) {
    mainImage.src = src;
    currentIndex = images.indexOf(src);
}