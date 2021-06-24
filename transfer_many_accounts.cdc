import FungibleToken from 0xf233dcee88fe0abe
import FlowToken from 0x1654653399040a61

transaction(addressAmountMap: {Address: UFix64}) {

    // The Vault resource that holds the tokens that are being transferred
    let vaultRef: &FlowToken.Vault

    prepare(signer: AuthAccount) {

        // Get a reference to the signer's stored vault
        self.vaultRef = signer.borrow<&FlowToken.Vault>(from: /storage/flowTokenVault)
			?? panic("Could not borrow reference to the owner's Vault!")
    }

    execute {

        for address in addressAmountMap.keys {

            // Withdraw tokens from the signer's stored vault
            let sentVault <- self.vaultRef.withdraw(amount: addressAmountMap[address]!)

            // Get the recipient's public account object
            let recipient = getAccount(address)

            // Get a reference to the recipient's Receiver
            let receiverRef = recipient.getCapability(/public/flowTokenReceiver)
                .borrow<&{FungibleToken.Receiver}>()
                ?? panic("Could not borrow receiver reference to the recipient's Vault")

            // Deposit the withdrawn tokens in the recipient's receiver
            receiverRef.deposit(from: <-sentVault)

        }
    }
}
