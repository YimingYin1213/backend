---
layout: post 
feedback: true
hide: true
title: HOME | Safe Passage Heals
permalink: /
show_reading_time: false
---


<p id="mario" class="sprite"></p>
<canvas id="fog"></canvas>

<!-- Mobile Controls -->
<div id="controls">
  <button data-dir="up">▲</button>
  <div class="middle">
    <button data-dir="left">◀</button>
    <button data-dir="down">▼</button>
    <button data-dir="right">▶</button>
  </div>
</div>

<!-- ================= STYLES ================= -->

<style>
body {
  background-color: white;
}

/* Prevent touch behavior only on game elements */
#mario,
#controls,
#controls button {
  touch-action: none;
}


  .sprite {
    height: {{pixels}}px;
    width: {{pixels}}px;
    background-image: url('{{sprite_file}}');
    background-repeat: no-repeat;
    position: absolute;
    z-index: 1001;
  }

  #mario {
    background-position: 0 0;
  }

  #fog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999;
  }

  .social-icon {
    filter: invert(1);
  }

  /* ================= MOBILE CONTROLS ================= */

  #controls {
    position: fixed;
    bottom: 20px;
    left: 20px;
    z-index: 2000;
    user-select: none;
  }

  #controls .middle {
    display: flex;
    justify-content: center;
  }

  #controls button {
    width: 60px;
    height: 60px;
    margin: 6px;
    font-size: 24px;
    border-radius: 12px;
    border: none;
    background: rgba(255, 255, 255, 0.15);
    color: black;
    backdrop-filter: blur(6px);
  }

  #controls button:active {
    background: rgba(171, 66, 252, 0.35);
  }
  #controls {
  display: none;
}

@media (max-width: 768px) {
  #controls {
    display: block;
  }
}

</style>

<!-- ================= GAME SCRIPT ================= -->

<script>
  //////////////////// METADATA ////////////////////

  var mario_metadata = {};
  {% for key in hash %}
  mario_metadata["{{key | first}}"] = {
    row: {{key.row}},
    col: {{key.col}},
    frames: {{key.frames}}
  };
  {% endfor %}

  //////////////////// FOG OF WAR ////////////////////

  const fogCanvas = document.getElementById("fog");
  const fogCtx = fogCanvas.getContext("2d");

  function resizeFog() {
    fogCanvas.width = window.innerWidth;
    fogCanvas.height = window.innerHeight;
    fogCtx.fillStyle = "rgba(0,0,0,0.6)";
    fogCtx.fillRect(0, 0, fogCanvas.width, fogCanvas.height);
  }

  window.addEventListener("resize", resizeFog);

  //////////////////// MARIO CLASS ////////////////////

  class Mario {
    constructor(meta) {
      this.meta = meta;
      this.el = document.getElementById("mario");
      this.pixels = {{pixels}};
      this.positionX = 0;
      this.positionY = 200;
      this.frame = 0;
      this.interval = 16;
      this.timer = null;
    }

    animate(state, dx, dy) {
      this.stop();
      const row = state.row * this.pixels;

      this.timer = setInterval(() => {
        const col = (this.frame + state.col) * this.pixels;
        this.el.style.backgroundPosition = `-${col}px -${row}px`;

        this.positionX += dx;
        this.positionY += dy;

        this.el.style.left = `${this.positionX}px`;
        this.el.style.top = `${this.positionY}px`;

        this.frame = (this.frame + 1) % state.frames;

        const rect = this.el.getBoundingClientRect();
        hole.cx = rect.left + rect.width / 2;
        hole.cy = rect.top + rect.height / 2;
      }, this.interval);
    }

    stop() {
      clearInterval(this.timer);
    }

    start(name, dx = 0, dy = 0) {
      this.animate(this.meta[name], dx, dy);
    }
  }

  const mario = new Mario(mario_metadata);



  //////////////////// INPUT (KEYBOARD + TOUCH) ////////////////////

  const keys = { left: false, right: false, up: false, down: false };

  function updateMovement() {
    const dx = (keys.right ? 5 : 0) + (keys.left ? -5 : 0);
    const dy = (keys.down ? 5 : 0) + (keys.up ? -5 : 0);

    if (!dx && !dy) {
      mario.stop();
      return;
    }

    mario.start(keys.left && !keys.right ? "WalkL" : "Walk", dx, dy);
  }

  window.addEventListener("keydown", e => {
    switch (e.key.toLowerCase()) {
      case "a":
      case "arrowleft": keys.left = true; break;
      case "d":
      case "arrowright": keys.right = true; break;
      case "w":
      case "arrowup": keys.up = true; break;
      case "s":
      case "arrowdown": keys.down = true; break;
    }
    updateMovement();
  });

  window.addEventListener("keyup", e => {
    switch (e.key.toLowerCase()) {
      case "a":
      case "arrowleft": keys.left = false; break;
      case "d":
      case "arrowright": keys.right = false; break;
      case "w":
      case "arrowup": keys.up = false; break;
      case "s":
      case "arrowdown": keys.down = false; break;
    }
    updateMovement();
  });

