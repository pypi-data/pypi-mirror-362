#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import (
    Iterable,
)

import click
import jinja2


template_loader = jinja2.FileSystemLoader(searchpath="./kibana_templates")
template_env = jinja2.Environment(loader=template_loader)


JSON = 'json'
NDJSON = 'ndjson'


class ResultObject:
    """
    Объект в экосистеме kibana
    """
    def generate(self, **kwargs):
        raise NotImplementedError

    def get_result_list(self, items):
        return '[\n' + ',\n '.join(items) + '\n]'

    def get_result_str(self, items, format):
        result = ','.join(items).replace(
            r'"',
            r'\"'
        ).replace(
            '\n',
            ''
        )

        return result


class Visualization(ResultObject):
    """Класс для визуализации"""
    guid = ''
    title = ''

    def __init__(self, height=15):
        super().__init__()

        self.height = height

    def generate(self, index_guid, format=JSON, **kwargs):
        state = template_env.get_template(
            f'{self.guid}.{format}'
        ).render(
            title=self.title,
        )

        return template_env.get_template(
            f'visualization.{format}'
        ).render(
            guid=self.guid,
            title=self.title,
            index_guid=index_guid,
            visualization_state=self.get_result_str([state], format),
        )


class RequestsDistributionByServerTime(Visualization):
    guid = '3a512643-ea85-463d-b408-e2a527030178'
    title = 'Распределение запросов по временным интервалам, серверное время, мсек'


class RequestsDistributionByClientTime(Visualization):
    guid = '77d1d261-5025-4f00-822e-ecce3a61886b'
    title = 'Распределение запросов по временным интервалам, клиентское время, мсек'


class RequestsDistributionBySQLTime(Visualization):
    guid = '6f09dbaf-1fb8-457e-94ff-75e0efa71e6f'
    title = 'Распределение запросов по временным интервалам, время SQL, мсек'


class MoreThanFiveRequestCountByServerTime(Visualization):
    guid = '6b79ba24-7a52-4db1-93c1-3317d45b397f'
    title = 'Количество запросов >5 секунд по серверному времени'


class MoreThanFiveRequestCountByClientTime(Visualization):
    guid = 'b3e3060d-e4da-4649-99f9-9c427ef58b10'
    title = 'Количество запросов >5 секунд по клиентскому времени'


class RequestCount(Visualization):
    guid = '841f8f54-2011-42d0-ae6b-c7cfd2586135'
    title = 'Общее количество запросов'


class TopTenURLMoreThanFiveRequestCountByClientTime(Visualization):
    guid = '929f45e1-f584-40c5-9150-7ec864105243'
    title = 'Топ 10 URL по количеству запросов по клиентскому времени >5 секунд'


class TopTenURLMoreThanFiveRequestCountByServerTime(Visualization):
    guid = '64be2e2b-7009-4e79-b1bc-de7eda3bb7e7'
    title = 'Топ 10 URL по количеству запросов по серверному времени >5 секунд'


class TopTenURLSumByServerTime(Visualization):
    guid = '84eb1ad1-72ce-481d-844f-94bf2f6029d3'
    title = 'Топ 10 URL по суммарному времени выполнения по серверному времени'


class TopTenURLSumBySQLTime(Visualization):
    guid = '339465aa-d599-47c9-a012-0a54f7371592'
    title = 'Топ 10 URL по суммарному времени выполнения по времени SQL'


class TopTenURLRequestCount(Visualization):
    guid = '4dc730e6-5b8a-4946-b71d-b813b9db66df'
    title = 'Топ 10 URL по количеству запросов'


class TopTenURLMoreThanFiveAverageByClientTime(Visualization):
    guid = 'c9579300-eb07-4255-9c2b-f6a3680e6761'
    title = 'Топ 10 URL по среднему времени выполнения по клиентскому времени >5 секунд'


class TopTenURLMoreThanFiveAverageByServerTime(Visualization):
    guid = '042005bc-1ab4-4139-9582-6ca1e08fb67d'
    title = 'Топ 10 URL по среднему времени выполнения по серверному времени >5 секунд'


class AverageByClientTime(Visualization):
    guid = '0ac8157f-70c5-404f-a219-5d7047a41aa6'
    title = 'Среднее время выполнения запросов по клиентскому времени'


class AverageByServerTime(Visualization):
    guid = 'fc79a5af-187e-413f-8a92-9957935ea126'
    title = 'Среднее время выполнения запросов по сервеному времени'


class TopTenURLAverageByClientTime(Visualization):
    guid = '96d1a6b7-d47d-4002-9956-dc8a599d99c4'
    title = 'Топ 10 URL по среднему времени выполнения по клиентскому времени'


class TopTenURLAverageByServerTime(Visualization):
    guid = 'bcbf9911-e0bb-4609-8057-94f3d0e38e7b'
    title = 'Топ 10 URL по среднему времени выполнения по серверному времени'


class AverageBySQLTime(Visualization):
    guid = 'd5cc5991-e2d1-4136-98a6-fc3363be947b'
    title = 'Среднее время выполнения запросов по времени SQL'


class TopTenURLAverageBySQLTime(Visualization):
    guid = '584cdda6-291b-4402-b7f1-2de3ba15f896'
    title = 'Топ 10 URL по среднему времени выполнения по времени SQL'


class SumRequestTime(Visualization):
    guid = 'f8e6099c-5a10-4102-875e-170f90ec5882'
    title = 'Суммарное время выполнения запросов'


class AverageRequestTime(Visualization):
    guid = 'c9169a10-06a0-4ec9-bd17-53ce822275d7'
    title = 'Среднее время выполнения запросов'


