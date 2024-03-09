
import os
LOG_DIR = '/work/netem/logs'
TEST_BASE = 'base'
test_name_list =[TEST_BASE]
def gen_traffic(h1,h4,test_name,duration):
    create_directory()

    if test_name == TEST_BASE:
        _test_base(h1,h4,duration)


def _test_base(h1,h4,duration):
    protocol = 'quic_rl'
    print(f'start {TEST_BASE} test...')
    h4.cmd(f'/work/netem/bin/qperf-go server --port=8080 --redis 127.0.0.1:6379 --cc rl &> {LOG_DIR}/{TEST_BASE}/{protocol}_h4.txt &')
    h1.cmd(f'/work/netem/bin/qperf-go client --log-prefix {TEST_BASE} --addr="{h4.IP()}:8080" --t={duration} &> {LOG_DIR}/{TEST_BASE}/{protocol}_h1.txt &')

def create_directory():
    """
    Create a directory if it does not exist.

    Args:
        directory_path (str): The path to the directory to create.
    """

    for name in test_name_list:
        directory_path = LOG_DIR+'/'+name
        if not os.path.exists(directory_path):
            os.makedirs(directory_path) 