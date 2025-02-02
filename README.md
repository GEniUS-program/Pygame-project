**Название проекта**

Space Invaders: Galactic Defense

**Авторы проекта**

Никитин Роман Ильич (Nikitin Roman Ilyich)

**Описание идеи**

Проект "*Space Invaders: Galactic Defense*" представляет собой аркадную игру, вдохновленную классическими космическими шутерами.
Игрок управляет космическим кораблем, который защищает планету от волн атакующих врагов. 
Цель игры заключается в уничтожении как можно большего числа врагов, зарабатывая очки и улучшая свой корабль. 
Игра предлагает динамичный игровой процесс, разнообразные уровни сложности и возможность улучшения навыков игрока через систему апгрейдов.

**Описание реализации**

Реализация игры выполнена с использованием библиотеки Pygame, что позволяет создать графику и анимацию, а также обрабатывать ввод пользователя. 
Основные классы и структуры данных включают в себя:

Игрок: управляет движением космического корабля и стрельбой. Реализована возможность многократной стрельбы, что добавляет динамики в игровой процесс.
Враги: создаются с различными параметрами здоровья и скоростью, что делает каждую волну уникальной. В игре предусмотрены разные модели врагов, в том числе более сложные, которые появляются на более высоких уровнях.
Пули: реализована система стрельбы, где игрок может стрелять несколькими пулями одновременно. Пули движутся вверх по экрану, пока не выйдут за его пределы или не столкнутся с врагами.
Система волн: игра разделена на волны, каждая из которых требует от игрока уничтожить определенное количество врагов для перехода на следующий уровень. При достижении новых волн увеличивается сложность, что требует от игрока адаптации.
Графика и звук: используются звуковые эффекты для различных действий (стрельба, столкновения и т.д.), что значительно улучшает погружение в игровой процесс.
Описание технологий + необходимые для запуска библиотеки

**Для разработки игры использовались следующие технологии и библиотеки**:

*Pygame*: основная библиотека для создания игр, обеспечивающая работу с графикой, звуком и обработкой событий.
*Sys*: используется для управления системными функциями, такими как завершение игры.
*Random*: применяется для генерации случайных чисел, что необходимо для спавна врагов и их характеристик.
*Json*: используется для хранения данных о максимальном количестве очков.
