import ded_dict as ed
import numpy as np


def routing_length(s, d):
    length = 0
    if len(s) == len(d) and s != d:  # packet in source node
        s = s[0:2]
        length += 1
    if s[0] != d[0]:   # different groups
        if s[1] != (d[0] - int(d[0] > s[0])) // L:  # not in target router
            s[1] = (d[0] - int(d[0] > s[0])) // L
            length += 1
        # in target group
        s[1] = (s[0] - int(d[0] < s[0])) // L
        s[0] = d[0]
        length += 1
    # the same group
    if s[1] != d[1]:   # not in destination router
        s[1] = d[1]
        length += 1
    if s != d:     # destination router
        length += 1
    return length


def routing(s, d, dct, ind, max_p=12, length=0):
    if ind == -1:   # packet in destination node
        return length, s, dct, ind
    elif ind == 0:  # packet in source node
        temp = s.copy()
        del temp[len(temp) - 1]
        rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
        if dct[rid] < max_p:
            dct[rid] += 1
            length += 1
            ind = 1
            s = temp
        return length, s, dct, ind
    elif s[0] != d[0]:  # different groups
        for i in range(1, len(s)):
            if s[0] < d[0]:
                index = ((d[0] - 1) // L) % (M ** i) // M ** (i - 1)  # target router ID in each dimension
            else:
                index = (d[0] // L) % (M ** i) // M ** (i - 1)
            if s[i] != index:  # to the target router of ith dimension
                temp = s.copy()
                temp[i] = index
                rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
                cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    length += 1
                    s = temp
                return length, s, dct, ind
        else:  # to the target group
            temp = s.copy()
            for i in range(1, len(s)):  # get the router ID of the target group in each dimension
                if temp[0] < d[0]:
                    temp[i] = int(int(temp[0] / L) % (M ** i) / M ** (i - 1))
                else:
                    temp[i] = int(int((temp[0] - 1) / L) % (M ** i) / M ** (i - 1))
            temp[0] = d[0]
            rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
            cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
    elif s[1:len(d)-1] != d[1:len(d)-1]:  # the same group
        for i in range(1, len(s)):
            if s[i] != d[i]:
                temp = s.copy()
                temp[i] = d[i]
                rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
                cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    length += 1
                    s = temp
                return length, s, dct, ind
    else:           # in destination router
        dct['0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])] -= 1
        s.append(d[len(d)-1])
        ind = 2
        length += 1
    return length, s, dct, ind


def packet(lam=0.75):
    times = int(lam * (L*M**N+1)* M**N*K)
    dct = ed.dct(M, N, L)
    SF = ed.config(lam, K, M, N, L)
    TF = ed.config(lam, K, M, N, L)

    S = SF.copy()
    T = TF.copy()
    cycle = 0
    mark = list(np.zeros(times, int))
    sb, tb = SF.copy(), TF.copy()
    throughput = []
    rl = []
    for p in range(len(SF)):
        rl.append(routing_length(SF[p].copy(), TF[p].copy()))
    drop = 0
    diff = 0
    while cycle < 100+terminate_cycle:    # simulate for 280 cycles
        rec = 0  # the number of received packets
        for i in range(len(mark)):
            s_cycle = i//times
            if cycle - s_cycle > rl[i%times] and mark[i] != -1:  # drop packets
                if mark[i] != 0:
                    dct['0' * (len(str(L * M ** N + 1)) - len(str(S[i][0]))) + "".join([str(x) for x in S[i]])] -= 1
                mark[i] = -1
                drop += 1
            res = routing(S[i], T[i], dct, mark[i])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
        if cycle > 80:
            throughput.append(rec)
        if cycle < 120:
            S += sb
            T += tb
            mark += list(np.zeros(times, int))
        cycle += 1
    return throughput


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router

    num = 100  # repeat the simulation for num times
    terminate_cycle = 100
    y = np.zeros(20+terminate_cycle-1, int)
    for j in range(num):
        res = packet(lam=0.75)
        y += res
        print(j)
    y = y/num
    file = open('cycles.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()


