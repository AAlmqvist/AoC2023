import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

DEBUG = False

def parse_data(s):
    info = s.split(' -> ')
    mod, vals = info[0], info[1].split(', ')
    return mod, vals

def fix_modules(data):
    # new_data = []
    mods = dict()
    for name, vals in data:
        # Flip flop, start off
        if name[0] == '%':
            # new_data.append((name[1:], 0, (0, vals)))
            mods[name[1:]] = (0, 0, vals)
            continue
        # Conjunction
        if name[0] == '&':
            # new_data.append((name[1:], 1, (0, vals)))
            mods[name[1:]] = (1, dict(), vals)
            continue
        mods[name] = (2, 0, vals)

    # Map all conjunctions input to 0
    for name, vals in data:
        for val in vals:
            if val not in mods.keys():
                mods[val] = (-1, 0, [])
            if mods[val][0] == 1:
                if name == 'broadcaster':
                    mods[val][1][name] = 0
                else:
                    mods[val][1][name[1:]] = 0
    return mods

def broadcast(mods, check=None, click_number=0):
    # One low is sent to broadcaster
    n_low, n_high = 1, 0
    curr = []
    for o in mods['broadcaster'][2]:
        n_low += 1
        curr.append(('broadcaster', o, 0))
    while curr:
        next_iter = []
        if DEBUG:
            print("------------------")
        for m_from, m_to, pulse in curr:
            m_type, m_cache, outputs = mods[m_to]
            if check != None:
                if (m_from, pulse) in check:
                    if len(check[(m_from, pulse)]) < 8:
                        check[(m_from, pulse)].append(click_number)
            if m_type < 0:
                continue
            # conjunction
            if m_type == 1:
                m_cache[m_from] = pulse
                # If all are high, send low
                if sum([v for _, v in m_cache.items()]) == len(m_cache.keys()):
                    n_low += len(outputs)
                    for o in outputs:
                        if DEBUG:
                            print(m_to, 0, '->', o)
                        next_iter.append((m_to, o, 0))
                # Else send high
                else:
                    n_high += len(outputs)
                    for o in outputs:
                        if DEBUG:
                            print(m_to, 1, '->', o)
                        next_iter.append((m_to, o, 1))
                # update tuple in outer dict
                mods[m_to] = (m_type, m_cache, outputs)
                continue

            # flip-flop, ignore high pulses
            if pulse == 1:
                continue

            # turn on/off
            m_cache = (m_cache + 1) % 2

            if m_cache == 1:
                n_high += len(outputs)
            else:
                n_low += len(outputs)
            for o in outputs:
                if DEBUG:
                    print(m_to, m_cache, '->', o)
                next_iter.append((m_to, o, m_cache))
            mods[m_to] = (m_type, m_cache, outputs)
        curr = next_iter
    return mods, n_low, n_high

def click_button(mods, times):
    tot_low, tot_high = 0, 0
    for _ in range(times):
        mods, n_low, n_high = broadcast(mods)
        tot_low += n_low
        tot_high += n_high

    return tot_low*tot_high

def click_until_period(mods, from_check):
    i = 1
    cont = True
    while cont:
        cont = False
        mods, _, _ = broadcast(mods, check=from_check, click_number=i)
        for _, v in from_check.items():
            if len(v) < 8:
                cont = True
        i += 1
    return from_check

def run():
    data = read_by_line('input.txt', parse_func=parse_data)
    mods = fix_modules(data)
    
    p1 = click_button(mods, 1000)
    print(p1)

    # Reset modules by parsing the input again
    mods = fix_modules(data)

    # Printed the last module before 'rx' and saw it was a conjunction.
    # Thought I'd see a pattern if I printed each time they fired a high pulse,
    # which turned out to be correct.
    last_conj = [k for k, v in mods.items() if 'rx' in v[2]][0]
    input_last_conj = mods[last_conj][1]
    periodicity_check = dict()
    for inp in input_last_conj:
        periodicity_check[(inp, 1)] = []

    # Keep clicking until we find a perdiod for all inputs to the last conjunction
    inp_check = click_until_period(mods, periodicity_check)
    LCM = 1
    # Saw that they we're all even periods, so I figured it would be good to try with the LCM
    for k, v in inp_check.items():
        diffs = [v[i+1]-v[i] for i in range(len(v)-1)]
        diff = diffs[0]
        if [1 for x in diffs if x != diff]:
            print("Non-even periodicity for", k)
            return
        LCM *= diffs[0]
    # And the LCM was the correct answer
    print(LCM)

if __name__ == "__main__":
    run()