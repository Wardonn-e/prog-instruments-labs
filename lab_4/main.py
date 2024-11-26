import aiohttp
import re
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from lab_7.constants import BOT_TOKEN, WEATHER_API_KEY

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Логи в консоль
        logging.FileHandler("weather_bot.log", mode="a", encoding="utf-8")  # Логи в файл
    ],
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Константы
API_URLS = {
    "current_weather": "http://api.openweathermap.org/data/2.5/weather",
    "forecast": "http://api.openweathermap.org/data/2.5/forecast",
}
WEATHER_PARAMS = {
    "appid": WEATHER_API_KEY,
    "units": "metric",
    "lang": "ru",
}


async def fetch_weather_data(url: str, params: dict) -> Optional[dict]:
    """
    Универсальная функция для запросов к API OpenWeather.

    :param url: URL для запроса.
    :param params: Параметры для запроса.
    :return: Данные в формате JSON.
    """
    logger.info(f"Запрос к API: {url} с параметрами {params}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    logger.info(f"Успешный ответ от API: {url}")
                    return await response.json()
                logger.warning(f"Ошибка API {url}: статус {response.status}")
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка сети при запросе {url}: {e}")
    return None


async def get_weather(lat: Optional[float] = None, lon: Optional[float] = None, city_name: Optional[str] = None) -> str:
    """
    Получение текущей погоды.

    :param lat: Широта.
    :param lon: Долгота.
    :param city_name: Название города.
    :return: Строка с описанием погоды.
    """
    params = WEATHER_PARAMS.copy()
    if city_name:
        params["q"] = city_name
        logger.info(f"Запрос погоды по городу: {city_name}")
    elif lat and lon:
        params["lat"] = lat
        params["lon"] = lon
        logger.info(f"Запрос погоды по координатам: lat={lat}, lon={lon}")
    else:
        logger.warning("Не указаны данные для поиска погоды.")
        return "Не указаны данные для поиска погоды."

    data = await fetch_weather_data(API_URLS["current_weather"], params)
    if not data:
        logger.error("Не удалось получить данные о погоде.")
        return "Не удалось получить данные о погоде."

    weather = data.get("weather", [{}])[0].get("description", "Неизвестно").capitalize()
    temp = data.get("main", {}).get("temp", "Неизвестно")
    city = data.get("name", "Неизвестный город")
    logger.info(f"Погода в {city}: {weather}, {temp}°C")
    return f"Погода в {city}:\n{weather}, {temp}°C"


async def get_forecast(city_name: str) -> str:
    """
    Получение прогноза погоды.

    :param city_name: Название города для прогноза.
    :return: Строка с прогнозом погоды.
    """
    params = WEATHER_PARAMS.copy()
    params["q"] = city_name
    logger.info(f"Запрос прогноза погоды для города: {city_name}")

    data = await fetch_weather_data(API_URLS["forecast"], params)
    if not data:
        logger.error("Не удалось получить данные о прогнозе.")
        return "Не удалось получить данные о прогнозе."

    forecast_list = [
        f"{forecast.get('dt_txt', 'Неизвестно')}: "
        f"{forecast.get('weather', [{}])[0].get('description', 'Неизвестно').capitalize()}, "
        f"{forecast.get('main', {}).get('temp', 'Неизвестно')}°C"
        for forecast in data.get("list", [])[:10]
    ]
    if forecast_list:
        logger.info(f"Успешно получен прогноз для {city_name}.")
    else:
        logger.warning(f"Прогноз для {city_name} не найден.")
    return "\n".join(forecast_list) if forecast_list else "Прогноз не найден."


def get_weather_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание клавиатуры для взаимодействия с пользователем.

    :return: Объект клавиатуры с кнопками.
    """
    logger.info("Создание клавиатуры для взаимодействия.")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отправить геопозицию", request_location=True))
    keyboard.add(KeyboardButton("Узнать погоду по городу"))
    keyboard.add(KeyboardButton("Прогноз на 5 дней"))
    return keyboard


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """
    Обработчик команды /start.

    :param message: Объект сообщения.
    """
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    await message.reply(
        "Привет! Я могу рассказать тебе о погоде. Выбери действие:",
        reply_markup=get_weather_keyboard(),
    )


@dp.message_handler(content_types=ContentType.LOCATION)
async def handle_location(message: types.Message):
    """
    Обработчик геопозиции от пользователя.

    :param message: Объект сообщения.
    """
    logger.info(f"Получена геопозиция от пользователя {message.from_user.id}: {message.location}")
    if message.location:
        weather_info = await get_weather(lat=message.location.latitude, lon=message.location.longitude)
        await message.reply(weather_info)


@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: types.Message):
    """
    Обработчик текстовых сообщений от пользователя.

    :param message: Объект сообщения.
    """
    user_input = message.text.strip().lower()
    logger.info(f"Получено текстовое сообщение от пользователя {message.from_user.id}: {user_input}")
    forecast_match = re.match(r"прогноз\s+(.+)", user_input, re.IGNORECASE)

    if user_input == "узнать погоду по городу":
        await message.reply("Введите название города, чтобы узнать погоду.")
    elif user_input == "прогноз на 5 дней":
        await message.reply("Введите название города для получения прогноза на 5 дней.")
    elif forecast_match:
        city_name = forecast_match.group(1).strip()
        forecast_info = await get_forecast(city_name)
        await message.reply(forecast_info)
    else:
        city_name = message.text.strip()
        weather_info = await get_weather(city_name=city_name)
        await message.reply(weather_info)


@dp.message_handler()
async def handle_unknown(message: types.Message):
    """
    Обработчик неизвестных сообщений.

    :param message: Объект сообщения.
    """
    logger.warning(f"Неизвестное сообщение от пользователя {message.from_user.id}: {message.text}")
    await message.reply("Я понимаю только команды /start, геопозицию и названия городов.")


# Запуск бота
if __name__ == "__main__":
    logger.info("Запуск бота...")
    executor.start_polling(dp, skip_updates=True)
