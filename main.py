import discord
import chess
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

prefix = '$'


board = chess.Board()
def reset():
    board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

in_game_players = {}
request = False
#requestee = ''
#requester = ''

turn = [0]

black = 0
white = 0

@client.event
async def on_ready():
    print(f'{client.user} is up and runnin')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'test':
        embedVar = discord.Embed(title="test", color=0xccccff)
        embedVar.add_field(name='test', value='```apache\ntest```', inline=False)
        await message.channel.send(embed=embedVar)

    if len(message.mentions) > 0 and message.mentions[0].id == 835648004820041809 and message.author.id == 536652716219432960:
        await message.channel.send('ilyt')
    
    if len(message.mentions) > 0 and message.mentions[0].id == 835648004820041809 and message.author.id == 542033277163274260:
        await message.channel.send('cock and ball man go do work')

    if message.content == 'quit':
        await message.channel.send('Killing bot')
        quit()

    if message.content[:len(prefix) + len('challenge')] == prefix + 'challenge':
        if len(message.mentions) < 1:
            await message.channel.send('Ping someone to challenge them')
        elif str(message.mentions[0].id) == str(message.author.id):
            await message.channel.send('You can\'t challenge yourself what')
        elif str(message.mentions[0].id) in in_game_players or str(message.author.id) in in_game_players:
            await message.channel.send('Player already in a game, request later')
        else:
            in_game_players[str(message.author.id)] = 'requester'
            in_game_players[str(message.mentions[0].id)] = 'requestee'
            requestee = str(message.mentions[0].id)
            requester = str(message.author.id)
            await message.channel.send(f'<@{message.author.id}> challenged <@{message.mentions[0].id}> to a chess match, do you accept?')

    if str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'requestee' and message.content == 'no' or message.content == 'n':
        in_game_players[str(message.author.id)] = ''
        requestee = ''
        await message.channel.send('Request denied')
    
    if str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'requestee' and message.content == 'yes' or message.content == 'y':
        requester = ''
        for key, value in in_game_players.items():
            if value == 'requester':
                requester = key

        requestee = ''
        for key, value in in_game_players.items():
            if value == 'requestee':
                requestee = key

        basic_board = ''.join(['  ' if i == ' ' and n > 343 else i for n, i in enumerate(board.unicode(borders=True))])
        clean_board = basic_board.replace('-----------------','-----------------------',9)
        embedVar = discord.Embed(title='Chess Match',description=f'<@{requester}> v <@{requestee}>\nWhite\'s turn',color=0xCCCCFF)
        embedVar.add_field(name='Board',value=f'```{clean_board}```')

        in_game_players[str(message.author.id)] = 'white'
        in_game_players[requester] = 'black'
        requester = ''
        requestee = ''
        await message.channel.send(embed=embedVar)

    if str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'white' and turn[0] == 0 and message.content[len(prefix)-1] == prefix:
        white = ''
        for key, value in in_game_players.items():
            if value == 'white':
                white = key

        black = ''
        for key, value in in_game_players.items():
            if value == 'black':
                black = key

        if message.content[len(prefix):len(prefix) + len('move')] == 'move':
            try: 
                chess.Move.from_uci(message.content[len(prefix)+len('move')+1:])
                if chess.Move.from_uci(message.content[len(prefix)+len('move')+1:]) in board.legal_moves:
                    board.push(chess.Move.from_uci(message.content[len(prefix)+len('move')+1:]))
                    basic_board = ''.join(['  ' if i == ' ' and n > 343 else i for n, i in enumerate(board.unicode(borders=True))])
                    clean_board = basic_board.replace('-----------------','-----------------------',9)
                    if board.is_checkmate():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nWhite wins',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        turn[0] = -1
                        await message.channel.send(embed=embedVar)
                        reset()
                    elif board.is_stalemate():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.is_insufficient_material():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.can_claim_threefold_repetition():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.can_claim_fifty_moves():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    else:
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nBlack\'s turn',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = 1
                else:
                    await message.channel.send('Invalid move, try again')
            except:
                await message.channel.send('Invalid move, try again')
        
        if message.content[len(prefix):len(prefix) + len('resign')] == 'resign':
            await message.channel.send(f'White resigns, <@{black}> wins')
            turn[0] = -1
            reset()

    elif str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'black' and turn[0] == 0 and message.content[len(prefix)-1] == prefix:
        if message.content[len(prefix):len(prefix) + len('resign')] == 'resign':
            white = ''
            for key, value in in_game_players.items():
                if value == 'white':
                    white = key

            black = ''
            for key, value in in_game_players.items():
                if value == 'black':
                    black = key
        
            await message.channel.send(f'Black resigns, <@{white}> wins')
            turn[0] = -1
            reset()
            
    if str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'black' and turn[0] == 1 and message.content[len(prefix)-1] == prefix:
        white = ''
        for key, value in in_game_players.items():
            if value == 'white':
                white = key

        black = ''
        for key, value in in_game_players.items():
            if value == 'black':
                black = key

        if message.content[len(prefix):len(prefix) + len('move')] == 'move':
            try:
                chess.Move.from_uci(message.content[len(prefix)+len('move')+1:])
                if chess.Move.from_uci(message.content[len(prefix)+len('move')+1:]) in board.legal_moves:
                    board.push(chess.Move.from_uci(message.content[len(prefix)+len('move')+1:]))
                    basic_board = ''.join(['  ' if i == ' ' and n > 343 else i for n, i in enumerate(board.unicode(borders=True))])
                    clean_board = basic_board.replace('-----------------','-----------------------',9)
                    if board.is_checkmate():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\Black wins',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        turn[0] = -1
                        await message.channel.send(embed=embedVar)
                        reset()
                    elif board.is_stalemate():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.is_insufficient_material():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.can_claim_threefold_repetition():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    elif board.can_claim_fifty_moves():
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>\nStalemate',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = -1
                        reset()
                    else:
                        embedVar = discord.Embed(title='Chess Match',description=f'<@{white}> v <@{black}>White\'s turn',color=0xCCCCFF)
                        embedVar.add_field(name='Board',value=f'```{clean_board}```')
                        await message.channel.send(embed=embedVar)
                        turn[0] = 0
                else:
                    await message.channel.send('Invalid move, try again')
            except:
                await message.channel.send('Invalid move, try again')
        
        if message.content[len(prefix):len(prefix) + len('resign')] == 'resign':
            await message.channel.send(f'Black resigns, <@{white}> wins')
            turn[0] = -1
            reset()

    elif str(message.author.id) in in_game_players and in_game_players[str(message.author.id)] == 'white' and turn[0] == 1 and message.content[len(prefix)-1] == prefix:
        if message.content[len(prefix):len(prefix) + len('resign')] == 'resign':
            white = ''
            for key, value in in_game_players.items():
                if value == 'white':
                    white = key

            black = ''
            for key, value in in_game_players.items():
                if value == 'black':
                    black = key
            
            await message.channel.send(f'White resigns, <@{black}> wins')
            turn[0] = -1
            reset()

    if message.content == 'players':
        await message.channel.send(in_game_players)

client.run(token)