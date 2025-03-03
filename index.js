const { Client, GatewayIntentBits, SlashCommandBuilder, REST, Routes } = require('discord.js');
require('dotenv').config(); // استدعاء المتغيرات البيئية من Vercel

const TOKEN = process.env.BOT_TOKEN;
const CLIENT_ID = process.env.CLIENT_ID; // معرف البوت
const GUILD_ID = process.env.GUILD_ID; // معرف السيرفر

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages]
});

// ✅ أمر سلاش لتغيير الاسم
const commands = [
    new SlashCommandBuilder()
        .setName('change_name')
        .setDescription('يغير اسم البوت')
        .addStringOption(option =>
            option.setName('newname')
                .setDescription('الاسم الجديد')
                .setRequired(true))
].map(command => command.toJSON());

// ✅ تسجيل الأوامر عند تشغيل البوت
const rest = new REST({ version: '10' }).setToken(TOKEN);
async function registerCommands() {
    try {
        await rest.put(Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID), { body: commands });
        console.log('✅ تم تسجيل أوامر السلاش!');
    } catch (error) {
        console.error('❌ خطأ في تسجيل الأوامر:', error);
    }
}

// ✅ عندما يصبح البوت جاهزًا
client.once('ready', () => {
    console.log(`✅ البوت شغال كـ ${client.user.tag}`);
    registerCommands();
});

// ✅ تنفيذ الأمر
client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    if (interaction.commandName === 'change_name') {
        const newName = interaction.options.getString('newname');

        try {
            await client.user.setUsername(newName);
            await interaction.reply(`✅ تم تغيير اسم البوت إلى: **${newName}**`);
        } catch (error) {
            console.error('❌ خطأ أثناء تغيير الاسم:', error);
            await interaction.reply('❌ حدث خطأ أثناء محاولة تغيير الاسم!');
        }
    }
});

// ✅ تسجيل الدخول
client.login(TOKEN);
