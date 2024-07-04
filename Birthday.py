import pandas as pd
from datetime import datetime
import random
from whatsapp_api_client_python.API import GreenAPI

# Green API credentials
INSTANCE_ID = 'INSTANCE ID HERE'  # Replace with your instance ID
API_TOKEN = 'API TOKEN HERE'  # Replace with your API token
GROUP_CHAT_ID = 'WHATSAPP GROUP CHAT ID HERE'  # Replace with your group chat ID
# GROUP_CHAT_ID = 'WHATSAPP GROUP CHAT ID HERE'  # Alternative group chat ID

# Initialize the GreenAPI object
greenAPI = GreenAPI(INSTANCE_ID, API_TOKEN)

# List of predefined birthday messages
messages = [
    "🎉 С Днем Рождения, Name! Желаю тебе потрясающего дня! Сегодня тебе исполнилось Age лет! 🎂",
    "🎈 Поздравляю с Днем Рождения, Name! Не могу поверить, что тебе уже Age! 🥳",
    "🎁 Пусть твой особенный день принесет тебе все, что желает твое сердце, Name! С Днем Рождения, Age-летний именинник! 🌟",
    "🎊 С Днем Рождения, Name! Желаю море радости и счастья в твой Age-й день рождения! 🎈",
    "🌟 Пусть все твои мечты сбудутся в этот особенный день, Name! С Днем Рождения! Age лет - прекрасный возраст! 🎉",
    "🥳 С Днем Рождения, Name! Пусть этот день будет наполнен радостью и улыбками! Age лет - это только начало! 🎂",
    "🎂 Поздравляю с Днем Рождения, Name! Желаю тебе много счастья, здоровья и успехов в твои Age лет! 🎈",
    "🎉 Желаю тебе незабываемого Дня Рождения, Name! Пусть каждый день будет таким же особенным, как твои Age лет сегодня! 🥳",
    "🌟 С Днем Рождения, Name! Пусть каждый момент твоей жизни будет полон счастья и радости! Age - замечательный возраст! 🎂",
    "🎈 Пусть твой Age-й День Рождения будет началом нового, удивительного года жизни, Name! С праздником! 🎉",
    "🥳 Поздравляю с Днем Рождения, Name! Пусть каждый твой день будет таким же ярким и радостным, как этот! Сегодня тебе Age! 🎁",
    "🎂 С Днем Рождения, Name! Желаю тебе море улыбок, счастья и любви! Сегодня тебе исполнилось Age лет! 🎉",
    # Add more messages as needed
]

# Load the birthday data
df = pd.read_excel('birthdays.xlsx')

# Get today's date
today = datetime.now().strftime("%d-%m")

# Flag to check if any birthday is today
birthday_today = False

# Iterate over the rows in the dataframe
for index, row in df.iterrows():
    # Extract the name and birthday
    name = row['Name']
    birthday = row['Date of birth']

    try:
        birthdate = datetime.strptime(birthday, "%d-%m-%Y")
        birthdate_str = birthdate.strftime("%d-%m")
    except ValueError as e:
        print(f"Error parsing date for {name}: {e}")
        continue

    # Check if today is the person's birthday
    if today == birthdate_str:
        birthday_today = True

        # Calculate the age
        age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))

        # Select a random message and replace the placeholder with the person's name and age
        message = random.choice(messages).replace("Name", name).replace("Age", str(age))

        # Send the message using Green API
        try:
            response = greenAPI.sending.sendMessage(GROUP_CHAT_ID, message)
            if response.code == 200:
                print(f"Sent message to {name} in group chat")
            else:
                print(f"Failed to send message to {name}: {response.data}")
        except Exception as e:
            print(f"Error sending message: {e}")

if not birthday_today:
    print("No birthdays today.")
