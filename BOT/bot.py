from aiogram import Bot, Dispatcher, executor, types
import os
from flask import Flask, request, Response

from keep_alive import keep_alive
keep_alive()


# Flask app for webhook support
app = Flask(__name__)

# Set your bot token here
token = "7503779929:AAHY66GntTltbDBY4Er5vVugLykhBAe3sWs"
bot = Bot(token=token)
dp = Dispatcher(bot)

# Set path where your PDF files are located
path = os.path.join(os.getcwd(), 'requirements')
files_names = [
    "Academic Forms.pdf",
    "Grading_System,_Administrative_Grades_and_Provisional_Grades_for.pdf",
    "Leave of Absence.pdf",
    "Requirements for Program Completion.pdf",
    "Student Trips for PhD.pdf"
]


# Command handler for /start and /help
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    # Create the markup with buttons
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = types.KeyboardButton("Academic Forms")
    btn2 = types.KeyboardButton("Grading System")
    btn3 = types.KeyboardButton("Leave of Absence")
    btn4 = types.KeyboardButton("Requirements for Program Completion")
    btn5 = types.KeyboardButton("Student Trips for PhD")

    # Add buttons to markup
    markup.add(btn1, btn2, btn3, btn4, btn5)

    await message.reply(
        '🚀 Welcome to the SEDS Student Bot! Instantly discover answers to your topics of interest. Please check the menu to select a topic.',
        reply_markup=markup)


# Handle button press events
@dp.message_handler(lambda message: message.text in [
    "Academic Forms", "Grading System", "Leave of Absence", "Requirements for Program Completion",
    "Student Trips for PhD"])
async def send_document(message: types.Message):
    # Handle each button press based on the button text
    if message.text == "Academic Forms":
        await send_file_and_message(message, files_names[0], "Please check the document for more info.")
    elif message.text == "Grading System":
        await send_file_and_message(message, files_names[1], "This is the Grading System document.")
    elif message.text == "Leave of Absence":
        await send_file_and_message(message, files_names[2], "Here is the Leave of Absence information.")
    elif message.text == "Requirements for Program Completion":
        await send_file_and_message(message, files_names[3], "Check out the requirements for program completion.")
    elif message.text == "Student Trips for PhD":
        await send_file_and_message(message, files_names[4], "This is the document for Student Trips for PhD.")
    else:
        await message.reply("Invalid option selected!")


# Function to send the file and a text message
async def send_file_and_message(message: types.Message, filename: str, info_text: str):
    try:
        file_path = os.path.join(path, filename)
        with open(file_path, "rb") as file:
            # Send the file
            await message.answer_document(file)

        # Send additional info message immediately after sending the file
        await message.reply(info_text)
    except Exception as e:
        await message.reply(f"Failed to send the file: {str(e)}")


# Webhook route for handling updates from Telegram
@app.route(f"/{token}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = types.Update.de_json(json_str)
    dp.process_update(update)
    return Response('ok', status=200)


if __name__ == "__main__":
    # Use polling or webhooks depending on your setup

    # If you're using polling (good for development), uncomment this:
    # executor.start_polling(dp)

    # If you're using webhooks with Flask (good for production), uncomment this:
    # bot.set_webhook(url="https://<your-ngrok-url>.ngrok-free.app/" + token)  # Replace with your actual ngrok URL
    # app.run(host="0.0.0.0", port=10000)
    executor.start_polling(dp)

