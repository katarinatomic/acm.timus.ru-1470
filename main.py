""" https://acm.timus.ru/problem.aspx?space=1&num=1470 """

import numpy as np
import itertools

ufoInfo = {}


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ValueRangeError(Error):
    """Exception raised for errors in the input."""

    def __init__(self, message='Coordinates have to be in range(0, N-1).'):
        self.message = message
        super().__init__(self.message)


def extract_coordinates(sequence):
    while len(sequence) != 1 & sequence[0] != 3:
        if sequence[0] == 1:
            x, y, z = int(sequence[1]), int(sequence[2]), int(sequence[3])
            if not (0 <= x < N) & (0 <= y < N) & (0 <= z < N):
                raise ValueRangeError(message='Coordinates have to be i range(0, N-1)')
            coordinates = [x, y, z]
            break
        elif sequence[0] == 2:
            x1, y1, z1 = int(sequence[1]), int(sequence[2]), int(sequence[3])
            x2, y2, z2 = int(sequence[4]), int(sequence[5]), int(sequence[6])

            x = make_coordinates(x1, x2)
            y = make_coordinates(y1, y2)
            z = make_coordinates(z1, z2)

            coordinates = list(itertools.product(x, y, z))  # Cartesian product
            break
    return coordinates


def make_coordinates(x1, x2):
    if not x2 >= x1:  # x1 ≤ x2
        raise ValueRangeError(message='Second value has to be bigger!')
    if x2 == x1:
        x = [x1]
    else:
        for x in range(x1, x2):
            x = np.arange(x1, x2 + 1)  # svi int od x1 do x2 ukljucujuci x2
    return x


def ufo_write(k_value, coordinates):
    if not (-20_000 <= k_value <= 20_000):
        raise ValueRangeError(message='Value of k has to be in range(-20.000, 20.000).')

    if tuple(coordinates) in ufoInfo:  # ako vec postoji
        old_value = ufoInfo.get(tuple(coordinates))
        new_value = int(old_value) + k_value
        if not new_value >= 0:
            raise ValueError('The number of UFOs in a sector cannot become negative.')
        ufoInfo[tuple(coordinates)] = new_value
    else:  # ako jos ne postoji
        ufoInfo[tuple(coordinates)] = k_value

    return ufoInfo


def ufo_sum(coordinates):
    total_sum = 0
    for i in coordinates:
        if i in ufoInfo:
            total_sum += ufoInfo.get(i)
        else:
            total_sum += 0  # inicijalan broj UFO je 0
            pass            # At the moment when Vasya starts his observations there are no UFOs in the whole space.
    return total_sum


if __name__ == '__main__':
    global N
    N = int(input())
    counter = 1
    if not 1 <= N <= 128:
        raise ValueRangeError(message='Number of sectors has to be in range(1, 128).')
    while counter < 100001:  # The number of entries does not exceed 100002. --> 100001 + prvi izvan while petlje
        counter += 1
        inputSeq = [int(x) for x in input().split()]
        if len(inputSeq) == 5 or len(inputSeq) == 7:  # duzine validnih nizova
            extracted_coordinates = extract_coordinates(inputSeq)
            m = inputSeq[0]
            if m == 1:
                k = inputSeq[4]
                dictUfo = ufo_write(k, extracted_coordinates)
                # print(dictUfo)
            elif m == 2:
                total_ufos = ufo_sum(extracted_coordinates)
                print('Total UFOs: ', total_ufos)
        elif inputSeq[0] == 3:
            print('Goodnight!')
            break
        else:
            print('Invalid input, try again!')
            pass

"""Test input:
23
1 1 1 1 3
1 1 2 1 2
1 2 1 2 2
2 1 1 1 2 2 2
1 3 3 3 2
2 2 2 2 3 3 3
3

Raise Error:
300 - izvan opsega (1,128)
1 1 1 1 2
1 1 1 1 -3 - negativni broj UFO
1 1 1 1 30000 - izvan opsega za k
1 130 1 1 1 - koordinata izvan opsega x>N
2 2 2 2 1 1 1 - x1 > x2
"""