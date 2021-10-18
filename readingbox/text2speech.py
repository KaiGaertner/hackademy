def tts_create(sounds_path, ID='TEST',text=''):
    sounds = []
    # split text into chunks and create sound files
    block_list = text.split("\n\n")
    for idx, block in enumerate(block_list):
        current_block = block.trim()
        if len(current_block) > 5: # current_block contains words
            os.system('''pico2wave -l de-DE -w {}{}_{}.wav "{}"'''.format(sounds_path, ID, f'{idx:03d}', current_block))
            soundfile = sounds_path+ID+'_'+f'{idx:03d}'+'.wav'
            try: # check soundfile and add if not error prone
                pygame.mixer.music.load(soundfile)
                sounds.append(soundfile)
                pygame.mixer.music.unload()
                print("["+f'{idx:03d}'+".wav] " + current_block) # for debugging purposes
                print('---') # for debugging purposes
            except pygame.error:
                continue
    return sounds