class SumRequestClientTime(Visualization):
    guid = 'a7901d1d-8478-41ec-83ae-fdadb35095b5'
    title = 'Суммарное время выполнения запросов по клиентскому времени'


class SumRequestServerTime(Visualization):
    guid = 'c7d15a8b-9854-4331-82b8-9c06e6725f56'
    title = 'Суммарное время выполнения запросов по серверному времени'


class SumRequestSQLTime(Visualization):
    guid = 'a143eecb-30cf-4469-9510-c9842d0d15cd'
    title = 'Суммарное время выполнения запросов по времени SQL'


class TopTenURLSumByClientTime(Visualization):
    guid = '51e1b7b6-54d0-40b1-a3af-d3a453978643'
    title = 'Топ 10 URL по суммарному времени выполнения по клиентскому времени'


class TopTenURLMoreThanFiveRequestCountBySQLTime(Visualization):
    guid = '934140d7-538d-4cd3-9ca6-900eb3b3b459'
    title = 'Топ 10 URL по количеству запросов по времени SQL >5 секунд'


class RequestByTime(Visualization):
    guid = '8c2d2451-7732-4bde-9fab-b45772311c02'
    title = 'Распределение запросов по времени'


class RequestBySQLCount(Visualization):
    guid = '00e3358b-2ad5-4105-a8f8-f78876c18b1b'
    title = 'Распределение запросов по количеству SQL, шт'


class UniqueUserCountPerHours(Visualization):
    guid = '14bb8fb2-849a-4d88-81fc-9b1e221d374c'
    title = 'Количество уникальных пользователей в час'


class Dashboard(ResultObject):
    """
    Доска для kibana
    """
    guid = ''
    title = ''
    visualizations = tuple()

    def __init__(self, index_guid, max_width=48, row_height=15):
        super().__init__()

        self.index_guid = index_guid
        self.max_width = max_width
        self.row_height = row_height

    def get_visualizations(self, convert=True):
        """
        Возвращает набор визуализаций для доски
        convert - конвертировать ли структуру для визуализаций
        """
        panel_index = 1

        for row_index, row in enumerate(self.visualizations):
            if not isinstance(row, Iterable):
                row = [row]

            width = int(self.max_width / len(row))

            for item_index, item in enumerate(row):
                params = {
                    'guid': item.guid,
                    'x': item_index * width,
                    'y': row_index * self.row_height,
                    'w': width,
                    'h': self.row_height,
                    'panel_index': panel_index,
                }

                if convert:
                    params['data'] = item.generate(index_guid=self.index_guid)

                yield params

                panel_index += 1

    def generate(self, format=JSON, generate_visualizations=True):
        """
        Генерирует представление объекта
        """
        result_data = []
        panel_data = []

        for visualization in self.get_visualizations(generate_visualizations):
            panel_data.append(
                template_env.get_template(
                    f'dashboard_item.{format}'
                ).render(
                    **visualization
                )
            )

            if generate_visualizations:
                result_data.append(visualization['data'])

        panel = template_env.get_template(
            f'dashboard.{format}',
        ).render(
            **{
               'title': self.title,
               'guid': self.guid,
               'panel_data': self.get_result_str(panel_data, format)
            }
        )
        result_data.append(panel)
        result = self.get_result_str(result_data, format)

        return result


class ProductionRequestDashboard(Dashboard):
    """
    Доска для данных логов production-request
    """
    guid = 'f3b424b2-d4e2-4d65-bce0-8db25cfd9037'
    title = 'ProductionRequest'
    visualizations = (
        (
            RequestCount(),
        ),
        (
            MoreThanFiveRequestCountByClientTime(),
            MoreThanFiveRequestCountByServerTime(),
        ),
        (
            SumRequestTime(),
        ),
        (
            AverageRequestTime(),
        ),
        (
            RequestByTime(),
        ),
        (
            RequestBySQLCount(),
        ),
        (
            RequestsDistributionByClientTime(),
        ),
        (
            RequestsDistributionByServerTime(),
        ),
        (
            RequestsDistributionBySQLTime(),
        ),
        (
            TopTenURLRequestCount(),
        ),
        (
            TopTenURLSumByClientTime(),
        ),
        (
            TopTenURLSumByServerTime(),
        ),
        (
            TopTenURLSumBySQLTime(),
        ),
        (
            TopTenURLMoreThanFiveRequestCountByClientTime(),
        ),
        (
            TopTenURLMoreThanFiveRequestCountByServerTime(),
        ),
        (
            AverageByClientTime(),
        ),
        (
            AverageByServerTime(),
        ),
        (
            AverageBySQLTime(),
        ),
        (
            TopTenURLAverageByClientTime(),
        ),
        (
            TopTenURLAverageByServerTime(),
        ),
        (
            TopTenURLAverageBySQLTime(),
        ),
        (
            TopTenURLMoreThanFiveAverageByClientTime(),
        ),
        (
            TopTenURLMoreThanFiveAverageByServerTime(),
        ),
        (
            TopTenURLMoreThanFiveRequestCountBySQLTime(),
        ),
        (
            UniqueUserCountPerHours(),
        ),
        (
            SumRequestClientTime(),
        ),
        (
            SumRequestServerTime(),
        ),
        (
            SumRequestSQLTime(),
        ),
    )


@click.command()
@click.argument('guid')
@click.option('--format', default=JSON, help='Формат выходного файла')
def export_dashboard(guid, format):
    result_data = ProductionRequestDashboard(guid).generate(format=format)
    with open(f'{guid}.{format}', 'w') as f:
        f.write(result_data)


if __name__ == '__main__':
    export_dashboard()

