
  // Получаем текущую сохраненную цветовую схему из localStorage
  const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

  // Если цветовая схема уже была сохранена, устанавливаем ее
  if (currentTheme) {
      document.documentElement.setAttribute('data-bs-theme', currentTheme);
  }

  // Обработчик события для переключения цветовой схемы
  document.getElementById('bd-theme').addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme');

      // Если текущая цветовая схема - светлая, переключаем на темную
      if (currentTheme === 'light') {
          document.documentElement.setAttribute('data-bs-theme', 'dark');
          localStorage.setItem('theme', 'dark');
      } 
      // Если текущая цветовая схема - темная или автоматическая, переключаем на светлую
      else {
          document.documentElement.setAttribute('data-bs-theme', 'light');
          localStorage.setItem('theme', 'light');
      }
  });

