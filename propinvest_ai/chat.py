import json

from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts.chat import PromptTemplate
from pydantic import BaseModel

from propinvest_ai.settings import settings

chat = GigaChat(
    credentials=settings.giga_token,
    scope=settings.giga_scope,
    verify_ssl_certs=False,
)


class Answer(BaseModel):
    score: int


parser = PydanticOutputParser(pydantic_object=Answer)  # type: ignore

system_message = """
{}

JSON выше результат анкетирования, характеристики человека.


На основе анкетирования давай ответы на вопросы о пользователе.
Твоим ответом должно быть одно число (float) от -2 до 5.
На основе анкетирования давай ответы на вопросы о пользователе.
Твоим ответом должно быть одно число (float) от -2 до 5. Не пытайся расписать подробно!
Ответь только одним числом!

"""

criteria = [
    {
        "title": "Уровень транспортной доступности",
        "criteria": "Низкий: -1;Высокий: 5",
    },
    {
        "title": "Перспективы изменения уровня транспортной доступности",
        "criteria": "Нет: 0;  Есть перспективы улучшения: 2;",
    },
    {
        "title": "Улучшение комфорта транспортного обслуживания",
        "criteria": "Нет: 0;  Есть: 0,2;",
    },
    {
        "title": "Количество бесплатных общественных парковочных мест на 1 квартиру в шаговой доступности",
        "criteria": "Менее 0.1: 0; 0.1-0.2 места: 0; 0.2-0.3 места: 0.1; 0.3-0.5 места: 0.25; 0.5-0.7: 0.4; 0.7-1 место: 0.65;",
    },
    {
        "title": "Количество платных общественных парковочных мест на 1 квартиру в шаговой доступности",
        "criteria": "Менее 0.1: 0; 0.1-0.2 места: 0; 0.2-0.3 места: 0.1; 0.3-0.5 места: 0.25; 0.5-0.7: 0.4; 0.7-1 место: 0.65",
    },
    {
        "title": "Количество машиномест в доме или на земельном участке на 1 квартиру",
        "criteria": "Менее 0.2 места: 0; 0.2-0,5 места: 1; 0.5-1 место: 2.5; более 1 места: 3",
    },
    {"title": "Лифт в паркинг", "criteria": "Нет: 0; Есть 0,4;"},
    {"title": "Зарядка для электромобилей", "criteria": "Нет: 0; Есть: 0.1;"},
    {
        "title": "Обеспеченность детскими садами в шаговой доступности",
        "criteria": "Нет: -1.2; Нет, но будет после завершения строительства: 0.6; Уже имеется: 2;",
    },
    {
        "title": "Обеспеченность школами в шаговой доступности",
        "criteria": "Нет: -1.2; Нет, но будет после завершения строительства: 0.6; Уже имеется: 2;",
    },
    {
        "title": "Обеспеченность поликлиникой в шаговой доступности",
        "criteria": "Нет: -1.2; Нет, но будет после завершения строительства: 0.6; Уже имеется: 2;",
    },
    {
        "title": "Обеспеченность продуктовыми магазинами в шаговой доступности",
        "criteria": "Будет: 0.1; Есть 0.2;",
    },
    {
        "title": "В районе есть крупный торговый центр",
        "criteria": "Нет:0; Есть или будет: 0.2;",
    },
    {
        "title": "В районе есть спортивные секции",
        "criteria": "Нет: 0; Есть или будет: 0.3; ",
    },
    {
        "title": "Летняя программа спорта",
        "criteria": "Нет: 0; 1-2 массовых вида спорта: 0.4; 3-5 массовых вида спорта: 0.9; Более 5 массовых видов спорта: 1.4; ",
    },
    {
        "title": "Зимняя программа спорта",
        "criteria": "Нет: 0; 1 массовый вид спорта: 0.4; Более 2 массовых видов спорта: 1.4;",
    },
    {
        "title": "Обеспеченность фитнес центрами в шаговой доступности",
        "criteria": "Нет: 0; 1-3 программы: 0.1; 4-5 программ: 0.4; 6 и более программ: 0.6;",
    },
    {
        "title": "Бассейн в шаговой доступности",
        "criteria": "Нет: 0; Есть: 0.4;",
    },
    {"title": "Двор без машин", "criteria": "Нет: 0; Да: 1.6;"},
    {
        "title": "Пешеходная улица внутри жилого комплекса",
        "criteria": "Нет: 0; Есть: 1;",
    },
    {"title": "Мощение пешеходных путей", "criteria": "Нет: 0; Есть: 0.5;"},
    {
        "title": "Парковая территория внутри жилого комплекса",
        "criteria": "Нет: 0; Есть от 0.5 га.: 1;",
    },
    {
        "title": "Озеленение двора кустарниками и деревьями",
        "criteria": "Нет: 0; Есть: 0.2; Есть, с учетом четырех сезонов: 1; ",
    },
    {"title": "Ландшафтный дизайн", "criteria": "Нет: 0; Есть: 0.6; "},
    {
        "title": "Двор на эксплуатируемой кровле дома",
        "criteria": "Нет: 0; Да: 0.5;",
    },
    {
        "title": "Велопарковка",
        "criteria": "Нет: 0; Есть: 0.3; Есть крытая: 0.5;",
    },
    {
        "title": "Дворовая спортплощадка workout",
        "criteria": "Нет: 0; Есть: 0.4; ",
    },
    {"title": "Малые архитектурные формы", "criteria": "Нет: 0; Есть: 0.4;"},
    {
        "title": "Деление дворового пространства по возрастным зонам",
        "criteria": "Нет: 0; Да: 0.4;",
    },
    {
        "title": "Детская площадка с улучшенным травмобезопасным покрытием",
        "criteria": "Нет: -0.5; Да: 0;",
    },
    {"title": "Дворовый интернет", "criteria": "Нет: 0; Есть: 0.1;"},
    {"title": "Зона выгула собак", "criteria": "Нет: 0; Есть: 0.5;"},
    {"title": "Наличие службы консьержа", "criteria": "Нет: 0; Есть: 2;"},
    {"title": "Огороженная территория", "criteria": "Нет: 0; Есть: 2;"},
    {"title": "Видеонаблюдение", "criteria": "Нет: 0; Есть: 3;"},
    {"title": "Наличие КПП или пункта охраны", "criteria": "Нет: 0; Есть: 3;"},
    {
        "title": "Вход в подъезд по смарт картам или с мобильного приложения",
        "criteria": "Нет: 0; Есть: 3;",
    },
]


def get_answer(payload: str):
    messages: list[BaseMessage] = [
        SystemMessage(content=system_message.format(payload))
    ]

    answer = {}

    for index, criterion in enumerate(criteria):
        user_message = HumanMessage(
            content=f"На сколько важно {criterion['title']}?. Критерии: {criterion['criteria']}"
        )
        print(f"{index} of {len(criteria)}", flush=True)
        result = chat([*messages, user_message])
        answer[criterion["title"]] = result.content
    return answer