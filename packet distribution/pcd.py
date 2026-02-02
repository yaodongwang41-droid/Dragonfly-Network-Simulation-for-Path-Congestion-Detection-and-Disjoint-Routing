import ded_dict as ed
import numpy as np


def remove_duplicates(arr):
    hash_table = {}
    result = []
    for item in arr:
        item.sort()
        key = tuple(map(tuple, item))
        if key not in hash_table:
            hash_table[key] = True
            result.append(item)
    return result


def routing(s, d, dct, ind, length=0):
    if ind == -2:  # packet in destination node
        ind = 0
        return length, s, dct, ind
    elif ind == -1:   # packet in destination node
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
                index = int(int((d[0] - 1) / L) % (M ** i) / M ** (i - 1))  # target router ID in each dimension
            else:
                index = int(int(d[0] / L) % (M ** i) / M ** (i - 1))
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


def packet(times):
    dct = ed.dct(M, N, L)

    S = ed.config(times, K, M, N, L)
    T = ed.config(times, K, M, N, L)
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    latency_distribution = np.zeros(terminated_cycle + 2)
    throughput_distribution = np.zeros(tp)
    while cycle < terminated_cycle:
        rec_p = 0  # the number of received packets per cycle
        for i in range(len(mark)):
            if mark[i] == 0:
                c_path = ed.routing_path(S[i].copy(), T[i].copy(), L)
                congestion_point = []
                for point in c_path:  # search for congestion point
                    rid = '0' * (len(str(L * M ** N + 1)) - len(str(point[0]))) + "".join([str(x) for x in point])
                    if dct[rid] > max_p - 2:
                        congestion_point.append(point)
                if len(congestion_point) > 0:  # path congestion
                    mark[i] = -2  # Schedule to the next cycle
            res = routing(S[i], T[i], dct, mark[i])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            length = length + res[0]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
                rec_p += 1
                label = cycle - i // times  # latency distribution label
                latency_distribution[label] += 1
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        throughput_distribution[rec_p] += 1
    return length, cycle, latency_distribution, throughput_distribution


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router
    max_p = 12   # buffer size

    terminated_cycle = 1000

    offered = 600  # number of injected packets
    number = K * (L * M ** N + 1) * M ** N
    y = np.zeros(terminated_cycle + 2)  # save the result of the latency distribution
    tp = int(offered * 1.3)  # Define throughput with sufficient redundancy
    z = np.zeros(tp)  # save the result of the throughput distribution
    num = 100  # repeat the simulation for num times
    for j in range(num):
        res = packet(offered)
        y += res[2]
        z += res[3]
        print(res[1])
        print(j)

    y /= num
    z /= num

    file = open('latency_distribution_pc.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('throughput_distribution_pc.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()

