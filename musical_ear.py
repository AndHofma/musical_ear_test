"""
Musical-Ear-Test

Adapted from:
Correia, A. I., Vincenzi, M., Vanzella, P., Pinheiro, A. P., Lima, C. F., & Schellenberg, E. G. (2022). Can musical ability be tested online?. Behavior Research Methods, 54(2), 955-969. https://doi.org/10.3758/s13428-021-01641-2

See: https://app.gorilla.sc/openmaterials/218554

Other references:
Wallentin, M., Nielsen, A. H., Friis-Olivarius, M., Vuust, C., & Vuust, P. (2010). The Musical Ear Test, a new reliable test for measuring musical competence. Learning and Individual Differences, 20(3), 188-196. https://doi.org/10.1016/j.lindif.2010.02.004
Swaminathan, S., Kragness, H. E., & Schellenberg, E. G. (2021). The Musical Ear Test: Norms and correlates from a large sample of Canadian undergraduates. Behavior Research Methods, 53(5), 2007-2024. https://doi.org/10.3758/s13428-020-01528-8
"""


# Set-up
import os
import random
import datetime
import time
from psychopy import visual, core, event, gui, sound, monitors
import re


def check_paths(base_audio_path, base_image_path, results_path):
    """
    Function checks the existence of specific directories and raises
    exceptions with appropriate error messages if any of the directories are not found.
    """

    # Check if the base audio directory exists
    if not os.path.exists(base_audio_path):
        raise Exception("No audio folder detected. Please make sure that "
                        "'base_audio_path' is correctly set in the configurations")

    # Check if the base image directory exists
    if not os.path.exists(base_image_path):
        os.mkdir(base_image_path)

    # Check if the results directory exists, if not, create it
    if not os.path.exists(results_path):
        os.mkdir(results_path)


def get_participant_info():
    """
    Open a dialogue box with 3 fields: experiment name, current date and time, and subject_ID.
    Returns a dictionary with the entered information.
    """
    exp_data = {
        'experiment': 'musical_ear_test',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Subject_ID': 'subject_ID'
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data, title='Musical Ear Test', fixed=['cur_date', 'experiment'])

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


# participant questionnaire musical skills
def load_audio_files(base_audio_path, test_type):
    """
    Load audio files for a given test type (melody or rhythm) from a folder.
    """
    # Set the folder path where the audio files are stored
    folder_path = os.path.join(base_audio_path)
    # Initialize two lists for storing example and test files
    example_files = []
    test_files = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file matches the test type (melody or rhythm)
        if filename.startswith(test_type):
            # Get the full file path
            file_path = os.path.join(folder_path, filename)
            # If the file is an example file, add it to the example_files list
            if "_example" in filename:
                example_files.append(file_path)
            # If the file is a test file, add it to the test_files list at the correct position
            elif "_test" in filename:
                # Extract the trial number from the filename
                trial_number = int(re.findall(r'\d+', filename.split("_test")[1])[0])
                # Insert the file into the test_files list based on the trial number
                test_files.insert(trial_number - 1, file_path)

    # Uncomment these lines for checking in IDE
    # print(f"Liste der examples: {example_files}")
    # print(f"Liste der stimuli: {test_files}")

    # Return the lists of example files and test files
    return example_files, test_files


def display_instructions(win, instruction_text):
    """
    Display instructions on the screen and wait for a key press to continue.
    """
    instructions = visual.TextStim(win,
                                   text=instruction_text,
                                   wrapWidth=2,
                                   height=0.1,
                                   color='black')
    instructions.draw()
    win.flip()
    event.waitKeys()
    win.flip()


def draw_progress_bar(win, trial_number, total_trials, bar_width=1.5, bar_height=0.1):
    """
    Draw a progress bar in the given PsychoPy window.

    :param win: A PsychoPy window object where the progress bar will be drawn
    :param trial_number: The current trial number
    :param total_trials: The total number of trials
    :param bar_width: The width of the progress bar (default: 1.5)
    :param bar_height: The height of the progress bar (default: 0.1)
    """
    # Draw the background bar (gray) using a visual.Rect object
    background_bar = visual.Rect(win,
                                 pos=(0, -0.7),
                                 width=bar_width,
                                 height=bar_height,
                                 fillColor='gray',
                                 lineColor='gray')
    background_bar.draw()

    # Calculate the width of the filled portion of the progress bar
    filled_portion_width = bar_width * (trial_number / total_trials)

    # Draw the progress bar (black) if the filled portion width is greater than 0
    if filled_portion_width > 0:
        progress_bar = visual.Rect(win,
                                   pos=(-(bar_width - filled_portion_width) / 2, -0.7),
                                   width=filled_portion_width,
                                   height=bar_height,
                                   fillColor='black',
                                   lineColor='black')
        progress_bar.draw()


