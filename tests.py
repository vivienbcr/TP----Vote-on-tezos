from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

# run this test with :
# pytest test.py


class TestContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.test = ContractInterface.create_from(
            join(project_dir, 'src/contract.tz'))

    def test_vote_yes(self):
        u = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        res = 1
        result = self.test.vote(
            1
        ).result(
            storage={
                "enabled": True,
                "y": 0,
                "n": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["y"])

    def test_vote_no(self):
        u = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        res = 1
        result = self.test.vote(
            2
        ).result(
            storage={
                "enabled": True,
                "y": 0,
                "n": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["n"])

    def test_vote_owner_deny(self):
        owner = "tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(
                1
            ).result(
                storage={
                    "enabled": True,
                    "y": 0,
                    "n": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_vote_contract_not_enabled(self):
        u = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(
                1
            ).result(
                storage={
                    "enabled": False,
                    "y": 0,
                    "n": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_reset_valid(self):
        owner = "tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou"
        result = self.test.reset(42).result(
            storage={
                "enabled": False,
                "y": 4,
                "n": 6,
                "voters": set()
            },
            sender = owner
        )
        self.assertEqual(0, result.storage["y"])

    def test_reset_active_contract(self):
        owner = "tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.reset(42).result(
                storage={
                    "enabled": True,
                    "y": 0,
                    "n": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_reset_restrict_access(self):
        u = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.reset(42).result(
                storage={
                    "enabled": False,
                    "y": 0,
                    "n": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_stdby_owner_set_disable(self):
        owner = "tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou"
        res = False
        result = self.test.stdby("False").result(
                storage={
                    "enabled":True,
                    "y":0,
                    "n":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["enabled"])
    
    def test_stdby_owner_set_enabled(self):
        owner = "tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou"
        res = True
        result = self.test.stdby("True").result(
                storage={
                    "enabled":False,
                    "y":0,
                    "n":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["enabled"])

    def test_stdby_user_set_enabled(self):
        u = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.stdby("True").result(
                storage={
                    "enabled": False,
                    "y": 0,
                    "n": 0,
                    "voters": set()
                },
                sender = u
            )

