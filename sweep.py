import itertools

input = "foo bar a=2,3 x=8,9"
words = input.split(" ")
shared_command = ' '.join(filter(lambda w: '=' not in w, words))
sweep_dict = {}
for word in words:
    if '=' in word:
        assert len(word.split('=')) == 2
        arg_name = word.split('=')[0]
        value_list = word.split('=')[1].split(',')
        sweep_dict[arg_name] = value_list
arg_assignment_sweep_list = []
for k,v in sweep_dict.items():
    arg_assignment_sweep_list.append([f"{k}={val}" for val in v])

command_list = []
for element in itertools.product(*arg_assignment_sweep_list):
    command_list.append(shared_command + " " + " ".join(element))

print(f"Submitting job array with following {len(command_list)} expts")
for com in command_list:
    print(com)
print("-------------------------------------------")