def play_stimulus_and_display_prompt(win, stimulus, prompt_text, time_limit, trial_number, base_image_path,
                                     total_trials, test_type):
    """
    Play a given auditory stimulus and display a prompt with 'yes' and 'no' buttons.

    :param win: A PsychoPy window object where the prompt will be displayed
    :param stimulus: An auditory stimulus to play
    :param prompt_text: The text to display as a prompt
    :param time_limit: The time limit for collecting a response (in seconds)
    :param trial_number: The current trial number
    :param base_image_path: The path to the image to display
    :param total_trials: The total number of trials
    :param test_type: The type of the test ('melody' or 'rhythm')
    :return: The collected response ('yes', 'no', or 'NA' if no response)
    """
    # Play the auditory stimulus
    stimulus.play()

    # Display trial number using a visual.TextStim object
    trial_text = visual.TextStim(win,
                                 text=f"{trial_number}",
                                 pos=(-0.7, 0.7),
                                 height=0.1,
                                 color='black')
    trial_text.draw()

    # Display test type (melody or rhythm) in German
    german_test_type = 'Melodie' if test_type == 'melody' else 'Rhythmus'
    testType = visual.TextStim(win,
                               text=german_test_type,
                               pos=(0, 0.7),
                               height=0.15,
                               color='black')
    testType.draw()

    # Display the prompt text using a visual.TextStim object
    prompt = visual.TextStim(win,
                             text=prompt_text,
                             pos=(0, 0.35),
                             height=0.15,
                             wrapWidth=1,
                             color='black')
    prompt.draw()

    # Display the image using a visual.ImageStim object
    image_stim = visual.ImageStim(win,
                                  image=base_image_path,
                                  pos=(0, -0.1))
    image_stim.draw()

    # Display the progress bar using the draw_progress_bar function
    if trial_number <= total_trials:
        draw_progress_bar(win, trial_number, total_trials)

    win.flip()

    # Wait for the stimulus duration and clear keyboard events
    core.wait(stimulus.getDuration() + 1)
    event.clearEvents(eventType='keyboard')

    # Create 'yes' and 'no' buttons using visual.Rect objects and text stimuli
    yes_button = visual.Rect(win,
                             pos=(-0.3, -0.2),
                             width=0.3,
                             height=0.3,
                             fillColor='green')
    no_button = visual.Rect(win,
                            pos=(0.3, -0.2),
                            width=0.3,
                            height=0.3,
                            fillColor='red')
    yes_text = visual.TextStim(win,
                               text='y \n yes / ja',
                               pos=(-0.3, -0.2),
                               height=0.1,
                               color='white')
    no_text = visual.TextStim(win,
                              text='n \n no / nein',
                              pos=(0.3, -0.2),
                              height=0.1,
                              color='white')

    # Wait for the specified time limit and collect responses
    response = None
    if time_limit is not None:
        timer = core.CountdownTimer(time_limit)
    while time_limit is None or timer.getTime() > 0:
        # Draw the prompt, buttons, and text on the window
        prompt.draw()
        yes_button.draw()
        yes_text.draw()
        no_button.draw()
        no_text.draw()
        win.flip()

        # Check for keyboard responses
        key_press = event.getKeys(keyList=['y', 'n'])
        if key_press:
            response = key_press[0]
            break

    # Translate the response from 'y' and 'n' to 'yes' and 'no'
    if response == 'y':
        response = 'yes'
    elif response == 'n':
        response = 'no'
    else:
        response = 'NA'

    # Clear the screen after collecting the response
    win.flip()
    core.wait(1)

    return response


