# test_examples.py
"""
TODO: better
"""


import io
import pytest


class TestExamples:
    def test_blueprint_operands(self):
        from examples.blueprint_operands import main

        main()

    def test_filtered_train(self):
        from examples.filtered_train import main

        main()

    # def test_flip_belts(self):
    #     from examples.flip_belts import main
    #     main()

    def test_item_stack_signals(self, monkeypatch):
        from examples.item_stack_signals import main

        main()

    # def test_pumpjack_placer(self): # TODO
    #     from examples.pumpjack_placer import main
    #     main()

    # def test_rail_planner_usage(self, monkeypatch): # TODO
    #     monkeypatch.setattr("sys.stdin", io.StringIO("test"))

    #     from examples.rail_planner_usage import main
    #     result = main()

    #     assert result == """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"""

    # def test_signal_index(self):
    #     from examples.signal_index import main

    #     main()

    def test_train_configuration(self):
        from examples.train_configuration_usage import main

        main()
