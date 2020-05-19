# TP - Vote on tezos

## Compile contract

input :

```bash

ligo compile-contract vote.ligo main > contract.tz

```

## Compile

```bash

contract.ligo :

ligo compile-storage contract.ligo main 'record[status = True; y = 0n; n = 0n; voters = (Set.empty : set(address)) result = "nope"]'

```

## Dry-run sample

```bash

ligo dry-run --source="tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou" vote.ligo main 'Vote(1n)' 'record[status = True; y = 0n; n = 0n; voters = (Set.empty : set(address)); res = "nope"]'

ligo dry-run --source="tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou" vote.ligo main 'Break("True")' 'record[status = True; y = 0n; n = 0n; voters = (Set.empty : set(address)); res = "nope"]'

```

## Run tests with pytest & pyligo

Require pytest-ligo and pytest

```bash

pytest tests.py

```
