const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

async function getBridgeStatus() {
    try {
        const response = await axios.get('https://canalstatus.com/api/bridges');
        const bridges = response.data;

        const now = new Date();
        const hour = now.getHours().toString().padStart(2, '0');
        const minute = now.getMinutes().toString().padStart(2, '0');

        let message = `⛩️ وضعیت پل‌ها
🕙 ${hour}:${minute}

`;

        for (const bridge of bridges) {
            let emoji = bridge.status === "open" ? "🟢" :
                        bridge.status === "closed" ? "🔴" : "🟡";
            message += `${emoji} ${bridge.name}
`;
        }

        return message;
    } catch (error) {
        return '❌ خطا در دریافت اطلاعات پل‌ها';
    }
}

bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    const status = await getBridgeStatus();
    bot.sendMessage(chatId, status);
});