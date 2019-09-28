def segment_overlap(a, b):
    if b['start'] > a['end']:
        return False

    if b['end'] < a['start']:
        return False

    return True


def chromosome_overlap(a, b):
    sorted_a = sorted(a, key=lambda x: x['start'])
    sorted_b = sorted(b, key=lambda x: x['start'])

    cur_a = sorted_a.pop(0)
    cur_b = sorted_b.pop(0)

    while True:
        if segment_overlap(cur_a, cur_b):
            return True

        if len(sorted_a) <= 0 or len(sorted_b) <= 0:
            return False

        if cur_a['start'] > cur_b['end']:
            cur_b = sorted_b.pop(0)
        else:
            cur_a = sorted_a.pop(0)

    return False


def match_overlap(a, b):

    sorted_a = sorted(a, key=lambda x: x['chromosome'])
    sorted_b = sorted(b, key=lambda x: x['chromosome'])

    cur_a = sorted_a.pop(0)
    cur_b = sorted_b.pop(0)

    while True:
        if cur_a['chromosome'] == cur_b['chromosome']:
            if chromosome_overlap(cur_a['segments'], cur_b['segments']):
                return True

        if len(sorted_a) <= 0 or len(sorted_b) <= 0:
            return False

        if cur_a['chromosome'] > cur_b['chromosome']:
            cur_b = sorted_b.pop(0)
        else:
            cur_a = sorted_a.pop(0)

    return False
