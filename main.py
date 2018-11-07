import snake_gather_data as snake

file_name = 'C:\\Users\\Jack Dubbs\\Desktop\\Kaggle\\Hackathon1\\data\\6000_iterations'
# This is how we open and close a file (with the with keyword)
with open(file_name, 'w') as output_file:
    for _ in range(6000):
        snake.run(output_file)
