import re

def score_letter(letter, position, letter_values):
    if position == 0:
        return 0
    elif letter == 'E':
        return 20
    else:
        base_score = 5 if position == -1 else position
        return base_score + letter_values.get(letter, 0)

def generate_abbreviations(name, letter_values):
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
    values = {}
    with open(filename, 'r') as file:
        for line in file:
            letter, value = line.split()
            values[letter.upper()] = int(value)
    return values

def main():
    surname = "Harry"  
    input_filename = input("Enter the name of the input file (.txt): ")
    letter_values = read_letter_values()

    names = []
    all_abbreviations = {}

    with open(input_filename, 'r') as file:
        for line in file:
            name = line.strip()
            names.append(name)
            abbreviations = generate_abbreviations(name, letter_values)
            for abbr, score in abbreviations.items():
                if abbr not in all_abbreviations:
                    all_abbreviations[abbr] = []
                all_abbreviations[abbr].append((name, score))

    output_filename = f"{surname}_{input_filename.split('.')[0]}_abbrevs.txt"
    with open(output_filename, 'w') as file:
        for name in names:
            abbreviations = generate_abbreviations(name, letter_values)
            valid_abbrs = {abbr: score for abbr, score in abbreviations.items() if len(all_abbreviations[abbr]) == 1}
            best_score = min(valid_abbrs.values(), default=None)
            best_abbrs = [abbr for abbr, score in valid_abbrs.items() if score == best_score]
            file.write(f"{name}\n{' '.join(best_abbrs) if best_abbrs else ''}\n")

    print(f"Output written to {output_filename}")

if __name__ == "__main__":
    main()










