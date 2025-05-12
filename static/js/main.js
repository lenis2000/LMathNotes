!function(){
  let e;
  function t(e) {
    "complete" === document.readyState || "interactive" === document.readyState
      ? setTimeout(e, 1)
      : document.addEventListener("DOMContentLoaded", e);
  }

  // ResizeObserver polyfill code...
  // (skipping the bulk of the code as it's not relevant to the fixes)

  t(function() {
    // Handle details/summary elements for local storage persistence
    document.addEventListener("DOMContentLoaded", function() {
      const details = document.querySelectorAll("details");
      
      details.forEach((detail) => {
        if (!detail || !detail.querySelector) return;
        
        const summary = detail.querySelector("summary");
        if (!summary) return;
        
        detail.addEventListener("toggle", function() {
          try {
            localStorage.setItem(
              "detail-" + summary.textContent.trim(),
              this.open
            );
          } catch (e) {
            console.warn("Failed to save detail state to localStorage:", e);
          }
        });

        try {
          const stored = localStorage.getItem(
            "detail-" + summary.textContent.trim()
          );
          if (stored === "true") {
            detail.open = true;
          }
        } catch (e) {
          console.warn("Failed to read detail state from localStorage:", e);
        }
      });
    });
  });
  
  // Right Links Details handling
  t(function() {
    let e = document.getElementById("right-links-details");
    if (e) {
      e.addEventListener("toggle", t => {
        if (e.open) {
          document.addEventListener("scroll", t => {
            e.open = false;
          }, {once: true});
        }
      });
    }
  });
  
  // Theme color handling (safely check if elements exist)
  t(function() {
    let e = document.querySelector(".navbar nav");
    if (!e) return; // Skip if element doesn't exist
    
    let t = document.querySelector('meta[name="theme-color"][data-tag=light]');
    let n = document.querySelector('meta[name="theme-color"][data-tag=dark]');
    
    if (!t || !n) return; // Skip if elements don't exist
    
    let o = window.matchMedia("(min-width: 720px)");
    let i = true;
    
    let r = () => {
      if (i) {
        t.setAttribute("content", "#00223E");
        n.setAttribute("content", "#08151E");
      } else {
        if (document.body.classList.contains("look-sheet-bkg") && !o.matches) {
          t.setAttribute("content", "#ffffff");
        } else {
          t.setAttribute("content", "#fffdf7");
        }
        n.setAttribute("content", "#17232D");
      }
    };
    
    try {
      new IntersectionObserver((e, t) => {
        if (e && e.length > 0) {
          i = e[0].isIntersecting;
          r();
        }
      }, {
        root: null,
        rootMargin: "0px",
        threshold: [0]
      }).observe(e);
      
      o.addEventListener("change", () => {
        r();
      });
    } catch (error) {
      console.warn("IntersectionObserver error:", error);
    }
  });
}();