# تعديل الاسم وتحديثه فورًا
@bot.command()
async def change_name(ctx, new_name: str):
    user_id = str(ctx.author.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['name'] = new_name
    save_user_data(user_data)
    await ctx.send(f'تم تغيير اسمك إلى {new_name} بنجاح!')

# نسخ لوحة البداية لحساب مبلغ الضريبة إلى اللوحة الأخيرة بعد الربط
async def show_final_panel(ctx):
    embed = discord.Embed(title="حساب الضريبة", description="قم بإدخال التفاصيل لحساب مبلغ الضريبة.", color=0x00ff00)
    embed.add_field(name="المبلغ الأساسي", value="...", inline=False)
    embed.add_field(name="نسبة الضريبة", value="...", inline=False)
    embed.add_field(name="المبلغ النهائي بعد الضريبة", value="...", inline=False)
    await ctx.send(embed=embed)

# منع إعادة الربط بعد الربط مرة واحدة
@bot.command()
async def link_account(ctx, account_id: str):
    user_id = str(ctx.author.id)
    user_data = load_user_data()
    
    if user_id in user_data and user_data[user_id].get('linked', False):
        await ctx.send("لقد قمت بربط حسابك مسبقًا ولا يمكنك إعادة ربطه!")
        return
    
    user_data[user_id] = {'linked': True, 'account_id': account_id}
    save_user_data(user_data)
    await ctx.send(f'تم ربط حسابك بنجاح!')

# تحميل وحفظ بيانات المستخدمين
def load_user_data():
    try:
        with open("user_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open("user_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
