import discord
import random
import sqlite3
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings

CURRENCY_NAME = 'fish'
CURRENCY_IMG = '🐟'
STARTING_VALUE = 500

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = "Admins Only: Change a user's balance")
    @commands.has_role('GOD')
    async def set_balance(self, ctx, amount : int, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # check if user already has an account
        cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
        account = cursor.fetchone()[0]
        if account < 1:
            if member == ctx.author:
                msg = "You don't have an account!"
            else:
                msg = f"{member.name} doesn't have an account!"
        else:
            # set funds
            cursor.execute(f'UPDATE economy SET currency = {amount} WHERE member_id = {member.id}')
            db.commit()
            if member == ctx.author:
                msg = f'Your Balance: {amount} {CURRENCY_NAME}'
            else:
                msg = f"{member.name}'s Balance: {amount} {CURRENCY_NAME}"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Make yourself a bank account to keep your {CURRENCY_NAME}. Admins can add an optional member.')
    async def make_account(self, ctx, member : discord.Member = None):
        # check member
        run = True
        if member == None:
            member = ctx.author
        elif not ('GOD' in [role.name for role in ctx.author.roles]):
            run = False
            msg = "You don't have permission to make bank accounts for others! <:Asami:610590675142049868>"
        if run:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user already has an account
            cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = cursor.fetchone()[0]
            if account >= 1:
                if member == ctx.author:
                    msg = 'You already have an account!'
                else:
                    msg = f'{member.name} already has an account!'
            else:
                # make an account
                cursor.execute('''
                INSERT INTO economy(member_id, currency)
                VALUES(?, ?)''', (member.id, STARTING_VALUE))
                db.commit()
                if member == ctx.author:
                    msg = f"Your account has been registered, here's {STARTING_VALUE} {CURRENCY_NAME} to get you started! <:Asami:610590675142049868>"
                else:
                    msg = f"{member.name}'s account has been registered.\nBalance: {STARTING_VALUE} {CURRENCY_NAME}"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Admins Only: Deletes an account and all of its {CURRENCY_NAME}')
    async def delete_account(self, ctx, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        if 'GOD' in [role.name for role in ctx.author.roles]:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user has an account
            cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = cursor.fetchone()[0]
            if account < 1:
                if member == ctx.author:
                    msg = "You don't have an account! Use ``.make_account`` to make one."
                else:
                    msg = f"{member.name} doesn't have an account!"
            else:
                if member == ctx.author:
                    msg = 'Your account has been deleted.'
                else:
                    msg = f"{member.name}'s account has been deleted."
                # delete account
                cursor.execute(f'DELETE FROM economy WHERE member_id = {member.id}')
                db.commit()
        else:
            msg = "You don't have permission to delete bank accounts! <:Asami:610590675142049868>"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'see how many {CURRENCY_NAME} you or someone else have')
    async def check_balance(self, ctx, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # get user account
        cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
        account = cursor.fetchone()
        if str(type(account)) == "<class 'NoneType'>":
            if member.id == ctx.author.id:
                msg = "You don't have an account! Use ``.make_account`` to make one."
            else:
                msg = f"{member.name} doesn't have an account!"
        else:
            currency = account[0]
            if member.id == ctx.author.id:
                msg = f'You have {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            else:
                msg = f'{member.name} has {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = 'Honest Bank', author = user,
        avatar = avatar, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)

        
    @commands.command(description = f'give some {CURRENCY_NAME}')
    async def transfer(self, ctx, member : discord.Member, amount : int):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        msg = ''
        # check if amount is valid
        if amount <= 0:
            msg = 'Amount transferred must be > 0'
        else:
            # check if member is valid
            if member.id == ctx.author.id:
                msg = "You can't transfer funds to yourself"
            else:
                # get sender account
                cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
                account = cursor.fetchone()
                if str(type(account)) == "<class 'NoneType'>":
                    if msg == '':
                        msg = "You don't have an account! Use ``.make_account`` to make one"
                else:
                    currency_sender = account[0]
                    if amount > currency_sender:
                        if msg == '':
                            msg = 'You have insufficient funds!'
                    else:
                        # get recipient account
                        cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
                        account = cursor.fetchone()
                        if str(type(account)) == "<class 'NoneType'>":
                            if msg == '':
                                msg = f"{member.name} doesn't have an account!"
                        else:
                            currency_recipient = account[0]
                            # decrease sender account by amount to transfer
                            cursor.execute(f'UPDATE economy SET currency = {currency_sender - amount} WHERE member_id = {ctx.author.id}')
                            # increase recipient account by amount to transfer
                            cursor.execute(f'UPDATE economy SET currency = {currency_recipient + amount} WHERE member_id = {member.id}')
                            db.commit()
                            msg = f"Transfer complete!\nYour Balance: {currency_sender - amount} {CURRENCY_NAME}\n{member.name}'s Balance: {currency_recipient + amount} {CURRENCY_NAME}"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'Returns top ten richest toucans')
    async def leaderboard(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # sort by currency
        cursor.execute(f'SELECT member_id, currency FROM economy ORDER BY currency DESC')
        # fetch data
        rows = cursor.fetchall()
        place = 1
        row_index = 0
        # top 10
        eObj = await embed(ctx, title = f'{CURRENCY_IMG} Honest Bank Leaderboard {CURRENCY_IMG}')
        while place <= 10 and row_index < len(rows):
            # try in case member wasn't found
            try:
                member = ctx.guild.get_member(rows[row_index][0])
                eObj.add_field(name = f'{place}. {member.name}#{member.discriminator}', value = f'```{rows[row_index][1]} {CURRENCY_NAME.capitalize()}```', inline = True)
                place += 1
            except:
                pass
            row_index += 1
        # send user message
        if eObj is not False:
            await ctx.send(embed = eObj)
            

def setup(bot):
    bot.add_cog(Economy(bot))