import snake_gather_data_smart as snake

file_name = 'C:\\Users\\jackd\\Desktop\\kaggle\\HackaThon1\\data\\test'
# This is how we open and close a file (with the with keyword)
with open(file_name, 'w') as output_file:
    for _ in range(2):
        snake.run(output_file)


# Notes: Use some numpy! It is good for data for a reason!
