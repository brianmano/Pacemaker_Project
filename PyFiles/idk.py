import time

q = [0, 0, 0, 0]

def jk(j, not_k, q):
    if ((j == 0) and (not_k == 1)):
        return q
    elif ((j == 0) and (not_k == 0)):
        return 0
    elif ((j == 1) and (not_k == 1)):
        return 1
    else:
        return not q

cur_state = 1

while True:
    print(f'state {cur_state}: {int(q[0])} {int(q[1])} {int(q[2])} {int(q[3])}')
    j1 = 1
    not_k1 = 0

    j2 = q[0]
    not_k2 = not q[0]

    j3 = q[1] or not q[3]
    not_k3 = not q[1]

    j4 = q[1] or q[3]
    not_k4 = not q[2]

    states = [[j1, not_k1], [j2, not_k2], [j3, not_k3], [j4, not_k4]]

    for i in range(len(q)):
        q[i] = jk(j=states[i][0], not_k=states[i][1], q=q[i])

    cur_state += 1
    time.sleep(1)