document.querySelectorAll("#controls button").forEach(btn => {
  const dir = btn.dataset.dir;

  btn.addEventListener("pointerdown", e => {
    e.preventDefault();
    keys[dir] = true;
    updateMovement();
  });

  btn.addEventListener("pointerup", () => {
    keys[dir] = false;
    updateMovement();
  });

  btn.addEventListener("pointercancel", () => {
    keys[dir] = false;
    updateMovement();
  });

  btn.addEventListener("pointerleave", () => {
    keys[dir] = false;
    updateMovement();
  });
});


  //////////////////// INIT ////////////////////

  document.addEventListener("DOMContentLoaded", () => {
    resizeFog();
    mario.el.style.transform = `scale(${0.2 * (window.devicePixelRatio || 1)})`;
    mario.start("Rest");

    const rect = mario.el.getBoundingClientRect();
    hole.cx = rect.left + rect.width / 2;
    hole.cy = rect.top + rect.height / 2;
    hole.targetRadius = Math.hypot(fogCanvas.width, fogCanvas.height);
    requestAnimationFrame(animateFog); 
  });
</script>

<!-- ================= PAGE CONTENT ================= -->

<div style="display: flex; align-items: flex-start; justify-content: center; gap: 40px; flex-wrap: wrap; color: black;">
<img src="{{site.baseurl}}/safepassageheals/sphbg1.png" alt="Home | Safe Passage Heals" style="width: 100%; max-width: 100%;">

<a href="https://ruchikak19.github.io/flaskandfurious/recovery/" style="display: block; margin-bottom: 16px; color: #6a0dad; font-weight: bold;">Click here for an interactive simulation on the path to recovery after experiencing domestic violence</a>

<strong>Who we are</strong>
Founded in 2000, Safe Passage Heals is a non-profit serving Southern California. Our mission is to break the cycle of domestic abuse by healing and empowering women and children, enabling them to live new, safe and productive lives. Since its creation, more than 2000 women and children have come to Safe Passage Heals looking for counseling and shelter. Founded by a domestic violence survivor herself, Trish Steele was inspired to help women and their children break the cycle of abuse and started as a small ministry out of her house, which grew into Safe Passage Heals and has served many over the years.

Our clients have a 95% success rate in breaking the cycle of domestic violence and creating a new life for themselves and their children. Upon completing our six-month program "Stepping Stones to a New Life," our graduates find steady employment and secure housing and enter the workforce in various industries such as nursing, social work, and cosmetology.

<img src="{{site.baseurl}}/safepassageheals/sph-kp.png" alt="Safe Passage Heals" style="width: 100%; max-width: 100%; margin-top: 20px;">

</div>