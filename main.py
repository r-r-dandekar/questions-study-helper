from pathlib import Path
import textwrap
import random

# Example directory structure
# /some/dir/main.py
# /some/dir/data/Q3B/all.txt

DATA_DIR = 'data'

def process(section, filename, create_backup_file=False):
    sectionpath = Path(DATA_DIR) / section
    filepath = sectionpath / filename
    content = ''
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if create_backup_file:
        # Rename the file to indicate that it has been processed
        new_filename = str(Path(filename).stem) + '-processed'
        i = 0
        while (sectionpath / (new_filename+f"{i:02}.txt")).exists():
            i += 1
        new_filename = sectionpath / (new_filename+f"{i:02}.txt")
        filepath.rename(new_filename)
    else:
        filepath.unlink(missing_ok=True)
    
    # Assumption: Neither the question nor the answer can contain the string '\n\n'
    question_answer_pairs = content.split('\n\n')

    randomize = input("Randomize question order? ")
    if randomize.lower().strip() in ('y', 'yes'):
        random.shuffle(question_answer_pairs)
    
    with    (open(sectionpath / 'easy.txt', 'a', encoding='utf-8') as easy,
            open(sectionpath / 'medium.txt', 'a', encoding='utf-8') as medium,
            open(sectionpath / 'hard.txt', 'a', encoding='utf-8') as hard,
            open(sectionpath / 'ask.txt', 'a', encoding='utf-8') as ask):

        quit = False
        for pair in question_answer_pairs:
            # Assumption: Neither the question nor the answer can contain the word 'Answer:'
            split = pair.split("Answer:")
            question, answer = split[0], split[-1]
            
            if not question.strip():
                continue

            if quit:
                with open(sectionpath / 'all.txt', 'a', encoding='utf-8') as all:
                    all.write(f'{question}Answer:{answer}\n\n')
                continue


            print(f'{question}Answer:\n{answer}\n')

            while True:
                try:
                    action = input(textwrap.dedent(f'''\
                                        Choose a number to continue:
                                        1. Move to Easy
                                        2. Move to Medium
                                        3. Move to Hard
                                        4. Move to Ask
                                        5. Quit
                                        Your choice: '''))
                    action = int(action)
                    if action == 1:
                        easy.write(f'{question}Answer:{answer}\n\n')
                        break
                    elif action == 2:
                        medium.write(f'{question}Answer:{answer}\n\n')
                        break
                    elif action == 3:
                        hard.write(f'{question}Answer:{answer}\n\n')
                        break
                    elif action == 4:
                        ask.write(f'{question}Answer:{answer}\n\n')
                        break
                    elif action == 5:                    
                        quit = True
                        with open(sectionpath / 'all.txt', 'a', encoding='utf-8') as all:
                            all.write(f'{question}Answer:{answer}\n\n')
                        break
                    else:
                            print('Please choose a valid option!')
                except Exception as e:
                    print(f'Error: {e}')



section = input('Enter section (directory): ')

while True:
    try:
        action = input(textwrap.dedent(f'''\
                            Choose a number to continue:
                            1. Process 'all.txt'
                            2. Process 'easy.txt'
                            3. Process 'medium.txt'
                            4. Process 'hard.txt'
                            5. Process 'ask.txt'
                            6. Quit
                            Your choice: '''))
        action = int(action)
        if action == 1:
            process(section, 'all.txt', create_backup_file=True)
            break
        elif action == 2:
            process(section, 'easy.txt')
            break
        elif action == 3:
            process(section, 'medium.txt')
            break
        elif action == 4:
            process(section, 'hard.txt')
            break
        elif action == 5:
            process(section, 'ask.txt')
            break
        elif action == 6:
            break
        else:
            print('Please choose a valid option!')
    except Exception as e:
        print(f'Error: {e}')