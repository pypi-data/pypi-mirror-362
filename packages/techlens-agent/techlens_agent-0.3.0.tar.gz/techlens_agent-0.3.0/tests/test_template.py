import os
from unittest.mock import patch
from pathlib import Path
import shutil

from techlens_agent.agent import Agent
from techlens_agent.config import Config
from techlens_agent.utils.utils import DebugLog

file_path = Path(__file__)
test_folder = file_path.parent.absolute()
results_dir = test_folder.joinpath("results").absolute()
str_path = str(test_folder.joinpath("str_conf.yaml").absolute())


@patch("techlens_agent.user.__get_input__", return_value="y")
def test_no_config(self):
    try:
        shutil.rmtree(results_dir)
    except Exception as e:
        print(e)
        pass
    os.makedirs(results_dir, exist_ok=True)
    agent = Agent()
    config = Config(str_path)
    config.output_dir = results_dir
    print(agent.config.output_dir)
    agent.config = config
    assert agent.config.use_uuid is True
    agent.config.shouldUpload = True
    agent.debug = DebugLog(path=agent.config.output_dir, debug=False)
    agent.log = agent.debug.log
    print(agent.debug.file)
    agent.scan()
    assert Path(results_dir).exists()
    assert results_dir.joinpath("results.html").exists()
