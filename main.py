"""Telegram Booking Bot for Beauty Salons & Restaurants

Professional booking assistant with AI scheduling capabilities.
"""

import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')


class BookingBot:
    """Main booking bot class handling all operations."""
    
    def __init__(self):
        """Initialize booking bot."""
        self.bookings = {}
        self.services = {
            'haircut': {'name': 'Haircut', 'duration': 30, 'price': 20},
            'massage': {'name': 'Massage', 'duration': 60, 'price': 50},
            'manicure': {'name': 'Manicure', 'duration': 45, 'price': 25}
        }
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command handler."""
        keyboard = [
            [InlineKeyboardButton("Book Service", callback_data='book')],
            [InlineKeyboardButton("View Bookings", callback_data='view')],
            [InlineKeyboardButton("Cancel Booking", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            'Welcome to Booking Bot! Select an option:',
            reply_markup=reply_markup
        )
    
    async def book_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle service booking."""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton(service['name'], callback_data=f"service_{key}")]
            for key, service in self.services.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="Select a service:",
            reply_markup=reply_markup
        )
    
    async def confirm_booking(self, user_id: int, service_key: str) -> str:
        """Confirm and save booking."""
        service = self.services[service_key]
        booking_time = datetime.now() + timedelta(hours=1)
        
        booking_id = f"{user_id}_{int(booking_time.timestamp())}"
        self.bookings[booking_id] = {
            'service': service_key,
            'time': booking_time,
            'user_id': user_id
        }
        
        return f"Booking confirmed for {service['name']} at {booking_time.strftime('%Y-%m-%d %H:%M')}"


async def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    bot = BookingBot()
    
    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(CallbackQueryHandler(bot.book_service, pattern='^book$'))
    
    await application.run_polling()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
