import telebot
from telebot import types
import os
from flask import Flask, request


token = "7830729501:AAHHpnLxvTv2GUZEqVeCcFbUUNmJCtSV5h0"
bot = telebot.TeleBot(token)
app = Flask(__name__)

#Replace with your token

#Set path where your PDF files are located
path = os.path.join(os.getcwd(), 'requirements')
files_names =[
	      "Academic Forms.pdf",
     "Grading_System,_Administrative_Grades_and_Provisional_Grades_for.pdf",
	      "Leave of Absence.pdf",
	      "Requirements for Program Completion.pdf",
	      "Student Trips for PhD.pdf"
]

#Store message IDs that bot sends so we can delete them later
bot_messages =[]


#Start command handler
@ bot.message_handler(commands =['start'])
def start(message):
#Create the markup with buttons
	markup = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)

	btn1 = types.KeyboardButton("Academic Forms")
	btn2 = types.KeyboardButton("Grading System")
	btn3 = types.KeyboardButton("Leave of Absence")
	btn4 = types.KeyboardButton("Requirements for Program Completion")
	btn5 = types.KeyboardButton("Student Trips for PhD")

	#Add buttons to markup
	markup.add(btn1, btn2, btn3, btn4, btn5)

	#Send the welcome message with the menu
	msg = bot.send_message(message.chat.id,
				   '�168 Welcome to the SEDS Student Bot! Instantly discover answers to your topics of interest. Please check the menu to select a topic.',
				   reply_markup = markup)

	bot_messages.append(msg.message_id)


#Handle button press events
@ bot.message_handler(func = lambda message:True)
def on_click(message):
	#Handle each button press based on the button text
	if message.text == "Academic Forms":
		send_file_and_message(message, files_names[0],
				  "Please check the document for more info.")
	#Assuming the first file is "Academic Forms.pdf"

	elif message.text == "Grading System":
		send_file_and_message(message, files_names[1],
					  "This is the Grading System document.")
	#Assuming the second file is "Grading System.pdf"

	elif message.text == "Leave of Absence":
		send_file_and_message(message, files_names[2],
					  "Here is the Leave of Absence information.")
	#Assuming the third file is "Leave of Absence.pdf"

	elif message.text == "Requirements for Program Completion":
		send_file_and_message(message, files_names[3],
				   "Check out the requirements for program completion.")
	#Assuming the fourth file is "Requirements for Program Completion.pdf"

	elif message.text == "Student Trips for PhD":
		send_file_and_message(message, files_names[4],
				  "This is the document for Student Trips for PhD.")
	#Assuming the fifth file is "Student Trips for PhD.pdf"
	else:
		bot.send_message(message.chat.id, "Invalid option selected!")


#Function to send the file and text message in succession
def send_file_and_message(message, filename, info_text):
	try:
		file_path = os.path.join(path, filename)
		with open(file_path, "rb") as file:
	#Send the file
			msg_file = bot.send_document(message.chat.id, file)
			bot_messages.append(msg_file.message_id)

	#Send the additional info message immediately after sending the file
		msg_info = bot.send_message(message.chat.id, info_text)
		bot_messages.append(msg_info.message_id)

	except Exception as e:
		msg_error = bot.send_message(message.chat.id, f"Failed to send the file: {str(e)}")
		bot_messages.append(msg_error.message_id)


# Webhook route
@app.route(f'/{token}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200


# Start Flask app
if __name__ == "__main__":
    # Set webhook URL for Telegram (replace with your domain name)
    bot.remove_webhook()
    # bot.set_webhook(url="https://1234abcd.ngrok.io/" + token)

    # Start Flask server on host 0.0.0.0 and port 8000
    app.run(host="0.0.0.0", port=10000)
