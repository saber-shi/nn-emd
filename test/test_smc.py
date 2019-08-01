import datetime
import logging

import numpy as np

from nn.utils import timer
from nn.smc import Secure2PC
from crypto.sife import SIFE


t_str = str(datetime.datetime.today())
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename="../logs/" + __name__ + '-' + '-'.join(t_str.split()[:1] + t_str.split()[1].split(':')[:2]) + '.log',
    filemode='w')

logger = logging.getLogger(__name__)


def test_smc():
    logger.info('Initialize the crypto system ...')
    tpa_config_file = '../config/sife_v25_b8.json'  # indicate kernel size 5
    client_config_file = '../config/sife_v25_b8_dlog.json'
    with timer('Load sife config file, cost time', logger) as t:
        sife = SIFE(tpa_config=tpa_config_file, client_config=client_config_file)
    smc = Secure2PC(crypto=sife, vec_len=25, precision=3)

    x = np.array(
        [[
            [0.,          0.,          0.,         0.,          0.],
            [0.,          0.,          0.,         0.,          0.],
            [0.,          0.,         -0.41558442, -0.41558442, -0.41558442],
            [0.,          0.,         -0.41558442, -0.41558442, -0.41558442],
            [0.,          0.,         -0.41558442, -0.41558442, -0.41558442],
        ]])

    y = np.array(
        [[
            [0.25199915, - 0.27933214, - 0.25121472, - 0.01450092, - 0.39264217],
            [-0.13325853,  0.02372098, - 0.1099066,   0.07761139, - 0.14452457],
            [0.18324971,  0.07725119, - 0.05726616,  0.18969544,  0.0127556],
            [-0.08113805,  0.19654118, - 0.37077826, 0.20517105, - 0.35461632],
            [-0.0618344, - 0.07832903, - 0.02575814, - 0.20281196, - 0.31189417]
        ]]
    )

    ct = smc.cnn_client_execute(x)
    sk = smc.cnn_server_key_request(y)
    dec = smc.cnn_server_execute(sk, ct, y)
    print(dec)
    print(np.sum(x * y))
