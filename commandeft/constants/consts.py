import os


class Models:
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-1106-preview"

    @classmethod
    def get_models_list(cls):
        return [cls.GPT_3_5_TURBO, cls.GPT_4, cls.GPT_4_TURBO]


class MaxTokens:
    GPT_3_5_TURBO = 4096
    GPT_4 = 8192
    GPT_4_TURBO = 4096


class Decision:
    EXIT = "exit"
    CONTINUE = "continue"
    ACTION = "action"


class Mode:
    INTERACTIVE = "interactive"
    INLINE = "inline"


class AcceptCommandBehavior:
    RUN = "run"
    COPY = "copy"


MODE = "mode"
MODEL = "model"
EXIT = "exit"

CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".commandeft", "config")

init_messages = [
    "What mischief are we up to now?\n Describe the command you're concocting:\n",
    "Oh no, caught in another coding conundrum?\n Share the details:\n",
    "Here to save the day!\n Enlighten me with the command you're grappling with:\n",
    "When your coding journey hits a snag,\n Describe the task that makes you sag:\n",
    "No shame in seeking guidance.\n What command do you need a helping hand with?:\n",
    "Trouble seems to find you often.\n Reveal the command conundrum you're facing now:\n",
    "We all need a helping hand sometimes.\n Describe the command that has you reaching out for support:\n",
    "In a pickle again, I see?\n Describe the trouble you're in and let's work it out together:\n",
    "Brave adventurer, share the quest for the command you seek and I shall guide you through:\n",
    "When bugs run rampant, causing you despair,\n Detail the task that makes you pull out your hair:\n",
    "Here to rescue you from the labyrinth of documentation!\n Unravel your challenge to me:\n",
    "Seeking shell enlightenment, are we?\n Unveil the path to wisdom you're pursuing:\n",
    "In the coding realm, when all is grim,\n Describe the prompt that makes you scream:\n",
    "Ready to conquer the coding riddles?\n Describe the challenge you're facing, and I'll be your guide:\n",
    "Stuck in the maze of complex requirements?\n Describe the twists and turns that have you feeling lost:\n",
    "In the vast realm of coding, even superheroes need a sidekick!\n Tell me about the command you need assistance with:\n",
    "Don't worry, I won't judge.\n We've all been there! Ask about the command that has you scratching your head:\n",
    "In the vast sea of commands,\n it's okay to feel overwhelmed. Let me know which one you're struggling with, and we'll figure it out together:\n",
    "Well, well, look who's in need of guidance.\n Pray tell, what has you seeking my wisdom?:\n",
    "In a code abyss, dark and deep,\n Share the task that makes you weep:\n",
    "In the digital realm, where all devs cry,\n A prompt for support, can't be denied!\n",
]

fail_messages = [
    "Oh well, maybe next time!",
    "Better luck next time!",
    "Didn't quite get it this time huh?",
    "I guess you'll have to try again!",
    "Sorry for letting you down...",
    "I'm sorry, Dave. I'm afraid I can't do that.",
    "OK! I admit it! I hallucinated the whole thing.",
    "Pff I'm not even sorry...",
    "Let's see you do it better buddy.",
    "If I gave you something wild, turn the temperature down.",
]

# pylint: disable=anomalous-backslash-in-string
COMMANDEFT_ASCII_DESC = """
   ___                           ___       __ _   
  / __|___ _ __  _ __  __ _ _ _ |   \ ___ / _| |_ 
 | (__/ _ | '  \| '  \/ _` | ' \| |) / -_|  _|  _|
  \___\___|_|_|_|_|_|_\__,_|_||_|___/\___|_|  \__|

  A simple Python CLI for generating shell commands using OpenAI's chat models.
  Prompt, Generate, Dominate!  

"""

COMMANDEFT_NORMAL_DESC = """
--- CommanDeft ---
A simple Python CLI for generating shell commands using OpenAI's chat models.
Prompt, Generate, Dominate! 

"""