def display_feedback(win, correct):
    """
    Display feedback (correct or incorrect) after the participant's response.

    Parameters:
    win (visual.Window): The PsychoPy window to display feedback on.
    correct (bool): Whether the participant's response was correct.
    """

    # Choose the appropriate feedback text based on the correctness of the response
    feedback_text = "Richtig!" if correct else "Falsch!"

    # Create a visual text stimulus with the feedback text
    feedback = visual.TextStim(win,
                               text=feedback_text,
                               pos=(0, 0),
                               height=0.25,
                               color='black')

    # Draw the feedback text on the window
    feedback.draw()

    # Update the window to show the feedback text
    win.flip()

    # Wait for 1 second before clearing the feedback text
    core.wait(1)

    # Clear the window after displaying the feedback
    win.flip()


def musical_ear_test(win, test_type, example_files, test_files, instruction_texts, practice_output_filename, test_output_filename, base_image_path, participant_info):

    """
    Perform the musical ear test using given example and test files, and save results progressively to the output file.

    Parameters:
    win (visual.Window): The PsychoPy window to display the test on.
    test_type (str): The type of the test, either 'melody' or 'rhythm'.
    example_files (list): A list of example audio file paths.
    test_files (list): A list of test audio file paths.
    instruction_texts (dict): A dictionary containing the instruction texts.
    practice_output_filename (str): The name of the output file to save practice trial results.
    test_output_filename (str): The name of the output file to save test trial results.
    base_image_path (str): The base path of the image files to display during the test.
    """

    # Initialize results list
    results = []

    # German translations for test types
    german_test_type = {
        "melody": "Melodien",
        "rhythm": "Rhythmen"  # German plurals for prompt
    }

    # Function to append a single result to the CSV file
    def append_result_to_csv(result, practice_filename, test_filename, participant_info):
        """
        Appends the given participant's test results to a CSV file. The function determines which file to write to (practice or test)
        based on the 'phase' key in the 'result' dictionary.

        Parameters:
        result (dict): A dictionary containing the participant's results from the test. It should include keys like 'trial', 'type',
        'phase', 'stimulus', 'response', 'correct', 'accuracy', 'start_time', 'end_time', and 'duration'.

        practice_filename (str): The name of the file where practice results should be written.

        test_filename (str): The name of the file where test results should be written.

        participant_info (dict): A dictionary containing information about the participant. It should include keys 'Subject_ID'
        and 'cur_date' (current date).

        Returns:
        None
        """
        output_filename = practice_filename if result['phase'] == 'practice' else test_filename
        with open(output_filename, 'a') as output_file:
            output_file.write(
                f"{participant_info['experiment']},{participant_info['Subject_ID']},{participant_info['cur_date']},{result['trial']},{result['type']},{result['phase']},{result['stimulus']},{result['response']},{result['correct']},{result['accuracy']},{result['start_time']},{result['end_time']},{result['duration']}\n"
            )

    # Start recording the duration of each task
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

    # Display part1 instructions
    display_instructions(win, instruction_texts[f'{test_type}_part1'])

    # Practice trials
    for i, example_file in enumerate(example_files):
        # Play stimulus and display prompt
        response = play_stimulus_and_display_prompt(win,
                                                    sound.Sound(example_file),
                                                    f"Sind die {german_test_type[test_type]} identisch?",
                                                    time_limit=None,  # Set time_limit=None for practice trials
                                                    trial_number=i + 1,
                                                    base_image_path=os.path.join(base_image_path, f"{test_type}.png"),
                                                    # Display corresponding image
                                                    total_trials=len(example_files),
                                                    test_type=test_type
                                                    )
        # Get the correct answer from the file name
        correct_answer = 'yes' if example_file.split('_')[-1].startswith('ident') else 'no'
        accuracy = 1 if response == correct_answer else (99 if response == "NA" else 0)

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Store the result and append it to the CSV file
        results.append({
            'trial': i + 1,
            'type': test_type,
            'phase': 'practice',
            'stimulus': example_file,
            'response': response,
            'correct': correct_answer,
            'accuracy': accuracy,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str
        })
        append_result_to_csv(results[-1], practice_output_filename, test_output_filename, participant_info)

        # Display feedback (correct or incorrect) after each example trial
        display_feedback(win, response == correct_answer)

        # Display practice instructions after each example trial
        display_instructions(win, instruction_texts[f'{test_type}_practice_{correct_answer}'])

    # Display instructions for test trials
    display_instructions(win, instruction_texts[f'{test_type}_part2'])

    # Test trials
    for i, test_file in enumerate(test_files):
        # Play stimulus and display prompt for test trials with a time limit of 2 seconds
        response = play_stimulus_and_display_prompt(win,
                                                    sound.Sound(test_file),
                                                    f"Sind die {german_test_type[test_type]} identisch?",
                                                    time_limit=2,
                                                    trial_number=i + 1,
                                                    base_image_path=os.path.join(base_image_path, f"{test_type}.png"),
                                                    total_trials=len(test_files),
                                                    test_type=test_type
                                                    )
        # Get the correct answer from the file name
        correct_answer = 'yes' if test_file.split('_')[-1].startswith('ident') else 'no'
        accuracy = 1 if response == correct_answer else (99 if response == "NA" else 0)

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Store the result and append it to the CSV file
        results.append({
            'trial': i + 1,
            'type': test_type,
            'phase': 'test',
            'stimulus': test_file,
            'response': response,
            'correct': correct_answer,
            'accuracy': accuracy,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str
        })
        append_result_to_csv(results[-1], practice_output_filename, test_output_filename, participant_info)

    return results


