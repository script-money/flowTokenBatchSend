// This script reads the balance field of an account's FlowToken Balance

import FungibleToken from 0xf233dcee88fe0abe
import FlowToken from 0x1654653399040a61

pub fun main(account: Address): UFix64 {
    let acct = getAccount(account)
    let vaultRef = acct.getCapability(/public/flowTokenBalance)
        .borrow<&FlowToken.Vault{FungibleToken.Balance}>()
        ?? panic("Could not borrow Balance reference to the Vault")

    return vaultRef.balance
}