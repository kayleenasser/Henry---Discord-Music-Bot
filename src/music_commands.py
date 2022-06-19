import henry

# Music Commands
# ---------------------------------------
# Play now ahead of queue
@henry.client.command(aliases=['pn'])
async def play(ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Join a VC first silly!")
    else:
        song = henry.yt_search(query)
        if type(song) == type(True):
            await ctx.send("Could not download song.")
        else:
            await ctx.send("Playing song! ٩(˘◡˘)۶")
            henry.queue_list.insert(0, [song, voice_channel])
            print(henry.queue_list)
            ctx.voice_client.stop()

            if henry.is_playing == False:
                await henry.play_music(ctx.voice_client)

            # Queue Stuff


# --------------------------------
# Adds to queue
@henry.client.command(aliases=['q', 'p'])
async def queue(ctx, *args):
    query = " ".join(args)
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Join a VC first silly!")
    else:
        song = henry.yt_search(query)
        if type(song) == type(True):
            await ctx.send("Could not download song.")
        else:
            await ctx.send("Added to queue! ٩(˘◡˘)۶")
            henry.queue_list.append([song, voice_channel])

            if not henry.is_playing:
                await henry.play_music(ctx.voice_client)


# Remove from Queue
@henry.client.command(aliases=['rmv'])
async def remove(ctx, number):
    try:
        del (henry.queue_list[int(number) - 1])
        if len(henry.queue_list) == 0:
            await ctx.send("Your queue is empty. (╥﹏╥)")
        else:
            return_val = ""
            num = 1
            if len(henry.queue_list) > 0:
                for i in range(0, len(henry.queue_list)):
                    return_val = str(
                        num) + ". " + henry.queue_list[i][0]['title'] + "\n"
                    print(return_val)
                    if return_val != "":
                        await ctx.send(return_val)
                        num = num + 1
    except:
        await ctx.send("Your queue is empty or out of range. (╥﹏╥)")


# Clear Queue
@henry.client.command(aliases=['c'])
async def clear(ctx):
    if len(henry.queue_list) > 0:
        henry.queue_list.clear()
        if len(henry.queue_list) == 0:
            await ctx.send("Queue cleared! ( ˘︹˘ )")
    else:
        await ctx.send("Your queue is already empty! (╥﹏╥)")


# View queue
@henry.client.command(aliases=['v'])
async def view(ctx):
    returnval = ""
    num = 1
    if len(henry.queue_list) > 0:
        for i in range(0, len(henry.queue_list)):
            returnval = str(num) + ". " + henry.queue_list[i][0]['title'] + "\n"
            print(returnval)
            if returnval != "":
                await ctx.send(returnval)
                num = num + 1
    else:
        await ctx.send("Your queue is empty. (╥﹏╥)")


# Skip from queue
@henry.client.command(aliases=['sk'])
async def skip(ctx):
    ctx.voice_client.stop()
    await ctx.send("Skipped :)")
    await henry.play_music(ctx.voice_client)


# Live Music Controls
# --------------------------------------------

# Pause
@henry.client.command(pass_context=True, aliases=['ps'])
async def pause(ctx):
    await ctx.send("Paused music (ง︡'-'︠)ง")
    await ctx.voice_client.pause()  # Pause the VC music


# Stop
@henry.client.command(pass_context=True, aliases=['s'])  # Stop music
async def stop(ctx):
    await ctx.send("Stopped music ( ͡• ͜ʖ ͡•)")
    await ctx.voice_client.stop()  # Stop the VC music


# Resume
@henry.client.command(pass_context=True, aliases=['r'])  # Resume music
async def resume(ctx):
    await ctx.send("Resumed music ( •̀ ω •́ )✧")
    await ctx.voice_client.resume()  # Resume the VC music
