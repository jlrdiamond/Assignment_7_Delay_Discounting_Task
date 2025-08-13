#Assignment Instructions: Write some code that summarizes the reaction time for the delay discounting task (for each person) according to whether a right or left response was made. Copy and paste the code [in Canvas].

#1st submission below:
#Assignment 7 code is interspersed throughout delay discounting task script from the LectureDD.py script (Lecture 6). 

if mouse.isPressedIn(rec1):	#If pt clicks mouse in rec1 (choosing either imm_off_amt or del_off_amt, depending on value of n)
            if x == 0:			#If x is equal to 0, which is also a click
                rt=trial_clock.getTime()	#Record the time and assign to variable, rt
            x=1				#Set x equal to 1, which is not a click. What is the purpose of doing this here? 
            if n < 0.5 and click ==0:	#If n is <0.5 and click is equal to 0 (we set it =0 so it has to be)
                resp = "delayed"	#Assign string "delay" string to variable resp
		side = "left"		#Added for Assignment 7: since rec1 is always on L and pt clicked in rec1, initialize string “left” and assign to variable, side
                click = 1		#Set click equal to 1 (assign value 1 to variable click)
            else:			#Otherwise
                resp="immediate"	#Assign string "immediate" to variable resp
		side = "left"		#Added for Assignment 7: since rec1 is always on L and pt clicked in rec1, initialize string “left” and assign to variable, side
                click = 1		#Set click equal to 1 (assign value 1 to variable click)
            win.mouseVisible=False	#Make the mouse not visible in exp window
            rec1.draw()			#Draw the choice options into exp window
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select1.draw()
            cue_present.draw()		#Draw the cue_present variable (where present either = cue or = "") into exp window
            win.flip()			#Flip all of that from back to front buffer so pt can see

 if mouse.isPressedIn(rec2):	#If pt clicks mouse in rec 2 (choosing either imm_off_amt or del_off_amt, depending on value of n)
            if x == 0:			#If x equals 0 (this will return false, since we most recently set x=1)
                rt=trial_clock.getTime()	#Record the time and assign to variable rt
            x=1				#Set x equal to 1
            if n < 0.5 and click==0:	#If n <0.5 and click is equivalent to 0 (will return false, since we most recently set click equal to 1)
                resp = "immediate"	
		side = "right"		#Added for Assignment 7: since rec2 is always on R and pt clicked in rec2, initialize string “right” and assign to variable, side
                click=1			#Set click equal to 1
            else:
                resp="delayed"
		side = "right"		#Added for Assignment 7: since rec2 is always on R and pt clicked in rec2, initialize string “right” and assign to variable, side
                click=1			#Set click equal to 1
        ## make mouse not visible	
            win.mouseVisible=False
            rec1.draw()			#Draw the choice options into exp window
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select2.draw()
            cue_present.draw()		#Draw the cue_present variable (where present either = cue or = "") into exp window
            win.flip()			#Flip all of that from back to front buffer so pt can see
    else:
        mouse.visible=False		
        fix_target.draw()
        win.flip()
        wait(1)

#[…]

#Record pt responses
print(resp)				#Print pt responses
offer_trial.loc[idx, 'rt'] = rt			#Create a new column in offer_trial spreadsheet called rt. Store data (in numerical form) collected for each trial for the variable, rt in the cells located here using the idx function which finds their row number.
offer_trial.loc[idx, 'resp'] = resp	#Create a new column in offer_trial spreadsheet called resp. Store data (in the form of a string) collected for each trial for the variable, resp n the cells located here using the idx function which finds their row number.
offer_trial.loc[idx, ‘side’] = side	#Added for Assignment 7: Create a new column in offer_trial spreadsheet called side. Store data (in the form of a string) collected for each trial for the variable, side in the cells located here using the idx function which finds their row number.


#Group by side, calculate mean of rt
side_avgs_df = (
	offer_trial			#Create new df side_avgs_df comprised of the results of the following done in offer_trial dataframe:
	.groupby(['side’])	#Group by side (i.e., left or right click)
	.agg(				#Conduct the following summary statistics
		avg_rt = (‘rt’, ‘mean’)	#Calculate the mean rt for the #times pt chose rec1 (left)/total trials and mean rt for the #times pt chose rec2 (right)/total trials (info found in the side column)
)

#Alternative code (inspired by lecture5.py emo_stroop task code):
side_avgs_df = offer_trial.dropna(subset=[‘rt’]).groupby([‘side’])[‘rt].mean()

#Save dataframe as csv file with pt number
offer_trial.to_csv(f"sub-{exp_info['participant_nr’]_raw}.csv")
side_avgs_df.to_csv(f"sub-{exp_info['participant_nr’]_avgs}.csv")

#Assignment 7 additional planning: Could then .pivot_wide() offer_trial dataframe, and .merge() with side_avgs_df in a new side_avgs column in a merged offer_trial_df dataframe


_________________________


#Assignment 7 for delay discounting task dataset from Lecture 7 (class_python_week1.ipynb (https://colab.research.google.com/drive/1M7IJkcKYkCV9D3LiBIqgFvaGneJvV_A4#scrollTo=9eec29ce-2d1a-45f5-b5c3-e113dde35437) and DelayDisc_example.csv file, https://raw.githubusercontent.com/CaitlinLloyd/Psychology_Programming2025/refs/heads/main/Data/DelayDisc_example.csv found here https://github.com/CaitlinLloyd/Psychology_Programming2025/tree/main/Data)

#Given this, from https://colab.research.google.com/drive/1M7IJkcKYkCV9D3LiBIqgFvaGneJvV_A4#scrollTo=9eec29ce-2d1a-45f5-b5c3-e113dde35437:
data=pd.read_csv("https://raw.githubusercontent.com/CaitlinLloyd/Psychology_Programming2025/refs/heads/main/Data/DelayDisc_example.csv")

#And that 1 = left and 2 = right (presumably in choice column)

#(At beginning of task)    
trial_clock.reset()			#Start timer by resetting trial clock

#(During task) record the time at which pt makes their choice [choice making code not present here] and assign it to a variable called rt
rt=trial_clock.getTime()

#Record rt values
print(choice)				#Print pt responses
data.loc[idx, 'rt'] = rt		#Record rt values in new column in data dataframe called rt

#At end of pt finishing experiment
#Calculate summary statistics for rt grouping by choice (where 1 = left, 2 = right)
sum_data = (		#Create a new summary dataframe
	data			#That contains information from the data dataframe
	.dropna(subset’=['rt’])		#drop values of na in the rt column
	.groupby([‘choice’])			#group by ‘choice’
	.agg(
		avg_rt = (‘rt’, ‘mean’)	#calculate the following summary statistic: mean of values in rt column
)	
#Alternative format
sum_data = data.dropna(subset=[‘rt’]).groupby([‘choice’])[‘rt’].mean()

#Save dataframe as csv file with pt number (assuming participant_nr was recorded in a dialogue box at start of experiment)
data.to_csv(f"sub-{exp_info['participant_nr’]_raw}.csv")
sum_data.to_csv(f"sub-{exp_info['participant_nr’]_sum_data}.csv")

