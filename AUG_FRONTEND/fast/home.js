// Function to check if an element is in the viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 && 
        rect.left >= 0 && 
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && 
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Function to add the 'visible' class to elements in view
function handleScroll() {
    const elements = document.querySelectorAll('.hero-content h1, .hero-content p, .hero-content a, .left-panel h1, .left-panel p, .right-panel h3, .right-panel p, .right-panel hr, .block-show-box1, .block-show-box2'); // Select all elements with the specified classes
    elements.forEach(element => {
        if (isInViewport(element)) {
            element.classList.add('visible'); // Add visible class if in viewport
        }
    });
}


// Listen for scroll and resize events
window.addEventListener('scroll', handleScroll);
window.addEventListener('resize', handleScroll);

// Initial check in case elements are already in view
document.addEventListener('DOMContentLoaded', handleScroll);
