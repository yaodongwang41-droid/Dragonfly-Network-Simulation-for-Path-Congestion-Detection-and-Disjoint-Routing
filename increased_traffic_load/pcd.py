import ded_dict as ed
import numpy as np


def routing_path(s, d):
    path = []
    if len(s) == len(d) and s != d:  # packet in source node
        s = s[0:2]
        path.append(s.copy())
    if s[0] != d[0]:   # different groups
        if s[1] != (d[0] - int(d[0] > s[0])) // L:  # not in target router
            s[1] = (d[0] - int(d[0] > s[0])) // L
            path.append(s.copy())
        # in target group
        s[1] = (s[0] - int(d[0] < s[0])) // L
        s[0] = d[0]
        path.append(s.copy())
    # the same group
    if s[1] != d[1]:   # not in destination router
        s[1] = d[1]
        path.append(s.copy())
    return path


def routing(s, d, dct, ind, length=0):
    if ind == -1:   # packet in destination node
        return length, s, dct, ind
    elif ind == -2:   # delay packet
        ind = 0
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


# def rid(y):
#     return '0' * (len(str(L * M ** N + 1)) - len(str(y[0]))) + "".join([str(x) for x in y])

def packet(lam=0.5):
    times = int(lam * (L*M**N+1)* M**N*K)
    dct = ed.dct(M, N, L)

    SF = ed.config(lam, K, M, N, L)
    TF = ed.config(lam, K, M, N, L)

    S = SF[0:len(SF)//5]         # select 20% of the source-destination pairs
    T = TF[0:len(TF)//5]
    times = times//5
    cycle = 0
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    throughput = []
    while cycle < 200+terminate_cycle:    # simulate for 300 cycles
        rec = 0  # the number of received packets
        send = []  # sending packets for last 2*N+3 cycles
        for i in range(len(mark)):
            if cycle > 220 and mark[i] == 0:
                c_path = routing_path(S[i].copy(), T[i].copy())
                congestion_point = []
                for point in c_path:      # search for congestion point
                    rid = '0' * (len(str(L * M ** N + 1)) - len(str(point[0]))) + "".join([str(x) for x in point])
                    if dct[rid] > max_p-2:
                        congestion_point.append(point)
                if len(congestion_point) > 0:  # path congestion
                    mark[i] = -2      # Schedule to the next cycle
            res = routing(S[i], T[i], dct, mark[i])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
        if cycle > 200:
            throughput.append(rec)
        if cycle == 220:  # add more source-destination pairs
            times = int(lam * (L * M ** N + 1) * M ** N * K)
            sb, tb = SF.copy(), TF.copy()
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
    return throughput


if __name__ == "__main__":
    K = 4     # number of nodes for each router0
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router
    max_p = 12  # buffer size

    num = 20  # repeat the simulation for num times
    terminate_cycle = 100
    y = np.zeros(terminate_cycle-1, int)
    for j in range(num):
        res = packet(lam=0.75)
        y += res
        print(j)
    y = y/num
    file = open('cycles_pb.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()


