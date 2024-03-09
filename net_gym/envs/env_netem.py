import gymnasium as gym
from gymnasium import spaces
import numpy as np
import logging
import envs.mq as mq
import time
from mininet.topo import Topo

from mininet.net import Mininet
from mininet.link import TCLink
import envs.traffic as traffic

log = logging.getLogger(__name__)


STATS_DICT = {"cwnd": 0, "rtt":1}
def my_rewards(obs,action):
    return 1
class DumbbellTopo(Topo):
    "Dumbbell Topology"
    def build(self): 
        leftSwitch = self.addSwitch('s1')
        rightSwitch = self.addSwitch('s2')

        leftHost1 = self.addHost('h1')
        leftHost2 = self.addHost('h2')
        rightHost1 = self.addHost('h3')
        rightHost2 = self.addHost('h4')

        self.addLink(leftHost1, leftSwitch)
        self.addLink(leftHost2, leftSwitch)
        self.addLink(rightHost1, rightSwitch)
        self.addLink(rightHost2, rightSwitch)
        self.addLink(leftSwitch, rightSwitch,
                     bw=10,
                     loss=0,
                     delay=10)

class NetEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self,connection_id,test_name='base',duration=10):
        # 定义 observation_space
        low = [0, 0]  # 观测空间的最小值，[最小的 cwnd 值, 最小的 rtt 值]
        high = [100, 1000]  # 观测空间的最大值，[最大的 cwnd 值, 最大的 rtt 值]
        self.observation_space = spaces.Box(low=np.array(low), high=np.array(high), dtype=np.int32)
        self.action_space = spaces.Discrete(5)
        self.connection_id = connection_id

        # 开启状态监听
        self.test_name = test_name
        self.duration = duration

         # 初始化 Mininet 网络
        self.net = Mininet(topo=DumbbellTopo(), link=TCLink)
      
    def _get_obs(self):
        print('into _get_obs')
        # obs = None
        # fin = False
        # while not fin and not obs:
        #     obs,fin = self.mq_client.read_state()
        #     if obs:
        #         print('obs:',obs)
        #     # else:
        #     #     print('waiting obs')
        #     time.sleep(0.01)
            
        obs,fin = self.mq_client.read_state()
        return obs,fin


    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        
        # 重置网络
        self.net.stop()
        self.net = Mininet(topo=DumbbellTopo(), link=TCLink)
        self.net.start()

        # 获取主机对象
        self.h1 = self.net.get('h1')
        self.h4 = self.net.get('h4')

        redis_port = 6379
        self.h4.cmd(f'/usr/bin/redis-server --port {redis_port} &> logs/redis.log &')
        self.mq_client= mq.QuicMqManager(self.connection_id,port=redis_port)

        # 生成流量
        traffic.gen_traffic(self.h1,self.h4,self.test_name,self.duration)

        observation,_ = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        self.mq_client.pub_action(action)
        observation,fin = self._get_obs()
        terminated = fin
        info = self._get_info()

        # cal reward
        reward = my_rewards(observation,action)

        return observation, reward, terminated, False, info

    def close(self):
        pass