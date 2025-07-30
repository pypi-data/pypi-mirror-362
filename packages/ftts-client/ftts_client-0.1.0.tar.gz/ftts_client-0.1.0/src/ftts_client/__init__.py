import requests
from pathlib import Path
from typing import Dict, List
from loguru import logger


class TTSClient:
    def __init__(self, base_url: str, headers: Dict = None):
        super().__init__()
        self.base_url = base_url
        self.headers = headers

    def list_speakers(self) -> List[str]:
        url = self.base_url + "/audio_roles"
        res = requests.get(url=url, headers=self.headers)
        if res.status_code != 200:
            logger.error(
                f"获取音色列表失败, 状态码: {res.status_code}, 响应: {res.text}"
            )
            return []
        return res.json()["roles"]

    def delete_speaker(self, speaker: str):
        url = self.base_url + "/delete_speaker"
        data = {"name": speaker}
        res = requests.post(url=url, data=data, headers=self.headers)
        return res.json()

    def add_speaker(
        self, audio_path: str | Path, speaker_name: str | None = None
    ) -> None:
        url = self.base_url + "/add_speaker"
        audio_path = Path(audio_path)
        audio_format = audio_path.suffix
        if not speaker_name:
            speaker_name = audio_path.stem
        files = {
            "audio_file": (audio_path, open(audio_path, "rb"), f"audio/{audio_format}")
        }
        data = {"name": speaker_name, "audio_file": str(audio_path)}
        res = requests.post(url=url, data=data, files=files, headers=self.headers)
        if res.status_code != 200:
            logger.error(f"上传音色失败, 状态码: {res.status_code}, 响应: {res.text}")
        logger.info(f"上传音色成功, 音色名称: {speaker_name}")
