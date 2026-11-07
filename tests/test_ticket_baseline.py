"""PQ11-001: all shipped missions, real worker effects, wrong submissions and replay."""
import os,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_flight import Game,ROOT,checked,pg
from python_quest_2d.core.challenges import LESSONS
from python_quest_2d.ui.terminal import Terminal

class ProtectedBaseline(unittest.TestCase):
    def test_all_76_worker_effects_and_replays(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ['PYTHONQUEST_SAVE']=str(Path(tmp)/'baseline.json')
            g=Game()
            try:
                self.assertEqual(len(LESSONS),76)
                for mission,ch in sorted(LESSONS.items()):
                    with self.subTest(mission=mission):
                        g.world.enter(ch['zone']);g.refresh()
                        g.term=Terminal(ch,g.p);g.scene='terminal'
                        previous=g.p['player']['xp'];completed=list(g.p['completed'])
                        wrong='raise RuntimeError("intentional baseline rejection")'
                        checked(g,wrong)
                        self.assertEqual(g.p['player']['xp'],previous)
                        self.assertEqual(g.p['completed'],completed)
                        self.assertEqual(g.p['drafts'][mission],wrong)
                        code=(ROOT/'content/authoring'/(mission+'.py')).read_text(encoding='utf8')
                        for replay in (False,True):
                            if g.term is None:g.term=Terminal(ch,g.p)
                            g.scene='terminal';checked(g,code);g.leave_terminal()
                            for _ in range(1000):
                                if not (g.p.get('deployment') or g.p.get('expedition_job')):break
                                g.update_field(.1)
                            self.assertIn(mission,g.p['completed'])
                            self.assertEqual(g.p['player']['xp'],previous+100)
                        self.assertFalse(g.p.get('deployment') or g.p.get('expedition_job'))
                self.assertEqual(g.p['player']['xp'],7600)
                self.assertEqual(set(g.p['completed']),set(LESSONS))
            finally:g.pool.shutdown()

if __name__=='__main__':unittest.main(verbosity=2)

