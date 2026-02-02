import numpy as np


def sort_length(input_array):
    sorted_array = sorted(input_array, key=lambda x: len(x))
    return sorted_array


def router_gen(m, n, l):
    out = np.zeros(n+1)
    out[0] = np.random.randint(0, l * m**n)  # group ID
    out[1:n+1] = np.random.randint(0, m - 1, size=n)  # router ID
    return [int(x) for x in out]


def local_neighbor_router(s, m, n):
    res = []
    for var in range(m - 1):    # find all the routers in the same dimension of the local group
        for ele in range(n):     # find all the routers in different dimension of the local group
            temp = s.copy()
            temp[1 + ele] = (s[1 + ele] + var + 1) % m
            res.append(temp)
    return res


def remote_neighbor_router(s, m, l):
    res = []
    temp_g = s.copy()
    pre = 0
    n = len(s) - 1
    for i in range(n):
        pre = pre + s[n - i] * m ** (n - 1 - i) * l
    for i in range(n):
        temp_g[1 + i] = ((s[0] - int(s[0] > pre)) // l) % (m ** (i+1)) // m ** i
    for var in range(l):   # find all the routers in remote groups
        temp = temp_g.copy()
        temp[0] = pre + var + int(s[0] <= (pre+var))
        res.append(temp)
    return res


def routing(s, d, L, M):   # router to router
    if s[0] != d[0]:  # different groups
        for i in range(1, len(s)):
            index = (d[0]-int(s[0] < d[0]))//L % (M ** i) // M**(i-1)        # target router ID in each dimension
            if s[i] != index:
                s[i] = index      # to the target router of ith dimension
                return s
        else:    # to the target group
            for i in range(1, len(s)):     # get the router ID of the target group in each dimension
                s[i] = (s[0]-int(s[0] > d[0])) // L % (M ** i) // M ** (i - 1)
            s[0] = d[0]
    else:    # the same group
        for i in range(1, len(s)):
            if s[i] != d[i]:
                s[i] = d[i]
                return s
    return s


def path(m, n, l, s, d):
    total_path = []
    jointed_router = []
    single_path = [d]
    temp = s.copy()
    if s == d:  # the same router
        return [[s.copy()]]
    while temp != d:
        if s != temp:
            jointed_router.append(temp.copy())
        single_path.insert(-1, temp.copy())
        temp = routing(temp, d, l, m)
    total_path.append(single_path.copy())
    router_list = remote_neighbor_router(s, m, l) + local_neighbor_router(s, m, n)
    des_router_list = remote_neighbor_router(d, m, l) + local_neighbor_router(d, m, n)
    global_router_list = []
    for row in des_router_list[l:]:
        global_router_list.append(remote_neighbor_router(row, m, l)[np.random.randint(0, l)])
    for i in range(len(router_list)):
        if router_list[i] not in jointed_router and router_list[i] != d:
            single_path = [s, des_router_list[i], d]
            mark = 1
            index = -2
            if i > l-1 and router_list[i] != des_router_list[i]:    # local neighbor routers
                single_path.insert(index, router_list[i].copy())
                router_list[i] = remote_neighbor_router(router_list[i], m, l)[np.random.randint(0, l)]
                des_router_list[i] = global_router_list[i-l]
                single_path.insert(index, des_router_list[i].copy())
                index = -3
            temp = router_list[i].copy()
            while temp != des_router_list[i]:
                if temp in jointed_router:
                    mark = 0
                    break
                else:
                    single_path.insert(index, temp.copy())
                    temp = routing(temp, des_router_list[i], l, m)
            if mark:
                head = 0
                tail = len(single_path)
                for label in range(len(single_path)):
                    if single_path[label] == d and label != len(single_path)-1:
                        tail = label+1
                    if single_path[label] == s and label != 0:
                        head = label
                single_path = single_path[head:tail]
                total_path.append(single_path.copy())
                jointed_router.extend(single_path[1:-1])
    total_path = sort_length(total_path)
    if total_path[0] == total_path[1]:
        total_path = total_path[1:]
    return total_path


if __name__ == "__main__":
    K = 3     # number of nodes for each router
    M = 4      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 2       # number of global links for each router

    res = path(M, N, L, [5, 0], [1, 3])
    for i in res:
        print(i)


