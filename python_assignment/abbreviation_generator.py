import re  # The 're' module in Python provides support for regular expressions. Regular expressions are a powerful tool for processing and manipulating strings based on specific patterns. In this script, 're' is used to filter and process text.
import os

def score_letter(letter, position, letter_values):
    """
    Calculate the score of a letter based on its position and predefined letter values.
    - letter: The letter to score.
    - position: The position of the letter in the word.
    - letter_values: A dictionary mapping letters to their respective values.
    Returns the calculated score.
    """
    if position == 0:
        return 0
    elif letter == 'E':
        return 20
    else:
        base_score = 5 if position == -1 else position
        return base_score + letter_values.get(letter, 0)

def generate_abbreviations(name, letter_values):
    """
    Generate possible abbreviations for a given name and calculate their scores.
    - name: The name to generate abbreviations for.
    - letter_values: A dictionary of letter scores.
    Returns a dictionary of abbreviations and their scores.
    """
    words = re.sub(r"[^a-zA-Z ]", "", name).upper().split()
    abbreviations = {}
    for word in words:
        for i in range(len(word)):
            for j in range(i + 1, len(word)):
                abbr = word[0] + word[i] + word[j]
                score = score_letter(word[i], i, letter_values) + score_letter(word[j], j, letter_values)
                if abbr not in abbreviations or score < abbreviations[abbr]:
                    abbreviations[abbr] = score
    return abbreviations

def read_letter_values(filename="values.txt"):
    """
    Read letter values from a file.
    - filename: The name of the file to read from.
    Returns a dictionary mapping letters to their values.
    """
    values = {}
    with open(filename, 'r') as file:
        for line in file:
            letter, value = line.split()
            values[letter.upper()] = int(value)
    return values

def main():
    """
    Main function to execute the script. It reads names from a file,
    generates abbreviations, and writes the results to an output file.
    """
    # Replace with your surname
    surname = "Harry"

    # Ask for the path of the input file and make it OS-independent
    input_filename = input("Enter the name of the input file (.txt): ")
    input_path = os.path.join(os.getcwd(), input_filename)
    letter_values = read_letter_values()

    names = []
    all_abbreviations = {}

    # Read names from the input file
    with open(input_path, 'r') as file:
        for line in file:
            name = line.strip()
            names.append(name)
            abbreviations = generate_abbreviations(name, letter_values)
            for abbr, score in abbreviations.items():
                if abbr not in all_abbreviations:
                    all_abbreviations[abbr] = []
                all_abbreviations[abbr].append((name, score))

    # Generate the output file name and path
    output_filename = f"{surname}_{os.path.splitext(input_filename)[0]}_abbrevs.txt"
    output_path = os.path.join(os.getcwd(), output_filename)
    with open(output_path, 'w') as file:
        for name in names:
            abbreviations = generate_abbreviations(name, letter_values)
            valid_abbrs = {abbr: score for abbr, score in abbreviations.items() if len(all_abbreviations[abbr]) == 1}
            best_score = min(valid_abbrs.values(), default=None)
            best_abbrs = [abbr for abbr, score in valid_abbrs.items() if score == best_score]
            file.write(f"{name}\n{' '.join(best_abbrs) if best_abbrs else ''}\n")

    print(f"Output written to {output_path}")

if __name__ == "__main__":
    main()
