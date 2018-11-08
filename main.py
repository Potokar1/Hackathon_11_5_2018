import snake_gather_data_smart as snake

file_name = 'C:\\Users\\Jack Dubbs\\Desktop\\Kaggle\\Hackathon1\\data\\600_pretty'
# This is how we open and close a file (with the with keyword)
with open(file_name, 'w') as output_file:
    for _ in range(600):
        snake.run(output_file)


# Notes: Use some numpy! It is good for data for a reason!
