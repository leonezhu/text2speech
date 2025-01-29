import unittest
from pathlib import Path
from kokoro_onnx import Kokoro

from audiblez import VOICES_FILE, MODEL_FILE, main


class MainTest(unittest.TestCase):
    def base(self, **kwargs):
        base_path = Path(__file__).parent / '..'
        kokoro = Kokoro(base_path / MODEL_FILE, base_path / VOICES_FILE)
        main(kokoro, lang='en-gb', voice='af_sky', providers=None, pick_manually=False, speed=1, **kwargs)

    def test_1_mini(self):
        Path('mini.m4b').unlink(missing_ok=True)
        self.base(file_path='../epub/mini.epub')
        self.assertTrue(Path('mini.m4b').exists())

    def test_2_allan_poe(self):
        Path('poe.m4b').unlink(missing_ok=True)
        self.base(file_path='../epub/poe.epub')
        self.assertTrue(Path('poe.m4b').exists())

    def test_3_gene(self):
        Path('gene.m4b').unlink(missing_ok=True)
        self.base(file_path='../epub/gene.epub')
        self.assertTrue(Path('gene.m4b').exists())

