export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { name, phone, location, package: pkg } = req.body;

    const botToken = "8785423339:AAFa1z7mfHn2uAHRhJGarioyiciSwYpqrxQ";
    const chatId = "2055556738";

    const message = `🔔 طلب اشتراك جديد عبر الموقع:\n\n` +
                    `👤 الاسم: ${name}\n` +
                    `📞 الهاتف: ${phone}\n` +
                    `📍 المنطقة: ${location}\n` +
                    `📦 الباقة: ${pkg}`;

    try {
        const telegramUrl = `https://api.telegram.org/bot${botToken}/sendMessage`;
        const response = await fetch(telegramUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: message })
        });

        const data = await response.json();

        if (data.ok) {
            return res.status(200).json({ success: true });
        } else {
            return res.status(500).json({ error: 'Telegram API error', details: data });
        }
    } catch (error) {
        return res.status(500).json({ error: 'Server error' });
    }
}
