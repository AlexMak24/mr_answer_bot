import asyncio
import sys
import telebot
from telebot import types
from g4f.client import Client

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
gpt_client = Client()

user_mode = {}

# Main menu with inline buttons
def generate_main_inline_buttons():
    markup = types.InlineKeyboardMarkup()
    btn_artist = types.InlineKeyboardButton("🎨 Artist", callback_data="set_mode_🎨 Artist")
    btn_programmer = types.InlineKeyboardButton("💻 Programmer", callback_data="set_mode_💻 Programmer")
    btn_writer = types.InlineKeyboardButton("✍️ Writer", callback_data="set_mode_✍️ Writer")
    btn_lawyer = types.InlineKeyboardButton("⚖️ Lawyer", callback_data="set_mode_⚖️ Lawyer")
    btn_businessman = types.InlineKeyboardButton("📈 Businessman", callback_data="set_mode_📈 Businessman")
    btn_info = types.InlineKeyboardButton("ℹ️ Info", callback_data="show_info")
    markup.add(btn_artist, btn_programmer)
    markup.add(btn_writer, btn_lawyer)
    markup.add(btn_businessman)
    markup.add(btn_info)
    return markup

# Reply keyboard with "Show Buttons"
def generate_reply_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_show = types.KeyboardButton("🏠 Show Buttons")
    markup.add(btn_show)
    return markup

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open("welcomephoto.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Hello and welcome to our bot! 🎉")

    welcome_text = (
        "Hello! I'm your personal assistant, here to help you in various fields. Whether you're a creative, a programmer, a writer, or a businessman, "
        "I can assist you with a wide range of tasks.\n\n"

        "Here’s what I can do for you:\n\n"

        "🎨 Artist Mode: Need an image? In this mode, you can describe anything you want to see, and I’ll generate a unique image based on your description. "
        "You can ask for different artistic styles, from classical paintings to modern digital art. The more details you provide, the better the image will be!\n\n"

        "💻 Programmer Mode: Stuck with some code or programming problem? I can help you debug your code, write new scripts, or even assist with algorithm solutions. "
        "Just let me know what you're working on, and I'll guide you through it!\n\n"

        "✍️ Writer Mode: Looking for help with writing? Whether it’s an article, a story, or a full-length novel, I can help you brainstorm ideas, structure your writing, "
        "or even generate text based on your ideas. If you're stuck, just ask for my assistance!\n\n"

        "⚖️ Lawyer Mode: Need legal advice or help understanding laws? I can answer your legal questions, assist with document creation, and explain complex legal topics in simple terms. "
        "Feel free to ask about anything related to law, and I'll do my best to provide accurate information.\n\n"

        "📈 Businessman Mode: Thinking about growing your business or starting a new project? In this mode, I’ll assist you with market research, business planning, and even help you strategize for success. "
        "Let’s talk about your goals and explore ideas to grow your business.\n\n"

        "All you need to do is choose the mode that fits your needs, and I’ll guide you from there. You can easily switch between modes anytime!\n\n"

        "To get started, simply choose a mode, and let's begin our journey together! 🌟"
    )

    bot.send_message(message.chat.id, welcome_text, reply_markup=generate_main_inline_buttons())

# Show main inline buttons when "Show Buttons" is pressed
@bot.message_handler(func=lambda message: message.text == "🏠 Show Buttons")
def show_main_buttons(message):
    bot.send_message(message.chat.id, "Choose a mode to start:", reply_markup=generate_main_inline_buttons())

# Inline button mode selection handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("set_mode_"))
def set_mode(call):
    chat_id = call.message.chat.id
    mode = call.data.replace("set_mode_", "")
    user_mode[chat_id] = mode
    bot.send_message(chat_id, f"Mode {mode} activated.")
    bot.edit_message_reply_markup(chat_id, call.message.message_id)

# Info button handler

# Info button handler
@bot.callback_query_handler(func=lambda call: call.data == "show_info")
def show_info(call):
    chat_id = call.message.chat.id
    info_text = (
        "Hello! This is a bot designed to assist you in various fields, offering a wide range of tools and features to make your tasks easier.\n\n"
        "Here are the available modes you can choose from:\n\n"

        "🎨 **Artist Mode**: In this mode, I will help you create unique images based on your descriptions. Simply describe what you'd like to see, and I will generate an image that fits your vision. Whether you need a classic painting or modern digital art, I can handle it! The more detailed your description, the better the result. Start creating art now!\n\n"

        "💻 **Programmer Mode**: Stuck with some code or need help with a programming task? In this mode, I will assist you in writing code, debugging issues, solving programming challenges, and improving your code. Whether you're working on algorithms or fixing bugs, I can help! Just share your problem or code, and I'll guide you through the solution.\n\n"

        "✍️ **Writer Mode**: Need help with writing? This mode is perfect for creating texts, articles, stories, essays, or even books. I can assist you in structuring your writing, generating ideas, or producing content based on your input. Whether you're a novice writer or a seasoned author, I can help bring your words to life. Tell me what you'd like to write, and I'll help you get started!\n\n"

        "⚖️ **Lawyer Mode**: Have legal questions or need legal advice? This mode is designed to assist you with understanding laws, answering legal queries, and providing guidance on legal matters. I can help explain complex legal concepts, assist with document creation, and give general legal advice. If you have any legal doubts, feel free to ask, and I'll do my best to help!\n\n"

        "📈 **Businessman Mode**: Are you an entrepreneur or a business owner? In this mode, I’ll assist you with market analysis, business planning, growth strategies, and investment advice. Whether you’re starting a new business or looking to optimize your current operations, I can offer valuable insights and suggestions. Let's discuss your business goals and explore ways to achieve success!\n\n"

        "To get started, simply choose a mode that suits your needs. You can switch between modes at any time! Feel free to explore and make the most of the bot's capabilities!"
    )
    bot.send_message(chat_id, info_text)


# Generate images for "Artist" mode
def generate_image(prompt):
    try:
        response = gpt_client.images.generate(model="flux", prompt=prompt, response_format="url")
        return response.data[0].url
    except Exception:
        return None

# Text message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    mode = user_mode.get(chat_id, "💻 Programmer")
    if mode == "🎨 Artist":
        image_url = generate_image(message.text)
        if image_url:
            bot.send_photo(chat_id, image_url, caption="Here is your image 🎨")
        else:
            bot.send_message(chat_id, "Failed to generate the image. Please try again later.")
    else:
        try:
            response = gpt_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message.text}],
                web_search=False
            )
            answer = response.choices[0].message.content
            bot.reply_to(message, answer)
        except Exception:
            bot.reply_to(message, "An error occurred, please try again later.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
