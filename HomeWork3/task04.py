def is_armstrong(number: int) -> bool:
    numbers=[int(i) for i in str(number)]
    count_numbers=len(numbers)
    Armstrong_num=sum([i**count_numbers for i in numbers])
    return Armstrong_num==number


assert is_armstrong(153) == True
assert is_armstrong(10) == False
