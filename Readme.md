<h1> Данный проект представляет собою решение <a href="https://docs.google.com/document/d/1XTnbcXhejyGB-I2cHRiiSZqI3ElHzqDJeetwHkJbTa8/edit?tab=t.0">тестового задания</a></h1>


<h3>Стек:</h3> Python3.13, Django
<h3>База данных:</h3> SQLite3
<h3>Контейнерезация:</h3> Docker (docker-compose)

<h2>Время выполнения:</h2> 10-15 часов всего (в течение 3-4 дней)


<h3>Инструкция по запуску #1 (Docker):</h3>
<ol>
    <li>docker-compose up --build -d</li>
</ol>
<h3>Инструкция по запуску #2 (Ubuntu, MacOS (No Docker)):</h3>
<ol>
    <li>python3.13 -m venv venv</li>
    <li>source venv/bin/activate</li>
    <li>cd DjangoTreeMenu</li>
    <li>chmod +x entrypoint.sh</li>
    <li>./entrypoint.sh</li>
    <li>python3 manage.py runserver</li>
</ol>

<h2>Готово!</h2>
<h3>http://127.0.0.1:8000/menu/</h3>


<h1>Меню</h1>
<img src="https://i.ibb.co/QFT4yYj2/2025-05-16-18-57-13.jpg" />

<h1>Админка</h1>
<img src="https://i.ibb.co/nNN1w7RG/2025-05-16-18-58-07.jpg" />


<h3>Что можно улучшить?</h3>
<ul>
    <li>Использовать базу данных - Posqtgresql</li>
    <li>Добавить кеширование - Redis</li>
    <li>Добавить разделение настроек settings/ base.py, local.py, dev.py, prod.py</li>
    <li>И прочие тонкости перехода (тесты, cicd и тп тп) в prod...</li>
</ul>
