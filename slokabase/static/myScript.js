const nav  = document.querySelector('nav')
const toggleLink = document.getElementById('toggleNav');
const prevLink = document.getElementById('prevSloka');
const nextLink = document.getElementById('nextSloka');

/* Reading pages (sloka / line view): nav starts collapsed,
   shown only on demand (toggle link or Up/Down arrow). */
if (toggleLink) {
  nav.style.display = 'none';
  toggleLink.textContent = '[ ▼ ]';
}

if (toggleLink) {
  toggleLink.addEventListener('click', function (event) {
    event.preventDefault(); // prevent page jump

    if (nav.style.display !== 'none') {
      nav.style.display = 'none';
      toggleLink.textContent = '[ ▼ ]';
    } else {
      nav.style.display = 'flex';
      toggleLink.textContent = '[ ▲ ]';
    }
  });
}


/*
    Previous Sloka and Next Sloka
*/

// When user clicks the anchor
if (prevLink) {
  prevLink.addEventListener('click', function(event) {
    event.preventDefault();

    window.location.href = this.getAttribute('href');

  });
}

if (nextLink) {
  nextLink.addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = this.getAttribute('href');
  });
}

// When user presses left/right arrow keys
document.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowLeft') {
    if (prevLink) prevLink.click();
  } else if (event.key === 'ArrowRight') {
    if (nextLink) nextLink.click();
  } else if (event.key === 'ArrowUp')  {
    if (toggleLink) toggleLink.click();
  }
  else if (event.key === 'ArrowDown')  {
    if (toggleLink) toggleLink.click();
  }
});
