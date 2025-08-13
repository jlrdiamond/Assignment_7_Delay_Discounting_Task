import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Rect, TextBox
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy import event
import random
### DIALOG BOX ROUTINE ###
exp_info = {'participant_nr': '', 'age': '','condition':['future','past','present']}
dlg = DlgFromDict(exp_info)

# If pressed Cancel, abort!
if not dlg.OK:
    quit()


# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
win = Window(size=(1200, 800), fullscr=False, monitor='samsung')

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=False)

# Initialize a (global) clock
clock = Clock()

# Initialize Keyboard
kb = Keyboard()
kb.clearEvents()

### START BODY OF EXPERIMENT ###
#
# This is where we'll add stuff from the second
# Coder tutorial.
#
### END BODY OF EXPERIMENT ###

### WELCOME ROUTINE ###
# Create a welcome screen and show for 2 seconds
welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0, -1), font='Calibri')
welcome_txt_stim.draw()
win.flip()
wait(2)

### INSTRUCTION ROUTINE ###
instruct_txt = """ 
In this experiment, you will make choices between monetary amounts.

On each trial you will choose between whether you prefer an immediate amount
or an amount available after a delay.
    
One trial will be randomly selected and you will receive the amount you chose on that 
trial. If you selected a delayed amount, the money will be paid to you after the respective delay.

You can click the offer you prefer

(Press ‘enter’ to start the experiment!)
 """
     
# Show instructions and wait until response (return)
instruct_txt = TextStim(win, instruct_txt, alignText='left', height=0.085)
instruct_txt.draw()
win.flip()

# Initialize keyboard and wait for response
kb = Keyboard()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        # The for loop was optional
        for key in keys:
            print(f"The {key.name} key was pressed within {key.rt:.3f} seconds for a total of {key.duration:.3f} seconds.")
        break  # break out of the loop!
        


offers = ['OffersA.csv','OffersB.csv']
random.shuffle(offers)

cues=pd.read_csv('cues.csv')
cue=cues.loc[0,'event']

### TRIAL LOOP ROUTINE ###
offer_trial = pd.read_csv(offers[0])
offer_trial = offer_trial.sample(frac=1)

# Create fixation target (a plus sign)
fix_target = TextStim(win, '+')
trial_clock = Clock()

# START exp clock
clock.reset()

# Show initial fixation
fix_target.draw()
win.flip()
wait(1)

rec1= Rect(win=win, size=0.4, fillColor=[0, 1, 0], lineColor=[1, 0, 0],pos=(-0.5,0)) 
rec2 = Rect(win=win, size=0.4, fillColor=[0, 1, 0], lineColor=[1, 0, 0],pos=(0.5,0)) 
rec_select1= Rect(win=win, size=0.6, fillColor=None, lineColor=[1, 0, 0],lineWidth=10, pos=(-0.5,0)) 
rec_select2 = Rect(win=win, size=0.6, fillColor=None, lineColor=[1, 0, 0],lineWidth=10, pos=(0.5,0)) 

for idx, row in offer_trial.iterrows():

    im_off = str(row['immediate_amount']) + " today"
    del_off = str(row['delayed_amount']) + " in " + str(row['delay']) + " days"

    n=random.randint(0, 1)
    if n < 0.5:
        stim_txt1 = TextStim(win, im_off, pos=(0.5, 0.0))
        stim_txt2 = TextStim(win, del_off, pos=(-0.5, 0.0))
    else:
        stim_txt1 = TextStim(win, im_off, pos=(-0.5, 0.0))
        stim_txt2 = TextStim(win, del_off, pos=(0.5, 0.0))


    m=random.randint(0, 1)
    if m == 0:
        present=cue
    else:
        present=""
    cue_present=TextStim(win,present,pos=(0,0.5))
    
    offer_trial.loc[idx, 'onset'] = -1

    trial_clock.reset()
    x=0
    click=0
    while trial_clock.getTime() < 4:
        if click == 0:
            win.mouseVisible=True
        rec1.draw()
        rec2.draw()
        stim_txt1.draw()
        stim_txt2.draw()
        cue_present.draw()
        win.flip()

        if mouse.isPressedIn(rec1):
            if x == 0:
                rt=trial_clock.getTime()
            x=1
            if n < 0.5 and click ==0:
                resp = "delayed"
                click = 1
            else:
                resp="immediate"
                click = 1
            win.mouseVisible=False
            rec1.draw()
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select1.draw()
            cue_present.draw()
            win.flip()
            
        if mouse.isPressedIn(rec2):
            if x == 0:
                rt=trial_clock.getTime()
            x=1
            if n < 0.5 and click==0:
                resp = "immediate"
                click=1
            else:
                resp="delayed"
                click=1
        ## make mouse not visible
            win.mouseVisible=False
            rec1.draw()
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select2.draw()
            cue_present.draw()
            win.flip()
    else:
        mouse.visible=False
        fix_target.draw()
        win.flip()
        wait(1)
        
    if offer_trial.loc[idx, 'onset'] == -1:
        offer_trial.loc[idx, 'onset'] = clock.getTime()
        

    resp_kb = kb.getKeys()
    if resp_kb:

        if 'q' in resp_kb:
            quit()

    if x == 0:
        resp = "miss"
        rt = "miss"
        
    print(resp)
    offer_trial.loc[idx, 'rt'] = rt
    offer_trial.loc[idx, 'resp'] = resp

offer_trial.to_csv(f"sub-{exp_info['participant_nr']}_results_no_manipulation.csv")