def main():
    """
    The main function to run the musical ear test experiment. This function initializes the experiment, displays
    instructions, collects participant information, and runs the melody and rhythm tests in random order.
    """
    # Instruction texts for various parts of the experiment
    instruction_texts = {
        'general_intro': 'Willkommen zum Test "Musikalisches-Gehör" \n\n'
                         'Dieser Test besteht aus zwei Teilen: \n\n'
                         'dem Melodie-Teil und dem Rhythmus-Teil. \n\n'
                         'Drücken Sie eine beliebige Taste, wenn Sie bereit sind, mit den Beispielen anzufangen.',

        'melody_part1': 'Melodie. \n\n'
                        'Sie werden nun immer zwei kurze Melodien hintereinander hören. \n\n'
                        'Sie müssen entscheiden, ob diese zwei Melodien identisch sind. \n'
                        'Sind sie identisch, drücken Sie "y" (yes) auf der Tastatur. \n'
                        'Sind sie nicht identisch, drücken Sie "n" (no) auf der Tastatur. \n\n'
                        'Lassen Sie uns mit 2 Beispielen starten. \n\n'
                        'Drücken Sie eine beliebige Taste, wenn Sie bereit sind.',

        'melody_practice_yes': 'In diesem Fall waren die Melodien identisch. \n\n'
                               'Die korrekte Antwort ist deshalb yes / ja \n'
                               'und Sie sollten "y" auf der Tastatur drücken. \n\n'
                               'Drücken Sie eine beliebige Taste, um das zweite Beispiel abzuspielen.',

        'melody_practice_no': 'In diesem Fall waren die Melodien nicht identisch. \n\n'
                              'Die korrekte Antwort ist deshalb no / nein \n'
                              'und Sie sollten "n" auf der Tastatur drücken. \n\n'
                              'Drücken Sie eine beliebige Taste, um die Übungsbeispiele abzuschließen.',

        'melody_part2': 'Jetzt beginnt der Test. \n\n'
                        'Sie werden insgesamt 52 Melodie-Paare hören. \n\n'
                        'Sie enthalten zusätzlich einen leisen Metronomton, \n in gleichmäßigen Abständen unterlegt. \n'
                        'Sie haben 2 Sekunden Zeit, per Tastatur zu antworten. \n'
                        'Drücken Sie die "y" oder "n" Taste, \n sobald die entsprechenden Button erscheinen. \n'
                        'Das nächste Melodie-Paar startet automatisch. \n'
                        'Versuchen Sie, so akkurat wie möglich zu antworten. \n\n'
                        'Drücken Sie eine beliebige Taste, wenn Sie bereit sind, anzufangen.',

        'rhythm_part1': 'Rhythmus. \n\n'
                        'Sie werden nun immer zwei kurze Rhythmen hintereinander hören. \n\n'
                        'Sie müssen entscheiden, ob diese zwei Rhythmen identisch sind. \n'
                        'Sind sie identisch, drücken Sie "y" (yes) auf der Tastatur. \n'
                        'Sind sie nicht identisch, drücken Sie "n" (no) auf der Tastatur. \n\n'
                        'Lassen Sie uns mit 2 Beispielen starten. \n\n'
                        'Drücken Sie eine beliebige Taste, wenn Sie bereit sind.',

        'rhythm_practice_yes': 'In diesem Fall waren die Rhythmen identisch. \n\n'
                               'Die korrekte Antwort ist deshalb yes / ja \n'
                               'und Sie sollten "y" auf der Tastatur drücken. \n\n'
                               'Drücken Sie eine beliebige Taste, um das zweite Beispiel abzuspielen.',

        'rhythm_practice_no': 'In diesem Fall waren die Rhythmen nicht identisch. \n\n'
                              'Die korrekte Antwort ist deshalb no / nein \n'
                              'und Sie sollten "n" auf der Tastatur drücken. \n\n'
                              'Drücken Sie eine beliebige Taste, um die Übungsbeispiele abzuschließen.',

        'rhythm_part2': 'Jetzt beginnt der Test. \n\n'
                        'Sie werden insgesamt 52 Rhythmus-Paare hören. \n'
                        'Sie enthalten zusätzlich einen leisen Metronomton, \n in gleichmäßigen Abständen unterlegt. \n'
                        'Sie haben 2 Sekunden Zeit, per Tastatur zu antworten. \n'
                        'Drücken Sie die "y" oder "n" Taste, \n sobald die entsprechenden Button erscheinen. \n'
                        'Das nächste Rhythmus-Paar startet automatisch. \n'
                        'Versuchen Sie, so akkurat wie möglich zu antworten. \n\n'
                        'Drücken Sie eine beliebige Taste, wenn Sie bereit sind, anzufangen.',

        'end': 'Sie haben es geschafft! \n\n'
               'Drücken Sie eine beliebige Taste, um den Test abzuschließen.'
    }

    # Define base paths for audio, images, and results
    base_audio_path = "audio"
    base_image_path = "pics"
    results_path = "results"

    # Ensure the required paths exist
    check_paths(base_audio_path, base_image_path, results_path)

    # Get participant information
    participant_info = get_participant_info()

    currentMonitor = monitors.Monitor(name='testMonitor')
    win = visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                        monitor="testMonitor",
                        allowGUI=True,
                        fullscr=True,
                        color=(255, 255, 255)
                        )
    win.flip()

    # Load melody and rhythm files from the 'audio' folder
    melody_example_files, melody_test_files = load_audio_files(base_audio_path, 'melody')
    rhythm_example_files, rhythm_test_files = load_audio_files(base_audio_path, 'rhythm')

    # Determine random starting test
    starting_tests = ['melody', 'rhythm']
    random.shuffle(starting_tests)

    # Create the output files with headers and save them in results/
    practice_output_filename = os.path.join(results_path,
                                            f"MET_practice_results_{participant_info['Subject_ID']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    test_output_filename = os.path.join(results_path,
                                        f"MET_test_results_{participant_info['Subject_ID']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    for output_file in [practice_output_filename, test_output_filename]:
        with open(output_file, 'w') as file:
            file.write(
                'experiment,subject_ID,date,trial,type,phase,stimulus,response,correct,accuracy,start_time,end_time,duration \n'
                )

    # Run the tests in random order
    for i, test in enumerate(starting_tests):
        # Display general instructions only once before the first practice trials
        if i == 0:
            display_instructions(win, instruction_texts['general_intro'])

        # Run the melody or rhythm test depending on the current test type
        if test == 'melody':
            musical_ear_test(
                win,
                'melody',
                melody_example_files,
                melody_test_files,
                instruction_texts,
                practice_output_filename,
                test_output_filename,
                base_image_path,
                participant_info
            )

        elif test == 'rhythm':
            musical_ear_test(
                win,
                'rhythm',
                rhythm_example_files,
                rhythm_test_files,
                instruction_texts,
                practice_output_filename,
                test_output_filename,
                base_image_path,
                participant_info
            )

    # Display the end instruction after the last trial of the second test trials
    display_instructions(win, instruction_texts['end'])

    # Close the experiment window
    win.close()


if __name__ == "__main__":
    main()
