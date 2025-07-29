use serde::Serialize;
use starknet_api::data_availability::DataAvailabilityMode;
use starknet_api::transaction::fields::Tip;
use starknet_types_core::felt::Felt;

use super::ResourceBoundsWrapper;
use super::broadcasted_declare_transaction_v3::BroadcastedDeclareTransactionV3;
use crate::contract_address::ContractAddress;
use crate::felt::{ClassHash, CompiledClassHash, Nonce, TransactionSignature, TransactionVersion};

#[derive(Debug, Clone, Serialize)]
#[cfg_attr(
    feature = "testing",
    derive(serde::Deserialize, PartialEq, Eq),
    serde(deny_unknown_fields)
)]
pub struct DeclareTransactionV3 {
    pub(crate) version: TransactionVersion,
    pub(crate) signature: TransactionSignature,
    pub(crate) nonce: Nonce,
    pub(crate) resource_bounds: ResourceBoundsWrapper,
    pub(crate) tip: Tip,
    pub(crate) paymaster_data: Vec<Felt>,
    pub(crate) nonce_data_availability_mode: DataAvailabilityMode,
    pub(crate) fee_data_availability_mode: DataAvailabilityMode,
    pub(crate) sender_address: ContractAddress,
    pub(crate) compiled_class_hash: CompiledClassHash,
    pub(crate) class_hash: ClassHash,
    pub(crate) account_deployment_data: Vec<Felt>,
}

impl DeclareTransactionV3 {
    pub fn new(broadcasted_txn: &BroadcastedDeclareTransactionV3, class_hash: ClassHash) -> Self {
        Self {
            version: broadcasted_txn.common.version,
            signature: broadcasted_txn.common.signature.clone(),
            nonce: broadcasted_txn.common.nonce,
            resource_bounds: broadcasted_txn.common.resource_bounds.clone(),
            tip: broadcasted_txn.common.tip,
            paymaster_data: broadcasted_txn.common.paymaster_data.clone(),
            nonce_data_availability_mode: broadcasted_txn.common.nonce_data_availability_mode,
            fee_data_availability_mode: broadcasted_txn.common.fee_data_availability_mode,
            sender_address: broadcasted_txn.sender_address,
            account_deployment_data: broadcasted_txn.account_deployment_data.clone(),
            compiled_class_hash: broadcasted_txn.compiled_class_hash,
            class_hash,
        }
    }

    pub fn get_class_hash(&self) -> &ClassHash {
        &self.class_hash
    }

    pub(crate) fn get_resource_bounds(&self) -> &ResourceBoundsWrapper {
        &self.resource_bounds
    }
}
