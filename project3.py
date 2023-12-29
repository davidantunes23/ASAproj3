from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpInteger, GLPK, value

args = input()
args_list = [int(num) for num in args.split()]

num_toys = args_list[0]
num_packs = args_list[1]
max_toys = args_list[2]

profit = []
capacity = []
packs = [[] for _ in range(num_toys)]
total_capacity = []

for i in range(num_toys):
    args = input()
    args_list = [int(num) for num in args.split()]
    xi = LpVariable("x" + str(i), 0, args_list[1], LpInteger)
    profit.append((args_list[0], xi))
    total_capacity.append((1, xi))
    capacity.append(args_list[1])
    packs[i].append(xi)

for i in range(num_toys, num_toys + num_packs):
    args = input()
    args_list = [int(num) for num in args.split()]
    xi = LpVariable("x" + str(i), 0, max_toys, LpInteger)
    total_capacity.append((3, xi))
    profit.append((args_list[3], xi))
    packs[args_list[0]-1].append(xi)
    packs[args_list[1]-1].append(xi)
    packs[args_list[2]-1].append(xi)

print(profit)
print(capacity)
print(packs)
print(total_capacity)

prob = LpProblem("Problema", LpMaximize)

prob += lpSum(coef * var for coef, var in profit)
prob += lpSum(coef * var for coef, var in total_capacity) <= max_toys

for i in range(num_toys):
    prob += lpSum(packs[i]) <= capacity[i]

prob.solve(GLPK(msg=0))
print("Valor da funcao objectivo:", value(prob.objective))
