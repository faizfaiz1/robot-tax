require('dotenv').config();
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const BOT_TOKEN = process.env.BOT_TOKEN; // استخدم متغير بيئي بدلاً من وضع التوكن مباشرة

app.post('/update-username', async (req, res) => {
    const { userId, newUsername } = req.body;
    
    if (!userId || !newUsername) {
        return res.status(400).json({ error: 'Missing userId or newUsername' });
    }

    try {
        const response = await axios.patch(`https://discord.com/api/v10/users/@me`, 
        { username: newUsername }, 
        {
            headers: {
                Authorization: `Bot ${BOT_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });

        res.json({ message: 'تم تحديث الاسم بنجاح!', data: response.data });
    } catch (error) {
        res.status(500).json({ error: 'حدث خطأ أثناء التحديث', details: error.response.data });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
