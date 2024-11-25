import asyncio
from create_bot import bot, dp, scheduler
from handlers.command import command_router
from handlers.common import common_router
import logging

# from work_time.time_func import send_time_msg


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(command_router, common_router)
    await bot.delete_webhook(drop_pending_updates=True)
    logging.getLogger().info("Start pooling.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
