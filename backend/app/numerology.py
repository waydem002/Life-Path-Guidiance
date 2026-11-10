def reduce_number(n: int, is_life_path: bool = False) -> int:
    """
    Reduces a number to a single digit by summing its components.
    If it's a Life Path calculation, it preserves Master Numbers (11, 22, 33).
    """
    while n > 9:
        if is_life_path and n in [11, 22, 33]:
            return n
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_life_path(dob_string: str) -> int:
    """
    Calculates the Life Path Number from a date string (expects YYYY-MM-DD).
    Sums all individual digits in the year, month, and day.
    """
    # Extract only the numbers
    digits = [int(char) for char in dob_string if char.isdigit()]
    if not digits:
        return 0
    return reduce_number(sum(digits), is_life_path=True)

def get_letter_value(char: str) -> int:
    """Maps letters to their Pythagorean numerology values."""
    char = char.upper()
    mapping = {
        'A': 1, 'J': 1, 'S': 1,
        'B': 2, 'K': 2, 'T': 2,
        'C': 3, 'L': 3, 'U': 3,
        'D': 4, 'M': 4, 'V': 4,
        'E': 5, 'N': 5, 'W': 5,
        'F': 6, 'O': 6, 'X': 6,
        'G': 7, 'P': 7, 'Y': 7,
        'H': 8, 'Q': 8, 'Z': 8,
        'I': 9, 'R': 9
    }
    return mapping.get(char, 0)

def calculate_birthday_number(dob_string: str) -> int:
    """
    Extracts the day portion of YYYY-MM-DD and reduces it.
    Example: '1995-11-14' -> Day 14 -> 1 + 4 = 5.
    """
    try:
        day_part = int(dob_string.split("-")[2])
        return reduce_number(day_part)
    except (IndexError, ValueError):
        return 0

def analyze_name_elements(full_name: str) -> dict:
    """
    Calculates Expression, Soul Urge (vowels), and Personality (consonants) numbers.
    Spaces and special characters are safely ignored.
    """
    vowels = "AEIOU"
    expression_total = 0
    soul_urge_total = 0
    personality_total = 0
    
    for char in full_name.upper():
        if char.isalpha():
            val = get_letter_value(char)
            expression_total += val
            
            if char in vowels:
                soul_urge_total += val
            else:
                personality_total += val
                
    return {
        "expression": reduce_number(expression_total),
        "soul_urge": reduce_number(soul_urge_total),
        "personality": reduce_number(personality_total)
    }

def generate_full_profile(full_name: str, dob_string: str) -> dict:
    """
    Gathers all 5 calculated core numerology figures into a single payload.
    """
    name_results = analyze_name_elements(full_name)
    life_path = calculate_life_path(dob_string)
    birthday_num = calculate_birthday_number(dob_string)
    
    return {
        "life_path": life_path,
        "expression": name_results["expression"],
        "soul_urge": name_results["soul_urge"],
        "personality": name_results["personality"],
        "birthday_number": birthday_num
    }