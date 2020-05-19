const owner : address = ("tz1cA4AkQgrNfLL9q9Wx986r4Sx7o6H1kSou" : address);

type storage is record [
  enabled : bool;
  y : nat;
  n : nat;
  voters : set(address);
  result : string;
  
]

type parameter is
| Reset of unit
| Stdby of string
| Vote of nat



type return is list (operation) * storage

// add_voter : add sender to voters set
function add_voter (const store : storage) : storage is 
block { 
  store.voters := Set.add (sender, store.voters)
   } with store

// count : count vote in pool
function count(const store : storage; const vote : nat) : storage is
block {
  if vote = 1n
    then store.y := store.y + 1n
  else if vote = 2n then
    store.n := store.n + 1n
  else skip;
} with store

// break : disable or enable vote, Only enable for the contract owner
function break (const stat : string; const store : storage) : storage is
 block { 
   if sender =/= owner
   then failwith("Access denied.")
   else if sender = owner and stat = "True"
      then 
        if stat = "True" then
          store.enabled := True
        else if stat = "False" then 
          store.enabled := False
        else skip;
    else skip;
    } with store

function vote (const vote : nat; const store : storage) : storage is
block {
  
    if sender = owner or store.voters contains sender or store.enabled = False
      then failwith ("Access denied.")
    else skip;
    
    // define a const who takes the numbers of input inside the set of voters then 
    // check if it's equal to 10
    const vLimit : nat = Set.size(store.voters);
    // if the set size of voter is >= to 10 we show the winner
    if vLimit >= 10n 
      then 
        if store.y > store.n 
          then failwith("Yes")
        else failwith("No")
    else if vLimit = 9n voters = empty_set;
      then {
        store := add_voter(store);
        if vote = 1n
          then store.y := store.y + 1n
        else if vote = 2n then
          store.n := store.n + 1n
        else skip;

        // after adding the 10th vote we get the result
        if store.y > store.n 
          then store := store with record [
              enabled = False;
              result = "Yes"
            ]
        else store := store with record [
              enabled = False;
              result = "No"
            ]
        
        // we reach 10 vote we can now block the vote
        
      } 
    else {
      store := add_voter(store);
      if vote = 1n
        then store.y := store.y + 1n
      else if vote = 2n then
        store.n := store.n + 1n
      else skip;
    }
} with storereset
   

function reset (const store : storage) : storage is
block {
    const empty_set : set (address) = Set.empty;
    // check if the owner of the contract is trying to reset -> if True then reset the value
    if sender = owner and store.enabled = False then 
        store := store with record [
          enabled = True;
          y = 0n;
          n = 0n;
          voters = empty_set;
        ]
    else failwith("Acces denied.")
  
} with store

function main (const action : parameter; const store : storage): return is
block {
  // Entrypoints
  const new_storage : storage = case action of
    | Vote (n) -> vote (n, store)
    | Reset -> reset (store)
    | Stdby (n) -> break (n, store)
  end
} with ((nil : list (operation)), new_storage)
  