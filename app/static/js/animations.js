const texts = [
    "Это интерактивное ИИ резюме.",
    "Задавайте какие угодно вопросы.",
    "Вы знали, что ИИ лучше знает английский?",
    "Будующее уже наступило."
  ];
  
  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let isTypingPaused = false;
  
  function typeText() {
    const currentText = texts[textIndex];
    if (!isDeleting && charIndex <= currentText.length) {
      document.getElementById("text-container").textContent = currentText.substring(0, charIndex);
      charIndex++;
      setTimeout(typeText, 160); // Задержка между печатью символов
    } else if (isDeleting && charIndex >= 0) {
      document.getElementById("text-container").textContent = currentText.substring(0, charIndex);
      charIndex--;
      setTimeout(typeText, 70); // Задержка перед стиранием символов
    } else {
      isDeleting = !isDeleting;
      if (!isDeleting) {
        textIndex = (textIndex + 1) % texts.length;
      }
      setTimeout(typeText, 800); // Задержка перед началом следующего текста
    }
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    typeText(); // Запуск анимации печати текста
  });