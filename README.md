# LunaGame
LUNAGAME - проект по программированию на языке Python, 
на который была потрачена уйма времени и сил. Идея для 
реализации появилась спонтанно, буквально из пустоты,но
по ходу разработки ни разу не возникло желания ее сменить, что все время добавляло мотивации.
Сама игра представляет собой РПГ в локации легендарного общежития №6 ФОПФ МФТИ. Передвигайся 
между локациями, сражайся с уникальными противниками, участвуй в интересных диалогах и узнай тайну Шестерки!
# Цель разработки
В проекте реализовано 2,5D пространство, что делает его в своем роде уникальным в жанре РПГ.
Менее 10 % игр выходят из рамок традиций и готовы экспериментировать, данный проект как раз из таких!
Главной целью разработки было создать комфортные, движкоподобные условия труда.

В проекте реализовано множество механик, повышающих скорость работы при разработке.
Одна из таких - модуль Scene_editor, позволяющий менять положение, размер, слой отрисовки объектов на сцене,
после всех изменений все положения сохраняется в SaveFile, откуда с ними удобно работать. Еще реализована работа со спрайт-листами, в которых изначально хранились все анимации.
Функция crop_image - разрезает изображение на несколько по количеству на различных осях, используя библиотеку PIL. 

В общем и целом цель была достигнута, работать стало гораздо удобнее.
# Структура проекта
Структура получилась достаточно сложной, но тем не менее логичной и немного удобной.
В сам проект входит 6 директорий под отдtльные функции: 

**Animations** - под разбитые на папки анимации, в которых они хранятся покадрово,
**dialogues** - тексты отдельных диалогов, в котором хранится информация об одном отдельном диалоге,
**materials** - все картинки, используемые в проекте,
**music** - вся музыка,

**bosses** и **scenes** - модули для отдельно взятых игровых сцен и сцен боевого режима. Для сцен и боссов есть
общие модули, которые называются соответственно Scene_class и Battle_scene, которые содержат общие для модулей элементы, например 
при отрисовке спрайтов в сцене вызывается класс из модуля Class_scene, в котором и прописана функция отрисовки, соответсвенно
отрисованный объект попадет на поверхность, находящуюся в Scene_class, которая в итоге и будет отрисована в модуле draw.

Для оптимизации работы программы отрисовываемая поверхность разделена на две части - статичная картинка - меняется только при создании сцены
и в особых случаях и изменяющийся экран, на нем отрисовка динамическая, и он отрисовывается на слой выше, с помощью этого можно отрисовывать подвижные 
объекты на сцене, например всплывающий текст, анимации персонажей и.т.д. С помощью этого игра стабильно выдает 60 ФПС.

Отрисовка происходит в три этапа: изначально персонажу присваиваются новые координаты, исходя из нажатий клавиш и внешних условий,
затем эти координаты посылаются в текущую сцену и происходит их обработка, в следствии которой возращаются возможные координаты игрока, 
которые допустимы в данной игровой ситуации (например при коллизии), а также происходит обработка столкновений с классом Area,
который при взаимодействии с игроком может посылать заранее заданные сигналы.

После происходит отрисовка элементов сцены на поверхности в Scene_Class, которая отрисовывается на главной поверхности экрана
по координатам камеры в игровом мире (статичная картинка под изменяющейся). Поверх этого отрисовывается игрок, после - элементы меню.

Модуль main отвечает за загрузку - сохранение игрового процесса, за игровую музыку, за базовые настройки ФПС, громкости итд

Также в проекте присутствует модуль globalsc, который является на глобальный скрипт связи. Изначально задумка была
в реализации быстрого доступа из одного модуля к другому, посредством избежания параллельного импорта, но в итоге 
там осталась лишь пара функций, не отвечающих за игровой процесс. В данный момент его смысл в управлении константами, которые используются
в большинстве модулей.

# Разработчики проекта
Студенты ЛФИ : Краев Алексей и Долгова Екатерина. За ними закрепляются все авторские права.

