class AnimEyes {
  constructor() {
    this.eyes = document.querySelectorAll(".eye");
    this.maxOffset = 6;
    this.init();
  }

  init() {
    document.addEventListener("mousemove", (event) => {
      this.eyes.forEach((eye) => this.moveEye(eye, event));
    });
  }

  moveEye(eye, event) {
    const iris = eye.querySelector(".iris");
    const rect = eye.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    let dx = event.clientX - centerX;
    let dy = event.clientY - centerY;

    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance > this.maxOffset) {
      dx = (dx / distance) * this.maxOffset;
      dy = (dy / distance) * this.maxOffset;
    }

    iris.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
  }
}

class AnimSign {
  constructor() {}
}
// inicializa a animação dos olhos
new AnimEyes();
