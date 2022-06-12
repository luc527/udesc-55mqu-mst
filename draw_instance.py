from common import parse_instance, output_image
from sys import stdin
from time import time

adj = parse_instance(stdin)
output_image(f'stdin{time()}', adj, None)