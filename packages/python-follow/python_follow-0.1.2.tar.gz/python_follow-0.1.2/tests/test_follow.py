import threading
import time
import unittest

from follow import follow, FollowConfig


class TestFollowDecorator(unittest.TestCase):
    def setUp(self):
        self.traces = []

    def collector(self, data):
        self.traces.append(data)

    def test_basic_trace(self):
        config = FollowConfig(
            follow_threads=False,
            follow_for_loops=True,
            follow_variable_set=True,
            follow_prints=True
        )

        @follow(config=config, follower=self.collector)
        def simple_func():
            x = 10
            for i in range(2):
                y = i
                print(y)
            return x

        result = simple_func()

        # Check function result is unchanged
        self.assertEqual(result, 10)

        # Should trace 'x =' assignment
        instructions = [t['instruction'] for t in self.traces]
        self.assertTrue(any('x =' in instr for instr in instructions))

        # Should trace 'for ' loop
        self.assertTrue(any(instr.startswith('for ') for instr in instructions))

        # Should trace 'print'
        self.assertTrue(any(instr.startswith('print') for instr in instructions))

        # Should include local_vars list
        for trace in self.traces:
            self.assertIn('local_vars', trace)
            self.assertIsInstance(trace['local_vars'], list)

    def test_config_disables_tracing(self):
        config = FollowConfig(
            follow_for_loops=False,
            follow_variable_set=False,
            follow_prints=False
        )

        @follow(config=config, follower=self.collector)
        def simple_func():
            x = 5
            for i in range(1):
                print(i)
            return x

        result = simple_func()
        self.assertEqual(result, 5)

        # All traced instructions should NOT include for/assignment/print
        instructions = [t['instruction'] for t in self.traces]
        self.assertTrue(all('for ' not in instr for instr in instructions))
        self.assertTrue(all('=' not in instr for instr in instructions))
        self.assertTrue(all(not instr.startswith('print') for instr in instructions))

    def test_follow_threads(self):
        config = FollowConfig(
            follow_threads=True
        )

        @follow(config=config, follower=self.collector)
        def threaded_func():
            def worker():
                a = 0
                for i in range(5):  # 5 lines traced
                    a += i
                    time.sleep(0.05)  # Slow down to guarantee tracing
                return a

            t = threading.Thread(target=worker)
            t.start()
            t.join()

        threaded_func()

        instructions = [t['instruction'] for t in self.traces]
        print("INSTRUCTIONS:", instructions)
        self.assertTrue(any('a =' in instr or 'a +=' in instr for instr in instructions))

    def test_return_value_trace(self):
        config = FollowConfig(
            follow_return=True
        )

        @follow(config=config, follower=self.collector)
        def add(a, b):
            result = a + b
            return result

        value = add(2, 3)
        self.assertEqual(value, 5)

        # The last trace should have the return line
        instructions = [t['instruction'] for t in self.traces]
        self.assertIn('result =', ' '.join(instructions))
