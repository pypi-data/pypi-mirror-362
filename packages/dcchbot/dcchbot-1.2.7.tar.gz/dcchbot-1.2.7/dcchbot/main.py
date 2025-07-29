# v1.0.0

def run():
    import discord
    from discord.ext import commands
    from discord import app_commands
    from datetime import timedelta

    intents = discord.Intents.all()
    intents.guilds = True
    intents.members = True
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    OWNER_ID = 1317800611441283139  # 不要加引號！

    def is_admin(interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.administrator

    @bot.event
    async def on_ready():
        await bot.wait_until_ready()
        try:
            synced = await bot.tree.sync()
            print(f"已同步 {len(synced)} 個 slash 指令")
        except Exception as e:
            print(f"同步 slash 指令失敗：{e}")
        print(f'機器人上線：{bot.user}')

    @bot.tree.command(name="hello", description="跟你說哈囉")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"哈囉 {interaction.user.mention}")

    @bot.tree.command(name="ping", description="顯示延遲")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"延遲：{round(bot.latency * 1000)}ms")

    @bot.tree.command(name="say", description="讓機器人說話")
    @app_commands.describe(message="你想說的話")
    async def say(interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @bot.tree.command(name="ban", description="封鎖使用者（限管理員）")
    @app_commands.describe(member="要封鎖的使用者", reason="封鎖原因")
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "未提供原因"):
        if not is_admin(interaction):
            return await interaction.response.send_message("你沒有權限執行此指令。", ephemeral=True)
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.mention} 已被封鎖。原因：{reason}")
        except discord.Forbidden:
            await interaction.response.send_message("無法封鎖對方，可能因為權限不足或目標層級過高。", ephemeral=True)

    @bot.tree.command(name="kick", description="踢出使用者（限管理員）")
    @app_commands.describe(member="要踢出的使用者", reason="踢出原因")
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "未提供原因"):
        if not is_admin(interaction):
            return await interaction.response.send_message("你沒有權限執行此指令。", ephemeral=True)
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.mention} 已被踢出。原因：{reason}")
        except discord.Forbidden:
            await interaction.response.send_message("無法踢出對方，可能因為權限不足或目標層級過高。", ephemeral=True)

    @bot.tree.command(name="timeout", description="暫時禁言使用者（限管理員）")
    @app_commands.describe(member="要禁言的使用者", seconds="禁言秒數", reason="禁言原因")
    async def timeout(interaction: discord.Interaction, member: discord.Member, seconds: int, reason: str = "未提供原因"):
        if not is_admin(interaction):
            return await interaction.response.send_message("你沒有權限執行此指令。", ephemeral=True)
        try:
            await member.timeout_for(timedelta(seconds=seconds), reason=reason)
            await interaction.response.send_message(f"{member.mention} 已被禁言 {seconds} 秒。原因：{reason}")
        except Exception as e:
            await interaction.response.send_message(f"無法禁言：{e}")

    @bot.tree.command(name="warn", description="警告使用者（限管理員）")
    @app_commands.describe(member="要警告的使用者", reason="警告原因")
    async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "未提供原因"):
        if not is_admin(interaction):
            return await interaction.response.send_message("你沒有權限執行此指令。", ephemeral=True)
        await interaction.response.send_message(f"{member.mention} 已被警告。原因：{reason}")
        try:
            await member.send(f"你在伺服器 {interaction.guild.name} 被警告：{reason}")
        except:
            await interaction.followup.send("無法傳送私人訊息給該用戶。")

    class ModerationView(discord.ui.View):
        def __init__(self, member: discord.Member, author: discord.Member):
            super().__init__(timeout=60)
            self.member = member
            self.author = author

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            return interaction.user.id == self.author.id

        @discord.ui.button(label="警告", style=discord.ButtonStyle.secondary)
        async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                await self.member.send(f"你在伺服器 {interaction.guild.name} 被警告。請注意言行。")
            except:
                pass
            await interaction.response.send_message(f"{self.member.mention} 已被警告。", ephemeral=True)

        @discord.ui.button(label="禁言 60 秒", style=discord.ButtonStyle.primary)
        async def timeout_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                await self.member.timeout_for(timedelta(seconds=60), reason="由管理員 GUI 操作禁言")
                await interaction.response.send_message(f"{self.member.mention} 已被禁言 60 秒。", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"禁言失敗：{e}", ephemeral=True)

        @discord.ui.button(label="踢出", style=discord.ButtonStyle.danger)
        async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                await self.member.kick(reason="由管理員 GUI 操作踢出")
                await interaction.response.send_message(f"{self.member.mention} 已被踢出。", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"踢出失敗：{e}", ephemeral=True)

        @discord.ui.button(label="封鎖", style=discord.ButtonStyle.danger)
        async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                await self.member.ban(reason="由管理員 GUI 操作封鎖")
                await interaction.response.send_message(f"{self.member.mention} 已被封鎖。", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"封鎖失敗：{e}", ephemeral=True)

    @bot.tree.command(name="moderate", description="打開管理 GUI 面板")
    @app_commands.describe(member="要管理的對象")
    async def moderate(interaction: discord.Interaction, member: discord.Member):
        if not is_admin(interaction):
            return await interaction.response.send_message("你沒有權限使用此指令。", ephemeral=True)
        view = ModerationView(member, interaction.user)
        await interaction.response.send_message(
            f"請選擇對 {member.mention} 的操作：", 
            view=view,
            ephemeral=True
        )

    @bot.tree.command(name="stop", description="關閉機器人（限擁有者）")
    async def stop(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("只有擁有者可以使用此指令。", ephemeral=True)
        await interaction.response.send_message("機器人即將關閉。")
        await bot.close()

    # 🔐 請使用者輸入 Token
    token = input("請輸入你的 Discord Bot Token：\n> ").strip()
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("Token 無效，請重新確認。")
    except Exception as e:
        print(f"發生錯誤：{e}")