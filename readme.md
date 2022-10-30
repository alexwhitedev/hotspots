- Запуск через Flask
$env:FLASK_APP="hotspots.py"

- API endpoint: 'host:port/api/user_hotspots_stat/<stat_field>/user/<int:user_id>'

- stat field имеет 5 вариантов в соответствии с задачей (добавил докстринг в соответстующих методах в user_project_stats.py):
1) hotspots_quantity
2) hotspots_with_places_quantity
3) hotspots_dates
4) hotspots_scored
5) hotspots_conns

- пример запросов и ответов можно получить при запуске client_test.py (при запущенном приложении)

- тесты в u_tests.py (забавно, что пригодились)

- user_id в соответствии с users.csv

- в тех задачах, где нет "за всё время", я понимал, что имеются в виду хотспоты, которые не удалены (NaN/Null в deleted_at поле)

- графики и предложенные метрики находятся в ноутбуке test_cast.ipynb
